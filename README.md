# carbonOrbit

Real-Time Bus Tracking and ETA Prediction for Sustainable Urban Mobility

## Summary
An open, reproducible project for bus arrival-time prediction, delay and
bus-bunching detection, and scenario-based environmental estimates. Its first
28-day synthetic evaluation is recorded in `docs/simulation_results.md`. It does
not validate live BMTC vehicle operations. Environmental outputs remain
assumption-based scenarios, not measured effects.

## Team
| Name | Role |
|------|------|
| R.Dhrutvan  | Backend, API, database, CI |
| Rahul A.M   | Data, simulator, reliability labels |
| L.Daneswar  | Dashboard, figures, testing |
| V.Rahul     | ETA models, emissions, statistics |

## Setup (Windows PowerShell)
    git clone https://github.com/thunderbolt3-14/carbonorbit.git
    cd carbonorbit
    py -3.12 -m venv venv
    .\venv\Scripts\Activate.ps1
    python -m pip install -r requirements-lock.txt

Python 3.12 is the recommended runtime for the locked dependency set. The pinned GTFS ZIP is not included in Git.
Download the archive pinned in `docs/data_sources.md` to
`data/raw/bmtc.zip`; the simulator checks its SHA-256 before reading it.
For the exact download URL, expected SHA-256, clean test commands, run configuration,
and release gates, see [`docs/release_baseline.md`](docs/release_baseline.md).

## Run the pipeline

    python scripts/carbonorbit.py all

This generates the normal synthetic run, trains and evaluates the ETA model
ladder on the declared chronological split, scores delay/bunching events, and
loads public artifacts into the local SQLite database.

For the normal, noisy-GPS, and high-dropout scenarios, applying the normal-run
selected model unchanged to the robustness runs:

    python scripts/carbonorbit.py suite

Start the local API and dashboard:

    python scripts/carbonorbit.py serve

Open http://127.0.0.1:5000. The dashboard and API display simulated or offline
evaluation artifacts only; they do not connect to live BMTC vehicles.

## Structure
- docs/ : literature survey, evaluation plan, SDG mapping, diary, report
- config/ : simulation, emissions and threshold settings
- data/ : raw (ignored) and processed route files
- src/ : simulator, api, analytics, common
- dashboard/ : simulated-service monitor and API-connected views
- notebooks/ and results/ : experiments, tables, figures
- tests/ and scripts/ : automated tests and run scripts

## Status
Phases 0–4 are complete for the current synthetic proof of concept. The
evaluation and regression suite passed (34 tests) on the preceding reviewed
implementation; the corrected normal/noisy-GPS/high-dropout run is reproducible.
After correcting event scoring, delay detection reached test F1 0.974 against
fixed 5-minute truth using validation-selected settings. Bunching could not be
scored because the configured truth rule produced no positive events. These
results do not establish live BMTC performance. Emissions remain unquantified
because compatible factors and observed passenger diversion are unavailable.
See `docs/phase_roadmap.md` for remaining Phase 5–6 work and
`docs/report/evidence/` for compact run artifacts.
