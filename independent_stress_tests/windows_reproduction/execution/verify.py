"""Verify the packaged GNN/SNN evidence or repeat the frozen training run."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest():
    for name, expected in read(ROOT / "SHA256_MANIFEST.json").items():
        path = ROOT / name
        if not path.is_file() or ROOT not in path.resolve().parents or sha(path) != expected:
            raise ValueError(f"Hash mismatch: {name}")


def replay():
    sys.path[:0] = [str(ROOT / name) for name in ("inputs", "predictor")]
    import independent_checker as prediction
    import snn_tlir_independent_checker as snn

    os.chdir(ROOT)
    snn.SEEDS = tuple(read(ROOT / "REPLICATION_PLAN.json")["snn_seeds"])
    snn.check(ROOT / "inputs/SNN_TLIR_formal", ROOT / "inputs/snn_tlir_frozen_protocol.json")
    prediction.SOURCE = ROOT / "inputs"
    observed = prediction.check(ROOT / "table3")
    assert observed == read(ROOT / "table3/INDEPENDENT_CHECK_RESULT.json")


def fresh(output):
    output = output.resolve()
    if output == ROOT or ROOT in output.parents:
        raise ValueError("Choose an output directory outside the evidence package")
    output.mkdir(parents=True, exist_ok=False)
    plan = read(ROOT / "REPLICATION_PLAN.json")
    for name in ["replicate.py", "REPLICATION_PLAN.json", *plan["frozen_inputs"]]:
        dest = output / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, dest)
    stages = ("gnn", "snn", "check-snn", "prepare", "seal", "adjudicate", "check-prediction")
    for stage in stages:
        subprocess.run([sys.executable, "-B", str(output / "replicate.py"), stage], check=True)
    for name, key in (
        ("inputs/gnn_tlir_formal_results.json", "runs"),
        ("inputs/SNN_TLIR_formal/FORMAL_SUMMARY.json", "runs"),
        ("table3/ADJUDICATION_REPORT.json", "system_summary"),
        ("table3/PREDICTIONS_SEALED.json", "events"),
    ):
        assert read(output / name)[key] == read(ROOT / name)[key], name
    print("FRESH_TRAINING_AND_SEALED_PREDICTIONS_MATCH")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fresh", type=Path, help="New output directory for training from scratch")
    args = parser.parse_args()
    os.environ["OPENBLAS_NUM_THREADS"] = os.environ["OMP_NUM_THREADS"] = "1"
    verify_manifest()
    if args.fresh is None:
        replay()
    else:
        fresh(args.fresh)


if __name__ == "__main__":
    main()
