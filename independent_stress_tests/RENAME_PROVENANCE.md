# TLI file-path migration and frozen evidence identity

This change removes superseded manuscript-navigation files (PNAS, Science and TLIR v8) and renames GNN/SNN **file paths** from `gnn_tlir` / `snn_tlir` / `SNN_TLIR` to `gnn_tli` / `snn_tli` / `SNN_TLI`.

**Evidence integrity:** Binary records, measurements, frozen protocols, result JSON payloads and replay logs were moved using their original Git blob identities. The producer programs `gnn/gnn_tli_counterexample.py` and `snn/snn_tli_adversarial.py` also retain byte-identical content and their frozen SHA-256 checksums. Frozen internal schema IDs, old command defaults embedded in hashed producer programs, and original log texts intentionally retain historic strings.

Python import statements, checker path lookups, and documentation links now use active TLI file paths. Since the original SNN independent checker's import had to be adapted, its historical byte-exact contents are **also** retained at `snn/frozen_checker_original.py` (identical Git blob). The runnable path-adapted script is `snn/snn_tli_independent_checker.py`. Do not compare the adapted checker's file hash to `independent_checker_sha256` in the frozen protocol; that hash designates the saved original checker. The frozen protocol itself was not modified.

Example from the repository root (after installing the recorded dependencies and native state restoration):

```bash
cd independent_stress_tests/snn
python restore_native_states.py
python snn_tli_independent_checker.py --root formal --protocol snn_tli_frozen_protocol.json
python snn_tli_independent_checker.py --root replay --protocol snn_tli_frozen_protocol.json
```

GNN rechecks use `cd independent_stress_tests/gnn && python gnn_independent_checker.py`; the code uses directory-relative paths for the renamed result files. Hash references to earlier commits, the archived raw logs, and frozen result schema identifiers remain historical identities, not the current manuscript name.

All prior filenames and draft manuscripts are still retrievable through Git history. This maintenance commit does not claim a new experimental rerun or change any scientific verdict.
