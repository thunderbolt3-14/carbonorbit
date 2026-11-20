# SQLite Schema

The local SQLite database is a cache of generated or derived artifacts. Ground-truth labels are stored separately from telemetry and detector outputs. Do not expose label tables through the API.

## Tables

### `runs`

`run_id TEXT PRIMARY KEY`, `created_at TEXT NOT NULL`, `gtfs_revision TEXT NOT NULL`, `gtfs_sha256 TEXT NOT NULL`, `config_json TEXT NOT NULL`, `seed INTEGER NOT NULL`, `simulator_version TEXT NOT NULL`.

### `pings`

`prediction_id TEXT PRIMARY KEY`, `run_id TEXT NOT NULL`, `timestamp_utc TEXT NOT NULL`, `service_date TEXT NOT NULL`, `bus_id TEXT NOT NULL`, `route_id TEXT NOT NULL`, `trip_id TEXT NOT NULL`, `lat REAL NOT NULL`, `lon REAL NOT NULL`, `speed_kmh REAL NOT NULL`, `current_stop_index INTEGER NOT NULL`, `target_stop_id TEXT NOT NULL`, `distance_to_next_stop_m REAL NOT NULL`, `hour_local INTEGER NOT NULL`, `noise_m REAL NOT NULL`.

This is a serving projection of `pings.csv`; offline-only `direction_id` and `current_stop_id` are not persisted because the current API does not need them.

### `predictions`

`prediction_id TEXT PRIMARY KEY`, `run_id TEXT NOT NULL`, `bus_id TEXT NOT NULL`, `route_id TEXT NOT NULL`, `target_stop_id TEXT NOT NULL`, `predicted_eta_min REAL NOT NULL`, `model_name TEXT NOT NULL`, `created_at TEXT NOT NULL`, optional interval columns.

### `alerts`

`alert_id TEXT PRIMARY KEY`, `run_id TEXT NOT NULL`, `alert_type TEXT NOT NULL`, `route_id TEXT NOT NULL`, `bus_id TEXT NOT NULL`, `related_bus_id TEXT`, `target_stop_id TEXT`, `timestamp_utc TEXT NOT NULL`, `severity REAL NOT NULL`, `message TEXT NOT NULL`.

### `evaluation_metrics`

`run_id TEXT NOT NULL`, `metric_name TEXT NOT NULL`, `metric_value REAL`, `unit TEXT NOT NULL`, `partition_name TEXT NOT NULL`, `group_key TEXT NOT NULL DEFAULT 'overall'`, primary key `(run_id, metric_name, partition_name, group_key)`.

### Offline-only artifacts

`eta_labels.csv` and `event_labels.csv` are not loaded into the API database. The analytics evaluator reads them only for training targets and scoring; they must never become prediction features or dashboard endpoints.

## Indexes and retention

Create indexes on `(run_id, bus_id, timestamp_utc)`, `(run_id, route_id, timestamp_utc)`, and `(run_id, alert_type, timestamp_utc)`. Each local run may replace the previous demo database; retain raw inputs and run artifacts outside SQLite according to repository policy.
