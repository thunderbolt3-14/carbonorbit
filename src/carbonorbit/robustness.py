"""Apply the normal-scenario model unchanged to noisy/dropout test runs."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .analytics import _event_match_metrics, _feature_frame, _historical_predict, _metrics, _sensitivity_event_metrics, _speed_predict, _load_frame, chronological_days


def evaluate_robustness(normal_run: str | Path, variant_runs: list[str | Path], output_dir: str | Path = "results/generated") -> Path:
    baseline_path = Path(normal_run)
    normal_frame = _load_frame(baseline_path)
    train, validation, test = chronological_days(normal_frame)
    metrics_path = Path(output_dir) / json.loads((baseline_path / "manifest.json").read_text(encoding="utf-8"))["run_id"] / "metrics.json"
    base_metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    selected = base_metrics["selection"]["selected_model"]
    model_path = metrics_path.parent / "eta_model.joblib"
    model = None
    if model_path.is_file():
        import joblib
        model = joblib.load(model_path)
    train_validation = pd.concat([train, validation], ignore_index=True)
    results = {}
    for raw_variant in variant_runs:
        variant_path = Path(raw_variant)
        variant = _load_frame(variant_path)
        _, _, variant_test = chronological_days(variant)
        if model is not None:
            prediction = model.predict(_feature_frame(variant_test))
        elif selected == "HistoricalMean":
            prediction = _historical_predict(train_validation, variant_test)
        else:
            prediction = _speed_predict(train_validation, variant_test)
        variant_manifest = json.loads((variant_path / "manifest.json").read_text(encoding="utf-8"))
        name = variant_manifest["scenario"]
        variant_truth = pd.read_csv(variant_path / "event_labels.csv")
        variant_alerts = pd.read_csv(variant_path / "detector_alerts.csv")
        sensitivity_path = variant_path / "event_sensitivity.csv"
        sensitivity = pd.read_csv(sensitivity_path) if sensitivity_path.is_file() else pd.DataFrame()
        test_days = set(variant_test.service_date.unique())
        if "service_date" in variant_truth:
            variant_truth = variant_truth[variant_truth.service_date.astype(str).isin(test_days)]
        if "service_date" in variant_alerts:
            variant_alerts = variant_alerts[variant_alerts.service_date.astype(str).isin(test_days)]
        variant_sensitivity = _sensitivity_event_metrics(sensitivity, test_days, {
            "delay_minutes": [variant_manifest.get("event_rules", {}).get("delay_minutes", 5.0), *variant_manifest.get("event_rules", {}).get("delay_sensitivity_minutes", [])],
            "bunching_ratio": [variant_manifest.get("event_rules", {}).get("bunching_headway_ratio", 0.5), *variant_manifest.get("event_rules", {}).get("bunching_sensitivity_ratios", [])],
        })
        normal_selected_event_scores = {}
        for event_type, selection in base_metrics.get("event_threshold_selection", {}).items():
            threshold_key = f"{selection['threshold_type']}={float(selection['selected_threshold']):g}"
            normal_selected_event_scores[event_type] = {
                "selected_on_normal_validation_threshold": selection["selected_threshold"],
                "metrics": variant_sensitivity.get(threshold_key, {}),
            }
        results[name] = {
            "run_id": variant_manifest["run_id"],
            "eta_test": _metrics(variant_test.actual_eta_min, prediction),
            "events": {
                "delay": _event_match_metrics(variant_truth, variant_alerts, "delay"),
                "bunching": _event_match_metrics(variant_truth, variant_alerts, "bunching"),
            },
            "event_threshold_sensitivity": variant_sensitivity,
            "events_at_normal_selected_thresholds": normal_selected_event_scores,
            "model": selected,
            "note": "The model selected on the normal run was applied without refitting.",
        }
    destination = metrics_path.parent / "robustness.json"
    destination.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    return destination
