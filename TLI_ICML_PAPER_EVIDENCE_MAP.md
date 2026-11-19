# TLI — ICML paper-to-evidence map

**Current manuscript:** [*Unified Dynamics of Training, Learning, and Inference in Neural Networks*](https://github.com/wind342/tli-paper/tree/icml-final/icml) (ICML-formatted manuscript; 8-page main text plus references, appendix, figures and declarations).

**Authority for ICML GNN/SNN numbers:** [Windows evidence](independent_stress_tests/windows_reproduction/README.md), [prediction metrics](independent_stress_tests/windows_reproduction/round-1/table3/ADJUDICATION_REPORT.json), and [checker receipt](independent_stress_tests/windows_reproduction/round-1/table3/INDEPENDENT_CHECK_RESULT.json). The November Windows runs establish the current paper's GNN/SNN evidence version. Earlier runs and the [PNAS map](TLIR_PNAS_PAPER_EVIDENCE_MAP_ARCHIVE.md) remain archived.

## ICML reading order

| Current ICML manuscript location | Experiment or evidence authority |
|---|---|
| [Introduction](https://github.com/wind342/tli-paper/blob/icml-final/icml/sections/intro.tex) | Questions motivating the nine core TLI experiments |
| [Experimental Methods and Findings: instruments](https://github.com/wind342/tli-paper/blob/icml-final/icml/sections/experiments_layout.tex) | [GFG and four reusable instruments](EXPERIMENTAL_INSTRUMENTS.md); frozen interventions and independently auditable results |
| Experimental section: training | TL-E01–TL-E05 (formation, receiver-state causal forks, finite-amplitude nonlinear responses, conditioning factors) |
| Experimental section: learning | TL-E06–TL-E08 (distributed support, persistent reallocation, target-boundary transitions) |
| Experimental section: inference | INF-E01 (13 histories, 52 checkpoints, query-conditioned support and exact learned-version rollback) |
| Experimental section: prediction | TL-P01; 4,652/5,088 = **91.43%**, four-transition macro recall **91.49%** |
| Experimental section: five additional TLI systems | ResNet, diffusion U-Net, Vision-MoE, GNN, hard-spiking SNN; see appendix **Table 2** (seven systems) and **Table 3** (six-system prediction results) |
| Experimental section: feedback | Seventh system, GRU RL-E05/06; distinct from the six complete TLI experimental chains |
| [Unified dynamical equations](https://github.com/wind342/tli-paper/blob/icml-final/icml/sections/dynamics_layout.tex) | Training action/state, functional response, support change, capability, frozen inference and feedback closure |
| [Mathematical unification](https://github.com/wind342/tli-paper/blob/icml-final/icml/sections/extrapolations_main_complete.tex) | Two complete main-text recoveries: **Edge of Stability** and **Catastrophic Forgetting**, tagged [T]/[A]/[R] |
| [This Is a Simple Theory](https://github.com/wind342/tli-paper/blob/icml-final/icml/sections/simple.tex) | Elementary neural-computation explanation of the coupled TLI relations |
| [Conclusion](https://github.com/wind342/tli-paper/blob/icml-final/icml/sections/conclusion.tex) | Synthesis of experiment-based TLI and mathematical unification |
| [Appendix: remaining 12 complete derivations](https://github.com/wind342/tli-paper/blob/icml-final/icml/sections/appendix_remaining_complete.tex) | All **14** derivations in total; organized full account and [independent mathematical audit](TLI_14_EXTRAPOLATIONS_MATH_AUDIT.md) |
| [Appendix experimental displays](https://github.com/wind342/tli-paper/blob/icml-final/icml/sections/appendix_floats.tex) | Figure 3 and Tables 1–3 |

**Document convention:** Section, figure, table and equation references follow the `icml-final` manuscript. Experiment identities remain stable across versions; the November Windows GNN/SNN runs have distinct registered seeds.

## Confirmed ICML GNN and SNN results

| System | Predictor correct/targets | Accuracy | Four-way macro recall | Structural criteria |
|---|---:|---:|---:|---|
| GNN | **3,068 / 3,072** | **99.87%** | **97.87%** | **8/9, 9/9, 8/9**; nonlinear counts **6/256, 36/256, 20/256** |
| Hard-spiking SNN | **6,713 / 7,200** | **93.24%** | **60.05%** | **12/12** in four seeds |

The GNN predictor meets its recorded transport criterion. The hard-spiking SNN predictor does **not** meet the recorded 90% four-way recall criterion, even though its 12/12 structural TLI checks passed in all four seeds. Source: [machine summary](independent_stress_tests/windows_reproduction/WINDOWS_REPRODUCTION.json) and [checker receipt](independent_stress_tests/windows_reproduction/round-1/table3/INDEPENDENT_CHECK_RESULT.json).

## 1. Introduction (ICML manuscript)

The introduction motivates the experimentally established TLI relations. The [experiment index](EXPERIMENT_INDEX.md) and [four-instrument index](EXPERIMENTAL_INSTRUMENTS.md) give their evidence authorities.

## 2. Core TLI experiments (ICML Experimental Methods and Findings)

### 2.1 Training: realized updates and receiving states

| Experiment | Question / evidence | Protocol and execution | Results / checks |
|---|---|---|---|
| TL-E01 | Insufficiency of familiar observables; formation, decline and recovery | [Contracts](experiments/gfg_nanogpt_autonomous_capability_discovery_v1/contracts/) | [Theory ledger](experiments/gfg_nanogpt_autonomous_capability_discovery_v1/research_archive/THEORY_LEDGER.md), [public summary](experiments/gfg_nanogpt_autonomous_capability_discovery_v1/reports/public_summary.json) |
| TL-E02 | Pausing parameter–optimizer evolution delays formation; clipping control | [Intervention contract](experiments/gfg_nanogpt_autonomous_capability_discovery_v1/contracts/intervention_api.json), [checkpoint forks](experiments/gfg_nanogpt_autonomous_capability_discovery_v1/checkpoint_fork.py) | [Archived executions and causal evaluations](experiments/gfg_nanogpt_autonomous_capability_discovery_v1/research_archive/entries/) |
| TL-E03 | Same formed update, different receiving states; separate optimizer-memory exchanges | [Reciprocal protocol](experiments/gfg_nanogpt_stepwise_support_transition_v1/RECIPROCAL_MATCHED_PAIR_PROTOCOL_V2.json), [P2 local response](experiments/gfg_nanogpt_stepwise_support_transition_v1/P2_RECIPROCAL_LOCAL_RESPONSE_PROTOCOL.json), [optimizer exchange](experiments/gfg_nanogpt_stepwise_support_transition_v1/H20_RECIPROCAL_OPTIMIZER_EXCHANGE_PROTOCOL.json) | [Reciprocal validator](experiments/gfg_nanogpt_stepwise_support_transition_v1/reciprocal_validator.py), [independent replay](experiments/gfg_nanogpt_stepwise_support_transition_v1/independent_replay_validator.py) |
| TL-E04 | Finite-amplitude response paths, including nonlinear morphologies | [Amplitude-path protocol](experiments/gfg_nanogpt_stepwise_support_transition_v1/B_UPDATE_AMPLITUDE_PATH_PROTOCOL.json) | [Path validator](experiments/gfg_nanogpt_stepwise_support_transition_v1/amplitude_path_validator.py), [GFG validator](experiments/gfg_nanogpt_stepwise_support_transition_v1/amplitude_path_gfg_validator.py) |
| TL-E05 | Seven frozen conditioning-factor blocks across 12 development runs, 72 finite-amplitude sections and 15,264 identity-aligned target responses; F1 target boundary, F3 target-update geometry and F5 receiving state identified as primary families | [Frozen contract](experiments/gfg_nanogpt_response_factor_analysis_v1/FACTOR_ANALYSIS_CONTRACT.md), [analysis and cross-run matching](experiments/gfg_nanogpt_response_factor_analysis_v1/analysis.py), [2,000 clustered-bootstrap resamples and factor-order/leave-one-out tests](experiments/gfg_nanogpt_response_factor_analysis_v1/runner.py) | [Independent validator](experiments/gfg_nanogpt_response_factor_analysis_v1/validator.py); [public verification record](PUBLIC_EVIDENCE_MATRIX.md) |

### 2.2 Learning: distributed support and capability boundaries

| Experiment | Question / evidence | Protocol / code / checker |
|---|---|---|
| TL-E06 | Distributed necessity, backup, substitution, synergy and failure slack | [CSRG-4C experiment](experiments/gfg_nanogpt_support_redundancy_v1/README.md), [capture contract](experiments/gfg_nanogpt_support_redundancy_v1/capture_contract_v2.json), [archive verifier](experiments/gfg_nanogpt_support_redundancy_v1/verify_archive.py) |
| TL-E07 | Actual updates reorganize support: 72 sections, 1,656 transitions, 1,636 defined allocations, 228 handoffs | [Scope](experiments/gfg_nanogpt_support_reallocation_audit_v1/ANALYSIS_SCOPE.md), [analysis](experiments/gfg_nanogpt_support_reallocation_audit_v1/analysis.py), [checker](experiments/gfg_nanogpt_support_reallocation_audit_v1/INDEPENDENT_CHECKER.py) |
| TL-E08 | Identity-aligned measured margins cross target readout boundaries | [Ledger construction](experiments/gfg_nanogpt_identity_aligned_margin_crossing_v1/experiment.py), [15,264-row ledger checking](experiments/gfg_nanogpt_actual_update_boundary_v1/INDEPENDENT_CHECKER.py) |

Undefined allocations are not zero support. TL-E08's measured endpoint facts are distinct from TL-P01's predictions, even when the archived ledger supports both analyses.

### 2.3 Inference: frozen recruitment of learned support

**INF-E01:** 13 nanoGPT histories, 52 historical checkpoint comparisons; target/query-conditioned recruitment, non-additive combinations, exact learned-version rollback and restoration.

- [Frozen protocol](experiments/gfg_nanogpt_training_learning_inference_projection_v1/PROTOCOL_FREEZE.md)
- [Analysis](experiments/gfg_nanogpt_training_learning_inference_projection_v1/analysis.py)
- [Independent checker](experiments/gfg_nanogpt_training_learning_inference_projection_v1/independent.py), [strict audit](experiments/gfg_nanogpt_training_learning_inference_projection_v1/strict_audit.py)
- [Public evidence boundary](experiments/gfg_nanogpt_training_learning_inference_projection_v1/PUBLIC_EVIDENCE.md)

## 3. Prediction and cross-system validation (ICML experimental section and appendix)

### 3.1 Prediction derived from TL-E05

**TL-P01:** [protocol](experiments/gfg_nanogpt_actual_update_boundary_v1/PROTOCOL_FREEZE.md), [results](experiments/gfg_nanogpt_actual_update_boundary_v1/RESULTS.md), [analysis](experiments/gfg_nanogpt_actual_update_boundary_v1/analysis.py), [independent checker](experiments/gfg_nanogpt_actual_update_boundary_v1/INDEPENDENT_CHECKER.py).

Confirmation: **4,652/5,088 = 91.43% accuracy; 91.49% four-transition macro recall**. The 92.17% confirmation balanced accuracy is a different metric. The all-run total is 14,069/15,264 with 91.30% four-transition macro recall.

The direct TL-P01 algorithm computes target-boundary outcomes from an already formed update and pre-response internal quantities. Separate coordinate-transport analyses evaluate KNN models.

### 3.2 Six TLI systems

**ICML appendix Table 2** lists all seven systems: these six TLI chains plus the separate GRU feedback-closure study.

| System | Identity | Protocol / code | Results / check |
|---|---|---|---|
| nanoGPT / Adam | TL-E01–08, INF-E01, TL-P01 | Sections 2 and 3.1 above | Original frozen release and Zenodo archive |
| ResNet-18 / CIFAR-100 / SGD momentum | TL-G01; inference also INF-G01 | [Protocol](experiments/gfg_resnet_cifar_training_learning_generalization_v1/PROTOCOL_FREEZE.md), [implementation](experiments/gfg_resnet_cifar_training_learning_generalization_v1/) | [Results](experiments/gfg_resnet_cifar_training_learning_generalization_v1/RESULTS.md), [checker](experiments/gfg_resnet_cifar_training_learning_generalization_v1/INDEPENDENT_CHECKER.py) |
| Diffusion U-Net / CIFAR-10 / AdamW | TL-G02; inference also INF-G01 | [Protocol](experiments/gfg_ddpm_cifar_training_learning_generalization_v1/PROTOCOL_FREEZE.md), [implementation](experiments/gfg_ddpm_cifar_training_learning_generalization_v1/) | [Results](experiments/gfg_ddpm_cifar_training_learning_generalization_v1/RESULTS.md), [checker](experiments/gfg_ddpm_cifar_training_learning_generalization_v1/INDEPENDENT_CHECKER.py) |
| Vision-MoE / CIFAR-100 / AdamW | **TL-G03 / INF-G02** | [Protocol](experiments/gfg_moe_cifar_training_learning_inference_generalization_v1/PROTOCOL_FREEZE.md), [model contract](experiments/gfg_moe_cifar_training_learning_inference_generalization_v1/MODEL_CONTRACT.json), [model](experiments/gfg_moe_cifar_training_learning_inference_generalization_v1/model.py), [runner](experiments/gfg_moe_cifar_training_learning_inference_generalization_v1/runner.py) | [Results](experiments/gfg_moe_cifar_training_learning_inference_generalization_v1/RESULTS.md), [machine results](experiments/gfg_moe_cifar_training_learning_inference_generalization_v1/FORMAL_RESULTS.json), [checker](experiments/gfg_moe_cifar_training_learning_inference_generalization_v1/INDEPENDENT_CHECKER.py), [historical check receipt](experiments/gfg_moe_cifar_training_learning_inference_generalization_v1/INDEPENDENT_CHECK_RESULT.json) |
| GNN / graph reachability / RMSprop | Independent TLI stress test | [Original protocol and native code](independent_stress_tests/gnn/) | [ICML machine result](independent_stress_tests/windows_reproduction/round-1/gnn_tlir_formal_results.json), [Windows summary](independent_stress_tests/windows_reproduction/WINDOWS_REPRODUCTION.json); historical native data retained under `independent_stress_tests/gnn/` |
| Hard-spiking SNN / digits / Adagrad | Independent TLI stress test | [Original protocol and native code](independent_stress_tests/snn/) | [ICML machine result](independent_stress_tests/windows_reproduction/round-1/SNN_TLIR_formal/FORMAL_SUMMARY.json), [Windows summary](independent_stress_tests/windows_reproduction/WINDOWS_REPRODUCTION.json); historical native data retained under `independent_stress_tests/snn/` |

ResNet and diffusion inference are separately documented in **INF-G01**: [protocol](experiments/gfg_cross_system_frozen_inference_projection_v1/PROTOCOL_FREEZE.md), [results](experiments/gfg_cross_system_frozen_inference_projection_v1/RESULTS.md), [checker](experiments/gfg_cross_system_frozen_inference_projection_v1/INDEPENDENT_CHECKER.py).

The **MoE formal experiment package** includes its protocol, source, machine results and checker. All three formal seeds (20260910–12) passed the registered joint verdict. Its routed forward uses deterministic top-2 selection among four experts; all expert branches execute and nonselected weights are zero. The [scientific assessment](experiments/gfg_moe_cifar_training_learning_inference_generalization_v1/SCIENTIFIC_ASSESSMENT.md) documents the test, and the [runtime manifest](experiments/gfg_moe_cifar_training_learning_inference_generalization_v1/FORMAL_RUNTIME_MANIFEST.json) identifies externally archived runtime objects.

In the **ICML GNN Windows run**, seeds 202611801–202611803 produced **6/256, 36/256 and 20/256** nonlinear responses and passed **8/9, 9/9 and 8/9** structural criteria. ICML SNN Windows seeds 71101–71104 passed **12/12** each. The [Windows evidence](independent_stress_tests/windows_reproduction/) has the current-machine results, and the earlier GNN/SNN tests are historical. These independent stress tests used PyTorch-native records and their own component intervention designs; see [experimental scope](independent_stress_tests/EVIDENCE_SCOPE.md).

### Table 3: post-update target-boundary classification

| System | Accuracy (%) | Four-way macro recall (%) | Source |
|---|---:|---:|---|
| nanoGPT | 91.43 | 91.49 | TL-P01 confirmation |
| ResNet | 99.28 | 97.99 | TL-G01 direct second-order predictor |
| Diffusion | 99.60 | 97.98 | TL-G02 direct second-order predictor |
| MoE | 99.63 | 96.95 | TL-G03 direct second-order predictor |
| GNN | 99.87 | 97.87 | [ICML Windows prediction record](independent_stress_tests/windows_reproduction/round-1/table3/ADJUDICATION_REPORT.json), 3,068/3,072 |
| Hard-spiking SNN | 93.24 | 60.05 | [ICML Windows prediction record](independent_stress_tests/windows_reproduction/round-1/table3/ADJUDICATION_REPORT.json), 6,713/7,200; prediction criterion NOT_SUPPORTED |

**GNN/SNN ICML prediction authorities:** [Windows overview](independent_stress_tests/windows_reproduction/README.md), [machine prediction metrics](independent_stress_tests/windows_reproduction/round-1/table3/ADJUDICATION_REPORT.json), and [independent checker receipt](independent_stress_tests/windows_reproduction/round-1/table3/INDEPENDENT_CHECK_RESULT.json). The prior checker reported `PASS` across **28 events and 10,272 target records**. The [earlier TL-P01 transport record](independent_stress_tests/tlp01_prediction/REPORT.md) documents a separate historical experiment.

## 4. Feedback allocation experiments in the shared GRU (ICML experimental section)

| Experiment | Scope | Protocol | Results / checker |
|---|---|---|---|
| RL-E05 | Selective correct feedback, support concentration, cross-skill interference, component-version rollback | [Protocol](experiments/gfg_rl_selective_positive_feedback_support_concentration_v1/PROTOCOL_FREEZE.md) | [Results](experiments/gfg_rl_selective_positive_feedback_support_concentration_v1/RESULTS.md), [assessment](experiments/gfg_rl_selective_positive_feedback_support_concentration_v1/SCIENTIFIC_ASSESSMENT.md), [checker](experiments/gfg_rl_selective_positive_feedback_support_concentration_v1/independent_checker.py) |
| RL-E06 | Fixed dose/duration and matched update-800 recovery forks | [Protocol](experiments/gfg_rl_selective_positive_feedback_dose_recovery_v1/PROTOCOL_FREEZE.md) | [Results](experiments/gfg_rl_selective_positive_feedback_dose_recovery_v1/RESULTS.md), [checker](experiments/gfg_rl_selective_positive_feedback_dose_recovery_v1/independent_checker.py) |

RL-E05 records **NOT_SUPPORTED** on its stronger temporal-precedence criterion (2/12 seeds; 10/11 composite gates passed) alongside its other measured intervention results.

RL-E06 retains all 12 seeds. The update-800 other-skill accuracy is 70.31%; rebalanced recovery reaches 99.48%, preserving skill 0 at 100%. Others-only repair reaches 99.83% but skill 0 falls to 89.06%.

**RL-E06 feedback allocation (ICML experimental narrative):** 60 episodes per update: balanced 15/15/15/15, mild 30/10/10/10, high 45/5/5/5, exclusive 60/0/0/0.

## 5. Unified equations and mathematical unification (ICML)

The ICML paper separates the [coupled dynamical equations](https://github.com/wind342/tli-paper/blob/icml-final/icml/sections/dynamics_layout.tex) from the [14 mathematical recoveries](TLI_THEORY_FIRST_14_DERIVATIONS.md). The main-text worked derivations are **Edge of Stability** (`icml/sections/extrap_cases/eos.tex`) and **Catastrophic Forgetting** (`icml/sections/extrap_cases/forgetting.tex`). The remaining **12** appear in the [appendix source](https://github.com/wind342/tli-paper/blob/icml-final/icml/sections/appendix_remaining_complete.tex): implicit bias, model collapse, spectral bias, benign overfitting, Chinchilla, dynamical isometry, dropout, grokking, μP, SAM/sharpness, gradient noise scale and double descent.

The complete source-oriented ledger remains in [14 theory-first derivations](TLI_THEORY_FIRST_14_DERIVATIONS.md), [21 historical positive/contrasting comparisons](TLI_HISTORICAL_COMPARISONS_21.md), the [combined original record](TLI_SECTION5_21_PAIRS_14_EXTRAPOLATIONS.md), and [14-item mathematical audit](TLI_14_EXTRAPOLATIONS_MATH_AUDIT.md). The historical 21-case research record is **supplementary**, not an assertion that all 21 appear in the current ICML main text.

## 6. ICML figures and appendix tables

| ICML item | Manuscript source | Evidence scope |
|---|---|---|
| **Figure 1** | [TLI core with feedback](https://github.com/wind342/tli-paper/blob/icml-final/icml/figures/fig1_tli_core_feedback.pdf) | Conceptual TLI and feedback schematic |
| **Figure 2** | [Experimental evidence](https://github.com/wind342/tli-paper/blob/icml-final/icml/figures/fig2_experimental_evidence.pdf) | 14 panels covering training, learning, inference and RL feedback; panel-by-panel map below |
| **Figure 3** | [Six-system TLI experiment chains](https://github.com/wind342/tli-paper/blob/icml-final/icml/figures/fig3_cross_system.pdf) | Two GNN seeds 8/9, one 9/9; four SNN seeds 12/12; detailed numerical authorities above |
| **Table 1 (appendix)** | [Experimental relations](https://github.com/wind342/tli-paper/blob/icml-final/icml/sections/appendix_floats.tex) | Nine experimental relations and their variables (labels `eq:exp1`–`eq:exp9`) |
| **Table 2 (appendix)** | [Seven systems](https://github.com/wind342/tli-paper/blob/icml-final/icml/sections/appendix_floats.tex) | Six TLI system chains plus the GRU feedback system |
| **Table 3 (appendix)** | [Boundary prediction](https://github.com/wind342/tli-paper/blob/icml-final/icml/sections/appendix_floats.tex) | Immediate post-update target-boundary accuracy and four-way macro recall; GNN/SNN numbers from the November Windows record |

**Figure 2 individual panels:**

| Panel | Evidence identity | What the plotted measurement means |
|---|---|---|
| a1 | TL-E02 | Formation steps of 11 pause pairs and one clipping control |
| a2 | TL-E03 P2 | Receiver-conditioned q10 response at alpha=0.125 |
| a3 | TL-E04 | Five measured finite-amplitude response morphologies normalized by their maximum absolute displacement |
| a4 | TL-E05 | F1/F3/F5 conditioning contrasts with 95% intervals |
| b1 | TL-E06 measurements retained in TL-E07 | Single/pair component-gating effects on the group-q10 failure boundary |
| b2 | TL-E07 | Measured before/after component-support handoff |
| b3 | TL-E08 | All 15,264 measured pre/post margins |
| c1 | INF-E01 | 23 target-group profiles: q10(full) minus q10(single gate) |
| c2 | INF-E01 | q10(full) minus both single-gate q10s plus joint-gate q10; zero means additive for this readout |
| c3 | INF-E01 | 52 historical-component rollback/restoration comparisons; exact restoration |
| d1–d2 | RL-E06 | Feedback dose, relative support share and other-skill margins across 12 seeds |
| d3 | RL-E05 | 168 proper-subset component rollbacks (14 × 12) |
| d4 | RL-E06 | Common update-800 state, continued exclusive feedback versus two recovery allocations |

Figure 3 summarizes the six-system experiment chains. The [November Windows records](independent_stress_tests/windows_reproduction/README.md) provide the ICML GNN/SNN numerical results; the earlier [GNN](independent_stress_tests/gnn/) and [SNN](independent_stress_tests/snn/) records remain archived.

## 7. Audit and availability

- [Frozen experiment index](EXPERIMENT_INDEX.md), [four instruments](EXPERIMENTAL_INSTRUMENTS.md), [public evidence boundaries](PUBLIC_EVIDENCE_MATRIX.md) and [original import authority](EVIDENCE_IMPORT.md)
- [Current ICML GNN/SNN machine results](independent_stress_tests/windows_reproduction/WINDOWS_REPRODUCTION.json) and [prediction checker receipt](independent_stress_tests/windows_reproduction/round-1/table3/INDEPENDENT_CHECK_RESULT.json); the receipt reports `PASS` for 28 events and 10,272 targets
- [RL-E05 scientific assessment](experiments/gfg_rl_selective_positive_feedback_support_concentration_v1/SCIENTIFIC_ASSESSMENT.md) retains its stronger temporal-precedence criterion as `NOT_SUPPORTED`; [RL-E06 formal results](experiments/gfg_rl_selective_positive_feedback_dose_recovery_v1/RESULTS.md) retain all twelve seeds
- [Historical PNAS-format map](TLIR_PNAS_PAPER_EVIDENCE_MAP_ARCHIVE.md) and [historical Science map](TLIR_SCIENCE_23PAGE_EVIDENCE_MAP_ARCHIVE.md) remain available for tracing older manuscripts
- [Original source and imported evidence archive](PUBLIC_ARCHIVE.md); [ICML manuscript sources](https://github.com/wind342/tli-paper/tree/icml-final/icml)

The Git repository contains programs, frozen protocols, machine summaries and checkers. The [public evidence matrix](PUBLIC_EVIDENCE_MATRIX.md) documents verification scope by experiment. This documentation revision reused the existing checks and experiment records.
