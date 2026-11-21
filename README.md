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

Open http://127.0.0.1:5000. The dashboard opens in **Live feed** mode and polls
an independent Bengaluru GTFS-Realtime mirror every 15 seconds. It displays
vehicle positions and stop arrival predictions when that source publishes them.
The source is not an official BMTC feed. Use **Simulator** to view the stored
synthetic run and its evaluation metrics. The live feed can be empty or
unavailable; the dashboard reports its status instead of substituting simulated
vehicles into the live view.

The live API is available at `/api/v1/live`. The source endpoints, attribution,
and current verification limits are recorded in `docs/data_sources.md`.

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
corrected normal/noisy-GPS/high-dropout run is reproducible and the merged
regression suite passed (34 tests).
After correcting event scoring, delay detection reached test F1 0.974 against
fixed 5-minute truth using validation-selected settings. Bunching could not be
scored because the configured truth rule produced no positive events. These
results do not establish live BMTC performance. Emissions remain unquantified
because compatible factors and observed passenger diversion are unavailable.
Phase 5 has an initial local dashboard/API review. Phase 6's report and evidence
package are prepared; a project-owner release review remains. See `docs/phase_roadmap.md` and
`docs/report/evidence/` for compact run artifacts.
