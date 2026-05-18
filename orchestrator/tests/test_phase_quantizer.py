"""Phase quantizer unit tests. Pure logic — no I/O, no TD."""
from __future__ import annotations

import pytest

from orchestrator.phase_quantizer import PhaseQuantizer


# ----- Quantization with n_phases=5 (masonry, default) -----

class TestQuantizationFiveSlots:
    @pytest.mark.parametrize("raw, expected_phase", [
        (0.00, 1), (0.10, 1),
        (0.20, 2), (0.30, 2),
        (0.45, 3), (0.55, 3),
        (0.70, 4), (0.80, 4),
        (0.95, 5), (1.00, 5),
    ])
    def test_quantizes_correctly(self, raw, expected_phase):
        q = PhaseQuantizer(n_phases=5)
        # Two updates with the same raw -> stabilised value
        q.update(raw, now_t=0.0)
        idx, _ = q.update(raw, now_t=0.0)
        # Allow ±1 due to hysteresis (raw=0.30 may not move from 2 to anywhere)
        assert abs(idx - expected_phase) <= 1


# ----- Quantization with n_phases=3 (3D PRINTED) -----

class TestQuantizationThreeSlots:
    @pytest.mark.parametrize("raw, expected_phase", [
        (0.00, 1), (0.10, 1),
        (0.45, 2), (0.55, 2),
        (0.90, 3), (1.00, 3),
    ])
    def test_quantizes_correctly(self, raw, expected_phase):
        q = PhaseQuantizer(n_phases=3)
        q.update(raw, now_t=0.0)
        idx, _ = q.update(raw, now_t=0.0)
        assert abs(idx - expected_phase) <= 1


# ----- Hysteresis: no oscillation at boundaries -----

class TestHysteresis:
    def test_boundary_hold_does_not_flip(self):
        """Hold the slider at a phase boundary; the index must not oscillate."""
        q = PhaseQuantizer(n_phases=5)
        # raw=0.125 is the boundary between phase 1 and 2 for n_phases=5
        q.update(0.10, now_t=0.0)         # land firmly in phase 1
        idx_initial, _ = q.update(0.10, now_t=0.001)
        # Now hover right at the boundary
        history = [q.update(0.125, now_t=0.01 * i)[0] for i in range(20)]
        # Should stay at idx_initial throughout (hysteresis keeps it)
        assert all(idx == idx_initial for idx in history), \
            f"Phase oscillated: {history}"


# ----- Manual override timer -----

class TestManualOverride:
    def test_movement_arms_override(self):
        q = PhaseQuantizer(n_phases=5, override_duration_s=10.0, override_threshold=0.05)
        q.update(0.10, now_t=0.0)
        # Move significantly
        _, wrapper = q.update(0.50, now_t=0.1)
        assert wrapper == 1

    def test_override_expires(self):
        q = PhaseQuantizer(n_phases=5, override_duration_s=10.0, override_threshold=0.05)
        q.update(0.10, now_t=0.0)
        q.update(0.50, now_t=0.1)         # arm override at t=0.1, expires t=10.1
        # Just before expiry
        _, w_before = q.update(0.50, now_t=10.0)
        assert w_before == 1
        # Just after expiry
        _, w_after = q.update(0.50, now_t=10.2)
        assert w_after == 0

    def test_small_movement_does_not_arm(self):
        q = PhaseQuantizer(n_phases=5, override_threshold=0.05)
        q.update(0.50, now_t=0.0)
        _, wrapper = q.update(0.52, now_t=0.1)         # delta = 0.02 < 0.05
        assert wrapper == 0

    def test_re_movement_restarts_timer(self):
        q = PhaseQuantizer(n_phases=5, override_duration_s=10.0, override_threshold=0.05)
        q.update(0.10, now_t=0.0)
        q.update(0.50, now_t=0.1)                       # arm; expires 10.1
        q.update(0.80, now_t=5.0)                       # re-arm; expires 15.0
        _, wrapper = q.update(0.80, now_t=12.0)        # still within new window
        assert wrapper == 1


# ----- Single-phase methods (defensive) -----

class TestDegenerateNPhases:
    def test_one_phase_method_always_returns_one(self):
        q = PhaseQuantizer(n_phases=1)
        for raw in (0.0, 0.25, 0.5, 0.75, 1.0):
            idx, _ = q.update(raw, now_t=0.0)
            assert idx == 1

    def test_reset_for_method_clears_state(self):
        q = PhaseQuantizer(n_phases=5)
        q.update(0.95, now_t=0.0)
        q.update(0.95, now_t=0.001)
        assert q._last_index == 5            # before reset

        q.reset_for_method(3)
        assert q.n_phases == 3
        assert q._last_index == 1            # back to default
