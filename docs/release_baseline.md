# Reproducibility and release baseline

**Prepared:** 21 November 2026. **Evaluation run:** `88d1eb4fc1efd6c1`. **Base repository commit:** `b4172ab6d518960047a631f00a29dc447c0d1c72`. **Run evidence:** [`report/evidence/88d1eb4fc1efd6c1/`](report/evidence/88d1eb4fc1efd6c1/).

This is the review baseline for the initial synthetic evaluation, not a release tag. The evidence is tied to the run manifest and source revision above. Team review and merge of the accompanying pull request(s) must happen before a release tag or publication.

## Environment

- Python: 3.12.0 (Windows clean virtual environment)
- Dependency file: `requirements-lock.txt`
- Dependency-lock SHA-256: `C6A6C7BED1B1BAF4956C37078B63E78D343A89A8AF12B1A1BE37AD33F6E1CA96`
- GTFS revision: `a4702664d65bfbb37290a5f75effaa24ead1d9dd`
- GTFS archive SHA-256: `812c7d472ff116024ca1e0a7ff6e28662f762ca09265da8d5c7e9f6241cf8a45`
- Raw GTFS ZIP: download locally to `data/raw/bmtc.zip`; it is not committed.

## Clean setup and verification (Git Bash)

```bash
git clone https://github.com/thunderbolt3-14/carbonorbit.git
cd carbonorbit
git checkout <reviewed-commit-or-branch>
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

On native PowerShell, use `py -3.12 -m venv venv`, `venv\\Scripts\\Activate.ps1`, `Invoke-WebRequest` for the URL above, and `(Get-FileHash data/raw/bmtc.zip -Algorithm SHA256).Hash` to check the archive against the recorded hash. The simulator also checks the pinned input hash.

For the recorded normal run, the seed is `20261109`, period is 9 November–6 December 2026, and the chronological split is 18 train / 5 validation / 5 test days. `python scripts/carbonorbit.py suite` generates normal, noisy-GPS, and high-dropout scenarios. Full-size raw and generated data stay in ignored local folders; compact summaries, charts, and manifests are committed with the evidence package.

## Recorded verification

- Automated suite: 34 tests passed in a clean Python 3.12.0 environment.
- Repeat-run check: normal-run output checksums matched for all 8 generated files; details in `reproducibility_check.json`.
- Dashboard/API integration: manual populated-dashboard check recorded in `simulation_results.md`.
- API latency: 50 serial requests per endpoint against the local Flask development server; endpoint p95s were below the 1,000 ms target. This is not production load evidence.
- Emissions: intentionally unquantified. No compatible approved factors or observed diversion/activity data were available.
- Evaluation boundary: all service traces, telemetry, arrivals, and event labels in this run are synthetic; the GTFS archive provides route/schedule context only.

## Release gate

Release tag and external publication are deferred until the team reviews and merges the evidence and documentation PRs, and records any required full-text citation access. No live-service or SDG impact claim may be added based on this simulation alone.
