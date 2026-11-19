# GNN and hard-spiking SNN: November 2026 Windows results

These records supply the current ICML manuscript's GNN/SNN cross-system subsection, Figure 3, and appendix Table 3. The reported native Windows CPU runs used three fixed GNN seeds and four fixed SNN seeds. Boundary predictions were calculated from updates recorded during training.

| System | Correct / targets | Accuracy | Four-way macro recall | Prediction criterion |
| --- | ---: | ---: | ---: | --- |
| GNN | 3,068 / 3,072 | 99.87% | 97.87% | Met |
| Hard-spiking SNN | 6,713 / 7,200 | 93.24% | 60.05% | Not met |

The prediction criterion requires accuracy and four-way macro recall of at least 90%. The GNN met 8/9, 9/9, and 8/9 structural criteria, with nonlinear response counts of 6/256, 36/256, and 20/256. All four SNN seeds met 12/12 criteria.

- [Run environment, seeds and results](WINDOWS_REPRODUCTION.json)
- [GNN structure](round-1/gnn_tli_formal_results.json) · [SNN structure](round-1/SNN_TLI_formal/FORMAL_SUMMARY.json)
- [Table 3](round-1/table3/ADJUDICATION_REPORT.json) · [Independent prediction audit](round-1/table3/INDEPENDENT_CHECK_RESULT.json)

## Source identity and verification level

The current directory contains the November machine-result summaries, seed/criterion record, prediction adjudication and independent-check receipt. The current tree does **not** contain the exact November-run native training programs, runnable environment specification, or full frozen execution protocol. The GNN and SNN source programs under the adjacent historical directories correspond to different October seeds and should be cited as historical source, not the executable authority for these November records. The existing prediction checker receipt reports `PASS` for 28 events and 10,272 targets; that receipt documents the recorded check, rather than a new native training rerun performed by this documentation update.

Earlier manuscript versions can still be audited with the archived [GNN](../gnn/), [SNN](../snn/), and [prediction](../tlp01_prediction/) evidence and the Git history.
