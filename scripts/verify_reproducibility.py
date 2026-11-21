"""Repeat the configured normal simulation and compare output-file checksums."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carbonorbit.config import load_config  # noqa: E402
from carbonorbit.simulator import simulate  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", default="data/simulated")
    parser.add_argument("--run-id", required=True, help="Run ID whose existing normal manifest is the comparison baseline")
    parser.add_argument("--record", default="results/reproducibility_check.json")
    args = parser.parse_args()

    config = load_config(ROOT / "config" / "simulation.yaml")
    expected_id = None
    output_root = Path(args.output_root)
    if not output_root.is_absolute():
        output_root = ROOT / output_root
    record_path = Path(args.record)
    if not record_path.is_absolute():
        record_path = ROOT / record_path

    before_dir = output_root / args.run_id / "normal"
    before_path = before_dir / "manifest.json"
    if before_path.is_file():
        before = json.loads(before_path.read_text(encoding="utf-8"))
        expected_id = before.get("run_id")
        before_hashes = before.get("files_sha256", {})
    else:
        before_hashes = None

    run_dir = simulate(config, "normal", output_root)
    after = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    if expected_id and expected_id != after.get("run_id"):
        raise SystemExit(f"Run ID changed: expected {expected_id}, found {after.get('run_id')}")
    after_hashes = after.get("files_sha256", {})
    if before_hashes is not None and before_hashes != after_hashes:
        changed = sorted(
            name for name in set(before_hashes) | set(after_hashes)
            if before_hashes.get(name) != after_hashes.get(name)
        )
        raise SystemExit("Normal-run output checksums changed: " + ", ".join(changed))

    record = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "run_id": after["run_id"],
        "scenario": "normal",
        "repeated_run_matches_previous_manifest": before_hashes is not None,
        "file_count": len(after_hashes),
        "files_sha256": after_hashes,
        "gtfs_revision": after["gtfs_revision"],
        "gtfs_sha256": after["gtfs_sha256"],
        "seed": after["seed"],
        "simulator_version": after["simulator_version"],
    }
    record_path.parent.mkdir(parents=True, exist_ok=True)
    record_path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    print(f"run_id={record['run_id']}")
    print(f"repeat_matches={record['repeated_run_matches_previous_manifest']}")
    print(f"file_count={record['file_count']}")
    print(f"record={record_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
