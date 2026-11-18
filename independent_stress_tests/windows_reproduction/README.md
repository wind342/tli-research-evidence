# GNN and hard-spiking SNN: Windows reproduction

Two independent fresh runs on Windows 11 CPU used the original data, seeds, schedules, and registered criteria. The Table 3 predictions in each round use the actual optimizer updates captured in that round.

| System | Correct / targets | Accuracy | Four-way macro recall | Prediction criterion |
| --- | ---: | ---: | ---: | --- |
| GNN | 3,063 / 3,072 | 99.71% | 98.96% | Met |
| Hard-spiking SNN | 6,825 / 7,200 | 94.79% | 71.30% | Not met |

The registered prediction criterion requires both metrics to reach 90%. In the structure experiments, the GNN met 8/9, 9/9, and 8/9 criteria, and all four SNN seeds met 12/12.

- [Environment, per-seed criteria, hashes, and two-round comparison](WINDOWS_REPRODUCTION.json)
- Round 1: [GNN structure](round-1/gnn_tlir_formal_results.json), [SNN structure](round-1/SNN_TLIR_formal/FORMAL_SUMMARY.json), [Table 3](round-1/table3/ADJUDICATION_REPORT.json), [prediction audit](round-1/table3/INDEPENDENT_CHECK_RESULT.json)
- Round 2: [GNN structure](round-2/gnn_tlir_formal_results.json), [SNN structure](round-2/SNN_TLIR_formal/FORMAL_SUMMARY.json), [Table 3](round-2/table3/ADJUDICATION_REPORT.json), [prediction audit](round-2/table3/INDEPENDENT_CHECK_RESULT.json)

The Windows runs supply the current ICML manuscript figures and table. The original [GNN](../gnn/), [SNN](../snn/), and [prediction](../tlp01_prediction/) archives are preserved separately.
