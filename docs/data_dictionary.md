# Data Dictionary

## Telemetry (`pings.csv`)

| Field | Type / unit | Meaning |
|---|---|---|
| `prediction_id` | string | Stable ID joining feature row to the corresponding ETA target; not derived from the target value. |
| `run_id` | string | Simulator run identifier. |
| `timestamp_utc` | ISO-8601 UTC | Simulated observation time. |
| `service_date` | `YYYY-MM-DD` | Simulated local service date used for chronological splitting. |
| `bus_id`, `route_id`, `trip_id`, `direction_id` | string | Synthetic bus and pinned GTFS identifiers. |
| `lat`, `lon` | decimal degrees | Simulated position with configured GPS perturbation. |
| `speed_kmh` | km/h | Simulated instantaneous movement speed; zero while stopped. |
| `current_stop_index` | integer | Index of the most recently passed stop in the trip sequence. |
| `current_stop_id` | string | Stop at the start of the current simulated leg. |
| `target_stop_id` | string | Next scheduled stop for this prediction row. |
| `distance_to_next_stop_m` | metres | Along-leg distance remaining, with position noise excluded. |
| `hour_local` | integer | Local hour of the observation (0–23). |
| `noise_m` | metres | GPS perturbation magnitude applied to this sample. |

Telemetry deliberately excludes actual future arrival time, ETA label, injected delay/bunching flags, and future simulator state.

## Separate labels and quality data

- `eta_labels.csv`: `prediction_id`, `actual_eta_min`; the actual simulated time from observation to next-stop arrival.
- `event_labels.csv`: event ID, event type, route, bus/pair, stop, start/end UTC, severity and label rule version. Labels derive from unperturbed simulator state.
- `stop_observations.csv`: noisy stop-arrival observations plus reference schedule values used by the event detector. Stop observations are independently subject to the configured dropout probability; the quality log records missing observations. This is a simulation proxy for incomplete operational observations, not a detector using the hidden stop truth.
- `quality_log.csv`: expected ping windows and missing/invalid sample intervals, including missing stop observations; missing pings cannot be represented as telemetry rows.

The SQLite `pings` table is a public-serving projection and omits `direction_id` and `current_stop_id`, which remain available in the generated CSV for offline analysis. API responses must never join simulator truth labels.

Keep IDs and service dates in all derived outputs to support traceability and group-aware evaluation.
