"""Deterministic windowing of token streams longer than the model context (D-023).

Purpose:
    A model with context length ``C`` cannot see a stream of ``N > C + 1`` tokens at once (for
    example the 477-token smoke fixture with Nano's context of 256). This module defines the one
    policy every consumer uses, so training (SMOKE-GPU-001, EXP-000), loss, perplexity,
    bits-per-byte, greedy token matching and generation all condition each prediction on the
    *same* context. It lives in ``kittylm.data`` so training and evaluation share one
    implementation without evaluation depending on training:

    - Windows start at multiples of ``stride`` (default ``C // 2``): ``0, S, 2S, ...``.
    - A window holds up to ``C + 1`` tokens: ``C`` inputs and the ``C`` shifted targets. The last
      window may be shorter; nothing is padded and the tokenizer is never involved.
    - Each target position ``1 .. N-1`` is scored by exactly one window: the first window that
      contains it. Later windows only score targets past the previous window's end.
    - ``context_start(t)`` is the start of the window that scores target ``t``. Generation
      predicting token ``t`` uses inputs ``ids[context_start(t) : t]``, so a KV cache is reset
      and re-filled exactly where the evaluation windows begin.

Public API:
    Window(start, end, score_from)
        ``input_length``, ``scored_targets``, ``score_offset``.
    default_stride(context_length) -> int
    evaluation_windows(n_tokens, context_length, stride=None) -> list[Window]
    context_start(position, context_length, stride=None) -> int
    WindowExample(window, inputs, targets)
    window_examples(ids, context_length, stride=None) -> list[WindowExample]
        Model inputs and targets per window, with targets not scored by that window replaced by
        IGNORE_INDEX; used by the fixed-window training sampler and by stream evaluation.
    IGNORE_INDEX

Math:
    ``context_start(t) = S * max(0, ceil((t - C) / S))``. Window ``k`` starts at ``kS``, ends at
    ``min(kS + C + 1, N)`` and scores targets ``[(k-1)S + C + 1, end)`` (``[1, end)`` for k=0).

Invariants:
    - Every target position in ``[1, N)`` is scored exactly once, in increasing order.
    - For every window and every target ``t`` it scores, ``context_start(t) == window.start``
      and ``t - window.start <= C`` (the prediction sees at most ``C`` input tokens).
    - The policy depends only on ``(N, C, S)``: no randomness, no token values.
    - ``window_examples`` keeps a target only where the window scores it, so the mean
      cross-entropy over all examples (ignoring IGNORE_INDEX) is exactly the stream loss.

Failure modes:
    - ``n_tokens < 2``, ``context_length < 1``, or a stride outside ``[1, context_length]``
      raises ValueError (a larger stride would leave targets unscored).

See:
    D-023, plan rev 3.3 sections 5 and 7 (SMOKE-GPU-001 fixture vs Nano context).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

__all__ = [
    "IGNORE_INDEX",
    "Window",
    "WindowExample",
    "context_start",
    "default_stride",
    "evaluation_windows",
    "window_examples",
]

# PyTorch cross-entropy's default ignore_index: targets with this value contribute no loss.
IGNORE_INDEX = -100


@dataclass(frozen=True)
class Window:
    """Tokens ``ids[start:end]``; scores targets at absolute positions ``[score_from, end)``."""

    start: int
    end: int
    score_from: int

    @property
    def input_length(self) -> int:
        """Number of input tokens fed to the model (``end - start - 1``)."""
        return self.end - self.start - 1

    @property
    def scored_targets(self) -> int:
        """Number of targets this window contributes to the loss."""
        return self.end - self.score_from

    @property
    def score_offset(self) -> int:
        """Index into this window's target row where scoring begins."""
        return self.score_from - (self.start + 1)


def default_stride(context_length: int) -> int:
    """Half the context (at least 1): each re-used context keeps half its history."""
    if context_length < 1:
        raise ValueError("context_length must be >= 1")
    return max(1, context_length // 2)


def _resolve_stride(context_length: int, stride: int | None) -> int:
    resolved = default_stride(context_length) if stride is None else stride
    if not 1 <= resolved <= context_length:
        raise ValueError(f"stride must be in [1, {context_length}], got {resolved}")
    return resolved


def evaluation_windows(
    n_tokens: int, context_length: int, stride: int | None = None
) -> list[Window]:
    """Windows that score every target of an ``n_tokens`` stream exactly once."""
    if n_tokens < 2:
        raise ValueError("a stream needs at least 2 tokens to have a target")
    step = _resolve_stride(context_length, stride)
    windows: list[Window] = []
    start, score_from = 0, 1
    while True:
        end = min(start + context_length + 1, n_tokens)
        windows.append(Window(start=start, end=end, score_from=score_from))
        if end == n_tokens:
            return windows
        score_from = end
        start += step


def context_start(position: int, context_length: int, stride: int | None = None) -> int:
    """Start of the context used to predict the token at ``position`` (``position >= 1``)."""
    if position < 1:
        raise ValueError("position must be >= 1 (token 0 is never predicted)")
    step = _resolve_stride(context_length, stride)
    overflow = position - context_length
    return 0 if overflow <= 0 else step * -(-overflow // step)


@dataclass(frozen=True)
class WindowExample:
    """One window's model inputs and targets (unscored targets are IGNORE_INDEX)."""

    window: Window
    inputs: tuple[int, ...]
    targets: tuple[int, ...]


def window_examples(
    ids: Sequence[int], context_length: int, stride: int | None = None
) -> list[WindowExample]:
    """Inputs and masked targets for every D-023 window of ``ids``."""
    examples = []
    for window in evaluation_windows(len(ids), context_length, stride):
        chunk = [int(t) for t in ids[window.start : window.end]]
        targets = chunk[1:]
        masked = [IGNORE_INDEX] * window.score_offset + targets[window.score_offset :]
        examples.append(WindowExample(window, tuple(chunk[:-1]), tuple(masked)))
    return examples
