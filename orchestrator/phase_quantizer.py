"""Slider B quantization with hysteresis + manual-override timer.

Pure logic, no I/O. Fully unit-testable.

Behavior:
- Given raw slider position 0..1 and a method's n_phases (3..5),
  output phase_index 1..n_phases.
- Hysteresis: only advance phase when raw moves past floor's half-step
  boundary plus PHASE_HYST_EPSILON. Prevents oscillation at boundaries.
- Manual-override: when slider movement > PHASE_OVERRIDE_THRESHOLD,
  start a PHASE_OVERRIDE_S countdown. While running, wrapper_state=1.
- After the timer expires, wrapper_state=0 (closed-loop CV resumes).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PhaseQuantizer:
    """Stateful per-method quantizer. One instance for Slider B, reset on method change."""

    n_phases: int = 5
    hyst_epsilon: float = 0.02
    override_threshold: float = 0.05
    override_duration_s: float = 10.0

    _last_index: int = 1
    _last_center: float = 0.0
    _last_movement_raw: float = -1.0
    _override_until_t: float = -1.0
    _initialized: bool = field(default=False, repr=False)

    def _center_for(self, idx: int) -> float:
        if self.n_phases <= 1:
            return 0.0
        return float(idx - 1) / float(self.n_phases - 1)

    def _quantize(self, raw: float) -> int:
        if self.n_phases <= 1:
            return 1
        # 1 + round(raw * (n_phases - 1))
        idx = 1 + int(round(raw * (self.n_phases - 1)))
        if idx < 1:
            idx = 1
        elif idx > self.n_phases:
            idx = self.n_phases
        return idx

    def update(self, raw: float, now_t: float) -> tuple[int, int]:
        """Return (phase_index, wrapper_state) for the given raw slider input.

        raw: float in [0,1]
        now_t: monotonic seconds (time.monotonic())
        """
        raw = max(0.0, min(1.0, float(raw)))

        # First-call seed — don't fire override on initial value
        if not self._initialized:
            self._last_movement_raw = raw
            self._last_index = self._quantize(raw)
            self._last_center = self._center_for(self._last_index)
            self._initialized = True

        # Movement detection -> arm override
        if abs(raw - self._last_movement_raw) > self.override_threshold:
            self._override_until_t = now_t + self.override_duration_s
            self._last_movement_raw = raw

        wrapper_state = 1 if now_t < self._override_until_t else 0

        # Hysteresis-gated quantization
        if self.n_phases <= 1:
            self._last_index = 1
        else:
            half_step = 1.0 / (2.0 * (self.n_phases - 1))
            if abs(raw - self._last_center) > (half_step + self.hyst_epsilon):
                new_idx = self._quantize(raw)
                if new_idx != self._last_index:
                    self._last_index = new_idx
                    self._last_center = self._center_for(new_idx)

        return self._last_index, wrapper_state

    def reset_for_method(self, n_phases: int) -> None:
        """Re-seed when active method changes (so center reflects new n_phases)."""
        self.n_phases = max(1, int(n_phases))
        self._last_index = 1
        self._last_center = self._center_for(1)
        self._initialized = False
