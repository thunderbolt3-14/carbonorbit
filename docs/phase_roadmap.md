# carbonOrbit — Phase Roadmap

**Updated:** 20 November 2026  
**Purpose:** Track the current project state and sequence remaining work. This roadmap does not assign work to individual members; assign owners after the design decisions below are agreed.

## Current status

- **Phase 0 — Repository setup: complete.** Setup and collaboration documents are in `main`.
- **Phase 1 — Research framing: document set complete.** The literature notes and consolidated survey, base-paper analysis, problem statement, objectives, and contribution statement are merged. The IEEE ETA review and Springer Amogha chapter remain full-text access checks; claims based on their abstracts are marked accordingly.
- **Phase 2 — Inputs and evaluation design: approved and frozen.** Team approval is accepted per project-owner instruction dated 20 November 2026; guide approval is not a gate. Individual reviewer names were not provided.
- **Phase 3 — Implementation: initial run complete.** PR #21 is merged. The local archive checksum matched the pinned snapshot. Normal, noisy-GPS, and high-dropout scenarios were generated; repeating the normal scenario reproduced the same output checksums.
- **Phase 4 — Analytics: initial results available.** Chronological model comparison, validation threshold selection, test metrics, route/hour breakdowns and robustness results are summarized in [`simulation_results.md`](simulation_results.md). Event F1 is below the proposed 0.90 target on held-out normal test days.
- **Phase 5 — Dashboard and validation: artifacts ingested; UI review remains.** The pipeline loaded generated predictions, alerts, and metrics into SQLite. A manual browser pass against the populated API remains to be done.
- **Phase 6 — Reporting: results summary ready; final report and emissions evidence remain.** Numerical ETA/event results are documented. Emission-factor values remain unset, so no emissions scenario is reported.

## Immediate decisions and deliverables

### 1. Accept the route-data basis

The pinned Vonter GTFS snapshot is the route-data basis. It is unofficial and its schedule caveats remain; generated operations must continue to be labelled synthetic. The raw archive stays local and must not be added to Git.

### 2. Evaluation protocol

The team-approved [`evaluation_plan.md`](evaluation_plan.md) records the ETA, split, metrics and event-threshold rules. Those thresholds are project assumptions, not universal transit standards. Change the method only through a dated amendment.

### 3. Complete the design contract

The architecture, data dictionary, database schema, API contract and dashboard wireframe are documented. A manual browser review of the populated dashboard remains.

## Remaining work and exit gates

| Stage | Work | Exit condition |
|---|---|---|
| **Phase 3 — Foundation** | Seeded scenarios and repeated-run checksum comparison are complete. | Generated artifacts remain synthetic and the checksum is preserved in the run manifest. |
| **Phase 4 — Analytics** | Initial model, event and robustness metrics are summarized in `simulation_results.md`. | Interpret results with route imbalance and event-target shortfall visible. |
| **Phase 5 — Dashboard and robustness** | Robustness scenarios are complete; manually inspect the populated dashboard/API and record UI fixes. | Dashboard values agree with saved SQLite and evaluation artifacts. |
| **Phase 6 — Reporting and release** | Finish the report, citation audit, SDG evidence and reproducibility appendix. Add numeric emissions only when compatible source factors are documented. | Report claims match the synthetic results and assumptions; release materials are complete. |

## Critical path

1. Manually review the populated dashboard and API, then record any needed fixes.
2. Review route-level sample imbalance before interpreting the aggregate ETA result.
3. Complete the report with held-out results, event-target shortfall, simulation limits and citations.
4. Source compatible emissions factors or leave numerical emissions results out of the report.
5. Archive the configuration, run manifest and reproducibility instructions for release.

Keep the access-limited full-text checks visible in the final citation audit. If institutional access is unavailable, retain the abstract-only caveat instead of delaying unrelated simulator and API work.
