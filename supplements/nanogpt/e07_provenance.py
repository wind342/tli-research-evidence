"""Recompute TL-E07 from the observed response sections and realized update objects."""
import argparse
from pathlib import Path
import sys

from reproduce import ROOT, read, require, sha


def obtain_rows(inventory, responses, selection, geom):
    selected = {s["section_id"]: s for pair in selection["pairs"] for s in pair["sections"]}
    native = {r["section_id"]: r for r in responses["sections"]}
    roster = {s["section_id"] for s in inventory["sections"]}
    require(set(selected) == set(native) == roster and len(roster) == len(inventory["sections"]),
            "E07_RESPONSE_ROSTER")
    rows = []
    for s in sorted(inventory["sections"], key=lambda x: x["section_id"]):
        sid = s["section_id"]
        response = Path(s["section_npz"])
        transition = Path(s["transition_path"])
        transition_doc = read(transition)
        require(response.name == native[sid]["data_file"] and
                sha(response) == native[sid]["data_file_sha256"] and native[sid]["status"] == "PASS",
                "E07_RESPONSE_IDENTITY:" + sid)
        step = int(selected[sid]["receiver_optimizer_step_audit_only"])
        require(transition_doc["entry_id"] == s["entry_id_audit_only"] and
                int(transition_doc["optimizer_step"]) == step, "E07_UPDATE_IDENTITY:" + sid)
        _, measured = geom._section_features(s)
        norms = {name.replace(".", "_") + "_update_l2": value
                 for name, value in measured["component_update_l2_norms"].items()}
        rows.append({"section_id": sid, "entry_id": s["entry_id_audit_only"], "optimizer_step": step,
                     "features": {"F3": {"numeric": {**norms, "update_l2_norm": measured["update_l2_norm"]}}},
                     "source_refs": {"section_npz": str(response), "section_npz_sha256": sha(response),
                                     "transition": str(transition), "transition_sha256": sha(transition)}})
    return rows


def native_reallocation(rows, analysis):
    original = analysis._sections
    try:
        analysis._sections = lambda: rows
        return analysis.run_analysis()
    finally:
        analysis._sections = original


def bound(root, name):
    path = (root / name).resolve(strict=True)
    require(path.is_relative_to(root) and path.is_file(), "E07_SOURCE_PATH:" + name)
    return path


def verify(root, source):
    from collections import Counter
    import gzip
    import json

    sys.path[:0] = [str(source), str(source / "src")]
    from experiments.gfg_nanogpt_adjacent_response_transport_v1 import geometry
    from experiments.gfg_nanogpt_support_reallocation_audit_v1 import analysis

    index = read(root / "SOURCE_INDEX.json")
    paths = index["source_files_sha256"]
    for path, digest in paths.items():
        require(sha(bound(root, path)) == digest, "E07_SOURCE_HASH:" + path)
    sections = [{**r, **{k: str(bound(root, r[k])) for k in ("section_npz", "transition_path", "receiver_probe_path")}}
                for r in index["sections"]]
    rows = obtain_rows({"section_count": len(sections), "sections": sections},
                       read(root / "inputs/FINITE_AMPLITUDE_CURVES_MANIFEST.json"),
                       read(root / "inputs/SELECTION_MANIFEST.json"), geometry)
    checked = native_reallocation(rows, analysis)
    for expected, actual in (("SECTION_UPDATE_LEDGER.jsonl.gz", checked["section_rows"]),
                             ("TARGET_SUPPORT_TRANSITION_LEDGER.jsonl.gz", checked["group_rows"])):
        with gzip.open(root / expected, "rt", encoding="utf-8") as stream:
            require(list(map(json.loads, stream)) == actual, "E07_LEDGER_MISMATCH:" + expected)
    require(checked["summary"] == read(root / "RESULTS.json")["summary"], "E07_SUMMARY_MISMATCH")
    require(Counter(r["entry_id"] for r in rows) == Counter({f"nano-supp-0{i}": 12 for i in (1, 2, 3)}),
            "E07_HISTORICAL_COVERAGE")
    print(f"TL-E07: {len(rows)} response sections, {len(checked['group_rows'])} target-group records; verified.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--records", type=Path, default=ROOT / "records" / "TL-E07")
    p.add_argument("--source", type=Path, default=ROOT.parent.parent / "research_source")
    args = p.parse_args()
    verify(args.records.resolve(strict=True), args.source.resolve(strict=True))
