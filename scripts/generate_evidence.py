"""Create compact report figures and tables from a completed synthetic run."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carbonorbit.analytics import _event_match_metrics  # noqa: E402

ROUTE_NAMES = {
    "BMTC:dd9ea3794c96": "285-M KBS-BMSIT",
    "BMTC:6f4d45186ddd": "285 BMSITY-YHKOT",
    "BMTC:b202977c0fc0": "406",
}
BOOTSTRAP_SEED = 20261121
BOOTSTRAP_REPLICATES = 10_000


def route_tables(metrics: dict, predictions: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    route_metrics = metrics["test"]["selected_model_breakdown"]["route_id"]
    route_rows = []
    stability_rows = []
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    predictions = predictions.copy()
    predictions["absolute_error_min"] = (
        predictions.actual_eta_min - predictions.predicted_eta_min
    ).abs()
    for route_id, values in sorted(route_metrics.items()):
        route_rows.append({
            "route_id": route_id,
            "route_name": ROUTE_NAMES.get(route_id, route_id),
            "test_predictions": values["count"],
            "mae_min": values["mae_min"],
            "rmse_min": values["rmse_min"],
            "p90_absolute_error_min": values["p90_absolute_error_min"],
            "within_2min_pct": values["within_2min_pct"],
        })
        part = predictions[predictions.route_id == route_id]
        days = sorted(part.service_date.astype(str).unique())
        day_errors = [part[part.service_date.astype(str) == day].absolute_error_min.to_numpy() for day in days]
        estimates = np.empty(BOOTSTRAP_REPLICATES, dtype=float)
        for index in range(BOOTSTRAP_REPLICATES):
            chosen = rng.integers(0, len(day_errors), size=len(day_errors))
            sampled = [day_errors[day_index] for day_index in chosen]
            estimates[index] = float(np.concatenate(sampled).mean())
        stability_rows.append({
            "route_id": route_id,
            "route_name": ROUTE_NAMES.get(route_id, route_id),
            "test_predictions": len(part),
            "test_days": len(days),
            "pooled_mae_min": float(part.absolute_error_min.mean()),
            "day_cluster_bootstrap_ci95_low_min": float(np.quantile(estimates, 0.025)),
            "day_cluster_bootstrap_ci95_high_min": float(np.quantile(estimates, 0.975)),
            "bootstrap_replicates": BOOTSTRAP_REPLICATES,
            "bootstrap_seed": BOOTSTRAP_SEED,
        })
    route_table = pd.DataFrame(route_rows)
    stability_table = pd.DataFrame(stability_rows)

    hour_metrics = metrics["test"]["selected_model_breakdown"]["hour_local"]
    hour_table = pd.DataFrame([
        {"hour_local": int(hour), **values}
        for hour, values in sorted(hour_metrics.items(), key=lambda item: int(item[0]))
    ])
    return route_table, hour_table, stability_table


def threshold_table(run_dir: Path, metrics: dict) -> pd.DataFrame:
    sensitivity = pd.read_csv(run_dir / "event_sensitivity.csv")
    train_days = set(metrics["split"]["train_days"])
    validation_days = set(metrics["split"]["validation_days"])
    test_days = set(metrics["split"]["test_days"])
    selected = {
        event_type: float(details["selected_threshold"])
        for event_type, details in metrics["event_threshold_selection"].items()
    }
    rows = []
    for (threshold_type, threshold_value), group in sensitivity.groupby(["threshold_type", "threshold_value"]):
        event_type = "delay" if threshold_type == "delay_minutes" else "bunching"
        threshold_value = float(threshold_value)
        for split_name, dates in (("validation", validation_days), ("test", test_days)):
            part = group[group.service_date.astype(str).isin(dates)]
            labels = part[part.dataset == "truth"]
            alerts = part[part.dataset == "detector"]
            score = _event_match_metrics(labels, alerts, event_type)
            rows.append({
                "event_type": event_type,
                "threshold_type": threshold_type,
                "threshold_value": threshold_value,
                "split": split_name,
                "selected_on_validation": split_name == "validation" and threshold_value == selected[event_type],
                **score,
            })
    return pd.DataFrame(rows).sort_values(["event_type", "threshold_value", "split"]).reset_index(drop=True)


def make_figures(route_table: pd.DataFrame, hour_table: pd.DataFrame, sensitivity: pd.DataFrame, out: Path) -> None:
    plt.rcParams.update({"font.size": 10, "axes.titlesize": 12, "figure.dpi": 150})

    stability = pd.read_csv(out / "eta_cluster_bootstrap.csv")
    plot = stability.sort_values("pooled_mae_min")
    labels = [f"{row.route_name}\n(n={row.test_predictions:,}; {row.test_days} days)" for row in plot.itertuples()]
    lower = plot.pooled_mae_min.to_numpy() - plot.day_cluster_bootstrap_ci95_low_min.to_numpy()
    upper = plot.day_cluster_bootstrap_ci95_high_min.to_numpy() - plot.pooled_mae_min.to_numpy()
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    ax.bar(range(len(plot)), plot.pooled_mae_min, color="#247ba0", width=0.62)
    ax.errorbar(range(len(plot)), plot.pooled_mae_min, yerr=np.vstack([lower, upper]), fmt="none", ecolor="#12263a", capsize=5)
    ax.set_xticks(range(len(plot)), labels)
    ax.set_ylabel("Test MAE (minutes)")
    ax.set_title("ETA error by route — synthetic held-out test")
    ax.text(0.01, -0.27, "Bars: pooled test MAE. Whiskers: exploratory 95% bootstrap interval resampling five service days.", transform=ax.transAxes, fontsize=8)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(out / "eta_error_by_route.png", bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    ax.plot(hour_table.hour_local, hour_table.mae_min, marker="o", color="#247ba0")
    for row in hour_table.itertuples():
        ax.annotate(f"n={row.count:,}", (row.hour_local, row.mae_min), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=7)
    ax.set_xticks(hour_table.hour_local)
    ax.set_xlabel("Local hour")
    ax.set_ylabel("Test MAE (minutes)")
    ax.set_title("ETA error by local hour — synthetic held-out test")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(out / "eta_error_by_hour.png", bbox_inches="tight")
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.8))
    for ax, event_type, title in zip(axes, ("delay", "bunching"), ("Delay threshold", "Bunching threshold")):
        part = sensitivity[sensitivity.event_type == event_type]
        threshold_rows = sorted(part.threshold_value.unique())
        positions = np.arange(len(threshold_rows))
        width = 0.36
        for offset, split_name, color in ((-width / 2, "validation", "#70c1b3"), (width / 2, "test", "#f25f5c")):
            points = part[part.split == split_name].set_index("threshold_value")
            vals = [float(points.loc[value, "f1"]) for value in threshold_rows]
            ax.bar(positions + offset, vals, width, label=split_name.title(), color=color)
        tick_labels = []
        for value in threshold_rows:
            if event_type == "delay":
                tick_labels.append(f"{value:g} min")
            else:
                tick_labels.append(f"{value:.0%} headway")
        ax.set_xticks(positions, tick_labels, rotation=15)
        ax.set_ylim(0, 1.05)
        ax.set_ylabel("Event F1")
        ax.set_title(title)
        ax.grid(axis="y", alpha=0.25)
        ax.legend(frameon=False)
        for idx, value in enumerate(threshold_rows):
            test_row = part[(part.threshold_value == value) & (part.split == "test")].iloc[0]
            ax.text(idx + width / 2, min(1.02, test_row.f1 + 0.025), f"{test_row.true_events} truth / {test_row.alerts} alerts", ha="center", fontsize=7, rotation=0)
    fig.suptitle("Threshold sensitivity; selection uses validation only", y=1.02, fontsize=12)
    fig.text(0.5, -0.03, "Test bars are sensitivity reporting after selection, not a tuning input. Event counts are simulator-generated.", ha="center", fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "event_threshold_sensitivity.png", bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args()
    run_id = args.run_id
    result_dir = ROOT / "results" / "generated" / run_id
    run_dir = ROOT / "data" / "simulated" / run_id / "normal"
    out = Path(args.output_dir) if args.output_dir else ROOT / "docs" / "report" / "evidence" / run_id
    if not out.is_absolute():
        out = ROOT / out
    out.mkdir(parents=True, exist_ok=True)

    metrics = json.loads((result_dir / "metrics.json").read_text(encoding="utf-8"))
    predictions = pd.read_csv(result_dir / "test_predictions.csv")
    route_table, hour_table, stability_table = route_tables(metrics, predictions)
    sensitivity = threshold_table(run_dir, metrics)
    route_table.to_csv(out / "eta_error_by_route.csv", index=False)
    hour_table.to_csv(out / "eta_error_by_hour.csv", index=False)
    stability_table.to_csv(out / "eta_cluster_bootstrap.csv", index=False)
    sensitivity.to_csv(out / "event_threshold_sensitivity.csv", index=False)
    shutil.copy2(result_dir / "metrics.json", out / "metrics.json")
    shutil.copy2(run_dir / "manifest.json", out / "run_manifest.json")
    shutil.copy2(result_dir / "robustness.json", out / "robustness.json")
    make_figures(route_table, hour_table, sensitivity, out)
    print(f"evidence_dir={out}")
    print(f"routes={len(route_table)} hours={len(hour_table)} threshold_rows={len(sensitivity)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
