"""SMOKE-GPU-001: engineering-only proof that the training stack works end to end on a GPU.

Usage:
    python scripts/smoke_gpu.py                 # ROCm/CUDA device, canonical configuration
    python scripts/smoke_gpu.py --device cpu    # same pipeline on CPU (fp32 configuration)

The run trains a 512-token smoke tokenizer on the fixture, trains Nano on the fixture's D-023
fixed windows, checkpoints, evaluates with the shared overfit gate, repeats the training to
compare loss series, and validates a fresh-process resume. Each run that starts ends in a
terminal state recorded in experiments/SMOKE-GPU-001/record.yaml:

- ``completed``: every measurement is present and validated;
- ``failed``: the failing stage and error are recorded; no results are claimed.

Planned and running states live in runs/smoke-gpu-001/status.json (not committed). A problem
found before the run starts (bad device, batch size, config) exits without writing a record,
because no run took place.

SMOKE records are engineering-only (D-017). KittyLM makes no network requests; every input is a
local repository file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import torch

from kittylm.config import (
    ConfigError,
    apply_overrides,
    config_hash,
    from_dict,
    load_yaml,
    to_dict,
)
from kittylm.data.loader import TOKEN_DTYPE, FixedWindowSampler, open_token_file
from kittylm.data.windows import default_stride, evaluation_windows
from kittylm.evaluation.gates import (
    OverfitGateReport,
    OverfitGateThresholds,
    compare_loss_series,
    evaluate_overfit_gate,
)
from kittylm.evaluation.perplexity import token_byte_lengths
from kittylm.inference.loading import precision_dtype
from kittylm.inference.runtime import synchronize
from kittylm.ledger import (
    SMOKE_LIMITATION,
    LedgerError,
    local_identifiers,
    parse_record,
    write_record,
)
from kittylm.model.accounting import count_parameters
from kittylm.model.config import ModelConfig
from kittylm.model.transformer import KittyLM
from kittylm.tokenizer.bpe import BPETokenizer
from kittylm.tokenizer.trainer import TokenizerConfig, train_from_config
from kittylm.training.checkpoint import RunIdentity
from kittylm.training.config import TrainingConfig
from kittylm.training.determinism import seed_everything
from kittylm.training.engine import RunInfo, StepResult, TrainingEngine
from kittylm.training.resume_harness import HarnessError, HarnessSpec, validate_resume
from kittylm.utils.git import head_commit, is_dirty

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT_ID = "SMOKE-GPU-001"
MODEL_CONFIG = ROOT / "configs" / "model" / "nano.yaml"
TRAINING_CONFIG = ROOT / "configs" / "training" / "smoke-gpu-001.yaml"
TOKENIZER_CONFIG = ROOT / "configs" / "tokenizer" / "smoke.yaml"
CORPUS = ROOT / "tests" / "fixtures" / "smoke_corpus.txt"
RUN_DIR = Path("runs") / "smoke-gpu-001"
SMOKE_VOCAB_SIZE = 512  # temporary smoke vocabulary (plan rev 3.3 section 7); never used formally
RESUME_KILL_STEP = 20
RESUME_TOTAL_STEPS = 40
LOSS_POINT_EVERY = 10
LIMITATIONS = (
    SMOKE_LIMITATION,
    "Single 477-token fixture: the run measures memorization of that fixture only.",
    "Gate and training use the same D-023 windows (stride context/2).",
    "ROCm GPU runs are semi-deterministic (D-012); the repeat loss series is compared.",
    "Wall-clock and VRAM figures are measurements of one run on one machine, not benchmarks.",
)


class SetupError(RuntimeError):
    """Found before the run started; no record is written because no run took place."""


class RunFailed(RuntimeError):
    """The run started and failed; the failure record has been written."""

    def __init__(self, stage: str, error: str, record: Path) -> None:
        super().__init__(f"failed at stage {stage!r} ({error}); record: {record.name}")
        self.stage = stage
        self.record = record


def sha256_bytes(data: bytes) -> str:
    """Hex sha256 of ``data``."""
    return hashlib.sha256(data).hexdigest()


def checkpoint_payload_sha(path: Path) -> str:
    """The payload digest recorded in a checkpoint's header (D-021)."""
    header = json.loads(path.read_bytes().split(b"\n", 1)[0].decode("ascii"))
    return str(header["payload_sha256"])


def redact(text: str, roots: Sequence[Path]) -> str:
    """Strip local paths and identifiers from a message before it enters a record."""
    for root in roots:
        text = text.replace(str(root), "<repo>")
    for identifier in local_identifiers():
        text = text.replace(identifier, "<local>")
    return text[:500]


def write_status(run_dir: Path, state: str, **details: Any) -> None:
    """Atomically record the run's state (planned, running, completed or failed)."""
    run_dir.mkdir(parents=True, exist_ok=True)
    payload = {"experiment": EXPERIMENT_ID, "state": state, **details}
    tmp = run_dir / "status.json.tmp"
    tmp.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, run_dir / "status.json")


def load_model_config(overrides: Sequence[str]) -> ModelConfig:
    """Nano with optional ``key=value`` overrides (for example the smoke vocabulary)."""
    data = {k: v for k, v in load_yaml(MODEL_CONFIG).items() if k != "kind"}
    return from_dict(ModelConfig, apply_overrides(data, list(overrides)))


def load_training_config() -> TrainingConfig:
    """The canonical SMOKE-GPU-001 training configuration."""
    data = {k: v for k, v in load_yaml(TRAINING_CONFIG).items() if k != "kind"}
    return from_dict(TrainingConfig, data)


def select_device(name: str) -> torch.device:
    """Validate the requested device before anything is trained."""
    try:
        device = torch.device(name)
    except (RuntimeError, ValueError) as exc:
        raise SetupError(f"invalid device {name!r}") from exc
    if device.type not in {"cpu", "cuda"}:
        raise SetupError(f"unsupported device type {device.type!r} (use cuda or cpu)")
    if device.type == "cuda" and not torch.cuda.is_available():
        raise SetupError(f"device {name!r} requested but no CUDA/ROCm GPU is available")
    return device


def prepare_artifacts(
    run_dir: Path, model_config: ModelConfig
) -> tuple[BPETokenizer, Path, bytes, list[int]]:
    """Train the smoke tokenizer, encode the fixture and write the packed token file."""
    data = {k: v for k, v in load_yaml(TOKENIZER_CONFIG).items() if k != "kind"}
    tokenizer = train_from_config(from_dict(TokenizerConfig, data), ROOT)
    if tokenizer.vocab_size != model_config.vocab_size:
        raise SetupError(
            f"tokenizer vocab_size {tokenizer.vocab_size} != model vocab_size "
            f"{model_config.vocab_size}; pass --set vocab_size={tokenizer.vocab_size}"
        )
    run_dir.mkdir(parents=True, exist_ok=True)
    tokenizer.save(run_dir / "tokenizer.json")
    corpus = CORPUS.read_bytes()
    ids = tokenizer.encode(corpus.decode("utf-8"))
    token_file = run_dir / "tokens.bin"
    np.asarray(ids, dtype=TOKEN_DTYPE).tofile(token_file)
    return tokenizer, token_file, corpus, ids


def make_engine(
    *,
    model_config: ModelConfig,
    training: TrainingConfig,
    token_file: Path,
    device: torch.device,
    run_dir: Path,
    identity: RunIdentity,
    commit: str,
    dirty: bool,
) -> TrainingEngine:
    """A fresh engine on the fixture's D-023 windows, seeded from the training config."""
    seed_everything(training.seed)
    sampler = FixedWindowSampler(
        open_token_file(token_file), context_length=model_config.context_length
    )
    return TrainingEngine(
        model=KittyLM(model_config),
        model_config=model_config,
        training_config=training,
        sampler=sampler,
        device=device,
        run_dir=run_dir,
        identity=identity,
        run=RunInfo(
            kind="smoke",
            experiment_id=EXPERIMENT_ID,
            git_commit=commit,
            git_dirty=dirty,
        ),
    )


def check_batch_matches_windows(
    training: TrainingConfig, model_config: ModelConfig, n_tokens: int
) -> int:
    """The number of D-023 windows must equal the configured batch size (no silent reshaping)."""
    stride = default_stride(model_config.context_length)
    windows = len(evaluation_windows(n_tokens, model_config.context_length, stride))
    if windows != training.batch_size:
        raise SetupError(
            f"training batch_size {training.batch_size} must equal the {windows} D-023 windows "
            f"of the fixture at context {model_config.context_length}"
        )
    return windows


def train_timed(
    engine: TrainingEngine, steps: int, device: torch.device
) -> tuple[list[StepResult], float]:
    """Train ``steps`` optimizer steps; return applied results and synchronized wall time."""
    synchronize(device)
    started = time.perf_counter()
    results = engine.train(steps)
    synchronize(device)
    return results, time.perf_counter() - started


def loss_trace(
    results: Sequence[StepResult], wall: float, model: torch.nn.Module
) -> dict[str, Any]:
    """The training trace: trajectory, state checks and a digest of the full loss series."""
    losses = [r.loss for r in results]
    grads = [r.grad_norm for r in results]
    if len(losses) < 2:
        raise RuntimeError("training applied fewer than two optimizer steps")
    finite_losses = all(math.isfinite(x) for x in losses)
    finite_grads = all(math.isfinite(x) for x in grads)
    finite_params = all(bool(torch.isfinite(p).all()) for p in model.parameters())
    increases = [losses[i + 1] / losses[i] for i in range(len(losses) - 1) if losses[i] > 0]
    last = len(losses) - 1
    points = [
        {"step": i + 1, "loss": losses[i]}
        for i in range(len(losses))
        if i == 0 or i == last or (i + 1) % LOSS_POINT_EVERY == 0
    ]
    series = json.dumps([float(x).hex() for x in losses]).encode("ascii")
    return {
        "steps": len(losses),
        "initial_loss": losses[0],
        "final_loss": losses[-1],
        "loss_trajectory": points,
        "loss_series_sha256": sha256_bytes(series),
        "max_grad_norm": max(grads) if finite_grads else math.inf,
        "max_loss_increase_ratio": max(increases) if increases else 1.0,
        "mean_step_time_ms": 1000.0 * wall / len(losses),
        "state_checks": {
            "loss_finite": finite_losses,
            "grad_norm_finite": finite_grads,
            "parameters_finite": finite_params,
            "learned": losses[-1] < losses[0],
        },
        "determinism_warnings": [],
    }


def read_metric_records(run_dir: Path) -> list[dict[str, Any]]:
    """The engine's ``metrics.jsonl`` lines (non-finite values are kept as strings)."""
    path = run_dir / "metrics.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def gate_block(
    report: OverfitGateReport,
    thresholds: OverfitGateThresholds,
    windows: int,
    stride: int,
    repeat_series: str,
    repeat_passed: bool | None,
) -> dict[str, Any]:
    """The overfit-gate section of the record (fields mirror OverfitGateInfo)."""
    return {
        "max_loss": thresholds.max_loss,
        "max_ppl": thresholds.max_ppl,
        "min_token_match": thresholds.min_token_match,
        "prompt_tokens": thresholds.prompt_tokens,
        "context_stride": stride,
        "windows": windows,
        "final_loss": report.final_loss,
        "final_ppl": report.final_ppl,
        "token_match_rate": report.token_match_rate,
        "longest_exact_prefix": report.longest_exact_prefix,
        "exact_match": report.exact_match,
        "scored_tokens": report.scored_tokens,
        "reference_tokens": report.reference_tokens,
        "generated_tokens": report.generated_tokens,
        "nonfinite": list(report.nonfinite),
        "checks": dict(report.checks),
        "passed": report.passed,
        "repeat_loss_series": repeat_series,
        "repeat_passed": repeat_passed,
    }


@dataclass(frozen=True)
class RunContext:
    """Everything about a run that is known before training starts."""

    commit: str
    dirty: bool
    device: torch.device
    model_config: ModelConfig
    training: TrainingConfig
    tokenizer: BPETokenizer
    corpus: bytes
    ids: Sequence[int]


def base_record(
    ctx: RunContext,
    *,
    status: str,
    steps_run: int,
    notes: str,
) -> dict[str, Any]:
    """Every section that does not depend on the outcome of the run."""
    commit, dirty, device = ctx.commit, ctx.dirty, ctx.device
    model_config, training, tokenizer = ctx.model_config, ctx.training, ctx.tokenizer
    corpus, ids = ctx.corpus, ctx.ids
    corpus_sha = sha256_bytes(corpus)
    parameters = count_parameters(KittyLM(model_config)).as_dict()
    hip = getattr(torch.version, "hip", None)
    return {
        "schema_version": 2,
        "experiment": {
            "id": EXPERIMENT_ID,
            "kind": "smoke",
            "name": "smoke-gpu-001-fixture-overfit",
            "description": "Engineering proof: Nano overfits the smoke fixture on D-023 windows.",
        },
        "repository": {"git_commit": commit, "git_dirty": dirty},
        "environment": {
            "python": platform.python_version(),
            "pytorch": str(torch.__version__),
            "backend": "rocm" if hip else device.type,
            "backend_version": hip,
            "device": torch.cuda.get_device_name(device) if device.type == "cuda" else "cpu",
            "dtype": training.precision,
            "os": f"{platform.system()} {platform.release()}",
        },
        "dataset": {
            "name": "smoke-corpus-fixture",
            "version": corpus_sha,
            "manifest_sha256": corpus_sha,
            "recipe_version": 0,
            "sources": 1,
            "documents": 1,
            "training_bytes": len(corpus),
            "validation_bytes": None,
            "training_tokens": len(ids),
            "validation_tokens": None,
        },
        "tokenizer": {
            "version": "bpe-512@smoke",
            "vocab_size": tokenizer.vocab_size,
            "tokenizer_sha256": tokenizer.sha256,
            "bytes_per_token": len(corpus) / len(ids),
            "tokens_per_byte": len(ids) / len(corpus),
        },
        "model": {
            "architecture": "transformer",
            "d_model": model_config.d_model,
            "layers": model_config.n_layers,
            "heads": model_config.n_heads,
            "ffn_dim": model_config.ffn_dim,
            "context_length": model_config.context_length,
            "parameters": parameters,
        },
        "training": {
            "optimizer": "AdamW",
            "learning_rate": training.learning_rate,
            "schedule": "warmup_cosine",
            "batch_size": training.batch_size,
            "gradient_accumulation": training.gradient_accumulation,
            "max_steps": training.max_steps,
            "training_steps": steps_run,
            "tokens_seen": 0,
            "bytes_seen": 0,
            "precision": training.precision,
            "attention_kernel": model_config.attention_backend,
            "seed": training.seed,
            "min_learning_rate": training.min_learning_rate,
            "warmup_steps": training.warmup_steps,
            "weight_decay": training.weight_decay,
            "beta1": training.beta1,
            "beta2": training.beta2,
            "adam_eps": training.adam_eps,
            "grad_clip": training.grad_clip,
            "effective_batch_size": training.batch_size * training.gradient_accumulation,
            "context_length": model_config.context_length,
            "sampler": "fixed_windows",
        },
        "results": None,
        "reproducibility": {
            "determinism_mode": training.determinism,
            "checkpoint_resume_test": "not_run",
            "resume_evidence": None,
        },
        "ci_evidence": None,
        "status": status,
        "failure": None,
        "training_trace": None,
        "gate": None,
        "checkpoint": None,
        "limitations": list(LIMITATIONS),
        "notes": notes,
    }


def run_experiment(
    *,
    device_name: str = "cuda",
    repo_root: Path = ROOT,
    model_overrides: Sequence[str] = (f"vocab_size={SMOKE_VOCAB_SIZE}",),
    training: TrainingConfig | None = None,
    resume: bool = True,
    repeat: bool = True,
) -> Path:
    """Run SMOKE-GPU-001 and return the written record path.

    Raises SetupError before any run starts, and RunFailed after a recorded failure.
    """
    device = select_device(device_name)
    model_config = load_model_config(model_overrides)
    training = training or load_training_config()
    if device.type == "cpu" and training.precision != "fp32":
        raise SetupError("CPU runs use precision fp32 (bf16 is the GPU configuration)")
    commit = head_commit(ROOT)
    dirty = is_dirty(ROOT)
    run_dir = repo_root / RUN_DIR
    write_status(run_dir, "planned", device=device.type)

    try:
        tokenizer, token_file, corpus, ids_raw = prepare_artifacts(run_dir, model_config)
    except SetupError:
        raise
    except (ConfigError, ValueError, OSError) as exc:
        raise SetupError(redact(str(exc), [ROOT, repo_root])) from exc
    ids = [int(t) for t in ids_raw]
    check_batch_matches_windows(training, model_config, len(ids))

    identity = RunIdentity(
        config_hash=config_hash(
            {
                "model": to_dict(model_config),
                "training": to_dict(training),
                "sampler": "fixed_windows",
            }
        ),
        tokenizer_sha256=tokenizer.sha256,
        dataset_version=sha256_bytes(corpus),
    )
    common = RunContext(
        commit=commit,
        dirty=dirty,
        device=device,
        model_config=model_config,
        training=training,
        tokenizer=tokenizer,
        corpus=corpus,
        ids=ids,
    )
    write_status(run_dir, "running", device=device.type)
    stage = "training"
    steps_run = 0
    try:
        engine = make_engine(
            model_config=model_config,
            training=training,
            token_file=token_file,
            device=device,
            run_dir=run_dir / "train",
            identity=identity,
            commit=commit,
            dirty=dirty,
        )
        results, wall = train_timed(engine, training.max_steps, device)
        steps_run = engine.global_step
        trace = loss_trace(results, wall, engine.model)
        summary = engine.summary()

        stage = "checkpoint"
        checkpoint_path = engine.save_checkpoint()
        checkpoint = {
            "file": checkpoint_path.name,
            "payload_sha256": checkpoint_payload_sha(checkpoint_path),
            "global_step": engine.global_step,
        }
        engine.close()
        model = engine.model

        stage = "gate"
        thresholds = OverfitGateThresholds()
        autocast = precision_dtype(training.precision)
        byte_lengths = token_byte_lengths(tokenizer, ids)
        gate = evaluate_overfit_gate(
            model,
            ids,
            byte_lengths,
            device=device,
            thresholds=thresholds,
            autocast_dtype=autocast,
            metrics_records=read_metric_records(run_dir / "train"),
            grad_norms=[r.grad_norm for r in results],
        )
        stride = default_stride(model_config.context_length)
        windows = len(evaluation_windows(len(ids), model_config.context_length, stride))

        repeat_series, repeat_passed = "not_run", None
        if repeat:
            stage = "repeat"
            second = make_engine(
                model_config=model_config,
                training=training,
                token_file=token_file,
                device=device,
                run_dir=run_dir / "repeat",
                identity=identity,
                commit=commit,
                dirty=dirty,
            )
            results2, _ = train_timed(second, training.max_steps, device)
            second.close()
            repeat_series = compare_loss_series(
                [r.loss for r in results], [r.loss for r in results2]
            )
            repeat_gate = evaluate_overfit_gate(
                second.model,
                ids,
                byte_lengths,
                device=device,
                thresholds=thresholds,
                autocast_dtype=autocast,
                metrics_records=read_metric_records(run_dir / "repeat"),
                grad_norms=[r.grad_norm for r in results2],
            )
            repeat_passed = repeat_gate.passed

        resume_report = None
        if resume:
            stage = "resume"
            spec = HarnessSpec(
                run_id=EXPERIMENT_ID,
                model=to_dict(model_config),
                training=to_dict(training),
                token_file=str(token_file),
                device=device.type,
                kill_step=RESUME_KILL_STEP,
                total_steps=RESUME_TOTAL_STEPS,
                git_commit=commit,
                sampler="fixed_windows",
                stride=None,
            )
            resume_report = validate_resume(spec, run_dir / "resume")

        stage = "record"
        total_tokens = int(summary["tokens_seen"])
        bpb = gate.bits_per_byte
        data = base_record(
            common,
            status="completed",
            steps_run=steps_run,
            notes="Engineering run. Not a model-quality result.",
        )
        data["training"]["tokens_seen"] = total_tokens
        data["training"]["bytes_seen"] = round(total_tokens * len(corpus) / len(ids))
        data["results"] = {
            "final_loss": gate.final_loss,
            "final_ppl": gate.final_ppl,
            "final_bpb": bpb,
            "val_bpb_by_category": {"fixture": bpb} if bpb is not None else {},
            "test_ppl": None,
            "tokens_per_second": total_tokens / wall,
            "samples_per_second": steps_run * training.batch_size / wall,
            "timing_breakdown": summary["timing_breakdown"],
            "peak_vram_gb": summary.get("peak_vram_gb"),
            "allocated_vram_gb": None,
            "duration_seconds": wall,
            "inference": None,
        }
        data["training_trace"] = trace
        data["gate"] = gate_block(gate, thresholds, windows, stride, repeat_series, repeat_passed)
        data["checkpoint"] = checkpoint
        if resume_report is not None:
            data["reproducibility"]["checkpoint_resume_test"] = resume_report.checkpoint_resume_test
            data["reproducibility"]["resume_evidence"] = to_dict(resume_report.evidence)
        record = parse_record(data, forbidden_identifiers=local_identifiers())
        target = write_record(record, repo_root)
        write_status(run_dir, "completed", steps=steps_run, record=target.name)
        return target
    except Exception as exc:  # any failure after the run starts is recorded, never hidden
        failed = base_record(
            common,
            status="failed",
            steps_run=steps_run,
            notes="The run did not complete; no measurements are claimed.",
        )
        failed["failure"] = {
            "stage": stage,
            "error_type": type(exc).__name__,
            "message": redact(str(exc), [ROOT, repo_root]),
        }
        target = write_record(
            parse_record(failed, forbidden_identifiers=local_identifiers()), repo_root
        )
        write_status(run_dir, "failed", stage=stage, error=type(exc).__name__, record=target.name)
        raise RunFailed(stage, type(exc).__name__, target) from exc


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point; expected problems print one line and set the exit code."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--device", default="cuda", help="cuda (ROCm) or cpu")
    parser.add_argument("--no-resume", action="store_true", help="skip the resume validation")
    parser.add_argument("--no-repeat", action="store_true", help="skip the repeat run")
    args = parser.parse_args(argv)
    try:
        path = run_experiment(
            device_name=args.device, resume=not args.no_resume, repeat=not args.no_repeat
        )
    except SetupError as exc:
        print(f"setup failed: {exc}")
        return 2
    except RunFailed as exc:
        print(f"{EXPERIMENT_ID} FAILED {exc}")
        return 1
    except (ConfigError, HarnessError, LedgerError) as exc:
        print(f"{EXPERIMENT_ID} failed: {exc}")
        return 1
    print(f"{EXPERIMENT_ID} completed; record: {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
