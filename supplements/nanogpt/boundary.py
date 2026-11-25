"""Re-execute TL-P01's original derivative kernel on newly captured updates."""
import argparse
import json
from pathlib import Path
import sys

import numpy as np
import torch

from reproduce import ROOT, checked_source, read, require, sha, write


def coordinates(trainer, state, update, inputs, targets, recorded):
    from experiments.gfg_nanogpt_joint_rotation_branch_v1.analysis import HiddenStateModel, _hidden_derivatives, _model

    wrapper = HiddenStateModel(_model(trainer)).cpu().eval()
    named = tuple(name for name, _ in wrapper.gpt.named_parameters())
    require(set(named) == set(state) == set(update), "PREDICTOR_PARAMETER_SET")
    params = {f"gpt.{k}": state[k].detach().cpu().clone() for k in named}
    tangent = {f"gpt.{k}": update[k].detach().cpu().clone() for k in named}
    h, h1, h2 = _hidden_derivatives(wrapper, params, tangent, inputs.cpu())
    h, h1, h2 = (v.detach().numpy().astype(np.float64) for v in (h, h1, h2))
    w = params["gpt.transformer.wte.weight"].numpy().astype(np.float64)
    dw = tangent["gpt.transformer.wte.weight"].numpy().astype(np.float64)
    require(float(np.max(np.abs(h @ w.T - recorded))) <= 5e-5, "PREDICTOR_HIDDEN_LOGIT_RECONSTRUCTION")
    count = len(targets)
    gaps = np.empty((count, 23), dtype=np.float64)
    first = np.empty((count, 23), dtype=np.float32)
    joint = np.empty_like(first)
    curve = np.empty_like(first)
    for i, target in enumerate(targets):
        order = np.argsort(recorded[i])[::-1]
        competitors = order[order != target]
        b = w[target][None, :] - w[competitors]
        bp = dw[target][None, :] - dw[competitors]
        gaps[i] = recorded[i, target] - recorded[i, competitors]
        require(float(np.max(np.abs(b @ h[i] - gaps[i]))) <= 1e-4, "PREDICTOR_GAP_RECONSTRUCTION")
        first[i] = bp @ h[i] + b @ h1[i]
        joint[i] = bp @ h1[i]
        curve[i] = 0.5 * (b @ h2[i])
    first, joint, curve = (v.astype(np.float64) for v in (first, joint, curve))
    return gaps, {
        "linear": gaps + first,
        "joint_rotation": gaps + first + joint,
        "hidden_curvature": gaps + first + curve,
        "quadratic_complete": gaps + first + joint + curve,
    }


def native_measure(logits, group, batch, contract):
    from gfg_instruments.boundaries import readout, validate_readout

    # Boundary is strict margin > 0, not token-argmax tie adjudication.
    measured = readout(logits, group, batch, contract)
    validate_readout(measured)
    return measured


def case_rows(runtime, trainer, step, run, task, output, journal):
    from experiments.gfg_nanogpt_support_redundancy_v1.runtime import tensor_sha256
    from gfg_instruments.contracts import Batch, BoundaryContract
    from gfg_instruments.ledger import adjudicate, seal_prediction

    anchor = (step // 100) * 100
    receiving, proof = runtime.load_source_state(anchor)
    runtime.restore(receiving)
    for t in range(anchor, step):
        runtime.train_actual_step(runtime.load_batch(t), execute_optimizer=True,
                                  seed=runtime.derive_seed(sha(ROOT / "PROTOCOL.json"), run, t, 1))
    pre = runtime.snapshot()
    source_parameters, source_adam = runtime.source_rows(step)
    require(all(tensor_sha256(pre.parameters[k]) == row["content_sha256"]
                for k, row in source_parameters.items()), "RECEIVER_NOT_NATIVE_EXACT")
    require(all(tensor_sha256(pre.optimizer[k.rsplit(".", 1)[0]][k.rsplit(".", 1)[1]]) ==
                row["content_sha256"] for k, row in source_adam.items()), "RECEIVER_ADAM_NOT_NATIVE_EXACT")
    native = runtime.train_actual_step(runtime.load_batch(step), execute_optimizer=True,
                                       seed=runtime.derive_seed(sha(ROOT / "PROTOCOL.json"), run, step, 1))
    post = runtime.snapshot()
    endpoint_parameters, endpoint_adam = runtime.source_rows(step + 1)
    require(all(tensor_sha256(post.parameters[k]) == row["content_sha256"]
                for k, row in endpoint_parameters.items()), "ENDPOINT_NOT_NATIVE_EXACT")
    require(all(tensor_sha256(post.optimizer[k.rsplit(".", 1)[0]][k.rsplit(".", 1)[1]]) ==
                row["content_sha256"] for k, row in endpoint_adam.items()), "ENDPOINT_ADAM_NOT_NATIVE_EXACT")
    runtime.restore(pre)
    runtime.model.eval()
    inputs = runtime.base.validation_inputs.cpu()
    labels = runtime.base.validation_targets.cpu()
    target = labels[:, -1].numpy()
    require(torch.equal(inputs, task.validation_inputs.cpu())
            and torch.equal(labels, task.validation_targets.cpu()), "VALIDATION_CONTENT_IDENTITY")
    batch = Batch(tuple(task.validation_sample_ids), (inputs,), labels, tuple(map(str, target)), run)
    boundary = BoundaryContract(name="tlir-native-target-gap-v1", correct_rule="positive", zero_evaluable=True)
    binding = journal.source(f"{run}:{step}:receiver", {"state": pre.parameters, "adam": pre.optimizer,
                             "source_step": step, "source_rows": source_parameters,
                             "source_adam": source_adam, "anchor_proof": proof})
    update = journal.record("actual_formed_native_update", [binding],
                            {"update": native.parameter_updates, "batch": runtime.load_batch(step).source_rows})
    pre_logits = runtime.base.forward()
    baseline = native_measure(pre_logits, labels[:, -1], batch, boundary)
    gaps, endpoint = coordinates(trainer, pre.parameters, native.parameter_updates,
                                 inputs, target, pre_logits.numpy().astype(np.float64))
    deriv = journal.record("quadratic_complete_directional_coordinates", [binding, update],
                           {"logits": pre_logits, "gaps": gaps, "candidate_gap_sets": endpoint})
    seal = seal_prediction(batch, boundary, baseline, np.min(endpoint["quadratic_complete"], axis=1),
                           journal, [deriv], method="quadratic_complete")
    write(output / f"{step:05d}-PREDICTION_SEAL.json", {
        "seal_sha256": seal["seal_sha256"], "occurrence": seal["evidence_ref"],
        "predicted_correct": seal["predicted_correct"].tolist(), "identities": list(batch.identities)
    })
    runtime.restore(post)
    runtime.model.eval()
    logits = runtime.base.forward()
    observed = native_measure(logits, labels[:, -1], batch, boundary)
    ref = journal.record("actual_native_endpoint_readout", [update, seal["evidence_ref"]], observed)
    result = adjudicate(seal, observed, batch, boundary, journal, ref)
    return {
        "run": run, "step": step, "exact_native_receiving_and_endpoint_state": True,
        "seal_sha256": seal["seal_sha256"], "adjudication": result,
        "predictions": {k: np.all(a > 0, axis=1).tolist() for k, a in endpoint.items()}
    }


def main(args):
    torch.set_num_threads(2)
    root = args.output.resolve(strict=True)
    protocol = read(ROOT / "PROTOCOL.json")
    engine, bindings = checked_source(args.source, args.trainer, protocol)
    require(sha(ROOT / "PROTOCOL.json") == sha(root / "PROTOCOL.json"), "SUPPLEMENT_PROTOCOL_DRIFT")
    require(read(root / "RUN_FREEZE.json")["source_sha256"] == bindings, "SOURCE_FREEZE_DRIFT")
    sys.path.insert(0, str(args.instruments.resolve(strict=True) / "src"))
    from gfg_instruments.evidence import Journal, validate_journal
    from experiments.gfg_nanogpt_stepwise_support_transition_v1 import runtime as sst
    from experiments.gfg_nanogpt_actual_update_boundary_v1.analysis import _macro_recall, _metrics, _repair, _transition_confusion

    # These checkpoint anchors were set independently of response results.
    grid = (1000, 1001, 3000, 3001, 7000, 7001)
    phase = args.window_selection is not None
    uses = {r["id"]: grid for r in protocol["runs"]}
    selected_path = args.window_selection.resolve(strict=True) if phase else None
    if phase:
        windows = read(selected_path)["windows"]
        for row in protocol["runs"]:
            tag = row["id"]
            selected = []
            for kind in ("matched_stable", "pre_decline", "recovery"):
                pool = [w for w in windows if w["entry_id"] == tag and kind in w["categories"] and
                        w["scientific_end_optimizer_step"] - w["scientific_start_optimizer_step"] >= 2]
                if not pool:
                    continue
                win = min(pool, key=lambda w: (w["scientific_start_optimizer_step"], w["window_id"]))
                first = (win["scientific_start_optimizer_step"] if kind == "matched_stable"
                         else win["scientific_end_optimizer_step"] - 2)
                selected.extend((first, first + 1))
            require(selected, "NO_PREDICTOR_PHASE_WINDOW:" + tag)
            uses[tag] = sorted(set(selected))
    out = root / ("TL-P01-window" if phase else "TL-P01")
    out.mkdir(exist_ok=False)
    write(out / "PREDICTION_CASE_FREEZE.json", {
        "optimizer_steps": uses, "source_protocol_sha256": sha(root / "PROTOCOL.json"),
        "selection_sha256": sha(selected_path) if phase else None,
        "registration": ("fixed two adjacent steps per available original maintain/decline/recovery window; no target or predictions used in selection"
                         if phase else "fixed-grid, pipeline-only check; not selected from endpoint outcomes"),
        "splits": {x["id"]: x["role"] for x in protocol["runs"]}
    })
    reg = Path(sst.__file__).parent
    registry = sst.ComponentRegistry.load(reg / "component_registry_csrg_4c_v1.json")
    probes = sst.ProbeContract.load(reg / "probe_contract_csrg_4c_v1.json", registry)
    all_cases = []
    for run in protocol["runs"]:
        tag = run["id"]
        native = root / "histories" / tag
        authority = read(root / "HISTORIES.json")[tag]
        require(authority["status"] == "PASS" and sha(native / "participant_gfg.sqlite3") ==
                authority["database_sha256"], "PREDICTION_CAPTURE_AUTHORITY")
        task = engine.build_formal_task(instance_id=tag, token_seed=run["token_seed"],
                                        split_seed=run["split_seed"])
        journal = Journal(out / tag / "gfg", tag)
        rt = sst.StepwiseTrainingRuntime(native, args.trainer.resolve(), registry, probes)
        try:
            for step in uses[tag]:
                value = case_rows(rt, args.trainer.resolve(), step, tag, task, out / tag, journal)
                value["role"] = run["role"]
                all_cases.append(value)
                write(out / tag / f"CASE_{step:05d}.json", value)
                print(tag, step, "sealed, then adjudicated", flush=True)
        finally:
            rt.close()
        journal.save()
        validate_journal(journal.root)
    rows = [row for case in all_cases for row in case["adjudication"]["rows"]]
    starts = np.asarray([row["before"] for row in rows], dtype=bool)
    truth = np.asarray([row["actual"] for row in rows], dtype=bool)
    phase = np.asarray([row["transition"].upper().replace("->", "_TO_") if "->" in row["transition"]
                        else row["transition"] for row in rows], dtype=object)
    phase[phase == "CORRECT_TO_CORRECT"] = "MAINTAIN_CORRECT"
    phase[phase == "WRONG_TO_WRONG"] = "MAINTAIN_WRONG"
    roles = np.asarray([case["role"] for case in all_cases for _ in case["adjudication"]["rows"]])
    run_ids = np.asarray([case["run"] for case in all_cases for _ in case["adjudication"]["rows"]])
    result = {}
    linear = np.asarray([p for case in all_cases for p in case["predictions"]["linear"]], dtype=bool)
    for name in ("development", "confirmation", "all_runs", *uses):
        mask = (run_ids == name if name in uses else roles == name if name != "all_runs" else np.ones(len(truth), dtype=bool))
        result[name] = {}
        for method in all_cases[0]["predictions"]:
            pred = np.asarray([p for case in all_cases for p in case["predictions"][method]], dtype=bool)
            m = _metrics(truth, pred, starts, phase, mask)
            m["four_way_macro_recall"] = (_macro_recall(m) if all(x is not None for x in m["transition_recall"].values()) else None)
            m["four_way_confusion"] = _transition_confusion(starts, truth, pred, mask)
            m["repair_vs_linear"] = _repair(truth, linear, pred, mask)
            result[name][method] = m
    confirm = result["confirmation"]["quadratic_complete"]
    verdict = ("NOT_EVALUABLE_MISSING_TRANSITIONS" if confirm["four_way_macro_recall"] is None else
               "CONFIRMATION_GATE_MET" if min(confirm["accuracy"], confirm["four_way_macro_recall"]) >= 0.90 else
               "CONFIRMATION_GATE_NOT_MET")
    write(out / "RESULTS.json", {"metrics": result, "section_count": len(all_cases), "target_count": len(rows), "verdict": verdict})
    e08 = root / ("TL-E08-window" if args.window_selection is not None else "TL-E08")
    e08.mkdir(exist_ok=False)
    from collections import Counter
    write(e08 / "RESULTS.json", {
        "scope": "identity-aligned measurement of native target-boundary changes; not the historical 500-case candidate",
        "section_count": len(all_cases), "target_count": len(rows),
        "native_transition_counts": dict(Counter(phase.tolist())),
        "case_ledgers": [f"../{out.name}/{case['run']}/CASE_{case['step']:05d}.json" for case in all_cases],
    })
    print(json.dumps(result["confirmation"]["quadratic_complete"], sort_keys=True), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("source", "trainer", "output", "instruments"):
        parser.add_argument("--" + arg, type=Path, required=True)
    parser.add_argument("--window-selection", type=Path)
    main(parser.parse_args())
