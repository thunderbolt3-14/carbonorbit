# SDG Indicator Mapping: carbonOrbit

Project: Real-Time Bus Tracking and ETA Prediction for Sustainable Urban Mobility
Goals: SDG 11, SDG 13 (supporting: SDG 9)

| Indicator / project proxy | Justification and scope | Initiation | Implementation evidence | Impact evidence / status |
|-----------|---------------|------------|----------------|--------|
| 11.2.1 Convenient access to public transport (project proxy only) | ETA error is an engineering proxy; it does not measure population access, affordability, or convenience | Phase 1: problem framing and literature | Synthetic ETA and dashboard pipeline; test share within 2 minutes is 98.86% | No SDG indicator value or user access impact measured; simulation evidence only |
| 11.6.2 Annual mean PM2.5 | Ambient city concentration requires monitoring/inventory evidence; no concentration or mode shift is measured | Phase 1: literature | Emissions interface exists; factors remain unset | No PM2.5 impact estimate; unquantified by design |
| 13.2.2 Total greenhouse gas emissions | National inventory indicator cannot be derived from this route simulator; no observed diversion or compatible approved factors | Phase 1: literature | Emissions scenario interface; factor register retains no numeric factors | No GHG inventory contribution or reduction quantified |
| 9.1.2 Passenger and freight volumes | This project does not currently measure passenger or freight volumes | Phase 1: scope definition | Route and synthetic vehicle analytics only | Not measured; ETA predictions are not passenger-volume evidence |

## Evidence log
| Date | Phase | Stage (Initiation/Implementation/Impact) | Evidence (commit or PR link, screenshot, dataset) |
|------|-------|------------------------------------------|---------------------------------------------------|
| 21 Nov 2026 | 6 | Implementation evidence; no impact claim | Synthetic evaluation run `88d1eb4fc1efd6c1`; manifest, metrics, uncertainty, figures, and validation outputs in `report/evidence/88d1eb4fc1efd6c1/`; report in `report/final_report.md` |
| 21 Nov 2026 | 6 | Implementation evidence; no impact claim | Local API/dashboard integration and latency check (50 serial requests per endpoint; p95 below 1 s) in `report/evidence/88d1eb4fc1efd6c1/api_latency.json`; not a production load test |
| 21 Nov 2026 | 6 | Impact | No impact evidence available: no live BMTC operation, passenger access survey, passenger counts/diversion, ambient PM2.5, or fleet-level GHG inventory was measured |
