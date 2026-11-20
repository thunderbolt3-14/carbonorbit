"""Command-line entry point for carbonOrbit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carbonorbit.analytics import evaluate_run
from carbonorbit.api import create_app
from carbonorbit.config import load_config
from carbonorbit.db import ingest_run
from carbonorbit.robustness import evaluate_robustness
from carbonorbit.simulator import simulate


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Simulate, evaluate, and serve carbonOrbit artifacts.")
    result.add_argument("--config", default="config/simulation.yaml", help="Simulation YAML path")
    commands = result.add_subparsers(dest="command", required=True)
    sim = commands.add_parser("simulate", help="Generate a seeded GTFS-based synthetic run")
    sim.add_argument("--scenario", default="normal")
    sim.add_argument("--output-root", default="data/simulated")
    evaluate = commands.add_parser("evaluate", help="Fit models and score one run")
    evaluate.add_argument("--run-dir", required=True)
    evaluate.add_argument("--output-dir", default="results/generated")
    evaluate.add_argument("--train-days", type=int, default=18)
    evaluate.add_argument("--validation-days", type=int, default=5)
    evaluate.add_argument("--test-days", type=int, default=5)
    ingest = commands.add_parser("ingest", help="Load run outputs into the local SQLite demo database")
    ingest.add_argument("--run-dir", required=True)
    ingest.add_argument("--evaluation-dir")
    ingest.add_argument("--database", default="data/carbonorbit.db")
    all_command = commands.add_parser("all", help="Run simulation, evaluation, and API database ingestion")
    all_command.add_argument("--scenario", default="normal")
    all_command.add_argument("--output-root", default="data/simulated")
    all_command.add_argument("--results-dir", default="results/generated")
    all_command.add_argument("--database", default="data/carbonorbit.db")
    suite = commands.add_parser("suite", help="Run normal and robustness scenarios; reuse the normal-selected model")
    suite.add_argument("--output-root", default="data/simulated")
    suite.add_argument("--results-dir", default="results/generated")
    suite.add_argument("--database", default="data/carbonorbit.db")
    serve = commands.add_parser("serve", help="Serve the local dashboard and JSON API")
    serve.add_argument("--database", default="data/carbonorbit.db")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=5000)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "serve":
            app = create_app(args.database, ROOT / "dashboard")
            app.run(host=args.host, port=args.port, debug=False)
            return 0
        config = load_config(args.config)
        if args.command == "simulate":
            print(simulate(config, args.scenario, args.output_root))
        elif args.command == "evaluate":
            print(evaluate_run(args.run_dir, args.output_dir, args.train_days, args.validation_days, args.test_days))
        elif args.command == "ingest":
            print(ingest_run(args.database, args.run_dir, args.evaluation_dir))
        elif args.command == "all":
            run_dir = simulate(config, args.scenario, args.output_root)
            eval_dir = evaluate_run(run_dir, args.results_dir)
            run_id = ingest_run(args.database, run_dir, eval_dir)
            print(f"run_id={run_id}\nrun_dir={run_dir}\nevaluation_dir={eval_dir}\ndatabase={args.database}")
        elif args.command == "suite":
            normal_dir = simulate(config, "normal", args.output_root)
            noisy_dir = simulate(config, "noisy_gps", args.output_root)
            dropout_dir = simulate(config, "high_dropout", args.output_root)
            eval_dir = evaluate_run(normal_dir, args.results_dir)
            robustness_path = evaluate_robustness(normal_dir, [noisy_dir, dropout_dir], args.results_dir)
            run_id = ingest_run(args.database, normal_dir, eval_dir)
            print(f"run_id={run_id}\nnormal_run={normal_dir}\nrobustness={robustness_path}\ndatabase={args.database}")
        return 0
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"carbonOrbit: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
