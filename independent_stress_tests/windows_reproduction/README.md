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

## Execution files and reproduction

The [execution directory](execution/README.md) contains the frozen plan,
model and prediction programs, runtime versions, seven seeds' native training
states, sealed predictions, endpoint records and independent checkers. These
files connect the current manuscript's reported measurements to executable
inputs and saved model states.

- [Complete execution ZIP](https://github.com/wind342/tli-research-evidence/releases/download/tli-execution-evidence-20261125/TLI_GNN_SNN_Execution_Evidence.zip)
- [Frozen plan](execution/REPLICATION_PLAN.json)
- [Model programs and structure records](execution/inputs/)
- [Prediction code](execution/predictor/) and [prediction records](execution/table3/)
- [File hashes](execution/SHA256_MANIFEST.json)

The execution README gives the environment installation, saved-state replay
and fresh-training commands.
