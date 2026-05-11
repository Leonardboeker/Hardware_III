"""Generate printable ArUco markers for the Hardware III installation.

Outputs PNG files to cad/aruco-markers/.
Print at the sizes specified in the comments below.

Usage:
    python cad/generate_aruco_markers.py

Requires: opencv-contrib-python (already installed)
"""
import cv2
import numpy as np
from pathlib import Path

OUTPUT_DIR = Path("cad/aruco-markers")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# DICT_4X4_50 — MUST match vision/src/aruco_detect.py
ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

# Marker size in pixels for the image (print at 300 DPI for physical size)
# At 300 DPI: 300px = 2.54cm, so 600px = ~5cm (good puck size)
MARKER_PX   = 600   # image size in pixels
BORDER_PX   = 60    # white border around marker (required for detection)
LABEL_PX    = 80    # height for text label below marker

# Which markers to generate:
MARKERS = {
    # Footprint pucks (place on table, tracked by overhead camera)
    "footprint": list(range(0, 10)),      # IDs 0-9, print at ~5x5cm
    # Height marker
    "height":    [10],                    # ID 10, print at ~5x5cm
    # Material controller
    "material":  [11],                    # ID 11, print at ~5x5cm
    # Method selectors (larger, for RFID pedestal)
    "method_masonry":   [20],             # ID 20, print at ~8x8cm
    "method_3d_print":  [21],             # ID 21, print at ~8x8cm
    "method_prefab":    [22],             # ID 22, print at ~8x8cm
}

LABELS = {
    **{i: f"FOOTPRINT-{i}" for i in range(10)},
    10: "HEIGHT",
    11: "MATERIAL",
    20: "METHOD: MASONRY",
    21: "METHOD: 3D PRINT",
    22: "METHOD: PREFAB",
}

def generate_marker(marker_id: int, filename: str):
    total_h = MARKER_PX + 2 * BORDER_PX + LABEL_PX
    total_w = MARKER_PX + 2 * BORDER_PX

    img = np.ones((total_h, total_w), dtype=np.uint8) * 255

    # Generate ArUco marker
    marker_img = cv2.aruco.generateImageMarker(ARUCO_DICT, marker_id, MARKER_PX)
    img[BORDER_PX:BORDER_PX + MARKER_PX, BORDER_PX:BORDER_PX + MARKER_PX] = marker_img

    # Label
    label = f"ID:{marker_id}  {LABELS.get(marker_id, '')}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.9
    thickness = 2
    text_size = cv2.getTextSize(label, font, font_scale, thickness)[0]
    text_x = (total_w - text_size[0]) // 2
    text_y = BORDER_PX + MARKER_PX + BORDER_PX // 2 + text_size[1]
    cv2.putText(img, label, (text_x, text_y), font, font_scale, 0, thickness)

    # Print size hint
    hint = "Print: 5x5cm (footprint/height/material)  |  8x8cm (method selectors)"
    hint_size = cv2.getTextSize(hint, font, 0.45, 1)[0]
    cv2.putText(img, hint, ((total_w - hint_size[0]) // 2, text_y + 30),
                font, 0.45, 100, 1)

    out_path = OUTPUT_DIR / filename
    cv2.imwrite(str(out_path), img)
    print(f"[OK] {out_path}  (ID={marker_id}  {LABELS.get(marker_id, '')})")


def main():
    print(f"Generating ArUco markers → {OUTPUT_DIR}/\n")

    for group, ids in MARKERS.items():
        for mid in ids:
            filename = f"aruco_id{mid:02d}_{group.replace(' ', '_')}.png"
            generate_marker(mid, filename)

    print(f"\nDone — {sum(len(v) for v in MARKERS.values())} markers saved to {OUTPUT_DIR}/")
    print("\nPrint instructions:")
    print("  Footprint pucks (ID 0-9):  5x5cm each — glue onto 3D-printed puck tops")
    print("  Height marker  (ID 10):   5x5cm")
    print("  Material ctrl  (ID 11):   5x5cm")
    print("  Method selectors (ID 20-22): 8x8cm — mount on RFID pedestal sides")
    print("\nFor a quick test right now: print ID 0 at any size on paper and hold it in front of the webcam.")


if __name__ == "__main__":
    main()
