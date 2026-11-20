"""SQLite persistence for generated observations and public-facing outputs."""

from __future__ import annotations

import csv
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS runs (
  run_id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL,
  gtfs_revision TEXT NOT NULL,
  gtfs_sha256 TEXT NOT NULL,
  config_json TEXT NOT NULL,
  seed INTEGER NOT NULL,
  simulator_version TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS pings (
  prediction_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
  timestamp_utc TEXT NOT NULL,
  service_date TEXT NOT NULL,
  bus_id TEXT NOT NULL,
  route_id TEXT NOT NULL,
  trip_id TEXT NOT NULL,
  lat REAL NOT NULL,
  lon REAL NOT NULL,
  speed_kmh REAL NOT NULL,
  current_stop_index INTEGER NOT NULL,
  target_stop_id TEXT NOT NULL,
  distance_to_next_stop_m REAL NOT NULL,
  hour_local INTEGER NOT NULL,
  noise_m REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS predictions (
  prediction_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
  bus_id TEXT NOT NULL,
  route_id TEXT NOT NULL,
  target_stop_id TEXT NOT NULL,
  predicted_eta_min REAL NOT NULL,
  model_name TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS alerts (
  alert_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
  alert_type TEXT NOT NULL,
  route_id TEXT NOT NULL,
  bus_id TEXT NOT NULL,
  related_bus_id TEXT,
  target_stop_id TEXT,
  timestamp_utc TEXT NOT NULL,
  severity REAL NOT NULL,
  message TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS evaluation_metrics (
  run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
  metric_name TEXT NOT NULL,
  metric_value REAL,
  unit TEXT NOT NULL,
  partition_name TEXT NOT NULL,
  group_key TEXT NOT NULL DEFAULT 'overall',
  PRIMARY KEY (run_id, metric_name, partition_name, group_key)
);
CREATE INDEX IF NOT EXISTS idx_pings_bus_time ON pings(run_id, bus_id, timestamp_utc);
CREATE INDEX IF NOT EXISTS idx_pings_route_time ON pings(run_id, route_id, timestamp_utc);
CREATE INDEX IF NOT EXISTS idx_alerts_type_time ON alerts(run_id, alert_type, timestamp_utc);
"""


class _ClosingConnection(sqlite3.Connection):
    """Commit/rollback as usual, then close for safe short-lived transactions."""

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            return super().__exit__(exc_type, exc_value, traceback)
        finally:
            self.close()


def connect(path: str | Path = "data/carbonorbit.db") -> sqlite3.Connection:
    db_path = Path(path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path, factory=_ClosingConnection)
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA)
    return connection


def _read_csv(path: Path):
    if not path.is_file():
        return []
    with path.open("r", encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def ingest_run(database: str | Path, run_dir: str | Path, evaluation_dir: str | Path | None = None) -> str:
    """Load telemetry, detector outputs, predictions, and metrics; never load labels."""
    root = Path(run_dir)
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    run_id = manifest["run_id"]
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    config_summary = json.dumps({key: manifest.get(key) for key in ("scenario", "seed", "start_date", "days", "route_ids", "ping_interval_seconds")}, sort_keys=True)
    with connect(database) as db:
        db.execute(
            "INSERT OR REPLACE INTO runs VALUES (?, ?, ?, ?, ?, ?, ?)",
            (run_id, created_at, manifest["gtfs_revision"], manifest["gtfs_sha256"], config_summary, int(manifest["seed"]), manifest["simulator_version"]),
        )
        ping_rows = _read_csv(root / "pings.csv")
        db.executemany(
            """INSERT OR REPLACE INTO pings
            (prediction_id,run_id,timestamp_utc,service_date,bus_id,route_id,trip_id,lat,lon,speed_kmh,current_stop_index,target_stop_id,distance_to_next_stop_m,hour_local,noise_m)
            VALUES (:prediction_id,:run_id,:timestamp_utc,:service_date,:bus_id,:route_id,:trip_id,:lat,:lon,:speed_kmh,:current_stop_index,:target_stop_id,:distance_to_next_stop_m,:hour_local,:noise_m)""",
            ping_rows,
        )
        ping_index = {row["prediction_id"]: row for row in ping_rows}
        alert_rows = _read_csv(root / "detector_alerts.csv")
        db.executemany(
            """INSERT OR REPLACE INTO alerts
            (alert_id,run_id,alert_type,route_id,bus_id,related_bus_id,target_stop_id,timestamp_utc,severity,message)
            VALUES (:alert_id,:run_id,:alert_type,:route_id,:bus_id,:related_bus_id,:stop_id,:timestamp_utc,:severity,:message)""",
            alert_rows,
        )
        if evaluation_dir:
            eval_path = Path(evaluation_dir)
            prediction_rows = _read_csv(eval_path / "test_predictions.csv")
            for row in prediction_rows:
                ping = ping_index.get(row["prediction_id"], {})
                row["run_id"] = run_id
                row["bus_id"] = ping.get("bus_id", "")
                row["created_at"] = created_at
            db.executemany(
                """INSERT OR REPLACE INTO predictions
                (prediction_id,run_id,bus_id,route_id,target_stop_id,predicted_eta_min,model_name,created_at)
                VALUES (:prediction_id,:run_id,:bus_id,:route_id,:target_stop_id,:predicted_eta_min,:model,:created_at)""",
                prediction_rows,
            )
            metrics_path = eval_path / "metrics.json"
            if metrics_path.is_file():
                metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
                selected = metrics.get("selection", {}).get("selected_model", "unknown")
                model_metrics = metrics.get("test", {}).get("models", {}).get(selected, {})
                for metric_name, value in model_metrics.items():
                    if isinstance(value, (float, int)):
                        db.execute(
                            "INSERT OR REPLACE INTO evaluation_metrics VALUES (?, ?, ?, ?, ?, ?)",
                            (run_id, f"eta_{metric_name}", value, "minutes" if metric_name.endswith("_min") else ("percent" if metric_name.endswith("_pct") else "count"), "test", "overall"),
                        )
                for event_type, summary in metrics.get("events", {}).items():
                    for metric_name in ("precision", "recall", "f1", "true_events", "alerts", "tp", "fp", "fn"):
                        value = summary.get(metric_name)
                        if isinstance(value, (float, int)):
                            db.execute(
                                "INSERT OR REPLACE INTO evaluation_metrics VALUES (?, ?, ?, ?, ?, ?)",
                                (run_id, f"{event_type}_{metric_name}", value, "ratio" if metric_name in ("precision", "recall", "f1") else "count", "test", "overall"),
                            )
                for event_type, selection in metrics.get("event_threshold_selection", {}).items():
                    db.execute(
                        "INSERT OR REPLACE INTO evaluation_metrics VALUES (?, ?, ?, ?, ?, ?)",
                        (run_id, f"{event_type}_selected_threshold", float(selection["selected_threshold"]), "minutes" if event_type == "delay" else "ratio", "validation", "overall"),
                    )
                    for metric_name in ("precision", "recall", "f1", "true_events", "alerts", "tp", "fp", "fn"):
                        value = selection.get("test_metrics", {}).get(metric_name)
                        if isinstance(value, (float, int)):
                            db.execute(
                                "INSERT OR REPLACE INTO evaluation_metrics VALUES (?, ?, ?, ?, ?, ?)",
                                (run_id, f"{event_type}_selected_{metric_name}", value, "ratio" if metric_name in ("precision", "recall", "f1") else "count", "test", "overall"),
                            )
    return run_id


def latest_run_id(db: sqlite3.Connection) -> str | None:
    row = db.execute("SELECT run_id FROM runs ORDER BY created_at DESC LIMIT 1").fetchone()
    return row["run_id"] if row else None
