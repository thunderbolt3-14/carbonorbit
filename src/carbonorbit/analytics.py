"""Chronological ETA model comparison and event-level detector evaluation."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, precision_recall_fscore_support
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

CATEGORICAL = ["route_id", "direction_id"]
NUMERIC = ["current_stop_index", "distance_to_next_stop_m", "speed_kmh", "hour_local"]


def _load_frame(run_dir: Path) -> pd.DataFrame:
    features = pd.read_csv(run_dir / "pings.csv")
    targets = pd.read_csv(run_dir / "eta_labels.csv")
    frame = features.merge(targets, on="prediction_id", how="inner", validate="one_to_one")
    frame["service_date"] = pd.to_datetime(frame["service_date"]).dt.date.astype(str)
    frame["actual_eta_min"] = pd.to_numeric(frame["actual_eta_min"], errors="coerce")
    frame = frame.dropna(subset=["actual_eta_min"])
    if frame.empty:
        raise ValueError("No valid ETA examples after joining telemetry and labels")
    if (frame["actual_eta_min"] <= 0).any():
        raise ValueError("ETA labels must be strictly positive")
    return frame.sort_values(["service_date", "timestamp_utc", "prediction_id"]).reset_index(drop=True)


def chronological_days(frame: pd.DataFrame, train_days: int = 18, validation_days: int = 5, test_days: int = 5) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    days = sorted(frame["service_date"].unique())
    required = train_days + validation_days + test_days
    if len(days) < required:
        raise ValueError(f"Need {required} distinct service days for the declared 18/5/5 split; found {len(days)}")
    train_set, validation_set, test_set = set(days[:train_days]), set(days[train_days:train_days + validation_days]), set(days[train_days + validation_days:required])
    return (
        frame[frame.service_date.isin(train_set)].copy(),
        frame[frame.service_date.isin(validation_set)].copy(),
        frame[frame.service_date.isin(test_set)].copy(),
    )


def _metrics(actual, predicted) -> dict:
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    errors = np.abs(actual - predicted)
    return {
        "count": int(len(actual)),
        "mae_min": float(mean_absolute_error(actual, predicted)),
        "rmse_min": float(np.sqrt(mean_squared_error(actual, predicted))),
        "median_absolute_error_min": float(np.median(errors)),
        "p90_absolute_error_min": float(np.quantile(errors, 0.90)),
        "within_2min_pct": float(np.mean(errors <= 2.0) * 100),
    }


def _group_metrics(frame: pd.DataFrame, actual, predicted, column: str) -> dict:
    scored = pd.DataFrame({
        "group": frame[column].astype(str).to_numpy(),
        "actual": np.asarray(actual, dtype=float),
        "predicted": np.asarray(predicted, dtype=float),
    })
    return {
        group: _metrics(part.actual, part.predicted)
        for group, part in scored.groupby("group", sort=True)
    }


def _historical_predict(train: pd.DataFrame, target: pd.DataFrame) -> np.ndarray:
    keys = ["route_id", "target_stop_id", "hour_local"]
    means = train.groupby(keys)["actual_eta_min"].mean().to_dict()
    fallback = float(train["actual_eta_min"].mean())
    return np.array([means.get(tuple(row[key] for key in keys), fallback) for _, row in target.iterrows()])


def _speed_predict(train: pd.DataFrame, target: pd.DataFrame) -> np.ndarray:
    fallback = float(train["actual_eta_min"].median())
    speed = np.maximum(pd.to_numeric(target["speed_kmh"], errors="coerce").fillna(0).to_numpy(), 1.0)
    distance = pd.to_numeric(target["distance_to_next_stop_m"], errors="coerce").fillna(0).to_numpy()
    prediction = distance * 60.0 / (speed * 1000.0)
    invalid = (~np.isfinite(prediction)) | (prediction <= 0) | (target["speed_kmh"].to_numpy(dtype=float) < 1.0)
    prediction[invalid] = fallback
    return prediction


def _make_pipeline(estimator) -> Pipeline:
    categorical = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    numeric = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])
    transform = ColumnTransformer(
        [("categorical", categorical, CATEGORICAL), ("numeric", numeric, NUMERIC)],
        remainder="drop",
        sparse_threshold=0,
    )
    return Pipeline([("features", transform), ("model", estimator)])


def _feature_frame(frame: pd.DataFrame) -> pd.DataFrame:
    columns = CATEGORICAL + NUMERIC
    features = frame[columns].copy()
    features["route_id"] = features["route_id"].astype(str)
    features["direction_id"] = features["direction_id"].astype(str)
    return features


def _event_match_metrics(labels: pd.DataFrame, alerts: pd.DataFrame, event_type: str, tolerance_seconds: int = 30) -> dict:
    truth = labels[labels.get("event_type", pd.Series(dtype=str)) == event_type].to_dict("records")
    predicted = alerts[alerts.get("alert_type", pd.Series(dtype=str)) == event_type].to_dict("records")
    candidates = []
    for pi, alert in enumerate(predicted):
        for ti, event in enumerate(truth):
            if alert.get("route_id") != event.get("route_id"):
                continue
            a = alert.get("timestamp_utc") or alert.get("start_utc")
            b = event.get("start_utc")
            if not a or not b:
                continue
            delta = abs((pd.Timestamp(a) - pd.Timestamp(b)).total_seconds())
            if event_type == "delay":
                # Delay labels and alerts are one event per trip. The alert may
                # cross its chosen threshold at a later stop than the fixed
                # truth rule, so trip identity is the correct event match.
                same_trip = alert.get("trip_id") == event.get("trip_id")
                same_day = alert.get("service_date") == event.get("service_date")
                if same_trip and same_day:
                    candidates.append((delta, pi, ti))
            elif (
                delta <= tolerance_seconds
                and (not alert.get("stop_id") or not event.get("stop_id") or alert.get("stop_id") == event.get("stop_id"))
            ):
                candidates.append((delta, pi, ti))
    matched_alerts, matched_events = set(), set()
    for _, pi, ti in sorted(candidates):
        if pi not in matched_alerts and ti not in matched_events:
            matched_alerts.add(pi)
            matched_events.add(ti)
    tp = len(matched_events)
    fp = len(predicted) - len(matched_alerts)
    fn = len(truth) - len(matched_events)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"true_events": len(truth), "alerts": len(predicted), "tp": tp, "fp": fp, "fn": fn, "precision": precision, "recall": recall, "f1": f1, "matching_method": "same route/trip/service date" if event_type == "delay" else "same route/stop within time tolerance", "matching_tolerance_seconds": None if event_type == "delay" else tolerance_seconds}


def _sensitivity_event_metrics(rows: pd.DataFrame, test_days: set[str], threshold_values: dict | None = None) -> dict:
    if "service_date" in rows:
        rows = rows[rows.service_date.astype(str).isin(test_days)]
    result = {}
    for threshold_type, values in (threshold_values or {}).items():
        event_type = "delay" if threshold_type == "delay_minutes" else "bunching"
        for value in values:
            key = f"{threshold_type}={float(value):g}"
            result[key] = _event_match_metrics(pd.DataFrame(), pd.DataFrame(), event_type)
    if rows.empty or not {"threshold_type", "threshold_value", "dataset"}.issubset(rows.columns):
        return result
    for (threshold_type, threshold_value), group in rows.groupby(["threshold_type", "threshold_value"]):
        labels = group[group.dataset == "truth"]
        alerts = group[group.dataset == "detector"]
        event_type = "delay" if threshold_type == "delay_minutes" else "bunching"
        result[f"{threshold_type}={float(threshold_value):g}"] = _event_match_metrics(labels, alerts, event_type)
    return result


def _select_event_threshold(validation_results: dict, threshold_type: str, default_value: float) -> tuple[float, str]:
    candidates = []
    prefix = threshold_type + "="
    for key, result in validation_results.items():
        if key.startswith(prefix):
            value = float(key[len(prefix):])
            # Maximize validation F1; ties prefer the predeclared default, then
            # the numerically smaller threshold for deterministic selection.
            # With no positive validation truth, F1 cannot distinguish detector
            # settings. Preserve the predeclared threshold instead of selecting
            # the setting that merely emits the fewest alerts.
            if int(result.get("true_events", 0)) > 0:
                candidates.append((-float(result["f1"]), abs(value - default_value), value, key))
    if not candidates:
        default_key = f"{threshold_type}={float(default_value):g}"
        if default_key not in validation_results:
            raise ValueError(f"No validation sensitivity results for {threshold_type}")
        return float(default_value), default_key
    _, _, value, key = min(candidates)
    return value, key


def evaluate_run(run_dir: str | Path, output_dir: str | Path = "results/generated", train_days: int = 18, validation_days: int = 5, test_days: int = 5) -> Path:
    """Train the candidate ladder, select from validation, and score the test block once."""
    run_path = Path(run_dir)
    frame = _load_frame(run_path)
    train, validation, test = chronological_days(frame, train_days, validation_days, test_days)
    y_train, y_validation, y_test = train.actual_eta_min.to_numpy(), validation.actual_eta_min.to_numpy(), test.actual_eta_min.to_numpy()
    x_train, x_validation, x_test = map(_feature_frame, (train, validation, test))

    estimators = {
        "Ridge": Ridge(alpha=1.0),
        "RandomForest": RandomForestRegressor(n_estimators=80, max_depth=12, min_samples_leaf=3, max_features=0.8, random_state=2026, n_jobs=-1),
        "GradientBoosting": GradientBoostingRegressor(n_estimators=80, learning_rate=0.05, max_depth=2, loss="huber", random_state=2026),
    }
    complexity = ["HistoricalMean", "MovingSpeed", "Ridge", "RandomForest", "GradientBoosting"]
    fitted, validation_results, validation_predictions = {}, {}, {}
    for name in complexity:
        if name == "HistoricalMean":
            prediction = _historical_predict(train, validation)
        elif name == "MovingSpeed":
            prediction = _speed_predict(train, validation)
        else:
            model = _make_pipeline(estimators[name])
            model.fit(x_train, y_train)
            fitted[name] = model
            prediction = model.predict(x_validation)
        validation_predictions[name] = prediction
        validation_results[name] = _metrics(y_validation, prediction)

    best_rmse = min(result["rmse_min"] for result in validation_results.values())
    rmse_eligible = [name for name in complexity if validation_results[name]["rmse_min"] <= best_rmse * 1.05]
    best_mae = min(validation_results[name]["mae_min"] for name in rmse_eligible)
    eligible = [name for name in complexity if name in rmse_eligible and validation_results[name]["mae_min"] <= best_mae * 1.05]
    # Among models within 5% of the best validation MAE and RMSE, keep the
    # first candidate in the declared simple-to-complex ordering.
    selected = next(name for name in complexity if name in eligible)

    # Refit the selected learned estimator on train+validation only after model
    # selection; the held-out test block is still unseen until this final pass.
    train_validation = pd.concat([train, validation], ignore_index=True)
    y_train_validation = train_validation.actual_eta_min.to_numpy()
    x_train_validation = _feature_frame(train_validation)
    final_models, test_predictions_by_model, test_results = {}, {}, {}
    for name in complexity:
        if name == "HistoricalMean":
            prediction = _historical_predict(train_validation, test)
        elif name == "MovingSpeed":
            prediction = _speed_predict(train_validation, test)
        else:
            model = _make_pipeline(estimators[name])
            model.fit(x_train_validation, y_train_validation)
            final_models[name] = model
            prediction = model.predict(x_test)
        test_predictions_by_model[name] = prediction
        test_results[name] = _metrics(y_test, prediction)
    final_model = final_models.get(selected)
    test_prediction = test_predictions_by_model[selected]
    test_predictions = pd.DataFrame({
        "prediction_id": test["prediction_id"].to_numpy(),
        "service_date": test["service_date"].to_numpy(),
        "route_id": test["route_id"].to_numpy(),
        "target_stop_id": test["target_stop_id"].to_numpy(),
        "actual_eta_min": y_test,
        "predicted_eta_min": test_prediction,
        "model": selected,
    })

    label_path, alert_path = run_path / "event_labels.csv", run_path / "detector_alerts.csv"
    labels = pd.read_csv(label_path) if label_path.is_file() else pd.DataFrame()
    alerts = pd.read_csv(alert_path) if alert_path.is_file() else pd.DataFrame()
    test_days = set(test.service_date.unique())
    if "service_date" in labels:
        labels = labels[labels.service_date.astype(str).isin(test_days)]
    if "service_date" in alerts:
        alerts = alerts[alerts.service_date.astype(str).isin(test_days)]
    event_results = {
        "delay": _event_match_metrics(labels, alerts, "delay"),
        "bunching": _event_match_metrics(labels, alerts, "bunching"),
    }
    sensitivity_path = run_path / "event_sensitivity.csv"
    sensitivity_rows = pd.read_csv(sensitivity_path) if sensitivity_path.is_file() else pd.DataFrame()
    manifest = json.loads((run_path / "manifest.json").read_text(encoding="utf-8"))
    validation_days = set(validation.service_date.unique())
    default_rules = manifest.get("event_rules", {})
    threshold_values = {
        "delay_minutes": sorted(set([float(default_rules.get("delay_minutes", 5.0)), *map(float, default_rules.get("delay_sensitivity_minutes", []))])),
        "bunching_ratio": sorted(set([float(default_rules.get("bunching_headway_ratio", 0.5)), *map(float, default_rules.get("bunching_sensitivity_ratios", []))])),
    }
    validation_sensitivity = _sensitivity_event_metrics(sensitivity_rows, validation_days, threshold_values)
    test_sensitivity = _sensitivity_event_metrics(sensitivity_rows, test_days, threshold_values)
    selected_event_thresholds = {}
    for event_type, threshold_type, default_value in (
        ("delay", "delay_minutes", float(default_rules.get("delay_minutes", 5.0))),
        ("bunching", "bunching_ratio", float(default_rules.get("bunching_headway_ratio", 0.5))),
    ):
        selected_value, result_key = _select_event_threshold(validation_sensitivity, threshold_type, default_value)
        selected_event_thresholds[event_type] = {
            "threshold_type": threshold_type,
            "selected_threshold": selected_value,
            "validation_metrics": validation_sensitivity[result_key],
            "test_metrics": test_sensitivity.get(result_key, {}),
            "selection_rule": "highest validation event F1 among settings with positive validation truth; ties prefer the configured default, then the smaller threshold; retain configured default if validation truth is empty",
        }
    metrics = {
        "run_id": json.loads((run_path / "manifest.json").read_text(encoding="utf-8")).get("run_id", run_path.name),
        "split": {"train_days": sorted(train.service_date.unique()), "validation_days": sorted(validation.service_date.unique()), "test_days": sorted(test.service_date.unique())},
        "validation_models": validation_results,
        "selection": {"selected_model": selected, "best_validation_rmse_min": best_rmse, "eligible_models": eligible, "rule": "lowest MAE among candidates with RMSE within 5% of best validation RMSE; use stated simplicity order for ties"},
        "test": {
            "selected_model": selected,
            "models": test_results,
            "selected_model_breakdown": {
                "route_id": _group_metrics(test, y_test, test_prediction, "route_id"),
                "hour_local": _group_metrics(test, y_test, test_prediction, "hour_local"),
            },
        },
        "events": event_results,
        "event_threshold_selection": selected_event_thresholds,
        "event_threshold_sensitivity": test_sensitivity,
        "limitations": ["Synthetic-data-only evaluation; does not validate live BMTC operations.", "Event scores depend on simulator event rules and matching tolerance."],
    }
    destination = Path(output_dir) / metrics["run_id"]
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")
    test_predictions.to_csv(destination / "test_predictions.csv", index=False)
    if final_model is not None:
        import joblib
        joblib.dump(final_model, destination / "eta_model.joblib")
    return destination
