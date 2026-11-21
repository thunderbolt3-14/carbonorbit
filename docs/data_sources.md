# Data Sources and Route Plan

**Project:** carbonOrbit — Real-Time Bus Tracking and ETA Prediction for Sustainable Urban Mobility  
**Status:** Static route audit complete; an independent BMTC GTFS-Realtime mirror is connected for live demo use; official BMTC feed access and licence remain unverified
**Reviewed:** 21 November 2026

## 1. Purpose

This project uses a real bus network as the geographic and timetable framework, simulated GPS observations for reproducible evaluation, and an independent GTFS-Realtime mirror for the live dashboard view. The independent mirror is not operated or endorsed by BMTC. Generated positions and delays remain simulated and must not be presented as observed BMTC vehicle operations. Official BMTC feed access and usage terms remain unverified.

## 2. Candidate route and timetable data

| Source | What it provides | Status and use | Caveats |
|---|---|---|---|
| [DULT Transport Data Hub](https://tdh.dult-karnataka.com/) | Karnataka transport open-data portal; BMTC open-data access is referenced by the Enroute partners | Checked on 20 November 2026; the portal returned a 502 gateway error, so no feed or licence terms could be verified | No official BMTC dataset or licence is claimed in this audit; re-check if access becomes available |
| [Vonter BMTC GTFS](https://github.com/Vonter/bmtc-gtfs) | Community-maintained GTFS schedule data for routes, stops, trips, shapes and timetables | **Selected reproducible fallback snapshot** at commit `a4702664d65bfbb37290a5f75effaa24ead1d9dd`; used for route geometry and stop sequences only | Explicitly unofficial and derived from Namma BMTC 2.0. The maintainer warns of inaccurate timetables/stop times, interpolated arrivals, and missing or failed routes/stops/timetables. It is not a live GPS feed. ODbL-1.0 applies; preserve attribution and assess share-alike obligations before redistributing adapted database contents. |
| [Mobility Database feed record](https://mobilitydatabase.org/feeds/gtfs/mdb-2595) | Catalog entry, feed validation, service dates and archived snapshots for the Vonter feed | Useful for reproducible discovery and validation; save the download date and archive used | It catalogs the community feed, so it does not make the source official or validate schedule accuracy. |
| [Reclaim Chennai India GTFS: Bengaluru BMTC GTFS-Realtime](https://github.com/reclaimchennai/India_GTFS#live-feeds-gtfs-realtime) | Vehicle positions, trip updates, and feed status JSON/protobuf endpoints | Connected to the dashboard through `/api/v1/live`; endpoints are documented as refreshed within about 15 seconds | Independent community-maintained mirror, not an official BMTC feed. Its static BMTC feed cites community GTFS and BMTC app routes. Check freshness and availability at runtime; do not describe this as an official or complete BMTC data service. |

### Live dashboard feed check (21 November 2026)

The dashboard polls `https://maps.reclaim.city/bengaluru/rt/status.json`, `vehicle_positions.json`, and `trip_updates.json` through the local Flask API every 15 seconds. The remote status endpoint responded successfully during this check, but reported **0 vehicles and 0 trip updates**. Therefore, the live integration is connected, but no live buses were available to display at the time of verification. The code reports empty/stale/unavailable states; it does not fill the live view with simulator data. Do not claim that live BMTC tracking was demonstrated until non-empty, fresh feed data is observed.

An industry announcement confirms Bengaluru's BMTC GTFS open-data initiative and points to the DULT portal, but it does not by itself establish the licence or exact dataset currently downloadable. We must record those from the portal/feed metadata when we access it.

## 3. Snapshot and audit record

The DULT portal returned a 502 gateway error when checked on 20 November 2026. No official DULT download or licence is claimed. The fallback archive was downloaded from the Vonter repository and matched against the pinned repository commit below. The feed README identifies it as unofficial, derived from Namma BMTC 2.0, and licensed under ODbL-1.0; it warns that schedules and stop timings may be inaccurate, some arrivals are interpolated, and some routes, stops, and timetables may be missing.

- Snapshot revision: [`a4702664d65bfbb37290a5f75effaa24ead1d9dd`](https://github.com/Vonter/bmtc-gtfs/tree/a4702664d65bfbb37290a5f75effaa24ead1d9dd)
- Pinned archive URL: `https://raw.githubusercontent.com/Vonter/bmtc-gtfs/a4702664d65bfbb37290a5f75effaa24ead1d9dd/gtfs/bmtc.zip`
- Download/audit date: 20 November 2026
- Feed version and dates from `feed_info.txt`: version `20261109`, feed start `20261109`, feed end `20271109`
- Archive size: 92,988,913 bytes; SHA-256: `812c7d472ff116024ca1e0a7ff6e28662f762ca09265da8d5c7e9f6241cf8a45`
- Archive contents: 12 GTFS text files; 5,063 routes, 10,128 stops, 69,642 trips, and 2,238,693 stop-time rows
- Local consistency checks: route, stop, and trip IDs are unique; stop-time rows have positive numeric sequences with no duplicate `(trip_id, stop_sequence)` pairs; no stop-time rows reference unknown trips or stops; all trip shape references resolve. This is a project-level sanity check, **not** a pass from an official GTFS validator.
- Stop coordinate extent: latitude 12.548240–13.484340, longitude 77.029410–77.958580
- Licence: repository README and `LICENSE` state ODbL-1.0; retain attribution and assess share-alike requirements before redistribution. Some individual contents may be BMTC copyright.
- Local storage: the raw archive is kept in ignored `data/raw/` and is not committed to this project repository.

The approximate BMSIT campus reference point (13.134592, 77.568169) is from a geotagged photograph in the official BMSIT&M February 2025 newsletter. Distances below are straight-line Haversine distances, not walking distances.

Keep the original snapshot unchanged. Put any cleaned or filtered derivative in the processed-data area and document the transformation script and source snapshot.

## 4. Route selection method

The team plan calls for three BMTC routes near BMSIT. For this audit, route IDs were selected from the pinned snapshot rather than guessed. The selection method was:

1. Find BMSIT&M's approximate coordinates and inspect nearby GTFS stops.
2. List routes serving those stops; select three with usable stop sequences and shape geometry.
3. Prefer routes with enough stops and a mix of shorter and longer trips for a useful demo.
4. Record each route's GTFS `route_id`, public route short name, start/end or headsign, stop count, shape availability, and the nearest stop's distance from campus.
5. Check the chosen schedules and stop order against the source's caveats; treat schedules as route context, not ground truth for simulated vehicle movement.

| GTFS route ID | Public route name | Direction / termini | Stops | Shape available? | Nearest stop to BMSIT (distance) | Selection note |
|---|---|---|---:|---|---|---|
| `BMTC:dd9ea3794c96` | 285-M KBS-BMSIT | BMSIT College Campus Yelahanka ⇔ Kempegowda Bus Station (Majestic/KBS) | 53 | Yes (100% of listed trips) | BMSIT College Campus Yelahanka (0.099 km) | Direct campus service; two directions, 5 trips in snapshot; longer route |
| `BMTC:6f4d45186ddd` | 285 BMSITY-YHKOT | BMSIT College Campus Yelahanka ⇔ Yelahanka Old Town | 21 | Yes (100% of listed trips) | BMSIT College Campus Yelahanka (0.099 km) | Direct campus service; two directions, 2 trips in snapshot; shorter route |
| `BMTC:b202977c0fc0` | 406 | Nelamangala Bus Station ⇔ NES Office | 110 | Yes (100% of listed trips) | Avalahalli Doddaballapura Road (0.132 km) | Nearby route; two directions and 15 trips in snapshot; adds a longer route with broader trip representation |

The direct 500-D CSB-BMSIT route was considered but not selected because the snapshot contains only one trip in one direction for it. Stop counts are unique stops across a route's listed trips. Snapshot trip counts do not establish current BMTC service frequency.

## 5. Data boundary and ethics

- Real input: published route, stop, shape, and schedule records from the documented GTFS snapshot.
- Synthetic input: bus IDs, timestamped positions, speeds, dwell events, delays, GPS noise, missing pings, and event labels.
- No real passenger identities or passenger-level records are needed. Passenger demand, if modeled, should be synthetic and aggregated.
- Do not claim that simulated reliability improvements caused measured emissions reductions. Environmental outcomes are scenario estimates described by the full team.
- Attribute the data source and follow its licence if distributing any source-derived or adapted files.

## References

1. Directorate of Urban Land Transport, Karnataka, [Transport Data Hub](https://tdh.dult-karnataka.com/), checked 20 November 2026; portal returned a 502 gateway error. No dataset or licence terms verified.
2. Vonter, [bmtc-gtfs: Unofficial GTFS dataset for BMTC](https://github.com/Vonter/bmtc-gtfs/tree/a4702664d65bfbb37290a5f75effaa24ead1d9dd), snapshot revision accessed 20 November 2026. The pinned README and license document provenance, caveats, and ODbL-1.0 licensing.
3. MobilityData, [Mobility Database: BMTC GTFS feed (mdb-2595)](https://mobilitydatabase.org/feeds/gtfs/mdb-2595), accessed 19 November 2026. This catalog entry does not make the community feed official or establish schedule accuracy.
4. Mercedes-Benz Research and Development India, WRI India, and Villgro, [“Open Data Fuels Bengaluru’s First-Ever End-to-End Public Transport App Solutions”](https://www.mbrdi.co.in/assets/docs/Open%20Data%20Fuels%20Bengaluru%E2%80%99s%20First-Ever%20End-to-End%20Public%20Transport%20App%20Solutions.pdf), 10 July 2025.
5. BMS Institute of Technology & Management, [February 2025 newsletter](https://bmsit.ac.in/pdf/newsletter/Feb%202025.pdf), used only for an approximate geotagged campus reference point.
6. Reclaim Chennai, [India GTFS repository and GTFS-Realtime endpoint documentation](https://github.com/reclaimchennai/India_GTFS#live-feeds-gtfs-realtime), accessed 21 November 2026. Independent service; its stated refresh interval and endpoint availability are not a BMTC service-level guarantee or authorization.
