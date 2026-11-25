"""Check the original full-network JVP contract and export true pre/post margins."""
import argparse
from pathlib import Path
import sys

import numpy as np
import torch
from torch.func import functional_call, jvp
from torch.nn.attention import SDPBackend, sdpa_kernel

from reproduce import ROOT, checked_source, read, require, sha, write


def run(args):
    root = args.output.resolve(strict=True)
    protocol = read(ROOT / "PROTOCOL.json")
    engine, _ = checked_source(args.source, args.trainer, protocol)
    sys.path.insert(0, str(args.instruments.resolve(strict=True) / "src"))
    from experiments.gfg_nanogpt_actual_update_boundary_v1.runner import write_ledger
    from experiments.gfg_nanogpt_full_network_receptive_state_v1.analysis import _model
    from gfg_instruments.evidence import payload, validate_journal

    torch.set_num_threads(2)
    prediction = root / "TL-P01-window"
    e08 = root / "TL-E08-window"
    source_pred = sha(prediction / "RESULTS.json")
    ledger, sections = [], []
    for run in protocol["runs"]:
        tag = run["id"]
        task = engine.build_formal_task(instance_id=tag,token_seed=run["token_seed"],split_seed=run["split_seed"])
        model = _model(args.trainer.resolve()).eval()
        journal_root = prediction / tag / "gfg"
        validate_journal(journal_root)
        journal = read(journal_root / "journal.json")
        refs = {r["id"]: r for r in (*journal["sources"], *journal["events"])}
        for case_path in sorted((prediction / tag).glob("CASE_*.json")):
            case = read(case_path)
            adj = refs[case["adjudication"]["evidence_ref"]]
            seal_event, actual_event = (refs[p] for p in adj["parents"])
            require(seal_event["operation"] == "pretarget_prediction_seal" and
                    actual_event["operation"] == "actual_native_endpoint_readout" and seal_event["index"] < actual_event["index"],
                    "BOUNDARY_AUDIT_TEMPORAL_BINDING")
            coordinate_ref = refs[seal_event["parents"][0]]
            pre_ref, update_ref = (refs[p] for p in coordinate_ref["parents"])
            pre = payload(journal_root, pre_ref["artifact"])
            native_update = payload(journal_root, update_ref["artifact"])
            coordinate = payload(journal_root, coordinate_ref["artifact"])
            sealed = payload(journal_root, seal_event["artifact"])
            observed = payload(journal_root, actual_event["artifact"])
            require(case["seal_sha256"] == sealed["seal_sha256"], "BOUNDARY_AUDIT_WRONG_SEAL")
            require(list(task.validation_sample_ids) == sealed["identities"], "BOUNDARY_AUDIT_WRONG_TARGETS")
            ordered = {name: x for name, x in model.named_parameters()}
            require(set(pre["state"]) == set(native_update["update"]) == set(ordered), "BOUNDARY_AUDIT_PARAM_SET")
            base = {name: pre["state"][name].cpu() for name in ordered}
            delta = {name: native_update["update"][name].cpu() for name in ordered}

            def forward(values):
                logits, _ = functional_call(model, values, (task.validation_inputs.cpu(),), tie_weights=True)
                return logits[:, -1, :]

            with sdpa_kernel(SDPBackend.MATH):
                primal, tangent = jvp(forward, (base,), (delta,))
            expected = coordinate["logits"].detach().cpu().numpy()
            primal_error = float(np.max(np.abs(primal.detach().numpy() - expected)))
            directional = tangent.detach().numpy().astype(np.float64)
            full = []
            for i, y in enumerate(task.validation_targets[:, -1].tolist()):
                competitor = np.argsort(expected[i].astype(np.float64))[::-1]
                competitor = competitor[competitor != y]
                full.append(directional[i, y] - directional[i, competitor])
            separated = coordinate["candidate_gap_sets"]["linear"] - coordinate["gaps"]
            diff = float(np.max(np.abs(np.asarray(full) - separated)))
            require(primal_error <= 5e-5 and diff <= 5e-4, f"ORIGINAL_JVP_GATE_FAILED:{tag}:{case['step']}:{primal_error}:{diff}")
            sections.append({"run": tag, "step": case["step"], "primal_max_abs": primal_error,
                             "full_network_jvp_reconstruction_max_abs": diff, "seal_sha256": case["seal_sha256"]})
            aligned = {identity: i for i, identity in enumerate(observed["identities"])}
            require(set(aligned) == set(sealed["identities"]) and sealed["item_hashes"] == observed["item_hashes"],
                    "BOUNDARY_MARGIN_TARGET_MISMATCH")
            for i, identity in enumerate(sealed["identities"]):
                j = aligned[identity]
                a, b = float(sealed["before_margins"][i]), float(observed["margins"][j])
                row = case["adjudication"]["rows"][i]
                require(row["identity"] == identity and row["before"] == (a > 0) and row["actual"] == (b > 0),
                        "MARGIN_LEDGER_SIGN_MISMATCH")
                ledger.append({"run": tag, "step": case["step"], "identity": identity,
                               "native_target_group": int(sealed["group_by_identity"][identity]),
                               "before_margin": a, "after_margin": b, "transition": row["transition"],
                               "source_journal_sha256": journal["journal_sha256"]})
    require(len(ledger) == read(e08 / "RESULTS.json")["target_count"], "MARGIN_LEDGER_COUNT")
    write_ledger(e08 / "MEASURED_MARGINS.jsonl.gz", ledger)
    require(sha(prediction / "RESULTS.json") == source_pred, "PREDICTION_RESULTS_CHANGED_DURING_AUDIT")
    report = {"status": "PASS", "section_count": len(sections), "sections": sections,
              "max_jvp_error": max(x["full_network_jvp_reconstruction_max_abs"] for x in sections),
              "measurement_count": len(ledger), "actual_margin_ledger_sha256": sha(e08 / "MEASURED_MARGINS.jsonl.gz"),
              "prediction_result_sha256_unchanged": source_pred}
    write(prediction / "DERIVATIVE_AUDIT.json", report)
    print(f"Full-network JVP verified on {len(sections)} sections, max gap error {report['max_jvp_error']:.6g}")


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    for key in ("source", "trainer", "output", "instruments"):
        cli.add_argument("--" + key, type=Path, required=True)
    run(cli.parse_args())
