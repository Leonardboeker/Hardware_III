"""Passive UDP sniffer on port 7000 — shows every packet that arrives
regardless of whether it's valid OSC or unknown addresses. Use to debug
whether vision-laptop traffic is reaching this machine at all.

Note: binds the same port as the orchestrator. Windows allows two UDP
listeners only if both set SO_REUSEADDR (which python-osc does NOT).
If this errors with WinError 10048, stop the orchestrator first.

Run:  python orchestrator/tests/udp_sniffer.py
Stop: Ctrl+C
"""
from __future__ import annotations

import socket
import sys
import time

PORT = 7000
HOST = "0.0.0.0"


def main() -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
    except OSError as e:
        print(f"[sniffer] FAILED to bind {HOST}:{PORT}: {e}")
        print("[sniffer] Hint: stop the orchestrator first, then run me alone.")
        sys.exit(2)

    print(f"[sniffer] listening on {HOST}:{PORT} — waiting for packets")
    sock.settimeout(30.0)
    count = 0
    seen_from = set()
    try:
        while True:
            try:
                data, addr = sock.recvfrom(8192)
            except socket.timeout:
                print(f"[sniffer] no packets in 30s (total {count} so far)")
                continue
            count += 1
            seen_from.add(addr[0])
            # Try to parse as OSC: first \x00-padded string is the address
            try:
                end = data.index(b"\x00")
                osc_addr = data[:end].decode("ascii", errors="replace")
            except Exception:
                osc_addr = "<unparseable>"
            ts = time.strftime("%H:%M:%S")
            print(f"{ts}  #{count}  from {addr[0]}:{addr[1]}  {len(data):4d}B  addr={osc_addr!r}")
    except KeyboardInterrupt:
        print(f"\n[sniffer] stopped. Total {count} packets from {seen_from}")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
