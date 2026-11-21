from __future__ import annotations

import math

import pytest

from carbonorbit.emissions import ScenarioInputError, calculate_scenario


def valid_scenario(**updates):
    payload = {
        "scenario_id": "test",
        "diverted_passengers": 100,
        "trip_distance_km": 8,
        "private_mode_factor_g_per_pkm": 150,
        "bus_factor_g_per_pkm": 60,
        "private_mode_boundary": "operational",
        "bus_boundary": "operational",
        "factor_sources": {"private_mode": "source A", "bus": "source B"},
    }
    payload.update(updates)
    return payload


def test_emissions_scenario_uses_declared_factors_and_shared_boundary():
    result = calculate_scenario(valid_scenario())
    assert result["passenger_km"] == 800
    assert result["private_avoided_kg"] == 120
    assert result["bus_added_kg"] == 48
    assert result["net_avoided_kg"] == 72
    assert result["factor_boundary"] == "operational"
    assert "No passenger diversion" in result["interpretation"]


def test_emissions_scenario_supports_fixed_existing_service_assumption():
    result = calculate_scenario(valid_scenario(bus_service_case="fixed_service"))
    assert result["bus_added_kg"] == 0
    assert result["net_avoided_kg"] == result["private_avoided_kg"]


@pytest.mark.parametrize(
    "payload",
    [
        {},
        valid_scenario(private_mode_boundary="tailpipe", bus_boundary="lifecycle"),
        valid_scenario(diverted_passengers=0),
        valid_scenario(trip_distance_km=0),
        valid_scenario(private_mode_factor_g_per_pkm=None),
        valid_scenario(bus_factor_g_per_pkm=-1),
        valid_scenario(private_mode_factor_g_per_pkm=math.inf),
        valid_scenario(factor_sources={"private_mode": "", "bus": ""}),
        valid_scenario(bus_service_case="unknown"),
    ],
)
def test_emissions_scenario_rejects_missing_or_invalid_inputs(payload):
    with pytest.raises(ScenarioInputError):
        calculate_scenario(payload)
