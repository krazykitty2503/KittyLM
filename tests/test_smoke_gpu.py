"""SMOKE-GPU-001 driver: record integrity on short CPU runs, and failure recording.

These tests run the real driver (tokenizer, engine, gate, record writer) with a temporary
repository root and a few optimizer steps. They prove the record contract, not that the model
learns; the canonical GPU run is executed separately and recorded in experiments/.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

from kittylm.ledger import load_record
from kittylm.training.config import TrainingConfig
from kittylm.training.engine import NonFiniteError, TrainingEngine
from tests.conftest import load_script

SMOKE = load_script("smoke_gpu")


def short_training(**changes: Any) -> TrainingConfig:
    base = SMOKE.load_training_config()
    values = {
        "max_steps": 6,
        "warmup_steps": 1,
        "precision": "fp32",
        "determinism": "deterministic",
        "log_every": 1,
        "timing_sync_every": 0,
        "cpu_threads": 1,
        **changes,
    }
    return replace(base, **values)


def cpu_run(tmp_path: Path, **kwargs: Any) -> Path:
    # The fixture produces 3 windows at context 256 (batch_size 3 in the canonical config).
    return SMOKE.run_experiment(
        device_name="cpu",
        repo_root=tmp_path,
        training=short_training(),
        resume=False,
        repeat=False,
        **kwargs,
    )


def test_canonical_configuration_matches_the_fixture_windows() -> None:
    training = SMOKE.load_training_config()
    model = SMOKE.load_model_config(["vocab_size=512"])
    assert training.batch_size == 3
    assert model.context_length == 256
    assert SMOKE.check_batch_matches_windows(training, model, 477) == 3


def test_batch_size_must_match_the_windows(tmp_path: Path) -> None:
    model = SMOKE.load_model_config(["vocab_size=512"])
    with pytest.raises(SMOKE.SetupError, match="must equal the 3 D-023 windows"):
        SMOKE.check_batch_matches_windows(short_training(batch_size=2), model, 477)


def test_invalid_device_is_a_setup_error_and_writes_nothing(tmp_path: Path) -> None:
    with pytest.raises(SMOKE.SetupError, match="invalid device|unsupported device"):
        SMOKE.run_experiment(device_name="meta", repo_root=tmp_path, training=short_training())
    assert not (tmp_path / "experiments").exists()


def test_bf16_on_cpu_is_refused_before_any_run(tmp_path: Path) -> None:
    with pytest.raises(SMOKE.SetupError, match="fp32"):
        SMOKE.run_experiment(
            device_name="cpu",
            repo_root=tmp_path,
            training=short_training(precision="bf16"),
            resume=False,
            repeat=False,
        )
    assert not (tmp_path / "runs").exists()


def test_short_cpu_run_produces_a_valid_completed_record(tmp_path: Path) -> None:
    path = cpu_run(tmp_path)
    assert path == tmp_path / "experiments" / "SMOKE-GPU-001" / "record.yaml"
    record = load_record(path)  # validates every section, including the D-025 invariants
    assert record.status == "completed" and record.failure is None
    assert record.experiment.kind == "smoke"
    trace = record.training_trace
    assert trace is not None and trace.steps == 6
    assert trace.loss_trajectory[0].step == 1 and trace.loss_trajectory[-1].step == 6
    assert trace.state_checks["loss_finite"] and trace.state_checks["parameters_finite"]
    gate = record.gate
    assert gate is not None and gate.windows == 3 and gate.context_stride == 128
    assert gate.repeat_loss_series == "not_run" and gate.repeat_passed is None
    assert record.checkpoint is not None and record.checkpoint.global_step == 6
    assert record.results is not None and record.results.final_loss == gate.final_loss
    assert record.reproducibility.checkpoint_resume_test == "not_run"
    text = path.read_text(encoding="utf-8")
    assert str(tmp_path) not in text  # no local paths enter the record


def test_record_contains_the_required_reproducibility_fields(tmp_path: Path) -> None:
    record = load_record(cpu_run(tmp_path))
    assert record.repository.git_commit and len(record.repository.git_commit) == 40
    assert record.dataset.version == record.dataset.manifest_sha256
    assert record.tokenizer.vocab_size == 512
    assert record.training.effective_batch_size == 3
    assert record.training.sampler == "fixed_windows"
    assert record.training.context_length == 256
    assert record.model.parameters.total > 0
    assert record.environment.pytorch and record.environment.dtype == "fp32"


def test_non_finite_training_fails_with_a_failed_record(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = TrainingEngine.train_step

    def explode(self: TrainingEngine) -> Any:
        if self.global_step == 2:
            raise NonFiniteError("non-finite loss or gradient norm at step 2 (injected)")
        return original(self)

    monkeypatch.setattr(TrainingEngine, "train_step", explode)
    with pytest.raises(SMOKE.RunFailed) as exc:
        SMOKE.run_experiment(
            device_name="cpu",
            repo_root=tmp_path,
            training=short_training(),
            resume=False,
            repeat=False,
        )
    assert exc.value.stage == "training"
    record = load_record(exc.value.record)
    assert record.status == "failed"
    assert record.results is None and record.gate is None and record.checkpoint is None
    assert record.failure is not None and record.failure.stage == "training"
    assert record.failure.error_type == "NonFiniteError"
    status = (tmp_path / "runs" / "smoke-gpu-001" / "status.json").read_text(encoding="utf-8")
    assert '"state": "failed"' in status


def test_cli_reports_setup_problems_with_exit_code_2(capsys: pytest.CaptureFixture[str]) -> None:
    assert SMOKE.main(["--device", "meta"]) == 2
    assert "setup failed" in capsys.readouterr().out
