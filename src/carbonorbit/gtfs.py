"""Small, dependency-light reader for the subset of GTFS used by carbonOrbit."""

from __future__ import annotations

import csv
import io
import math
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from zipfile import ZipFile


def parse_gtfs_time(value: str) -> int:
    """Convert GTFS HH:MM:SS (including service times past midnight) to seconds."""
    try:
        hours, minutes, seconds = (int(part) for part in value.strip().split(":"))
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError(f"Invalid GTFS time {value!r}; expected HH:MM:SS") from exc
    if hours < 0 or not 0 <= minutes < 60 or not 0 <= seconds < 60:
        raise ValueError(f"Invalid GTFS time {value!r}; values are out of range")
    return hours * 3600 + minutes * 60 + seconds


@dataclass(frozen=True)
class Stop:
    stop_id: str
    name: str
    lat: float
    lon: float


@dataclass(frozen=True)
class StopTime:
    stop_id: str
    stop_sequence: int
    arrival_seconds: int
    departure_seconds: int


@dataclass(frozen=True)
class Trip:
    route_id: str
    trip_id: str
    service_id: str
    direction_id: str
    shape_id: str
    stop_times: tuple[StopTime, ...]


@dataclass
class GTFSFeed:
    routes: dict[str, dict[str, str]]
    stops: dict[str, Stop]
    trips: list[Trip]
    shapes: dict[str, list[tuple[float, float]]]
    service_calendar: dict[str, dict[str, str]]
    service_exceptions: dict[tuple[str, str], int]
    revision: str = "unknown"

    def active_service_ids(self, service_day: date) -> set[str]:
        day_key = service_day.strftime("%Y%m%d")
        weekday = service_day.strftime("%A").lower()
        active: set[str] = set()
        for service_id, row in self.service_calendar.items():
            if row.get("start_date", "00000000") <= day_key <= row.get("end_date", "99999999") and row.get(weekday) == "1":
                active.add(service_id)
        for (service_id, exception_day), exception_type in self.service_exceptions.items():
            if exception_day == day_key:
                if exception_type == 1:
                    active.add(service_id)
                elif exception_type == 2:
                    active.discard(service_id)
        # Some feeds omit calendar tables. In that case schedules are treated as
        # daily templates; the manifest records this fallback.
        if not self.service_calendar and not self.service_exceptions:
            return {trip.service_id for trip in self.trips}
        return active


def _rows(archive: ZipFile, filename: str):
    try:
        member = archive.open(filename)
    except KeyError:
        return
    with member:
        text = io.TextIOWrapper(member, encoding="utf-8-sig", newline="")
        yield from csv.DictReader(text)


def load_gtfs(path: str | Path, route_ids: list[str], revision: str = "unknown") -> GTFSFeed:
    """Load only selected routes and their referenced stops/trips/shapes."""
    archive_path = Path(path)
    if not archive_path.is_file():
        raise FileNotFoundError(f"GTFS archive not found: {archive_path}. Download the pinned archive described in docs/data_sources.md.")
    with ZipFile(archive_path) as archive:
        names = set(archive.namelist())
        required = {"routes.txt", "trips.txt", "stop_times.txt", "stops.txt"}
        missing = sorted(required - names)
        if missing:
            raise ValueError(f"GTFS archive is missing required files: {', '.join(missing)}")
        wanted = set(route_ids)
        routes = {}
        for row in _rows(archive, "routes.txt"):
            route_id = row.get("route_id", "")
            if route_id in wanted:
                routes[route_id] = {
                    "route_id": route_id,
                    "short_name": row.get("route_short_name", ""),
                    "long_name": row.get("route_long_name", ""),
                    "route_type": row.get("route_type", ""),
                }
        absent = sorted(wanted - routes.keys())
        if absent:
            raise ValueError(f"Selected route IDs are not present in the archive: {', '.join(absent)}")

        selected_trip_rows = [r for r in _rows(archive, "trips.txt") if r.get("route_id") in wanted]
        selected_trip_ids = {r["trip_id"] for r in selected_trip_rows}
        stop_rows_by_trip: dict[str, list[dict[str, str]]] = {trip_id: [] for trip_id in selected_trip_ids}
        for row in _rows(archive, "stop_times.txt"):
            if row.get("trip_id") in selected_trip_ids:
                stop_rows_by_trip[row["trip_id"]].append(row)

        stop_ids = {row.get("stop_id", "") for rows in stop_rows_by_trip.values() for row in rows}
        stops = {}
        for row in _rows(archive, "stops.txt"):
            stop_id = row.get("stop_id", "")
            if stop_id not in stop_ids:
                continue
            try:
                lat, lon = float(row["stop_lat"]), float(row["stop_lon"])
            except (KeyError, ValueError) as exc:
                raise ValueError(f"Stop {stop_id!r} has invalid coordinates") from exc
            if not (math.isfinite(lat) and math.isfinite(lon) and -90 <= lat <= 90 and -180 <= lon <= 180):
                raise ValueError(f"Stop {stop_id!r} has out-of-range or non-finite coordinates")
            stops[stop_id] = Stop(stop_id, row.get("stop_name", ""), lat, lon)
        missing_stops = sorted(stop_ids - stops.keys())
        if missing_stops:
            raise ValueError(f"Stop times refer to unknown stop IDs: {', '.join(missing_stops[:8])}")

        trips = []
        selected_shape_ids = set()
        for row in selected_trip_rows:
            trip_id = row["trip_id"]
            try:
                sequenced_rows = [
                    (int(item["stop_sequence"]), item)
                    for item in stop_rows_by_trip[trip_id]
                ]
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"Trip {trip_id!r} has a malformed stop_sequence") from exc
            sequences = [sequence for sequence, _ in sequenced_rows]
            if any(sequence < 1 for sequence in sequences):
                raise ValueError(f"Trip {trip_id!r} has a non-positive stop_sequence")
            if len(sequences) != len(set(sequences)):
                raise ValueError(f"Trip {trip_id!r} has duplicate stop_sequence values")
            st_rows = [item for _, item in sorted(sequenced_rows, key=lambda pair: pair[0])]
            if len(st_rows) < 2:
                continue
            st = tuple(
                StopTime(
                    stop_id=item["stop_id"],
                    stop_sequence=int(item["stop_sequence"]),
                    arrival_seconds=parse_gtfs_time(item.get("arrival_time") or item.get("departure_time", "")),
                    departure_seconds=parse_gtfs_time(item.get("departure_time") or item.get("arrival_time", "")),
                )
                for item in st_rows
            )
            if any(item.departure_seconds < item.arrival_seconds for item in st):
                raise ValueError(f"Trip {trip_id!r} has a departure before its arrival")
            if any(later.arrival_seconds < earlier.departure_seconds for earlier, later in zip(st, st[1:])):
                raise ValueError(f"Trip {trip_id!r} has non-monotonic stop times")
            shape_id = row.get("shape_id", "")
            if shape_id:
                selected_shape_ids.add(shape_id)
            trips.append(Trip(row["route_id"], trip_id, row.get("service_id", ""), row.get("direction_id", "0"), shape_id, st))

        shape_points: dict[str, list[tuple[int, float, float]]] = {shape_id: [] for shape_id in selected_shape_ids}
        for row in _rows(archive, "shapes.txt"):
            shape_id = row.get("shape_id", "")
            if shape_id in selected_shape_ids:
                shape_points[shape_id].append((int(row["shape_pt_sequence"]), float(row["shape_pt_lat"]), float(row["shape_pt_lon"])))
        shapes = {
            shape_id: [(lat, lon) for _, lat, lon in sorted(points)]
            for shape_id, points in shape_points.items()
            if points
        }
        calendar = {row["service_id"]: row for row in _rows(archive, "calendar.txt") if "service_id" in row}
        exceptions = {}
        for row in _rows(archive, "calendar_dates.txt"):
            try:
                exceptions[(row["service_id"], row["date"])] = int(row["exception_type"])
            except (KeyError, ValueError):
                continue

    if not trips:
        raise ValueError("No usable trips found for the selected GTFS routes")
    return GTFSFeed(routes, stops, trips, shapes, calendar, exceptions, revision)


def iter_days(start: date, count: int):
    for offset in range(count):
        yield start + timedelta(days=offset)
