"""Configuration loading and validation."""

from __future__ import annotations

from pathlib import Path

import yaml


def load_config(path: str | Path = "config/simulation.yaml") -> dict:
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as stream:
        config = yaml.safe_load(stream) or {}
    project = config.get("project", {})
    simulation = config.get("simulation", {})
    required = ("gtfs_path", "gtfs_revision", "gtfs_sha256", "route_ids")
    missing = [key for key in required if not project.get(key)]
    if missing:
        raise ValueError(f"Missing project settings in {config_path}: {', '.join(missing)}")
    if not project["route_ids"]:
        raise ValueError("At least one GTFS route ID must be configured")
    if int(simulation.get("days", 0)) < 1:
        raise ValueError("simulation.days must be positive")
    if int(simulation.get("ping_interval_seconds", 0)) < 1:
        raise ValueError("simulation.ping_interval_seconds must be positive")
    return config
