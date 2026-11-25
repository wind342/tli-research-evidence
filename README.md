# TLI research evidence

Evidence for *Unified Dynamics of Training, Learning, and Inference in Neural Networks*.

- **Paper:** [ICML 2027 submission PDF](https://github.com/wind342/tli-paper/blob/icml-final/submission/icml2027/TLI_ICML2027_Anonymous.pdf) · [LaTeX source](https://github.com/wind342/tli-paper/tree/icml-final/submission/icml2027)
- **Evidence navigation:** [paper-to-evidence map](TLI_ICML_PAPER_EVIDENCE_MAP.md) · [experiment index](EXPERIMENT_INDEX.md)
- **Complete downloads:** [GNN/SNN execution package and integrated nanoGPT supplement](https://github.com/wind342/tli-research-evidence/releases/tag/tli-execution-evidence-20261125)

## Evidence in paper order

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

## Download and reproduce

| Package | Contents | Entry point |
|---|---|---|
| GNN and SNN | Frozen run plan, model code, runtime versions, native training states, predictions and endpoint checks for the paper's November runs | [Results and execution](independent_stress_tests/windows_reproduction/README.md) · [ZIP download](https://github.com/wind342/tli-research-evidence/releases/download/tli-execution-evidence-20261125/TLI_GNN_SNN_Execution_Evidence.zip) |
| nanoGPT three-history supplement | Three 10,000-update histories, complete GFGs, checkpoints, interventions, response and support ledgers, frozen inference and boundary prediction | [Download, run, results and numbering](supplements/nanogpt/README.md) |

The execution packages connect the reported measurements with their captured
inputs, model programs and reproduction commands. The nanoGPT supplement is
distributed as one complete sequence. Its README maps the saved record
identifiers to the current paper.

The repository provides the programs, protocols and result records. The
release downloads also include the GNN/SNN native states and the nanoGPT
captures, checkpoints and shared dependencies. For the other experiments,
see the [evidence and reproduction matrix](PUBLIC_EVIDENCE_MATRIX.md) for
file availability and verification scope.

## Mathematical evidence and checks

- [Fourteen derivations](theory/TLI_THEORY_FIRST_14_DERIVATIONS.md) and [mathematical audit](audits/TLI_14_EXTRAPOLATIONS_MATH_AUDIT.md)
- [Runnable 21-check mathematical audit](math_audit/README.md)
- [Four experimental instruments](EXPERIMENTAL_INSTRUMENTS.md)
- [Repository integrity checker](tools/verify_tli_repository_integrity.py)

```sh
python -B tools/verify_tli_repository_integrity.py
```

This command checks navigation, required files and selected recorded values.
Experiment-specific reproduction commands are linked from the evidence map
and package READMEs.

This repository has no open-source license. See [PROPRIETARY_NOTICE.md](PROPRIETARY_NOTICE.md).
