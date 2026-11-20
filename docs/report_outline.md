# Final Report Outline

1. **Abstract** — problem, proposed synthetic BMTC-route study, methods, and measured results only after the final evaluation.
2. **Introduction** — Bengaluru bus information context, problem statement, research question, objectives, contribution boundaries.
3. **Literature review** — ETA methods, reliability/bunching, passenger information, Indian transport emissions; use the agreed paper-note template and distinguish full-text from abstract-only sources.
4. **Data and ethics** — pinned GTFS revision, license/caveats, selected routes, synthetic-data design, exclusion of passenger identities and raw restricted data.
5. **System design** — architecture, API/database contracts, simulator and dashboard.
6. **Methodology** — simulator parameters, random seeds, ETA target, leakage safeguards, chronological split, model ladder, event rules, and emissions equations.
7. **Results** — route/scenario summaries, ETA test performance, event-level scores and sensitivity, robustness runs, emissions scenarios only where source-supported inputs exist.
8. **Discussion** — interpretation against literature, simulation-specific limits, source uncertainty, transfer limits.
9. **Conclusion and future work** — answer only the research question supported by the synthetic evaluation.
10. **Reproducibility appendix** — pinned data revision/checksum, configurations, commands, versions, schemas and output manifest.

Do not describe synthetic GPS as live BMTC observations. Do not claim passenger diversion, service improvement, causal emissions savings, or ambient PM2.5 change without new evidence.
