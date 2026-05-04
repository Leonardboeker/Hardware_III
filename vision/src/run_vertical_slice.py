"""CLI entry point for the ArUco footprint CV pipeline.

Detects all ArUco markers in camera view and streams their projector-space
positions to TouchDesigner via OSC. TD draws the footprint visualization.

Usage:
    python -m vision.src.run_vertical_slice \\
        --camera 0 \\
        --intrinsics vision/calibration/camera_intrinsics.yml \\
        --homography vision/calibration/homography.yml

    # With synthetic calibration for dev/testing:
    python -m vision.src.run_vertical_slice --camera 0 \\
        --intrinsics vision/calibration/synthetic_intrinsics.yml \\
        --homography vision/calibration/synthetic_homography.yml

Press Q to quit.
"""
from __future__ import annotations

import argparse
import sys
import time

import cv2

from vision.src.aruco_detect import detect_pucks_in_projector_coords, open_camera
from vision.src.osc_send import make_sender


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="ArUco footprint pipeline — streams all pucks to TD")
    p.add_argument("--camera", type=int, default=0)
    p.add_argument("--intrinsics", default="vision/calibration/camera_intrinsics.yml")
    p.add_argument("--homography", default="vision/calibration/homography.yml")
    p.add_argument("--td-host", default="127.0.0.1")
    p.add_argument("--td-port", type=int, default=7000)
    return p.parse_args()


def main() -> None:
    args = parse_args()

    cap = open_camera(args.camera)
    sender = make_sender(args.td_host, args.td_port)

    print(f"[INFO] Streaming ALL pucks to TD at {args.td_host}:{args.td_port}")
    print("[INFO] Press Q in the preview window to quit\n")

    frame_times: list[float] = []

    try:
        while True:
            t0 = time.perf_counter()
            ret, frame = cap.read()
            if not ret:
                print("[ERROR] Camera read failed", file=sys.stderr)
                break

            detections = detect_pucks_in_projector_coords(
                frame, args.intrinsics, args.homography
            )
            sender.send_frame(detections)

            dt_ms = (time.perf_counter() - t0) * 1000
            frame_times.append(dt_ms)
            if len(frame_times) > 30:
                frame_times.pop(0)
            avg_ms = sum(frame_times) / len(frame_times)

            for d in detections:
                px, py = int(d["projector_xy"][0]), int(d["projector_xy"][1])
                cv2.circle(frame, (int(d["camera_xy"][0]), int(d["camera_xy"][1])), 8, (0, 255, 0), 2)
                cv2.putText(frame, f"ID:{d['id']} proj:({px},{py})",
                           (int(d["camera_xy"][0]) + 10, int(d["camera_xy"][1])),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            cv2.putText(frame, f"avg {avg_ms:.1f}ms/frame", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(frame, f"detections: {len(detections)}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            cv2.imshow("ArUco footprint pipeline — press Q to quit", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        if frame_times:
            print(f"\n[PERF] avg latency: {sum(frame_times)/len(frame_times):.1f} ms")
            print(f"[PERF] max latency: {max(frame_times):.1f} ms")


if __name__ == "__main__":
    main()
