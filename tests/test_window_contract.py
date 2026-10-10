"""One window contract for training, evaluation and the overfit gate (D-023).

The same token sequence must yield the same windows, the same model inputs, the same scored
targets and the same loss whether it is consumed by the fixed-window training sampler, by
stream evaluation (stream_nll), or by the overfit gate. A divergence here would let training
optimize a different objective from the one the gate and records report.
"""

from __future__ import annotations

import math

import pytest
import torch

from kittylm.data.loader import FixedWindowSampler
from kittylm.data.windows import IGNORE_INDEX, default_stride, evaluation_windows, window_examples
from kittylm.evaluation.gates import OverfitGateThresholds, evaluate_overfit_gate
from kittylm.evaluation.perplexity import stream_nll
from kittylm.model.transformer import KittyLM
from kittylm.training.loss import causal_lm_loss
from tests.training_helpers import TINY_MODEL

CPU = torch.device("cpu")


def fixture_ids(n: int = 477, vocab: int = 64, seed: int = 11) -> list[int]:
    generator = torch.Generator().manual_seed(seed)
    return torch.randint(0, vocab, (n,), generator=generator).tolist()


@pytest.mark.parametrize("n_tokens", [477, 100, 17])
def test_training_windows_are_the_evaluation_windows(n_tokens: int) -> None:
    context = 16
    ids = fixture_ids(n_tokens)
    sampler = FixedWindowSampler(ids, context_length=context)
    expected = evaluation_windows(n_tokens, context, default_stride(context))
    assert sampler.preview_starts() == [w.start for w in expected]
    batch = sampler.next_batch()
    assert batch.starts == [w.start for w in expected]
    assert batch.inputs.shape[0] == len(expected)


def test_model_inputs_and_masked_targets_match_window_examples() -> None:
    context = 16
    ids = fixture_ids(100)
    examples = window_examples(ids, context)
    batch = FixedWindowSampler(ids, context_length=context).next_batch()
    for row, example in enumerate(examples):
        length = len(example.inputs)
        assert batch.inputs[row, :length].tolist() == list(example.inputs)
        assert batch.targets[row, :length].tolist() == list(example.targets)
        assert batch.targets[row, length:].eq(IGNORE_INDEX).all()  # padding never scored
    scored_in_batch = int((batch.targets != IGNORE_INDEX).sum())
    assert scored_in_batch == len(ids) - 1  # every target exactly once across all windows


def test_training_loss_equals_the_evaluation_stream_loss() -> None:
    # Same weights, same tokens: the loss the trainer optimizes is the loss evaluation reports.
    torch.manual_seed(0)
    model = KittyLM(TINY_MODEL).eval()
    ids = fixture_ids(100)
    batch = FixedWindowSampler(ids, context_length=TINY_MODEL.context_length).next_batch()
    with torch.no_grad():
        train_loss = float(causal_lm_loss(model(batch.inputs), batch.targets))
    evaluation = stream_nll(model, ids, [1] * len(ids), device=CPU)
    assert evaluation.tokens == len(ids) - 1
    assert train_loss == pytest.approx(evaluation.mean_loss, rel=1e-5)


def test_gate_scores_the_same_targets_as_training() -> None:
    torch.manual_seed(0)
    model = KittyLM(TINY_MODEL).eval()
    ids = fixture_ids(100)
    report = evaluate_overfit_gate(
        model,
        ids,
        [1] * len(ids),
        device=CPU,
        thresholds=OverfitGateThresholds(prompt_tokens=16),
    )
    stride = default_stride(TINY_MODEL.context_length)
    assert report.scored_tokens == len(ids) - 1
    assert report.reference_tokens == len(ids) - 16
    expected_windows = len(evaluation_windows(len(ids), TINY_MODEL.context_length, stride))
    # 100 tokens, context 16, stride 8: starts 0, 8, ..., 88 (the last window reaches the end).
    assert expected_windows == 12
    assert math.isfinite(report.final_loss)


def test_fixed_window_sampler_refuses_a_different_stream_on_resume() -> None:
    ids = fixture_ids(100)
    state = FixedWindowSampler(ids, context_length=16).state_dict()
    other = FixedWindowSampler(fixture_ids(100, seed=99), context_length=16)
    with pytest.raises(ValueError, match="stream_sha256"):
        other.load_state_dict(state)


def test_batch_size_is_the_number_of_windows() -> None:
    ids = fixture_ids(477)
    sampler = FixedWindowSampler(ids, context_length=256)
    assert sampler.batch_size == 3  # the D-023 windows of the smoke fixture at Nano's context
    assert sampler.next_batch().n_tokens == 732  # real input positions: 256 + 256 + 220
