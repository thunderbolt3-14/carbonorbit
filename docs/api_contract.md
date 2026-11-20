# API Contract

**Version:** v1 proposal
**Base URL:** `http://127.0.0.1:5000/api/v1` (health is also exposed at `/ping`)

All responses are JSON. Timestamps use ISO-8601 UTC (`Z`). Distances use metres, speed uses km/h, ETA and delay use minutes. Route and bus IDs are strings. Responses include `run_id` where data is run-specific.

## Endpoints

| Method and path | Purpose | Success response |
|---|---|---|
| `GET /ping` | Health/readiness | `{"ok":true,"service":"carbonOrbit","version":"v1"}` |
| `GET /buses?route_id=...` | Latest simulated position per bus | `{"run_id":"...","buses":[{"bus_id":"...","route_id":"...","trip_id":"...","timestamp":"...Z","lat":0.0,"lon":0.0,"speed_kmh":0.0,"next_stop_id":"..."}]}` |
| `GET /eta?bus_id=...` | Latest stored prediction per bus | `{"run_id":"...","predictions":[{"bus_id":"...","route_id":"...","target_stop_id":"...","predicted_eta_min":0.0,"interval_low_min":null,"interval_high_min":null,"model":"...","timestamp":"...Z"}]}` |
| `GET /alerts?route_id=...&limit=100` | Detector alerts (never ground-truth labels) | `{"run_id":"...","alerts":[{"alert_id":"...","type":"delay|bunching","route_id":"...","bus_id":"...","timestamp":"...Z","severity":0.0,"message":"..."}]}` |
| `GET /metrics` | Latest evaluation summary | `{"run_id":"...","metrics":{"eta_mae_min":null,"eta_rmse_min":null,"delay_precision":null,"delay_recall":null,"delay_f1":null,"bunching_precision":null,"bunching_recall":null,"bunching_f1":null}}` |
| `POST /emissions/scenario` | Calculate a declared scenario | Input and output below |

An empty collection is a valid `200` response when no artifact has been loaded. Unknown route or bus IDs return an empty collection, not a fabricated estimate. The alerts `limit` must be an integer; values are bounded to 1–500.

## Emissions request

Runtime validation requires separate private-mode and bus boundaries and rejects a mismatch. Both source descriptions must be supplied. This makes the shared-boundary requirement explicit for each factor.

```json
{
  "scenario_id": "central",
  "diverted_passengers": 100,
  "trip_distance_km": 8.0,
  "private_mode_factor_g_per_pkm": 1.0,
  "bus_factor_g_per_pkm": 1.0,
  "private_mode_boundary": "operational",
  "bus_boundary": "operational",
  "pollutant": "CO2",
  "factor_sources": {
    "private_mode": "source URL and context",
    "bus": "source URL and context"
  }
}
```

The factor values above are deliberately toy values to illustrate the JSON shape; they are not defaults, evidence, or approved BMTC factors. Do not use them for a project result. The calculator reports `private_avoided_kg`, `bus_added_kg`, `net_avoided_kg`, units, the common boundary, and echoed factor sources. Requests without source descriptions, a positive private-mode factor, a non-negative bus factor, or matching boundaries return `400` with an error.

## Error shape

`{"error":{"code":"invalid_request","message":"..."}}`
