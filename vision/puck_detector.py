"""puck_detector.py — HSV-based red puck tracker.

Replaces gestures.py / MediaPipe for point placement.
Tracks the largest red-coloured blob in the camera frame using HSV
thresholding.  Holding the puck still for DWELL_PLACE seconds fires
a 'place_point' action — same trigger that the index-finger dwell used.

Red wraps around the H=0/180 boundary in OpenCV HSV, so two masks are
combined:
    lower  H  0–10   S 100–255  V  50–255
    upper  H 165–180 S 100–255  V  50–255

Output dict  (identical keys to GestureDetector.process() for drop-in use)
    gesture         'puck' | 'none'
    dwell           float  — seconds puck has been stable at current position
    actions         list   — ['place_point'] fires once; resets when puck moves
    index_tip_cam   (x, y) puck centre in camera pixels, or None
    landmarks       None   — no hand skeleton

Tune HSV_LOWER / HSV_UPPER and MIN_AREA to match your lighting and puck.
"""

from __future__ import annotations

import time
import cv2
import numpy as np

# ── HSV colour ranges for red ──────────────────────────────────────────────────
# Adjust S/V floors if detections are noisy under your lighting.
HSV_LOWER_1 = np.array([  0, 100,  50], np.uint8)   # lower red band
HSV_UPPER_1 = np.array([ 10, 255, 255], np.uint8)
HSV_LOWER_2 = np.array([165, 100,  50], np.uint8)   # upper red band
HSV_UPPER_2 = np.array([180, 255, 255], np.uint8)

MIN_AREA      = 400    # px² — blobs smaller than this are ignored
STABLE_RADIUS = 25     # px  — max movement that still counts as "stable"
DWELL_PLACE   = 3.0    # s   — hold still this long to place a point
REARM_RADIUS  = 40     # px  — puck must move this far before it can fire again


class RedPuckDetector:
    """HSV red-puck tracker with dwell-based place_point triggering."""

    def __init__(self) -> None:
        self._stable_center: tuple[float, float] | None = None
        self._stable_start:  float | None               = None
        self._fired_at:      tuple[float, float] | None = None   # last fire position
        self._fired_frame:   bool                       = False  # action sent this frame

    # ── Public API (same signature as GestureDetector) ─────────────────────────

    def process(self, frame: np.ndarray) -> dict:
        """Detect red puck and compute dwell-based actions.

        Returns
        -------
        dict with keys: gesture, dwell, actions, index_tip_cam, landmarks
        """
        self._fired_frame = False
        center = _find_red_puck(frame)

        gesture       = 'puck' if center is not None else 'none'
        dwell         = 0.0
        actions: list = []

        if center is not None:
            dwell, fire = self._update_dwell(center)
            if fire:
                actions.append('place_point')
                self._fired_frame = True
        else:
            self._stable_center = None
            self._stable_start  = None

        return {
            'gesture':       gesture,
            'dwell':         dwell,
            'actions':       actions,
            'index_tip_cam': center,
            'landmarks':     None,
        }

    def draw(self, frame: np.ndarray, result: dict) -> None:
        """Overlay puck position and dwell progress onto frame."""
        center = result['index_tip_cam']
        dwell  = result['dwell']
        h, w   = frame.shape[:2]

        if center is None:
            cv2.putText(frame, 'no red puck', (10, h - 55),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (100, 100, 100), 2)
            return

        cx, cy = int(center[0]), int(center[1])

        # Outer ring — grows as dwell progresses
        progress = min(dwell / DWELL_PLACE, 1.0)
        ring_r   = int(18 + 14 * progress)
        color    = (0, int(200 * progress), 255) if not self._fired_frame else (0, 255, 80)
        cv2.circle(frame, (cx, cy), ring_r, color, 2)
        cv2.circle(frame, (cx, cy), 5,      color, -1)

        # Dwell arc (progress ring)
        if 0 < dwell < DWELL_PLACE:
            angle = int(360 * progress)
            cv2.ellipse(frame, (cx, cy), (ring_r + 4, ring_r + 4),
                        -90, 0, angle, (0, 220, 255), 2)

        label = f'puck  {dwell:.1f}s / {DWELL_PLACE:.0f}s'
        cv2.putText(frame, label, (10, h - 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 200, 255), 2)

        # Progress bar
        bar_w = int(300 * progress)
        cv2.rectangle(frame, (10, h - 38), (310, h - 18), (60, 60, 60), -1)
        cv2.rectangle(frame, (10, h - 38), (10 + bar_w, h - 18), (0, 200, 255), -1)

    def close(self) -> None:
        pass   # nothing to release

    # ── Dwell logic ────────────────────────────────────────────────────────────

    def _update_dwell(self, center: tuple[float, float]) -> tuple[float, bool]:
        """Return (dwell_seconds, should_fire)."""
        now = time.time()

        # Re-arm check: if we already fired, require the puck to move away first
        if self._fired_at is not None:
            dx = center[0] - self._fired_at[0]
            dy = center[1] - self._fired_at[1]
            if (dx*dx + dy*dy) ** 0.5 < REARM_RADIUS:
                # Still near the fire point — return the current dwell but don't fire again
                dwell = now - self._stable_start if self._stable_start else 0.0
                return dwell, False
            else:
                self._fired_at = None   # puck moved away — re-armed

        if self._stable_center is None:
            self._stable_center = center
            self._stable_start  = now
            return 0.0, False

        dx = center[0] - self._stable_center[0]
        dy = center[1] - self._stable_center[1]
        dist = (dx*dx + dy*dy) ** 0.5

        if dist > STABLE_RADIUS:
            # Puck moved — reset the dwell clock
            self._stable_center = center
            self._stable_start  = now
            return 0.0, False

        dwell = now - self._stable_start
        if dwell >= DWELL_PLACE:
            self._fired_at      = center
            self._stable_start  = now   # reset so it doesn't keep firing
            return dwell, True

        return dwell, False


# ── HSV detection ──────────────────────────────────────────────────────────────

def _find_red_puck(frame: np.ndarray) -> tuple[float, float] | None:
    """Return (cx, cy) of the largest red blob, or None if nothing found."""
    hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.bitwise_or(
        cv2.inRange(hsv, HSV_LOWER_1, HSV_UPPER_1),
        cv2.inRange(hsv, HSV_LOWER_2, HSV_UPPER_2),
    )

    # Morphological cleanup: close small holes then erode speckles
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask   = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask   = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    largest = max(contours, key=cv2.contourArea)
    if cv2.contourArea(largest) < MIN_AREA:
        return None

    M = cv2.moments(largest)
    if M['m00'] == 0:
        return None

    return float(M['m10'] / M['m00']), float(M['m01'] / M['m00'])
