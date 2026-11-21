# Initial Synthetic Evaluation Results

**Run:** `88d1eb4fc1efd6c1`
**Generated:** 20 November 2026
**Status:** Reproducible initial result; simulator-only evidence, not a claim about actual BMTC operations.

## Dataset and reproducibility

The run used the pinned unofficial Vonter GTFS snapshot only for route geometry, stop order and schedule context. The raw ZIP remains local at `data/raw/bmtc.zip` and is not committed.

- GTFS revision: `a4702664d65bfbb37290a5f75effaa24ead1d9dd`
- GTFS SHA-256: `812c7d472ff116024ca1e0a7ff6e28662f762ca09265da8d5c7e9f6241cf8a45`
- Period: 9 November–6 December 2026; 28 simulated service days
- Routes: `BMTC:dd9ea3794c96`, `BMTC:6f4d45186ddd`, `BMTC:b202977c0fc0`
- Normal scenario artifacts: 117,713 telemetry pings and ETA labels; 24,760 ground-truth stop arrivals; 24,051 noisy stop observations; 535 labeled delay/bunching events; 3,599 quality-log rows.
- Split: train 9–26 November (18 days), validation 27 November–1 December (5 days), test 2–6 December (5 days).
- Repeating the normal simulation with the same configuration produced the same output-file checksums.

Full CSVs and JSON manifests are generated under ignored `data/simulated/88d1eb4fc1efd6c1/`; evaluation files are under ignored `results/generated/88d1eb4fc1efd6c1/`. Recreate them from the repository root with `venv\\Scripts\\python.exe scripts\\carbonorbit.py suite`.

Committed compact evidence for this run is in [`report/evidence/88d1eb4fc1efd6c1/`](report/evidence/88d1eb4fc1efd6c1/): run manifest, metric summaries, route/hour tables and charts, event-threshold sensitivity, reproducibility check, and API latency measurements. Route-level intervals use 10,000 day-cluster bootstrap resamples (seed 20261121); the five held-out service days, rather than individual pings, are the resampling unit.

## ETA model comparison

The parsimony rule selected **RandomForest** from validation results. The untouched test block contains 21,007 predictions.

| Model | Test MAE (minutes) | Test RMSE (minutes) | Within 2 minutes |
|---|---:|---:|---:|
| HistoricalMean | 0.8907 | 1.2997 | 91.73% |
| MovingSpeed | 0.3595 | 0.8049 | 97.72% |
| Ridge | 0.3005 | 0.7828 | 98.52% |
| RandomForest (selected) | **0.2217** | **0.6452** | **98.86%** |
| GradientBoosting | 0.2636 | 0.7141 | 98.51% |

The selected RandomForest test MAE is 75.1% lower than the HistoricalMean baseline and 26.2% lower than Ridge on this simulated split. The small route has only 431 test examples, compared with 2,745 and 17,831 on the other two routes; its RandomForest MAE is 0.5805 minutes. Aggregate performance is therefore dominated by route `BMTC:b202977c0fc0`.

The 95% day-cluster bootstrap intervals for route MAE were 0.3664–0.7921 minutes for 285 BMSITY-YHKOT, 0.1915–0.2555 for 406, and 0.1529–0.1836 for 285-M KBS-BMSIT. These quantify variation across the five simulated test days only; they are not confidence intervals for real BMTC service.

An early run showed near-zero MovingSpeed error because the speed feature exposed the realized future segment duration. That run is invalid and excluded here. The simulator was corrected to derive speed from scheduled leg speed plus independent observation variation, and to derive remaining distance from the noisy observed coordinate. The metrics above are from the corrected run.

## Delay and bunching detection

Operating thresholds were selected on validation event F1 and then scored on test days. A 30-second event-onset matching tolerance was used.

| Event | Selected threshold | Validation F1 | Test TP / FP / FN | Test precision | Test recall | Test F1 |
|---|---:|---:|---:|---:|---:|---:|
| Delay | 3 minutes | 0.776 | 74 / 24 / 24 | 0.755 | 0.755 | 0.755 |
| Bunching | 75% of scheduled headway | 0.957 | 12 / 1 / 4 | 0.923 | 0.750 | 0.828 |

Neither selected-threshold test F1 reaches the proposed 0.90 target. At the configured default bunching threshold of 50%, the held-out test block has no labeled events or alerts, so the score is not informative. The 75% sensitivity threshold produces 16 positive test events and is the selected operating rule for this run.

Event scoring is one-to-one event matching and reports TP, FP, FN, precision, recall and F1. The project has not yet defined a finite set of negative event opportunities, so TN, specificity and event-level accuracy are not reported.

Threshold sensitivity was computed for delay thresholds 3, 5, and 10 minutes and bunching ratios 0.50 and 0.75. On the held-out test days, delay F1 was 0.755, 0.785, and 0.885 respectively; the 10-minute threshold still did not reach 0.90. Bunching at 0.50 had no positive events and is uninformative; at 0.75 its F1 was 0.828. Only the 3-minute delay and 0.75 bunching rules were selected on validation. Test-set sensitivity rows are descriptive and were not used to select the operating rule. See [`event_threshold_sensitivity.csv`](report/evidence/88d1eb4fc1efd6c1/event_threshold_sensitivity.csv) and [`event_threshold_sensitivity.png`](report/evidence/88d1eb4fc1efd6c1/event_threshold_sensitivity.png).

## Robustness scenarios

The RandomForest model and event thresholds selected on normal validation data were applied unchanged to each scenario's test block.

| Scenario | Test predictions | ETA MAE (minutes) | Delay F1 at normal-selected threshold | Bunching F1 at normal-selected threshold |
|---|---:|---:|---:|---:|
| Normal | 21,007 | 0.2217 | 0.755 | 0.828 |
| Noisy GPS (25 m std. dev.) | 21,007 | 0.2446 | 0.755 | 0.828 |
| High dropout (15%) | 18,915 | 0.2236 | 0.694 | 0.640 |

These variants are controlled simulator perturbations. They do not measure actual GPS error or missing-message rates in BMTC operations.

## Interpretation and remaining evidence gaps

- These results validate that the pipeline can generate data, fit candidates, select using validation, score a held-out period and repeat the configured run. They do not establish real-world ETA accuracy or service improvement.
- Leakage review of the implementation confirmed chronological disjoint splits, validation-only model/threshold selection, and final model fitting on train+validation before test predictions. Test labels are used for scoring only. The simulation feature correction also excludes realized future segment duration and hidden simulator position from the speed/distance features.
- The GTFS snapshot is unofficial and has documented schedule caveats. All vehicle movements and event truth labels are synthetic.
- The simulator produces no passenger diversion observations. Emissions factors remain unset, so no carbon or pollutant reduction is calculated.
- The API/database ingestion ran as part of the pipeline. A manual browser pass confirmed the dashboard loaded 22 buses, 100 alerts, RandomForest and the 0.22-minute test MAE from the populated local API.
- A serial local Flask development-server check made 50 requests to each API endpoint; all endpoint p95 latencies were under the 1,000 ms project target (buses 381 ms, ETA 269 ms, alerts 32 ms, metrics 31 ms). This is a local functional latency check, not a production concurrency/load test. See [`api_latency.json`](report/evidence/88d1eb4fc1efd6c1/api_latency.json).
- The project has no live BMTC vehicle data or external-city validation in this run.
