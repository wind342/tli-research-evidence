#!/usr/bin/env python3
"""Check the active TLI repository structure and selected recorded results.

This is a lightweight, non-mutating consistency check. It does not rerun
neural-network training, the fourteen mathematical derivations, or historical
archive imports. The original import verifier remains a historical tool.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = (
    "README.md",
    "LETTER_TO_FUTURE_AI.md",
    "TLI_ICML_PAPER_EVIDENCE_MAP.md",
    "EXPERIMENT_INDEX.md",
    "EXPERIMENTAL_INSTRUMENTS.md",
    "PUBLIC_EVIDENCE_MATRIX.md",
    "PROPRIETARY_NOTICE.md",
    "EVIDENCE_IMPORT_MANIFEST.json",
    "EVIDENCE_IMPORT_CHECKS.json",
    "theory/TLI_UNIFIED_DYNAMICS.md",
    "theory/TLI_THEORY_FIRST_14_DERIVATIONS.md",
    "audits/TLI_14_EXTRAPOLATIONS_MATH_AUDIT.md",
    "audits/FULL_REPRODUCTION_AUDIT.md",
    "provenance/EVIDENCE_IMPORT.md",
    "provenance/SOURCE_MANIFEST.md",
    "provenance/EXTERNAL_ARTIFACTS.md",
    "docs/RL_EVIDENCE_CHAIN.md",
    "docs/CROSS_SYSTEM_EVIDENCE_CHAIN.md",
    "research_notes/TLI_INFERENCE_EXPLORATORY_DERIVATIONS.md",
    "math_audit/README.md",
    "math_audit/verify_14.py",
    "math_audit/inputs.json",
    "math_audit/RESULTS.json",
    "independent_stress_tests/windows_reproduction/WINDOWS_REPRODUCTION.json",
    "experiments/gfg_rl_selective_positive_feedback_support_concentration_v1/RESULTS.md",
    "experiments/gfg_rl_selective_positive_feedback_dose_recovery_v1/RESULTS.md",
)

ACTIVE_DOCS = (
    "README.md",
    "AGENTS.md",
    "EVIDENCE_FIRST_AI_REVIEW_STANDARD.md",
    "EXPERIMENT_INDEX.md",
    "EXPERIMENTAL_INSTRUMENTS.md",
    "PUBLIC_EVIDENCE_MATRIX.md",
    "PROPRIETARY_NOTICE.md",
    "TLI_ICML_PAPER_EVIDENCE_MAP.md",
    "LETTER_TO_FUTURE_AI.md",
)

MD_LINK = re.compile(r"\]\(([^)\s]+)\)")


def audit(root: Path) -> dict:
    root = root.resolve()
    errors: list[str] = []
    for rel in REQUIRED:
        if not (root / rel).is_file():
            errors.append(f"MISSING_REQUIRED:{rel}")
    if (root / "PUBLIC_ARCHIVE.md").exists():
        errors.append("WITHDRAWN_PUBLIC_ARCHIVE_PRESENT")
    if (root / "manuscripts/tlir_v8").exists():
        errors.append("RETIRED_MANUSCRIPT_DIRECTORY_PRESENT")

    docs = [root / rel for rel in ACTIVE_DOCS]
    for folder in ("theory", "audits", "provenance", "docs",
                   "research_notes", "math_audit"):
        if (root / folder).is_dir():
            docs.extend(sorted((root / folder).glob("*.md")))

    links_checked = 0
    for doc in docs:
        if not doc.is_file():
            errors.append(f"MISSING_ACTIVE_DOCUMENT:{doc.relative_to(root)}")
            continue
        data = doc.read_text(encoding="utf-8")
        for match in MD_LINK.finditer(data):
            link = match.group(1).strip()
            if link.startswith(("#", "http://", "https://", "mailto:", "//")):
                continue
            target = unquote(link.split("#", 1)[0].split("?", 1)[0])
            if not target:
                continue
            absolute = (doc.parent / target).resolve()
            links_checked += 1
            if not absolute.is_relative_to(root):
                errors.append(f"LINK_ESCAPES_REPO:{doc.relative_to(root)}:{link}")
            elif not absolute.exists():
                errors.append(f"BROKEN_LINK:{doc.relative_to(root)}:{link}")

    windows = root / "independent_stress_tests/windows_reproduction/WINDOWS_REPRODUCTION.json"
    if windows.is_file():
        record = json.loads(windows.read_text(encoding="utf-8"))
        gn = record["table3"]["gnn"]
        sn = record["table3"]["snn"]
        if (gn["correct"], gn["count"]) != (3068, 3072):
            errors.append("GNN_PREDICTION_COUNT_CHANGED")
        if (sn["correct"], sn["count"]) != (6713, 7200):
            errors.append("SNN_PREDICTION_COUNT_CHANGED")
        if not math.isclose(gn["accuracy"], gn["correct"] / gn["count"], abs_tol=1e-12):
            errors.append("GNN_ACCURACY_ARITHMETIC")
        if not math.isclose(sn["accuracy"], sn["correct"] / sn["count"], abs_tol=1e-12):
            errors.append("SNN_ACCURACY_ARITHMETIC")
        if not math.isclose(gn["four_way_macro_recall"], 0.9787234042553191, abs_tol=1e-10):
            errors.append("GNN_RECORDED_RECALL_CHANGED")
        if not math.isclose(sn["four_way_macro_recall"], 0.6005419093609791, abs_tol=1e-10):
            errors.append("SNN_RECORDED_RECALL_CHANGED")
        if record["gnn_structure_criteria_met"] != [8, 9, 8]:
            errors.append("GNN_STRUCTURE_VERDICT_CHANGED")
        if record["snn_structure_criteria_met"] != [12, 12, 12, 12]:
            errors.append("SNN_STRUCTURE_VERDICT_CHANGED")
        if sn["verdict"] != "PREDICTION_TRANSPORT_NOT_SUPPORTED":
            errors.append("SNN_NEGATIVE_PREDICTION_VERDICT_CHANGED")

    for rel, expected in (
        ("experiments/gfg_rl_selective_positive_feedback_support_concentration_v1/RESULTS.md",
         "NOT_SUPPORTED"),
        ("experiments/gfg_rl_selective_positive_feedback_dose_recovery_v1/RESULTS.md",
         "SUPPORTED"),
    ):
        file = root / rel
        if file.is_file() and expected not in file.read_text(encoding="utf-8"):
            errors.append(f"RL_RECORDED_VERDICT_CHANGED:{rel}")

    script = root / "math_audit/verify_14.py"
    if script.is_file() and "theory/TLI_THEORY_FIRST_14_DERIVATIONS.md" not in script.read_text(encoding="utf-8"):
        errors.append("MATH_AUDIT_SOURCE_PATH_STALE")
    result_file = root / "math_audit/RESULTS.json"
    if result_file.is_file():
        saved = json.loads(result_file.read_text(encoding="utf-8"))
        if (saved.get("checks"), saved.get("PASS"), saved.get("FAIL")) != (21, 21, 0):
            errors.append("SAVED_MATH_RECEIPT_CHANGED")

    return {
        "schema": "tli-current-tree-integrity-v1",
        "status": "PASS" if not errors else "FAIL",
        "scope": "active paths, Markdown links and selected committed result concordance",
        "not_performed": [
            "neural-network experiment rerun",
            "mathematical derivation rerun",
            "historical ZIP/archive import validation",
        ],
        "required_files": len(REQUIRED),
        "active_documents": len(docs),
        "local_links_checked": links_checked,
        "errors": errors,
    }


def main() -> int:
    output = audit(ROOT)
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0 if output["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
