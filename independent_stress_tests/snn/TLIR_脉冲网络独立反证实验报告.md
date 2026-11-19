# Hard-spiking recurrent neural network: historical independent TLI stress test

**Date of original experiment:** 2026-10-24. This report records the original four-seed hard-spiking network study. The historical filename retains TLIR. The **current TLI/ICML** manuscript uses the distinct [November 2026 Windows GNN/SNN evidence](../windows_reproduction/README.md): four SNN structural checks of 12/12, with predictor accuracy **93.24%**, four-way macro recall **60.05%**, and **6,713/7,200** correct boundary predictions.

## Scientific question and frozen system

The experiment measured TLI relations under discontinuous hard-spike forward computation and recurrent transient membrane states.

- **Model:** Four hard-spiking recurrent blocks, six temporal steps, hard discrete-spike forward passes and surrogate-gradient backpropagation.
- **Task:** Classification of the scikit-learn 8×8 handwritten digits; stratified 75/25 train/held-out split, with 96 fixed held-out queries per seed.
- **Optimizer:** Adagrad; 800 actual optimizer updates per seed.
- **Formal seeds:** 71001, 71002, 71003 and 71004; pilot seed 42 was separated before freezing.
- **Frozen checkpoints:** Updates 50, 200, 400 and 700; stored pre/post parameters, realized increments, gradients, optimizer accumulators and batch identities.
- **Interventions:** Receiving-state transplants of identical actual updates; earlier/later optimizer-memory exchanges; amplitude grid 0, 0.125, 0.25, 0.5, 0.75, 1; 16 four-component coalitions and Shapley support; complete-logit interactions; repeat-forward integrity; learned-version rollback and exact restoration.
- **Frozen protocol:** [snn_tlir_frozen_protocol.json](snn_tlir_frozen_protocol.json), SHA-256 `9cc39a3ca6dc7b60697136ddccfa0caa9753860f2598f2e679bb62242a1ddace`.
- **Frozen source SHA-256:** `718931152b06d6b7aa0d8416fe094463fed714e9cf06efb0e90dbb270a748cf1`.

## Formal twelve-criterion result

| Historical formal seed | Held-out accuracy | Nonlinear-response fraction (384 target-update records) | Frozen structural criteria |
|---|---:|---:|---:|
| 71001 | 97.33% | 37.24% | 12/12 |
| 71002 | 95.56% | 45.31% | 12/12 |
| 71003 | 96.67% | 43.23% | 12/12 |
| 71004 | 94.89% | 42.45% | 12/12 |

All four formal seeds passed their twelve registered criteria. The observations include receiving-state-dependent responses, optimizer-memory effects on formed updates, finite-amplitude nonlinear responses, persistent support reallocation, query-conditioned frozen inference, complete-logit non-additivity and version-dependent responses under rollback. Maximum single-parameter error when reconstructing the native Adagrad update was approximately 6×10⁻⁸ or less.

### Individual checkpoint observations

- Seed 71004 at update 700: optimizer-memory-exchange response NRMSE approximately **0.019**, below the individual-response threshold of 0.05. The formal gate required at least two of three registered comparisons to pass; the other two did.
- Seed 71002 at update 700: support-reallocation frequency approximately **1.0%**, below its earlier-checkpoint measurements.

These checkpoint values remain in the stored records and preserve within-run variation in effect size.

## Subsequent exploratory measurements

- At updates 400 and 700, **733/768** target-update records retained correct predictions across the update; **148** showed Shapley-support allocation changes above 0.01.
- Comparison of surrogate-gradient JVP and native finite differences at 16 checkpoints (`eps=0.001`) gave mean normalized disagreement **1.177**.
- The exploratory surrogate-based one-step logit predictor had mean RMSE **0.268**, versus **0.308** for the unchanged-parameter baseline.

The predictor uses surrogate differentiation across a hard threshold, whereas the current ICML TL-P01 table records the registered endpoint-boundary results from distinct November 2026 Windows runs.

## Reproduction and audit

- **Original formal summary SHA-256:** `578bdf5f17c7398ede73697373d435d662b80310ff063a56688d766a113c8191`.
- A fresh run of the four formal seeds under the same environment reproduced all twelve native state/measurement/gate files byte-for-byte per seed. The two summary files differ in their runtime metadata, as described in [SNN_TLIR_replay_comparison.json](SNN_TLIR_replay_comparison.json).
- The independent checker replayed model forwards from native parameters, updates and component-coalition logits. Both source and replay audits returned **PASS**.

## Evidence and interpretation

- [Original formal summary](formal/FORMAL_SUMMARY.json), [replay summary](replay/FORMAL_SUMMARY.json), [frozen protocol](snn_tlir_frozen_protocol.json), [native program](snn_tlir_adversarial.py), [independent checker](snn_tlir_independent_checker.py) and [native-state assembly](native_parts/README.md).
- This study used its own operational TLI stress-test program, component coalitions and native-state integrity records. GFG Core v3 instrument execution and feedback reinforcement trials are separate experimental lines.
- The original formal structural results are positive across four seeds; local hard-threshold measurements show varying finite-response sizes. [Current ICML GNN/SNN results](../windows_reproduction/README.md) have distinct seeds and predictor metrics.

