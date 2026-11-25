"""Run original feature extraction and window selection on the new roster."""
import argparse
import importlib.util
import inspect
from pathlib import Path
import sys

from reproduce import ROOT, captured_protocol, checked_source, read, require, sha, write


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "MISSING_ORIGINAL_HELPER")
    obj = importlib.util.module_from_spec(spec)
    sys.modules[name] = obj
    spec.loader.exec_module(obj)
    return obj


def roster_selector(original, allow_missing_phases=False):
    # Replace the four source-population counts, not the matching features,
    # distance, timing, ordering, or decline/recovery definitions.
    edits = (
        ('len(source_bundles) == 13', 'len(source_bundles) == roster_count'),
        ('require(len(stable_candidates) >= 72, "SST_STABLE_CANDIDATE_POOL_TOO_SMALL")', ''),
        ('require(len(decline_events) == 72, f"SST_LEGAL_DECLINE_COUNT_INVALID:{len(decline_events)}")',
         ('require(len(stable_candidates) >= len(decline_events), "SST_STABLE_CANDIDATE_POOL_TOO_SMALL")'
          if allow_missing_phases else
          'require(bool(decline_events) and len(stable_candidates) >= len(decline_events), "SST_STABLE_CANDIDATE_POOL_TOO_SMALL_OR_NO_DECLINES")')),
        ('row["categories"] for row in windows) == 72', 'row["categories"] for row in windows) == len(decline_events)'),
        ('row["categories"] for row in windows) == 13',
         'row["categories"] for row in windows) == ' + ('len(recovery_rows)' if allow_missing_phases else 'roster_count')),
    )
    if allow_missing_phases:
        edits += (
            ('require(bool(complete), f"SST_RECOVERY_WINDOW_MISSING:{entry_id}")', 'if not complete: continue'),
            ('require(bool(candidates), f"SST_REPLAY_PAIR_MISSING:{entry_id}")', 'if not candidates: continue'),
            ('max(use_counts.values())', 'max(use_counts.values(), default=0)'),
        )
    text = inspect.getsource(original)
    for before, after in edits:
        require(text.count(before) == 1, "ORIGINAL_SELECTOR_ADAPTER_DRIFT:" + before)
        text = text.replace(before, after)
    env = dict(original.__globals__)
    env["roster_count"] = 3
    exec(compile(text, original.__code__.co_filename, "exec"), env)
    return env[original.__name__]


def bind_legacy_payload_root(features):
    original = features.EvidenceTensors

    class LocalEvidenceTensors(original):
        def __init__(self, client, entry_id):
            super().__init__(client, entry_id)
            require(client.gfg_root is not None, "SUPPLEMENT_GFG_ROOT_REQUIRED")
            self.root = client.gfg_root / client.runs[entry_id]["gfg_bundle_id"] / "tensor-objects"

    features.EvidenceTensors = LocalEvidenceTensors


def run(args):
    root = args.output.resolve(strict=True)
    protocol = captured_protocol(root)
    checked_source(args.source, args.trainer, protocol)
    from experiments.gfg_nanogpt_stepwise_support_transition_v1 import batch_availability, execution, selection as original

    local = root / "window-inputs"
    local.mkdir(exist_ok=True)
    participants = root / "source_bundles"
    index = read(root / "SOURCE_INDEX.json")
    require(len(index["entries"]) == 3, "ROSTER_INPUT_COUNT")
    support = root / "TL-E06"
    require(read(support / "INDEPENDENT_REPLAY.json")["status"] == "PASS", "CSRG_REPLAY_NOT_VALIDATED")
    client_path = args.cumulative_client.resolve(strict=True)
    feature_path = args.legacy_features.resolve(strict=True)
    csrg_path = args.csrg_features.resolve(strict=True)
    sys.path[:0] = [str(feature_path.parent), str(csrg_path.parent)]
    client = module(client_path, "cumulative_gfg")
    features = module(feature_path, "feature_extraction")
    bind_legacy_payload_root(features)
    csrg_features = module(csrg_path, "tlir_original_csrg_analysis")
    write(local / "HELPER_IDENTITIES.json", {
        path.name: sha(path) for path in (client_path, feature_path, csrg_path, Path(original.__file__))
    })
    manifest = local / "CUMULATIVE_SOURCE.json"
    write(manifest, {"runs": [dict(x, candidate_sealed=False) for x in index["entries"]]})
    legacy = local / "STABILITY_FEATURES.json"
    with client.CumulativeGFG(ROOT, manifest_path=manifest, gfg_root=participants) as gfg:
        rows = []
        for entry in index["entries"]:
            row = features.extract_run(gfg, entry["entry_id"])
            rows.append(row)
            print(entry["entry_id"], "original legacy features", len(row["rows"]), flush=True)
    write(legacy, {"schema": "cumulative-gfg-prefix-feature-cache-v1", "runs": rows})
    _, index_value, receipt = csrg_features.extract_support_evidence(support, legacy)
    csrg_index = local / "CSRG_FEATURES.json"
    write(csrg_index, index_value)
    write(local / "CSRG_EXTRACTION.json", receipt)
    original_dir = Path(original.__file__).parent
    registry = original_dir / "component_registry_csrg_4c_v1.json"
    probes = original_dir / "probe_contract_csrg_4c_v1.json"
    v1, v2 = (local / s for s in ("base", "phase"))
    v1.mkdir(exist_ok=True)
    v2.mkdir(exist_ok=True)
    roster_selector(original.freeze_stepwise_selection, allow_missing_phases=protocol["targets"] == ["TL-E05"])(
        stability_feature_cache=legacy, csrg_feature_index=csrg_index,
        source_archive_manifest=support / "archive_manifest.json",
        protocol_path=original_dir / "STEPWISE_SUPPORT_TRANSITION_PROTOCOL.json",
        component_registry_path=registry, probe_contract_path=probes,
        window_output=v1 / "WINDOWS.json", pairing_output=v1 / "PAIRS.json",
        budget_output=v1 / "BUDGET.json",
    )
    windows, _, budget = original.freeze_phase_selection(
        parent_window_selection_path=v1 / "WINDOWS.json", parent_pairing_path=v1 / "PAIRS.json",
        protocol_path=original_dir / "STEPWISE_SUPPORT_TRANSITION_PROTOCOL_V2.json",
        finite_difference_protocol_path=original_dir / "SUPPORT_PHASE_FINITE_DIFFERENCE_PROTOCOL.json",
        component_registry_path=registry, probe_contract_path=probes,
        window_output=v2 / "WINDOWS.json", pairing_output=v2 / "PAIRS.json",
        budget_output=v2 / "BUDGET.json",
    )
    print("Frozen", len(windows["windows"]), "windows with",
          budget["captured_training_transition_count"], "captured transitions", flush=True)
    v3 = local / "v3"
    v3.mkdir(exist_ok=True)
    frozen_v3 = original_dir / "STEPWISE_SUPPORT_TRANSITION_PROTOCOL_V3.json"
    selection_path = v3 / "WINDOWS.json"
    result, _, _ = original.rebind_phase_selection_protocol(
        parent_window_selection_path=v2 / "WINDOWS.json", parent_pairing_path=v2 / "PAIRS.json",
        parent_budget_path=v2 / "BUDGET.json", protocol_path=frozen_v3,
        window_output=selection_path, pairing_output=v3 / "PAIRS.json", budget_output=v3 / "BUDGET.json",
    )
    batch_availability.audit_batch_identity_availability(
        source_root=participants, source_archive_manifest_path=support / "archive_manifest.json",
        selection_path=selection_path, output_path=v3 / "BATCH_AVAILABILITY.json")
    if args.execute:
        for row in index["entries"]:
            if any(w["entry_id"] == row["entry_id"] for w in result["windows"]):
                execution.execute_entry_windows(
                    entry_id=row["entry_id"], source_bundle=participants / row["gfg_bundle_id"],
                    trainer_root=args.trainer.resolve(), output_root=root / "stepwise",
                    protocol_path=frozen_v3, selection_path=selection_path,
                    component_registry_path=registry, probe_contract_path=probes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("source", "trainer", "output", "cumulative-client", "legacy-features", "csrg-features"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--execute", action="store_true")
    run(parser.parse_args())
