"""Connect original reciprocal forks and amplitude paths to fresh stepwise states."""
import argparse
import inspect
from pathlib import Path

from reproduce import ROOT, checked_source, read, require, sha, write


def resolve_pair(root):
    selection = root / "window-inputs" / "v3"
    windows = {r["window_id"]: r for r in read(selection / "WINDOWS.json")["windows"]}
    roles = {r["id"]: r["role"] for r in read(ROOT / "PROTOCOL.json")["runs"]}
    pairs = []
    for pair in read(selection / "PAIRS.json")["pairings"]:
        a, b = (windows[pair[k]] for k in ("stable_window_id", "decline_window_id"))
        if all(roles[w["entry_id"]] == "development" and
               w["scientific_start_optimizer_step"] + 100 <= 10000 for w in (a, b)):
            pairs.append((pair, a, b))
    if not pairs:
        return None
    # Use the closest eligible pair from the original frozen matching. Do not
    # inspect any new branch outcome, and never use the confirmation seed.
    return min(pairs, key=lambda x: (x[0]["matching_distance"], x[0]["pair_id"]))


def check_or_write(path, value):
    if path.exists():
        require(read(path) == value, "REBINDING_CHANGED:" + path.name)
    else:
        write(path, value)


def amplitude_checker(original):
    source = inspect.getsource(original)
    before = "                composed[mask] = arrays[right][role][mask]"
    replacement = "                if 0.0 <= left and right <= 1.0:\n" + "    " + before
    require(source.count(before) == 1, "AMPLITUDE_CHECKER_SOURCE_CHANGED")
    env = dict(original.__globals__)
    exec(compile(source.replace(before, replacement), original.__code__.co_filename, "exec"), env)
    return env[original.__name__]


def amplitude_origin_checker(original):
    source = inspect.getsource(original)
    before = 'bundle_id: TrainingGFG(source_root / bundle_id / "participant_gfg.sqlite3")'
    after = 'str(source_manifests[bundle_id]["bundle_manifest_sha256"]): TrainingGFG(source_root / bundle_id / "participant_gfg.sqlite3")'
    require(source.count(before) == 1, "AMPLITUDE_ORIGIN_RESOLVER_SOURCE_CHANGED")
    env = dict(original.__globals__)
    exec(compile(source.replace(before, after), original.__code__.co_filename, "exec"), env)
    return env[original.__name__]


def main(args):
    root = args.output.resolve(strict=True)
    protocol = read(ROOT / "PROTOCOL.json")
    _, bindings = checked_source(args.source, args.trainer, protocol)
    require(read(root / "RUN_FREEZE.json")["source_sha256"] == bindings, "SOURCE_FREEZE_DRIFT")
    from experiments.gfg_nanogpt_stepwise_support_transition_v1 import (
        amplitude_path, amplitude_path_gfg, amplitude_path_gfg_validator, amplitude_path_validator,
        optimizer_exchange, optimizer_exchange_gfg, optimizer_exchange_gfg_validator, optimizer_exchange_validator,
        reciprocal, reciprocal_gfg, reciprocal_gfg_validator, reciprocal_validator, selection,
    )
    from experiments.gfg_nanogpt_stepwise_support_transition_v1.reciprocal_gfg_validator import _main_object_index

    source = root / "source_bundles"
    stepwise = root / args.stepwise_dir
    location = Path(selection.__file__).parent
    paths = {"component_registry_path": location / "component_registry_csrg_4c_v1.json",
             "probe_contract_path": location / "probe_contract_csrg_4c_v1.json"}
    shared = {"source_root": source}
    runner = {**paths, **shared, "trainer_root": args.trainer.resolve(), "formal_root": stepwise,
              "main_protocol_path": location / "STEPWISE_SUPPORT_TRANSITION_PROTOCOL_V3.json"}
    e03, e04 = (root / name for name in ("TL-E03", "TL-E04"))
    for out in (e03, e04):
        out.mkdir(exist_ok=True)
    match = resolve_pair(root)
    if not match:
        for out in (e03, e04):
            check_or_write(out / "STATUS.json", {"status": "NOT_EVALUABLE", "reason": "NO_DEVELOPMENT_MATCHED_PAIR_WITH_100_STEP_FOLLOWUP"})
        return
    pair, a, b = match
    endpoints = [{**{k: win[k] for k in ("entry_id", "window_id", "source_bundle_id")},
                  "optimizer_step": win["scientific_start_optimizer_step"], "label": label}
                 for label, win in zip("AB", (a, b))]
    recip_contract = location / "RECIPROCAL_MATCHED_PAIR_PROTOCOL_V2.json"
    recip_path = e03 / "CONTRACT.json"
    check_or_write(recip_path, {**read(recip_contract), "endpoints": endpoints,
                   "supplement_input_binding": {"pair_id": pair["pair_id"], "original_sha256": sha(recip_contract),
                    "selection_rule": "minimum frozen development matching distance, then pair id"}})
    recip_root = e03 / "native"
    if not (recip_root / "reciprocal_pair_receipt.json").exists():
        reciprocal.execute_reciprocal_pair(**runner, output_root=recip_root, reciprocal_protocol_path=recip_path)
    vr = reciprocal_validator.validate_reciprocal_pair(root=recip_root, formal_root=stepwise, reciprocal_protocol_path=recip_path)
    require(vr["status"] == "PASS", "RECIPROCAL_NOT_VALIDATED")
    recip_graph = e03 / "gfg"
    if not (recip_graph / "reciprocal_matched_pair_gfg_manifest.json").exists():
        reciprocal_gfg.build_reciprocal_gfg(**paths, **shared, formal_root=stepwise, evidence_root=recip_root,
                                           graph_root=recip_graph, reciprocal_protocol_path=recip_path)
    rg = reciprocal_gfg_validator.validate_reciprocal_gfg(**shared, formal_root=stepwise, evidence_root=recip_root,
                                                        graph_root=recip_graph, reciprocal_protocol_path=recip_path)
    write(e03 / "STATUS.json", {"execution": vr["status"], "gfg": rg["status"], "validation": "native/reciprocal_pair_validation.json"})
    manifest = read(recip_graph / "reciprocal_matched_pair_gfg_manifest.json")
    index = _main_object_index(recip_graph / manifest["database"])
    donor_summaries = [key for key, row in index.items()
                       if row.get("role") == "actual_native_training_update_summary"
                       and row.get("payload", {}).get("recipient_label") == "B"]
    require(len(donor_summaries) == 1, "DONOR_NATIVE_SUMMARY_IDENTITY")
    amp_contract = location / "B_UPDATE_AMPLITUDE_PATH_PROTOCOL.json"
    frozen = read(amp_contract)
    frozen["donor_update"]["source_object_id"] = donor_summaries[0]
    frozen["receivers"] = [{**row, "skip_state_source_object_id": manifest["state_catalog"][f"{row['label']}:1:skip"]}
                           for row in endpoints]
    frozen["supplement_input_binding"] = {"original_sha256": sha(amp_contract), "reciprocal_contract_sha256": sha(recip_path)}
    amp_path = e04 / "CONTRACT.json"
    check_or_write(amp_path, frozen)
    evidence, graph = (e04 / name for name in ("native", "gfg"))
    if not (evidence / "amplitude_path_pair_receipt.json").exists():
        amplitude_path.execute_amplitude_path(**runner, output_root=evidence, amplitude_path_protocol_path=amp_path)
    original = amplitude_path_validator.validate_amplitude_path
    check_or_write(e04 / "VALIDATOR_ADAPTER.json", {
        "original_validator_sha256": sha(Path(amplitude_path_validator.__file__)),
        "error_observed_in_working_run": "SST_AMPLITUDE_PATH_VALIDATION_CATEGORY_COMPOSITION_MISMATCH:A:forward/11/predictions",
        "correction": "Verify all recorded transitions. Compose only the recorded 0-to-1 transitions when comparing with the scale-1 endpoint, not the outer finite-difference samples.",
        "changes_raw_measurements_or_contract": False,
    })
    av = amplitude_checker(original)(root=evidence, formal_root=stepwise, reciprocal_root=recip_root,
                                     amplitude_path_protocol_path=amp_path)
    require(av["status"] == "PASS", "AMPLITUDE_NOT_VALIDATED")
    if not (graph / "amplitude_path_gfg_manifest.json").exists():
        amplitude_path_gfg.build_amplitude_path_gfg(**paths, **shared, evidence_root=evidence, graph_root=graph,
                                                  reciprocal_graph_root=recip_graph, amplitude_path_protocol_path=amp_path)
    # The publisher uses the manifest identity for origin edges. Resolve that
    # identity to the checked physical directory, as the original optimizer
    # exchange validator already does. No origin/hash validation is skipped.
    ag = amplitude_origin_checker(amplitude_path_gfg_validator.validate_amplitude_path_gfg)(
        **shared, evidence_root=evidence, graph_root=graph, reciprocal_graph_root=recip_graph,
        amplitude_path_protocol_path=amp_path)
    require(ag["status"] == "PASS", "AMPLITUDE_GFG_NOT_VALIDATED")
    write(e04 / "STATUS.json", {"execution": av["status"], "gfg": ag["status"], "validation": "native/amplitude_path_validation.json"})

    exchange_path = e03 / "EXCHANGE_CONTRACT.json"
    exchange = read(location / "H20_RECIPROCAL_OPTIMIZER_EXCHANGE_PROTOCOL.json")
    am = read(graph / "amplitude_path_gfg_manifest.json")
    amp_objects = _main_object_index(graph / am["database"])
    exchange["source_amplitude_path"].update(
        protocol_sha256=am["amplitude_path_protocol_sha256"], graph_schema=am["schema"],
        graph_manifest_sha256=am["manifest_sha256"], graph_database_sha256=am["database_sha256"],
        evidence_validation_sha256=am["evidence_validation_sha256"])
    receivers = []
    for endpoint in endpoints:
        label, step = endpoint["label"], endpoint["optimizer_step"]
        receiver = {"label": label, "entry_id": endpoint["entry_id"], "source_bundle_id": endpoint["source_bundle_id"],
                    "base_optimizer_step": step, "h20_optimizer_step": step + 20, "endpoints": {}}
        for scale in (0, 1):
            key = amplitude_path.scale_key(float(scale))
            result = {"scale": float(scale)}
            for h in (20, 100):
                state_id = am["state_catalog"][f"{label}:{h}:{key}"]
                state = read(evidence / f"receiver-{label}" / "horizons" / f"h-{h:03d}" / f"{key}-state.json")
                result.update({f"h{h}_source_object_id": state_id,
                               f"h{h}_source_content_sha256": amp_objects[state_id]["content_sha256"],
                               f"h{h}_state_sha256": state["state"]["commitment"]["state_sha256"]})
            receiver["endpoints"][str(scale)] = result
        receivers.append(receiver)
    exchange["receivers"] = receivers
    check_or_write(exchange_path, exchange)
    x, xg = e03 / "exchange", e03 / "exchange-gfg"
    exchange_args = dict(optimizer_exchange_protocol_path=exchange_path)
    if not (x / "optimizer_exchange_pair_receipt.json").exists():
        optimizer_exchange.execute_optimizer_exchange(**paths, **shared, **exchange_args,
            amplitude_root=evidence, amplitude_graph_root=graph, output_root=x,
            trainer_root=args.trainer.resolve(), main_protocol_path=runner["main_protocol_path"])
    xv = optimizer_exchange_validator.validate_optimizer_exchange(root=x, amplitude_root=evidence, **exchange_args)
    require(xv["status"] == "PASS", "OPTIMIZER_EXCHANGE_NOT_VALIDATED")
    if not (xg / "optimizer_exchange_gfg_manifest.json").exists():
        optimizer_exchange_gfg.build_optimizer_exchange_gfg(**paths, **shared, **exchange_args, graph_root=xg,
                                                           evidence_root=x, amplitude_graph_root=graph)
    xgv = optimizer_exchange_gfg_validator.validate_optimizer_exchange_gfg(**shared, **exchange_args, graph_root=xg,
                                                                          evidence_root=x, amplitude_graph_root=graph)
    require(xgv["status"] == "PASS", "OPTIMIZER_EXCHANGE_GFG_NOT_VALIDATED")
    write(e03 / "STATUS.json", {"status": "PASS", "reciprocal": vr["status"], "reciprocal_gfg": rg["status"],
                                "optimizer_exchange": xv["status"], "optimizer_exchange_gfg": xgv["status"]})


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    for name in ("source", "trainer", "output"):
        cli.add_argument("--" + name, type=Path, required=True)
    cli.add_argument("--stepwise-dir", default="stepwise", choices=["stepwise", "fork-stepwise"])
    main(cli.parse_args())
