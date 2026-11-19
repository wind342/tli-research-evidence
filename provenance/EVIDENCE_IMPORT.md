# Evidence import and preservation

> **Historical import record.** This file documents the original import and its availability at that point in time. Subsequent ICML alignment updated documentation and added November GNN/SNN machine records; see [the current TLI evidence map](../TLI_ICML_PAPER_EVIDENCE_MAP.md). Original imported experimental source files and machine results retain their recorded provenance.

## Sources

This repository is an owner-authorized copy and evidence-navigation layer over the existing public [research-evidence repository](https://github.com/wind342/gfg-training-learning-inference-experiments). Nothing is moved out of or deleted from that repository.

| Imported scope | Immutable source |
|---|---|
| Complete public main snapshot, including GFG Core, all original experiments, ResNet, diffusion, **MoE**, GRU feedback, existing documentation and public v8 manuscript assets | commit `766715a9728cce4e949714969f118fc7f16a0b41` |
| Complete `independent_stress_tests/` subtree, including GNN, SNN, native SNN binary parts and prediction-transport reports/code | commit `a35d143ea4952c48fce425161acd8f3ead408317` |
| Original publication archive | [Zenodo 22032772](https://doi.org/10.5281/zenodo.22032772), 10 original ZIPs and original archive metadata |
| Original frozen release | annotated tag `paper-experiments-cross-system-feedback-release`, commit `36dab5ce347dbbdac157ef23205f556606d18294` |

The source main history is retained. The annotated tag object is copied unchanged, not moved or recreated. The new combined repository has a new tip/tree identity: it is **not** the old frozen release. Historical manifests continue to identify their historical scope.

At the original import, experimental files were copied with their then-current Git blob identities, and the root README was extended. Later TLI maintenance removed obsolete manuscript assets and renamed GNN/SNN paths while retaining the original result records and historical source commits. The present working tree is not byte-identical to the original imported tree; original identities remain in Git history and the historical import manifest.

## Historical archive mirror (not a current TLI release)

The historical [GitHub Release mirror](https://github.com/wind342/tli-research-evidence/releases/tag/zenodo-22032772-mirror) and Zenodo record `22032772` identify the original import, not a current-paper evidence package. The historical import manifest records the old filenames and checksum identities; see the [current paper evidence map](../TLI_ICML_PAPER_EVIDENCE_MAP.md) for active experimental records.

The original import check compared the former release payload identities with its historical manifest. Its recorded outcome is not a fresh validation of the present directory.

## Explicit availability limits

1. **MoE:** the complete 20-file public experiment directory is included. Its `FORMAL_RESULTS.json`, historical independent-check receipt and 34-entry runtime manifest are present. The three raw final checkpoints, per-event records and compact GFG runtime files listed by that manifest were not in the source Git snapshot, were not in Zenodo 22032772, and were not located in the inspected local evidence locations. No reconstruction or claimed fresh replay is substituted for them.
2. **GNN/SNN prediction transport:** all five public files are included. The checker additionally requires `PREPARED_MANIFEST.json`, `PREDICTIONS_SEALED.json`, `PREDICTIONS_SEAL_RECEIPT.json`, `ADJUDICATION.json` and matching native/pretarget states; those are not in that public subtree. The report's historical audit claim is not a newly executed audit here.
3. **SNN structural tests:** all four distinct native states are present as 16 binary fragments. Their concatenated SHA-256 identities can be checked without deserializing PyTorch files. The existing restoration script reconstructs formal/replay copies.
4. **nanoGPT / original release:** public archives and compact records retain the scope documented in `PUBLIC_EVIDENCE_MATRIX.md`; not every historical training checkpoint or full CSRG runtime is included.
5. **Manuscript history and literature:** the original import included a v8 manuscript; those obsolete manuscript files were subsequently removed from the active tree and remain in Git history. The source import did not include the present paper's private plotting project. The later 21-pair research comparison ledger is a separate supplemental document under [`theory/`](../theory/).

These are original-import availability statements. Historical GNN/SNN stress-test and RL-E05 verdicts remain recorded; the current November GNN/SNN version is indexed separately in the [paper evidence map](../TLI_ICML_PAPER_EVIDENCE_MAP.md).

## Verification paths

**Current repository:** Run `python tools/verify_tli_repository_integrity.py` from the repository root to check active documentation paths and selected committed experiment-result identities.

**Original import (historical):** `tools/verify_tlir_evidence_import.py` compares the file tree against the original imported snapshot; the original byte-for-byte comparison does not apply after deliberate directory cleanup and renames. Its [import receipt](../EVIDENCE_IMPORT_CHECKS.json) and [manifest](../EVIDENCE_IMPORT_MANIFEST.json) remain historical records, not current-tree verification results.

## Rights and privacy

The original [proprietary notice](../PROPRIETARY_NOTICE.md) and third-party authority notices remain in force. No new open-source licence is applied. This copy was requested by the repository owner; public access does not grant third parties unrestricted redistribution rights. No newly supplied confidential manuscript, local user path, credential or private working directory is added.

