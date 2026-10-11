"""Ledger tests. All numbers here are synthetic test fixtures, not experiment results."""

from __future__ import annotations

import copy
import hashlib
import math
from pathlib import Path
from typing import Any

import pytest

from kittylm.ledger import (
    REQUIRED_CI_JOBS,
    RESUME_CATEGORIES,
    RESUME_EXACT_REQUIRED,
    RESUME_GPU_MAX_ABS_DEV,
    RESUME_HARNESS,
    LedgerError,
    load_all_records,
    load_record,
    parse_record,
    render_ablation_table,
    render_record,
    resume_verdict_ok,
    write_record,
)
from tests.conftest import ROOT
from tests.fakes import fake_github_token

SHA = hashlib.sha256(b"fixture").hexdigest()
COMMIT = hashlib.sha1(b"fixture").hexdigest()  # fixture commit id, not a security use


def valid_record() -> dict[str, Any]:
    loss = 2.0
    return {
        "schema_version": 2,
        "experiment": {
            "id": "EXP-900",
            "kind": "formal",
            "name": "fixture",
            "description": "test fixture",
        },
        "repository": {"git_commit": COMMIT, "git_dirty": False},
        "environment": {
            "python": "3.12.10",
            "pytorch": "2.13.0",
            "backend": "cpu",
            "backend_version": None,
            "device": "cpu",
            "dtype": "fp32",
            "os": "test-os",
        },
        "dataset": {
            "name": "fixture-v1",
            "version": SHA,
            "manifest_sha256": SHA,
            "recipe_version": 1,
            "sources": 1,
            "documents": 3,
            "training_bytes": 4000,
            "validation_bytes": 400,
            "training_tokens": 1000,
            "validation_tokens": 100,
        },
        "tokenizer": {
            "version": "bpe-512@fixture",
            "vocab_size": 512,
            "tokenizer_sha256": SHA,
            "bytes_per_token": 4.0,
            "tokens_per_byte": 0.25,
        },
        "model": {
            "architecture": "transformer",
            "d_model": 16,
            "layers": 1,
            "heads": 2,
            "ffn_dim": 32,
            "context_length": 8,
            "parameters": {
                "total": 10000,
                "trainable": 10000,
                "embedding": 8192,
                "attention": 1024,
                "mlp": 752,
                "normalization": 32,
                "positional": 0,
                "output": 0,
                "tied_parameters": 8192,
                "non_embedding": 1808,
            },
        },
        "training": {
            "optimizer": "AdamW",
            "learning_rate": 0.001,
            "schedule": "cosine",
            "batch_size": 4,
            "gradient_accumulation": 1,
            "max_steps": 10,
            "training_steps": 10,
            "tokens_seen": 320,
            "bytes_seen": 1280,
            "precision": "fp32",
            "attention_kernel": "math",
        },
        "results": {
            "final_loss": loss,
            "final_ppl": math.exp(loss),
            "final_bpb": 0.72,
            "val_bpb_by_category": {"code": 0.7},
            "test_ppl": None,
            "tokens_per_second": 100.0,
            "samples_per_second": 1.0,
            "timing_breakdown": {"forward": {"mean_ms": 1.0, "p50_ms": 1.0, "p95_ms": 2.0}},
            "peak_vram_gb": None,
            "allocated_vram_gb": None,
            "duration_seconds": 3.5,
            "inference": None,
        },
        "reproducibility": {
            "determinism_mode": "deterministic",
            "checkpoint_resume_test": "not_run",
            "resume_evidence": None,
        },
        "ci_evidence": {
            "commit": COMMIT,
            "workflow": "Test",
            "run_id": 1,
            "event": "push",
            "jobs": {
                name: {"job_id": i + 1, "conclusion": "success"}
                for i, name in enumerate(REQUIRED_CI_JOBS)
            },
        },
        "limitations": ["synthetic fixture"],
        "notes": "",
    }


def complete_smoke_record() -> dict[str, Any]:
    """A valid completed smoke record: every D-025 section present and consistent."""
    from kittylm.ledger import SMOKE_LIMITATION

    data = valid_record()
    data["experiment"].update(id="SMOKE-GPU-001", kind="smoke")
    data["ci_evidence"] = None
    data["limitations"] = [SMOKE_LIMITATION, "tiny fixture"]
    data["training"].update(
        seed=1,
        min_learning_rate=0.0001,
        warmup_steps=1,
        weight_decay=0.0,
        beta1=0.9,
        beta2=0.95,
        adam_eps=1e-8,
        grad_clip=1.0,
        effective_batch_size=4,
        context_length=8,
        sampler="fixed_windows",
    )
    losses = [3.0 - 0.1 * i for i in range(10)]
    data["training_trace"] = {
        "steps": 10,
        "initial_loss": losses[0],
        "final_loss": losses[-1],
        "loss_trajectory": [{"step": i + 1, "loss": loss} for i, loss in enumerate(losses)],
        "loss_series_sha256": SHA,
        "max_grad_norm": 1.5,
        "max_loss_increase_ratio": 1.0,
        "mean_step_time_ms": 12.5,
        "state_checks": {"learned": True, "finite_parameters": True},
        "determinism_warnings": [],
    }
    data["gate"] = {
        "max_loss": 0.05,
        "max_ppl": 1.05,
        "min_token_match": 0.95,
        "prompt_tokens": 16,
        "context_stride": 4,
        "windows": 2,
        "final_loss": 2.0,
        "final_ppl": math.exp(2.0),
        "token_match_rate": 0.25,
        "longest_exact_prefix": 1,
        "exact_match": False,
        "scored_tokens": 99,
        "reference_tokens": 84,
        "generated_tokens": 84,
        "nonfinite": [],
        "checks": {"final_loss_below_max": False, "all_values_finite": True},
        "passed": False,
        "repeat_loss_series": "identical",
        "repeat_passed": False,
    }
    data["checkpoint"] = {
        "file": "step-00000010-0123456789abcdef.pt",
        "payload_sha256": SHA,
        "global_step": 10,
    }
    return data


def test_valid_record_parses_and_round_trips() -> None:
    record = parse_record(valid_record())
    assert record.model.parameters.total == 10000
    assert render_record(record) == render_record(record)


def mutate(path: str, value: Any) -> dict[str, Any]:
    data = copy.deepcopy(valid_record())
    node = data
    keys = path.split(".")
    for key in keys[:-1]:
        node = node[key]
    node[keys[-1]] = value
    return data


@pytest.mark.parametrize(
    ("path", "value", "problem"),
    [
        ("model.parameters.attention", 1000, "!= total"),
        ("model.parameters.non_embedding", 1, "non_embedding"),
        ("results.final_ppl", 9.0, "exp(final_loss)"),
        ("tokenizer.bytes_per_token", 3.0, "bytes_per_token"),
        ("repository.git_commit", "abc", "40-character"),
        ("dataset.version", "v1", "sha256"),
        ("experiment.id", "exp-1", "EXP-###"),
        ("reproducibility.checkpoint_resume_test", "passed", "requires resume_evidence"),
        ("limitations", [], "at least one"),
        ("notes", "ran from C:\\Users\\someone\\kittylm", "absolute path"),
        ("notes", "see /home/someone/runs", "absolute path"),
        ("results.tokens_per_second", -1.0, ">= 0"),
        ("training.precision", "int8", "expected one of"),
        ("unexpected", 1, "unknown key"),
    ],
)
def test_invalid_records_are_rejected(path: str, value: Any, problem: str) -> None:
    with pytest.raises(LedgerError) as exc:
        parse_record(mutate(path, value))
    assert problem in str(exc.value)


def full_comparison(device_type: str = "cpu", **verdicts: str) -> dict[str, str]:
    comparison = {category: "exact" for category in RESUME_CATEGORIES}
    comparison.update(verdicts)
    comparison["device_type"] = device_type
    return comparison


def resume_record(status: str, comparison: dict[str, str]) -> dict[str, Any]:
    data = mutate("reproducibility.checkpoint_resume_test", status)
    data["reproducibility"]["resume_evidence"] = {
        "harness": RESUME_HARNESS,
        "run_id": "run-1",
        "kill_step": 5,
        "resumed_to_step": 10,
        "metrics_sha256": SHA,
        "comparison": comparison,
    }
    return data


def test_resume_evidence_rules() -> None:
    data = resume_record("passed", full_comparison())
    evidence = data["reproducibility"]["resume_evidence"]
    assert parse_record(data).reproducibility.checkpoint_resume_test == "passed"

    forged = copy.deepcopy(data)
    forged["reproducibility"]["resume_evidence"]["harness"] = "typed-by-hand"
    with pytest.raises(LedgerError, match="harness"):
        parse_record(forged)

    stale = mutate("reproducibility.resume_evidence", evidence)
    with pytest.raises(LedgerError, match="must be null"):
        parse_record(stale)


@pytest.mark.parametrize("missing", RESUME_CATEGORIES)
def test_resume_comparison_must_be_complete(missing: str) -> None:
    comparison = full_comparison()
    del comparison[missing]
    for status in ("passed", "failed"):
        with pytest.raises(LedgerError, match=f"missing categories \\['{missing}'\\]"):
            parse_record(resume_record(status, comparison))


@pytest.mark.parametrize("category", RESUME_EXACT_REQUIRED["cpu"])
def test_passed_requires_every_exact_category_on_cpu(category: str) -> None:
    comparison = full_comparison(**{category: "max_abs_dev=1.000e-07"})
    with pytest.raises(LedgerError, match="not exact"):
        parse_record(resume_record("passed", comparison))
    # The same divergence is a consistent record when the status says failed.
    assert parse_record(resume_record("failed", comparison))


def test_gpu_passed_allows_measured_tensor_deviations_only() -> None:
    deviations = {
        c: "max_abs_dev=2.000e-06"
        for c in RESUME_CATEGORIES
        if c not in RESUME_EXACT_REQUIRED["cuda"]
    }
    assert set(deviations) == {"optimizer_state", "model_parameters", "loss_series"}
    assert parse_record(resume_record("passed", full_comparison("cuda", **deviations)))
    for category in RESUME_EXACT_REQUIRED["cuda"]:
        broken = full_comparison("cuda", **{category: "values differ"})
        with pytest.raises(LedgerError, match="not exact"):
            parse_record(resume_record("passed", broken))


@pytest.mark.parametrize(
    ("comparison", "status", "problem"),
    [
        (full_comparison(), "failed", "every category is within tolerance"),
        (full_comparison("rocm"), "passed", "device_type must be one of"),
        ({**full_comparison(), "vibes": "exact"}, "passed", "unknown categories"),
        ({"global_step": "exact"}, "passed", "device_type must be one of"),
        ({}, "passed", "device_type must be one of"),
    ],
)
def test_inconsistent_resume_comparisons_are_rejected(
    comparison: dict[str, str], status: str, problem: str
) -> None:
    with pytest.raises(LedgerError, match=problem):
        parse_record(resume_record(status, comparison))


def test_forbidden_identifiers_and_secrets() -> None:
    with pytest.raises(LedgerError, match="username/hostname"):
        parse_record(mutate("notes", "trained on kittybox"), forbidden_identifiers=["kittybox"])
    with pytest.raises(LedgerError, match="secret scanner"):
        parse_record(mutate("notes", f"oops {fake_github_token()}"))


def test_write_and_load_record(tmp_path: Path) -> None:
    record = parse_record(valid_record())
    path = write_record(record, tmp_path)
    assert path == tmp_path / "experiments" / "EXP-900" / "record.yaml"
    assert load_record(path) == record
    assert load_all_records(tmp_path / "experiments") == [record]


def test_record_directory_must_match_id(tmp_path: Path) -> None:
    record = parse_record(valid_record())
    wrong = tmp_path / "EXP-901" / "record.yaml"
    wrong.parent.mkdir()
    wrong.write_text(render_record(record), encoding="utf-8")
    with pytest.raises(LedgerError, match="!= experiment.id"):
        load_record(wrong)


def test_ablation_table_is_deterministic() -> None:
    a = parse_record(valid_record())
    b = parse_record(mutate("experiment.id", "EXP-100"))
    table = render_ablation_table([a, b])
    assert table == render_ablation_table([b, a])
    assert table.index("EXP-100") < table.index("EXP-900")
    assert "81.9" in table  # embedding share 8192 / 10000
    assert "No formal experiment records yet" in render_ablation_table([])


def test_committed_ablation_table_is_in_sync() -> None:
    records = load_all_records(ROOT / "experiments")
    committed = (ROOT / "experiments" / "ablations.md").read_text(encoding="utf-8")
    assert committed == render_ablation_table(records)


@pytest.mark.parametrize(
    ("verdict", "ok"),
    [
        ("exact", True),
        (f"max_abs_dev={RESUME_GPU_MAX_ABS_DEV:.3e}", True),
        ("max_abs_dev=0.000e+00", True),
        ("max_abs_dev=2.000e-04", False),
        ("max_abs_dev=inf", False),
        ("max_abs_dev=nan", False),
        ("structure differs", False),
        ("length differs (3 vs 4)", False),
        ("max_abs_dev=oops", False),
    ],
)
def test_gpu_resume_tolerance_for_tensor_categories(verdict: str, ok: bool) -> None:
    assert resume_verdict_ok("model_parameters", verdict, "cuda") is ok
    # Exact-required categories never accept a deviation, on any device.
    assert resume_verdict_ok("rng_torch", verdict, "cuda") is (verdict == "exact")
    assert resume_verdict_ok("model_parameters", verdict, "cpu") is (verdict == "exact")


def test_passed_gpu_record_beyond_tolerance_is_rejected() -> None:
    beyond = full_comparison("cuda", loss_series="max_abs_dev=5.000e-03")
    with pytest.raises(LedgerError, match="exceed the GPU tolerance"):
        parse_record(resume_record("passed", beyond))
    assert parse_record(resume_record("failed", beyond))
