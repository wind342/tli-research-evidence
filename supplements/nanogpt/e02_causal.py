"""Run matched pause/clip forks at the last captured pre-formation checkpoint."""
import argparse
import json
from pathlib import Path

import torch

from reproduce import ROOT, checked_source, read, require, sha, write

VARIANTS = {
    "nano-supp-01": ("pause", "entry-786d0a3628f6f791399f"),
    "nano-supp-02": ("pause", "entry-786d0a3628f6f791399f"),
    "nano-supp-03": ("clip", "entry-362ded584a953f360aec"),
}


def verify_intervention(receipt, cut, kind, horizon, content_hash):
    events = receipt["events"]
    require(receipt["event_count"] == len(events) and content_hash({k: v for k, v in receipt.items() if k != "receipt_sha256"}) ==
            receipt["receipt_sha256"], "TREATMENT_RECEIPT_IDENTITY")
    if kind == "pause":
        gradients = [x["step"] for x in events if x["stage"] == "after_backward" and x["change"] == "current_gradients"]
        gates = [x["step"] for x in events if x["stage"] == "before_optimizer_step" and x["change"] == "optimizer_group_hyperparameters"]
        require(gradients == list(range(cut, cut + 800)) and gates == [cut, cut + 800], "WRONG_PAUSE_EXECUTION")
    else:
        changes = [x for x in events if x["change"] == "gradient_clipping_control" and x["stage"] == "before_gradient_clip"]
        require([x["step"] for x in changes] == list(range(cut, horizon)) and
                all(x["before"] == 1.0 and x["after"] == 0.25 for x in changes), "WRONG_CLIP_EXECUTION")
    return {"status": "PASS", "kind": kind, "events": len(events), "receipt_sha256": receipt["receipt_sha256"]}


def run(args):
    root = args.output.resolve(strict=True)
    protocol = read(ROOT / "PROTOCOL.json")
    engine, bindings = checked_source(args.source, args.trainer, protocol)
    require(read(root / "RUN_FREEZE.json")["source_sha256"] == bindings, "SOURCE_FREEZE_DRIFT")
    from experiments.gfg_nanogpt_autonomous_capability_discovery_v1 import evaluation_capture as evals
    from experiments.gfg_nanogpt_autonomous_capability_discovery_v1.common import payload_sha256
    from experiments.gfg_nanogpt_autonomous_capability_discovery_v1.intervention_runtime import AuditedIntervention
    from experiments.gfg_nanogpt_autonomous_capability_discovery_v1.nanogpt_adapter import (
        build_model_and_optimizer, restore_checkpoint, train_plain,
    )
    from experiments.gfg_nanogpt_stepwise_support_transition_v1 import runtime as sst
    from experiments.gfg_nanogpt_support_redundancy_v1.runtime import tensor_sha256

    config_dir = Path(sst.__file__).parent
    registry = sst.ComponentRegistry.load(config_dir / "component_registry_csrg_4c_v1.json")
    probes = sst.ProbeContract.load(config_dir / "probe_contract_csrg_4c_v1.json", registry)
    plan = {}
    for row in protocol["runs"]:
        tag = row["id"]
        history = root / "histories" / tag
        metrics = read(history / "segment_result.json")["metrics"]
        formed = evals.capability_transition(metrics)
        require(formed is not None, "NATIVE_FORMATION_NOT_OBSERVED:" + tag)
        cut = max(x["step"] for x in metrics if x["step"] < formed and x["step"] % 100 == 0)
        kind, spec = VARIANTS[tag]
        sub = Path(engine.__file__).parent / "research_archive" / "entries" / spec / "submission"
        plan[tag] = {"cut": cut, "native_formation": formed, "intervention": kind,
                     "variant": spec, "native_sha256": sha(history / "participant_gfg.sqlite3"),
                     "hook_sha256": sha(sub / "intervention.py")}
    out = root / "TL-E02-causal"
    out.mkdir(exist_ok=True)
    frozen = {"rule": "Last 100-step checkpoint strictly before first native sustained formation. The frozen native history is the baseline; the treatment is a new branch from the authenticated identical state.",
              "historical_forecast_gate_used": False, "plan": plan}
    if (out / "FORK_FREEZE.json").exists():
        require(read(out / "FORK_FREEZE.json") == frozen, "CAUSAL_FORK_PLAN_DRIFT")
    else:
        write(out / "FORK_FREEZE.json", frozen)
    result_path = out / "RESULTS.json"
    completed = {x["run"]: x for x in read(result_path)["runs"]} if result_path.exists() else {}
    for row in protocol["runs"]:
        tag = row["id"]
        item = plan[tag]
        case = out / tag
        if tag in completed:
            audit = verify_intervention(read(case / "INTERVENTION_RECEIPT.json"), item["cut"], item["intervention"],
                                        protocol["steps_per_history"], payload_sha256)
            write(case / "HOOK_VALIDATION.json", audit)
            continue
        case.mkdir(exist_ok=True)
        history = root / "histories" / tag
        cut = item["cut"]
        task = engine.build_formal_task(instance_id=tag, token_seed=row["token_seed"], split_seed=row["split_seed"])
        config = engine.frozen_training_config(model_seed=row["model_seed"], data_order_seed=row["data_order_seed"])
        trainer = args.trainer.resolve()
        prefix = train_plain(trainer, task, config, stop_step=cut)
        cp = prefix["checkpoint"]
        require(cp.step == cut, "PREFIX_CUT_DRIFT:" + tag)
        model, opt = build_model_and_optimizer(trainer, task, config)
        restore_checkpoint(cp, model, opt, torch.Generator(device="cpu"), config.device)
        rt = sst.StepwiseTrainingRuntime(history, trainer, registry, probes)
        try:
            receiver, authority = rt.load_source_state(cut)
            live = dict(model.named_parameters())
            require(set(receiver.parameters) == set(live), "FORK_PARAMETER_IDENTITY")
            exact_parameters = {name: tensor_sha256(live[name].detach().cpu()) == tensor_sha256(value)
                                for name, value in receiver.parameters.items()}
            exact_optimizer = {name: {slot: tensor_sha256(opt.state[live[name]][slot].detach().cpu()) == tensor_sha256(value)
                                      for slot, value in states.items()} for name, states in receiver.optimizer.items()}
            before = rt.load_batch(cut)
            native_order = torch.randperm(task.train_inputs.shape[0], generator=torch.Generator().manual_seed(config.data_order_seed))
            require(torch.equal(before.inputs.cpu(), task.train_inputs[native_order]) and
                    torch.equal(before.targets.cpu(), task.train_targets[native_order]), "FORK_BATCH_IDENTITY")
            require(all(exact_parameters.values()) and all(all(x.values()) for x in exact_optimizer.values()), "FORK_NATIVE_STATE_MISMATCH:" + tag)
            write(case / "FORK_AUTHORITY.json", {"step": cut, "native_database_sha256": item["native_sha256"],
                  "parameter_identity": exact_parameters, "optimizer_identity": exact_optimizer,
                  "batch_matches": True, "state_source": authority, "checkpoint_sha256": prefix["checkpoint_sha256"]})
        finally:
            rt.close()
        del model, opt, receiver
        spec = Path(engine.__file__).parent / "research_archive" / "entries" / item["variant"] / "submission"
        intervention = AuditedIntervention(submission=spec, mechanism_state={}, forecast={})
        changed = engine.run_captured_segment(trainer_root=trainer, task=task, config=config,
            run_id=tag + "-native-causal-" + item["intervention"], output_directory=case / "treatment",
            initial_checkpoint=cp, intervention_hook=intervention, intervention_state=intervention.state)
        actual = evals.capability_transition(prefix["metrics"] + changed["metrics"])
        receipt = intervention.receipt()
        write(case / "INTERVENTION_RECEIPT.json", receipt)
        write(case / "HOOK_VALIDATION.json", verify_intervention(receipt, cut, item["intervention"], config.max_steps, payload_sha256))
        require(changed["gfg_validation"]["status"] == "PASS" and changed["start_step"] == cut, "TREATMENT_CAPTURE_NOT_VALIDATED")
        step_delta = actual - item["native_formation"] if actual is not None else None
        row_result = {"run": tag, "status": "EXECUTED", "cut": cut,
                      "baseline_transition_step": item["native_formation"], "intervention_transition_step": actual,
                      "actual_shift_optimizer_steps": step_delta, "variant": {"kind": item["intervention"]},
                      "interpretation": "NO_FORMATION_BY_FIXED_HORIZON" if actual is None else "MEASURED", "gfg": "PASS"}
        completed[tag] = row_result
        write(result_path, {"runs": list(completed.values()), "total_planned": len(plan)})
        print(json.dumps(row_result, sort_keys=True), flush=True)


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    for key in ("source", "trainer", "output"):
        cli.add_argument("--" + key, type=Path, required=True)
    run(cli.parse_args())
