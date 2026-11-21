"""Flask API for the local carbonOrbit simulation dashboard."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, g, jsonify, request, send_from_directory
import requests

from .db import connect, latest_run_id
from .emissions import ScenarioInputError, calculate_scenario


def _as_dicts(rows) -> list[dict]:
    return [dict(row) for row in rows]


def create_app(database: str | Path = "data/carbonorbit.db", dashboard_dir: str | Path = "dashboard") -> Flask:
    app = Flask(__name__)
    app.config["DATABASE"] = str(database)
    dashboard_path = Path(dashboard_dir)
    if not dashboard_path.is_absolute():
        dashboard_path = Path(__file__).resolve().parents[2] / dashboard_path
    app.config["DASHBOARD_DIR"] = str(dashboard_path.resolve())
    app.config["LIVE_FEED_BASE_URL"] = "https://maps.reclaim.city/bengaluru/rt"

    def db() -> sqlite3.Connection:
        if "database" not in g:
            g.database = connect(app.config["DATABASE"])
        return g.database

    @app.teardown_appcontext
    def close_db(_error=None):
        connection = g.pop("database", None)
        if connection is not None:
            connection.close()

    @app.get("/")
    def dashboard():
        return send_from_directory(app.config["DASHBOARD_DIR"], "index.html")

    @app.get("/ping")
    @app.get("/api/v1/ping")
    def ping():
        return jsonify({"ok": True, "service": "carbonOrbit", "version": "v1"})

    @app.get("/api/v1/live")
    def live_feed():
        """Proxy the independent Bengaluru GTFS-Realtime feed and report freshness."""
        base = app.config["LIVE_FEED_BASE_URL"].rstrip("/")
        try:
            status_response = requests.get(f"{base}/status.json", timeout=(3, 8))
            status_response.raise_for_status()
            feed_status = status_response.json()
            positions_response = requests.get(f"{base}/vehicle_positions.json", timeout=(3, 8))
            positions_response.raise_for_status()
            feed = positions_response.json()
            updates_response = requests.get(f"{base}/trip_updates.json", timeout=(3, 8))
            updates_response.raise_for_status()
            updates_feed = updates_response.json()
        except (requests.RequestException, ValueError) as exc:
            return jsonify({
                "source": "Independent GTFS-Realtime mirror (not an official BMTC feed)",
                "official": False,
                "error": "live_feed_unavailable",
                "message": str(exc),
                "buses": [],
            }), 502

        header = feed.get("header") or {}
        feed_timestamp = header.get("timestamp") or feed_status.get("feed_time")
        try:
            feed_epoch = int(feed_timestamp) if feed_timestamp is not None else None
            age_seconds = max(0, int(datetime.now(timezone.utc).timestamp()) - feed_epoch) if feed_epoch is not None else None
            feed_time_utc = datetime.fromtimestamp(feed_epoch, timezone.utc).isoformat().replace("+00:00", "Z") if feed_epoch is not None else None
        except (TypeError, ValueError, OSError):
            age_seconds, feed_time_utc = None, None

        buses = []
        for entity in feed.get("entity", []):
            vehicle = entity.get("vehicle") or {}
            position = vehicle.get("position") or {}
            trip = vehicle.get("trip") or {}
            if position.get("latitude") is None or position.get("longitude") is None:
                continue
            buses.append({
                "bus_id": (vehicle.get("vehicle") or {}).get("id") or entity.get("id"),
                "route_id": trip.get("routeId"),
                "trip_id": trip.get("tripId"),
                "lat": position["latitude"],
                "lon": position["longitude"],
                "bearing": position.get("bearing"),
                "speed_mps": position.get("speed"),
                "timestamp_utc": feed_time_utc,
                "next_stop_id": vehicle.get("stopId"),
                "current_status": vehicle.get("currentStatus"),
            })
        buses.sort(key=lambda bus: (bus.get("route_id") or "", bus.get("bus_id") or ""))
        predictions = []
        now_epoch = int(datetime.now(timezone.utc).timestamp())
        for entity in updates_feed.get("entity", []):
            update = entity.get("tripUpdate") or {}
            trip = update.get("trip") or {}
            vehicle = update.get("vehicle") or {}
            bus_id = (vehicle.get("id") if isinstance(vehicle, dict) else None) or trip.get("tripId") or entity.get("id")
            for stop_update in update.get("stopTimeUpdate", []):
                stop_id = stop_update.get("stopId")
                arrival = stop_update.get("arrival") or {}
                departure = stop_update.get("departure") or {}
                predicted_epoch = arrival.get("time") or departure.get("time")
                if predicted_epoch is None:
                    continue
                try:
                    eta_min = (int(predicted_epoch) - now_epoch) / 60
                except (TypeError, ValueError):
                    continue
                if eta_min < -2:
                    continue
                predictions.append({
                    "bus_id": bus_id,
                    "route_id": trip.get("routeId"),
                    "trip_id": trip.get("tripId"),
                    "target_stop_id": stop_id,
                    "predicted_eta_min": max(0, round(eta_min, 1)),
                    "arrival_time_utc": datetime.fromtimestamp(int(predicted_epoch), timezone.utc).isoformat().replace("+00:00", "Z"),
                })
        predictions.sort(key=lambda row: (row["predicted_eta_min"], row.get("route_id") or ""))
        return jsonify({
            "source": "Independent GTFS-Realtime mirror (not an official BMTC feed)",
            "official": False,
            "network": feed_status.get("network", "bengaluru"),
            "feed_time_utc": feed_time_utc,
            "feed_age_seconds": age_seconds,
            "stale": age_seconds is None or age_seconds > 120,
            "reported_vehicle_count": feed_status.get("vehicles"),
            "reported_trip_update_count": feed_status.get("trip_updates"),
            "buses": buses,
            "predictions": predictions,
        })

    @app.get("/api/v1/buses")
    def buses():
        run_id = latest_run_id(db())
        route_id = request.args.get("route_id")
        if not run_id:
            return jsonify({"run_id": None, "buses": []})
        sql = """
          SELECT p.prediction_id, p.bus_id, p.route_id, p.trip_id, p.timestamp_utc,
                 p.lat, p.lon, p.speed_kmh, p.target_stop_id AS next_stop_id,
                 p.distance_to_next_stop_m
          FROM pings p
          WHERE p.run_id = ?
            AND NOT EXISTS (
              SELECT 1 FROM pings newer
              WHERE newer.run_id=p.run_id AND newer.bus_id=p.bus_id
                AND newer.timestamp_utc > p.timestamp_utc
            )
        """
        params: list = [run_id]
        if route_id:
            sql += " AND p.route_id = ?"
            params.append(route_id)
        sql += " ORDER BY p.route_id, p.bus_id"
        return jsonify({"run_id": run_id, "buses": _as_dicts(db().execute(sql, params).fetchall())})

    @app.get("/api/v1/eta")
    def eta():
        run_id = latest_run_id(db())
        if not run_id:
            return jsonify({"run_id": None, "predictions": []})
        sql = """
          SELECT e.prediction_id, e.bus_id, e.route_id, e.target_stop_id,
                 e.predicted_eta_min, NULL AS interval_low_min, NULL AS interval_high_min,
                 e.model_name AS model, p.timestamp_utc
          FROM predictions e
          LEFT JOIN pings p ON p.prediction_id=e.prediction_id
          WHERE e.run_id=?
        """
        params: list = [run_id]
        bus_id = request.args.get("bus_id")
        if bus_id:
            sql += " AND e.bus_id=?"
            params.append(bus_id)
        sql += " ORDER BY p.timestamp_utc DESC LIMIT 500"
        return jsonify({"run_id": run_id, "predictions": _as_dicts(db().execute(sql, params).fetchall())})

    @app.get("/api/v1/alerts")
    def alerts():
        try:
            limit = max(1, min(500, int(request.args.get("limit", "100"))))
        except ValueError:
            return jsonify({"error": {"code": "invalid_request", "message": "limit must be an integer"}}), 400
        run_id = latest_run_id(db())
        if not run_id:
            return jsonify({"run_id": None, "alerts": []})
        route_id = request.args.get("route_id")
        sql = "SELECT alert_id, alert_type AS type, route_id, bus_id, related_bus_id, target_stop_id, timestamp_utc, severity, message FROM alerts WHERE run_id=?"
        params: list = [run_id]
        if route_id:
            sql += " AND route_id=?"
            params.append(route_id)
        sql += " ORDER BY timestamp_utc DESC LIMIT ?"
        params.append(limit)
        return jsonify({"run_id": run_id, "alerts": _as_dicts(db().execute(sql, params).fetchall())})

    @app.get("/api/v1/metrics")
    def metrics():
        run_id = latest_run_id(db())
        if not run_id:
            return jsonify({"run_id": None, "metrics": {}})
        rows = db().execute(
            "SELECT metric_name, metric_value, unit, partition_name, group_key FROM evaluation_metrics WHERE run_id=? ORDER BY metric_name",
            (run_id,),
        ).fetchall()
        return jsonify({"run_id": run_id, "metrics": {row["metric_name"]: {"value": row["metric_value"], "unit": row["unit"], "partition": row["partition_name"], "group": row["group_key"]} for row in rows}})

    @app.post("/api/v1/emissions/scenario")
    def emissions():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": {"code": "invalid_request", "message": "Request body must be a JSON object"}}), 400
        try:
            result = calculate_scenario(payload)
        except (ScenarioInputError, TypeError, ValueError) as exc:
            return jsonify({"error": {"code": "invalid_request", "message": str(exc)}}), 400
        return jsonify(result)

    return app
