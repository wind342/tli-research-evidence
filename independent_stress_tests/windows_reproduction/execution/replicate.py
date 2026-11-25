"""Run new seeds through the unchanged archived model and prediction code."""
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import sys


ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT.parent / "p/research_source/independent_stress_tests"
INPUTS = ROOT / "inputs"
PREDICTOR = ROOT / "predictor"
TABLE3 = ROOT / "table3"
GNN_SEEDS = (202611801, 202611802, 202611803)
SNN_SEEDS = (71101, 71102, 71103, 71104)
PLAN = ROOT / "REPLICATION_PLAN.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def write(path, data):
    with path.open("x", encoding="utf-8") as output:
        json.dump(data, output, indent=2, sort_keys=True, allow_nan=False)
        output.write("\n")


def freeze():
    INPUTS.mkdir(exist_ok=False)
    PREDICTOR.mkdir(exist_ok=False)
    tools = (
        ("gnn/gnn_tlir_counterexample.py", INPUTS),
        ("snn/snn_tlir_adversarial.py", INPUTS),
        ("snn/snn_tlir_independent_checker.py", INPUTS),
        ("tlp01_prediction/tlp01_cross_system.py", PREDICTOR),
        ("tlp01_prediction/independent_checker.py", PREDICTOR),
    )
    for name, folder in tools:
        shutil.copyfile(ARCHIVE / name, folder / Path(name).name)

    gnn = ARCHIVE / "gnn/gnn_falsification_frozen.json"
    snn = ARCHIVE / "snn/snn_tlir_frozen_protocol.json"
    table = ARCHIVE / "tlp01_prediction/FROZEN_PROTOCOL.json"
    gnn_protocol, snn_protocol, table_protocol = [read(p) for p in (gnn, snn, table)]
    assert not set(GNN_SEEDS).intersection(gnn_protocol["formal_seeds"] + [gnn_protocol["pilot_seed"]])
    assert not set(SNN_SEEDS).intersection(snn_protocol["formal_seeds"] + [snn_protocol["pilot_seed"]])
    for expected, staged_source in (
        (gnn_protocol["source_sha256"], INPUTS / "gnn_tlir_counterexample.py"),
        (snn_protocol["source_sha256"], INPUTS / "snn_tlir_adversarial.py"),
        (snn_protocol["independent_checker_sha256"], INPUTS / "snn_tlir_independent_checker.py"),
        (table_protocol["predictor_source_sha256"], PREDICTOR / "tlp01_cross_system.py"),
    ):
        assert expected == sha(staged_source), staged_source.name
    gnn_protocol["formal_seeds"] = list(GNN_SEEDS)
    snn_protocol["formal_seeds"] = list(SNN_SEEDS)
    table_protocol.update(gnn_seeds=list(GNN_SEEDS), snn_seeds=list(SNN_SEEDS), date="2026-11-18",
                          evidence_type="New-seed independent training. Predictions sealed before endpoint adjudication.")
    write(INPUTS / gnn.name, gnn_protocol)
    write(INPUTS / snn.name, snn_protocol)
    write(PREDICTOR / table.name, table_protocol)
    write(PLAN, {
        "date": "2026-11-18",
        "gnn_seeds": GNN_SEEDS,
        "snn_seeds": SNN_SEEDS,
        "seed_selection": "Fixed consecutive new IDs, disjoint from the archived pilot and formal seeds; retain every result.",
        "design": "Use the archived models, data-generation rules, training budgets, checkpoints, evaluation and thresholds.",
        "environment": {"platform": "Windows", "python": "3.12.10", "torch": "2.13.0+cpu", "numpy": "2.4.4",
                        "scipy": "1.17.1", "sklearn": "1.8.0", "openblas_num_threads": "1",
                        "omp_num_threads_environment": "1", "torch_threads": 2},
        "archived_protocols": {p.relative_to(ARCHIVE).as_posix(): sha(p) for p in (gnn, snn, table)},
        "frozen_inputs": {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted([*INPUTS.iterdir(), *PREDICTOR.iterdir()])},
        "runner_sha256": sha(Path(__file__)),
    })
    print("PLAN_SHA256", sha(PLAN), flush=True)


def validate_environment():
    import numpy
    import scipy
    import sklearn
    import torch

    plan = read(PLAN)
    assert sha(Path(__file__)) == plan["runner_sha256"]
    for name, expected in plan["frozen_inputs"].items():
        assert sha(ROOT / name) == expected, name
    observed = {"platform": platform.system(), "python": platform.python_version(), "torch": torch.__version__,
                "numpy": numpy.__version__, "scipy": scipy.__version__, "sklearn": sklearn.__version__,
                "openblas_num_threads": os.environ.get("OPENBLAS_NUM_THREADS"),
                "omp_num_threads_environment": os.environ.get("OMP_NUM_THREADS")}
    assert torch.version.cuda is None
    assert observed == {k: plan["environment"][k] for k in observed}, observed
    return torch


def train_gnn(torch):
    import gnn_tlir_counterexample as gnn

    assert torch.get_num_threads() == read(PLAN)["environment"]["torch_threads"]
    native = ROOT / "gnn-native"
    native.mkdir(exist_ok=False)
    original_relation_tests = gnn.relation_tests

    def capture(model, train, test, initial, records, seed):
        torch.save({"seed": seed, "initial": initial, "records": records, "test": test}, native / f"seed_{seed}.pt")
        return original_relation_tests(model, train, test, initial, records, seed)

    gnn.relation_tests = capture
    runs = []
    for seed in GNN_SEEDS:
        run = gnn.run(seed, formal=True)
        assert run["seed"] == seed
        write(native / f"seed_{seed}.json", run)
        runs.append(run)
        print("GNN", seed, run["train_log"][-1], run["gates"], flush=True)
    write(INPUTS / "gnn_tlir_formal_results.json", {
        "schema": "gnn_tlir_falsification_v1", "kind": "NEW_SEED_REPLICATION", "seeds": GNN_SEEDS,
        "runs": runs, "source_sha256": sha(INPUTS / "gnn_tlir_counterexample.py"),
        "torch": torch.__version__, "python": platform.python_version(), "replication_plan_sha256": sha(PLAN),
    })


def train_snn(torch):
    import snn_tlir_adversarial as snn

    assert torch.get_num_threads() == read(PLAN)["environment"]["torch_threads"]
    snn.SEEDS = SNN_SEEDS
    sys.argv = [str(INPUTS / "snn_tlir_adversarial.py"), "--formal",
                "--protocol", str(INPUTS / "snn_tlir_frozen_protocol.json"),
                "--output", str(INPUTS / "SNN_TLIR_formal")]
    snn.main()


def prediction_stage(stage, torch):
    import tlp01_cross_system as tlp

    tlp.SOURCE_ROOT, tlp.GNN_SEEDS, tlp.SNN_SEEDS = INPUTS, GNN_SEEDS, SNN_SEEDS
    if stage == "prepare":
        reference = read(INPUTS / "gnn_tlir_formal_results.json")

        def load_gnn(seed):
            data = torch.load(ROOT / f"gnn-native/seed_{seed}.pt", map_location="cpu", weights_only=False)
            assert data["seed"] == seed
            records = data["records"]
            identity = next(r["identities"] for r in reference["runs"] if r["seed"] == seed)
            state_sha = tlp.gnn.state_sha
            assert state_sha(data["initial"]) == identity["model_initial_sha256"]
            assert state_sha(records["final"]) == identity["final_sha256"]
            adj, features, labels, ids = data["test"]
            assert hashlib.sha256("".join(ids).encode()).hexdigest() == identity["test_rows_sha256"]
            events = {}
            endpoints = {}
            for row in identity["updates"]:
                step = row["step"]
                item = records[step]
                for key, field in (("pre", "pre_sha"), ("delta", "update_sha"), ("post", "post_sha")):
                    assert state_sha(item[key]) == row[field], (seed, step, field)
                assert all(torch.equal(item["post"][name] - value, item["delta"][name])
                           for name, value in item["pre"].items())
                assert hashlib.sha256(str(item["batch_ids"]).encode()).hexdigest() == row["batch_indices_sha"]
                events[step] = {"pre": item["pre"], "delta": item["delta"], "step": step,
                                "pre_sha": row["pre_sha"], "delta_sha": row["update_sha"], "post_sha": row["post_sha"]}
                endpoints[step] = {"post": item["post"], "step": step, "post_sha": row["post_sha"]}
            return {"seed": seed, "inputs": {"adj": adj, "x": features}, "labels": labels, "ids": ids,
                    "events": events, "original_results_sha256": sha(INPUTS / "gnn_tlir_formal_results.json")}, endpoints

        tlp.train_gnn_prepare = load_gnn
        tlp.prepare(TABLE3, "both")
    elif stage == "seal":
        tlp.seal(TABLE3)
    else:
        save = tlp.save_json

        def annotate_report(path, data):
            if path.name == "ADJUDICATION_REPORT.json":
                data["limitations"] = [
                    "Independent new-seed replication using the archived training rules and an alternate environment.",
                    "Predictions sealed from pre-state and actual update before adjudication reads post-state.",
                    "Seeds and environment both changed; this design does not estimate their effects separately.",
                    *data["limitations"][2:],
                ]
                data["replication_plan_sha256"] = sha(PLAN)
            save(path, data)

        tlp.save_json = annotate_report
        tlp.adjudicate(TABLE3)


def check_snn():
    import snn_tlir_independent_checker as checker

    checker.SEEDS = SNN_SEEDS
    checker.check(INPUTS / "SNN_TLIR_formal", INPUTS / "snn_tlir_frozen_protocol.json")


def check_prediction():
    import independent_checker as checker

    checker.SOURCE = INPUTS
    write(TABLE3 / "INDEPENDENT_CHECK_RESULT.json", checker.check(TABLE3))


def main():
    stage = sys.argv[1]
    if stage == "freeze":
        freeze()
        return
    sys.path[:0] = [str(INPUTS), str(PREDICTOR), str(ROOT / "deps")]
    torch = validate_environment()
    if stage == "gnn":
        train_gnn(torch)
    elif stage == "snn":
        train_snn(torch)
    elif stage in ("prepare", "seal", "adjudicate"):
        prediction_stage(stage, torch)
    elif stage == "check-snn":
        check_snn()
    elif stage == "check-prediction":
        check_prediction()
    else:
        raise ValueError(stage)


if __name__ == "__main__":
    main()
