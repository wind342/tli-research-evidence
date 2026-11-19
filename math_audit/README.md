# Reproducible mathematical checks for the 14 TLI recoveries

This directory is the **current** runnable numerical/algebraic verification, not a copy of the historical 2026-11-03 `verify_14.py` program. It tests 21 representative relations and notation rules across the 14 cases in [`../TLI_THEORY_FIRST_14_DERIVATIONS.md`](../theory/TLI_THEORY_FIRST_14_DERIVATIONS.md).

## Inputs and outputs

- `verify_14.py` — executable 21-check implementation, one case-labelled verdict per assertion group
- `inputs.json` — exact deterministic input parameters, fixed random seed and Monte Carlo tolerance
- `requirements.txt` — dependencies for this particular independent audit only
- `RESULTS.json` — saved results, case names, input hash and numerical test results

To repeat from the repository root:

```sh
python -m pip install -r math_audit/requirements.txt
python math_audit/verify_14.py
```

The output has 21 checks across 14 cases, including seeded Gaussian inverse-Wishart Monte Carlo for both sides of Double Descent. All mathematical checks are under their stated original-model conditions; a passing check is **not** an independent reconstruction of every historical theorem or a rerun of experiments. The November 3 historical 21/21 statement has been replaced as the current audit authority by this archived, reproducible test suite.

The final Double Descent check also reads the current derivation document to enforce the notation distinction between TLI functional response `R_{t,\mathrm{test}}` and risk `\mathcal E_{\mathrm{test}}`. The associated active paper is the [current TLI ICML manuscript](https://github.com/wind342/tli-paper/tree/icml-final/icml).
