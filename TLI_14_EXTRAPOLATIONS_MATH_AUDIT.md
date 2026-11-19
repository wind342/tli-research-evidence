# TLI — 14 mathematical recoveries: sources, algebra and equation-concordance audit

**Current authoritative paper:** [TLI ICML manuscript](https://github.com/wind342/tli-paper/tree/icml-final/icml).  
**Theory equations:** [`icml/sections/dynamics_layout.tex`](https://github.com/wind342/tli-paper/blob/icml-final/icml/sections/dynamics_layout.tex).  
**Evidence text:** [14 complete derivations](TLI_THEORY_FIRST_14_DERIVATIONS.md), [TLI coupled dynamical equations](TLI_UNIFIED_DYNAMICS.md).  
**Audit record:** Original November 3, 2026 mathematical audit; current-equation alignment reviewed on November 20, 2026.

## November 3, 2026 — Original mathematical audit

**Audit date:** November 3, 2026  
**Reference documents:** `TLI_UNIFIED_DYNAMICS.md`, `TLI_THEORY_FIRST_14_DERIVATIONS.md`, and `TLI_HISTORICAL_COMPARISONS_21.md`.  
**Tags:** <sup>[T]</sup> Original TLI equation; <sup>[A]</sup> mathematical model and conditions in the cited research; <sup>[R]</sup> result recovered through substitution and computation.

## Summary of the mathematical cases

All fourteen cases retain the original mathematical objects and principal closed-form relationships. Their records identify TLI starting equations, conditions taken from the original studies and specific substitution/calculation chains. The audit addresses the displayed mathematical statements and their domains.

| Case | Topic | Mathematical conditions | Audit finding |
|---|---|---|---|
| 1 | Edge of Stability | **Local linearization** | Substituting GD into the state transition gives $e_{i,t+1}=(1-\eta\lambda_i)e_{i,t}$; $2/\eta$ is the local stability edge for positive curvature in the stated model. |
| 2 | Implicit Bias | **Direct one-dimensional calculation; original multidimensional theorem** | The update remains positive after correctness saturates, and $w_t=\log t+O(1)$; the maximum-margin direction in multiple dimensions is established by Soudry et al.'s original theorem. |
| 3 | Model Collapse | **Exact finite-discrete sampling; mixed-data expectation** | Both $\Pr(q_{t+1}=0\mid q_t)=(1-q_t)^M$ and $E[q_{t+1}\mid q_t]=q_t$ hold. Random disappearance of support differs from a per-generation decline in expected frequency. |
| 4 | Spectral Bias | **Frozen-kernel approximation; conditional frequency ordering** | Residual modes decay as $(1-\eta\lambda_k)^t$; any low-frequency-first conclusion uses the original kernel spectral order. |
| 5 | Benign Overfitting | **Exact risk expectation conditioned on noise** | The minimum-norm solution selected by GD gives bias and variance terms for expected risk, distinct from a single-sample risk. |
| 6 | Chinchilla | **Compute optimization conditional on the original empirical power law** | Differentiation gives $aAN^{-a}=bBD^{-b}$; optimum $N,D$ and the optimized loss exponent follow, with the empirical power-law exponents supplied by the original model. |
| 7 | Dynamical Isometry | **First-order actual-action response; corrected singular-value bound** | Chain-rule propagation yields local response; a Jacobian with a nullspace has zero minimum gain on the full space, so the smallest nonzero singular value applies to restricted directions. |
| 8 | Dropout | **Exact GLM expected-loss decomposition and Gaussian linear regularizer** | Independent Bernoulli masks preserve the mean label-linear term; squared loss gives a feature-weighted $L_2$ contribution. Individual masked actions and their conditional expectations remain distinct. |
| 9 | Catastrophic Forgetting | **Exact telescoping and boundary crossing; first-order gradient geometry** | The accumulated response and correctness boundary are exact, while gradient-angle interpretations require a small-update approximation. |
| 10 | Grokking | **Original linear teacher–student spectral-endpoint asymptotics** | The original state dynamics and training/generalization readouts are retained; the delay expression preserves the $\sqrt\lambda$ factor and its threshold conditions. |
| 11 | μP | **One-step scaling from Appendix E of the original work** | $\Delta\bar h_j,\Delta f=\Theta(n^{-c})$ in the specified regime; the general μP family and μTransfer have their own independent derivations. |
| 12 | SAM/Sharpness | **Exact product-model Hessian; first-order SAM action** | $(a,b)\mapsto(ca,b/c)$ preserves the function and changes Hessian eigenvalues; the SAM neighborhood/action relation uses its registered approximations. |
| 13 | Gradient Noise Scale | **Exact covariance of the parameter action, first-order functional variance** | For independent sampling, $\operatorname{Cov}(\delta)=\eta^2\Sigma_g/B$; Jacobian projection supplies query-dependent response noise. $B$ is batch size, distinguished from feedback $B_t$. |
| 14 | Double Descent | **Gaussian zero-signal least-squares finite-sample expectation** | Inverse-Wishart moments yield piecewise noise risk on either side of interpolation at $p<n-1$ and $p>n+1$, under the stated original model. |

## Original mathematical sources (selected)

- Edge of Stability: [Cohen et al., ICLR 2021](https://openreview.net/forum?id=jh-rTtvkGeM).
- Implicit Bias: [Soudry et al., JMLR 2018](https://jmlr.org/papers/v19/18-188.html).
- Recursive Model Collapse: [Shumailov et al., *Nature* 2024](https://www.nature.com/articles/s41586-024-07566-y).
- Compute-Optimal Scaling: [Hoffmann et al., NeurIPS 2022](https://proceedings.neurips.cc/paper_files/paper/2022/hash/c1e2faff6f588870935f114ebe04a3e5-Abstract.html).
- Dynamical Isometry: [Pennington et al., NeurIPS 2017](https://research.google/pubs/resurrecting-the-sigmoid-in-deep-learning-through-dynamical-isometry-theory-and-practice/).
- Dropout regularization: [Wager et al., NeurIPS 2013](https://papers.nips.cc/paper_files/paper/2013/hash/38db3aed920cf82ab059bfccbd02be6a-Abstract.html).
- Grokking: [Levi, Beck & Bar-Sinai, ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/8c0a85ee3eddb1858d9142f0d51d67b2-Abstract-Conference.html), particularly its Equation (11).
- μP: [Yang & Hu, ICML 2021](https://proceedings.mlr.press/v139/yang21c.html), Appendix E.
- Sharpness: [Dinh et al., ICML 2017](https://proceedings.mlr.press/v70/dinh17b.html); SAM: [Foret et al., ICLR 2021](https://research.google/pubs/sharpness-aware-minimization-for-efficiently-improving-generalization/).
- Gradient Noise: [McCandlish, Kaplan & Amodei, 2018](https://openai.com/index/how-ai-training-scales/).
- Double Descent: [Hastie et al., *Annals of Statistics* 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9481183/).

## Recorded code and formal checks

**Original November 3, 2026 audit:** The script `verify_14.py` was reported to pass **21/21 checks**. It is absent from the current Git evidence tree and was not rerun during the subsequent version-alignment pass. Its reported checks covered local Hessian stability, continued logistic updates, binomial conditional moments, fixed-kernel residuals, bias–variance trace identities, Chinchilla marginal balance, Jacobian nullspaces, exhaustive finite Bernoulli dropout masks, old-capability readout boundaries, Grokking spectral small-threshold asymptotics, SAM coordinate transforms, gradient-noise projection, and Monte Carlo simulation of Gaussian Wishart risk on both sides of interpolation.

**Review scope:** Numerical spot checks detect some formula errors and sign mistakes. The original audit documented correction of earlier equation numbering, the dynamical-isometry nullspace bound, the distinction between exact relationships and first-order approximations, and the mathematical conditions of Grokking, μP and Chinchilla.

## Alignment of the research documentation

- `TLI_THEORY_FIRST_14_DERIVATIONS.md`: Explicit equation provenance and applicability for all fourteen recoveries.
- `TLI_HISTORICAL_COMPARISONS_21.md`: Twenty-one paired comparisons of published theories and contrasting results.
- `TLI_UNIFIED_DYNAMICS.md`: Training and feedback arguments updated to the current ICML equations, while state, response, support, capability and frozen-inference relations retain their scientific definitions.

**Conclusion:** All fourteen records follow **TLI starting equation [T] → original-study conditions [A] → substitution and calculation → recovered relation [R]**, with the mathematical strength and domain of each relation specified.

## 2026-11-20 — ICML equations and recovered-mathematics cross-check

### Exact correspondence of the [T] starting equations

| Relation | Current ICML mathematical form | TLI evidence form |
|---|---|---|
| Receiving state | \(Z_t=(L_t,\omega_t)\) | Exact match |
| Training | \(A_t=\mathcal U(Z_t,B_t)\), \(Z_{t+1}=\mathcal T(Z_t,A_t)\) | Exact match; earlier text with distinct \(D_t,B_t\) inputs updated |
| Actual update | \(\delta_t=\Psi(\theta_t,\omega_t,B_t)\), \(\theta_{t+1}=\theta_t+\delta_t\) | Exact match |
| Response | \(R_{t,q}=m_q(L_{t+1})-m_q(L_t)\) | Exact match |
| Functional support | \(P_{t,q}=\mathcal P_q(L_t;\mathcal J_q)\), \(\Delta P_{t,q}=P_{t+1,q}-P_{t,q}\) | Exact match |
| Capability | \(C_{t,q}=\chi_q(m_q(L_t))\), \(C_{t+1,q}=\chi_q(m_q(L_t)+R_{t,q})\) | Exact match |
| Frozen inference | \(S_{x,c}^{\mathrm{active}}=\Pi_{x,c}(L^*)\), \(Y_{x,c}=H_{x,c}(S_{x,c}^{\mathrm{active}})\), \(\Delta_{\mathrm{inf}}L=0\) | Exact match |
| Feedback closure | \(B_{t+x}=\mathcal B(Y_t,E_t)\), \(A_{t+x}=\mathcal U(Z_{t+x},B_{t+x})\), \(Z_{t+x+1}=\mathcal T(Z_{t+x},A_{t+x})\), \(x\ge1\) | Exact match; earlier feedback-memory input removed |

The [current manuscript](https://github.com/wind342/tli-paper/blob/icml-final/icml/sections/extrapolations_main_complete.tex) includes Edge of Stability and Catastrophic Forgetting in the main text, while [the appendix](https://github.com/wind342/tli-paper/blob/icml-final/icml/sections/appendix_remaining_complete.tex) contains the remaining twelve mathematical cases. The fourteen cases in the TLI evidence document retain the paper's corresponding mathematical results and original-source conditions.

### Independently checked algebra in this pass

SymPy simplification and exact arithmetic were executed for these representative relationships:

1. **Edge of Stability:** for \(\lambda=2/\eta\), the discrete GD multiplier is \(1-\eta\lambda=-1\), which identifies the positive-curvature linear stability boundary.
2. **Sharpness/SAM product response:** \((a+\delta_a)(b+\delta_b)-ab=b\delta_a+a\delta_b+\delta_a\delta_b\) holds identically (symbolic difference zero).
3. **Chinchilla:** differentiating \(-AN^{-\alpha}-BD^{-\beta}\) along \(D=C/(6N)\) gives \(+\alpha AN^{-\alpha-1}-\beta BD^{-\beta}/N\), equal to the paper's expression (symbolic difference zero).
4. **Bernoulli dropout:** exact enumeration of independent binary masks for two coordinates yields \(\operatorname{Var}(w^\top\widetilde x)=(1-r)r^{-1}\sum_jw_j^2x_j^2\) (symbolic difference zero).
5. **Exploratory E-I04 feedback stability:** the current-paper feedback specialization \(J=\left(\begin{smallmatrix}1-\alpha&\beta\\\kappa&0\end{smallmatrix}\right)\) has \(\det(I-J)=\alpha-\beta\kappa\), eigenvalues \(\big[(1-\alpha)\pm\sqrt{(1-\alpha)^2+4\beta\kappa}\big]/2\). For \(0<\alpha<1,\beta,\kappa\ge0\), its spectral-radius threshold is \(\beta\kappa=\alpha\).

**Scope of this review:** All fourteen theory cases were checked against the corresponding ICML source sections for their starting TLI equations, original-model conditions, and displayed main mathematical results. The five checks above independently verify representative algebra. This review did not reproduce every original paper theorem or rerun the historical 21-check script; the original 2026-11-03 findings remain documented separately. E-I04 is an exploratory calculation, outside the official fourteen cases, and its local Jacobian was corrected to match the current feedback map.

