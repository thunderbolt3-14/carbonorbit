"""Scenario-only emissions arithmetic with mandatory factor provenance."""

from __future__ import annotations

import math


class ScenarioInputError(ValueError):
    """Raised when an emissions scenario lacks valid, traceable inputs."""


def calculate_scenario(payload: dict) -> dict:
    required = [
        "diverted_passengers",
        "trip_distance_km",
        "private_mode_factor_g_per_pkm",
        "bus_factor_g_per_pkm",
        "private_mode_boundary",
        "bus_boundary",
        "factor_sources",
    ]
    missing = [key for key in required if payload.get(key) is None]
    if missing:
        raise ScenarioInputError("Missing required fields: " + ", ".join(missing))
    passengers = float(payload["diverted_passengers"])
    distance = float(payload["trip_distance_km"])
    private_factor = float(payload["private_mode_factor_g_per_pkm"])
    bus_factor = float(payload["bus_factor_g_per_pkm"])
    if not all(math.isfinite(value) for value in (passengers, distance, private_factor, bus_factor)):
        raise ScenarioInputError("Passengers, distance, and emission factors must be finite numbers")
    if passengers <= 0 or distance <= 0 or private_factor <= 0 or bus_factor < 0:
        raise ScenarioInputError("Passengers and distance must be positive; factors must be non-negative")
    sources = payload["factor_sources"]
    if not isinstance(sources, dict) or not str(sources.get("private_mode", "")).strip() or not str(sources.get("bus", "")).strip():
        raise ScenarioInputError("factor_sources must identify both private_mode and bus sources")
    private_boundary = str(payload["private_mode_boundary"]).strip()
    bus_boundary = str(payload["bus_boundary"]).strip()
    if not private_boundary or not bus_boundary:
        raise ScenarioInputError("Both factor boundaries must be non-empty labels")
    if private_boundary.casefold() != bus_boundary.casefold():
        raise ScenarioInputError("Private-mode and bus emission factors must use the same boundary")
    boundary = private_boundary

    passenger_km = passengers * distance
    private_avoided_kg = passenger_km * private_factor / 1000
    bus_service_case = payload.get("bus_service_case", "average_factor_allocation")
    if bus_service_case == "fixed_service":
        bus_added_kg = 0.0
        explanation = "Assumes existing bus service absorbs the trips; incremental bus-service emissions are excluded."
    elif bus_service_case == "average_factor_allocation":
        bus_added_kg = passenger_km * bus_factor / 1000
        explanation = "Applies the stated average bus passenger-kilometre factor to diverted passenger-kilometres; this is allocation, not marginal-service accounting."
    else:
        raise ScenarioInputError("bus_service_case must be fixed_service or average_factor_allocation")
    return {
        "scenario_id": str(payload.get("scenario_id", "unspecified")),
        "pollutant": str(payload.get("pollutant", "CO2e")),
        "unit": f"kg {payload.get('pollutant', 'CO2e')} per scenario",
        "factor_boundary": boundary,
        "diverted_passengers": passengers,
        "trip_distance_km": distance,
        "passenger_km": passenger_km,
        "bus_service_case": bus_service_case,
        "private_avoided_kg": private_avoided_kg,
        "bus_added_kg": bus_added_kg,
        "net_avoided_kg": private_avoided_kg - bus_added_kg,
        "factor_sources": sources,
        "interpretation": explanation + " No passenger diversion or real-world emissions reduction is observed by this project.",
    }
