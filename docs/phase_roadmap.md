# carbonOrbit — Phase Roadmap

**Updated:** 20 November 2026  
**Purpose:** Track the current project state and sequence remaining work. This roadmap does not assign work to individual members; assign owners after the design decisions below are agreed.

## Current status

- **Phase 0 — Repository setup: complete.** Setup and collaboration documents are in `main`.
- **Phase 1 — Research framing: document set complete.** The literature notes and consolidated survey, base-paper analysis, problem statement, objectives, and contribution statement are merged. The IEEE ETA review and Springer Amogha chapter remain full-text access checks; claims based on their abstracts are marked accordingly.
- **Phase 2 — Inputs and evaluation design: in progress.** PR #18 added the proposed evaluation plan. PR #19 audited a pinned unofficial GTFS snapshot and selected three routes. The plan is not frozen, and the simulator/system design decisions below remain open.
- **Implementation and validation phases: next.** No simulation configuration has been agreed yet; start with a one-route, one-day prototype after the data contract and event definitions are set.

## Immediate decisions and deliverables

### 1. Accept the route-data basis

Review [`data_sources.md`](data_sources.md) and agree whether to use its pinned Vonter GTFS snapshot for route geometry and stop order. The DULT portal returned a gateway error during the audit, so the chosen snapshot is unofficial. Its schedules are not ground truth for actual service, and the project must continue to label generated operations as synthetic. Do not add the raw archive to Git.

### 2. Freeze the evaluation protocol

Review [`evaluation_plan.md`](evaluation_plan.md) and record decisions on:

- the ETA prediction point, target stop and forecast horizon;
- whether to retain the proposed 28 simulated days and 18/5/5 chronological split;
- the baseline/model ladder, H1–H5 hypotheses, validation-based selection rule and primary metrics;
- proposed event labels: at least 5 minutes late (sensitivity at 3/10 minutes) and observed headway no more than 50% of scheduled/target headway (sensitivity at 33%/75%);
- event matching, positive-label volume, and polling/GPS-dropout scenarios;
- emissions boundary, source-supported factors, occupancy and diversion ranges, and which pollutants can be reported.

Treat these numeric thresholds as review proposals until the team accepts them. After review, add the date and reviewers, mark the plan frozen, and tag the agreed version before using test results for model selection.

### 3. Complete the design contract

Agree the simulator/API data fields and label separation, timezone convention, random-seed policy, and run manifest. Then document the system architecture, database schema, API endpoints/response shapes, and dashboard wireframe so implementation work can proceed against one shared contract.

## Recommended implementation sequence

| Stage | Work | Exit condition |
|---|---|---|
| **Phase 3 — Foundation** | Implement route loading and a seeded one-route/one-day simulator; validate movement, timestamps, stop alignment, and injected labels. Build the API/database and analytics input contract in parallel against the agreed schema. | Repeated runs with the same inputs/config produce the same outputs; route and label checks pass; the API returns the agreed shapes. |
| **Phase 4 — Analytics** | Add ETA baselines and candidate models on chronological splits; add leakage safeguards; score delay and bunching events against independent simulator labels; implement emissions scenarios only with declared, sourced inputs. | Validation-based selection is recorded before one final test evaluation; all metrics include counts and scenario breakdowns. |
| **Phase 5 — Dashboard and robustness** | Connect the dashboard to the API; show route, ETA and alerts; run agreed noise/dropout variants and performance checks. | End-to-end workflow runs reproducibly and the dashboard/API outputs agree with the saved evaluation results. |
| **Phase 6 — Reporting and release** | Assemble methods, source/data boundaries, results, limitations, SDG evidence and reproducibility instructions; archive the approved configuration and outputs. | Report claims match the measured simulation results and documented assumptions; release materials are complete. |

## Critical path

1. Agree the pinned route-data basis and evaluation plan.
2. Freeze the schema, simulation settings, thresholds and emissions boundary.
3. Build and validate the small simulator prototype.
4. Scale the simulator and add analytics, API and dashboard work against the frozen contracts.
5. Run final evaluation once, then prepare the report.

Keep the access-limited full-text checks visible in the final citation audit. If institutional access is unavailable, retain the abstract-only caveat instead of delaying unrelated simulator and API work.
