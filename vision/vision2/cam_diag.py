"""Camera diagnostic — run this directly to find the right index and backend."""
import cv2

BACKENDS = [
    ("DSHOW",   cv2.CAP_DSHOW),
    ("MSMF",    cv2.CAP_MSMF),
    ("DEFAULT", 0),
]

print("\n=== Camera Diagnostic ===\n")
found = []

for idx in range(6):
    for bname, backend in BACKENDS:
        try:
            cap = cv2.VideoCapture(idx, backend) if backend else cv2.VideoCapture(idx)
            if not cap.isOpened():
                cap.release()
                continue
            ret, frame = cap.read()
            ok = ret and frame is not None and frame.size > 0
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cap.release()
            status = "OK" if ok else "OPEN but no frame"
            print(f"  index {idx} | {bname:7s} | {w}x{h} | {status}")
            if ok:
                found.append((idx, bname, backend))
        except Exception as e:
            print(f"  index {idx} | {bname:7s} | ERROR: {e}")

print()
if not found:
    print("No working camera found at all.")
else:
    idx, bname, _ = found[-1]
    print(f"Recommended: index={idx}  backend={bname}")
    print(f"  → set CAM_INDEX={idx} in run.bat or run:  set CAM_INDEX={idx} && run.bat")
    print()
    print("Opening live preview — press Q to quit...")
    _, _, backend = found[-1]
    cap = cv2.VideoCapture(idx, backend) if backend else cv2.VideoCapture(idx)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    while True:
        ret, frame = cap.read()
        if ret and frame is not None and frame.size > 0:
            cv2.imshow("Diagnostic Preview", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
