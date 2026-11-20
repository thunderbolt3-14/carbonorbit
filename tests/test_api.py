from __future__ import annotations

from carbonorbit.api import create_app
from carbonorbit.db import connect


def seed_database(path):
    with connect(path) as db:
        db.execute(
            "INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("run-1", "2026-11-20T00:00:00Z", "rev", "sha", "{}", 1, "0.1.0"),
        )
        db.execute(
            "INSERT INTO pings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("p1", "run-1", "2026-11-20T08:00:00Z", "2026-11-20", "bus-1", "route-1", "trip-1", 13.0, 77.0, 20.0, 2, "stop-2", 500.0, 8, 2.0),
        )
        db.execute(
            "INSERT INTO predictions VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("p1", "run-1", "bus-1", "route-1", "stop-2", 2.5, "RandomForest", "2026-11-20T08:00:00Z"),
        )
        db.execute(
            "INSERT INTO alerts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("a1", "run-1", "delay", "route-1", "bus-1", None, "stop-2", "2026-11-20T08:00:00Z", 3.0, "Synthetic delay alert"),
        )
        db.execute(
            "INSERT INTO evaluation_metrics VALUES (?, ?, ?, ?, ?, ?)",
            ("run-1", "eta_mae_min", 0.2, "minutes", "test", "overall"),
        )


def test_api_empty_database_and_health_shapes(tmp_path):
    app = create_app(tmp_path / "empty.db", "dashboard")
    app.testing = True
    client = app.test_client()
    assert client.get("/ping").json == {"ok": True, "service": "carbonOrbit", "version": "v1"}
    assert client.get("/api/v1/buses").json == {"run_id": None, "buses": []}
    assert client.get("/api/v1/eta").json == {"run_id": None, "predictions": []}
    assert client.get("/api/v1/alerts").json == {"run_id": None, "alerts": []}
    assert client.get("/api/v1/metrics").json == {"run_id": None, "metrics": {}}
    assert client.get("/").status_code == 200
    assert b"SIMULATED DATA" in client.get("/").data


def test_api_populated_response_fields_and_filters(tmp_path):
    database = tmp_path / "populated.db"
    seed_database(database)
    app = create_app(database, "dashboard")
    app.testing = True
    client = app.test_client()

    buses = client.get("/api/v1/buses?route_id=route-1").json
    assert buses["run_id"] == "run-1"
    assert len(buses["buses"]) == 1
    assert buses["buses"][0]["timestamp_utc"] == "2026-11-20T08:00:00Z"
    assert buses["buses"][0]["next_stop_id"] == "stop-2"

    eta = client.get("/api/v1/eta?bus_id=bus-1").json
    assert eta["run_id"] == "run-1"
    assert eta["predictions"][0]["model"] == "RandomForest"
    assert eta["predictions"][0]["interval_low_min"] is None

    alerts = client.get("/api/v1/alerts?route_id=route-1&limit=1").json
    assert alerts["run_id"] == "run-1"
    assert alerts["alerts"][0]["type"] == "delay"

    metrics = client.get("/api/v1/metrics").json
    assert metrics["metrics"]["eta_mae_min"]["value"] == 0.2


def test_api_rejects_invalid_alert_limit_and_unconfigured_emissions(tmp_path):
    app = create_app(tmp_path / "api.db", "dashboard")
    app.testing = True
    client = app.test_client()
    bad_limit = client.get("/api/v1/alerts?limit=not-an-int")
    assert bad_limit.status_code == 400
    assert bad_limit.json["error"]["code"] == "invalid_request"
    missing_factors = client.post("/api/v1/emissions/scenario", json={})
    assert missing_factors.status_code == 400
    assert missing_factors.json["error"]["code"] == "invalid_request"
