"""Measure local HTTP response times for the populated demo API."""

from __future__ import annotations

import argparse
import json
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import requests

ROOT = Path(__file__).resolve().parents[1]


def available_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def wait_ready(base_url: str, process: subprocess.Popen, timeout: float = 20.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"API server exited early with code {process.returncode}")
        try:
            if requests.get(base_url + "/ping", timeout=1).ok:
                return
        except requests.RequestException:
            pass
        time.sleep(0.2)
    raise TimeoutError("API server did not become ready within 20 seconds")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", default="data/carbonorbit.db")
    parser.add_argument("--samples", type=int, default=50)
    parser.add_argument("--output", default="docs/report/evidence/api_latency.json")
    args = parser.parse_args()
    if args.samples < 10:
        raise SystemExit("Use at least 10 samples per endpoint")

    database = Path(args.database)
    if not database.is_absolute():
        database = ROOT / database
    if not database.is_file():
        raise SystemExit(f"Database not found at {database}; run the documented suite first")
    port = available_port()
    base_url = f"http://127.0.0.1:{port}"
    command = [
        sys.executable, str(ROOT / "scripts" / "carbonorbit.py"), "serve",
        "--host", "127.0.0.1", "--port", str(port), "--database", str(database),
    ]
    creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    process = subprocess.Popen(
        command,
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=creation_flags,
    )
    endpoints = {
        "buses": "/api/v1/buses",
        "eta": "/api/v1/eta",
        "alerts": "/api/v1/alerts?limit=100",
        "metrics": "/api/v1/metrics",
    }
    results = {}
    run_id = None
    try:
        wait_ready(base_url, process)
        for name, path in endpoints.items():
            response = requests.get(base_url + path, timeout=5)
            response.raise_for_status()
            run_id = response.json().get("run_id") or run_id
            timings = []
            for _ in range(args.samples):
                started = time.perf_counter()
                response = requests.get(base_url + path, timeout=5)
                response.raise_for_status()
                timings.append((time.perf_counter() - started) * 1000)
            results[name] = {
                "samples": len(timings),
                "p50_ms": float(np.percentile(timings, 50)),
                "p95_ms": float(np.percentile(timings, 95)),
                "max_ms": float(max(timings)),
            }
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)

    record = {
        "measured_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "run_id": run_id,
        "base_url": "http://127.0.0.1:<ephemeral-port>",
        "samples_per_endpoint": args.samples,
        "latency_target_ms_p95": 1000,
        "meets_all_endpoint_p95_target": all(item["p95_ms"] < 1000 for item in results.values()),
        "measurement_scope": "serial requests to the local Flask development server; not a production load test",
        "endpoints": results,
    }
    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
