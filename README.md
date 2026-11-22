# TLI research evidence — current ICML manuscript

This repository accompanies the current **TLI paper**, [*Unified Dynamics of Training, Learning, and Inference in Neural Networks*](https://github.com/wind342/tli-paper/tree/icml-final/icml). Frozen experimental identifiers and historical schema strings are preserved for provenance; active GNN/SNN artifact filenames use TLI.

**Start with the [TLI/ICML paper-to-evidence map](TLI_ICML_PAPER_EVIDENCE_MAP.md)**, organized around the current `icml-final` manuscript sections, figures and appendix tables. The [compiled paper](https://github.com/wind342/tli-paper/blob/icml-final/icml/TLI_ICML_Manuscript.pdf) is hosted alongside its LaTeX source.

Experiment identifiers follow the current manuscript and [experiment index](EXPERIMENT_INDEX.md). Historical releases remain available in Git history.

| In ICML paper order | Frozen experimental evidence |
|---|---|
| Training and receiving-state interventions | [TL-E01–TL-E04](TLI_ICML_PAPER_EVIDENCE_MAP.md#21-training-realized-updates-and-receiving-states) |
| Learning, support reallocation and capability | [TL-E05–TL-E07](TLI_ICML_PAPER_EVIDENCE_MAP.md#22-learning-distributed-support-and-capability-boundaries) |
| Frozen inference | [INF-E01](TLI_ICML_PAPER_EVIDENCE_MAP.md#23-inference-frozen-recruitment-of-learned-support) |
| Theory-derived target-boundary predictor | [TL-P01](TLI_ICML_PAPER_EVIDENCE_MAP.md#31-theory-derived-target-boundary-prediction) |
| Five additional TLI systems | [ResNet, diffusion, MoE, GNN, SNN](TLI_ICML_PAPER_EVIDENCE_MAP.md#32-six-tli-systems) |
| Seventh system: GRU feedback | [RL-E05/RL-E06](TLI_ICML_PAPER_EVIDENCE_MAP.md#4-feedback-allocation-experiments-in-the-shared-gru-icml-experimental-section) |
| Unified equations, simple theory and 14 mathematical derivations | [ICML mathematical map](TLI_ICML_PAPER_EVIDENCE_MAP.md#5-unified-equations-and-mathematical-unification-icml) |
| Figures 1–3 and appendix Tables 1–3 | [Figure/panel and table evidence map](TLI_ICML_PAPER_EVIDENCE_MAP.md#6-icml-figures-and-appendix-tables) |

## ICML GNN and SNN evidence authority

The corresponding **GNN/SNN** evidence is the [Windows-run machine results and audit records](independent_stress_tests/windows_reproduction/), now in this default branch:

| System | Correct / targets | Prediction accuracy | Four-way macro recall | Structural checks |
|---|---:|---:|---:|---|
| **GNN** | 3,068 / 3,072 | **99.87%** | **97.87%** | 8/9, 9/9, 8/9; nonlinear counts 6/256, 36/256, 20/256 |
| **Hard-spiking SNN** | 6,713 / 7,200 | **93.24%** | **60.05%** | 12/12 in all four seeds |

[Independent prediction audit receipt](independent_stress_tests/windows_reproduction/round-1/table3/INDEPENDENT_CHECK_RESULT.json): `PASS`, 28 events and 10,272 target records. The figures match ICML appendix Table 3. The GNN predictor met its registered criterion; the SNN predictor's **60.05%** four-way macro recall fell below its prediction threshold, while all four SNN seeds passed the **12/12 structural TLI criteria**. Earlier experiment versions remain archived. The November GNN/SNN result directory includes machine summaries and an independent prediction-check receipt; it does not include the exact November native execution programs or frozen source/protocol files. The adjacent October programs belong to different registered seeds. See the [current-result provenance note](independent_stress_tests/windows_reproduction/README.md).

## Mathematical and historical materials

- The current ICML paper presents two worked mathematical recoveries in the main text (**Edge of Stability, Catastrophic Forgetting**) and twelve further complete recoveries in the appendix, all linked from the [ICML map](TLI_ICML_PAPER_EVIDENCE_MAP.md).
- [Run and inspect the current 21-check mathematical audit](math_audit/README.md) (script, fixed inputs, versioned dependencies, and result records).
- The [complete 14-derivation record](theory/TLI_THEORY_FIRST_14_DERIVATIONS.md), [21 historical positive/contrasting explanations](theory/TLI_HISTORICAL_COMPARISONS_21.md) and [independent mathematical audit](audits/TLI_14_EXTRAPOLATIONS_MATH_AUDIT.md) are supporting TLI research documents. Their equation references and terminology were aligned with the current ICML manuscript on November 20, 2026.
- [Verification levels](PUBLIC_EVIDENCE_MATRIX.md), [import provenance](provenance/EVIDENCE_IMPORT.md), and [source manifest](provenance/SOURCE_MANIFEST.md) record experiment authority and audit scope. Historical receipts retain their original verification dates and scope.
- [Current-tree integrity checker](tools/verify_tli_repository_integrity.py) checks active links, required scientific records, selected reported values and directory layout without rerunning the experiments.

## Document organization

- [Theory and fourteen derivations](theory/) — TLI equations, mathematical recoveries and historical comparisons
- [Audit reports](audits/) — mathematical and experimental verification and reproduction notes
- [Evidence provenance](provenance/) — imported-source identities, manifests and external file hashes
- [Experiment chains and current abstract](docs/) — cross-system and reinforcement evidence navigation
- [Exploratory research notes](research_notes/) — unfinished hypotheses and calculations

The original [letter to future AI](LETTER_TO_FUTURE_AI.md) stays in the repository root. The superseded `PUBLIC_ARCHIVE.md` evidence-package listing has been removed; the experiment data and recorded source identities are unchanged.

## Original research-evidence collection (preserved)

The preserved original release collected executable experiments used to
establish and test the generation-fact, training–learning, inference and
reinforcement-learning claims across historical manuscripts.

The current index contains **15 primary experiment entries**:

- two structural projection experiments;
- seven experiments forming the training–learning theory;
- one direct prediction experiment;
- one frozen-inference projection experiment; and
- four reinforcement-learning experiments spanning feedback closure,
  long-delay credit discovery, recursive optimization of credit discovery and
  stochastic long-chain credit.

The primary entries are indexed in [EXPERIMENT_INDEX.md](EXPERIMENT_INDEX.md).
The verification scope for every indexed experiment is recorded in
[PUBLIC_EVIDENCE_MATRIX.md](PUBLIC_EVIDENCE_MATRIX.md).
The four reinforcement-learning experiments form one cumulative evidence chain,
summarized in [RL_EVIDENCE_CHAIN.md](docs/RL_EVIDENCE_CHAIN.md).
Additional experiment directories support primary entries or reconstruct
the underlying Generation-Fact Graph
(GFG). These directories provide experimental dependencies.

The index also exposes **GF-S01**, a four-stage real-signal experiment showing
that the generation-fact and GFG structures remain fixed while their concrete
domain semantics change across filtering, downsampling, Fourier analysis and
SVG rendering.

The separate **TL-G01** cross-system falsification experiment changes
architecture, modality, task and optimizer from nanoGPT/text/Adam to
ResNet-18/CIFAR-100/SGD momentum and retests the primary training--learning
relations under a frozen protocol. It is a separately registered extension
to the sealed original experiment set.

The separate **TL-G02** experiment moves the same falsification programme to a
generative diffusion objective: a time-conditioned U-Net predicts identified
noise occurrences on CIFAR-10 under AdamW. It retests receiving-state
conditioning, nonlinear response, distributed support and held-out coordinate
transport with a non-classification readout boundary.

The separate **INF-G01** experiment then retests the frozen-inference projection
relation in both cross-system models. Across three ResNet seeds and three
diffusion seeds, it checks exact training-version identity, causal component
recruitment, query-conditioned non-additive support combination and exact
pre-learning rollback/restoration while keeping persistent learned state frozen.
The cumulative relation among TL-G01, TL-G02 and INF-G01 is summarized in
[CROSS_SYSTEM_EVIDENCE_CHAIN.md](docs/CROSS_SYSTEM_EVIDENCE_CHAIN.md).

The separate **TL-G03/INF-G02** frozen experiment adds deterministic top-2
routed expert organization. Across three Vision-MoE/CIFAR-100/AdamW seeds, it
retests receiving-state conditioning, nonlinear response, expert-support
reorganization, routing, prospective coordinate transport and exact frozen-
inference expert/router rollback. Its result, independent check and bounded
scientific assessment are retained in
[the MoE experiment directory](experiments/gfg_moe_cifar_training_learning_inference_generalization_v1/).

Two later feedback-dynamics experiments test a bounded consequence of the
training--learning--inference loop in a shared policy. RL-E05 studies selective
positive feedback and support concentration; RL-E06 freezes feedback dose,
duration and recovery forks and independently re-executes all 12 formal seeds.
They are indexed as extensions to the primary experiment collection. See [RL_EVIDENCE_CHAIN.md](docs/RL_EVIDENCE_CHAIN.md).

Four reusable instruments developed for the training--learning experiments are
exposed through [EXPERIMENTAL_INSTRUMENTS.md](EXPERIMENTAL_INSTRUMENTS.md):
CSRG-4C, realized-update causal forks, finite-amplitude update paths and the
identity-aligned target-boundary ledger. The index points directly to their
canonical code, frozen contracts and validators.

## Structural basis

The two added structural experiments are:

1. **GF-P01 — five mature mechanisms as exact strict projections:** database
   which-lineage, ECMA-426 Source Maps, OpenTelemetry, W3C PROV and PyTorch
   Autograd.
2. **GF-P02 — classical provenance semiring projection:** exact strict
   projection to canonical `N[X]`, followed by the frozen algebraic and task
   projections specified by the experiment.

## Repository provenance

The original experiment set and RL-E02 were imported without rewriting their
experimental content from frozen source commits. RL-E03 and RL-E04 were then
developed and frozen directly in this companion repository. Exact source
commits and Git tree identities are recorded in
[SOURCE_MANIFEST.md](provenance/SOURCE_MANIFEST.md).

Four large base-GFG JSON payloads are intentionally not added to this companion
repository. Their byte sizes and SHA-256 identities are recorded in
[EXTERNAL_ARTIFACTS.md](provenance/EXTERNAL_ARTIFACTS.md); their generators, validation
outputs and source-commit identities remain present.

## Reproduction

Each primary experiment retains its frozen protocol, implementation, machine
results, negative controls and independent checker where those objects existed
in the source experiment. External payload identities and verification boundaries are recorded in
[provenance](provenance/EXTERNAL_ARTIFACTS.md) and the [evidence matrix](PUBLIC_EVIDENCE_MATRIX.md).
Historical archive records and superseded package-building scripts remain available through Git history. Reproduction commands
and the distinction between result recomputation and full native re-execution
are documented in `PUBLIC_EVIDENCE_MATRIX.md`. The common Python package and
Core v3 schemas are retained under `src/` and `protocol/core_v3/`.

Environment-dependent and source-history-dependent checks are identified in
[REPRODUCIBILITY_NOTES.md](audits/REPRODUCIBILITY_NOTES.md).
The final pre-publication experiment-by-experiment audit is recorded in
[FULL_REPRODUCTION_AUDIT.md](audits/FULL_REPRODUCTION_AUDIT.md).
The single cumulative cross-system and feedback-dynamics freeze is described in
[FINAL_EXTENSION_RELEASE_AUDIT.md](audits/FINAL_EXTENSION_RELEASE_AUDIT.md); its validation script is `tools/verify_final_extension_evidence.py`.

This repository has no open-source license. See
[PROPRIETARY_NOTICE.md](PROPRIETARY_NOTICE.md).

Two third-party provenance papers used as frozen audit authorities in GF-P02
are intentionally not redistributed in this public snapshot. Their citations,
DOIs and audited file hashes are preserved in
[THIRD_PARTY_AUTHORITIES.md](provenance/THIRD_PARTY_AUTHORITIES.md).
