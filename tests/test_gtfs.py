from __future__ import annotations

from zipfile import ZipFile

import pytest

from carbonorbit.gtfs import load_gtfs, parse_gtfs_time


def write_feed(tmp_path, *, include=None, overrides=None):
    tables = {
        "routes.txt": "route_id,route_short_name,route_long_name,route_type\nr1,1,One,3\n",
        "trips.txt": "route_id,service_id,trip_id,direction_id,shape_id\nr1,s1,t1,0,sh1\n",
        "stop_times.txt": (
            "trip_id,arrival_time,departure_time,stop_id,stop_sequence\n"
            "t1,08:00:00,08:00:00,s1,1\n"
            "t1,08:10:00,08:10:00,s2,2\n"
        ),
        "stops.txt": (
            "stop_id,stop_name,stop_lat,stop_lon\n"
            "s1,Start,13.0,77.0\n"
            "s2,End,13.1,77.1\n"
        ),
        "shapes.txt": (
            "shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence\n"
            "sh1,13.0,77.0,1\nsh1,13.1,77.1,2\n"
        ),
        "calendar.txt": (
            "service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\n"
            "s1,1,1,1,1,1,1,1,20260101,20271231\n"
        ),
    }
    if overrides:
        tables.update(overrides)
    names = include if include is not None else tables.keys()
    path = tmp_path / "feed.zip"
    with ZipFile(path, "w") as archive:
        for name in names:
            archive.writestr(name, tables[name])
    return path


def test_parse_gtfs_time_supports_after_midnight_service_times():
    assert parse_gtfs_time("26:15:30") == 26 * 3600 + 15 * 60 + 30


@pytest.mark.parametrize("bad_time", ["", "8:00", "08:60:00", "-1:00:00", "08:00:xx"])
def test_parse_gtfs_time_rejects_malformed_values(bad_time):
    with pytest.raises(ValueError, match="Invalid GTFS time"):
        parse_gtfs_time(bad_time)


def test_load_gtfs_reads_selected_route_and_shape(tmp_path):
    feed = load_gtfs(write_feed(tmp_path), ["r1"], revision="fixture")
    assert feed.revision == "fixture"
    assert feed.routes["r1"]["short_name"] == "1"
    assert len(feed.trips) == 1
    assert [stop.stop_id for stop in feed.trips[0].stop_times] == ["s1", "s2"]
    assert feed.shapes["sh1"] == [(13.0, 77.0), (13.1, 77.1)]


def test_load_gtfs_reports_missing_archive(tmp_path):
    with pytest.raises(FileNotFoundError, match="GTFS archive not found"):
        load_gtfs(tmp_path / "missing.zip", ["r1"])


def test_load_gtfs_rejects_archive_missing_required_table(tmp_path):
    archive = write_feed(tmp_path, include=["routes.txt"])
    with pytest.raises(ValueError, match="missing required files"):
        load_gtfs(archive, ["r1"])


def test_load_gtfs_rejects_unknown_selected_route(tmp_path):
    with pytest.raises(ValueError, match="Selected route IDs are not present"):
        load_gtfs(write_feed(tmp_path), ["not-a-route"])


def test_load_gtfs_rejects_unknown_stop_reference(tmp_path):
    archive = write_feed(
        tmp_path,
        overrides={
            "stop_times.txt": (
                "trip_id,arrival_time,departure_time,stop_id,stop_sequence\n"
                "t1,08:00:00,08:00:00,s1,1\n"
                "t1,08:10:00,08:10:00,missing,2\n"
            )
        },
    )
    with pytest.raises(ValueError, match="unknown stop IDs"):
        load_gtfs(archive, ["r1"])


@pytest.mark.parametrize(
    ("sequence_rows", "message"),
    [
        ("t1,08:00:00,08:00:00,s1,x\nt1,08:10:00,08:10:00,s2,2\n", "malformed stop_sequence"),
        ("t1,08:00:00,08:00:00,s1,1\nt1,08:10:00,08:10:00,s2,1\n", "duplicate stop_sequence"),
        ("t1,08:00:00,08:00:00,s1,0\nt1,08:10:00,08:10:00,s2,2\n", "non-positive stop_sequence"),
    ],
)
def test_load_gtfs_rejects_malformed_stop_sequences(tmp_path, sequence_rows, message):
    archive = write_feed(
        tmp_path,
        overrides={
            "stop_times.txt": "trip_id,arrival_time,departure_time,stop_id,stop_sequence\n" + sequence_rows
        },
    )
    with pytest.raises(ValueError, match=message):
        load_gtfs(archive, ["r1"])


def test_load_gtfs_rejects_invalid_coordinates(tmp_path):
    archive = write_feed(
        tmp_path,
        overrides={
            "stops.txt": "stop_id,stop_name,stop_lat,stop_lon\ns1,Start,91,77\ns2,End,13,77\n"
        },
    )
    with pytest.raises(ValueError, match="coordinates"):
        load_gtfs(archive, ["r1"])


def test_load_gtfs_rejects_non_monotonic_trip_times(tmp_path):
    archive = write_feed(
        tmp_path,
        overrides={
            "stop_times.txt": (
                "trip_id,arrival_time,departure_time,stop_id,stop_sequence\n"
                "t1,08:10:00,08:10:00,s1,1\n"
                "t1,08:00:00,08:00:00,s2,2\n"
            )
        },
    )
    with pytest.raises(ValueError, match="non-monotonic stop times"):
        load_gtfs(archive, ["r1"])
