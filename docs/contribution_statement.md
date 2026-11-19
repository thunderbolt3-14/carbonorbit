# Contribution Statement — carbonOrbit

**Phase:** 1 draft for team and guide review

## Proposed contribution

carbonOrbit proposes a reproducible, route-based evaluation workflow that connects four pieces often evaluated separately in a student project: (1) ETA model comparison, (2) labelled delay and bunching detection, (3) an interactive presentation of predictions and alerts, and (4) an explicitly bounded environmental scenario analysis. The workflow will use selected BMTC route geometry and schedules with synthetic GPS trajectories and simulator ground truth.

The intended project contribution is an applied integration and evaluation for a Bengaluru route context, not a new ETA algorithm and not the first system to combine ETA prediction with bus-bunching work. Rawat et al. already combine ETA estimation and bunching prevention in a New York City data and multi-agent simulation setting. carbonOrbit differs in its planned BMTC route context, detection-focused reliability scope, reproducibility, and separate scenario-based emissions layer.

## What the project can establish

- Which of the selected ETA methods performs best under the project’s documented simulation and chronological test split.
- How well pre-specified delay and bunching rules identify the simulator’s labelled events under the evaluated scenarios.
- How emissions estimates change when declared diversion, occupancy, service, distance, and emission-factor assumptions vary.
- Whether the pipeline can be reproduced from its documented route snapshot, configuration, seed, and analysis steps.

## What it cannot establish without new evidence

- Actual ETA accuracy, delay frequency, or bunching prevalence on operating BMTC buses.
- That passenger information changes ridership or causes private-vehicle trips to be replaced.
- That scenario-estimated emissions reductions occurred in Bengaluru or changed ambient PM2.5 concentrations.
- That the selected routes or results generalize to all BMTC services.

## Novelty wording for the report

Use: “This project applies a reproducible ETA and reliability-evaluation workflow to simulated service on selected BMTC routes and adds a sensitivity-tested emissions scenario layer.”

Avoid: “the first integrated ETA and bunching system,” “proves real-world BMTC emissions savings,” or “validated on BMTC GPS,” unless new field evidence supports those statements.
