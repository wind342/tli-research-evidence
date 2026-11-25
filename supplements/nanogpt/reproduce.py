"""Fresh, resumable nanoGPT supplementary runs with the frozen capture implementation."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
FAMILY = "experiments.gfg_nanogpt_autonomous_capability_discovery_v1"
SHARED_E05_PROTOCOL = ROOT / "PROTOCOL_E05_SHARED_TASK.json"


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    temporary = path.with_suffix(path.suffix + ".pending")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def checked_source(source, trainer, protocol):
    source = source.resolve(strict=True)
    trainer = trainer.resolve(strict=True)
    if (trainer / ".git").exists():
        head = subprocess.check_output(["git", "-C", str(trainer), "rev-parse", "HEAD"], text=True).strip()
    else:
        export = read(trainer / "TRAINER_EXPORT.json")
        require(export["model_sha256"] == protocol["trainer_model_sha256"], "NANOGPT_EXPORT_IDENTITY_MISMATCH")
        head = export["upstream_commit"]
    require(head == protocol["trainer_commit"], "NANOGPT_COMMIT_MISMATCH")
    require(sha(trainer / "model.py") == protocol["trainer_model_sha256"], "NANOGPT_MODEL_MISMATCH")
    # Source remains an immutable input. The output root is never inside it.
    sys.path[:0] = [str(source), str(source / "src")]
    from experiments.gfg_nanogpt_autonomous_capability_discovery_v1 import experiment_instance as engine
    require(Path(engine.__file__).resolve().is_relative_to(source), "SOURCE_IMPORT_WRONG_TREE")
    contracts = Path(engine.__file__).parent / "contracts"
    profile = read(contracts / "training_profile.json")
    require(profile["max_steps"] == protocol["steps_per_history"], "STEP_COUNT_CHANGED")
    require(profile["evaluation_interval"] == protocol["evaluation_interval"], "EVAL_INTERVAL_CHANGED")
    bindings = {str(p.relative_to(source)): sha(p) for p in sorted(
        list((Path(engine.__file__).parent).glob("*.py")) + list(contracts.glob("*.json")))}
    return engine, bindings


def captured_protocol(root):
    frozen = read(root / "RUN_FREEZE.json")
    expected = root / "PROTOCOL.json"
    require(frozen["protocol_sha256"] == sha(expected), "CAPTURED_PROTOCOL_HASH_DRIFT")
    require(sha(expected) == sha(ROOT / "PROTOCOL.json") or
            (SHARED_E05_PROTOCOL.is_file() and sha(expected) == sha(SHARED_E05_PROTOCOL)),
            "UNKNOWN_CAPTURED_PROTOCOL")
    return read(expected)


def e05_input_keys(inputs, targets):
    import numpy as np
    from experiments.gfg_nanogpt_adjacent_response_transport_v1.inventory import sha256_bytes

    x, y = np.ascontiguousarray(inputs), np.asarray(targets, dtype=np.int64)
    require(x.shape == (212, 3) and x.dtype == np.int64 and y.shape == (212,), "E05_INPUT_SCHEMA_INVALID")
    keys = [(sha256_bytes(row.tobytes(order="C")), int(target)) for row, target in zip(x, y, strict=True)]
    require(len({key[0] for key in keys}) == 212, "E05_IDENTITIES_NOT_UNIQUE")
    return keys


def shared_task_preflight(engine, protocol):
    from itertools import combinations

    roster = protocol["runs"]
    require(len(roster) == 3 and all(r["role"] == "development" for r in roster), "E05_ROSTER_INVALID")
    require(all(len({r[k] for r in roster}) == 1 for k in ("token_seed", "split_seed")), "E05_TASK_NOT_SHARED")
    require(all(len({r[k] for r in roster}) == 3 for k in ("model_seed", "data_order_seed")), "E05_TRAINING_SEEDS_NOT_DISTINCT")
    train, validation, ordered = {}, {}, {}
    for row in roster:
        tag = row["id"]
        task = engine.build_formal_task(instance_id=tag, token_seed=row["token_seed"], split_seed=row["split_seed"])
        keys = e05_input_keys(task.validation_inputs.numpy(), task.validation_targets[:, -1].numpy())
        ordered[tag] = keys
        validation[tag] = {key[0] for key in keys}
        train[tag] = {hashlib.sha256(x.numpy().tobytes(order="C")).hexdigest() for x in task.train_inputs}
    require(all(not train[a] & validation[b] for a in train for b in validation), "E05_TRAIN_VALIDATION_OVERLAP")
    require(all(ordered[a] == ordered[b] and train[a] == train[b] for a, b in combinations(ordered, 2)),
            "E05_ORIGINAL_PAIRING_PREFLIGHT_FAILURE")
    return {"status": "PASS", "pairing_key": ["row_content_sha256", "target_group"],
            "ordered_keys_sha256": hashlib.sha256(json.dumps(next(iter(ordered.values()))).encode()).hexdigest(),
            "targets_per_history": 212, "shared_unique_targets_all_three": 212,
            "shared_unique_targets_by_pair": [{"histories": [a, b], "count": 212} for a, b in combinations(ordered, 2)],
            "cross_history_train_validation_overlap": 0}


def execute_histories(args, protocol, protocol_path=None, reuse_anchor=None, preflight_only=False):
    import numpy as np
    import torch

    engine, bindings = checked_source(args.source, args.trainer, protocol)
    output = args.output.resolve()
    for authority in (args.source.resolve(), args.trainer.resolve()):
        require(output != authority and not output.is_relative_to(authority), "OUTPUT_OVERLAPS_AUTHORITY")
    protocol_path = protocol_path or ROOT / "PROTOCOL.json"
    is_shared_task = protocol["schema"] == "tlir-e05-shared-task-v1"
    if is_shared_task:
        require(not output.exists() or (output / "RUN_FREEZE.json").is_file(), "SHARED_TASK_OUTPUT_NOT_FRESH")
        approval = shared_task_preflight(engine, protocol)
        if preflight_only:
            print(json.dumps(approval, indent=2), flush=True)
            return
    require(torch.cuda.is_available(), "CUDA_REQUIRED")
    fingerprint = {"protocol_sha256": sha(protocol_path), "source_sha256": bindings,
                   "runtime": {"python": platform.python_version(), "platform": platform.platform(),
                               "torch": torch.__version__, "cuda": torch.version.cuda,
                               "numpy": np.__version__, "device": torch.cuda.get_device_name()}}
    output.mkdir(parents=True, exist_ok=True)
    frozen = output / "RUN_FREEZE.json"
    if frozen.exists():
        require(read(frozen) == fingerprint, "RERUN_FREEZE_MISMATCH")
    else:
        shutil.copyfile(protocol_path, output / "PROTOCOL.json")
        write(frozen, fingerprint)
    if is_shared_task:
        preflight = output / "E05_ALIGNMENT_PREFLIGHT.json"
        if preflight.exists():
            require(read(preflight) == approval, "E05_PREFLIGHT_DRIFT")
        else:
            write(preflight, approval)
        print("E05 alignment preflight PASS: 212/212 shared native targets across all three histories", flush=True)
    histories = output / "histories"
    histories.mkdir(exist_ok=True)
    summary_path = output / "HISTORIES.json"
    summary = read(summary_path) if summary_path.exists() else {}
    if reuse_anchor is not None:
        require(is_shared_task, "ANCHOR_ONLY_FOR_SHARED_TASK_E05")
        old = reuse_anchor.resolve(strict=True)
        anchor = protocol["runs"][0]
        run = anchor["id"]
        previous_freeze = read(old / "RUN_FREEZE.json")
        require(previous_freeze["source_sha256"] == bindings and previous_freeze["runtime"] == fingerprint["runtime"],
                "E05_REUSE_ANCHOR_ENVIRONMENT_DRIFT")
        require(captured_protocol(old)["runs"][0] == anchor, "E05_REUSE_ANCHOR_SEEDS_DRIFT")
        src = old / "histories" / run
        dst = histories / run
        previous = read(old / "HISTORIES.json")[run]
        require(previous["status"] == "PASS" and previous["steps"] == protocol["steps_per_history"],
                "E05_REUSE_ANCHOR_INVALID")
        require(sha(src / "capture_manifest.json") == previous["capture_manifest_sha256"] and
                sha(src / "participant_gfg.sqlite3") == previous["database_sha256"] and
                (not (src / "participant_gfg.sqlite3-wal").exists() or
                 (src / "participant_gfg.sqlite3-wal").stat().st_size == 0), "E05_REUSE_ANCHOR_HASH_MISMATCH")
        if run not in summary:
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("*-wal", "*-shm", "*-journal"))
            summary[run] = {**previous, "reused_verified_capture": True}
            write(summary_path, summary)
    for row in protocol["runs"]:
        run = row["id"]
        native = histories / run
        if run in summary and summary[run]["status"] == "PASS":
            require(sha(native / "capture_manifest.json") == summary[run]["capture_manifest_sha256"],
                    "RESUME_CAPTURE_MANIFEST_MISMATCH")
            require(sha(native / "participant_gfg.sqlite3") == summary[run]["database_sha256"],
                    "RESUME_DATABASE_MISMATCH")
            print(run, "verified existing result", flush=True)
            continue
        require(not native.exists(), f"UNVERIFIED_ATTEMPT_RETAINED:{native}")
        task = engine.build_formal_task(instance_id=run, token_seed=row["token_seed"],
                                        split_seed=row["split_seed"])
        config = engine.frozen_training_config(model_seed=row["model_seed"],
                                               data_order_seed=row["data_order_seed"])
        free_before = shutil.disk_usage(output).free
        torch.cuda.reset_peak_memory_stats()
        started = time.monotonic()
        print(run, row["role"], "starting frozen", config.max_steps, "updates", flush=True)
        summary[run] = {"status": "RUNNING", "role": row["role"]}
        write(summary_path, summary)
        try:
            segment = engine.run_captured_segment(trainer_root=args.trainer.resolve(), task=task,
                                                  config=config, run_id=run, output_directory=native)
            require(segment["start_step"] == 0 and segment["stop_step"] == protocol["steps_per_history"],
                    "FORMAL_STEP_COVERAGE")
            database = native / "participant_gfg.sqlite3"
            summary[run] = {"status": "PASS", "role": row["role"], "steps": segment["stop_step"],
                            "evaluations": len(segment["metrics"]),
                            "capture_manifest_sha256": sha(native / "capture_manifest.json"),
                            "database_sha256": sha(database),
                            "bytes": sum(p.stat().st_size for p in native.rglob("*") if p.is_file()),
                            "elapsed_seconds": round(time.monotonic() - started, 2),
                            "device_peak_allocated_bytes": torch.cuda.max_memory_allocated(),
                            "net_disk_bytes": free_before - shutil.disk_usage(output).free}
        except Exception as exc:
            summary[run] = {"status": "FAIL", "role": row["role"], "error": repr(exc)}
            write(summary_path, summary)
            raise
        write(summary_path, summary)
        print(run, json.dumps(summary[run], sort_keys=True), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["histories"])
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--trainer", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--shared-task-e05", action="store_true")
    parser.add_argument("--reuse-anchor", type=Path)
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()
    require(args.shared_task_e05 or not (args.reuse_anchor or args.preflight_only), "E05_OPTION_REQUIRES_SHARED_TASK")
    protocol_path = SHARED_E05_PROTOCOL if args.shared_task_e05 else ROOT / "PROTOCOL.json"
    protocol = read(protocol_path)
    require(len(protocol["runs"]) == 3, "FORMAL_ROSTER_COUNT")
    execute_histories(args, protocol, protocol_path, args.reuse_anchor, args.preflight_only)


if __name__ == "__main__":
    main()
