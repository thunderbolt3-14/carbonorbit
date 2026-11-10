cat > README.md << 'EOF'
# carbonOrbit

Real-Time Bus Tracking and ETA Prediction for Sustainable Urban Mobility

BMSIT&M | V Sem Environmental Science Mini Project | SDG 11, SDG 13

## Summary
An open, reproducible pipeline that predicts bus arrival times, detects delays and
bus bunching, and estimates the CO2 and PM implications of better transit information.
Validated on simulated GPS over real BMTC routes. All environmental results are
scenario-based estimates, not measurements.

## Team
| Name | USN | Role |
|------|-----|------|
| (Owner) | | Backend, API, database, CI |
| | | Data, simulator, reliability labels |
| | | Dashboard, figures, testing |
|Rahul v |1BY24CS332 | ETA models, emissions, statistics |

Guide: (name)

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
Phase 0: repository and workflow set up.
