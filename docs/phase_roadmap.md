# carbonOrbit — Phase Roadmap

**Updated:** 21 November 2026
**Purpose:** Track the current project state and sequence remaining work. This roadmap does not assign work to individual members; assign owners after the design decisions below are agreed.

## Current status

- **Phase 0 — Repository setup: complete.** Setup and collaboration documents are in `main`.
- **Phase 1 — Research framing: document set complete.** The literature notes and consolidated survey, base-paper analysis, problem statement, objectives, and contribution statement are merged. The IEEE ETA review and Springer Amogha chapter remain full-text access checks; claims based on their abstracts are marked accordingly.
- **Phase 2 — Inputs and evaluation design: approved and frozen.** Team approval is accepted per project-owner instruction dated 20 November 2026; guide approval is not a gate. Individual reviewer names were not provided.
- **Phase 3 — Implementation: complete for the synthetic prototype.** The pinned archive checksum was verified. The seeded normal, noisy-GPS, and high-dropout suite completes locally; repeating the normal run reproduced checksums for all eight output files. GTFS/API validation and regression coverage are in the merged verification work; the clean Python 3.12 test run passed all 34 tests. This phase does not provide live BMTC ingestion.
- **Phase 4 — Analytics: evaluation complete; H4 target not met.** The pre-specified model ladder, chronological selection, held-out test scoring, route/hour breakdowns, day-cluster uncertainty, event-threshold sensitivity, and robustness analysis are documented in [`simulation_results.md`](simulation_results.md) and the evidence package. Test event F1 was 0.755 for delay and 0.828 for bunching, both below the proposed 0.90 target. This is a reported hypothesis outcome, not a reason to tune against test data.
- **Phase 5 — Dashboard and validation: initial integration review complete.** The pipeline loaded generated predictions, alerts, and metrics into SQLite. The local dashboard rendered 22 buses, 100 alerts, the selected model and ETA test MAE; its API requests returned successfully.
- **Phase 6 — Reporting: review package prepared.** Report and citation audit are in `docs/report/final_report.md` and `docs/citation_audit.md`. The reproducible evidence package, route/day uncertainty, event-threshold sensitivity, repeated-run checksum check, and local API latency evidence are under `docs/report/evidence/88d1eb4fc1efd6c1/`. Emissions are deliberately unquantified. Citation metadata checks were extended; full-text access restrictions remain labeled.

## Immediate decisions and deliverables

### 1. Accept the route-data basis

The pinned Vonter GTFS snapshot is the route-data basis. It is unofficial and its schedule caveats remain; generated operations must continue to be labelled synthetic. The raw archive stays local and must not be added to Git.

### 2. Evaluation protocol

The team-approved [`evaluation_plan.md`](evaluation_plan.md) records the ETA, split, metrics and event-threshold rules. Those thresholds are project assumptions, not universal transit standards. Change the method only through a dated amendment.

### 3. Verify dashboard and API

The architecture, data dictionary, database schema, API contract and dashboard wireframe are documented. The populated dashboard received a manual browser review. A local serial latency check measured 50 calls per endpoint; all p95 values were below the 1,000 ms target. This is not a production load test.

## Phase 0–4 closeout

Phases 0–4 are closed for the project’s current, bounded synthetic proof of concept. Phase 4’s evaluation work is complete, but H4 (test event F1 ≥ 0.90) was **not supported** by these data. The project must retain that result and the simulator-only boundary in presentations and reports. No claim is made that all proposed performance targets were achieved.

## Remaining work and exit gates

| Stage | Work | Exit condition |
|---|---|---|
| **Phase 3 — Foundation** | Complete for the synthetic prototype; tests, suite, and repeat-run check pass. | Reopen only for defects or new real-feed integration work. |
| **Phase 4 — Analytics** | Complete for run `88d1eb4fc1efd6c1`; metrics and evidence are documented. H4 target is unmet and remains an explicit result. | Reopen only through a dated protocol amendment or new independently held-out data; do not tune on this test set. |
| **Phase 5 — Dashboard and robustness** | Populated dashboard manual review and local API latency check are recorded. | Team reviews dashboard and simulated-data notices. Production load behavior remains unevaluated. |
| **Phase 6 — Reporting and release** | Report and evidence package are prepared; SDG impact limitations and the unquantified emissions decision are recorded; citation metadata checks are updated. | Team reviews/merges PRs; team obtains any unavailable full text if required; release tag and publication remain post-review. |

## Critical path

1. Review route-level sample imbalance before interpreting the aggregate ETA result.
2. Review the report and citation audit; complete the source checks explicitly left open in the audit.
3. Source compatible emissions factors or leave numerical emissions results out of the report.
4. Review the evidence package, approve the SDG scope statements, then archive the configuration, run manifest, dependency lock hash, and reproducibility instructions for release.

Keep the access-limited full-text checks visible in the final citation audit. If institutional access is unavailable, retain the abstract-only caveat instead of delaying unrelated simulator and API work.
