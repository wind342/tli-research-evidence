# Evidence-based scientific audit procedure for the current TLI paper

**Current manuscript:** [*Unified Dynamics of Training, Learning, and Inference in Neural Networks* (TLI)](https://github.com/wind342/tli-paper/tree/icml-final/submission/icml2027). This procedure also applies to the historical TLIR research archives when their distinct versions are identified.

**Evidence map:** [TLI_ICML_PAPER_EVIDENCE_MAP.md](TLI_ICML_PAPER_EVIDENCE_MAP.md)  
**Original documentation version:** 2026-10-25; current-paper alignment: 2026-11-20.

## 1. Reconstruct the research from its primary evidence

Record the manuscript's actual proposition, the relevant system and target, the registered experimental operation, measured quantity, numerical result and validation status. Keep experimental findings, interpretation, mathematical derivation and algorithm performance as distinguishable types of evidence.

The current paper follows this experimental and mathematical sequence:

1. **Eight nanoGPT experiments** (TL-E01–TL-E07 and INF-E01) establish the training, learning and frozen-inference relations. Realized updates, receiving states, target responses, distributed functional support, capability-readout boundaries and query-conditioned inference are measured through registered interventions.
2. **Prediction:** TL-P01 uses the established TLI relations to predict immediate target-boundary transitions using an already formed actual update and pre-response information. nanoGPT confirmation is **4,652/5,088 = 91.43%** accuracy and **91.49%** four-way macro recall.
3. **Five additional TLI systems:** ResNet-18, diffusion U-Net, Vision-MoE, GNN and hard-spiking SNN test the TLI relations with distinct architectures, tasks and optimizers. Together with nanoGPT, these are **six** TLI systems.
4. **Seventh system and feedback:** Shared GRU experiments RL-E05 and RL-E06 test concentrated correct feedback, functional-support changes, cross-skill erosion and recovery through feedback redistribution.
5. **Unified mathematical relationships:** The paper writes a coupled system from the experimentally established relations. Two complete recoveries appear in the ICML main text (**Edge of Stability**, **Catastrophic Forgetting**); the other **twelve** appear in the appendix. Each derivation identifies its starting TLI relation [T], original-study model and mathematical conditions [A], and recovered relation [R].

The experimental instruments are indexed in [EXPERIMENTAL_INSTRUMENTS.md](EXPERIMENTAL_INSTRUMENTS.md). The discovery sequence is recorded in [EXPERIMENT_INDEX.md](EXPERIMENT_INDEX.md).

## 2. Separate scientific operations and criteria

| Object | Audited quantity and evidence |
|---|---|
| Training action and receiving state | Exact formed update, matched receiver-state forks and optimizer-memory exchanges |
| Learning and functional support | Reversible component coalitions, persistent support allocation, target-boundary readout and version identity |
| Frozen inference | Query-conditioned component calls, complete-logit interactions, pre-formation component rollback and exact restoration |
| TL-P01 | Predicted post-update target correctness and four transition categories, after the actual update is formed |
| Cross-system tests | Per-system frozen criteria, per-seed outcomes, nonlinearity, support measures and boundary-prediction metrics |
| Feedback | Concentration dose, training duration, support profile, other-skill margins/accuracy and exact-state recovery forks |
| Mathematical recovery | Explicit [T]/[A]/[R] chain, equalities, approximations, original-source conditions and algebraic calculations |

A protocol-specific failure, model-specific prediction score and a verified structural relation are recorded under their corresponding experimental identities.

### Current ICML GNN and SNN numbers

These are the [November Windows experiment records](independent_stress_tests/windows_reproduction/README.md), with a [machine-readable summary](independent_stress_tests/windows_reproduction/WINDOWS_REPRODUCTION.json):

| System | Accuracy | Four-way macro recall | Structural criteria |
|---|---:|---:|---|
| GNN | **99.87%** (3,068/3,072) | **97.87%** | **8/9, 9/9, 8/9**; nonlinear counts **6/256, 36/256, 20/256** |
| Hard-spiking SNN | **93.24%** (6,713/7,200) | **60.05%** | **12/12** in all four seeds |

The GNN predictor meets the registered transport criterion. The SNN predictor's four-way macro recall falls below its **90%** registered threshold, while all four seeds satisfy the separate structural TLI tests. The [recorded independent checker](independent_stress_tests/windows_reproduction/round-1/table3/INDEPENDENT_CHECK_RESULT.json) reports **PASS**, 28 events and 10,272 target records. Earlier GNN/SNN experiments are retained in their historical source directories.

### RL-E05 and RL-E06

RL-E05's stronger registered temporal-precedence criterion has status **NOT_SUPPORTED**: **2/12** seeds satisfy the timing gate, with **10/11** composite gates passed. RL-E06 uses its separately frozen dose/duration/recovery design and reports all **12** formal seeds. Record each result with its own contract, checker and target outcome.

## 3. Evidence hierarchy and traceability

For every manuscript statement, record:

1. **Location and exact claim:** paper revision, section, figure/table/equation, target and measurement definition.
2. **Experimental authority:** frozen protocol, experiment ID, source program, model/optimizer checkpoint identities, target identity and result record.
3. **Observed result:** complete registered sample count, relevant metric, negative outcomes, seed-level variation and comparison against the stated criterion.
4. **Independent check:** validator, raw-recalculation result and source/hash authorities.
5. **Scientific effect:** the exact proposition supported or contradicted by the result.

Distinguish the evidence operation conducted:

- **Native rerun:** training/interventions executed from the protocol under a specified environment.
- **Recalculation:** results independently recomputed from saved machine-native records.
- **Archive verification:** identity, integrity and SHA-256 verified against stored records.

[PUBLIC_EVIDENCE_MATRIX.md](PUBLIC_EVIDENCE_MATRIX.md), [FULL_REPRODUCTION_AUDIT.md](audits/FULL_REPRODUCTION_AUDIT.md), [REPRODUCIBILITY_NOTES.md](audits/REPRODUCIBILITY_NOTES.md) and [source manifest](provenance/SOURCE_MANIFEST.md) identify the available verification depth. Record missing source authorities as unresolved observations with their file paths.

## 4. Scientific review and document editing

A scientific review report should contain: actual claims; evidence inspected; results supported by records; concrete discrepancies with file/line/field locations; and an assessment at the same level as the stated scientific proposition. Where the inspected material supplies no documented contradiction, report that observation directly.

For formatting work, preserve mathematical expressions, experimental sequence, numbers, figure content and scientific wording. For language editing, maintain the original proposition and specify any proposed substantive change. Use the current manuscript source and [TLI evidence map](TLI_ICML_PAPER_EVIDENCE_MAP.md) to control terminology and result versions.

