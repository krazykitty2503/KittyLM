"""Token-window loading: random or fixed training windows and fixed validation windows.

Purpose:
    Turn a packed token stream (one flat array of token ids, documents separated by
    ``<|endoftext|>``) into training batches. Training draws random windows so every step sees a
    different slice of the corpus; the random generator is explicit and its state is saved in
    checkpoints, so a resumed run draws exactly the batches an uninterrupted run would have
    drawn. Validation uses fixed, non-overlapping windows so every evaluation measures the same
    tokens. Overfit experiments (SMOKE-GPU-001, EXP-000) instead train on the fixed D-023 windows
    of one stream, in one fixed order, so training optimizes exactly the loss the overfit gate and
    evaluation measure.

Public API:
    TOKEN_DTYPE, open_token_file(path) -> np.memmap
    Batch(inputs, targets, starts, n_tokens)
    BatchSampler (Protocol implemented by both training samplers)
    FixedWindowSampler(tokens, context_length, stride=None, pad_id=0)
        Every step yields the same batch: all D-023 windows (kittylm/data/windows.py), padded to
        the longest window, targets outside each window's scored range set to IGNORE_INDEX.
    TrainWindowSampler(tokens, context_length, batch_size, seed)
        ``next_batch()``, ``preview_starts()`` (next batch's window starts without advancing),
        ``state_dict()`` / ``load_state_dict()``, ``batches_drawn``.
    validation_batches(tokens, context_length, batch_size, max_batches=None) -> list[Batch]

Shapes:
    ``inputs`` and ``targets`` are ``[batch_size, context_length]``; ``targets`` is ``inputs``
    shifted left by one token (each window reads ``context_length + 1`` tokens). Fixed-window
    batches are ``[number of windows, longest window input]``.

Dtype:
    Token files are ``uint16`` (vocabularies up to 65,536); batches are ``int64`` for embedding
    lookup and cross-entropy.

Device:
    Batches are built on CPU; the caller moves them to the training device. The generator is a
    CPU ``torch.Generator``, so window order is identical on CPU and GPU runs.

Math:
    Window starts are drawn uniformly from ``[0, N - context_length - 1]`` with replacement.

Invariants:
    - Same tokens, context length, batch size and seed -> same sequence of batches.
    - ``preview_starts()`` never changes the sampler state.
    - ``load_state_dict`` refuses state from a sampler with a different context length, batch
      size or token count, so a checkpoint cannot silently resume on different data (the
      fixed-window sampler also checks the stride and the sha256 of the token stream).
    - ``Batch.n_tokens`` counts real input tokens (padding excluded).
    - Fixed-window padding only follows real tokens and its targets are IGNORE_INDEX, so with a
      causal model the padded batch produces exactly the loss of the unpadded windows.

Failure modes:
    - A token stream shorter than ``context_length + 1`` raises ValueError.
    - A mismatched sampler state raises ValueError.

See:
    Plan rev 3.3 section 4, D-005 (split by document), D-012 (resume evidence).
"""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

import numpy as np
import torch

from kittylm.data.windows import IGNORE_INDEX, default_stride, window_examples

__all__ = [
    "TOKEN_DTYPE",
    "Batch",
    "BatchSampler",
    "FixedWindowSampler",
    "TrainWindowSampler",
    "open_token_file",
    "validation_batches",
]

TOKEN_DTYPE = np.uint16


def open_token_file(path: Path) -> np.ndarray:
    """Memory-map a packed ``uint16`` token file read-only."""
    return np.memmap(path, dtype=TOKEN_DTYPE, mode="r")


@dataclass(frozen=True)
class Batch:
    """One batch of input/target windows and the window start offsets that produced it."""

    inputs: torch.Tensor
    targets: torch.Tensor
    starts: list[int]
    n_tokens: int = field(default=-1)

    def __post_init__(self) -> None:
        """Default ``n_tokens`` to every input position (no padding)."""
        if self.n_tokens < 0:
            object.__setattr__(self, "n_tokens", int(self.inputs.numel()))


class BatchSampler(Protocol):
    """What the training engine needs from a sampler."""

    context_length: int
    batch_size: int
    batches_drawn: int

    def next_batch(self) -> Batch:
        """Return the next training batch and advance the sampler."""
        ...

    def preview_starts(self) -> list[int]:
        """Window starts of the next batch, without advancing the sampler."""
        ...

    def state_dict(self) -> dict[str, Any]:
        """Checkpointable sampler state."""
        ...

    def load_state_dict(self, state: dict[str, Any]) -> None:
        """Restore state saved by ``state_dict``; mismatched state must raise ValueError."""
        ...


def _windows(tokens: np.ndarray, starts: list[int], context_length: int) -> Batch:
    rows = np.stack([np.asarray(tokens[s : s + context_length + 1]) for s in starts])
    data = torch.from_numpy(rows.astype(np.int64))
    return Batch(inputs=data[:, :-1].contiguous(), targets=data[:, 1:].contiguous(), starts=starts)


class TrainWindowSampler:
    """Random training windows with a checkpointable generator."""

    def __init__(
        self, tokens: np.ndarray, *, context_length: int, batch_size: int, seed: int
    ) -> None:
        if context_length < 1 or batch_size < 1:
            raise ValueError("context_length and batch_size must be >= 1")
        if len(tokens) < context_length + 1:
            raise ValueError(
                f"token stream of {len(tokens)} tokens is shorter than context_length + 1"
            )
        self.tokens = tokens
        self.context_length = context_length
        self.batch_size = batch_size
        self.seed = seed
        self.max_start = len(tokens) - context_length - 1
        self.generator = torch.Generator().manual_seed(seed)
        self.batches_drawn = 0

    def _draw(self, generator: torch.Generator) -> list[int]:
        starts = torch.randint(0, self.max_start + 1, (self.batch_size,), generator=generator)
        return [int(s) for s in starts]

    def next_batch(self) -> Batch:
        """Draw the next random batch and advance the generator."""
        starts = self._draw(self.generator)
        self.batches_drawn += 1
        return _windows(self.tokens, starts, self.context_length)

    def preview_starts(self) -> list[int]:
        """Window starts of the next batch, without advancing the sampler."""
        clone = torch.Generator()
        clone.set_state(self.generator.get_state())
        return self._draw(clone)

    def state_dict(self) -> dict[str, Any]:
        """Checkpointable sampler state."""
        return {
            "generator": self.generator.get_state(),
            "batches_drawn": self.batches_drawn,
            "seed": self.seed,
            "context_length": self.context_length,
            "batch_size": self.batch_size,
            "num_tokens": len(self.tokens),
        }

    def load_state_dict(self, state: dict[str, Any]) -> None:
        """Restore sampler state saved by ``state_dict`` (structure must match)."""
        for key, expected in (
            ("context_length", self.context_length),
            ("batch_size", self.batch_size),
            ("num_tokens", len(self.tokens)),
        ):
            if state.get(key) != expected:
                raise ValueError(
                    f"sampler state {key}={state.get(key)!r} does not match this sampler "
                    f"({expected!r})"
                )
        self.generator.set_state(state["generator"])
        self.batches_drawn = int(state["batches_drawn"])
        self.seed = int(state["seed"])


class FixedWindowSampler:
    """All D-023 windows of one stream as a single batch, identical at every step."""

    kind = "fixed_windows"

    def __init__(
        self,
        tokens: Sequence[int] | np.ndarray,
        *,
        context_length: int,
        stride: int | None = None,
        pad_id: int = 0,
    ) -> None:
        ids = [int(t) for t in tokens]
        examples = window_examples(ids, context_length, stride)  # validates the arguments
        self.context_length = context_length
        self.stride = default_stride(context_length) if stride is None else stride
        self.num_tokens = len(ids)
        self.stream_sha256 = hashlib.sha256(np.asarray(ids, dtype=np.int64).tobytes()).hexdigest()
        self.examples = examples
        self.batch_size = len(examples)
        self.batches_drawn = 0
        width = max(len(e.inputs) for e in examples)
        inputs = torch.full((len(examples), width), pad_id, dtype=torch.long)
        targets = torch.full((len(examples), width), IGNORE_INDEX, dtype=torch.long)
        for row, example in enumerate(examples):
            length = len(example.inputs)
            inputs[row, :length] = torch.tensor(example.inputs)
            targets[row, :length] = torch.tensor(example.targets)
        self._inputs, self._targets = inputs, targets
        self._starts = [e.window.start for e in examples]
        self._n_tokens = sum(len(e.inputs) for e in examples)

    @property
    def scored_targets(self) -> int:
        """Targets contributing to the loss per batch (``num_tokens - 1``)."""
        return int((self._targets != IGNORE_INDEX).sum())

    def next_batch(self) -> Batch:
        """The fixed batch (fresh tensors each call)."""
        self.batches_drawn += 1
        return Batch(
            inputs=self._inputs.clone(),
            targets=self._targets.clone(),
            starts=list(self._starts),
            n_tokens=self._n_tokens,
        )

    def preview_starts(self) -> list[int]:
        """Window starts of the next batch (always the same)."""
        return list(self._starts)

    def state_dict(self) -> dict[str, Any]:
        """Checkpointable sampler state."""
        return {
            "kind": self.kind,
            "batches_drawn": self.batches_drawn,
            "context_length": self.context_length,
            "stride": self.stride,
            "batch_size": self.batch_size,
            "num_tokens": self.num_tokens,
            "stream_sha256": self.stream_sha256,
        }

    def load_state_dict(self, state: dict[str, Any]) -> None:
        """Restore state saved by ``state_dict`` (same stream and window policy required)."""
        for key, expected in (
            ("kind", self.kind),
            ("context_length", self.context_length),
            ("stride", self.stride),
            ("batch_size", self.batch_size),
            ("num_tokens", self.num_tokens),
            ("stream_sha256", self.stream_sha256),
        ):
            if state.get(key) != expected:
                raise ValueError(
                    f"sampler state {key}={state.get(key)!r} does not match this sampler "
                    f"({expected!r})"
                )
        self.batches_drawn = int(state["batches_drawn"])


def validation_batches(
    tokens: np.ndarray, *, context_length: int, batch_size: int, max_batches: int | None = None
) -> list[Batch]:
    """Fixed, non-overlapping validation windows.

    The trailing tokens that do not fill a whole window are dropped. The last *batch* may hold
    fewer than ``batch_size`` windows; consumers must weight losses by token count (the engine's
    ``validate`` does) so those windows are not over-weighted.
    """
    if len(tokens) < context_length + 1:
        raise ValueError("validation stream is shorter than context_length + 1")
    starts = list(range(0, len(tokens) - context_length, context_length))
    batches = [
        _windows(tokens, starts[i : i + batch_size], context_length)
        for i in range(0, len(starts), batch_size)
    ]
    return batches[:max_batches] if max_batches is not None else batches
