"""
MediaPipe hand gesture detector with dwell-based action triggering.
Uses the MediaPipe Tasks API (mediapipe >= 0.10.0).

Gestures:
  index_only     index finger up, rest folded
  peace          index + middle up, rest folded
  three_fingers  index + middle + ring up, pinky folded
  fist           all fingers folded

Dwell rules:
  index_only    held >= 3 s  -> 'place_point'    (fires once; re-raise to place again)
  peace         held >= 3 s  -> 'add_window'     (fires once; re-raise to add again)
  three_fingers held >= 4 s  -> 'extrude'        (fires once; re-raise to re-confirm)
  fist released at 4-5 s     -> 'undo'
  fist released at  > 5 s    -> 'reset'
"""

import os
import time
import urllib.request
import cv2
import mediapipe as mp

_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hand_landmarker.task')
_MODEL_URL  = ('https://storage.googleapis.com/mediapipe-models/'
               'hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task')

# Finger landmark indices
_TIPS = [8, 12, 16, 20]   # index middle ring pinky tips
_PIPS = [6, 10, 14, 18]   # corresponding PIP joints

# Hand skeleton connections for manual drawing
_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),           # thumb
    (0, 5), (5, 6), (6, 7), (7, 8),            # index
    (0, 9), (9, 10), (10, 11), (11, 12),       # middle
    (0, 13), (13, 14), (14, 15), (15, 16),     # ring
    (0, 17), (17, 18), (18, 19), (19, 20),     # pinky
    (5, 9), (9, 13), (13, 17),                 # palm knuckles
]

DWELL_POINT   = 3.0
DWELL_EXTRUDE = 4.0
DWELL_UNDO    = 4.0
DWELL_RESET   = 5.0


def _ensure_model():
    """Download the hand landmarker model file on first run (~8 MB)."""
    if not os.path.exists(_MODEL_PATH):
        print("[INFO] Downloading hand landmarker model (~8 MB) — one-time setup...")
        try:
            urllib.request.urlretrieve(_MODEL_URL, _MODEL_PATH)
            print("[INFO] Model saved.")
        except Exception as e:
            if os.path.exists(_MODEL_PATH):
                os.remove(_MODEL_PATH)
            raise RuntimeError(f"[ERROR] Model download failed: {e}") from e


class GestureDetector:
    def __init__(self):
        _ensure_model()
        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=_MODEL_PATH),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.7,
            min_tracking_confidence=0.7,
        )
        self._landmarker    = mp.tasks.vision.HandLandmarker.create_from_options(options)
        self._current       = None
        self._start         = None
        self._index_fired   = False
        self._peace_fired   = False
        self._extrude_fired = False
        self._grace_frames  = 0
        self._t0            = time.time()

    # ------------------------------------------------------------------
    def _classify(self, lm):
        """Return gesture name from a list of 21 NormalizedLandmark objects."""
        up = [lm[_TIPS[i]].y < lm[_PIPS[i]].y for i in range(4)]
        idx, mid, ring, pinky = up
        if idx and not mid and not ring and not pinky:
            return 'index_only'
        if idx and mid and not ring and not pinky:
            return 'peace'
        if idx and mid and ring and not pinky:
            return 'three_fingers'
        if not any(up):
            return 'fist'
        return 'none'

    # ------------------------------------------------------------------
    def process(self, frame):
        """
        Process one camera frame.

        Returns dict:
          gesture       current gesture string
          dwell         seconds current gesture has been held
          actions       list of action strings triggered this frame
          index_tip_cam (x, y) pixel coords of index fingertip, or None
          landmarks     list of 21 NormalizedLandmark objects, or None
        """
        h, w = frame.shape[:2]
        now      = time.time()
        rgb      = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result   = self._landmarker.detect_for_video(mp_image, int((now - self._t0) * 1000))

        actions       = []
        gesture       = 'none'
        dwell         = 0.0
        index_tip_cam = None
        landmarks     = None

        if result.hand_landmarks:
            self._grace_frames = 0
            lm        = result.hand_landmarks[0]   # list of 21 landmarks
            landmarks = lm
            gesture   = self._classify(lm)
            tip        = lm[8]
            index_tip_cam = (int(tip.x * w), int(tip.y * h))

            if gesture != self._current:
                # gesture changed: check fist release
                if self._current == 'fist' and self._start is not None:
                    held = now - self._start
                    if held >= DWELL_RESET:
                        actions.append('reset')
                    elif held >= DWELL_UNDO:
                        actions.append('undo')
                self._current       = gesture
                self._start         = now
                self._index_fired   = False
                self._peace_fired   = False
                self._extrude_fired = False
                dwell = 0.0
            else:
                dwell = now - self._start if self._start else 0.0

            if gesture == 'index_only' and dwell >= DWELL_POINT and not self._index_fired:
                actions.append('place_point')
                self._index_fired = True
            elif gesture == 'peace' and dwell >= DWELL_POINT and not self._peace_fired:
                actions.append('add_window')
                self._peace_fired = True
            elif gesture == 'three_fingers' and dwell >= DWELL_EXTRUDE and not self._extrude_fired:
                actions.append('extrude')
                self._extrude_fired = True

        else:
            # Hand disappeared — 3-frame grace period before resetting
            self._grace_frames += 1
            if self._grace_frames <= 3:
                # Carry forward last gesture so one-frame occlusions don't break dwell
                gesture = self._current or 'none'
                dwell   = now - self._start if self._start else 0.0
            else:
                if self._current == 'fist' and self._start is not None:
                    held = now - self._start
                    if held >= DWELL_RESET:
                        actions.append('reset')
                    elif held >= DWELL_UNDO:
                        actions.append('undo')
                self._current       = None
                self._start         = None
                self._grace_frames  = 0
                self._index_fired   = False
                self._peace_fired   = False
                self._extrude_fired = False

        return {
            'gesture':       gesture,
            'dwell':         dwell,
            'actions':       actions,
            'index_tip_cam': index_tip_cam,
            'landmarks':     landmarks,
        }

    # ------------------------------------------------------------------
    def draw(self, frame, result):
        """Draw hand skeleton, gesture label, and dwell progress bar."""
        h, w = frame.shape[:2]

        if result['landmarks']:
            lm = result['landmarks']
            for i, j in _CONNECTIONS:
                x1, y1 = int(lm[i].x * w), int(lm[i].y * h)
                x2, y2 = int(lm[j].x * w), int(lm[j].y * h)
                cv2.line(frame, (x1, y1), (x2, y2), (80, 80, 80), 2)
            for lmk in lm:
                cx, cy = int(lmk.x * w), int(lmk.y * h)
                cv2.circle(frame, (cx, cy), 4, (255, 255, 255), -1)

        gesture = result['gesture']
        dwell   = result['dwell']

        COLOR = {
            'index_only':    (0, 200, 255),
            'peace':         (255, 180, 0),
            'three_fingers': (0, 220, 120),
            'fist':          (0, 60, 255),
            'none':          (160, 160, 160),
        }
        LABEL = {
            'index_only':    'INDEX         - hold 3s to place point',
            'peace':         'PEACE         - hold 3s to add window',
            'three_fingers': 'THREE FINGERS - hold 4s to extrude walls',
            'fist':          'FIST          - 4s undo / 5s reset',
            'none':          'no gesture',
        }
        THRESH = {
            'index_only':    DWELL_POINT,
            'peace':         DWELL_POINT,
            'three_fingers': DWELL_EXTRUDE,
            'fist':          DWELL_RESET,
            'none':          0,
        }

        color = COLOR.get(gesture, COLOR['none'])
        label = LABEL.get(gesture, gesture)
        cv2.putText(frame, label, (10, h - 55), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

        thresh = THRESH.get(gesture, 0)
        if thresh > 0:
            progress = min(dwell / thresh, 1.0)
            bar_w    = int(300 * progress)
            cv2.rectangle(frame, (10, h - 38), (310, h - 18), (60, 60, 60), -1)
            cv2.rectangle(frame, (10, h - 38), (10 + bar_w, h - 18), color, -1)
            cv2.putText(frame, f"{dwell:.1f}s", (318, h - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)

    # ------------------------------------------------------------------
    def close(self):
        self._landmarker.close()
