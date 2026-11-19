# Historical independent TLI stress tests: GNN and SNN (2026-10-24)

Independent ChatGPT-assisted experiments on two new neural systems, using their own PyTorch-native interventions, frozen programs and independent checkers. This October study covers TLI structural relations in GNN and SNN. Its execution environment and program differ from the [November Windows results](windows_reproduction/README.md) used in the current ICML Table 3. The October tests address training, learning and frozen inference; feedback closure is evaluated separately in the GRU experiments.

## Experiments

- [GNN, four-layer residual message-passing, RMSprop](gnn/GNN_TLIR_独立反证实验报告.md): 3 formal seeds; one frozen finite-amplitude nonlinear-frequency gate **FAILED** (seed 20261024: 4/256 = 1.56% versus a 10% threshold), while both other seeds passed this gate. This formal negative result is retained.
- [Hard-spiking recurrent SNN, Adagrad](snn/TLIR_脉冲网络独立反证实验报告.md): 4 formal seeds, all 12 operational checks passed per seed; single-branch low-response cases and surrogate-derivative mismatch are retained.

## Source identity and reproduction

The October source, frozen protocols, results, replay logs, checkers and reports are preserved as historical experimental evidence. The current ICML GNN/SNN result authorities appear in the [November records](windows_reproduction/README.md). The SNN native PyTorch .pt states require a trusted source (do not load untrusted pickle) and hashes are documented by the formal manifest and replay comparison.

Some scripts embed absolute /mnt/data source paths, which were **preserved to retain the original frozen hashes**. A new-directory reproduction may require a matching path layout or a clearly disclosed working-copy path edit; it then is not a byte-identical original-source replay.

Original publication tag and core `experiments/` files retain their original experimental content. See [evidence scope](EVIDENCE_SCOPE.md).
