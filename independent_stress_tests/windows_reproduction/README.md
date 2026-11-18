# GNN and hard-spiking SNN: Windows reproduction

These results supply Section 2.3.2, Figure 3, and Table 3 of the ICML manuscript. The native Windows CPU runs used three fixed GNN seeds and four fixed SNN seeds. The prediction calculation used the actual updates captured during training.

| System | Correct / targets | Accuracy | Four-way macro recall | Prediction criterion |
| --- | ---: | ---: | ---: | --- |
| GNN | 3,068 / 3,072 | 99.87% | 97.87% | Met |
| Hard-spiking SNN | 6,713 / 7,200 | 93.24% | 60.05% | Not met |

The prediction criterion requires accuracy and four-way macro recall of at least 90%. The GNN met 8/9, 9/9, and 8/9 structural criteria, with nonlinear response counts of 6/256, 36/256, and 20/256. All four SNN seeds met 12/12 criteria.

- [Run environment, seeds and results](WINDOWS_REPRODUCTION.json)
- [GNN structure](round-1/gnn_tlir_formal_results.json) · [SNN structure](round-1/SNN_TLIR_formal/FORMAL_SUMMARY.json)
- [Table 3](round-1/table3/ADJUDICATION_REPORT.json) · [Independent prediction audit](round-1/table3/INDEPENDENT_CHECK_RESULT.json)

Earlier manuscript versions can still be audited with the archived [GNN](../gnn/), [SNN](../snn/), and [prediction](../tlp01_prediction/) evidence and the Git history.
