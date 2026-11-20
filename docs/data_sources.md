# Data Sources and Route Plan

**Project:** carbonOrbit — Real-Time Bus Tracking and ETA Prediction for Sustainable Urban Mobility  
**Status:** Source review complete; route-level audit blocked pending retrieval of a reproducible feed snapshot
**Reviewed:** 19 November 2026

## 1. Purpose

This project needs a real bus network as the geographic and timetable framework, plus simulated GPS observations for testing. We do not currently have access to a verified live BMTC GPS feed. Therefore, generated positions and delays must be clearly labelled as simulated; they must not be presented as observed BMTC vehicle operations.

## 2. Candidate route and timetable data

| Source | What it provides | Status and use | Caveats |
|---|---|---|---|
| [DULT Transport Data Hub](https://tdh.dult-karnataka.com/) | Karnataka transport open-data portal; BMTC open-data access is referenced by the Enroute partners | **Check first** for a downloadable BMTC feed and its licence/access terms before selecting the project snapshot | Portal access, feed version, permitted use, and whether vehicle positions are available have not yet been verified for this project |
| [Vonter BMTC GTFS](https://github.com/Vonter/bmtc-gtfs) | Community-maintained GTFS schedule data for routes, stops, trips, shapes and timetables | **Practical fallback** for route geometry and stop sequences if the team records the exact downloaded snapshot and licence | Explicitly unofficial. Its maintainer warns that the upstream Namma BMTC 2.0 information has incorrect schedules and stop timings; some times are interpolated. It is not a live GPS feed. Repository states ODbL-1.0; preserve attribution and check share-alike obligations before redistributing adapted database contents. |
| [Mobility Database feed record](https://mobilitydatabase.org/feeds/gtfs/mdb-2595) | Catalog entry, feed validation, service dates and archived snapshots for the Vonter feed | Useful for reproducible discovery and validation; save the download date and archive used | It catalogs the community feed, so it does not make the source official or validate schedule accuracy. |

An industry announcement confirms Bengaluru's BMTC GTFS open-data initiative and points to the DULT portal, but it does not by itself establish the licence or exact dataset currently downloadable. We must record those from the portal/feed metadata when we access it.

## 3. Snapshot and audit record

The DULT portal could not be independently opened during this review (gateway error), so no DULT download or licence is claimed. The community feed repository was reviewed on 19 November 2026. Its README states that it is unofficial, sourced from the Namma BMTC 2.0 app, and distributed under ODbL-1.0; it also warns that timetables and stop timings may be inaccurate, arrival times may be interpolated, and some routes, stops, and timetables may be missing. This identifies it as a candidate, but does not establish that a particular snapshot was downloaded, validated, or audited.

- Download URL: no archive downloaded in this review; repository points to `https://raw.githubusercontent.com/Vonter/bmtc-gtfs/main/gtfs/bmtc.zip`
- Review date: 19 November 2026 (source pages); archive download date: not recorded
- Feed version / service date range: not verified from a local archive
- Licence: repository README states ODbL-1.0; assess attribution and share-alike duties before distributing adapted data
- SHA-256 checksum: unavailable (no archive downloaded)
- GTFS files and validator result: not independently inspected; no validation result claimed
- Known source limitations: unofficial upstream app; inaccurate schedules/stop times; interpolated arrival times; known missing/failed routes, stops, timetables, and fare information
- Local storage: no raw feed stored

Mobility Database catalogues this community feed and may provide dated archives and validation metadata; catalog validation does not establish schedule accuracy or official status. Record the current archive and service dates when a team member downloads a snapshot.

The route-selection table remains unfilled. The feed's CSV summaries are too large for the connected repository reader, and direct raw-file download was unavailable in this environment. No route IDs, nearest-stop distances, or shape coverage have been invented. A team member should download a dated archive, verify the campus point against the official BMSIT&M location, then complete the audit before routes are frozen.

Keep the original snapshot unchanged. Put any cleaned or filtered derivative in the processed-data area and document the transformation script and source snapshot.

## 4. Route selection method

The team plan calls for three BMTC routes near BMSIT. Route IDs should be selected from the chosen snapshot rather than guessed. After downloading the feed:

1. Find BMSIT&M's approximate coordinates and inspect nearby GTFS stops.
2. List routes serving those stops; select three with usable stop sequences and shape geometry.
3. Prefer routes with enough stops and a mix of shorter and longer trips for a useful demo.
4. Record each route's GTFS `route_id`, public route short name, start/end or headsign, stop count, shape availability, and the nearest stop's distance from campus.
5. Check the chosen schedules and stop order against the source's caveats; treat schedules as route context, not ground truth for simulated vehicle movement.

| GTFS route ID | Public route name | Direction / termini | Stops | Shape available? | Nearest stop to BMSIT (distance) | Selection note |
|---|---|---|---:|---|---|---|
| Pending dated feed audit | | | | | | |
| Pending dated feed audit | | | | | | |
| Pending dated feed audit | | | | | | |

## 5. Data boundary and ethics

- Real input: published route, stop, shape, and schedule records from the documented GTFS snapshot.
- Synthetic input: bus IDs, timestamped positions, speeds, dwell events, delays, GPS noise, missing pings, and event labels.
- No real passenger identities or passenger-level records are needed. Passenger demand, if modeled, should be synthetic and aggregated.
- Do not claim that simulated reliability improvements caused measured emissions reductions. Environmental outcomes are scenario estimates described by the full team.
- Attribute the data source and follow its licence if distributing any source-derived or adapted files.

## References

1. Directorate of Urban Land Transport, Karnataka, [Transport Data Hub](https://tdh.dult-karnataka.com/), accessed 19 November 2026. Dataset and licence details pending direct feed audit.
2. Vonter, [bmtc-gtfs: Unofficial GTFS dataset for BMTC](https://github.com/Vonter/bmtc-gtfs), accessed 19 November 2026. Repository README documents provenance, limitations and ODbL-1.0 licensing; no archive was downloaded for this audit.
3. MobilityData, [Mobility Database: BMTC GTFS feed (mdb-2595)](https://mobilitydatabase.org/feeds/gtfs/mdb-2595), accessed 19 November 2026.
4. Mercedes-Benz Research and Development India, WRI India, and Villgro, [“Open Data Fuels Bengaluru’s First-Ever End-to-End Public Transport App Solutions”](https://www.mbrdi.co.in/assets/docs/Open%20Data%20Fuels%20Bengaluru%E2%80%99s%20First-Ever%20End-to-End%20Public%20Transport%20App%20Solutions.pdf), 10 July 2025.
