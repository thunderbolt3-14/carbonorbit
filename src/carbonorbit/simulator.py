"""Seeded GTFS-based bus movement simulation with separate labels."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import random
from collections import defaultdict
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from .gtfs import GTFSFeed, Trip, iter_days, load_gtfs

UTC = timezone.utc


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _utc(service_day: date, seconds: float, timezone_name: str) -> datetime:
    local_start = datetime.combine(service_day, time.min, ZoneInfo(timezone_name))
    return (local_start + timedelta(seconds=seconds)).astimezone(UTC)


def _stamp(value: datetime) -> str:
    return value.isoformat(timespec="seconds").replace("+00:00", "Z")


def _distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 6_371_000 * 2 * math.asin(min(1.0, math.sqrt(h)))


def _projected_shape(feed: GTFSFeed, trip: Trip) -> list[int]:
    """Find monotonically ordered nearest shape vertices for each trip stop."""
    shape = feed.shapes.get(trip.shape_id, [])
    if not shape:
        return []
    indices, floor_index = [], 0
    for item in trip.stop_times:
        stop = feed.stops[item.stop_id]
        nearest = min(range(floor_index, len(shape)), key=lambda i: _distance((stop.lat, stop.lon), shape[i]))
        indices.append(nearest)
        floor_index = nearest
    return indices


def _leg_line(feed: GTFSFeed, trip: Trip, leg_index: int, shape_indices: list[int]) -> list[tuple[float, float]]:
    start = feed.stops[trip.stop_times[leg_index].stop_id]
    end = feed.stops[trip.stop_times[leg_index + 1].stop_id]
    shape = feed.shapes.get(trip.shape_id, [])
    if shape and shape_indices and shape_indices[leg_index] < shape_indices[leg_index + 1]:
        part = shape[shape_indices[leg_index]:shape_indices[leg_index + 1] + 1]
        return [(start.lat, start.lon), *part, (end.lat, end.lon)]
    return [(start.lat, start.lon), (end.lat, end.lon)]


def _line_measure(line: list[tuple[float, float]]) -> tuple[list[float], float]:
    cumulative = [0.0]
    for first, second in zip(line, line[1:]):
        cumulative.append(cumulative[-1] + _distance(first, second))
    return cumulative, cumulative[-1]


def _at_fraction(line: list[tuple[float, float]], cumulative: list[float], total: float, fraction: float) -> tuple[float, float]:
    if total <= 0:
        return line[0]
    target = max(0.0, min(1.0, fraction)) * total
    for index in range(1, len(cumulative)):
        if cumulative[index] >= target:
            span = cumulative[index] - cumulative[index - 1]
            ratio = 0.0 if span == 0 else (target - cumulative[index - 1]) / span
            a, b = line[index - 1], line[index]
            return a[0] + ratio * (b[0] - a[0]), a[1] + ratio * (b[1] - a[1])
    return line[-1]


def _noise(lat: float, lon: float, sigma_m: float, rng: random.Random) -> tuple[float, float, float]:
    offset = rng.gauss(0.0, sigma_m) if sigma_m else 0.0
    angle = rng.random() * math.tau
    lat_delta = offset * math.cos(angle) / 111_320
    lon_scale = max(1.0, 111_320 * abs(math.cos(math.radians(lat))))
    lon_delta = offset * math.sin(angle) / lon_scale
    return lat + lat_delta, lon + lon_delta, abs(offset)


def _write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _config_signature(config: dict, actual_gtfs_sha: str, scenario: str) -> str:
    payload = {
        "project": config["project"],
        "simulation": config["simulation"],
        "scenario": scenario,
        "gtfs_sha256": actual_gtfs_sha,
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:16]


def simulate(config: dict, scenario_name: str = "normal", output_root: str | Path = "data/simulated") -> Path:
    project, base, scenarios = config["project"], config["simulation"], config.get("scenarios", {})
    if scenario_name not in scenarios:
        raise ValueError(f"Unknown scenario {scenario_name!r}; choose one of {', '.join(sorted(scenarios))}")
    settings = {**base, **scenarios[scenario_name]}
    gtfs_path = Path(project["gtfs_path"])
    if not gtfs_path.is_file():
        raise FileNotFoundError(f"GTFS ZIP not found at {gtfs_path}; the pinned archive is intentionally not stored in Git")
    archive_hash = _sha256(gtfs_path)
    expected_hash = project.get("gtfs_sha256")
    if expected_hash and archive_hash.lower() != expected_hash.lower():
        raise ValueError(f"GTFS SHA-256 mismatch: expected {expected_hash}, found {archive_hash}")
    run_id = _config_signature(config, archive_hash, scenario_name)

    feed = load_gtfs(gtfs_path, project["route_ids"], project["gtfs_revision"])
    local_tz = project.get("timezone", "Asia/Kolkata")
    start_day = date.fromisoformat(settings["start_date"])
    rng = random.Random(int(settings["seed"]))
    interval = int(settings["ping_interval_seconds"])
    dropout = float(settings["ping_dropout_probability"])
    noise_std = float(settings["gps_noise_std_m"])
    event_rules = settings["event_rules"]
    delay_labels, pings, eta_labels = [], [], []
    stop_truth, stop_observations, quality_log = [], [], []

    for service_day in iter_days(start_day, int(settings["days"])):
        active = feed.active_service_ids(service_day)
        for trip in feed.trips:
            if trip.service_id not in active:
                continue
            stop_times = trip.stop_times
            trip_rng = random.Random(rng.getrandbits(64))
            bus_id = f"sim-{trip.route_id}-{trip.trip_id}"
            shape_indices = _projected_shape(feed, trip)
            scheduled_arrivals = [item.arrival_seconds for item in stop_times]
            actual_arrivals = [float(scheduled_arrivals[0])]
            actual_departures = []
            delay_start = None
            persistent_delay = 0.0
            if len(stop_times) > 2 and trip_rng.random() < float(settings["delay_injection_probability"]):
                delay_start = trip_rng.randint(1, len(stop_times) - 1)
                persistent_delay = trip_rng.uniform(float(settings["delay_minutes_min"]), float(settings["delay_minutes_max"])) * 60

            for stop_index, scheduled in enumerate(stop_times):
                if stop_index > 0:
                    previous = stop_times[stop_index - 1]
                    schedule_leg = max(30, scheduled.arrival_seconds - previous.departure_seconds)
                    factor = trip_rng.uniform(float(settings["travel_time_factor_min"]), float(settings["travel_time_factor_max"]))
                    leg_seconds = max(20.0, schedule_leg * factor)
                    actual_arrivals.append(actual_departures[-1] + leg_seconds)
                    if delay_start is not None and stop_index == delay_start:
                        actual_arrivals[-1] += persistent_delay
                    elif delay_start is not None and stop_index > delay_start and persistent_delay:
                        recovery = min(persistent_delay * 0.08, max(0.0, leg_seconds - 20.0))
                        actual_arrivals[-1] -= recovery
                        persistent_delay -= recovery

                dwell = max(0.0, scheduled.departure_seconds - scheduled.arrival_seconds)
                dwell += trip_rng.uniform(float(settings["dwell_seconds_min"]), float(settings["dwell_seconds_max"]))
                actual_departures.append(actual_arrivals[stop_index] + dwell)

                exact = _utc(service_day, actual_arrivals[stop_index], local_tz)
                scheduled_dt = _utc(service_day, scheduled.arrival_seconds, local_tz)
                stop_truth.append({
                    "run_id": "", "service_date": service_day.isoformat(), "route_id": trip.route_id,
                    "trip_id": trip.trip_id, "bus_id": bus_id, "direction_id": trip.direction_id,
                    "stop_id": scheduled.stop_id, "stop_sequence": scheduled.stop_sequence,
                    "scheduled_arrival_utc": _stamp(scheduled_dt), "actual_arrival_utc": _stamp(exact),
                    "delay_minutes": round((exact - scheduled_dt).total_seconds() / 60, 4),
                })

                measured = exact + timedelta(seconds=trip_rng.uniform(-interval / 2, interval / 2))
                if trip_rng.random() >= dropout:
                    stop_observations.append({
                        "run_id": "", "service_date": service_day.isoformat(), "route_id": trip.route_id,
                        "trip_id": trip.trip_id, "bus_id": bus_id, "direction_id": trip.direction_id,
                        "stop_id": scheduled.stop_id, "stop_sequence": scheduled.stop_sequence,
                        "scheduled_arrival_utc": _stamp(scheduled_dt), "observed_arrival_utc": _stamp(measured),
                        "lat": feed.stops[scheduled.stop_id].lat, "lon": feed.stops[scheduled.stop_id].lon,
                    })
                else:
                    quality_log.append({
                        "run_id": "", "service_date": service_day.isoformat(), "bus_id": bus_id,
                        "route_id": trip.route_id, "trip_id": trip.trip_id,
                        "expected_timestamp_utc": _stamp(exact),
                        "quality_event": "stop_observation_dropout", "interval_seconds": interval,
                    })

            trip_truth = stop_truth[-len(stop_times):]
            delay_values = [float(row["delay_minutes"]) for row in trip_truth]
            if max(delay_values, default=0) >= float(event_rules["delay_minutes"]):
                first = next((row for row in trip_truth if float(row["delay_minutes"]) >= float(event_rules["delay_minutes"])), trip_truth[-1])
                delay_labels.append({
                    "event_id": hashlib.sha1(f"{run_id}|{service_day}|{trip.trip_id}|delay".encode()).hexdigest()[:20],
                    "run_id": "", "event_type": "delay", "service_date": service_day.isoformat(),
                    "route_id": trip.route_id, "trip_id": trip.trip_id, "bus_id": bus_id,
                    "related_bus_id": "", "stop_id": first["stop_id"],
                    "start_utc": first["actual_arrival_utc"], "end_utc": trip_truth[-1]["actual_arrival_utc"],
                    "severity": round(max(delay_values), 3), "rule_version": "delay-v1",
                })

            for leg_index in range(len(stop_times) - 1):
                start_stop, end_stop = stop_times[leg_index], stop_times[leg_index + 1]
                depart, arrive = actual_departures[leg_index], actual_arrivals[leg_index + 1]
                duration = max(1.0, arrive - depart)
                line = _leg_line(feed, trip, leg_index, shape_indices)
                cumulative, leg_distance = _line_measure(line)
                leg_distance = max(1.0, leg_distance)
                n_steps = max(1, int(math.ceil(duration / interval)))
                for step in range(n_steps):
                    sample_seconds = depart + min(step * interval, duration - 0.001)
                    timestamp = _utc(service_day, sample_seconds, local_tz)
                    if step and trip_rng.random() < dropout:
                        quality_log.append({
                            "run_id": "", "service_date": service_day.isoformat(), "bus_id": bus_id,
                            "route_id": trip.route_id, "trip_id": trip.trip_id,
                            "expected_timestamp_utc": _stamp(timestamp),
                            "quality_event": "ping_dropout", "interval_seconds": interval,
                        })
                        continue
                    fraction = min(0.999999, max(0.0, (sample_seconds - depart) / duration))
                    lat, lon = _at_fraction(line, cumulative, leg_distance, fraction)
                    lat, lon, noise_m = _noise(lat, lon, noise_std, trip_rng)
                    prediction_id = hashlib.sha1(f"{run_id}|{service_day}|{trip.trip_id}|{leg_index}|{step}".encode()).hexdigest()[:20]
                    pings.append({
                        "prediction_id": prediction_id, "run_id": "", "timestamp_utc": _stamp(timestamp),
                        "service_date": service_day.isoformat(), "bus_id": bus_id, "route_id": trip.route_id,
                        "trip_id": trip.trip_id, "direction_id": trip.direction_id, "lat": round(lat, 7),
                        "lon": round(lon, 7), "speed_kmh": round(leg_distance / duration * 3.6, 3),
                        "current_stop_index": leg_index, "current_stop_id": start_stop.stop_id,
                        "target_stop_id": end_stop.stop_id,
                        "distance_to_next_stop_m": round(max(0, leg_distance * (1 - fraction)), 2),
                        "hour_local": timestamp.astimezone(ZoneInfo(local_tz)).hour,
                        "noise_m": round(noise_m, 3),
                    })
                    target_time = _utc(service_day, arrive, local_tz)
                    eta_labels.append({"prediction_id": prediction_id, "actual_eta_min": round((target_time - timestamp).total_seconds() / 60, 4)})

    for collection in (stop_truth, stop_observations, delay_labels, pings, quality_log):
        for row in collection:
            row["run_id"] = run_id
    true_bunching = _bunching_events(stop_truth, float(event_rules["bunching_headway_ratio"]), run_id, "true")
    observed_bunching = _bunching_events(stop_observations, float(event_rules["bunching_headway_ratio"]), run_id, "detected")
    detected_delays = _delay_alerts(stop_observations, float(event_rules["delay_minutes"]), run_id)
    event_sensitivity = []
    for threshold in sorted(set([float(event_rules["delay_minutes"]), *map(float, event_rules.get("delay_sensitivity_minutes", []))])):
        for row in _delay_event_labels(stop_truth, threshold, run_id):
            event_sensitivity.append({**row, "dataset": "truth", "threshold_type": "delay_minutes", "threshold_value": threshold})
        for row in _delay_alerts(stop_observations, threshold, run_id):
            event_sensitivity.append({**row, "dataset": "detector", "threshold_type": "delay_minutes", "threshold_value": threshold})
    for ratio in sorted(set([float(event_rules["bunching_headway_ratio"]), *map(float, event_rules.get("bunching_sensitivity_ratios", []))])):
        for row in _bunching_events(stop_truth, ratio, run_id, "true"):
            event_sensitivity.append({**row, "dataset": "truth", "threshold_type": "bunching_ratio", "threshold_value": ratio})
        for row in _bunching_events(stop_observations, ratio, run_id, "detected"):
            event_sensitivity.append({**row, "dataset": "detector", "threshold_type": "bunching_ratio", "threshold_value": ratio})

    root = Path(output_root) / run_id / scenario_name
    root.mkdir(parents=True, exist_ok=True)
    fields = {
        "pings.csv": ["prediction_id", "run_id", "timestamp_utc", "service_date", "bus_id", "route_id", "trip_id", "direction_id", "lat", "lon", "speed_kmh", "current_stop_index", "current_stop_id", "target_stop_id", "distance_to_next_stop_m", "hour_local", "noise_m"],
        "eta_labels.csv": ["prediction_id", "actual_eta_min"],
        "stop_truth.csv": list(stop_truth[0]) if stop_truth else ["run_id"],
        "stop_observations.csv": list(stop_observations[0]) if stop_observations else ["run_id"],
        "event_labels.csv": list((delay_labels + true_bunching)[0]) if delay_labels or true_bunching else ["event_id", "run_id", "event_type"],
        "detector_alerts.csv": list((detected_delays + observed_bunching)[0]) if detected_delays or observed_bunching else ["alert_id", "run_id", "alert_type"],
        "event_sensitivity.csv": ["dataset", "threshold_type", "threshold_value", "event_id", "alert_id", "run_id", "event_type", "alert_type", "service_date", "route_id", "trip_id", "bus_id", "related_bus_id", "stop_id", "start_utc", "end_utc", "timestamp_utc", "severity", "rule_version", "message"],
        "quality_log.csv": list(quality_log[0]) if quality_log else ["run_id", "service_date", "quality_event"],
    }
    outputs = {
        "pings.csv": pings, "eta_labels.csv": eta_labels, "stop_truth.csv": stop_truth,
        "stop_observations.csv": stop_observations, "event_labels.csv": delay_labels + true_bunching,
        "detector_alerts.csv": detected_delays + observed_bunching, "event_sensitivity.csv": event_sensitivity,
        "quality_log.csv": quality_log,
    }
    for filename, rows in outputs.items():
        _write_csv(root / filename, fields[filename], rows)

    manifest = {
        "run_id": run_id, "scenario": scenario_name, "simulator_version": project.get("simulator_version", "0.1.0"),
        "gtfs_revision": project["gtfs_revision"], "gtfs_sha256": _sha256(Path(project["gtfs_path"])),
        "seed": int(settings["seed"]), "start_date": settings["start_date"], "days": int(settings["days"]),
        "timezone": local_tz, "route_ids": project["route_ids"], "ping_interval_seconds": interval,
        "event_rules": event_rules,
        "rows": {name: len(rows) for name, rows in outputs.items()},
        "files_sha256": {name: _sha256(root / name) for name in outputs},
        "service_calendar_fallback": not feed.service_calendar and not feed.service_exceptions,
    }
    (root / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return root


def _bunching_events(rows: list[dict], ratio_threshold: float, run_id: str, event_kind: str) -> list[dict]:
    groups = defaultdict(list)
    for row in rows:
        groups[(row["service_date"], row["route_id"], row["direction_id"], row["stop_id"])].append(row)
    result = []
    for key, group in groups.items():
        actual_key = "actual_arrival_utc" if event_kind == "true" else "observed_arrival_utc"
        group.sort(key=lambda item: item[actual_key])
        for previous, current in zip(group, group[1:]):
            actual_gap = (datetime.fromisoformat(current[actual_key].replace("Z", "+00:00")) - datetime.fromisoformat(previous[actual_key].replace("Z", "+00:00"))).total_seconds()
            scheduled_gap = (datetime.fromisoformat(current["scheduled_arrival_utc"].replace("Z", "+00:00")) - datetime.fromisoformat(previous["scheduled_arrival_utc"].replace("Z", "+00:00"))).total_seconds()
            if scheduled_gap <= 0 or actual_gap < 0 or actual_gap > scheduled_gap * ratio_threshold:
                continue
            start = current[actual_key]
            event = {
                "run_id": run_id, "route_id": key[1], "trip_id": current.get("trip_id", ""),
                "bus_id": current["bus_id"], "related_bus_id": previous["bus_id"], "stop_id": key[3],
                "start_utc": start, "end_utc": start, "severity": round(actual_gap / scheduled_gap, 4),
                "rule_version": f"bunching-{event_kind}-v1",
            }
            if event_kind == "true":
                event.update(event_id=hashlib.sha1(f"{run_id}|{key}|{current['trip_id']}|bunch".encode()).hexdigest()[:20], event_type="bunching", service_date=key[0])
            else:
                event.update(alert_id=hashlib.sha1(f"{run_id}|{key}|{current['bus_id']}|alert".encode()).hexdigest()[:20], alert_type="bunching", service_date=key[0], timestamp_utc=start, message=f"Observed headway is {actual_gap / scheduled_gap:.0%} of scheduled headway")
            result.append(event)
    return result


def _delay_alerts(rows: list[dict], threshold: float, run_id: str) -> list[dict]:
    alerts = []
    by_trip = defaultdict(list)
    for row in rows:
        by_trip[(row["service_date"], row["route_id"], row["trip_id"])].append(row)
    for _, trip_rows in by_trip.items():
        trip_rows.sort(key=lambda row: row["observed_arrival_utc"])
        row = next((item for item in trip_rows if (
            datetime.fromisoformat(item["observed_arrival_utc"].replace("Z", "+00:00"))
            - datetime.fromisoformat(item["scheduled_arrival_utc"].replace("Z", "+00:00"))
        ).total_seconds() / 60 >= threshold), None)
        if row is None:
            continue
        scheduled = datetime.fromisoformat(row["scheduled_arrival_utc"].replace("Z", "+00:00"))
        observed = datetime.fromisoformat(row["observed_arrival_utc"].replace("Z", "+00:00"))
        delay = (observed - scheduled).total_seconds() / 60
        alerts.append({
            "alert_id": hashlib.sha1(f"{run_id}|{row['service_date']}|{row['trip_id']}|{row['stop_id']}|delay".encode()).hexdigest()[:20],
            "run_id": run_id, "alert_type": "delay", "service_date": row["service_date"],
            "route_id": row["route_id"], "trip_id": row["trip_id"], "bus_id": row["bus_id"],
            "related_bus_id": "", "stop_id": row["stop_id"], "timestamp_utc": row["observed_arrival_utc"],
            "severity": round(delay, 3), "message": f"Observed arrival is {delay:.1f} minutes later than schedule",
            "threshold_value": threshold,
        })
    return alerts


def _delay_event_labels(rows: list[dict], threshold: float, run_id: str) -> list[dict]:
    by_trip = defaultdict(list)
    for row in rows:
        by_trip[(row["service_date"], row["route_id"], row["trip_id"])].append(row)
    events = []
    for (service_date, route_id, trip_id), trip_rows in by_trip.items():
        trip_rows.sort(key=lambda row: row["actual_arrival_utc"])
        matching = [row for row in trip_rows if float(row["delay_minutes"]) >= threshold]
        if not matching:
            continue
        first = matching[0]
        events.append({
            "event_id": hashlib.sha1(f"{run_id}|{service_date}|{trip_id}|delay|{threshold}".encode()).hexdigest()[:20],
            "run_id": run_id, "event_type": "delay", "service_date": service_date,
            "route_id": route_id, "trip_id": trip_id, "bus_id": first["bus_id"],
            "related_bus_id": "", "stop_id": first["stop_id"], "start_utc": first["actual_arrival_utc"],
            "end_utc": trip_rows[-1]["actual_arrival_utc"],
            "severity": round(max(float(row["delay_minutes"]) for row in trip_rows), 3),
            "rule_version": f"delay-v1-{threshold:g}",
        })
    return events
