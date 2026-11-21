# Initial Synthetic Evaluation Results

**Run:** `88d1eb4fc1efd6c1`
**Generated:** 20 November 2026
**Status:** Corrected reproducible result; simulator-only evidence, not a claim about actual BMTC operations.

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

The 95% day-cluster bootstrap intervals for route MAE were 0.3664–0.7921 minutes for 285 BMSITY-YHKOT, 0.1915–0.2555 for 406, and 0.1529–0.1836 for 285-M KBS-BMSIT. These quantify variation across the five simulated test days only; they are not confidence intervals for real BMTC service. They are uncertainty intervals for route-level MAE, not individual ETA prediction intervals.

An early run showed near-zero MovingSpeed error because the speed feature exposed the realized future segment duration. That run is invalid and excluded here. The simulator was corrected to derive speed from scheduled leg speed plus independent observation variation, and to derive remaining distance from the noisy observed coordinate. The metrics above are from the corrected run.

## Delay and bunching detection

Operating thresholds were selected on validation event F1 and then scored on test days. Delay events are matched by route, trip, and service date because the label and alert are both trip-level events and can cross their respective thresholds at different stops. Bunching events use same-route/same-stop matching within 30 seconds.

| Event | Selected threshold | Validation F1 | Test TP / FP / FN | Test precision | Test recall | Test F1 |
|---|---:|---:|---:|---:|---:|---:|
| Delay | 3 minutes | 0.995 | 93 / 5 / 0 | 0.949 | 1.000 | 0.974 |
| Bunching | configured default retained (50%; no validation positives) | not scorable | 0 / 0 / 0 | not scorable | not scorable | not scorable |

Delay detection exceeds the proposed 0.90 test F1 target in this synthetic run. The configured 50% bunching truth rule produces no positive events in either validation or test, so bunching detection cannot be evaluated and its threshold is not tuned. This is an evaluation-data limitation, not evidence that bunching detection works or fails.

Event scoring is one-to-one event matching and reports TP, FP, FN, precision, recall and F1. The project has not yet defined a finite set of negative event opportunities, so TN, specificity and event-level accuracy are not reported.

Threshold sensitivity compares detector settings against one fixed truth definition (delay >=5 minutes; bunching <=50% of scheduled headway). On test, delay F1 was 0.974, 1.000, and 0.967 at detector thresholds of 3, 5, and 10 minutes. These are post-selection descriptive comparisons; the selected 3-minute setting was chosen on validation only. Bunching truth had zero positive events in validation and test, so all bunching F1 values are uninformative; detector alerts at a looser 75% threshold are false positives relative to the frozen 50% rule. See [`event_threshold_sensitivity.csv`](report/evidence/88d1eb4fc1efd6c1/event_threshold_sensitivity.csv) and [`event_threshold_sensitivity.png`](report/evidence/88d1eb4fc1efd6c1/event_threshold_sensitivity.png).

### Evaluation correction (21 November 2026)

The original sensitivity implementation changed truth labels along with the detector threshold, invalidating cross-threshold F1 comparisons. The corrected implementation keeps truth rules fixed and varies only detector settings; it also retains the configured threshold when validation has no positive truth events. The event results above replace pre-correction values. Delay matching now follows the plan's trip-level event definition. The bunching test cannot be scored because no ground-truth bunching events were generated under the frozen rule; more representative, independently reviewed service observations or a separately approved bunching-rich simulation scenario are needed before claiming detector performance.

## Robustness scenarios

The RandomForest model and event thresholds selected on normal validation data were applied unchanged to each scenario's test block.

| Scenario | Test predictions | ETA MAE (minutes) | Delay F1 at normal-selected threshold | Bunching F1 at normal-selected threshold |
|---|---:|---:|---:|---:|
| Normal | 21,007 | 0.2217 | 0.974 | not scorable (0 truth events) |
| Noisy GPS (25 m std. dev.) | 21,007 | 0.2446 | 0.974 | not scorable (0 truth events) |
| High dropout (15%) | 18,915 | 0.2236 | 0.974 | not scorable (0 truth events) |

These delay scores use the normal-validation-selected 3-minute detector threshold against the fixed 5-minute delay truth and same-trip matching. Bunching remains unscorable because the fixed truth rule yields zero events. These are controlled simulator perturbations; they do not measure actual GPS error or missing-message rates in BMTC operations.

## Interpretation and remaining evidence gaps

- These results validate that the pipeline can generate data, fit candidates, select using validation, score a held-out period and repeat the configured run. They do not establish real-world ETA accuracy or service improvement.
- Leakage review of the implementation confirmed chronological disjoint splits, validation-only model/threshold selection, and final model fitting on train+validation before test predictions. Test labels are used for scoring only. The simulation feature correction also excludes realized future segment duration and hidden simulator position from the speed/distance features. The corrected normal simulation repeated with all eight output-file checksums matching; see [`reproducibility_check.json`](report/evidence/88d1eb4fc1efd6c1/reproducibility_check.json).
- The GTFS snapshot is unofficial and has documented schedule caveats. All vehicle movements and event truth labels are synthetic.
- The simulator produces no passenger diversion observations. Emissions factors remain unset, so no carbon or pollutant reduction is calculated.
- The API/database ingestion ran as part of the pipeline. A manual browser pass confirmed the dashboard loaded 22 buses, 100 alerts, RandomForest and the 0.22-minute test MAE from the populated local API.
- A serial local Flask development-server check made 50 requests to each API endpoint; all endpoint p95 latencies were under the 1,000 ms project target (buses 381 ms, ETA 269 ms, alerts 32 ms, metrics 31 ms). This is a local functional latency check, not a production concurrency/load test. See [`api_latency.json`](report/evidence/88d1eb4fc1efd6c1/api_latency.json).
- The project has no live BMTC vehicle data or external-city validation in this run.
