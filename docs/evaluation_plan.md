# Evaluation Plan — carbonOrbit

**Phase:** 1 proposed protocol for team and guide review
**Status:** Not frozen. Freeze only after source/route audit and team/guide review.
**Purpose:** Pre-specify evaluation so model selection and claims are not changed after seeing test results.

## 1. Evaluation questions

1. How accurately do candidate methods predict bus arrival time at downstream stops on held-out simulated days?
2. How reliably do the declared delay and bunching rules identify injected simulator events under normal, noisy, and dropout conditions?
3. How do scenario emissions estimates change under plausible combinations of trip diversion, occupancy, bus service, and emission factors?

These are separate questions and need separate outputs. A high ETA score does not demonstrate improved service, ridership, mode shift, or emissions.

## 2. Data and experimental unit

- Use one documented GTFS snapshot and three routes selected by the rule in `docs/data_sources.md`. Record the snapshot, licence, service dates, validation, route IDs, and route geometry availability before generating results.
- Generate synthetic vehicle pings and event labels with a fixed, recorded seed. The simulator plan currently proposes 30-second pings and a 28-day period; confirm feasibility and freeze those values before the full run.
- Primary ETA target: minutes from prediction timestamp to the next scheduled GTFS stop actually reached in the simulator. If the team retains multi-stop horizons, report each horizon separately and do not pool them with next-stop scores.
- Primary unit for ETA metrics: one bus-at-stop prediction instance. Also report breakdowns by route, horizon, hour band, and scenario. Do not treat correlated pings from one trip as independent replicates in significance tests.
- Keep ground-truth labels and future trajectory fields out of model features. Fit preprocessing and feature transformations on training data only.

## 3. Chronological split (proposal)

If a 28-day run is approved, use contiguous whole-day blocks:

| Partition | Days | Use |
|---|---:|---|
| Train | 1–18 | Fit models and training-only transforms |
| Validation | 19–23 | Hyperparameter tuning and model/threshold decisions |
| Test | 24–28 | One final report after choices are frozen |

Do not randomly split pings or trips across partitions. Keep complete trips and all rows from a given service day in only one partition. If generation yields fewer days, revise this split and freeze the revision before model comparison. The test block must not be used for tuning, route selection, threshold selection, or feature changes.

## 4. ETA model ladder

Run all candidates against the same target, eligible prediction instances, features available at prediction time, and temporal partitions. Keep a model only if it trains and predicts reproducibly in the project environment.

| ID | Candidate | Purpose |
|---|---|---|
| B0 | Route/stop/time-bin historical mean from training data | Simple historical baseline |
| B1 | Recent moving average or last-observed running-time estimate | Lightweight online baseline |
| M1 | Regularized linear regression using only prediction-time features | Interpretable statistical model |
| M2 | Gradient-boosted trees using prediction-time route, time, and observed-trip features | Nonlinear tabular model |
| M3 (optional) | LSTM/GRU sequence model | Include only if the training set, compute budget, and implementation support a fair comparison |

Do not assume the more complex model wins. Final model selection is based on validation results using the rule below; report test results once for the selected model and all pre-specified baselines.

## 5. ETA metrics and selection rule

Report in minutes, overall and by route/horizon/scenario:

- MAE as the primary accuracy metric.
- RMSE to reveal sensitivity to large errors.
- Median absolute error and 90th-percentile absolute error to describe typical and tail performance.
- Percentage of predictions within ±2 minutes, labelled as a project reporting threshold rather than a universal standard.
- Runtime per prediction and training runtime for practical comparison.
- If prediction intervals are implemented: empirical coverage and mean interval width at the stated nominal level. Do not report coverage without interval width.

**Proposed selection rule:** choose the lowest-validation-MAE model among candidates whose validation RMSE is no more than 5% worse than the best validation RMSE; among eligible models, choose the simplest/fastest model. Freeze and document the exact simplicity ranking and rule before the test run. If the team chooses a different tolerance, record and justify it before viewing test results.

Report uncertainty using day-level or trip-level resampling that respects clustering; do not bootstrap individual pings as if independent. Any test must be pre-specified and interpreted as simulator-specific evidence.

## 6. Delay and bunching detection

Keep detection separate from control. No holding, stop-skipping, or dispatch action is evaluated in this project unless the scope is formally changed.

- **Proposed delay rule:** a bus is delayed when its simulated actual arrival is at least 5 minutes later than its simulated target arrival. This is a project operating definition, not a universal literature threshold. Generate sensitivity labels at 3 and 10 minutes as well.
- **Proposed bunching rule:** compare consecutive buses in the same route and direction at a common stop. Label bunching when the observed headway is no more than 50% of the scheduled headway. This is a project operating definition; repeat sensitivity at 33% and 75%. Exclude pairs without a valid positive scheduled headway.
- Define each event’s start, end, route, bus pair (for bunching), minimum/maximum severity, and alert-matching tolerance in the simulator configuration. Proposed matching tolerance: one ping interval (30 seconds) on either side of event onset; revise if the ping interval changes. The detector may not use simulator-only label fields.
- Match predicted and true events once using a declared temporal tolerance; avoid counting repeated alerts for one event as multiple true positives.

Report event-level precision, recall, and F1, plus false alerts per route-hour and detection delay. Provide confusion counts and results by normal, delay, bunching, noise, and dropout scenario. Include the declared threshold-sensitivity table. The numeric rules above are **proposed defaults for review**, not approved or frozen; the team and guide must accept or replace them before label generation.

## 7. Robustness and realism checks

Before interpreting model scores, report simulator summaries against the intended configuration: route adherence, speed and dwell distributions, headway distributions, delay/bunching counts, GPS noise, missing-ping rate, and output completeness. Repeat evaluation for planned noise/dropout variants with the same frozen model choices. Report performance by route and scenario so aggregate results cannot hide failures.

## 8. Emissions scenario method

The emissions module estimates changes under explicit assumptions; it does not infer passenger response from ETA accuracy.

For pollutant *p*, define the comparison and system boundary first. A simple operational scenario can be expressed as:

`net change_p = emissions from additional bus service_p − emissions avoided by displaced private-vehicle travel_p`

Specify bus fuel/technology, distance, service added or unchanged, occupancy, passenger-kilometres diverted, private mode mix, private-vehicle occupancy, and pollutant-specific factors. Show a baseline and sensitivity ranges, plus break-even occupancy/diversion where possible. Keep a fixed-service case distinct from a marginal-extra-service case. Do not combine lifecycle factors with tailpipe-only factors.

Report CO2/CO2e and particulate emissions only when supported by a defined factor and boundary. Particulate exhaust emissions are not ambient PM2.5 concentration; no air-quality concentration claim is planned. Any mode-shift percentage must be labelled an assumed scenario, not an observed effect of real-time information.

## 9. Reproducibility and reporting

Archive or identify the GTFS snapshot, licence, simulator version, random seed, configuration, feature list, partition dates, model parameters, event thresholds, and output checksums. Keep raw/source data out of Git unless the licence and repository policy permit it. Report exclusions and failed runs. Use the same test dataset across all final comparisons.

## 10. Freeze checklist

Before tagging a frozen plan, all four members and the guide should review and agree on:

- GTFS source, licence, route IDs, and audit record.
- Simulation duration, ping interval, seed policy, and output schema.
- ETA target, available features, model ladder, split dates, primary metric, and selection rule.
- Delay/bunching definitions, numeric thresholds, and event-matching tolerance.
- Emissions boundary, factors, occupancy/diversion ranges, and sensitivity design.
- Reporting limitations and reproducibility artifacts.

Record approvals and any changes in the diary. Until then this file is a proposal, not a frozen protocol.
