"""Freeze and replay the six TL-E05 strata using all three captured histories."""
import argparse
from pathlib import Path

import numpy as np
import torch

from reproduce import captured_protocol, checked_source, read, require, sha, write
from adjacent import response_windows


def run(args):
    root = args.output.resolve(strict=True)
    protocol = captured_protocol(root)
    shared_task = protocol["targets"] == ["TL-E05"]
    _, bindings = checked_source(args.source, args.trainer, protocol)
    require(read(root / "RUN_FREEZE.json")["source_sha256"] == bindings, "SOURCE_FREEZE_DRIFT")
    from experiments.gfg_nanogpt_autonomous_capability_discovery_v1.common import payload_sha256
    from experiments.gfg_nanogpt_autonomous_capability_discovery_v1.evaluation_capture import capability_transition
    from experiments.gfg_nanogpt_stepwise_support_transition_v1 import execution, phase, phase_validator, runtime, stepwise_gfg, stepwise_gfg_validator
    from experiments.gfg_nanogpt_support_redundancy_v1.builder import decision_outputs
    from experiments.gfg_nanogpt_support_redundancy_v1.runtime import tensor_sha256

    compare_grid = runtime.StepwiseTrainingRuntime.compare_historical_state

    def compare_endpoint(self, state, step):
        parameters, optimizer = self.source_rows(step)
        if all(row["materialized"] for row in (*parameters.values(), *optimizer.values())):
            return compare_grid(self, state, step)
        p = {name: tensor_sha256(state.parameters[name]) == row["content_sha256"] for name, row in parameters.items()}
        o = {}
        for semantic, row in optimizer.items():
            name, slot = semantic.rsplit(".", 1)
            o[semantic] = tensor_sha256(state.optimizer[name][slot]) == row["content_sha256"]
        require(bool(p and o) and all(p.values()) and all(o.values()), f"E05_SHORT_ENDPOINT_NOT_NATIVE_EXACT:{step}")
        return {"historical_stepwise_replay_exact": True, "runtime_deterministic_reexecution": True,
                "parameter_exact_count": len(p), "parameter_object_count": len(p),
                "optimizer_exact_count": len(o), "optimizer_object_count": len(o),
                "parameter_max_abs_error": 0.0, "optimizer_max_abs_error": 0.0,
                "parameter_per_object_exact": p, "optimizer_per_object_exact": o,
                "parameter_per_object_max_abs_error": dict.fromkeys(p, 0.0),
                "optimizer_per_object_max_abs_error": dict.fromkeys(o, 0.0),
                "endpoint_identity_authority": "Per-step native tensor SHA-256; non-grid tensor bytes were not separately materialized",
                "tolerance_repair_used": False}

    runtime.StepwiseTrainingRuntime.compare_historical_state = compare_endpoint

    source = root / "source_bundles"
    out = root / "aligned-stepwise"
    out.mkdir(exist_ok=True)
    predictor = root / "TL-P01-window" / "RESULTS.json"
    if shared_task:
        preflight = root / "E05_ALIGNMENT_PREFLIGHT.json"
        require(read(preflight)["status"] == "PASS", "E05_INPUT_NOT_PREFLIGHTED")
        before_lock = sha(preflight)
    else:
        require(predictor.is_file(), "PREDICTOR_EVALUATION_NOT_LOCKED")
        before_lock = sha(predictor)
    config = Path(execution.__file__).parent
    main_contract = config / "STEPWISE_SUPPORT_TRANSITION_PROTOCOL_V3.json"
    phase_contract = config / "SUPPORT_PHASE_FINITE_DIFFERENCE_PROTOCOL.json"
    reg = config / "component_registry_csrg_4c_v1.json"
    pc = config / "probe_contract_csrg_4c_v1.json"
    registry = runtime.ComponentRegistry.load(reg)
    probes = runtime.ProbeContract.load(pc, registry)
    base = root / "window-inputs" / "v3" / "WINDOWS.json"
    supports = root / "window-inputs" / "CSRG_FEATURES.json"
    bundle_ids = {r["entry_id"]: r["gfg_bundle_id"] for r in read(root / "SOURCE_INDEX.json")["entries"]}
    lock = out / "STRATA_FREEZE.json"
    policy = {"histories": [r["id"] for r in protocol["runs"]],
        "source_selection_sha256": sha(base), "source_csrg_sha256": sha(supports), "p01_already_scored_sha256": before_lock,
        "identity": "Cross-history matching is performed by the original factor runner using encoded row_content_sha256 and native target_group. Window selection does not use target matches.",
        "phase_windows": "Earliest original matched-stable/pre-decline/recovery window by start. Stable: first adjacent pair. Decline or recovery: last adjacent pair inside window.",
        "support_change": "Largest L1 change in normalized four-component mean necessity between adjacent captured checkpoints.",
        "near_far": "Smallest and largest median absolute per-example native margin on the checkpoint grid. Old logits only; no new alpha response is consulted.",
        "exclusion": "Post-formation checkpoints only; distinct within-run windows, 13 or more steps apart to avoid overlapping predecessor observations. Ties by earliest step.",
        "new_training_histories": 0, "phase_source": "Existing frozen native capture"}
    if shared_task:
        del policy["p01_already_scored_sha256"]
        policy["e05_alignment_preflight_sha256"] = before_lock
        policy["phase_availability"] = "Record absent native strata explicitly. Do not extend training, swap in another window category, or replace histories."
        policy["new_training_histories"] = sum(not row.get("reused_verified_capture", False)
                                               for row in read(root / "HISTORIES.json").values())
    policy_file = out / "POLICY.json"
    if policy_file.exists():
        legacy = {**policy, "identity": "Ordered operands and result decoded from frozen task permutations; canonicalize competing arithmetic labels for cross-history matching. Only examples held out in both histories are eligible."}
        require(read(policy_file) in (policy, legacy), "E05_ALIGNMENT_POLICY_DRIFT")
    else:
        write(policy_file, policy)
    if not lock.exists():
        candidates = response_windows(read(base)["windows"], protocol["runs"], allow_missing=shared_task)
        rows = []
        support_rows = {v["entry_id"]: v["rows"] for v in read(supports)["entries"]}
        names = ["csrg_necessity_" + component.replace(".", "_") + "_mean" for component in registry.component_ids]
        for entry in protocol["runs"]:
            tag = entry["id"]
            picks = [(kind, t, None, parent["window_id"]) for e, kind, parent, t in candidates if e == tag]
            formed = capability_transition(read(root / "histories" / tag / "segment_result.json")["metrics"])
            require(formed is not None, "E05_NO_RECORDED_FORMATION:" + tag)

            def eligible(step):
                return formed <= step <= 9900 and all(abs(step - old[1]) >= 13 for old in picks)

            series = sorted(support_rows[tag], key=lambda item: item["optimizer_step"])
            ranks = []
            for previous, current in zip(series, series[1:]):
                t = current["optimizer_step"]
                if t - previous["optimizer_step"] != 100 or not eligible(t):
                    continue
                a, b = [np.asarray([row["features"][k] for k in names], dtype=np.float64) for row in (previous, current)]
                if min(a.sum(), b.sum()) > 0:
                    ranks.append((float(np.sum(np.abs(a / a.sum() - b / b.sum()))), t))
            require(ranks, "NO_AUTHENTIC_SUPPORT_CHANGE_WINDOW:" + tag)
            value, t = max(ranks, key=lambda x: (x[0], -x[1]))
            picks.append(("large_support_change", t, value, None))
            rt = runtime.StepwiseTrainingRuntime(source / bundle_ids[tag], args.trainer, registry, probes)
            try:
                margin_ranks = []
                for t in range(100, 10000, 100):
                    if not eligible(t):
                        continue
                    receiver, _ = rt.load_source_state(t)
                    rt.restore(receiver)
                    rt.model.eval()
                    measured = decision_outputs(rt.base.forward(), rt.base.validation_targets)
                    margin_ranks.append((float(np.median(np.abs(measured["margins"]))), t))
            finally:
                rt.close()
            value, t = min(margin_ranks)
            picks.append(("near_boundary", t, value, None))
            value, t = max((x for x in margin_ranks if eligible(x[1])), key=lambda x: (x[0], -x[1]))
            picks.append(("far_boundary", t, value, None))
            for name, t, value, original in picks:
                start, end = t - 10, t + 2
                anchor = start // 100 * 100
                wid = "e05-window-" + payload_sha256({"entry_id": tag,"stratum": name,"optimizer_step": t,"bundle": bundle_ids[tag]})[:24]
                window = {"categories": [name], "entry_id": tag, "source_bundle_id": bundle_ids[tag], "window_id": wid,
                    "restore_optimizer_step": anchor, "capture_start_optimizer_step": start, "capture_end_optimizer_step": end,
                    "scientific_start_optimizer_step": t, "scientific_end_optimizer_step": end, "start_optimizer_step": t,
                    "end_optimizer_step": end, "lookback_scales": [1, 2, 5, 10], "captured_prehistory_steps": 10,
                    "replay_warmup_transition_count": start - anchor, "training_transition_count": end - start,
                    "scientific_transition_count": end - t, "state_count": end - start + 1}
                rows.append({"entry_id": tag, "stratum": name, "optimizer_step": t, "value": value,
                             "original_phase_window_id": original, "window": window})
            print(tag, [(name, t) for name, t, _, _ in picks], flush=True)
        data = {"policy_sha256": sha(policy_file), "rows": rows, "new_alpha_response_used_in_selection": False}
        if shared_task:
            strata = ("matched_stable", "pre_decline", "recovery", "large_support_change", "near_boundary", "far_boundary")
            data["missing_native_strata"] = {
                tag: [name for name in strata if (tag, name) not in {(r["entry_id"], r["stratum"]) for r in rows}]
                for tag in bundle_ids
            }
        write(lock, data)
    locked = read(lock)
    require(locked["policy_sha256"] == sha(policy_file), "E05_STRATA_SCHEMA_DRIFT")
    if shared_task:
        actual = [(row["entry_id"], row["stratum"]) for row in locked["rows"]]
        require({tag for tag, _ in actual} == set(bundle_ids)
                and len(set(actual)) == len(actual) and len(actual) <= 18, "E05_FROZEN_STRATA_INVALID")
    else:
        require(len(locked["rows"]) == 18, "E05_FROZEN_STRATA_COUNT")
    selection = out / "WINDOWS.json"
    material = {"schema": "nanogpt-three-history-e05-window-selection-v1", "protocol_sha256": sha(main_contract),
                "finite_difference_protocol_sha256": sha(phase_contract), "windows": [row["window"] for row in locked["rows"]]}
    write(selection, {**material, "selection_sha256": payload_sha256(material)})
    common = {"component_registry_path": reg, "probe_contract_path": pc, "selection_path": selection}
    for tag, bid in bundle_ids.items():
        entry = out / tag
        gfg = entry / "stepwise_support_transition_gfg_manifest.json"
        if not (entry / "entry_receipt.json").exists():
            execution.execute_entry_windows(**common, protocol_path=main_contract, entry_id=tag, source_bundle=source / bid,
                                            trainer_root=args.trainer.resolve(), output_root=out)
        phase_kwargs = {**common, "formal_root": out, "phase_protocol_path": phase_contract, "entry_id": tag}
        if not (entry / "PHASE_VALIDATION.json").exists():
            phase.derive_phase_evidence(**phase_kwargs)
            phase_validator.validate_phase_evidence(**phase_kwargs, output_path=entry / "PHASE_VALIDATION.json")
        if not gfg.exists():
            stepwise_gfg.build_entry_stepwise_gfg(**phase_kwargs, protocol_path=main_contract, source_bundle=source / bid)
        db = entry / read(gfg)["database"]
        check = stepwise_gfg_validator.validate_stepwise_gfg(database_path=db, source_database_path=source / bid / "participant_gfg.sqlite3",
            tensor_directory=entry / "tensor-objects", manifest_path=gfg, output_path=entry / "GFG_VALIDATION.json")
        require(check["status"] == "PASS", "E05_ALIGNMENT_STEPWISE_GFG")
    seal = preflight if shared_task else predictor
    require(sha(seal) == before_lock, "E05_WINDOW_PREREQUISITE_CHANGED")
    status = {"status": "PASS", "freeze_sha256": sha(lock), "histories": len(bundle_ids), "windows": len(locked["rows"])}
    if shared_task:
        status["missing_native_strata"] = locked["missing_native_strata"]
    write(out / "STATUS.json", status)


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    for key in ("source", "trainer", "output"):
        cli.add_argument("--" + key, type=Path, required=True)
    run(cli.parse_args())
