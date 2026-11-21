from __future__ import annotations

import pandas as pd
import pytest

from carbonorbit.analytics import CATEGORICAL, NUMERIC, _feature_frame, chronological_days


def test_chronological_split_has_disjoint_consecutive_service_days():
    dates = pd.date_range("2026-11-01", periods=28, freq="D").strftime("%Y-%m-%d")
    frame = pd.DataFrame({"service_date": [day for day in dates for _ in range(2)], "row": range(56)})
    train, validation, test = chronological_days(frame)
    train_days, validation_days, test_days = map(
        lambda part: set(part.service_date), (train, validation, test)
    )
    assert (len(train_days), len(validation_days), len(test_days)) == (18, 5, 5)
    assert train_days.isdisjoint(validation_days)
    assert train_days.isdisjoint(test_days)
    assert validation_days.isdisjoint(test_days)
    assert max(train_days) < min(validation_days) < max(validation_days) < min(test_days)


def test_chronological_split_rejects_too_few_days():
    frame = pd.DataFrame({"service_date": ["2026-11-01", "2026-11-02"]})
    with pytest.raises(ValueError, match="Need 28 distinct service days"):
        chronological_days(frame)


def test_eta_feature_allowlist_excludes_targets_future_values_and_labels():
    row = {
        "route_id": "route-1",
        "direction_id": "0",
        "current_stop_index": 2,
        "distance_to_next_stop_m": 500.0,
        "speed_kmh": 20.0,
        "hour_local": 8,
        "actual_eta_min": 3.0,
        "future_arrival_utc": "2026-11-01T08:03:00Z",
        "is_delayed": True,
        "is_bunched": False,
        "noise_m": 2.0,
    }
    features = _feature_frame(pd.DataFrame([row]))
    assert list(features.columns) == CATEGORICAL + NUMERIC
    assert not {"actual_eta_min", "future_arrival_utc", "is_delayed", "is_bunched"} & set(features.columns)
    assert features.iloc[0].route_id == "route-1"
