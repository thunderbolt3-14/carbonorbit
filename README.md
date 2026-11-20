# carbonOrbit

Real-Time Bus Tracking and ETA Prediction for Sustainable Urban Mobility

## Summary
An open, reproducible project plan for bus arrival-time prediction, delay and
bus-bunching detection, and scenario-based environmental estimates. The proposed
evaluation uses synthetic GPS on BMTC route geometry; no simulator results or live
BMTC vehicle-data validation are available yet. Environmental outputs will be
assumption-based estimates, not measured effects.

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
Phase 0 and the Phase 1 research-document set are complete. Phase 2 has a pinned
community GTFS snapshot, three audited routes, a proposed evaluation plan, and
an initial implementation foundation for simulation, the API, analytics,
emissions scenarios, and the dashboard. Runtime results have not been produced
in this checkout: the archive is local-only, dependencies may need installation,
and the protocol remains subject to team/guide review. Emissions factor values
are intentionally unset until compatible sources are recorded. See
`docs/phase_roadmap.md` for remaining validation and approval gates.
