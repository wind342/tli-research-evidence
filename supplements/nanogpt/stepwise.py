"""Re-execute the frozen supplementary windows and bind them to original GFG."""
import argparse
from datetime import datetime, timezone
import os
from pathlib import Path

from reproduce import ROOT, checked_source, read, require, sha, write


def run(args):
    root = args.output.resolve(strict=True)
    _, bindings = checked_source(args.source, args.trainer, read(ROOT / "PROTOCOL.json"))
    require(read(root / "RUN_FREEZE.json")["source_sha256"] == bindings, "SOURCE_FREEZE_DRIFT")
    from experiments.gfg_nanogpt_stepwise_support_transition_v1 import execution, phase, phase_validator, stepwise_gfg, stepwise_gfg_validator

    selection = root / "window-inputs" / "v3" / "WINDOWS.json"
    config = Path(execution.__file__).parent
    formal = root / "stepwise"
    formal.mkdir(exist_ok=True)
    chosen = read(selection)
    common = dict(selection_path=selection, protocol_path=config / "STEPWISE_SUPPORT_TRANSITION_PROTOCOL_V3.json",
                  component_registry_path=config / "component_registry_csrg_4c_v1.json",
                  probe_contract_path=config / "probe_contract_csrg_4c_v1.json")
    if args.fork_only or args.response_only:
        from experiments.gfg_nanogpt_autonomous_capability_discovery_v1.common import payload_sha256
        if args.fork_only:
            from long_paths import resolve_pair
            pair = resolve_pair(root)
            require(pair is not None, "NO_DEVELOPMENT_MATCHED_PAIR_WITH_100_STEP_FOLLOWUP")
            windows = {w["window_id"] for w in pair[1:]}
            tag = "fork"
        else:
            from adjacent import response_windows
            development = [r for r in read(ROOT / "PROTOCOL.json")["runs"] if r["role"] == "development"]
            windows = {w["window_id"] for _, _, w, _ in response_windows(chosen["windows"], development)}
            tag = "response"
        subset = {k: v for k, v in chosen.items() if k not in {"selection_sha256", "windows"}}
        subset["windows"] = [w for w in chosen["windows"] if w["window_id"] in windows]
        subset["parent_full_selection_sha256"] = chosen["selection_sha256"]
        chosen = {**subset, "selection_sha256": payload_sha256(subset)}
        selection = root / "window-inputs" / "v3" / f"{tag.upper()}_DEPENDENCIES.json"
        write(selection, chosen)
        common["selection_path"] = selection
        natural = formal
        formal = root / f"{tag}-stepwise"
        formal.mkdir(exist_ok=True)
        for w in chosen["windows"]:
            entry, key = w["entry_id"], w["window_id"]
            parent = natural / entry
            fresh = formal / entry
            if not (parent / "windows" / key / "window_receipt.json").is_file():
                continue
            for part in (Path("windows") / key, Path("tensor-objects"), Path("probe-observations")):
                for path in (parent / part).rglob("*"):
                    if path.is_file() and not path.name.endswith(".pending"):
                        target = fresh / path.relative_to(parent)
                        if not target.exists():
                            target.parent.mkdir(parents=True, exist_ok=True)
                            os.link(path, target)
    rows = []
    for row in read(root / "SOURCE_INDEX.json")["entries"]:
        tag = row["entry_id"]
        if not any(w["entry_id"] == tag for w in chosen["windows"]):
            continue
        bundle = root / "source_bundles" / row["gfg_bundle_id"]
        entry = formal / tag
        manifest = entry / "stepwise_support_transition_gfg_manifest.json"
        if not (entry / "entry_receipt.json").exists():
            execution.execute_entry_windows(entry_id=tag, source_bundle=bundle, trainer_root=args.trainer,
                                            output_root=formal, **common)
        phase_contract = config / "SUPPORT_PHASE_FINITE_DIFFERENCE_PROTOCOL.json"
        phase_args = {k: common[k] for k in ("selection_path", "component_registry_path", "probe_contract_path")}
        phase_args.update(formal_root=formal, phase_protocol_path=phase_contract, entry_id=tag)
        phase_file = entry / "PHASE_VALIDATION.json"
        if not phase_file.exists():
            phase.derive_phase_evidence(**phase_args)
            phase_validator.validate_phase_evidence(**phase_args, output_path=phase_file)
        require(read(phase_file)["status"] == "PASS", "STEPWISE_PHASE_VALIDATION_FAILED:" + tag)
        if not manifest.exists():
            # Retain failed graph attempts, not validated data or raw captures.
            incomplete = [entry / ("stepwise_support_transition_gfg.sqlite3" + suffix) for suffix in ("", "-wal", "-shm")]
            if any(p.exists() for p in incomplete):
                failed = entry / "failed-graph-attempts" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
                failed.mkdir(parents=True, exist_ok=False)
                for p in incomplete:
                    if p.exists():
                        p.rename(failed / p.name)
            stepwise_gfg.build_entry_stepwise_gfg(entry_id=tag, source_bundle=bundle, formal_root=formal,
                phase_protocol_path=phase_contract, **common)
        graph = read(manifest)
        report = stepwise_gfg_validator.validate_stepwise_gfg(
            database_path=entry / graph["database"], source_database_path=bundle / "participant_gfg.sqlite3",
            tensor_directory=entry / "tensor-objects", manifest_path=manifest,
            output_path=entry / "STEPWISE_GFG_VALIDATION.json")
        require(report["status"] == "PASS", "STEPWISE_GFG_VALIDATION_FAILED:" + tag)
        rows.append({"entry_id": tag, "manifest_sha256": sha(manifest), "status": "PASS"})
    require(rows, "MISSING_EXECUTABLE_STEPWISE_WINDOWS")
    write(formal / "STATUS.json", {"status": "PASS", "entries": rows, "selection_sha256": sha(selection)})


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    for arg in ("source", "trainer", "output"):
        cli.add_argument("--" + arg, required=True, type=Path)
    paths = cli.add_mutually_exclusive_group()
    paths.add_argument("--fork-only", action="store_true")
    paths.add_argument("--response-only", action="store_true")
    run(cli.parse_args())
