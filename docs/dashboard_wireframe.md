# Dashboard Wireframe

**Status:** Initial implementation layout; all live values are simulated/project artifacts.

```text
┌ carbonOrbit | SIMULATED SERVICE | run id | updated at ─────────────┐
│ Route filter [all ▼]   Day [date]   Scenario [normal ▼] [Refresh] │
├──────────────────────────────────────┬───────────────────────────┤
│ Route view                           │ Service summary           │
│ bus markers + route line             │ active buses / alerts     │
│ click marker → bus / ETA / next stop │ mean ETA / model name     │
├──────────────────────────────────────┴───────────────────────────┤
│ Alerts: timestamp | route | type | bus(es) | severity | status   │
├──────────────────────────────────────────────────────────────────┤
│ Evaluation (offline): MAE / RMSE | event precision/recall/F1      │
│ Scenario emissions: assumptions and factors shown beside result  │
└──────────────────────────────────────────────────────────────────┘
```

## Display rules

- Persistent label: **Simulated data — not live BMTC tracking**.
- Omit empty ETA or alert estimates; do not substitute ground-truth labels.
- Show the active model, run ID, timestamp, and route filter.
- Emissions panel shows factor sources, units, boundary, diversion and occupancy assumptions; it never attributes a scenario result to an observed passenger response.
- On API failure, retain the page and show a readable service-unavailable message.
