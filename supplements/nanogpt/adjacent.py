"""Bind the original adjacent-update response/factor runners to fresh observations."""
import argparse
from collections import defaultdict
import gzip
import inspect
from itertools import combinations
import json
from pathlib import Path
import shutil

import numpy as np

from reproduce import captured_protocol, checked_source, e05_input_keys, read, require, sha, write
from e07_provenance import obtain_rows, native_reallocation


def response_windows(windows, roster, allow_missing=False):
    result = []
    for run in roster:
        tag = run["id"]
        pool = [w for w in windows if w["entry_id"] == tag and
                w["scientific_end_optimizer_step"] - w["scientific_start_optimizer_step"] >= 2]
        for category in ("matched_stable", "pre_decline", "recovery"):
            matches = [w for w in pool if category in w["categories"]]
            if not matches and allow_missing:
                continue
            require(matches, f"ADJACENT_REQUIRED_PHASE_MISSING:{tag}:{category}")
            win = min(matches, key=lambda w: (w["scientific_start_optimizer_step"], w["window_id"]))
            step = (win["scientific_start_optimizer_step"] if category == "matched_stable"
                    else win["scientific_end_optimizer_step"] - 2)
            result.append((tag, category, win, step))
    return result


def rebind_counts(function, replacements, constants):
    source = inspect.getsource(function)
    for before, after in replacements:
        require(before in source, "ORIGINAL_COUNT_BINDING_DRIFT:" + before)
        source = source.replace(before, after)
    env = {**function.__globals__, **constants}
    exec(compile(source, function.__code__.co_filename, "exec"), env)
    return env[function.__name__]


def replay_responses(runtime, options, output, previous, anchor):
    old = previous / "ADJACENT_RESPONSE-aligned"
    cached = {r["section_id"]: r for r in read(old / "RESOLVED_INVENTORY.json")["sections"]}
    baseline = read(old / "FINITE_AMPLITUDE_CURVES_MANIFEST.json")
    replay = read(old / "independent-replay" / "FINITE_AMPLITUDE_CURVES_MANIFEST.json")
    verified = read(old / "VALIDATION.json")
    require(baseline == replay and verified["status"] == "PASS"
            and read(old / "INDEPENDENT_REPLAY.json") == {"status": "PASS", "matched_sections": len(cached)},
            "E05_RESPONSE_CACHE_NOT_VERIFIED")
    candidates = {r["section_id"]: r for r in baseline["sections"]}
    graph_inputs = ("receiver_state_path", "native_endpoint_state_path", "transition_path",
                    "receiver_probe_path", "native_endpoint_probe_path")
    copied = []

    def bound_run(source):
        def replay_or_copy(rt, section, target):
            sid = section["section_id"]
            ref = cached.get(sid)
            if (ref and section["entry_id_audit_only"] == ref["entry_id_audit_only"] == anchor
                    and all(section[k] == ref[k] for k in ("pair_id", "observation_id", "evaluation_input_sha256"))
                    and all(sha(Path(section[k])) == sha(Path(ref[k])) for k in graph_inputs)
                    and sha(Path(section["evaluation_input_path"])) == sha(Path(ref["evaluation_input_path"]))):
                actual, meta = source / f"{sid}.npz", source / f"{sid}.json"
                record = read(meta)
                require(record == candidates[sid] and sha(actual) == record["data_file_sha256"],
                        "E05_CACHED_RESPONSE_HASH_MISMATCH:" + sid)
                target.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(actual, target / actual.name)
                shutil.copyfile(meta, target / meta.name)
                if source == old / "sections":
                    copied.append(sid)
                return record
            return rt.run_section(section, target)

        return rebind_counts(runtime.run_all_sections,
                             (("runtime.run_section(section, section_dir)", "replay_or_copy(runtime, section, section_dir)"),),
                             {"replay_or_copy": replay_or_copy})

    first = bound_run(old / "sections")(output_root=output, **options)
    second = bound_run(old / "independent-replay" / "sections")(output_root=output / "independent-replay", **options)
    write(output / "RESPONSE_REUSE.json", {
        "source_validation_sha256": sha(old / "VALIDATION.json"), "anchor_history": anchor,
        "reused_section_ids": sorted(copied), "fresh_section_count": first["section_count"] - len(copied)
    })
    return first, second


def run(args):
    root = args.output.resolve(strict=True)
    protocol = captured_protocol(root)
    shared_task = protocol["targets"] == ["TL-E05"]
    engine, bindings = checked_source(args.source, args.trainer, protocol)
    require(read(root / "RUN_FREEZE.json")["source_sha256"] == bindings, "SOURCE_FREEZE_DRIFT")
    from experiments.gfg_nanogpt_adjacent_response_transport_v1 import analysis, geometry, inventory, runtime, validator
    from experiments.gfg_nanogpt_stepwise_support_transition_v1 import runtime as sst

    stepwise = root / args.stepwise_dir
    alignment_file = args.alignment_lock.resolve(strict=True) if args.alignment_lock else None
    alignment = read(alignment_file) if alignment_file else None
    require(not shared_task or alignment is not None, "SHARED_TASK_E05_REQUIRES_LOCKED_STRATA")
    output = root / ("ADJACENT_RESPONSE-aligned" if alignment else "ADJACENT_RESPONSE")
    if args.e05_only:
        require(alignment and output.is_dir(), "E05_ONLY_REQUIRES_EXISTING_SIX_STRATUM_RESPONSE")
    else:
        output.mkdir(exist_ok=True)
    selected = read(root / "window-inputs" / "v3" / "WINDOWS.json")
    legacy = read(root / "window-inputs" / "STABILITY_FEATURES.json")
    local = {r["entry_id"]: {p["optimizer_step"]: p for p in r["rows"]} for r in legacy["runs"]}
    roster = protocol["runs"] if alignment else [r for r in protocol["runs"] if r["role"] == "development"]
    unseen = ("SHARED_TASK_E05_NO_GLOBAL_HOLDOUT" if shared_task else
              "NO_E05_HOLDOUT_AFTER_PREDICTIONS_SCORED" if alignment else
              next(r["id"] for r in protocol["runs"] if r["role"] == "confirmation"))
    bundles = {r["entry_id"]: r["gfg_bundle_id"] for r in read(root / "SOURCE_INDEX.json")["entries"]}
    registry_path = Path(sst.__file__).with_name("component_registry_csrg_4c_v1.json")
    probes_path = Path(sst.__file__).with_name("probe_contract_csrg_4c_v1.json")
    registry = sst.ComponentRegistry.load(registry_path)
    probes = sst.ProbeContract.load(probes_path, registry)
    contract_sha = sha(args.response_contract.resolve(strict=True))
    pairs, sources = [], {}
    inputs = output / "validation"
    if not args.e05_only:
        inputs.mkdir(exist_ok=True)

    chosen = ([(row["entry_id"], row["stratum"], row["window"], row["optimizer_step"]) for row in alignment["rows"]]
              if alignment else response_windows(selected["windows"], roster))
    for tag, category, closest, t in chosen:
        win = closest["window_id"]
        pair_id = f"{tag}-{category}-{t:05d}"
        sections = []
        for i in range(2):
            ids = []
            for step in (t + i, t + i + 1):
                entry = stepwise / tag
                state = read(inventory._state_path(entry, win, step))["state"]["state_id"]
                obs = read(inventory._probe_path(entry, state))["probe_observation_id"]
                ids.append({"observed_state_id": state, "probe_observation_id": obs})
            section = f"{pair_id}-{i}"
            sections.append({"section_id": section, "observation_id": section, "section_ordinal_within_pair": i,
                             "receiver_optimizer_step_audit_only": t + i, "native_endpoint_optimizer_step_audit_only": t + i + 1,
                             "receiver_prestate": ids[0], "native_endpoint_adjudication_only": ids[1]})
        pairs.append({"pair_id": pair_id, "sections": sections, "window_id": win,
                      "entry_id_audit_only": tag, "primary_stratum": category})
    for run in roster:
        tag = run["id"]
        task = engine.build_formal_task(instance_id=tag, token_seed=run["token_seed"], split_seed=run["split_seed"])
        adapter = sst.StepwiseTrainingRuntime(root / "source_bundles" / bundles[tag], args.trainer, registry, probes)
        try:
            data = np.ascontiguousarray(adapter.base.validation_inputs.numpy())
            require(np.array_equal(data, task.validation_inputs.numpy()), "ADJACENT_VALIDATION_IDENTITY_MISMATCH")
            if shared_task:
                captured = e05_input_keys(data, adapter.base.validation_targets[:, -1].numpy())
                expected = e05_input_keys(data, task.validation_targets[:, -1].numpy())
                digest = inventory.sha256_bytes(json.dumps(captured).encode())
                require(captured == expected and digest == read(root / "E05_ALIGNMENT_PREFLIGHT.json")["ordered_keys_sha256"],
                        "SHARED_TASK_CAPTURED_IDENTITY_MISMATCH:" + tag)
            input_path = inputs / f"{tag}.npy"
            if args.e05_only:
                require(np.array_equal(np.load(input_path, allow_pickle=False), data),
                        "CACHED_VALIDATION_IDENTITY_MISMATCH:" + tag)
            else:
                np.save(input_path, data, allow_pickle=False)
            sources[tag] = {"original_training_gfg": {
                "task_commitment": task.participant_task_commitment,
                "validation_input": {"object_id_at_step_100": local[tag][100]["validation_input_object_id"],
                                     "content_sha256": inventory.sha256_bytes(data.tobytes())}}}
        finally:
            adapter.close()

    n, p, m = len(roster), len(pairs), 2 * len(pairs)
    manifest = {"status": "SELECTION_FROZEN_NO_NEW_CURVES_VIEWED", "entry_sources": sources, "pairs": pairs,
                "development_entry_count": n, "adjacent_pair_count": p, "response_section_count": m,
                "section_id_set_sha256": inventory.sha256_bytes(inventory.canonical_bytes(sorted(
                    section["section_id"] for pair in pairs for section in pair["sections"]))),
                "global_unseen_policy": {"entry_id": unseen}, "parent_window_selection_sha256": sha(root / "window-inputs" / "v3" / "WINDOWS.json"),
                "original_response_contract_sha256": contract_sha,
                "selection_scope": ("All three shared-task histories; observed strata only" if shared_task else
                     "All three histories and six selection strata" if alignment else
                     "Three fixed phase strata per development history; no additional near/far or high support strata claimed."),
                "alignment_lock_sha256": sha(alignment_file) if alignment else None}
    path = output / "SELECTION_MANIFEST.json"
    if path.exists():
        require(read(path) == manifest, "ADJACENT_SELECTION_DRIFT")
    else:
        require(not args.e05_only, "CACHED_ADJACENT_SELECTION_MISSING")
        write(path, manifest)
    counts = {"DEV_COUNT": n, "PAIR_COUNT": p, "SECTION_COUNT": m, "GLOBAL_UNSEEN_ENTRY": unseen}
    validate_edits = (("== 72", "== SECTION_COUNT"), ("== 2544", "== DEV_COUNT * 212"),
                      ('"section_count": 72', '"section_count": SECTION_COUNT'))
    if args.e05_only:
        validate = rebind_counts(validator.validate_package, validate_edits, {**counts, "_write": lambda *_: None})
        require(validate(root=output) == read(output / "VALIDATION.json"), "CACHED_RESPONSE_VALIDATION_DRIFT")
        require(read(output / "INDEPENDENT_REPLAY.json") == {"status": "PASS", "matched_sections": m},
                "CACHED_INDEPENDENT_REPLAY_INCOMPLETE")
        run_e05(args, output, stepwise, root / "TL-E05-native", counts)
        return
    builder = rebind_counts(inventory.build_inventory, (("== 12", "== DEV_COUNT"), ("== 36", "== PAIR_COUNT"),
        ("== 72", "== SECTION_COUNT"), ('"development_entry_count": 12', '"development_entry_count": DEV_COUNT'),
        ('"adjacent_pair_count": 36', '"adjacent_pair_count": PAIR_COUNT'),
        ('"response_section_count": 72', '"response_section_count": SECTION_COUNT'),
        ('"entry_count": 12', '"entry_count": DEV_COUNT'), ('"verified_section_count": 72', '"verified_section_count": SECTION_COUNT')), counts)
    inventory_summary = builder(selection_path=path, raw_root=stepwise, validation_input_root=inputs, output_root=output)
    inventory_path = output / "RESOLVED_INVENTORY.json"
    geometry_path = output / "UPDATE_GEOMETRY_CONTROL_MANIFEST.json"
    section_count = ('"section_count": 72', '"section_count": SECTION_COUNT')
    geometry_fn = rebind_counts(geometry.build_geometry_controls, (("== 72", "== SECTION_COUNT"), section_count,
        ('"all 72 frozen development sections; no response-curve outcomes"', 'f"all {SECTION_COUNT} frozen development sections; no response-curve outcomes"')), counts)
    geometry_fn(inventory_path=inventory_path, output_path=geometry_path)
    replay_options = dict(inventory_path=inventory_path, trainer_root=args.trainer, registry_path=registry_path,
                          probe_contract_path=probes_path)
    if args.reuse_response_anchor:
        anchor = roster[0]["id"]
        hist = read(root / "HISTORIES.json")[anchor]
        old_hist = read(args.reuse_response_anchor / "HISTORIES.json")[anchor]
        require(shared_task and hist.get("reused_verified_capture") and
                all(hist[k] == old_hist[k] for k in ("database_sha256", "capture_manifest_sha256")),
                "E05_RESPONSE_REUSE_REQUIRES_IDENTICAL_ANCHOR_CAPTURE")
        first, second = replay_responses(runtime, replay_options, output, args.reuse_response_anchor, anchor)
    else:
        first = runtime.run_all_sections(output_root=output, **replay_options)
        second = runtime.run_all_sections(output_root=output / "independent-replay", **replay_options)
    require(first == second, "ADJACENT_FINITE_RESPONSE_REPLAY_MISMATCH")
    write(output / "INDEPENDENT_REPLAY.json", {"status": "PASS", "matched_sections": m})
    analysis.adjacent_transport = rebind_counts(analysis.adjacent_transport, (section_count,), counts)
    analysis.local_to_endpoint = rebind_counts(analysis.local_to_endpoint, (section_count,), counts)
    analysis.run_deterministic_analysis(inventory_path=inventory_path, geometry_path=geometry_path, output_root=output)
    validate = rebind_counts(validator.validate_package, validate_edits, counts)
    validate(root=output)
    require(inventory_summary["native_update_identity_exact_section_count"] == m, "NATIVE_UPDATE_INCOMPLETE")

    if not args.e07_without_factors:
        e05 = root / ("TL-E05-native" if alignment else "TL-E05")
        run_e05(args, output, stepwise, e05, counts)
    if not shared_task:
        inv = read(inventory_path)
        for section in inv["sections"]:
            section["section_npz"] = str(output / "sections" / (section["section_id"] + ".npz"))
        observed = obtain_rows(inv, first, manifest, geometry)
        run_e07(root / ("TL-E07-aligned" if alignment else "TL-E07"), observed, counts)


def run_e05(args, output, stepwise, e05, counts):
    from experiments.gfg_nanogpt_response_factor_analysis_v1 import analysis as factors, runner, validator as factor_check

    section_count = ('"section_count": 72', '"section_count": SECTION_COUNT')
    entry_count = ('"entry_count": 12', '"entry_count": DEV_COUNT')
    factor_build = rebind_counts(factors.build_records,
                                (("== 72 * 212", "== SECTION_COUNT * 212"), section_count, entry_count), counts)
    run_edits = [("== 15264", "== SECTION_COUNT * 212"), ("== 36 * 212", "== PAIR_COUNT * 212"), section_count, entry_count]
    factor_run = rebind_counts(runner.run_factor_analysis, run_edits,
                             {**counts, "build_records": factor_build})
    if not (e05 / "MANIFEST.json").exists():
        factor_run(response_root=output, stepwise_root=stepwise, output_root=e05,
                   contract_path=Path(factors.__file__).with_name("FACTOR_ANALYSIS_CONTRACT.md"),
                   original_task_path=args.response_contract, resume_frozen=(e05 / "ANALYSIS_FREEZE.json").exists())
    # The original validator also checks that the old run disclosed an
    # unrelated exposure. This run never accesses that analysis's holdout.
    factor_validator = rebind_counts(factor_check.validate_factor_analysis, (
        ('boundary = read_json(analysis_root / "BOUNDARY_VIOLATION.json")', ''),
        ('require(manifest["global_unseen_entry_accessed"] is True, "MANIFEST_DISCLOSED_UNSEEN_ACCESS_MISSING")',
         'require(manifest["global_unseen_entry_accessed"] is False, "CONFIRMATION_LEAKAGE")'),
        ('require(boundary["strict_unseen_claim_remains_valid"] is False, "BOUNDARY_VIOLATION_NOT_DISCLOSED")', ''),
        ('require(boundary["used_in_factor_analysis"] is False, "BOUNDARY_ENTRY_USED_IN_ANALYSIS")', ''),
        ('checks += 7', 'checks += 5'), ('== 15264', '== SECTION_COUNT * 212'),
        ('== 12 and GLOBAL_UNSEEN_ENTRY', '== DEV_COUNT and GLOBAL_UNSEEN_ENTRY'),
        ('== 7632', '== PAIR_COUNT * 212'),
        ('"status": "PASS_WITH_DISCLOSED_BOUNDARY_VIOLATION"', '"status": "PASS"'),
        ('"global_unseen_entry_accessed": True', '"global_unseen_entry_accessed": False'),
        ),
        {**counts, "REQUIRED_ANALYSIS_FILES": tuple(x for x in factor_check.REQUIRED_ANALYSIS_FILES
             if x not in {"BOUNDARY_VIOLATION.json", "RECOVERY_AUDIT.json"})})
    factor_validator(analysis_root=e05, response_root=output)
    coverage = native_match_coverage(e05, counts)
    if (output.parent / "E05_ALIGNMENT_PREFLIGHT.json").is_file():
        require(coverage["shared_unique_targets_by_all_histories"] == 212, "E05_ANALYSIS_IDENTITY_OVERLAP_FAILURE")
    write(e05 / "NATIVE_MATCH_COVERAGE.json", coverage)


def native_match_coverage(e05, counts):
    ids = defaultdict(set)
    with gzip.open(e05 / "PRETARGET_FACTOR_RECORDS.jsonl.gz", "rt", encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            key = f"{row['row_content_sha256']}:{row['target_group']}"
            require(row["semantic_target_key"] == key, "NON_NATIVE_E05_TARGET_MATCH_KEY")
            ids[row["entry_id"]].add(key)
    require(len(ids) == counts["DEV_COUNT"] and {len(keys) for keys in ids.values()} == {212},
            "E05_NATIVE_IDENTITY_COVERAGE_MISMATCH")
    encoded_rows = {tag: {key.rsplit(":", 1)[0] for key in keys} for tag, keys in ids.items()}
    current = read(e05 / "INCREMENTAL_CONDITIONING_RESULTS.json")["summaries"]["C6"]
    return {"identity": ["row_content_sha256", "target_group"],
            "unique_targets_by_history": {tag: len(keys) for tag, keys in sorted(ids.items())},
            "shared_unique_targets_by_pair": [{"histories": [a, b], "count": len(ids[a] & ids[b]),
                                              "shared_encoded_input_rows": len(encoded_rows[a] & encoded_rows[b])}
                                             for a, b in combinations(sorted(ids), 2)],
            "shared_unique_targets_by_all_histories": len(set.intersection(*ids.values())),
            "full_current_condition": {k: current[k] for k in ("eligible_query_count", "matched_query_count",
                                                                "covered_run_pair_count")}}


def run_e07(e07, observed, counts):
    from experiments.gfg_nanogpt_support_reallocation_audit_v1 import analysis as reallocation, independent as realloc_check, runner as realloc_io

    e07.mkdir(exist_ok=True)
    report = native_reallocation(observed, reallocation)
    for name, key in (("SOURCE_SECTION_LEDGER.jsonl.gz", "source_ledger"), ("SECTION_UPDATE_LEDGER.jsonl.gz", "section_rows"),
                      ("TARGET_SUPPORT_TRANSITION_LEDGER.jsonl.gz", "group_rows")):
        realloc_io.write_rows(e07 / name, report[key])
    scope = Path(reallocation.__file__).with_name("ANALYSIS_SCOPE.md")
    originals = [scope, *(Path(row[key]) for row in report["source_ledger"] for key in ("section_npz", "transition"))]
    write(e07 / "ANALYSIS_MANIFEST.json", {"claim_scope": "EXPLORATORY_POST_HOC_CAUSAL_DESCRIPTION_NOT_ADVANCE_PREDICTION",
          "source_hashes": {str(path.resolve()): sha(path) for path in originals}})
    write(e07 / "SUPPORT_REALLOCATION_RESULTS.json", report["summary"])
    check = rebind_counts(realloc_check.check, (("== 72", "== SECTION_COUNT"), ("== 1656", "== SECTION_COUNT * 23"),
        ('== summary["valid_allocation_transition_count"] == 1636', '== summary["valid_allocation_transition_count"]')), counts)
    checked = check(e07)
    write(e07 / "RESULTS.json", {"summary": report["summary"], "validation": checked})


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    for arg in ("source", "trainer", "output", "response-contract"):
        cli.add_argument("--" + arg, required=True, type=Path)
    cli.add_argument("--stepwise-dir", default="stepwise", choices=["stepwise", "response-stepwise", "aligned-stepwise"])
    cli.add_argument("--alignment-lock", type=Path)
    cli.add_argument("--e05-only", action="store_true", help="Validate existing responses and run only E05.")
    cli.add_argument("--e07-without-factors", action="store_true")
    cli.add_argument("--reuse-response-anchor", type=Path)
    run(cli.parse_args())
