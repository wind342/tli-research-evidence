"""Reuse the original CSRG and inference kernels against this run's own states."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

from reproduce import ROOT, captured_protocol, checked_source, read, require, sha, write


def bind_core_checkout(source, core_checkout, root):
    # The frozen Core inspects its tracked blobs. The source ZIP has the
    # original bytes but no Git metadata, so use the matching Core checkout.
    checkout = core_checkout.resolve(strict=True)
    sys.path.insert(0, str(checkout))
    sys.path.insert(0, str(checkout / "src"))
    from generation_relation_core.implementation_identity import IMPLEMENTATION_FILES, build_implementation_content_identity

    observed = {}
    for relative, _ in IMPLEMENTATION_FILES:
        expected = sha(source / relative)
        require(sha(checkout / relative) == expected, "CORE_SOURCE_BYTES_DIFFER:" + relative)
        observed[relative] = expected
    value = {
        "git_commit": subprocess.check_output(["git", "-C", str(checkout), "rev-parse", "HEAD"],
                                               text=True).strip(),
        "implementation_identity": build_implementation_content_identity(checkout),
        "matching_source_sha256": observed,
    }
    path = root / "CORE_SOURCE.json"
    if path.exists():
        require(read(path) == value, "CORE_SOURCE_FREEZE_DRIFT")
    else:
        write(path, value)


def prepare_bundles(root, protocol):
    from experiments.gfg_nanogpt_autonomous_capability_discovery_v1.common import payload_sha256
    from experiments.gfg_nanogpt_autonomous_capability_discovery_v1.core_validation import validate_core_representatives
    from experiments.gfg_nanogpt_autonomous_capability_discovery_v1.participant_evidence import build_participant_evidence_bundle

    rows = []
    histories = read(root / "HISTORIES.json")
    participants = root / "source_bundles"
    participants.mkdir(exist_ok=True)
    for row in protocol["runs"]:
        run = row["id"]
        require(histories[run]["status"] == "PASS", "SOURCE_CAPTURE_NOT_COMPLETE:" + run)
        native = root / "histories" / run
        database = native / "participant_gfg.sqlite3"
        capture = native / "capture_manifest.json"
        require(sha(database) == histories[run]["database_sha256"], "CAPTURE_DATABASE_CHANGED")
        require(sha(capture) == histories[run]["capture_manifest_sha256"], "CAPTURE_MANIFEST_CHANGED")
        core_report = native / "core_representative_validation.json"
        if not core_report.exists():
            write(core_report, validate_core_representatives(database))
        require(read(core_report)["status"] == "PASS", "CORE_REPRESENTATIVE_VALIDATION_FAILED:" + run)
        content_id = payload_sha256({
            "capture_manifest_sha256": sha(capture), "database_sha256": sha(database),
            "run": run,
        })
        bundle = participants / content_id
        if not bundle.exists():
            build_participant_evidence_bundle(captured_directory=native, bundle_directory=bundle)
        bundle_manifest = read(bundle / "manifest.json")
        require(bundle_manifest["gfg_database_sha256"] == sha(database)
                and bundle_manifest["capture_manifest_sha256"] == sha(capture),
                "PARTICIPANT_BUNDLE_CHANGED:" + run)
        rows.append({"entry_id": run, "gfg_bundle_id": content_id, "role": row["role"],
                     "manifest_sha256": sha(bundle / "manifest.json")})
    index = root / "SOURCE_INDEX.json"
    value = {"protocol_sha256": sha(root / "PROTOCOL.json"), "entries": rows}
    if index.exists():
        require(read(index) == value, "SOURCE_INDEX_DRIFT")
    else:
        write(index, value)
    return participants, index


def csrg(root, participants, index, trainer):
    from experiments.gfg_nanogpt_support_redundancy_v1 import build_archive, verify_archive

    output = root / "TL-E06"
    contract = Path(build_archive.__file__).parent / "capture_contract_v2.json"
    build_archive.build_archive(archive_index=index, source_gfg_root=participants, output_root=output,
                                trainer_root=trainer, contract_path=contract)
    return verify_archive.verify_archive(output, participants, trainer,
                                         output_path=output / "INDEPENDENT_REPLAY.json")


def inference(root, participants, index, trainer):
    from experiments.gfg_nanogpt_training_learning_inference_projection_v1 import analysis, gfg, independent, runner, runtime

    output = root / "INF-E01"
    output.mkdir(exist_ok=False)
    graph = output / "gfg"
    graph.mkdir()
    contract_hash = sha(Path(runtime.__file__).parent / "PROTOCOL_FREEZE.md")
    rows = read(index)["entries"]
    chosen, not_measured = {}, {}
    for entry in rows:
        run = entry["entry_id"]
        curve = runtime.validated_accuracy_curve(root / "TL-E06" / entry["gfg_bundle_id"])
        if not any(row["validation_accuracy"] >= 0.90 for row in curve):
            not_measured[run] = "NO_FORMED_CHECKPOINT"
            continue
        try:
            chosen[run] = runtime.select_phases(curve)
        except RuntimeError as exc:
            if str(exc) not in {"TLI_NO_PREFORMATION_CHECKPOINT", "TLI_NO_POSTFORMATION_DECLINE"}:
                raise
            not_measured[run] = str(exc)
    write(output / "PHASE_FREEZE.json", {"original_protocol_sha256": contract_hash,
                                       "source_index_sha256": sha(index), "selected": chosen,
                                       "not_measured": not_measured})
    ledgers, replays, validations = [], [], []
    for entry in rows:
        run, bundle = entry["entry_id"], entry["gfg_bundle_id"]
        if run not in chosen:
            continue
        kwargs = dict(entry_id=run, source_bundle_id=bundle, source_bundle=participants / bundle,
                      trainer_root=trainer, phase_selection=chosen[run])
        record = runtime.execute_run(**kwargs)
        ledger, arrays = analysis.analyse_run(record)
        gfg.write_run_gfg(record=record, ledger=ledger, phase_arrays=arrays, graph_root=graph,
                          protocol_sha256=contract_hash)
        validations.append(gfg.validate_run_gfg(graph / run))
        replay, _ = analysis.analyse_run(runtime.execute_run(**kwargs))
        replays.append({"entry_id": run, "checks": independent._compare_entry(ledger, replay)})
        ledgers.append(ledger)
        print(run, "INF-E01 native execution and replay matched", flush=True)
    if ledgers:
        gfg.aggregate_manifest(graph, ledgers)
        runner.write_rows(output / "OBSERVATION_LEDGER.jsonl.gz", ledgers)
        summary = analysis.summarize(ledgers)
        # The original result formatter hard-codes its 13-run wording.
        summary["interpretation"] = (
            "Original frozen gate functions evaluated on the measured subset "
            "of the three-history supplementary roster."
        )
    else:
        summary = {"status": "NOT_EVALUABLE", "run_count": 0}
    outcome = {"scientific": summary, "planned_run_count": len(rows), "not_measured": not_measured,
               "replay_checks": replays, "gfg_checks": validations}
    write(output / "RESULTS.json", outcome)
    return outcome


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["support", "inference", "support-and-inference"])
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--core-source", type=Path, default=ROOT.parent / "gfg-core-structural-experiments")
    parser.add_argument("--trainer", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.output.resolve(strict=True)
    protocol = captured_protocol(root)
    require(protocol["targets"] != ["TL-E05"] or args.stage == "support", "SHARED_TASK_RUN_IS_E05_ONLY")
    bind_core_checkout(args.source.resolve(strict=True), args.core_source, root)
    _, bindings = checked_source(args.source, args.trainer, protocol)
    require(read(root / "RUN_FREEZE.json")["source_sha256"] == bindings, "SOURCE_FREEZE_DRIFT")
    participants, index = prepare_bundles(root, protocol)
    trainer = args.trainer.resolve()
    if args.stage in ("support", "support-and-inference"):
        print(json.dumps(csrg(root, participants, index, trainer), sort_keys=True), flush=True)
    if args.stage in ("inference", "support-and-inference"):
        print(json.dumps(inference(root, participants, index, trainer), sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
