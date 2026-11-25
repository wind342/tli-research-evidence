"""Run the Supplement from newly trained histories or independently verify and replay archived histories."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys

from reproduce import ROOT, read, require, sha, write


def verify_bundle():
    index = ROOT / "SHA256_MANIFEST.json"
    package_root = ROOT.parent.parent
    if not index.is_file() and (ROOT / "PACKAGE_SCOPE.json").is_file():
        index = package_root / "SHA256_MANIFEST.json"
        prefix = ROOT.relative_to(package_root).as_posix() + "/"
        manifest = read(index)
        entries = {name.removeprefix(prefix): info["sha256"]
                   for name, info in manifest.items() if name.startswith(prefix)}
        require(entries, "SUPPLEMENT_PACKAGE_MANIFEST_EMPTY")
    elif index.is_file():
        entries = read(index)["files"]
    else:
        return False
    for name, expected in entries.items():
        path = (ROOT / name).resolve(strict=True)
        require(path.is_relative_to(ROOT), "BUNDLE_MANIFEST_PATH_ESCAPE")
        require(sha(path) == expected, "BUNDLE_FILE_HASH:" + name)
    return True


def git(path, *args):
    subprocess.run(["git", "-C", str(path), "-c", "core.autocrlf=false", *args], check=True)


def archive_core(output, verified_source):
    target = output.parent / (output.name + "-packaged-core")
    if not (target / ".git").is_dir():
        require(not target.exists(), "PACKAGED_CORE_TARGET_EXISTS")
        shutil.copytree(verified_source, target)
        git(target, "init", "-q")
        git(target, "add", "--", "src", "compat", "protocol")
        git(target, "-c", "user.name=Evidence packaging", "-c", "user.email=archive@example.invalid",
            "-c", "commit.gpgsign=false", "commit", "-q", "--no-verify", "-m", "Restore exported tracked Core content")
    return target


def archive_trainer(output, exported):
    target = output.parent / (output.name + "-packaged-trainer")
    registered = read(exported / "TRAINER_EXPORT.json")
    if not (target / ".git").is_dir():
        require(not target.exists(), "PACKAGED_TRAINER_TARGET_EXISTS")
        subprocess.run(["git", "-c", "core.autocrlf=false", "clone", "-q", "--no-checkout", str(exported / "nanoGPT.bundle"), str(target)], check=True)
        git(target, "checkout", "-q", "--detach", registered["upstream_commit"])
        sha_blob = sha(target / "model.py")
        require(sha_blob == registered["upstream_blob_sha256"], "PACKAGED_TRAINER_TRACKED_BYTES")
        shutil.copyfile(exported / "model.py", target / "model.py")
    require(sha(target / "model.py") == registered["model_sha256"], "PACKAGED_TRAINER_WORKING_BYTES")
    return target


def seed_from_pack(output, captured):
    # Native captured files are required; no result JSON is accepted by itself.
    require(not output.exists(), "CLEAN_REPLAY_OUTPUT_EXISTS")
    output.mkdir(parents=True)
    for name in ("PROTOCOL.json", "HISTORIES.json", "RUN_FREEZE.json"):
        shutil.copyfile(captured / name, output / name)
    shutil.copytree(captured / "histories", output / "histories")
    require(sha(output / "PROTOCOL.json") == sha(ROOT / "PROTOCOL.json"), "ARCHIVED_PROTOCOL_DRIFT")


def main(args):
    verified_bundle = verify_bundle()
    if args.command == "verify-package":
        require(verified_bundle, "NO_BUNDLE_MANIFEST")
        print("Bundle file hashes verified.")
        return
    out = args.output.resolve()
    source, trainer = args.source.resolve(strict=True), args.trainer.resolve(strict=True)
    args.core_source = args.core_source.resolve(strict=True)
    require(not out.is_relative_to(source) and not out.is_relative_to(trainer), "OUTPUT_INSIDE_SOURCE")
    using_pack = args.command == "replay-captured"
    if using_pack:
        seed_from_pack(out, args.captured.resolve(strict=True))
    elif not args.resume:
        require(not out.exists(), "RERUN_OUTPUT_EXISTS_USE_RESUME_FOR_VERIFIED_STAGES")
    out.mkdir(parents=True, exist_ok=True)
    core = (args.core_source if (args.core_source / ".git").exists()
            else archive_core(out, args.core_source))
    if not (trainer / ".git").exists():
        trainer = archive_trainer(out, trainer)
    a = ["--source", str(source), "--trainer", str(trainer), "--output", str(out)]
    helpers = args.helpers.resolve(strict=True)
    packaged_scope = ROOT / "PACKAGE_SCOPE.json"
    e07_only = packaged_scope.is_file() and read(packaged_scope)["new_experiment_ids"] == [
        "TL-E01", "TL-E02", "TL-E03", "TL-E04", "TL-E06", "TL-E07", "TL-E08", "INF-E01", "TL-P01"]
    require(not (e07_only and args.experiment == "TL-E05"), "TL-E05_RECORDS_IN_PAPER_EVIDENCE")
    windows = out / "window-inputs" / "v3"
    plan = {
        "histories": ("reproduce.py", ["histories", *a], "HISTORIES.json", ()),
        "support": ("measure.py", ["support", *a, "--core-source", str(core)], "TL-E06/INDEPENDENT_REPLAY.json", ("histories",)),
        "inference": ("measure.py", ["inference", *a, "--core-source", str(core)], "INF-E01/RESULTS.json", ("support",)),
        "interventions": ("e02_causal.py", a, "TL-E02-causal/RESULTS.json", ("histories",)),
        "selection": ("select_windows.py", [*a, "--cumulative-client", str(helpers / "cumulative_gfg.py"),
           "--legacy-features", str(helpers / "theory" / "feature_extraction.py"), "--csrg-features", str(helpers / "csrg" / "csrg_analysis.py")],
           "window-inputs/v3/BATCH_AVAILABILITY.json", ("support",)),
        "fork_windows": ("stepwise.py", [*a, "--fork-only"], "fork-stepwise/STATUS.json", ("selection",)),
        "forks_paths_exchange": ("long_paths.py", [*a, "--stepwise-dir", "fork-stepwise"], "TL-E03/STATUS.json", ("fork_windows",)),
        "boundaries": ("boundary.py", [*a, "--window-selection", str(windows / "WINDOWS.json"), "--instruments", str(args.instruments.resolve(strict=True))],
                       "TL-P01-window/RESULTS.json", ("selection",)),
        "boundary_audit": ("audit_boundary.py", [*a, "--instruments", str(args.instruments.resolve(strict=True))],
                           "TL-P01-window/DERIVATIVE_AUDIT.json", ("boundaries",)),
        "aligned_windows": ("e05_windows.py", a, "aligned-stepwise/STATUS.json", ("boundary_audit",)),
        "aligned_factors": ("adjacent.py", [*a, "--stepwise-dir", "aligned-stepwise", "--response-contract", str(helpers / "EXPERIMENT_CONTRACT.md"),
              "--alignment-lock", str(out / "aligned-stepwise" / "STRATA_FREEZE.json"),
              *(["--e07-without-factors"] if e07_only else [])], "TL-E07-aligned/RESULTS.json", ("aligned_windows",)),
    }
    experiments = {"TL-E01": "histories", "TL-E02": "interventions", "TL-E03": "forks_paths_exchange",
        "TL-E04": "forks_paths_exchange", "TL-E05": "aligned_factors", "TL-E06": "support",
        "TL-E07": "aligned_factors", "TL-E08": "boundary_audit", "INF-E01": "inference", "TL-P01": "boundary_audit"}
    if e07_only:
        del experiments["TL-E05"]
    wanted = set()

    def visit(name):
        if name in wanted:
            return
        wanted.add(name)
        for parent in plan[name][3]:
            visit(parent)

    for name in ([experiments[args.experiment]] if args.experiment else plan):
        visit(name)
    receipt = out / "RERUN_REPORT.json"
    records = read(receipt)["stages"] if args.resume and receipt.exists() else {}
    for name, (script, argv, expected, parents) in plan.items():
        if name not in wanted:
            continue
        if any(records[p]["execution"] not in {"PASS", "VERIFIED_CAPTURE"} for p in parents):
            records[name] = {"execution": "BLOCKED_DEPENDENCY", "dependencies": list(parents)}
        else:
            path = out / expected
            if args.resume and records.get(name, {}).get("execution") == "PASS":
                require(sha(path) == records[name]["record_sha256"], "RERUN_STAGE_RECEIPT_MODIFIED:" + name)
                continue
            if name == "histories" and using_pack:
                # Original validator runs against all actual archived capture blocks.
                from reproduce import checked_source
                checked_source(source, trainer, read(ROOT / "PROTOCOL.json"))
                from experiments.gfg_nanogpt_autonomous_capability_discovery_v1.training_gfg import validate_training_gfg
                from inspect import signature
                require("database_path" in signature(validate_training_gfg).parameters, "CAPTURE_VALIDATOR_INTERFACE_DRIFT")
                for tag, frozen in read(path).items():
                    state = out / "histories" / tag
                    db = state / "participant_gfg.sqlite3"
                    require(sha(db) == frozen["database_sha256"] and sha(state / "capture_manifest.json") == frozen["capture_manifest_sha256"],
                            "PACKAGED_HISTORY_IDENTITY:" + tag)
                    result = validate_training_gfg(db)
                    require(result["status"] == "PASS", "PACKAGED_HISTORY_VALIDATION:" + tag)
                records[name] = {"execution": "VERIFIED_CAPTURE", "source": expected, "record_sha256": sha(path)}
            else:
                print(name, flush=True)
                completed = subprocess.run([sys.executable, "-B", "-u", str(ROOT / script), *argv])
                records[name] = {"execution": "PASS" if completed.returncode == 0 and path.is_file() else "FAIL",
                                 "return_code": completed.returncode, "source": expected,
                                 "record_sha256": sha(path) if path.is_file() else None}
        write(receipt, {"stages": records, "experiment_stages": experiments, "mode": args.command})
    if any(records[name]["execution"] not in {"PASS", "VERIFIED_CAPTURE"} for name in wanted):
        raise SystemExit(1)


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("command", choices=["rerun-all", "rerun", "replay-captured", "verify-package"])
    cli.add_argument("experiment", nargs="?", choices=read(ROOT / "PROTOCOL.json")["targets"])
    cli.add_argument("--resume", action="store_true")
    cli.add_argument("--output", type=Path, default=ROOT.parent / "nanoGPT-independent-rerun")
    for option, name in (("source", "research_source"), ("trainer", "trainer"), ("core-source", "core"),
                         ("instruments", "instruments"), ("helpers", "helpers"), ("captured", "captured")):
        default = ROOT / name
        if option == "source" and not default.is_dir():
            default = ROOT.parent.parent / name
        cli.add_argument("--" + option, type=Path, default=default)
    args = cli.parse_args()
    require((args.command == "rerun") == (args.experiment is not None), "RERUN_REQUIRES_ONE_EXPERIMENT_ID")
    main(args)
