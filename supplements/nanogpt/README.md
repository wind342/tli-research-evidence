# nanoGPT three-history experimental supplement

This supplement connects three complete training histories to their measured
update responses, support changes, target-boundary transitions and frozen
inference. The upload brings the captured GFGs, checkpoints, measurement code
and result ledgers together so the full experimental sequence can be obtained
and reproduced from one entry point.

Each history contains 10,000 training updates, with evaluation every 100
updates. The first two histories supply the development set; the third is the
confirmation history. Together they provide 30,000 captured updates.

| History | Role | Model seed | Updates |
| --- | --- | ---: | ---: |
| nano-supp-01 | Development | 2611701 | 10,000 |
| nano-supp-02 | Development | 2611702 | 10,000 |
| nano-supp-03 | Confirmation | 2611703 | 10,000 |

The sequence covers capability formation, matched pause and clipping
interventions, receiving-state and optimizer-memory exchanges, finite-amplitude
response paths, component gating, support reallocation, target-boundary
measurements, frozen inference and actual-update boundary prediction.

The pause branches postponed formation by 800 and 1,100 updates. The clipping
branch and its baseline reached formation at update 1,200. The support ledger
contains 828 target-group records across 36 update sections and 24 primary
support hand-offs. The target-boundary records contain 3,816 measured targets.
The complete quadratic predictor scored 1,264/1,272 on the confirmation
history, with 99.37% accuracy and 98.31% four-way macro recall.

## Download and run

Download the two parts of `TLI_nanoGPT_Three_History_Evidence.zip` and the
`TLI_nanoGPT_Three_History_Evidence.parts.json` manifest from the release.
Join them with `fetch_archive.py`; the helper checks each part and the joined
archive. Extract the ZIP into a new directory. From that directory:

```sh
python -B verify_package.py
python -B supplements/nanogpt/e07_provenance.py
python -B supplements/nanogpt/run_all.py replay-captured --output ../nanogpt-replay
python -B supplements/nanogpt/run_all.py rerun-all --output ../nanogpt-training
```

The package checker verifies file hashes. The ledger command recomputes the
support transitions from saved responses and updates. Replay starts from the
three captured histories; the training command runs the full sequence from
the registered seeds.

Reference environment: Windows, Python 3.12.10, PyTorch 2.11.0+cu128,
NumPy 2.5.2, SciPy 1.16.3, jsonschema 4.25.1, Git and an NVIDIA CUDA GPU.
The package includes the nanoGPT model, Git bundle, Core implementation,
instrument code and shared analysis dependencies.

## Files

- [Release and full download](https://github.com/wind342/tli-research-evidence/releases/tag/tli-execution-evidence-20261125)
- [Download manifest](DOWNLOAD.json) and [download/join helper](fetch_archive.py)
- [Frozen training configuration](PROTOCOL.json) and [history identities](captured/HISTORIES.json)
- [Measurement records](records/) and [archive file identities](ARCHIVE_FILE_MANIFEST.json)
- [Execution entry point](run_all.py)

For automatic download, place the helper and manifest in one directory and run:

```sh
python fetch_archive.py --manifest DOWNLOAD.json --download --directory nanoGPT-download
```
