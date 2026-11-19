# Graph Neural Network: historical independent TLI stress test

**Record type:** Historical native PyTorch study of Training–Learning–Inference (TLI) relations, run under an independently frozen protocol. The original file path retains its historical TLIR naming. **Current ICML authority:** [November 2026 GNN/SNN Windows records](../windows_reproduction/README.md), with GNN seeds 202611801–202611803, nonlinear-response counts **6/256, 36/256, 20/256**, and structural results **8/9, 9/9, 8/9**. The historical GNN study reported below used *different seeds and measurements*.

## Experimental question and design

The test measures TLI relationships in a four-layer residual message-passing network trained by RMSprop on graph-reachability labels. Its measurements cover actual training updates, receiving-state exchanges, finite-amplitude responses, component-coalition effects, persistent support reallocation, frozen inference and exact version rollback.

- **Data:** 12-node undirected Erdős–Rényi graphs, edge probabilities 0.13–0.37, two semantically identified marked nodes, and permutations of non-anchor nodes. Labels indicate whether the target lies within two hops of the anchor.
- **Network:** 40-dimensional hidden state; four residual message-passing blocks; readout from the anchor node.
- **Training:** RMSprop, learning rate 0.003, batch size 64 and 500 actual optimizer updates; 1,024 training graphs and 256 disjoint test graphs per seed.
- **Registration:** Pilot seed 99999 was separate from the three formal seeds 20261024, 20261025 and 20261026. Checkpoints were updates 25, 100, 200 and 350; paired receiver/update comparisons were (100←25), (200←100) and (350←200).
- **Component intervention:** All 16 four-component coalitions were evaluated, with exact Shapley allocation. The interaction test used complete logits.
- **Protocol SHA-256:** `e2bd6b803c20df9bc3e612edc931631df4b8ec14016b2db1fb5fc5a321932085`.
- **Source SHA-256:** `28e9b9d8d611c05fa3b6a45b89f359181c6d83ef21d4fb8681f85e4d6ab5a722`.

## Frozen nine-criterion results (historical seeds)

| Criterion | 20261024 | 20261025 | 20261026 |
|---|:---:|:---:|:---:|
| Training accuracy ≥85% | PASS | PASS | PASS |
| Frozen inference and repeat-output integrity | PASS | PASS | PASS |
| Same actual update in different receiving states | PASS | PASS | PASS |
| Finite-amplitude nonlinear-response frequency ≥10% | **FAIL** | PASS | PASS |
| Distributed component support | PASS | PASS | PASS |
| Support reallocation after the actual update | PASS | PASS | PASS |
| Query-conditioned support in inference | PASS | PASS | PASS |
| Non-additivity of complete logits | PASS | PASS | PASS |
| Exact rollback and restoration of learned component versions | PASS | PASS | PASS |

| Formal seed | Test accuracy | Nonlinear target-update responses | Mean fraction exceeding support-reallocation threshold |
|---|---:|---:|---:|
| 20261024 | 100.00% | 4/256 (1.56%) | 61.72% |
| 20261025 | 100.00% | 44/256 (17.19%) | 34.38% |
| 20261026 | 100.00% | 36/256 (14.06%) | 49.61% |

All three seeds attained 100% test accuracy by update 100. Seed 20261024 missed the registered nonlinear-frequency criterion; the other eight criteria passed in all three seeds. The observed nonlinear-response frequency varied across seeds.

## Native reproduction and checker

A second run of the same frozen three-seed program reproduced the formal experiment's state and result identities.

- **Formal/replay result SHA-256:** `5579099e40bc605dec076134ab7393b936411b6bc18d286166a1d525a523de47`.
- **Independent checker:** `gnn_independent_checker.py`; its frozen-protocol, data-identity, checkpoint and nine-gate audit returned **PASS**.
- **Native computation:** The program performed fresh training and real forward passes. The independent checker independently evaluates the stored records and criteria.

## Exploratory graph-structure controls (after formal registration)

| Seed | New-label accuracy after adjacency swap | Accuracy against original labels | New-label accuracy after marker relocation | Accuracy against original labels |
|---|---:|---:|---:|---:|
| 20261024 | 100.00% | 56.25% | 100.00% | 61.72% |
| 20261025 | 100.00% | 51.17% | 100.00% | 61.72% |
| 20261026 | 100.00% | 50.00% | 100.00% | 60.16% |

The graph controls were conducted after the nine frozen criteria and remain exploratory. Their model and state hashes were checked against the relevant repeated native executions.

## Evidence and scope

- [Frozen protocol](gnn_falsification_frozen.json), [native code](gnn_tlir_counterexample.py), [machine results](gnn_tlir_formal_results.json), [replay](gnn_tlir_formal_replay.json), [independent checker](gnn_independent_checker.py), [audit](gnn_falsification_audit.json) and [exploratory controls](gnn_graph_negative_controls.json).
- The experiment evaluated supervised graph reachability and the nine registered TLI operational criteria. The full GFG Core v3 instrument stack and environmental-feedback interventions were outside this particular protocol.
- **Current TLI/ICML figures and Table 3:** use [the November Windows records](../windows_reproduction/README.md), with a separate frozen source and distinct seed identities.

