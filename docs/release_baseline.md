# Reproducibility and release baseline

**Prepared:** 21 November 2026. **Current repository baseline:** `main` at `79f8b3a`; PRs #24, #25, and #26 are merged. **Evaluation run:** `88d1eb4fc1efd6c1`. **Run evidence:** [`report/evidence/88d1eb4fc1efd6c1/`](report/evidence/88d1eb4fc1efd6c1/).

This documents a reviewable baseline for the synthetic proof of concept. It is not a release tag. The recorded evaluation used the simulator and analysis implementation included in the run evidence's commit history; later main commits correct event scoring and associated report files. All current project PRs are merged. A project owner can decide whether to tag the synthetic prototype after reviewing the report and evidence. A tag must not imply live-service validation.

## Environment

- Python: 3.12.0 (Windows clean virtual environment)
- Dependency file: `requirements-lock.txt`
- Dependency-lock SHA-256: `C6A6C7BED1B1BAF4956C37078B63E78D343A89A8AF12B1A1BE37AD33F6E1CA96`
- GTFS revision: `a4702664d65bfbb37290a5f75effaa24ead1d9dd`
- GTFS archive SHA-256: `812c7d472ff116024ca1e0a7ff6e28662f762ca09265da8d5c7e9f6241cf8a45`
- Raw GTFS ZIP: download locally to `data/raw/bmtc.zip`; it is not committed.

## Clean setup and verification (Git Bash)

Use a fresh clone directory for this reproduction. The pipeline writes generated run files under `data/simulated/`, evaluation files under `results/generated/`, and the local database at `data/carbonorbit.db`. It does not use the top-level `output/` directory. Avoid reusing a working folder with untracked generated results you need to preserve.

```bash
git clone https://github.com/thunderbolt3-14/carbonorbit.git
cd carbonorbit
git switch main
git pull --ff-only origin main
git rev-parse --short HEAD
py -3.12 -m venv venv
source venv/Scripts/activate
python -m pip install -r requirements-lock.txt
python -m pytest -q
```

Download and verify the exact GTFS snapshot:

```bash
mkdir -p data/raw
curl -L 'https://raw.githubusercontent.com/Vonter/bmtc-gtfs/a4702664d65bfbb37290a5f75effaa24ead1d9dd/gtfs/bmtc.zip' -o data/raw/bmtc.zip
echo '812c7d472ff116024ca1e0a7ff6e28662f762ca09265da8d5c7e9f6241cf8a45  data/raw/bmtc.zip' | sha256sum -c -
python scripts/carbonorbit.py suite
```

The test command should report 34 passing tests for the current baseline. The synthetic suite takes several minutes and writes its run files under `data/simulated/`, evaluation outputs under `results/generated/`, and the local API database at `data/carbonorbit.db`. To open the local dashboard after the suite:

```bash
python scripts/carbonorbit.py serve --host 127.0.0.1 --port 5000
```

Then open `http://127.0.0.1:5000/` in a browser. Stop the server with `Ctrl+C` in the Git Bash window. The dashboard opens in independent GTFS-Realtime mode; click **Simulator** to view stored synthetic artifacts. The community feed is not official BMTC data and may be empty or unavailable. The live mode must not be used as evidence of BMTC operational accuracy; see `docs/data_sources.md` for source and verification status.

On native PowerShell, use `py -3.12 -m venv venv`, `venv\\Scripts\\Activate.ps1`, `Invoke-WebRequest` for the URL above, and `(Get-FileHash data/raw/bmtc.zip -Algorithm SHA256).Hash` to check the archive against the recorded hash. The simulator also checks the pinned input hash.

For the recorded normal run, the seed is `20261109`, period is 9 November–6 December 2026, and the chronological split is 18 train / 5 validation / 5 test days. `python scripts/carbonorbit.py suite` generates normal, noisy-GPS, and high-dropout scenarios. Full-size raw and generated data stay in ignored local folders; compact summaries, charts, and manifests are committed with the evidence package.

## Recorded verification

- Automated suite: 34 tests passed in a clean Python 3.12.0 environment.
- Repeat-run check: normal-run output checksums matched for all 8 generated files; details in `reproducibility_check.json`.
- Dashboard/API integration: manual populated-dashboard check recorded in `simulation_results.md`.
- API latency: 50 serial requests per endpoint against the local Flask development server; endpoint p95s were below the 1,000 ms target. This is not production load evidence.
- Emissions: intentionally unquantified. No compatible approved factors or observed diversion/activity data were available.
- Evaluation boundary: all service traces, telemetry, arrivals, and event labels in this run are synthetic; the GTFS archive provides route/schedule context only.

## Release decision

No PR merge gate remains. Before tagging or externally presenting the project, the project owner should review the corrected report, verify the evidence links render, and accept the recorded citation and evaluation limits. A tag may identify the synthetic proof of concept; it must not state or imply that live BMTC, passenger diversion, emissions reduction, or bunching detection was validated. Production load testing is needed only if a deployment target is planned.
