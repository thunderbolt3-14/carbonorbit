"""Flask API for the local carbonOrbit simulation dashboard."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import Flask, g, jsonify, request, send_from_directory

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
