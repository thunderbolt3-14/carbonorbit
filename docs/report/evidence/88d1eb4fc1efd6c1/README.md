# Evidence package: `88d1eb4fc1efd6c1`

This directory contains compact, reviewable outputs from the synthetic run. It does not contain full-size generated telemetry or the raw GTFS archive.

- `run_manifest.json`, `metrics.json`, `robustness.json`: run configuration, model/event results, and scenario summaries.
- `eta_error_by_route.csv` / `.png`, `eta_error_by_hour.csv` / `.png`: held-out ETA errors by subgroup.
- `eta_cluster_bootstrap.csv`: 95% intervals from 10,000 bootstrap resamples of the five held-out service days, seed 20261121.
- `event_threshold_sensitivity.csv` / `.png`: validation and test values for the declared delay and bunching threshold candidates. Test values are descriptive and do not select thresholds.
- `reproducibility_check.json`: checksum comparison from a repeat normal simulation.
- `dashboard_check.json`: manual browser confirmation of the populated simulated dashboard.
- `api_latency.json`: 50 serial local Flask development-server requests per endpoint; not a production concurrency test.

The report explains the limits for each result. Every metric here is based on synthetic service generated from the pinned GTFS route/schedule context.
