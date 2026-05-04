"""CLI entry point for the Phase 2 one-puck closed-loop CV vertical slice.

Usage:
    python -m vision.src.run_vertical_slice \\
        --camera 0 \\
        --intrinsics vision/calibration/camera_intrinsics.yml \\
        --homography vision/calibration/homography.yml \\
        --td-host 127.0.0.1 \\
        --td-port 7000 \\
        --puck-id 0 \\
        --target-x 640 --target-y 400

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
    p = argparse.ArgumentParser(description="Phase 2 vertical slice — ArUco → OSC → TD")
    p.add_argument("--camera", type=int, default=0)
    p.add_argument("--intrinsics", default="vision/calibration/camera_intrinsics.yml")
    p.add_argument("--homography", default="vision/calibration/homography.yml")
    p.add_argument("--td-host", default="127.0.0.1")
    p.add_argument("--td-port", type=int, default=7000)
    p.add_argument("--puck-id", type=int, default=0, help="ArUco ID of the single test puck")
    p.add_argument("--target-x", type=float, required=True, help="Target projector-px X")
    p.add_argument("--target-y", type=float, required=True, help="Target projector-px Y")
    p.add_argument("--dry-run", action="store_true", help="Use synthetic calibration YAMLs")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    intrinsics_path = args.intrinsics
    homography_path = args.homography

    if args.dry_run:
        print("[WARN] --dry-run: using synthetic calibration — DO NOT USE IN FINAL DEMO")
        intrinsics_path = "vision/calibration/synthetic_intrinsics.yml"
        homography_path = "vision/calibration/synthetic_homography.yml"

    cap = open_camera(args.camera)
    sender = make_sender(args.td_host, args.td_port)
    target_zones = {args.puck_id: (args.target_x, args.target_y)}

    print(f"[INFO] Streaming to TD at {args.td_host}:{args.td_port}")
    print(f"[INFO] Watching puck ID={args.puck_id}, target=({args.target_x}, {args.target_y})")
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
                frame, intrinsics_path, homography_path
            )
            sender.send_frame(detections, target_zones)

            dt_ms = (time.perf_counter() - t0) * 1000
            frame_times.append(dt_ms)
            if len(frame_times) > 30:
                frame_times.pop(0)
            avg_ms = sum(frame_times) / len(frame_times)

            # Debug overlay
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

            cv2.imshow("ArUco vertical slice — press Q to quit", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        if frame_times:
            print(f"\n[PERF] avg latency: {sum(frame_times)/len(frame_times):.1f} ms")
            print(f"[PERF] max latency: {max(frame_times):.1f} ms")
            print(f"[NOTE] target is <150ms end-to-end (this measures only CV+OSC, not TD render)")


if __name__ == "__main__":
    main()
