# Current TLI experiment index

The index follows the ICML 2027 submission. The [paper-to-evidence map](TLI_ICML_PAPER_EVIDENCE_MAP.md)
links its sections, figures and tables to protocols, results and checkers.

## Eight core nanoGPT experiments

| ID | Experiment | Main scientific role | Code, protocol and evidence |
|---|---|---|---|
| TL-E01 | Cross-run state sufficiency and post-formation trajectory audit | Falsifies loss, accuracy, absolute step, a single margin and LayerNorm gain as sufficient states; establishes post-formation decline and recovery as phenomena requiring explanation. | [theory and counterexample ledger](experiments/gfg_nanogpt_autonomous_capability_discovery_v1/research_archive/THEORY_LEDGER.md) |
| TL-E02 | Optimizer pauses and clipping negative controls | Tests whether effective parameter–optimizer evolution, rather than a superficial clipping change, moves capability-formation time. | [intervention experiment](experiments/gfg_nanogpt_autonomous_capability_discovery_v1/) |
| TL-E03 | Full/skip, receiving-state exchange and reciprocal response | Establishes that the same realized update produces different functional responses in different receiving states. | [stepwise causal experiment](experiments/gfg_nanogpt_stepwise_support_transition_v1/) |
| TL-E04 | Multi-amplitude realized-update paths | Falsifies a globally fixed linear or quadratic local extrapolation and establishes finite-amplitude nonlinear functional response. | [frozen amplitude-path protocol](experiments/gfg_nanogpt_stepwise_support_transition_v1/B_UPDATE_AMPLITUDE_PATH_PROTOCOL.json) |
| TL-E05 | CSRG single- and paired-component gating | Establishes distributed functional support, including necessity, substitution, backup, synergy and failure slack. | [CSRG experiment](experiments/gfg_nanogpt_support_redundancy_v1/) |
| TL-E06 | Support reallocation across an actual update | Measures persistent reorganization and support hand-off caused by realized training updates. | [support-reallocation experiment](experiments/gfg_nanogpt_support_reallocation_audit_v1/) |
| TL-E07 | Identity-aligned target margins and readout crossings | Connects internal change to the four observable target transitions through the target-specific readout boundary. | [identity-aligned boundary experiment](experiments/gfg_nanogpt_identity_aligned_margin_crossing_v1/) |
| INF-E01 | Frozen-inference projection | Tests exact learned-version use, causal support recruitment, query conditioning, non-additive combination and rollback dependence under frozen inference. | [inference experiment](experiments/gfg_nanogpt_training_learning_inference_projection_v1/) |

## Target-boundary prediction

| ID | Experiment | Main scientific role | Code, protocol and evidence |
|---|---|---|---|
| TL-P01 | Actual-update target-boundary prediction | Tests the TLI-derived prediction of immediate target-boundary outcomes from the pre-update state and the realized update, before post-update target outputs are read. | [prediction experiment](experiments/gfg_nanogpt_actual_update_boundary_v1/) |

## Five additional TLI systems

| ID | Experiment | Main scientific role | Code, protocol and evidence |
|---|---|---|---|
| TL-G01 | ResNet/CIFAR-100/SGD-momentum generalization | Changes architecture, modality, task and optimizer together, then retests receiving-state conditioning, finite-amplitude nonlinearity, distributed-support reallocation, target boundaries under a frozen protocol. | [cross-system generalization experiment](experiments/gfg_resnet_cifar_training_learning_generalization_v1/) |
| TL-G02 | DDPM-style U-Net/CIFAR-10/AdamW generalization | Changes the task to generative diffusion residual prediction and the target identity to an image--timestep--noise occurrence, then retests receiving-state conditioning, finite-amplitude nonlinearity, distributed-support reallocation, residual-error boundaries. | [diffusion generalization experiment](experiments/gfg_ddpm_cifar_training_learning_generalization_v1/) |
| INF-G01 | Cross-system frozen-inference projection | Retests exact learned-version use, causal component recruitment, query-conditioned distributed support, non-additive combination and exact rollback dependence in both TL-G01 and TL-G02. | [cross-system inference experiment](experiments/gfg_cross_system_frozen_inference_projection_v1/) |
| TL-G03 | Deterministic top-2 Vision-MoE/CIFAR-100/AdamW generalization | Adds routed expert organization and retests receiving parameter and Adam-state conditioning, finite-amplitude nonlinear response, expert-support reallocation, routing integrity under a frozen protocol. | [MoE training--learning experiment](experiments/gfg_moe_cifar_training_learning_inference_generalization_v1/) |
| INF-G02 | Vision-MoE frozen-inference projection | Tests exact persistent-state preservation, deterministic top-2 routing, query-conditioned expert recruitment, non-additive expert combination, trained expert/router version dependence and exact rollback restoration. | [MoE inference experiment](experiments/gfg_moe_cifar_training_learning_inference_generalization_v1/) |
| GNN | Graph reachability / RMSprop | Tests the TLI relations and target-boundary predictor across three registered seeds. | [Results, frozen plan and execution](independent_stress_tests/windows_reproduction/README.md) |
| SNN | Hard-spiking digits / Adagrad | Tests structural TLI criteria and the target-boundary predictor across four registered seeds. | [Results, frozen plan and execution](independent_stress_tests/windows_reproduction/README.md) |

## GRU feedback dynamics

| ID | Experiment | Main scientific role | Code, protocol and evidence |
|---|---|---|---|
| RL-E05 | Selective positive feedback and support concentration | Tests whether prolonged exact positive feedback for one skill concentrates its relative functional support, crowds other mastered skills and creates a component-version trade-off under selective, balanced and frozen controls. | [support-concentration experiment](experiments/gfg_rl_selective_positive_feedback_support_concentration_v1/) |
| RL-E06 | Positive-feedback dose, duration and recovery | Tests feedback concentration as a dose and duration coordinate, distinguishes continuous margin erosion from discrete boundary loss, and causally tests balanced and other-skills-only recovery from the exact same exclusive-feedback state. | [dose--duration--recovery experiment](experiments/gfg_rl_selective_positive_feedback_dose_recovery_v1/) |

## nanoGPT three-history experimental supplement

The [integrated supplement](supplements/nanogpt/README.md) provides three
10,000-update histories with their matched interventions, response and support
measurements, frozen inference and target-boundary prediction. Its single
entry contains the download, reproduction commands, results and
[record-to-paper numbering](supplements/nanogpt/README.md#record-to-paper-numbering).
