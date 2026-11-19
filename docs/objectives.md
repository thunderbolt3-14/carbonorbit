# Objectives — carbonOrbit

**Phase:** 1 draft for team and guide review

## General objective

Design and evaluate a reproducible bus ETA and reliability-monitoring workflow using synthetic GPS trajectories on selected BMTC routes, and report environmental outcomes only as transparent, assumption-dependent scenarios.

## Specific objectives

1. Audit and document an eligible BMTC GTFS source, its licence, snapshot date, service period, validation results, and limitations; select three usable routes using a recorded rule.
2. Specify and implement a seeded simulator that generates timestamped route positions and controlled dwell, delay, bunching, noise, and dropout conditions, while preserving separate ground-truth labels.
3. Compare a pre-specified ladder of historical, statistical, and machine-learning ETA models on identical, chronological train, validation, and test periods, reporting errors, interval performance where available, and runtime.
4. Evaluate delay and headway-based bunching detection against simulator event labels using pre-declared event rules and event-level precision, recall, and F1.
5. Produce scenario-based operational emissions estimates under clearly stated vehicle, occupancy, diversion, and emission-factor assumptions; report sensitivity and break-even conditions.
6. Communicate the methods, limitations, and results through a documented API/dashboard and a reproducible report, without presenting synthetic results as observed BMTC performance or emissions reductions.

## Out of scope

This phase does not claim a live BMTC deployment, causal ridership change, verified private-car diversion, bus-control intervention, measured ambient air-quality change, or universal performance across Bengaluru routes.
