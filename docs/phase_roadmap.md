# carbonOrbit — Phase Roadmap

**Updated:** 21 November 2026
**Repository baseline:** `main` at `79f8b3a` (PRs #24, #25, and #26 merged; no open PRs at update time)
**Purpose:** Track prototype status, remaining evidence limits, and release decisions.

## Current status

- **Phase 0 — Repository setup: complete.** Setup and collaboration documents are in `main`.
- **Phase 1 — Research framing: document set complete.** The literature notes and consolidated survey, base-paper analysis, problem statement, objectives, and contribution statement are merged. The IEEE ETA review and Springer Amogha chapter full texts were not reviewed; current claims are restricted to their publisher records/abstracts, so this is an access limitation rather than a release blocker.
- **Phase 2 — Inputs and evaluation design: approved and frozen.** Team approval is accepted per project-owner instruction dated 20 November 2026; guide approval is not a gate. Individual reviewer names were not provided.
- **Phase 3 — Implementation: complete for the synthetic prototype.** The pinned archive checksum was verified. The seeded normal, noisy-GPS, and high-dropout suite completes locally; repeating the normal run reproduced checksums for all eight output files. GTFS/API validation and regression coverage are in the merged verification work; the clean Python 3.12 test run passed all 34 tests. This phase does not provide live BMTC ingestion.
- **Phase 4 — Analytics: corrected evaluation complete for the synthetic prototype.** ETA model selection and held-out scoring remain as reported. A 21 November audit corrected event sensitivity so detector thresholds are compared against fixed truth labels, and delay events are matched at trip level. Delay test F1 is 0.974; bunching cannot be evaluated because the frozen 50% truth rule produces zero positive events in validation and test. The corrected values replace earlier event results; no test-set tuning was performed.
- **Phase 5 — Dashboard and validation: initial integration review complete.** The pipeline loaded generated predictions, alerts, and metrics into SQLite. The local dashboard rendered 22 buses, 100 alerts, the selected model and ETA test MAE; its API requests returned successfully.
- **Phase 6 — Reporting: submission review package prepared.** Report and citation audit are in `docs/report/final_report.md` and `docs/citation_audit.md`. The reproducible evidence package and API/dashboard checks are under `docs/report/evidence/88d1eb4fc1efd6c1/`. Named citation metadata checks are closed; full texts that were unavailable remain explicitly abstract-only. Emissions are deliberately unquantified.

## Immediate decisions and deliverables

### 1. Accept the route-data basis

The pinned Vonter GTFS snapshot is the route-data basis. It is unofficial and its schedule caveats remain; generated operations must continue to be labelled synthetic. The raw archive stays local and must not be added to Git.

### 2. Evaluation protocol

The team-approved [`evaluation_plan.md`](evaluation_plan.md) records the ETA, split, metrics and event-threshold rules. Those thresholds are project assumptions, not universal transit standards. Change the method only through a dated amendment.

### 3. Verify dashboard and API

The architecture, data dictionary, database schema, API contract and dashboard wireframe are documented. The populated dashboard received a manual browser review. A local serial latency check measured 50 calls per endpoint; all p95 values were below the 1,000 ms target. This is not a production load test.

## Phase 0–4 closeout

Phases 0–4 are closed for the project’s current, bounded synthetic proof of concept. Delay detection exceeds the proposed H4 F1 threshold on the synthetic held-out block, but the bunching half of H4 is **not evaluable** because there are no positive truth events. This is not sufficient evidence to claim the combined event hypothesis is met. The project must retain this limitation and the simulator-only boundary in presentations and reports.

## Remaining evidence limits and release steps

| Stage | Work | Exit condition |
|---|---|---|
| **Phase 3 — Foundation** | Complete for the synthetic prototype; merged validation fixes and tests, suite, and repeat-run check pass. | Reopen only for defects or new authorized real-feed integration work. |
| **Phase 4 — Analytics** | Corrected metrics and evidence for run `88d1eb4fc1efd6c1` are documented. Delay target is met synthetically; bunching is unscorable because the frozen 50% truth rule yielded zero positive validation/test events. | To evaluate bunching, obtain independently collected operational observations or have the team approve a realistic bunching-rich simulation amendment and new held-out split. Never tune on the existing test set. |
| **Phase 5 — Dashboard and robustness** | Populated dashboard manual review and local API latency check are recorded. | The current local prototype has no production deployment target, so production load testing was not run. If deployment is planned, specify infrastructure, concurrency/load profile, and acceptance target first. |
| **Phase 6 — Reporting and release** | Report/evidence package prepared; SDG limitations and no-emissions decision recorded; named citation metadata closeout completed. PRs #24–26 are merged to `main`. | Project owner reviews the final report, accepts abstract-only citation boundaries and remaining scientific limits, then decides whether to create a version tag for the synthetic prototype. Real-world validation and numerical emissions remain future research, not prototype release gates. |

## Critical path

1. Review route-level sample imbalance before interpreting the aggregate ETA result.
2. Have the project owner perform the final report/evidence review and approve a prototype version/tag if desired.
3. Keep emissions unquantified until compatible factors and explicit, supportable activity/diversion inputs are available.
4. Treat authorized BMTC observations, operational validation, and any production load assessment as separate future-work gates; do not present them as completed.

Keep the remaining full-text access limits visible in the citation audit. Current report claims are constrained to source records/abstracts where full text was not reviewed; additional access is needed only before expanding those claims.
