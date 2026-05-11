"""
Generate the 4 board corner ArUco markers (IDs 10-13, DICT_6X6_50).
Print these at ~50mm and tape them to the 4 corners of your workspace board.

Layout:
    ID 10 ─────────── ID 11
     │                  │
     │    workspace     │
     │                  │
    ID 13 ─────────── ID 12
"""

import cv2
import numpy as np

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)

# Generate individual markers
for marker_id in [10, 11, 12, 13]:
    img = cv2.aruco.generateImageMarker(aruco_dict, marker_id, 300)
    filename = f"board_marker_{marker_id}.png"
    cv2.imwrite(filename, img)
    print(f"Saved {filename}")

# Generate a print sheet with all 4
sheet = np.ones((800, 1200), dtype=np.uint8) * 255
positions = [(50, 50), (650, 50), (650, 450), (50, 450)]
labels = ["ID 10 (Top-Left)", "ID 11 (Top-Right)", "ID 12 (Bottom-Right)", "ID 13 (Bottom-Left)"]

for (x, y), label, marker_id in zip(positions, labels, [10, 11, 12, 13]):
    marker = cv2.aruco.generateImageMarker(aruco_dict, marker_id, 250)
    sheet[y:y+250, x:x+250] = marker
    cv2.putText(sheet, label, (x, y + 280),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, 0, 2)

cv2.imwrite("board_markers_print_sheet.png", sheet)
print("Saved board_markers_print_sheet.png")
print("\nPrint this sheet and cut out the 4 markers.")
print("Tape them to the 4 corners of your workspace board.")
