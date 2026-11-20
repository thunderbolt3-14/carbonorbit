# carbonOrbit Evaluation Plan

**Status:** Team approval accepted per project-owner instruction, 20 November 2026; individual reviewer names were not provided. Guide approval is not a project gate.
**Prepared by:** Rahul Velpuri (Person D)  
**Project:** carbonOrbit — GPS-enabled public transit monitoring and emissions scenarios

> This document records the proposed evaluation method before model development. The team should agree on the data schema, split, metrics, thresholds, and model-selection rule, then freeze and version this plan before using test results to select or tune models. Any later change should be dated and justified here.

## 1. Evaluation goals

The evaluation will answer four questions:

1. How accurately can the system estimate bus arrival time on held-out simulated service days?
2. Do candidate ETA models improve on simple, reproducible baselines?
3. How reliably can delay and bus-bunching events be detected when the simulator supplies ground-truth labels?
4. How do estimated greenhouse-gas and particulate emissions change under explicitly stated passenger-shift and occupancy scenarios?

The GPS trajectories are simulated on selected BMTC routes. Results therefore validate the pipeline against the simulator and its assumptions; they are not measurements of BMTC operations or proof of real-world emissions reductions.

## 2. Data and prediction target

### Route and schedule input

The current candidate is the pinned Vonter BMTC GTFS snapshot and the three routes audited in [`docs/data_sources.md`](data_sources.md): `BMTC:dd9ea3794c96` (285-M KBS-BMSIT), `BMTC:6f4d45186ddd` (285 BMSITY-YHKOT), and `BMTC:b202977c0fc0` (406). The snapshot revision, service dates, checksum, project-level consistency checks, and source caveats are recorded there. The feed is an unofficial geometry/schedule source, not live vehicle data; generated trajectories, operations, and event labels remain synthetic. Confirm the team's use of this fallback before freezing the protocol.

### ETA target

For each prediction row, estimate the number of minutes remaining until the bus reaches a specified downstream stop. The target is:

`eta_minutes = actual_stop_arrival_time - prediction_timestamp`

Only rows with a valid downstream stop arrival and a positive prediction horizon should be included. The project must define one prediction point consistently (for example, a bus ping at a configured distance or time before the target stop) and document it in the data dictionary.

### Required data fields

The final field names must match the simulator/API data contract. At minimum, the analytical table needs:

- service date and timestamp, bus ID, route ID, and trip ID;
- current and target stop IDs, direction, and route position;
- latitude/longitude or derived distance to target stop;
- speed and recent segment/travel-time history, where available;
- hour/day or service period, if used by a model;
- actual stop-arrival timestamp or derived ETA target;
- schedule arrival time, if delay is evaluated;
- simulator ground-truth bunching and delay labels, plus the rule used to create them.

Document units, missing-value handling, and label-generation rules in the data dictionary. Identifiers should not accidentally encode the target or split membership.

## 3. Data splitting and leakage control

### Proposed temporal split

For the planned 28-day simulation, use chronological service-day blocks:

| Set | Proposed days | Use |
|---|---:|---|
| Training | First 18 days | Fit model parameters and preprocessing |
| Validation | Next 5 days | Select features, tune parameters, and choose among candidates |
| Test | Final 5 days | One final, held-out comparison after choices are frozen |

The exact dates, simulator seed, route coverage, and row counts must be recorded when the dataset is generated. Do not randomly split individual pings: nearby observations from the same trip can otherwise appear in both training and test sets and inflate performance. If the final dataset is not 28 days, preserve chronological separation and agree on replacement day counts before modeling.

### Leakage safeguards

- Fit imputers, scalers, encoders, and feature selection on training data only; apply the fitted transformations to validation and test data.
- Build every feature from information available at the prediction timestamp. Do not use actual future arrival time, future pings, realized segment duration after prediction, or simulator-only future state as model inputs.
- In the simulator, derive speed observations from scheduled leg speed with an independent observation factor; do not calculate the predictor's speed feature from the realized duration of the leg being predicted. Derive distance from the observed, GPS-perturbed coordinate to the next stop, not the hidden simulator progress fraction.
- Keep all rows from a service day in the same split. Where trip IDs span service dates, keep the full trip together.
- Tune and select models using training and validation only. Use the test set once for the final reported comparison.
- Add automated checks in `tests/test_leakage.py` for future-derived columns, split overlap, and preprocessing fitted outside the training set.
- Preserve a simple data-generation seed and configuration so the evaluation dataset can be regenerated.

## 4. ETA models and baselines

The following ladder is proposed; the team may trim it if time or data volume is limited:

| ID | Model | Role |
|---|---|---|
| B0 | Historical mean ETA by route/stop or segment, computed from training data | Minimum benchmark |
| B1 | Moving-average link travel-time method | Simple operational baseline, inspired by the project literature |
| L1 | Ridge regression | Linear feature baseline |
| T1 | Random forest regression | Nonlinear tree comparator |
| M1 | Gradient-boosting regression | Main candidate model |
| M2 | Quantile gradient boosting, if supported | Prediction-interval candidate |
| Optional | XGBoost or a small MLP | Include only if dependencies, time, and data support a fair comparison |

All models must use the same target rows, chronological split, and primary metrics. Compare against B0 and B1, not just against one another. Record feature sets, package versions, parameters, and random seeds.

## 5. ETA metrics and reporting

Report all errors in minutes on validation and final test data:

- **MAE (primary):** mean absolute error; easy to interpret as average ETA error.
- **RMSE:** penalizes larger misses more strongly.
- **Median absolute error and 90th/95th percentile absolute error:** describe typical and tail errors.
- **Within ±2 minutes:** share of predictions whose absolute error is at most two minutes.
- **Relative MAE improvement over B0:** `100 × (MAE_B0 − MAE_model) / MAE_B0`.
- If prediction intervals are implemented: empirical coverage and average interval width, with the nominal coverage stated.

Provide an overall result and breakdowns by route, service period/hour, and prediction horizon where sample sizes permit. Include test sample counts. Do not hide poor segments behind a single aggregate score.

## 6. Proposed hypotheses and decision rules

These thresholds are **draft proposals**, not results or commitments, and require team approval before the evaluation is frozen.

- **H1 — Baseline value:** M1 reduces test MAE by at least 15% versus B0.
- **H2 — Added nonlinear value:** M1 reduces test MAE by at least 5% versus L1.
- **H3 — Interval calibration (only if M2 is used):** an 80% interval has observed test coverage between 75% and 85%; interval width is reported alongside coverage.
- **H4 — Event detection:** the selected delay/bunching detector reaches test F1 of at least 0.90 against simulator labels. Report precision and recall as well, since F1 alone can conceal missed events or false alarms.
- **H5 — Robustness:** report how ETA error and detection scores change under the agreed polling and GPS-dropout variants; no performance threshold is assumed until the team reviews simulator feasibility.

### Model selection

1. Use validation data for all tuning and candidate selection.
2. Find the best validation RMSE and keep candidates whose validation RMSE is no more than 5% above it.
3. Among those candidates, find the best validation MAE. Keep candidates whose validation MAE is within 5% of that minimum, then choose the simplest in this order: HistoricalMean, MovingSpeed, Ridge, RandomForest, GradientBoosting. This explicit parsimony rule replaces a model-specific L1/M1 comparison.
4. After model-selection rules are fixed on validation, fit each pre-specified candidate using training plus validation data and score each once on the untouched test set. Identify the selected model, but do not use test scores to change the choice or retune.
5. Report all pre-specified candidate test results, including models that do not improve on the baselines.

If the team wishes to use statistical comparisons, specify the test and comparison unit before looking at test outcomes. A possible approach is paired absolute errors by service day, with a bootstrap confidence interval over days; avoid treating correlated pings as independent samples. Statistical significance should supplement, not replace, effect size and error summaries.

## 7. Delay and bus-bunching evaluation

The simulator/data owner must define ground-truth event rules before detection thresholds are tuned. Record schedule assumptions, headway definitions, and the exact event window.

- **Proposed delay rule:** label an event when simulated actual arrival is at least 5 minutes later than its target arrival. Repeat sensitivity analysis at 3 and 10 minutes. These are project defaults for review, not universal standards.
- **Proposed bunching rule:** compare consecutive buses in the same route and direction at a common stop; label bunching when observed headway is no more than 50% of the scheduled/target headway. Repeat sensitivity at 33% and 75%; exclude pairs without a valid positive reference headway. These are project defaults for review, not universal standards.
- Report delay error for any delay estimator and event-level precision, recall, and F1 for alerts. Define the event window and matching tolerance before scoring; if the proposed ping interval remains 30 seconds, one ping interval on either side of event onset is a candidate tolerance.
- Report confusion counts, precision, recall, F1, and the number of positive/negative events. Select the event threshold that maximizes validation event-level F1; break ties by choosing the value closest to the configured default, then the numerically smaller value. Freeze that threshold before scoring it on test. Report the full threshold sensitivity table separately.
- Score events at the event/trip level where possible, rather than counting every adjacent ping as a separate event.

The proposed numeric event rules and H4 F1 target require team review before freeze. Report event metrics on the same held-out test service days as ETA metrics; use validation only for threshold selection. The F1 target is meaningful only if labels are generated independently of the detector and there are enough positive events in the held-out days. If not, report the limitation and counts rather than implying strong validation.

## 8. Emissions scenario method (Rahul Velpuri)

The emissions component is a scenario calculator, not an observed impact measurement. Keep the ETA-model evaluation separate from the emissions calculation: better information may support a modal-shift scenario, but the project does not directly measure that travelers changed modes.

### Proposed calculation

For a stated number of diverted passenger trips and trip distance:

`net CO2e change = (diverted private-mode passenger-km × private-mode factor) − (incremental bus passenger-km × bus factor)`

If the chosen emission factors are already expressed per passenger-km, multiply each factor by passenger-km. If factors are per vehicle-km, convert using explicit vehicle occupancy and vehicle-km assumptions before comparing. Do not mix per-vehicle and per-passenger factors.

For a **marginal-capacity scenario**, state whether an added bus trip is assumed; if no additional bus service is assumed, explain that only incremental service emissions are omitted under that scenario. For an **average-occupancy scenario**, allocate bus emissions per passenger using the stated average occupancy. Keep these scenarios distinct and explain what each represents.

### Scenario inputs and outputs

Vary and document at least:

- private mode (for example, two-wheeler, car, or taxi) and corresponding source-supported factor;
- trip distance and number of diverted trips/passengers;
- bus emission factor and occupancy or load assumption;
- diversion share / ridership uplift, clearly labeled as an assumed scenario;
- pollutant and unit (for example, kg CO2e per day or per scenario period; PM only when a defensible factor and consistent boundary are available).

Present a sensitivity grid including low, central, and high assumptions. Show the inputs, source, unit, calculation, and resulting estimate. Include a break-even occupancy or other threshold analysis if the required factors and assumptions support it. Do not claim PM2.5 or CO2 reductions from an ETA score alone.

### Source and boundary requirements

For each factor, cite the original/authoritative source and record the vehicle type, fuel, geography, year, system boundary (tailpipe or lifecycle), and unit. Prefer like-for-like boundaries. If the chosen sources differ in boundary or context, disclose the mismatch and avoid presenting the figures as directly comparable. The emissions references assigned to Rahul Velpuri (Ramachandra & Shwetmala, ITF, CSTEP, TERI, and Wills et al.) should be checked against their full texts before numerical factors are entered.

## 9. Reproducibility and artifacts

The final evaluation should preserve:

- simulator configuration, seed, dataset version, and data dictionary;
- this frozen plan and any dated amendments;
- feature definitions and leakage checks;
- model parameters, software versions, and run commands;
- scripts/notebooks that regenerate result tables and figures;
- emissions-factor source notes and scenario input tables;
- final metrics with split dates and sample/event counts.

Generated data and figures should follow the repository’s data policy. Do not commit secrets, virtual environments, or restricted source datasets. Use small reproducible examples or documented generation steps where appropriate.

## 10. Phase 2 decisions for team review

Before modeling begins, the team should record agreement on:

1. Whether the project uses 28 simulated days and the proposed 18/5/5 chronological split.
2. The ETA prediction point, target, horizon, and minimum valid sample rules.
3. The baseline/model ladder and which optional models are in scope.
4. The primary/secondary metrics, H1–H5 thresholds, and parsimony rule.
5. Delay and bunching ground-truth definitions and event-level scoring method.
6. Emissions boundary, factors, occupancy/diversion scenarios, and supported pollutants.
7. Dataset schema, seed/version, artifact locations, and the process for freezing this plan.

The project owner confirmed team approval on 20 November 2026 and instructed that guide approval is not a gate. Preserve that approval record without inventing individual reviewer names. Tag the merged agreed version `eval-plan-v1`; change the protocol only through a dated amendment.

## References to verify for the emissions section

Use the project’s verified bibliography and confirm full citation details and numerical assumptions against the source text before final submission:

- T. V. Ramachandra and Shwetmala, “Emissions from India's transport sector: Statewise synthesis,” *Atmospheric Environment*, 2009. DOI: [10.1016/j.atmosenv.2009.07.015](https://doi.org/10.1016/j.atmosenv.2009.07.015).
- International Transport Forum, India transport life-cycle assessment report, 2023. DOI: [10.1787/2d11e416-en](https://doi.org/10.1787/2d11e416-en).
- CSTEP, *Decarbonisation Impact on Road Transport Sector Emissions*, 2017. [Report PDF](https://shaktifoundation.in/wp-content/uploads/2022/04/CSTEP-2017-Decarbonisation-impact-on-Road-Transport-Sector-Emissions-1.pdf).
- TERI, *Per Passenger Emission in Delhi: Different Modes*. [Report PDF](https://teriin.org/sites/default/transport/Per_passenger_emission_in_Delhi_Different_Modes.pdf).
- Wills et al. (2019), arXiv:1907.09335. [Paper record](https://arxiv.org/abs/1907.09335v1).

These references are starting points from the project notes; verify titles, authors, dates, units, and methods from the full source before using them to support a numerical result.
