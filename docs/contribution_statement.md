# Contribution Statement — carbonOrbit

**Phase:** 1 draft for team and guide review

## Proposed contribution

carbonOrbit proposes a reproducible evaluation workflow for selected BMTC route geometry and schedules, using synthetic GPS trajectories and simulator ground truth to compare ETA models and evaluate delay and bunching detection, with a separate, explicitly bounded environmental scenario analysis. Prior work has already connected bus-delay prediction with per-trip CO2 estimation (Amogha et al., 2026), and other work combines ETA prediction with bunching control (Rawat et al., 2026). The project must therefore not claim that integration of prediction, reliability, or emissions is itself new.

The intended contribution is a bounded, reproducible BMTC-route simulation and evaluation: event detection is scored against known synthetic labels, and emissions are reported as scenarios with assumptions separated from ETA and delay metrics. This is not a new ETA algorithm, a field validation, or the first system to link prediction and reliability or emissions. Rawat et al. combine ETA and bunching prevention in an NYC data and multi-agent simulation setting; Amogha et al. combine bus-delay prediction with per-trip CO2 estimation on real Indian bus data. carbonOrbit’s proposed difference is its explicit synthetic BMTC-route benchmark, event-level detection evaluation, and transparent separation of results from conditional emissions scenarios.

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
