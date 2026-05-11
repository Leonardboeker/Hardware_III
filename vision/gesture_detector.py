"""gesture_detector.py — MediaPipe hand gesture detector for secondary interactions.

Runs alongside puck_detector.py. The puck places points; this handles
everything else: undo, reset, extrude, add_window.

Gestures and their dwell triggers
-----------------------------------
  flat_fist     hand held horizontal (palm down)  hold 2 s  → undo
  upright_fist  hand raised vertically             hold 5 s  → reset
  index_only    index finger up, rest curled       hold 3 s  → extrude
  peace         index + middle up, rest curled     hold 2 s  → add_window

Flat vs upright fist detection
--------------------------------
MediaPipe y increases downward (top = 0, bottom = 1).
We compute the angle of the wrist→middle-MCP (lm[9]) vector from horizontal:
  angle ≈ 0°   → hand is held flat / horizontal  → flat_fist
  angle ≈ 90°  → hand is raised vertically        → upright_fist
  between      → ambiguous 'fist' (no action)

Output dict  (same keys as RedPuckDetector for drop-in use in main.py)
  gesture         str   — one of the names above or 'fist' / 'none'
  dwell           float — seconds current gesture has been held
  actions         list  — fires once per trigger: 'undo'|'reset'|'extrude'|'add_window'
  index_tip_cam   (x,y) index fingertip in camera pixels, or None
  landmarks       list of 21 NormalizedLandmark objects, or None
"""

from __future__ import annotations

import math
import os
import time
import urllib.request

import cv2
import mediapipe as mp

_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hand_landmarker.task')
_MODEL_URL  = (
    'https://storage.googleapis.com/mediapipe-models/'
    'hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task'
)

_TIPS = [8, 12, 16, 20]    # index middle ring pinky tips
_PIPS = [6, 10, 14, 18]    # corresponding PIP joints

_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (0,9),(9,10),(10,11),(11,12),
    (0,13),(13,14),(14,15),(15,16),
    (0,17),(17,18),(18,19),(19,20),
    (5,9),(9,13),(13,17),
]

DWELL_UNDO    = 2.0   # s — flat fist  → undo
DWELL_RESET   = 5.0   # s — upright fist → reset
DWELL_EXTRUDE = 3.0   # s — index only → extrude
DWELL_WINDOW  = 2.0   # s — peace      → add_window

# Angle thresholds (degrees) for flat vs upright fist
_FLAT_MAX    = 35.0   # wrist-to-MCP9 angle below this = flat fist
_UPRIGHT_MIN = 50.0   # above this = upright fist


def _ensure_model() -> None:
    if not os.path.exists(_MODEL_PATH):
        print("[INFO] Downloading hand landmarker model (~8 MB) — one-time setup...")
        urllib.request.urlretrieve(_MODEL_URL, _MODEL_PATH)
        print("[INFO] Model saved.")


def _classify(lm) -> str:
    """Return gesture name from 21 NormalizedLandmark objects."""
    up = [lm[_TIPS[i]].y < lm[_PIPS[i]].y for i in range(4)]
    idx, mid, ring, pinky = up

    if not any(up):
        # All fingers curled — distinguish flat vs upright by hand orientation
        # wrist = lm[0], middle-MCP = lm[9]
        dy = lm[0].y - lm[9].y   # >0 when MCP is above wrist in image
        dx = lm[9].x - lm[0].x
        angle = abs(math.degrees(math.atan2(abs(dy), abs(dx))))
        if angle < _FLAT_MAX:
            return 'flat_fist'
        if angle > _UPRIGHT_MIN:
            return 'upright_fist'
        return 'fist'   # ambiguous — no action

    if idx and not mid and not ring and not pinky:
        return 'index_only'
    if idx and mid and not ring and not pinky:
        return 'peace'
    return 'none'


class GestureDetector:
    """Hand gesture detector using MediaPipe HandLandmarker."""

    def __init__(self) -> None:
        _ensure_model()
        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=_MODEL_PATH),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.7,
            min_tracking_confidence=0.7,
        )
        self._lm  = mp.tasks.vision.HandLandmarker.create_from_options(options)
        self._cur  = None
        self._t0   = None
        self._fired = False

    # ── Public API ─────────────────────────────────────────────────────────────

    def process(self, frame) -> dict:
        h, w = frame.shape[:2]
        now  = time.time()
        rgb  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img  = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        res  = self._lm.detect_for_video(img, int(now * 1000))

        gesture       = 'none'
        dwell         = 0.0
        actions: list = []
        index_tip_cam = None
        landmarks     = None

        if res.hand_landmarks:
            lm        = res.hand_landmarks[0]
            landmarks = lm
            gesture   = _classify(lm)
            tip        = lm[8]
            index_tip_cam = (int(tip.x * w), int(tip.y * h))

            if gesture != self._cur:
                self._cur   = gesture
                self._t0    = now
                self._fired = False
                dwell = 0.0
            else:
                dwell = now - self._t0 if self._t0 else 0.0

            if not self._fired:
                if gesture == 'flat_fist'    and dwell >= DWELL_UNDO:
                    actions.append('undo');        self._fired = True
                elif gesture == 'upright_fist' and dwell >= DWELL_RESET:
                    actions.append('reset');       self._fired = True
                elif gesture == 'index_only'   and dwell >= DWELL_EXTRUDE:
                    actions.append('extrude');     self._fired = True
                elif gesture == 'peace'        and dwell >= DWELL_WINDOW:
                    actions.append('add_window');  self._fired = True
        else:
            self._cur   = None
            self._t0    = None
            self._fired = False

        return {
            'gesture':       gesture,
            'dwell':         dwell,
            'actions':       actions,
            'index_tip_cam': index_tip_cam,
            'landmarks':     landmarks,
        }

    def draw(self, frame, result) -> None:
        """Draw hand skeleton and gesture progress — rendered above the puck bar."""
        h, w = frame.shape[:2]
        lm   = result['landmarks']

        if lm:
            for i, j in _CONNECTIONS:
                cv2.line(frame,
                         (int(lm[i].x * w), int(lm[i].y * h)),
                         (int(lm[j].x * w), int(lm[j].y * h)),
                         (80, 80, 80), 2)
            for p in lm:
                cv2.circle(frame, (int(p.x * w), int(p.y * h)), 4, (255, 255, 255), -1)

        gesture = result['gesture']
        dwell   = result['dwell']

        COLOR = {
            'flat_fist':    (0,  80, 255),
            'upright_fist': (0,   0, 220),
            'index_only':   (0, 220, 120),
            'peace':        (255, 180,  0),
            'fist':         (120, 120, 120),
        }
        LABEL = {
            'flat_fist':    'FLAT FIST    — hold 2s → undo',
            'upright_fist': 'UPRIGHT FIST — hold 5s → reset',
            'index_only':   'INDEX        — hold 3s → extrude',
            'peace':        'PEACE V      — hold 2s → add window',
            'fist':         'FIST (tilt up or down to activate)',
        }
        THRESH = {
            'flat_fist':    DWELL_UNDO,
            'upright_fist': DWELL_RESET,
            'index_only':   DWELL_EXTRUDE,
            'peace':        DWELL_WINDOW,
        }

        label = LABEL.get(gesture)
        if not label:
            return

        color  = COLOR.get(gesture, (160, 160, 160))
        # Render 70 px above the puck dwell bar
        cv2.putText(frame, label, (10, h - 125),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

        thresh = THRESH.get(gesture, 0)
        if thresh > 0:
            progress = min(dwell / thresh, 1.0)
            bar_w    = int(300 * progress)
            cv2.rectangle(frame, (10, h - 108), (310, h - 88), (60, 60, 60), -1)
            cv2.rectangle(frame, (10, h - 108), (10 + bar_w, h - 88), color, -1)
            cv2.putText(frame, f"{dwell:.1f}s", (318, h - 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)

    def close(self) -> None:
        self._lm.close()
