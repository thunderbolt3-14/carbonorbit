# Team Workflow

## Rules
- Never commit directly to main. Use a branch and open a Pull Request.
- Every PR needs one review from another member. The owner merges.
- Pull before you start: git checkout main && git pull
- Do not commit data/raw, .env, or API keys.

## Branch names
phaseN-short-description-yourname, e.g. phase3-simulator-ravi

## Commit messages
Phase N: what you did, e.g. Phase 3: add bus movement simulator

## Roles
- Member A (owner): backend, API, database, CI, release
- Member B: GTFS audit, simulator, reliability labels, external data check
- Member C: dashboard, figures, latency tests, SDG evidence
- Member D: ETA models, statistics, emissions, evaluation plan

## Weekly rhythm
- Monday: pull main, pick issues, branch
- Friday: review and merge PRs, diary entry with commit links, guide meeting notes
