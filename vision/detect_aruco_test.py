"""
Test which ArUco dictionary matches your printed markers.
Point your webcam at the markers and this script will try all common dictionaries.
Press 'q' to quit.
"""

import cv2

def _find_external_camera():
    for idx in range(1, 5):
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, _ = cap.read()
            cap.release()
            if ret:
                print(f"[CAM] Using external camera at index {idx}")
                return idx
    print("[CAM] WARNING: no external camera found — falling back to built-in webcam (index 0)")
    return 0

CAMERA_ID = _find_external_camera()

DICTS = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
}

cap = cv2.VideoCapture(CAMERA_ID, cv2.CAP_DSHOW)
if not cap.isOpened():
    cap = cv2.VideoCapture(CAMERA_ID)
if not cap.isOpened():
    print(f"Cannot open camera {CAMERA_ID}")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("Point camera at your ArUco markers...")
print("Press 'q' to quit.\n")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    y_offset = 30

    for name, dict_id in DICTS.items():
        aruco_dict = cv2.aruco.getPredefinedDictionary(dict_id)
        params = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(aruco_dict, params)
        corners, ids, _ = detector.detectMarkers(grey)

        if ids is not None and len(ids) > 0:
            detected_ids = sorted(ids.flatten().tolist())
            text = f">>> {name}: DETECTED IDs {detected_ids} <<<"
            color = (0, 255, 0)
            print(f"MATCH: {name} -> IDs {detected_ids}")
        else:
            text = f"    {name}: no markers"
            color = (0, 0, 200)

        cv2.putText(frame, text, (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        y_offset += 25

    cv2.imshow("ArUco Dictionary Test", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
