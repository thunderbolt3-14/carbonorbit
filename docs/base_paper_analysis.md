# Base Paper Analysis — Rawat et al. (2026)

**Paper:** Seema Rawat, Alyona Abaidullina, Dilnaz Alimbayeva, Deepak Kumar, and Praveen Kumar, “Real-Time Bus Arrival Prediction and Bus Bunching Prevention Using a Multi-Agent LSTM Approach,” *Frontiers in Built Environment*, vol. 12 (2026), DOI: [10.3389/fbuil.2026.1894212](https://doi.org/10.3389/fbuil.2026.1894212).
**Access checked:** Publisher abstract, 19 November 2026. The publisher page states that the final formatted version will be published soon; claims here are therefore limited to the abstract.
**Status:** Draft analysis for Phase 1 review.

## Research problem and motivation

Sparse, low-frequency bus telemetry makes arrival-time prediction difficult. The paper asks how ETA prediction can be combined with decentralized, proactive bus-bunching prevention rather than relying only on reactive central dispatch.

## Data and setting

The authors report using MTA SIRI real-time data from New York City’s 20 highest-frequency bus routes. Their control evaluation uses a multi-agent simulation on routes B82 and Bx9. The dataset and operating context differ from the planned synthetic BMTC route data.

## Method

The paper describes an LSTM ETA model with route embeddings and a forward-looking target-imputation method intended to retain more than 90% of raw telemetry despite sparse observations. The predictions feed bus agents that coordinate a decentralized stop-skipping action described as “Express” mode.

## Reported results

The abstract reports overall ETA MAE of 2.02 minutes, 28.5% below historical baselines. In 120-step simulations on B82 and Bx9, it reports no zero-gap full bunching collapse; Express mode was triggered in 19.2% and 25.8% of steps, respectively, and headways recovered above the authors’ safe threshold after interventions. These are results reported in the abstract and in the paper’s simulation setting; they are not benchmarks for carbonOrbit.

## Strengths relevant to this project

- It links model performance to a service-reliability question rather than treating ETA error as the only outcome.
- It discusses data sparsity explicitly and reports a named historical baseline comparison.
- It distinguishes prediction from an operational response, giving carbonOrbit a useful scope comparison.

## Limitations and transfer boundaries

- New York City routes, SIRI data, and MTA operating conditions do not establish performance on BMTC routes.
- Bunching prevention is simulated operational control involving stop skipping; carbonOrbit’s planned reliability task is event detection and display, not bus control.
- The reported prevention outcomes do not measure passenger response, modal shift, fuel use, or emissions.
- The full formatted article was not available on the publisher page when checked; methods and result details should be verified against the final text before being cited beyond the abstract.

## Relationship to carbonOrbit

Rawat et al. are the closest base-paper comparator and already combine ETA prediction with bunching prevention. carbonOrbit should therefore frame its difference narrowly: a reproducible application to selected BMTC route geometry using synthetic GPS, labelled event detection rather than control, and a separate sensitivity-tested emissions scenario layer. The project should compare baselines, target definitions, temporal splits, and metrics, but must not claim superiority unless its own evaluation supports it.

## Likely examiner questions

**Has Rawat et al. already integrated ETA and bunching?** Yes. Their paper combines ETA prediction and bunching prevention; carbonOrbit’s contribution is the BMTC-focused simulation and bounded emissions scenario analysis.

**Why not implement their stop-skipping approach?** It is an operational control intervention with passenger and service trade-offs. That is outside carbonOrbit’s current detection-and-display scope.

**Does a 2.02-minute MAE mean carbonOrbit should target the same score?** No. The dataset, route, sampling, target, and evaluation design differ. We should report our own held-out results and compare cautiously.

## Source

Rawat et al., publisher abstract: [Frontiers in Built Environment](https://www.frontiersin.org/journals/built-environment/articles/10.3389/fbuil.2026.1894212/abstract).
