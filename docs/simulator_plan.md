# Person B: GPS Simulator Plan

**Project:** carbonOrbit  
**Owner:** Rahul A.M. (Person B)  
**Status:** Initial design draft for team review; Phase 2 route inputs are documented in `data_sources.md`

## Goal

Generate reproducible, clearly synthetic bus position pings along selected BMTC GTFS routes. The simulator should create realistic variation and known delay/bunching events so the analytics work can be checked against ground-truth labels.

## Inputs

- Three routes from the pinned GTFS snapshot audited in `data_sources.md`: `BMTC:dd9ea3794c96` (285-M KBS-BMSIT), `BMTC:6f4d45186ddd` (285 BMSITY-YHKOT), and `BMTC:b202977c0fc0` (406). These provide route geometry and stop-sequence inputs only; simulated vehicle movement and event labels remain synthetic.
- Simulation settings in `config/simulation.yaml` (fixed random seed, date range, ping interval, bus counts, noise/dropout levels, and event settings).
- Route shapes when present; otherwise ordered stop coordinates, with the fallback documented.

## First prototype scope

Start small: one route, one service day, and a few simulated buses. Confirm that a bus follows the route in the right direction and that timestamps and coordinates are valid before scaling to the team target of at least 10 buses and three routes. The broader team plan proposes 30-second pings and 28 days of data; confirm storage size and run time with the API/data team before generating the full dataset.

## Simulation steps

1. Read route shape/stop coordinates and build a distance-along-route representation.
2. Assign synthetic bus IDs, service start times, and staggered departures.
3. Advance each bus along the route at a configurable speed profile; slow or pause at stops for dwell time.
4. Add controlled variation: time-of-day speed changes, dwell variation, GPS coordinate noise, and configurable missing-ping/dropout events.
5. Inject known delay and bunching scenarios with explicit start/end times and causes in the ground-truth labels.
6. Emit timestamped pings and separate event labels. Use fixed seeds so the same configuration reproduces the same run.
7. Save a run manifest with source GTFS snapshot identifier, config, seed, simulator version, and generated-file checksums.

## Suggested ping fields

`timestamp`, `bus_id`, `route_id`, `trip_id`, `latitude`, `longitude`, `speed_kmh`, `distance_along_route_m`, `is_dwell`, `is_delayed`, `is_bunched`, `is_gps_noisy`, `is_ping_missing`.

Missing pings cannot themselves appear as rows; represent them in a separate event/quality log with the expected time window and missing interval. Keep generation labels available for evaluation, but do not feed labels into prediction features.

## Validation checklist

- Coordinates stay near the selected route and move in the expected direction.
- Timestamps are ordered per bus and use an explicit timezone convention (UTC internally; convert to local time only for display).
- Speeds, stop dwell, headways, route lengths, and dropout rates are summarized in realism plots.
- Injected delay and bunching windows match the separate ground-truth event file.
- Fixed seed plus identical inputs/config produces identical output.
- Report output row count, simulated period, and any discarded or invalid records.

## Planned project files

- `docs/data_sources.md` — source audit and route selection record.
- `config/simulation.yaml` — reproducible simulation controls.
- `src/simulator/` — route loading, movement, noise/dropout, event labelling, and output.
- `tests/` — reproducibility and route/timestamp/label checks, coordinated with the team.
- `data/processed/` — generated data only if repository policy permits; otherwise generate locally and document the command/config.

## Decisions still needed from the team

- Decide whether to continue with the documented Vonter snapshot as the project geometry source. DULT was inaccessible on the audit date; the Vonter data is unofficial and its schedules must not be treated as observed service truth.
- Confirm bus count, simulation duration, ping interval, speed/dwell profiles, noise/dropout scenarios, and whether 28 days is practical.
- Agree the ping, trip, ground-truth event, and quality-log schemas with the API and analytics work before implementation.
- Approve the event-generation rules and keep simulator-only labels out of model features.
