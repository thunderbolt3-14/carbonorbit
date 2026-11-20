# carbonOrbit — Phase Roadmap

**Updated:** 20 November 2026  
**Purpose:** Track the current project state and sequence remaining work. This roadmap does not assign work to individual members; assign owners after the design decisions below are agreed.

## Current status

- **Phase 0 — Repository setup: complete.** Setup and collaboration documents are in `main`.
- **Phase 1 — Research framing: document set complete.** The literature notes and consolidated survey, base-paper analysis, problem statement, objectives, and contribution statement are merged. The IEEE ETA review and Springer Amogha chapter remain full-text access checks; claims based on their abstracts are marked accordingly.
- **Phase 2 — Inputs and evaluation design: draft complete, review pending.** PR #18 added the proposed evaluation plan. PR #19 audited a pinned unofficial GTFS snapshot and selected three routes. System, data, API, database and dashboard contracts are now documented. The protocol and contracts are not frozen; team/guide review remains open.
- **Phase 3 — Implementation: code drafted, data run pending.** The repository contains a GTFS loader, seeded simulator, ETA/event analytics, robustness runner, Flask API, SQLite store, dashboard and emissions scenario calculator (implementation in [PR #21](https://github.com/thunderbolt3-14/carbonorbit/pull/21)). Python dependencies import and the CLI starts in the local virtual environment. The pinned archive is absent, so no simulated dataset or end-to-end run has been produced.
- **Phase 4 — Analytics: code drafted, results pending.** Chronological model selection, test metrics, route/hour breakdowns, event matching, threshold sensitivity and robustness reporting are implemented. There are no measured project results until the local dataset can be generated and the team accepts the evaluation protocol.
- **Phase 5 — Dashboard and validation: dashboard drafted, integration run pending.** The dashboard calls the local API and marks outputs simulated. Its API/database integration has not been exercised with generated artifacts.
- **Phase 6 — Reporting: outline ready.** A report outline and emissions-factor register are present. Numerical results and emissions scenarios require successful runs and compatible, source-supported factors.

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

Review the documented system architecture, data dictionary, database schema, API endpoint/response contract, and dashboard wireframe. Confirm the simulator/API data fields and label separation, timezone convention, random-seed policy, and run manifest before calling the contract frozen.

## Remaining work and exit gates

| Stage | Work | Exit condition |
|---|---|---|
| **Phase 3 — Foundation** | Obtain the pinned ZIP locally, run the seeded simulator, and inspect movement, timestamps, stop alignment, outputs and data quality. | Repeated runs with the same inputs/config reproduce the same files; GTFS route and label checks pass; API returns the documented shapes for generated artifacts. |
| **Phase 4 — Analytics** | After team review of the protocol, execute ETA baselines/models, event metrics and sensitivity; inspect sample counts and subgroup results. Add sourced emissions factors only when accepted sources are recorded. | Validation-based selection precedes one test evaluation; saved metrics include counts and route/hour and event-threshold breakdowns. |
| **Phase 5 — Dashboard and robustness** | Run normal, noisy-GPS and high-dropout scenarios through the API/dashboard and review failure handling and output consistency. | End-to-end workflow runs reproducibly and dashboard/API outputs agree with saved evaluation artifacts. |
| **Phase 6 — Reporting and release** | Assemble methods, source/data boundaries, results, limitations, SDG evidence and reproducibility instructions; archive the approved configuration and outputs. | Report claims match the measured simulation results and documented assumptions; release materials are complete. |

## Critical path

1. Team/guide reviews and freezes the route-data basis, evaluation plan and system contracts.
2. Place the pinned GTFS ZIP at `data/raw/bmtc.zip`; verify its expected checksum through the simulator.
3. Run the simulator and inspect deterministic outputs, data quality and event labels.
4. Run the model, event and robustness workflows; review the metrics before drafting results.
5. Source and review compatible emissions factors or leave numeric scenarios unreported.
6. Complete report with limitations and measured findings, then agree ownership/release steps as a team.

Keep the access-limited full-text checks visible in the final citation audit. If institutional access is unavailable, retain the abstract-only caveat instead of delaying unrelated simulator and API work.
