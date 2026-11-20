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

## Setup (Windows, Git Bash)
    git clone https://github.com/thunderbolt3-14/carbonorbit.git
    cd carbonorbit
    python -m venv venv
    source venv/Scripts/activate
    pip install -r requirements.txt
    python -m pytest -q

## Structure
- docs/ : literature survey, evaluation plan, SDG mapping, diary, report
- config/ : simulation, emissions and threshold settings
- data/ : raw (ignored) and processed route files
- src/ : simulator, api, analytics, common
- dashboard/ : live map and charts
- notebooks/ and results/ : experiments, tables, figures
- tests/ and scripts/ : automated tests and run scripts

## Status
Phase 0 is complete. Phase 1's shared research documents are merged, and the
Phase 2 data audit has pinned a community GTFS snapshot and selected three
routes. The evaluation plan and simulator plan are still drafts: simulation
settings, data/API contracts, event thresholds, emissions inputs, and team/guide
review must be settled before implementation and protocol freeze. See
`docs/phase_roadmap.md` for the ordered remaining work.
