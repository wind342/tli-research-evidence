# GNN and hard-spiking SNN execution evidence

This package connects the GNN and SNN measurements in Figure 3 and Table 3
to their frozen execution plan, model programs, training states, sealed
predictions and independent-check records. It provides the executable inputs
and native records for the seven runs used in the manuscript.

| System | Seeds | Correct / targets | Accuracy | Four-way macro recall |
| --- | --- | ---: | ---: | ---: |
| GNN | 202611801, 202611802, 202611803 | 3,068 / 3,072 | 99.87% | 97.87% |
| Hard-spiking SNN | 71101, 71102, 71103, 71104 | 6,713 / 7,200 | 93.24% | 60.05% |

The GNN structural results are 8/9, 9/9 and 8/9, with nonlinear-response
counts of 6/256, 36/256 and 20/256. Each SNN run passed 12/12 structural
criteria. The prediction criterion requires accuracy and four-way macro
recall of at least 90%: the GNN met this criterion and the SNN did not.

- [Execution plan and frozen source identities](REPLICATION_PLAN.json)
- [Model code and structural records](inputs/)
- [Prediction code and protocol](predictor/)
- [Sealed predictions and endpoint records](table3/)
- [SHA-256 file manifest](SHA256_MANIFEST.json)

## Reproduction

Use Windows x64, Python 3.12.10 and the versions in the execution plan.
From the extracted package directory:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --index-url https://download.pytorch.org/whl/cpu torch==2.13.0+cpu
.\.venv\Scripts\python.exe -m pip install numpy==2.4.4 scipy==1.17.1 scikit-learn==1.8.0 joblib==1.6.0 threadpoolctl==3.8.0 cloudpickle==3.1.2
.\.venv\Scripts\python.exe -B verify.py
.\.venv\Scripts\python.exe -B verify.py --fresh ../gnn-snn-run
```

The first verification command replays the stored SNN states and the Table 3
endpoints. The fresh-run command trains the seven seeds and compares their
measurements and sealed predictions with the packaged records.
