> **Fourteen formal TLI mathematical recoveries.** The [current ICML unified equations](https://github.com/wind342/tli-paper/blob/icml-final/icml/sections/dynamics_layout.tex) provide the starting relations [T], combined with original-study mathematical conditions [A] to recover results [R]. Two full cases appear in the main text and twelve in the appendix. The local indices (1)–(5) below differ from LaTeX equation numbers; section 5.2.E1 is a separate exploratory derivation.

## 5.2 Theory-first mathematical recoveries and comparisons

**Equation provenance:** The current ICML coupled equations, locally indexed in [TLI_UNIFIED_DYNAMICS.md](TLI_UNIFIED_DYNAMICS.md), are [T]. The original mathematical model and assumptions of each study are [A], and relations obtained through explicit substitution and calculation are [R]. Equalities, conditional expectations, approximations and asymptotics are kept distinct. The TLI equations specify relations among state, update, response, support and readout; coefficients, spectra and empirical exponents come from the original-model conditions.
The recovery procedure starts with experimentally established TLI relations and introduces the mathematical models and conditions used by the studies being compared; calculations then recover their relevant functional, stability, risk or optimization results.

**Fourteen completed core mathematical recoveries:** §§5.2.1–5.2.14. Each identifies its TLI entry, original-study conditions, calculation and relation recovered. Section 5.2.2 invokes Soudry et al.'s multidimensional maximum-margin theorem; 5.2.6 optimizes the original Chinchilla empirical loss law; 5.2.10 computes delay in the original soluble linear grokking model; 5.2.11 obtains the characteristic single-step response scaling in the original μP MLP example. Section 5.2.8 uses dropout's GLM/Bernoulli conditions to recover adaptive regularization.

**Displayed-equation provenance:** <sup>[T]</sup> marks an original TLI equation, <sup>[A]</sup> the mathematical model or assumptions of the cited study, and <sup>[R]</sup> the relation obtained by substitution and computation. A multi-step display is marked by its final mathematical role, with the original input identified in the neighboring [A] text. E1 is exploratory and retains its own numbering. **Classification rule:** Completed derivations require explicit mathematics, distinct from qualitative cross-field interpretation.

### 5.2.1 Edge of Stability: Local dynamical stability

**Derivation type:** Local stability threshold under the original theory's conditions.

**Equation provenance.** [T] \(\theta_{t+1}=\theta_t+\delta_t\) and \(Z_{t+1}=\mathcal T(Z_t,A_t)\). [A] The local quadratic model and gradient descent: \(\delta_t=-\eta He_t\), \(H=H^\top\), \(e_t=\theta_t-\theta^\star\). Substitution yields \(e_{t+1}=(I-\eta H)e_t\), projected onto each eigendirection of \(H\). [R] Along positive-curvature directions, local linear contraction requires \(\lvert1-\eta\lambda_i\rvert<1\); the largest positive-curvature direction reaches its boundary at \(\eta\lambda_{\max}=2\). This is a **local linear stability edge** for the specified model.

**TLI object.** Actual update formation and state transition \(\theta_{t+1}=\theta_t+\delta_t\), giving the one-step functional response \(R_q(\theta_t,\delta_t)=m_q(\theta_t+\delta_t)-m_q(\theta_t)\).

**Original-study conditions.** Ordinary gradient descent at fixed learning rate \(\eta>0\), a local quadratic approximation near a stationary point, and locally fixed symmetric Hessian \(H=H^\top\). This is the frozen local-linear stability problem used in Edge-of-Stability analysis.

**Step-by-step derivation.**

\[
\delta_t=-\eta\nabla L(\theta_t),\qquad
e_t=\theta_t-\theta^\star,\qquad
\nabla L(\theta_t)\approx He_t.
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

Substituting the actual action into the TLI state transition gives

\[
e_{t+1}=(I-\eta H)e_t.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

In an eigendirection satisfying \(Hv_i=\lambda_i v_i\),

\[
e_{i,t+1}=(1-\eta\lambda_i)e_{i,t}.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Along positive-curvature directions, local contraction holds if and only if

\[
|1-\eta\lambda_i|<1
\iff 0<\eta\lambda_i<2.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Therefore, the local edge in the largest positive-curvature direction is

\[
\boxed{\lambda_{\max}(H)=2/\eta.}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

**Recovered conclusion.** \(2/\eta\) is the positive-curvature local stability boundary for the specified gradient-descent map. Actual training changes the receiving state and local curvature; the calculation with frozen \(H\) determines the instantaneous linear stability condition.

**Research comparison.** Edge-of-Stability experiments by Cohen et al.; catapult trajectories by Lewkowycz et al.

**Internal experimental anchors.** TL-E03 (receiving-state dependence of actual-action effects); TL-E04 (finite-amplitude update response).

### 5.2.2 Implicit Bias: Continuing internal evolution after capability formation

**Derivation type:** Direct one-dimensional calculation showing a correct readout with continuing state evolution; the multidimensional maximum-margin direction follows Soudry et al.'s original theorem.

**Equation provenance.** [T] \(\theta_{t+1}=\theta_t+\delta_t\), \(R_{t,q}=m_q(L_{t+1})-m_q(L_t)\), \(C_{t,q}=\chi_q(m_q(L_t))\). [A] Linearly separable logistic regression trained by gradient descent. For a one-dimensional example, \(m(w)=w\) and \(\delta_t=\eta/(1+e^{w_t})\). Once \(w_t>0\), \(\chi(m)=1\) remains unchanged while \(\delta_t>0\); \(e^{w_{t+1}}-e^{w_t}\to\eta\) yields \(w_t=\log t+O(1)\). [R] A saturated discrete correctness readout coexists with continuing state change. Multidimensional directional convergence is the original theorem of Soudry et al.

**TLI object.** \(C_{t,q}=\mathbf1[m_q(\theta_t)>0]\) and \(\theta_{t+1}=\theta_t+\delta_t\). Correctness is a target-specific readout, while the parameter state can continue changing.

**Original-study conditions.** Linearly separable data, a linear classifier, logistic loss, gradient descent and no explicit regularization; these are the conditions of the original maximum-margin analysis.

**Step-by-step derivation.** For examples \((x_i,y_i)\), with \(y_i\in\{-1,1\}\), write \(m_i=y_iw^\top x_i\). Then

\[
L(w)=\sum_i\log(1+e^{-m_i}),\qquad
-\nabla L(w)=\sum_i\frac{y_i x_i}{1+e^{m_i}}.
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

Even when all \(m_i>0\) and training accuracy has reached \(100\%\), the right-hand side generally remains nonzero: actual updates continue moving \(w\) and the individual margins.

For an exactly solvable case in the same model class, take the one-dimensional separable example \(x=y=1\) and gradient descent:

\[
w_{t+1}=w_t+\frac{\eta}{1+e^{w_t}}.
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

The sequence \(w_t\) grows monotonically without bound. Once \(w_t>0\), discrete correctness remains 1 while the update stays strictly positive. From

\[
e^{w_{t+1}}-e^{w_t}
=e^{w_t}\!\left(e^{\eta/(1+e^{w_t})}-1\right)
\longrightarrow\eta
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

the asymptotic relation follows:

\[
\boxed{w_t=\log t+O(1),\qquad C_t=1\ \text{while}\ \Delta w_t>0.}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

For multidimensional linearly separable data, Soudry et al. establish convergence of the gradient-descent **direction** toward the hard-margin SVM direction under their original step-size and loss conditions. The direct calculation here concerns the one-dimensional instance.

**Recovered conclusion.** Saturated observable correctness and continuing evolution of the internal learned state can hold simultaneously; the optimizer trajectory may also select a particular separating direction.

**Research comparison.** [Soudry et al., JMLR 2018](https://jmlr.org/papers/v19/18-188.html).

**Internal experimental anchors.** TL-E07 (support reorganizes while correctness stays fixed); TL-E08 (correctness boundary); RL-E06 (persistent functional change after mastery).

### 5.2.3 Recursive Model Collapse: Information loss through finite-sample absorbing states

**Derivation type:** Under the original finite-discrete-distribution, generational-sampling and exact-fitting model, derive the probability of tail loss and eventual absorption. Under the original mixed-real-data setting, derive the corresponding expectation.

**Equation provenance.** [T] Feedback loop \(Y_t=\mathcal I(L_t,x_t,c_t)\), \(B_{t+x}=\mathcal B(Y_t,E_t)\), \(A_{t+x}=\mathcal U(Z_{t+x},B_{t+x})\), \(Z_{t+x+1}=\mathcal T(Z_{t+x},A_{t+x})\), with \(x\ge1\). One recursive model generation corresponds to one feedback-loop transition, rather than one optimizer step. [A] A finite discrete support, \(M\) independent samples per generation, and exact matching of empirical frequencies: \(N_{t+1,i}\mid p_t\sim\mathrm{Bin}(M,q_t)\), \(q_{t+1}=N_{t+1,i}/M\). [R] \(\Pr(q_{t+1}=0\mid q_t)=(1-q_t)^M\), \(\mathbb E(q_{t+1}\mid q_t)=q_t\); the finite absorbing Markov chain reaches a point mass on one category. Mixing in genuine data at a fixed positive proportion makes missing categories recoverable, with probabilities calculated from the original mixture model. Random loss of support does not imply a declining mean frequency at each generation.

**TLI objects.** Local group (4) describes frozen inference, group (5) the delayed return of inference consequences as \(B_{t+x}\), and group (1) the subsequent learned-state transition, \(Z_{t+1}=\mathcal T(Z_t,\mathcal U(Z_t,B_t))\). Here \(t\) counts **model generations**, not optimizer steps. The generation, sampling and fitting maps use the original paper's definitions.

**Original-study conditions.** The finite-discrete, exact-fitting model of Shumailov et al. (*Nature*, 2024): category set \(\{1,\ldots,K\}\), fixed \(M\ge1\) observations per generation, \(M\) independent samples from \(p_t\), and an exact fit of \(p_{t+1}\) to their empirical distribution. No additional information-retention rate, noise-decay exponent or model-capacity law is introduced.

**Step-by-step derivation: loss of information in one generation.** For category \(i\), let \(q_t=p_t(i)\); its next-generation count \(N_{t+1,i}\) satisfies

\[
N_{t+1,i}\mid p_t\sim \operatorname{Binomial}(M,q_t),\qquad
q_{t+1}=\frac{N_{t+1,i}}{M}.
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

Consequently,

\[
\boxed{
\begin{aligned}
\Pr(q_{t+1}=0\mid q_t)&=(1-q_t)^M,\\
\mathbb E[q_{t+1}\mid q_t]&=q_t,\\
\operatorname{Var}(q_{t+1}\mid q_t)&=\frac{q_t(1-q_t)}{M}.
\end{aligned}}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

When \(q_t\ll1/M\), the probability of omitting that category is high. **The one-generation expected frequency remains unchanged**: collapse here concerns random support-set loss through finite sampling, rather than an assumed recurrence \(q_{t+1}=\rho q_t\) with \(\rho<1\).

**Step-by-step derivation: eventual absorption under repeated generation.** For the full distribution,

\[
p_{t+1}=\frac1M\,\operatorname{Multinomial}(M,p_t).
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

Once \(p_t(i)=0\), purely recursive sampling cannot regenerate category \(i\). If \(p_t=e_i\), a point mass on one category, then necessarily \(p_{t+1}=e_i\). Since \(M\) is fixed, empirical distributions take values on a finite grid. From every nonabsorbing state there is positive probability \(\sum_i p_t(i)^M>0\) that all observations take the same category; hence a point-mass absorbing state is eventually reached with probability one. The bounded-martingale property of each coordinate further gives

\[
\boxed{
p_t\xrightarrow[t\to\infty]{\mathrm{a.s.}}e_I,\qquad
\Pr(I=i)=p_0(i).
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

**Core conclusion.** Replacing every generation with finite samples from the previous generative model causes random contraction of support and eventual absorption into one category in the stated finite-discrete model. The result follows from its sampling–fitting map without requiring a uniform per-generation decay coefficient.

**A different data regime from the original research: continually mixing real data.** With a fixed proportion \(\alpha\in(0,1]\) from a real source distribution and the remainder generated by the preceding model, let category \(i\) have real probability \(r_i>0\). The mixture sampling probability is \(\widetilde q_t=(1-\alpha)q_t+\alpha r_i\); therefore

\[
\boxed{
\mathbb E[q_{t+1}]=(1-\alpha)\mathbb E[q_t]+\alpha r_i
=r_i+(1-\alpha)^{t+1}(q_0-r_i)
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

where the final expression takes \(t=0\) as the initial generation. At \(q_t=0\), the probability that category \(i\) reappears in the next generation is

\[
\Pr(q_{t+1}>0\mid q_t=0)=1-(1-\alpha r_i)^M>0.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Consequently, introducing real data makes a missing category a recoverable rather than absorbing state. The equations describe **long-run expectations and recovery probabilities**, while individual finite samples can still omit categories. Gerstgrasser et al. study a different retain-and-accumulate-data scheme and prove a bounded error for its corresponding linear model; these two data-generation processes have distinct recursions.

**Independent studies.** [Shumailov et al., *AI models collapse when trained on recursively generated data*, *Nature* 2024](https://doi.org/10.1038/s41586-024-07566-y); [Seddik et al., *How Bad is Training on Synthetic Data?* (2024)](https://arxiv.org/abs/2404.05090); [Gerstgrasser et al., *Is Model Collapse Inevitable?* (2024)](https://arxiv.org/abs/2404.01413).

**Internal experimental anchors.** TLI local groups (4)–(5) for inference output and delayed feedback, group (1) for state transition; RL-E06 for feedback-data allocation and sustained functional effects.

### 5.2.4 Spectral Bias: Frequency-dependent response and learning rates

**Derivation type:** Modal convergence rates recovered under the original theory's kernel-dynamics conditions.

**Equation provenance.** [T] \(\theta_{t+1}=\theta_t+\delta_t\) and \(R_{t,q}=m_q(\theta_{t+1})-m_q(\theta_t)\). [A] Squared loss, GD, local linearization \(J=\partial f/\partial\theta\) and a frozen kernel \(K=JJ^\top\). Substituting \(\delta_t=-\eta J^\top(f_t-y)\) gives \(\Delta f_t\approx-\eta K(f_t-y)\), with iteration along modes \(Kv_k=\lambda_kv_k\). [R] \(r_{k,t}\approx(1-\eta\lambda_k)^t r_{k,0}\). A low-frequency-first order follows when the original model's **Fourier-mode kernel spectrum** assigns larger eigenvalues to lower frequencies.

**TLI object.** An actual update produces a functional response \(R_q(\theta,\delta)\). First-order expansion of the current output vector \(f_\theta\) maps parameter actions into functional-output space.

**Original-study conditions.** Squared loss, gradient descent and the local linearization or fixed tangent-kernel assumptions used in the kernel-spectrum research. Let \(y\) be the targets, \(r_t=f_{\theta_t}-y\) the residual vector, and \(J_t\) the output-parameter Jacobian.

**Step-by-step derivation.**

\[
L=\tfrac12\|r_t\|^2,\quad
\delta_t=-\eta J_t^\top r_t,\quad
\Delta f_t\approx J_t\delta_t=-\eta J_tJ_t^\top r_t.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Define \(K_t=J_tJ_t^\top\). In a locally frozen regime with \(K_t=K\),

\[
r_{t+1}\approx(I-\eta K)r_t.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Diagonalize \(K\) using \(Kv_k=\lambda_kv_k\):

\[
\boxed{r_{k,t}\approx(1-\eta\lambda_k)^t r_{k,0}.}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

For \(0<\eta\lambda_k<1\), modes with larger \(\lambda_k\) have faster residual decay. In the original Spectral Bias setting, if the Fourier modes of the relevant input distribution and kernel have larger eigenvalues at low frequencies, a low-frequency-first learning order follows.

**Recovered conclusion.** The TLI action–response relation decomposes into explicit modal learning rates in a frozen-kernel regime. Frequency ordering is supplied by the kernel spectrum of the original model.

**Research comparison.** Kernel-spectrum and frequency-convergence studies by Basri et al. and Cao et al.; Fourier Features by Tancik et al.

**Internal anchors.** TL-E03, TL-E04 and TL-E07.

### 5.2.5 Benign Overfitting: Interpolating solutions and population risk

**Derivation type:** Population-risk decomposition for the minimum-norm solution under the original overparameterized linear-regression model.

**Equation provenance.** [T] Training transition \(\theta_{t+1}=\theta_t+\delta_t\). Population test risk can be treated as a continuous functional readout \(m_{\rm test}(\theta)\), so \(R_{t,\rm test}=m_{\rm test}(\theta_{t+1})-m_{\rm test}(\theta_t)\). [A] Original minimum-norm regression: \(y=X\beta^\star+\varepsilon\), zero-initialized GD on squared loss, \(p>n\), full-row-rank \(X\), and test covariance \(\Sigma\). GD selects \(\hat\beta=X^\top(XX^\top)^{-1}y\); substitute into population risk and take conditional expectation over independent mean-zero noise. [R] \(\beta^{\star\top}(I-P_X)\Sigma(I-P_X)\beta^\star+\sigma^2\operatorname{tr}[\Sigma X^\top(XX^\top)^{-2}X]\), an identity for **conditional expected risk** rather than for every sampled test outcome.

**TLI object.** Realized training actions select a final parameter state; training performance and population risk are distinct readouts of that state.

**Original-study conditions.** \(y=X\beta^\star+\varepsilon\), \(p>n\), \(X\in\mathbb R^{n\times p}\) with full row rank, squared loss, and GD from zero initialization converging to the minimum-norm interpolator. Test-input covariance is \(\Sigma\); training noise is independent, mean-zero, with covariance \(\sigma^2 I_n\). These are conditions of the original benign-overfitting and unregularized least-squares analyses.

**Step-by-step derivation.** Gradients lie in the column space of \(X^\top\), so zero-initialized GD converges to the interpolating solution

\[
\hat\beta=X^\top(XX^\top)^{-1}y.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Let \(P_X=X^\top(XX^\top)^{-1}X\). Substituting \(y\) gives

\[
\hat\beta-\beta^\star
=-(I-P_X)\beta^\star+X^\top(XX^\top)^{-1}\varepsilon.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Population excess squared prediction risk is
\(R=(\hat\beta-\beta^\star)^\top\Sigma(\hat\beta-\beta^\star)\)。
Taking conditional expectation over training noise eliminates the cross term:

\[
\boxed{
\begin{aligned}
\mathbb E_\varepsilon[R\mid X]
={}&\beta^{\star\top}(I-P_X)\Sigma(I-P_X)\beta^\star\\
&+\sigma^2\operatorname{tr}\!\left[
\Sigma X^\top(XX^\top)^{-2}X
\right].
\end{aligned}}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

**Recovered conclusion.** All training samples may be interpolated with zero training error, while population risk is determined by uncovered signal directions and amplified noise directions. Conditions on effective rank and covariance spectrum in the original research determine whether the latter contribution is small enough to yield benign overfitting.

**Research comparison.** [Hastie et al., *Annals of Statistics* 2022](https://doi.org/10.1214/21-AOS2133); effective-rank analysis by Bartlett et al.

**Internal anchors.** TL-E03 (receiving states and actual updates); TL-E08 (target-specific readouts).

### 5.2.6 Scaling Laws and Chinchilla: TLI Functional Response and Compute-Optimal Allocation

**Derivation type:** Substitute the original Chinchilla empirical loss law into the TLI response to obtain the marginal benefit of additional training tokens at fixed model size. Combine this with the original model-size term and compute constraint to recover compute-optimal allocation. The empirical power law and its exponents come from the original study.

**Equation provenance.** [T] Original TLI state transition and functional response. [A] Empirical loss law and compute budget from the original study. [R] Functional response, marginal benefit, optimal allocation and optimized-loss scaling.

**TLI starting equations [T].** Realized training actions change the learned state, and target responses are differences between readouts of the two states:

\[
Z_{t+1}=\mathcal T(Z_t,A_t),\qquad
\theta_{t+1}=\theta_t+\delta_t.
\qquad {}^{\scriptscriptstyle\text{[T]}}
\]

\[
R_{t,q}=m_q(L_{t+1})-m_q(L_t).
\qquad {}^{\scriptscriptstyle\text{[T]}}
\]

**Original-study conditions [A].** Hoffmann et al.'s empirical loss form and approximate compute cost are

\[
\mathcal L(N,D)=E+AN^{-\alpha}+BD^{-\beta},\quad
A,B,\alpha,\beta>0,\qquad C=6ND.
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

Here \(N\) is the parameter count, \(D\) the number of training tokens and \(C\) the compute budget. At fixed model size \(N\), let cumulative tokens \(D_t\) index the learned state attained by training; take the negative training loss as the TLI continuous functional readout:

\[
m_{\ell}(L_t)=-\mathcal L(N,D_t)\qquad(N\ \text{fixed}).
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

**Step 1: Substitute the original loss law into the TLI functional response [T]+[A]→[R].**

\[
\begin{aligned}
R_{t,\ell}
&=m_\ell(L_{t+1})-m_\ell(L_t)\\
&=-\mathcal L(N,D_{t+1})+\mathcal L(N,D_t)\\
&=B\left(D_t^{-\beta}-D_{t+1}^{-\beta}\right).
\end{aligned}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Let \(D_{t+1}=D_t+\Delta D\). The token-marginal functional improvement at fixed model size is

\[
\lim_{\Delta D\to0}\frac{R_{t,\ell}}{\Delta D}
=\frac{\partial m_\ell}{\partial D}
=\beta BD^{-\beta-1}.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

This calculation combines the TLI before/after functional difference with the original empirical loss law.

**Step 2: Apply the original compute budget and model-size effect.** Along a fixed-compute configuration curve:

\[
D=\frac{C}{6N},\qquad
\left.\frac{dD}{dN}\right|_C=-\frac DN.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

The original loss law gives the model-size marginal benefit \(\partial m_\ell/\partial N=\alpha AN^{-\alpha-1}\). Combine it with the token-marginal benefit from Step 1 and the compute constraint:

\[
\begin{aligned}
\left.\frac{dm_\ell}{dN}\right|_C
&=\frac{\partial m_\ell}{\partial N}
+\frac{\partial m_\ell}{\partial D}\frac{dD}{dN}\\
&=\alpha AN^{-\alpha-1}
-\beta BD^{-\beta-1}\frac{D}{N}.
\end{aligned}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Setting this expression to zero at the optimum yields

\[
\boxed{\alpha AN^{-\alpha}=\beta BD^{-\beta}.}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Hence:

\[
\boxed{
N_\star=
\left(\frac{\alpha A}{\beta B}\right)^{1/(\alpha+\beta)}
\left(\frac C6\right)^{\beta/(\alpha+\beta)},
\qquad
D_\star=\frac{C}{6N_\star}\propto C^{\alpha/(\alpha+\beta)}.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Substituting the optimal allocation back into the original loss law gives

\[
\boxed{\mathcal L_\star(C)-E\propto C^{-\alpha\beta/(\alpha+\beta)}.}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

**Recovered conclusion.** Specializing the TLI functional response with the original Chinchilla conditions yields a marginal improvement from training tokens; combining it with the original model-size term and compute budget recovers the compute-optimal configuration. Derivatives in \(N\) compare different compute configurations. The empirical loss exponents are supplied by Hoffmann et al.'s fitted law [A].

**Research comparison.** [Hoffmann et al., *Training Compute-Optimal Large Language Models* (2022)](https://arxiv.org/abs/2203.15556); empirical scaling laws by Kaplan et al.

**Internal experimental anchors.** TL-E03 (actions and receiving states), TL-E04 (functional response), TL-E07 (continuing reorganization) and cross-architecture TLI tests.

### 5.2.E1 (exploratory, outside the fourteen): Scaling from TLI Support, Capability and Loss to a Solvable Spectral Model

**Status: EXPLORATORY — separate mathematical research beyond the fourteen formal recoveries.** Section 5.2.6 inserts Hoffmann et al.'s fitted loss law to obtain compute-optimal allocation. This section instead considers a **solvable Gaussian-sequence and orthogonal-spectral model**, computes functional-support contributions and derives its own loss–scale asymptotics. Conditions include Gaussian coefficient observations, orthogonal features, squared loss and specified spectral assumptions; the evidence consists of analytical derivations.

**Equation provenance.** [T] The current ICML coupled equations and registered component-intervention support (see [unified dynamics](TLI_UNIFIED_DYNAMICS.md)). [A] Gaussian-sequence observations, orthogonal features, spectral decay, gradient descent and the specific truncation/budget conditions used below. [R] Relations obtained by substitution. The regression readout and Shapley coalition values specialize general TLI formulas to this mathematical model.

**TLI starting equations [T].** Persistent learned states, realized actions, target responses, intervention-measured support, capability and frozen inference follow

\[
\begin{gathered}
Z_t=(L_t,\omega_t),\quad A_t=\mathcal U(Z_t,B_t),\quad
Z_{t+1}=\mathcal T(Z_t,A_t),\\
\theta_{t+1}=\theta_t+\delta_t,\qquad
R_{t,q}=m_q(L_{t+1})-m_q(L_t),\\
P_{t,q}=\mathcal P_q(L_t;\mathcal J_q),\qquad
\Delta P_{t,q}=P_{t+1,q}-P_{t,q},\qquad
C_{t,q}=\chi_q(m_q(L_t)),\\
S_{x,c}^{\mathrm{active}}=\Pi_{x,c}(L^*),\qquad
Y_{x,c}=H_{x,c}(S_{x,c}^{\mathrm{active}}),\qquad
\Delta_{\mathrm{inf}}L=0.
\end{gathered}
\qquad {}^{\scriptscriptstyle\text{[T]}}
\]

This section studies supervised training rather than the closed feedback loop. The task's loss and capability readouts are computed from its own outputs and decision rule, keeping capability distinct from parameter count, mode count and loss.

**Solvable classical conditions [A].** Use independent \(x_k\sim N(0,1)\) in a Gaussian orthogonal basis. The true function is \(y=f^*(x)=\sum_{k\ge1}a_kx_k\) with \(\sum_ka_k^2<\infty\). The parameterized model of size \(N\) can represent at most the first \(N\) modes, while \(M\le N\) modes are actually enabled. Frozen inference recruits and combines their learned outputs:

\[
\Pi_x(L^*)=(z_1,\ldots,z_M),\quad z_k=\theta_kx_k,\qquad
H_x(\Pi_x(L^*))=\widehat y(x)=\sum_{k=1}^{M}z_k.
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

To calculate data effects exactly, use a **Gaussian-sequence observation model**: each enabled mode's observed coefficient is \(\widetilde a_{k,D}=a_k+\sigma D^{-1/2}\xi_k\), where independent \(\xi_k\sim N(0,1)\) are also independent of the test input. Here \(D\) is the **effective observation count per coefficient**, with a definition distinct from raw language-model training tokens or ordinary i.i.d.-sample least squares. Training minimizes \(Q_M(\theta)=\frac12\sum_{k\le M}(\theta_k-\widetilde a_{k,D})^2\), from zero initialization at step size \(0<\eta<2\).

**Step 1: Link TLI functional support to capability and loss through fixed-coalition interventions [T]+[A]→[R].** For target \(q=(x,y)\) and tolerated regression error \(\varepsilon>0\), define this task's readout and capability rule as

\[
m_q(L)=\varepsilon^2-(y-\widehat y)^2,\qquad
C_q(L)=\mathbf1[m_q(L)>0].
\qquad {}^{\scriptscriptstyle\text{[T]}}
\]

Under fixed intervention protocol \(\mathcal J_q\), enumerate every coalition \(S\subseteq\{1,\ldots,M\}\) of registered modes. The coalition readout is

\[
v_q(S;L)=\varepsilon^2-\left(y-\sum_{k\in S}z_k\right)^2.
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

Define signed functional contributions \(\varphi_{k,q}\) using the paper's coalition Shapley intervention measure. Averaging marginal contributions over coalitions and the Shapley completeness identity give the **exact equations**:

\[
\boxed{\varphi_{k,q}=z_k(2y-\widehat y),\qquad
\sum_{k=1}^{M}\varphi_{k,q}=2y\widehat y-\widehat y^2.}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\tag{E1}
\]

For the all-disabled baseline \(b_q=v_q(\varnothing;L)=\varepsilon^2-y^2\), we have
\(m_q(L)=b_q+\sum_k\varphi_{k,q}(L)\). Comparing the same target \(q\) before and after actual training leaves \(b_q\) fixed, so the realized TLI functional response is

\[
\boxed{
R_{t,q}=\sum_k\Delta\varphi_{t,k,q},\qquad
\Delta\ell_{t,q}=-\tfrac12 R_{t,q}
=-\tfrac12\sum_k\Delta\varphi_{t,k,q}.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\tag{E2}
\]

Thus the task's squared loss and capability readout arise from the **same complete support decomposition**:

\[
\boxed{
\ell_q(L)=\tfrac12(y-\widehat y)^2
=\tfrac12\left(y^2-\sum_k\varphi_{k,q}(L)\right),\qquad
C_q(L)=\mathbf1\left[\sum_k\varphi_{k,q}(L)>y^2-\varepsilon^2\right].
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\tag{E3}
\]

These identities retain every signed contribution, the all-disabled baseline and the same fixed coalition protocol. A normalized positive-only support share has a different definition. The model's forward output is additive, while the non-additive coalition interaction in its readout arises from the **squared readout**.

**Step 2: Compute the evolution of support contributions under actual TLI training transitions [T]+[A]→[R].** Classical gradient descent specializes the action to
\(\delta_{t,k}=-\eta(\theta_{t,k}-\widetilde a_{k,D})\)。
Substitute \(\theta_{t+1,k}=\theta_{t,k}+\delta_{t,k}\) and write \(s_t=1-(1-\eta)^t\). Then

\[
\boxed{\theta_{t,k}=s_t\widetilde a_{k,D}.}
\qquad {}^{\scriptscriptstyle\text{[A]}}
\tag{E4}
\]

Using (E1), take expectation first over independent Gaussian test inputs and then over coefficient-observation noise:

\[
\begin{aligned}
\mathbb E_{x,\xi}[\varphi_{t,k,q}]
&=2a_k\mathbb E_\xi[\theta_{t,k}]
-\mathbb E_\xi[\theta_{t,k}^2]\\
&=\boxed{(2s_t-s_t^2)a_k^2-\frac{s_t^2\sigma^2}{D}}.
\end{aligned}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\tag{E5}
\]

At convergence, as \(s_t\to1\),

\[
\boxed{\mathbb E[\varphi_{\infty,k}]=a_k^2-\sigma^2/D.}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\tag{E6}
\]

Training-dependent support contributions enter the loss calculation directly. An expected functional contribution can be negative when coefficient-estimation error offsets its net contribution under this squared readout.

**Step 3: Derive average loss from functional support and then impose classical spectral conditions [T]+[A]→[R].** At any training time, (E3) gives exactly

\[
\begin{aligned}
\mathbb E\mathcal L_t(M,D)
&=\frac12\left(\sum_{k\ge1}a_k^2
-\sum_{k\le M}\mathbb E[\varphi_{t,k}]\right)\\
&=\frac12\left[
\sum_{k>M}a_k^2+
(1-s_t)^2\sum_{k\le M}a_k^2+
\frac{s_t^2\sigma^2M}{D}\right].
\end{aligned}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\tag{E7}
\]

At convergence, assume the classical power-law spectral condition \(a_k^2=\Lambda k^{-(1+\alpha)}\), with \(\Lambda>0\), \(\alpha>0\). Then

\[
\begin{aligned}
\mathbb E\mathcal L_\infty(M,D)
&=\frac12\left[
\Lambda\sum_{k>M}k^{-(1+\alpha)}
+\frac{\sigma^2M}{D}\right]\\
&\sim \boxed{\frac{\Lambda}{2\alpha}M^{-\alpha}
+\frac{\sigma^2M}{2D}}
\qquad(M\to\infty).
\end{aligned}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\tag{E8}
\]

Here the **power-law spectrum is a classical target-function assumption [A]**; the loss scaling is recovered [R] by substituting it into the TLI support–loss relation. Training all \(N\) modes to convergence, \(M=N\), gives

\[
\boxed{
\mathbb E\mathcal L_\infty(N,D)
\sim\frac{\Lambda}{2\alpha}N^{-\alpha}
+\frac{\sigma^2N}{2D}.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\tag{E9}
\]

Equation (E9) provides an explicit model–data scale relationship. Its form differs from the separable additive empirical Chinchilla law.

**Step 4: Under classical optimal spectral truncation, derive two-variable Chinchilla-like scaling orders [A]→[R].** Treat \(M\le N\) as the selectable number of effectively learned modes. Setting the derivative of (E8) to zero gives

\[
M_D=\left(\frac{\Lambda D}{\sigma^2}\right)^{1/(\alpha+1)},\qquad
M_*=\min\{N,M_D\}
\quad\text{(continuous approximation; choose a neighboring integer mode count)}.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

When \(N,D\) grow jointly with \(\sigma^2>0\) under this truncation rule, compare representation and estimation errors to obtain

\[
\boxed{
\mathbb E\mathcal L_\infty(N,D;M_*)
=
\Theta\left(
N^{-\alpha}+D^{-\alpha/(\alpha+1)}
\right).
}
\qquad {}^{\scriptscriptstyle\text{[A]}}
\tag{E10}
\]

Equation (E10) describes the **power-law order in two scaling variables** under the stated model and truncation conditions. Its coefficients and exponents are model-specific; the result is an asymptotic scaling specialization rather than a fit to the Chinchilla empirical coefficients.

**Step 5: Relate capability success to loss under the same fixed learned state [T]+[A]→[R].** Fix a trained state \(L\). For independent test inputs, the prediction error is Gaussian:

\[
e(x;L)=f^*(x)-\widehat y(x)\mid L\sim N(0,V(L)),
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

\[
V(L)=\sum_{k\le M}(a_k-\theta_k)^2+\sum_{k>M}a_k^2,\qquad
\overline{\mathcal L}(L)=\tfrac12V(L).
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Therefore, for the specified regression-error tolerance \(\varepsilon>0\),

\[
\boxed{
\Pr_x(C_q=1\mid L)
=\Pr_x(|e|<\varepsilon\mid L)
=\operatorname{erf}\left(\frac{\varepsilon}{2\sqrt{\overline{\mathcal L}(L)}}\right).
}
\qquad {}^{\scriptscriptstyle\text{[A]}}
\tag{E11}
\]

This is an exact relationship between capability success probability and average squared loss **conditional on the fixed learned state**. For \(V(L)=0\), take the limiting success probability 1. Additional averaging over training noise passes through the nonlinear \(\operatorname{erf}\) according to its expectation, rather than by substituting \(\mathbb E_L[\overline{\mathcal L}(L)]\) into the function. The readout and result are specific to this regression model.

**Step 6: Optional compute-optimal relation [A]→[R].** Analyze only case (E9), in which **all \(N\) modes participate in training and computation**, with this model's budget approximation \(\mathcal K=\kappa ND\). Substitute \(D=\mathcal K/(\kappa N)\):

\[
\mathbb E\mathcal L_\infty(N,\mathcal K)
\sim\frac{\Lambda}{2\alpha}N^{-\alpha}
+\frac{\sigma^2\kappa}{2\mathcal K}N^2.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Differentiate with respect to \(N\) and set the derivative to zero:

\[
\boxed{
N_*\asymp\mathcal K^{1/(\alpha+2)},\qquad
D_*\asymp\mathcal K^{(\alpha+1)/(\alpha+2)},\qquad
\mathcal L_*(\mathcal K)\asymp\mathcal K^{-\alpha/(\alpha+2)}.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\tag{E12}
\]

This budget calculation uses the all-mode regime of (E9), distinct from the truncated-training condition in (E10). Its exponent is determined by the current model's assumptions.

**Exploratory results and applicable conditions.** (E1)–(E3) connect TLI intervention support, functional response, frozen inference and target capability/loss readouts. (E4)–(E8) compute how actual updates form support contributions and affect average loss. (E9)–(E12) derive testable scaling relationships under explicit classical spectrum and training-selection conditions. The solvable setting uses Gaussian-sequence observations, orthogonal linear features, a clean teacher test target and squared loss. The formulas describe this model, rather than the full training dynamics of Transformers, cross-entropy, mult-token conditional distributions or realistic corpus statistics. Section 5.2.6 retains the separate Chinchilla empirical loss-law input.

**Mathematical check.** (E1)–(E3) were checked numerically by enumerating all coalitions of four components; the Shapley decomposition and direct squared loss agreed within floating-point precision. (E4)–(E12) are analytic derivations with explicit steps and have not been independently tested against real scaling curves.

**Related research.** [Bahri et al., *Explaining neural scaling laws*, *PNAS* 2024, DOI:10.1073/pnas.2311878121](https://doi.org/10.1073/pnas.2311878121) (random-feature and spectral scaling); [Bordelon, Atanasov and Pehlevan, *A Dynamical Model of Neural Scaling Laws*, ICML 2024](https://proceedings.mlr.press/v235/bordelon24a.html) (solvable random-feature training dynamics); [Hoffmann et al., *Training Compute-Optimal Large Language Models*, 2022](https://arxiv.org/abs/2203.15556) (empirical Chinchilla law used as a separate comparison).

**Experimental anchors for the TLI relations.** TL-E03/E04 (realized updates and finite responses), TL-E06/E07 (intervention-defined support and reorganization), TL-E08 (capability boundaries), INF-E01 and INF-G01/G02 (frozen inference and trained component versions). The exploratory spectral exponents in (E8)–(E12) are derived under [A], separately from these empirical measurements.

### 5.2.7 Dynamical Isometry: Transmission of Training Actions through Deep Networks

**Derivation type:** Direct derivation from layered composition and the chain rule in the original network.

**Equation provenance.** [T] Functional response \(R_q=m_q(\theta+\delta\theta)-m_q(\theta)\), with local form \(R_q\approx\nabla_\theta m_q^\top\delta\theta\). [A] The original layered network \(h^{\ell+1}=F_\ell(h^\ell,\theta_\ell)\), the differentiable chain rule and cross-layer Jacobian \(J_{L\leftarrow\ell+1}\). Propagating \(\delta h^{\ell+1}=B_\ell\delta\theta_\ell\) gives [R] \(\delta f\approx\sum_\ell J_{L\leftarrow\ell+1}B_\ell\delta\theta_\ell\), a **local first-order response**. Dynamical isometry constrains transmission through the relevant Jacobian singular values. If the Jacobian has a nontrivial nullspace, the minimum norm gain on the **entire space** is zero; a positive lower bound from the smallest nonzero singular value applies only on the suitable restricted subspace.

**TLI object.** An actual parameter increment \(\delta\theta\) changes the network output \(f_\theta\), with its local response conditioned by the current receiving state.

**Original-study conditions.** A differentiable layered network \(h^{\ell+1}=F_\ell(h^\ell,\theta_\ell)\), its interlayer Jacobians and the singular-value conditions studied in dynamical isometry.

**Step-by-step derivation.** For a small parameter perturbation at layer \(\ell\), first write

\[
\delta h^{\ell+1}\approx
B_\ell\delta\theta_\ell,\qquad
B_\ell=\frac{\partial F_\ell}{\partial\theta_\ell}.
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

The remaining layers transmit the change by the chain rule. Let \(J_{L\leftarrow\ell+1}=\partial h^L/\partial h^{\ell+1}\). Then

\[
\boxed{\delta f\approx
\sum_{\ell}J_{L\leftarrow\ell+1}B_\ell\delta\theta_\ell.}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Likewise, for a perturbation \(v\) of the activation leaving layer \(\ell\),

\[
\|J_{L\leftarrow\ell}v\|
\in[\sigma_{\min}^{\mathrm{all}}(J)\|v\|,\ \sigma_{\max}(J)\|v\|]
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Here \(\sigma_{\min}^{\mathrm{all}}(J)=\inf_{\|v\|=1}\|Jv\|\), which is zero when \(J\) has a nontrivial nullspace. A lower bound from the smallest nonzero singular value applies on the effective subspace orthogonal to that nullspace. Backpropagated gradients travel through the corresponding transpose Jacobian. When relevant nonzero singular values cluster near one, signals and gradients on those directions undergo little norm amplification or attenuation; strongly displaced spectra yield directional expansion or contraction.

**Recovered conclusion.** Dynamical isometry gives **conditions for transporting activations and gradients at a fixed state**, derived directly from the original network's composition. The parameter-to-activation Jacobian \(B_\ell\) also enters the response to an actual parameter update.

**Research comparison.** [Pennington, Schoenholz and Ganguli, NeurIPS 2017](https://arxiv.org/abs/1711.04735).

**Internal anchors.** TL-E03 (receiving state), TL-E04 (actual update paths), TL-E05 (update geometry).

### 5.2.8 Dropout: Adaptive Regularization from Random Feature Masking

**Derivation type:** Use independent Bernoulli feature dropout and generalized linear model (GLM) assumptions from the original dropout theory to derive a label-independent regularizer. In Gaussian linear regression, an original GLM special case, derive an exact data-dependent diagonal quadratic penalty and its effects on actual training updates.

**Equation provenance.** [T] Training transition \(\theta_{t+1}=\theta_t+\delta_t\) and response \(R_{t,q}=m_q(\theta_{t+1})-m_q(\theta_t)\). [A] Independent Bernoulli feature masks, inverse scaling \(\tilde x_j=z_jx_j/r\) and a convex GLM log-partition function \(A(u)\), as in Wager et al. Taking mask expectation preserves the label-linear term and gives [R] \(\overline L_{\rm drop}=L_0+\frac1n\sum_i\{\mathbb E_zA(w^\top\tilde x_i)-A(w^\top x_i)\}\ge L_0\). For the Gaussian linear case \(A(u)=u^2/2\), the penalty is exactly \((1-r)/(2r)\sum_j s_j^2w_j^2\). [T→A] Substitution into an update gives \(\mathbb E_z[\delta_t\mid w_t]=-\eta\nabla\overline L_{\rm drop}\). A single sampled mask gives its own realized update; a general nonlinear network has a different inference model-averaging relation.

**TLI objects.** Local groups (1)–(2) write training as \(A_t=\mathcal U(Z_t,B_t)\) and \(\theta_{t+1}=\theta_t+\delta_t\). Randomly masking features during training changes the formation of actual updates; group (3) measures their continuous target responses, and group (4) concerns subsequent frozen inference.

**Original-study conditions.** Wager, Wang and Liang (NeurIPS 2013) study **independent feature dropout** in generalized linear models. Each mask \(z_{ij}\) is independent with distribution \(\operatorname{Bernoulli}(r)\), for keep probability \(r\in(0,1]\). Inverse scaling is \(\widetilde x_{ij}=x_{ij}z_{ij}/r\), so \(\mathbb E_z[\widetilde x_i]=x_i\). The per-example GLM negative log likelihood is

\[
\ell_i(w;x_i,y_i)=A(w^\top x_i)-y_iw^\top x_i-\log h(y_i),
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

Here \(A\) is the convex log-partition function of the original GLM; the derivation uses this dropout noise model and no added regularization term.

**Step 1: Compute the dropout-averaged objective under the original masking mechanism.** Let \(L_0(w)=n^{-1}\sum_i\ell_i(w;x_i,y_i)\). Averaging over masks gives

\[
\begin{aligned}
\overline L_{\rm drop}(w)
&=\frac1n\sum_i\mathbb E_z[\ell_i(w;\widetilde x_i,y_i)]\\
&=L_0(w)+\mathcal R_{\rm drop}(w),\\
\boxed{\mathcal R_{\rm drop}(w)
&=\frac1n\sum_i\left[
\mathbb E_z A(w^\top\widetilde x_i)-A(w^\top x_i)
\right]\ge0.}
\end{aligned}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

The final inequality follows from convexity of \(A\), \(\mathbb E_z[\widetilde x_i]=x_i\), and Jensen's inequality. The label-linear term retains its expectation under masking, so \(\mathcal R_{\rm drop}\) contains no \(y_i\). This is the exact decomposition under the original GLM assumptions.

**Step 2: Calculate the regularizer for Gaussian linear regression, a case included in the original GLM.** With unit-normalized fixed variance, \(A(u)=u^2/2\) and squared loss \(\ell_i=\tfrac12(y_i-w^\top x_i)^2+\mathrm{const}\). Independent masks give

\[
\operatorname{Var}_z(w^\top\widetilde x_i)
=\frac{1-r}{r}\sum_{j=1}^d w_j^2x_{ij}^2.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Let \(s_j^2=n^{-1}\sum_i x_{ij}^2\). Then

\[
\boxed{
\overline L_{\rm drop}(w)
=L_0(w)+\frac{1-r}{2r}\sum_{j=1}^d s_j^2w_j^2.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

This is the **exact connection between dropout and data-dependent diagonal \(L_2\) regularization**. Penalty coefficients depend on each feature's empirical second moment and the original dropout keep probability.

**Step 3: Substitute into the actual TLI update to obtain functional response.** Use the original gradient-descent action for this expected objective (the conditional mean gradient of one-mask SGD matches its gradient). With \(D_s=\operatorname{diag}(s_1^2,\ldots,s_d^2)\),

\[
\boxed{
\begin{aligned}
\mathbb E_z[\delta_t\mid w_t]
&=-\eta\nabla_w\overline L_{\rm drop}(w_t)\\
&=-\eta\left[\nabla L_0(w_t)+\frac{1-r}{r}D_sw_t\right].
\end{aligned}}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

The expectation holds **at fixed receiving state and training data, averaging only over dropout masks**. One actual training step uses the increment \(\delta_t\) formed from the mask sampled on that step.

For a linear model with continuous readout \(m_q(w)=w^\top x_q\) at fixed query \(x_q\), the TLI response is exactly

\[
\boxed{
R_{t,q}
=m_q(w_t+\delta_t)-m_q(w_t)
=x_q^\top\delta_t.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Random masking therefore changes actual training actions and creates query-dependent functional responses. The expected update includes the adaptive shrinkage term calculated above. Regularization is the deterministic average effect of the original stochastic training mechanism on the state transition.

**Step 4: Relate dropout training to frozen inference.** In the linear model, since \(\mathbb E_z[\widetilde x]=x\),

\[
\boxed{
\mathbb E_z[f_w(\widetilde x)]=f_w(x)=w^\top x.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

For this linear model, the mean prediction of the randomly masked training submodels **equals exactly** the unmasked inference prediction at frozen weights. The original dropout paper treats test-time rescaling or ensemble averaging in nonlinear deep networks using approximations with different conditions.

**Core recovered relationship.** Under the original GLM and independent-dropout conditions, **random feature masking ⇒ a nonnegative label-independent regularizer**. Under the Gaussian linear specialization this yields an **exact adaptive quadratic penalty ⇒ changed actual gradient update ⇒ query-conditioned functional response**. This connects directly to the TLI training–learning–frozen-inference chain.

**Independent studies.** [Srivastava et al., *Dropout: A Simple Way to Prevent Neural Networks from Overfitting*, JMLR 2014](https://www.jmlr.org/papers/v15/srivastava14a.html); [Wager, Wang and Liang, *Dropout Training as Adaptive Regularization*, NeurIPS 2013](https://papers.nips.cc/paper_files/paper/2013/hash/38db3aed920cf82ab059bfccbd02be6a-Abstract.html).

**Internal anchors.** TL-E03 (actual-action formation and receiver dependence), TL-E04 (finite-amplitude response) and INF-E01 (query-dependent frozen inference).

### 5.2.9 Catastrophic Forgetting: Exact Boundary for Loss of a Previously Correct Target

**Derivation type:** An exact consequence of TLI functional responses and capability readouts, combined with gradient conditions from the original forgetting literature.

**Equation provenance.** [T] Response \(R_{t,q}=m_q(L_{t+1})-m_q(L_t)\) and capability readout \(C_{t,q}=\mathbf1[m_q(L_t)>0]\). Exact telescoping gives \(m_q(L_T)=m_q(L_0)+\sum_{t<T}R_{t,q}\). For an initially correct target with \(m_q(L_0)>0\), [R] failure occurs exactly when \(\sum_{t<T}R_{t,q}\le-m_q(L_0)\). [A] With the SGD action \(\delta_t=-\eta\nabla L_{\rm new}(\theta_t)\) and differentiable readouts from the original continual-learning setting, the **first-order approximation** is \(R_{t,q}\approx-\eta\nabla m_q^\top\nabla L_{\rm new}\); the change in old-task loss is \(\Delta L_{\rm old}\approx-\eta g_{\rm old}^\top g_{\rm new}\). The accumulated boundary identity is exact; the gradient relation is local and approximate.

**TLI object.**

\[
R_{t,q}=m_q(\theta_{t+1})-m_q(\theta_t),\qquad
C_{t,q}=\mathbf1[m_q(\theta_t)>0].
\qquad {}^{\scriptscriptstyle\text{[T]}}
\]

**Step 1: Exact accumulation of functional responses.**

\[
\boxed{
m_q(\theta_T)=m_q(\theta_0)+\sum_{t=0}^{T-1}R_{t,q}.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

For a previously correct target \(m_q(\theta_0)>0\), failure at time \(T\) occurs exactly when

\[
\boxed{
\sum_{t=0}^{T-1}R_{t,q}\leq-m_q(\theta_0).
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

The same identity describes retention and recovery: later positive responses can move the margin back across zero and restore correctness.

**Step 2: Substitute the original continual-learning SGD action.** For new-task loss \(L_{\rm new}\), the increment is \(\delta_t=-\eta g_{\rm new}\). With a differentiable readout and a sufficiently small step,

\[
R_{t,q}\approx-\eta\nabla_\theta m_q(\theta_t)^\top g_{\rm new}.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

For a differentiable old-task loss \(L_{\rm old}\),

\[
\boxed{
\Delta L_{\rm old}
\approx-\eta g_{\rm old}^\top g_{\rm new}.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

A negative gradient inner product causes a positive first-order change in old-task loss under the current new-task update; a positive inner product causes the opposite sign. A single action can change many target margins because the tasks share parameters.

**Recovered conclusion.** Forgetting is the computational event in which a previously correct target crosses its readout boundary. Methods that protect old tasks act by changing the trajectory of accumulated functional responses to those targets.

**Research comparison.** Elastic Weight Consolidation (Kirkpatrick et al.); Gradient Episodic Memory (Lopez-Paz and Ranzato); gradient projection and experience replay.

**Internal anchors.** TL-E03, TL-E07 and TL-E08; [RL-E06](experiments/gfg_rl_selective_positive_feedback_dose_recovery_v1/RESULTS.md), which records mastery, subsequent deterioration and recovery.

### 5.2.10 Grokking: Different Crossing Times for Training and Generalization Readouts

**Derivation type:** Use the original solvable linear teacher–student grokking model, gradient flow and random-matrix spectrum to derive training/test loss trajectories and delayed generalization times.

**Equation provenance.** [T] The original state update \(\theta_{t+1}=\theta_t+\delta_t\), specialized to the original gradient-flow limit with continuous state \(D(t)\); TLI response \(R_{t,q}=m_q(L_{t+1})-m_q(L_t)\) and capability \(C_{t,q}=\chi_q(m_q(L_t))\). [A] Levi, Beck and Bar-Sinai's scalar-output (\(d_{\rm out}=1\)) Gaussian linear teacher–student model, zero weight decay, squared-loss gradient flow, training covariance \(\Sigma_{\rm tr}\), population covariance \(I\), and the original Marčenko–Pastur spectrum and accuracy threshold. The update yields \(D(t)=e^{-2\eta_0\Sigma_{\rm tr}t}D_0\), with readouts \(L_{\rm tr}(t)=D_0^\top e^{-4\eta_0\Sigma_{\rm tr}t}\Sigma_{\rm tr}D_0\) and \(L_{\rm gen}(t)=D_0^\top e^{-4\eta_0\Sigma_{\rm tr}t}D_0\). At the original threshold \(L=\epsilon/4\), one can use TLI readout \(m_q=\epsilon/4-L_q\) and \(\chi_q(m)=\mathbf1[m\ge0]\). Original spectral-edge asymptotics yield [R] \(\Delta t_{\rm grok}\simeq-\ln(1-\sqrt\lambda)/[2\eta_0(1-\sqrt\lambda)^2]\), for \(0<\lambda<1\). This time expression is conditional on that asymptotic model.

**TLI objects.** The actual parameter action (local group 2) and continuous response and capability readout (group 3). Training and test targets are **different readouts of the same learned state**, and their threshold crossings can occur at different times.

**Original-study conditions.** Levi, Beck and Bar-Sinai (ICLR 2024) use an unbiased linear teacher–student setup: \(x\sim\mathcal N(0,I_d)\), teacher parameters \(T\) and student parameters \(S_t\); squared loss, scalar output, \(n\) fixed training examples, zero weight decay, gradient flow, \(\Sigma_{\rm tr}=\frac1n\sum_jx_jx_j^\top\) and population covariance \(I_d\). In the high-dimensional limit \(d,n\to\infty\), the ratio \(\lambda=d/n\in(0,1)\) is fixed, and the derivation uses the original Marčenko–Pastur law, isotropic initialization and error threshold \(\epsilon\).

**Step 1: Substitute the original optimizer action into the TLI transition.** Let \(D_t=S_t-T\). The two continuous training and test readouts are

\[
L_{\rm tr}(D)=D^\top\Sigma_{\rm tr}D,\qquad
L_{\rm gen}(D)=D^\top D.
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

Under the original gradient flow and time-scale parameter \(\eta_0\),

\[
\dot D(t)=-2\eta_0\Sigma_{\rm tr}D(t),\qquad
\boxed{D(t)=e^{-2\eta_0\Sigma_{\rm tr}t}D_0}.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Substitution into the two readouts of the same state gives the **exact** loss evolution:

\[
\boxed{
\begin{aligned}
L_{\rm tr}(t)&=D_0^\top e^{-4\eta_0\Sigma_{\rm tr}t}\Sigma_{\rm tr}D_0,\\
L_{\rm gen}(t)&=D_0^\top e^{-4\eta_0\Sigma_{\rm tr}t}D_0.
\end{aligned}}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

**Step 2: Use the covariance spectrum of the original paper.** Let \(\nu\) follow the Marčenko–Pastur spectrum for \(\lambda=d/n\). Under the original isotropic initial direction and high-dimensional approximation,

\[
L_{\rm tr}(t)\approx\mathbb E_\nu[\nu e^{-4\eta_0\nu t}],\qquad
L_{\rm gen}(t)\approx\mathbb E_\nu[e^{-4\eta_0\nu t}].
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

The lower positive spectral edge is \(\nu_-=(1-\sqrt\lambda)^2\). When \(\eta_0t\gg\sqrt\lambda/(1-\sqrt\lambda)^2\), the original spectral-edge asymptotics give

\[
\boxed{
L_{\rm tr}(t)\simeq
\frac{e^{-4\eta_0(1-\sqrt\lambda)^2t}}
{16\sqrt{\pi}\lambda^{3/4}(\eta_0t)^{3/2}},
\qquad
L_{\rm gen}(t)\simeq\frac{L_{\rm tr}(t)}{(1-\sqrt\lambda)^2}.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

**Step 3: Calculate the delayed threshold-crossing time using the original accuracy readout.** Correctness on an input is defined by squared error below \(\epsilon\):

\[
C_x(t)=\mathbf1[(D(t)^\top x)^2<\epsilon].
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

Under the corresponding Gaussian-readout approximation,

\[
A(t)=\operatorname{erf}\!\left(\sqrt{\frac{\epsilon}{2L(t)}}\right).
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

The original paper uses \(A=\operatorname{erf}(\sqrt2)\approx95.45\%\) as its crossing criterion, corresponding to \(L(t^*)=\epsilon/4\). Solve for when \(L_{\rm tr}(t_{\rm tr}^*)\) and \(L_{\rm gen}(t_{\rm gen}^*)\) reach the threshold. In the small-\(\epsilon\) regime:

\[
\boxed{
\Delta t_{\rm grok}=t_{\rm gen}^*-t_{\rm tr}^*
\simeq-\frac{\ln(1-\sqrt\lambda)}
{2\eta_0(1-\sqrt\lambda)^2}>0,\quad 0<\lambda<1.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

**Core conclusion.** Training and test performance follow the same continuous parameter trajectory. With the original model's distinct readout geometries and common correctness criterion, test correctness can rise long after training correctness. The delay is quantitatively determined by the original conditions in \(\lambda,\eta_0\).

**Research comparison.** [Levi, Beck and Bar-Sinai, *Grokking in Linear Estimators—A Solvable Model that Groks without Understanding*, ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/8c0a85ee3eddb1858d9142f0d51d67b2-Abstract-Conference.html); [Žunkovič and Ilievski, *Grokking phase transitions in learning local rules with gradient descent*, JMLR 2024](https://www.jmlr.org/papers/v25/22-1228.html).

**Internal anchors.** TL-E03 (receiving-state-dependent response), TL-E07 (continuing support reorganization), TL-E08 (continuous margin and discrete readout) and TL-P01 (target-boundary prediction).

### 5.2.11 Maximal Update Parameterization (μP): Finite Functional Updates as Width Grows

**Derivation type:** Use the original MLP parameterization and SGD regime in Tensor Programs IV to compute update scaling and output stability, then apply the paper's first-layer modification to describe conditions for learning in all layers.

**Equation provenance.** [T] Actual action \(\theta_{t+1}=\theta_t+\delta_t\) and response \(R_{t,q}=m_q(\theta_t+\delta_t)-m_q(\theta_t)\). [A] The linear MLP parameterization in Appendix E.1 of Yang and Hu's *Tensor Programs IV*, with output scaling \(f=n^{-1/2}v\bar h\), specified weight scales and learning rate \(\eta_n\propto n^{-c}\). Applying the chain rule to the **same SGD action** gives [R] \(\Delta\bar h_j=\Theta(n^{-c})\) and \(\Delta f=\Theta(n^{-c})\). At \(c=0\) both are \(\Theta(1)\) in one step. These are **one-step scaling statements for the specified parameterization**; the complete μP family and μTransfer are separate results in the original work.

**TLI objects.** Actual update \(\theta_{t+1}=\theta_t+\delta_t\) and response \(R_q(\theta,\delta)=m_q(\theta+\delta)-m_q(\theta)\). Across widths, compare the realized parameter action's effect in **functional and representation space**, in addition to the parameter increment.

**Original-study conditions.** The two-hidden-layer linear MLP example and SGD width limit in Appendix E of Yang and Hu (ICML 2021): width \(n\to\infty\), \(h=U\xi\), \(\bar h=Wh\), \(h^\top h=\Theta(n)\); original middle- and output-layer Gaussian initialization scale \(n^{-1/2}\); output-loss derivative \(\chi=\mathcal L'(f,y)=\Theta(1)\). Output scaling is \(f=n^{-1/2}v\bar h\), learning rate \(\eta_n\propto n^{-c}\), with one realized SGD action on a fixed input.

**Step 1: Substitute the original parameterization and actual action into the TLI response.** For a middle-layer SGD update, the original Appendix E.1 obtains by chain-rule differentiation

\[
\Delta\bar h
=-n^{-c-1/2}\chi\,v^\top(h^\top h),\qquad
\Delta f
=-n^{-c-1}\chi(vv^\top)(h^\top h).
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

At the original initialization scale, each \(v_j=\Theta(n^{-1/2})\), \(vv^\top=\Theta(1)\), and \(h^\top h=\Theta(n)\). Hence

\[
\boxed{
\Delta\bar h_j=\Theta(n^{-c}),\qquad
\Delta f=\Theta(n^{-c}).
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

If \(c>0\), feature and output updates vanish at fixed step count as width grows. If \(c=0\), then

\[
\boxed{\Delta\bar h_j=\Theta(1),\qquad \Delta f=\Theta(1).}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

The original forward computation and backpropagated update thus give the scaling condition for **nondegenerate functional change at increasing width**.

**Step 2: Adjust output scaling along with representation updates.** The original study compares the \(n^{-1/2}\) output scaling with standard parameterization. Under standard output scaling, allowing a \(\Theta(1)\) hidden-feature update can make the correlated output-weight/updated-feature term grow as \(\Theta(\sqrt n)\), destabilizing logits. Appendix E.1's μP output scaling keeps that term \(\Theta(1)\). Feature update scale and output stability must therefore be controlled together.

**Step 3: Enable feature learning in the first layer as well.** The original paper adjusts the first-layer parameterization exponents to \(a_1=-1/2,b_1=1/2\) (and \(a_{L+1}=1/2,c=0\) at the output layer), retaining nondegenerate influence from input-layer updates on hidden features. Each layer has its corresponding initialization and update scaling conditions, rather than one assumed common learning rate.

**Core conclusion.** μP regulates actual layerwise updates and forward scales so that **functional changes remain finite and nonvanishing as width increases, without divergent logits**. The original MLP provides the order-of-magnitude calculation. Tensor Programs V's μTransfer further studies width-stable optimal hyperparameters; its full parameterization results and transfer measurements are separate research results.

**Research comparison.** [Yang and Hu, *Tensor Programs IV: Feature Learning in Infinite-Width Neural Networks*, ICML 2021](https://proceedings.mlr.press/v139/yang21c.html), particularly [Appendix E](https://proceedings.mlr.press/v139/yang21c/yang21c-supp.pdf); [Yang et al., *Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer*, NeurIPS 2021](https://proceedings.nips.cc/paper_files/paper/2021/hash/8df7c2e3c3c3be098ef7b382bd2c37ba-Abstract.html).

**Internal anchors.** TL-E03 (receiving-state-dependent responses), TL-E04 (nonlinear finite-update effects), TL-E05 (target and update geometry).

### 5.2.12 Sharpness and SAM: Parameter Geometry, Realized Updates, and Functional Responses

**Derivation type.** Using the function-preserving reparameterization of Dinh et al. and the SAM training rule of Foret et al., substitute realized SAM updates into the TLI functional response to calculate the one-step output changes under SGD and SAM.

**Equation provenance.** <sup>[T]</sup> TLI state updates and functional responses; <sup>[A]</sup> the original product model and squared loss, function-preserving transformation, SAM neighborhood objective and update rule; <sup>[R]</sup> Hessian eigenvalues and concrete SGD/SAM functional responses. SAM uses its algorithmic first-order perturbation approximation; the one-step product-output response is algebraically exact for the resulting update.

**TLI equation [T].**

\[
\theta_{t+1}=\theta_t+\delta_t,\qquad
R_q(\theta,\delta)=m_q(\theta+\delta)-m_q(\theta).
\qquad {}^{\scriptscriptstyle\text{[T]}}
\]

**Original-study conditions [A].** Use the two-parameter product example and squared loss under the function-preserving reparameterization idea of Dinh et al.:

\[
f(a,b)=ab,\qquad \mathcal L(a,b)=\tfrac12(ab-1)^2.
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

**Step 1: Function preservation with changed parameter sharpness.** For any \(c>0\), the transformation \((a,b)\mapsto(ca,b/c)\) preserves \(f=ab\). At a fitted point \(ab=1\), the Hessian is:

\[
H=\nabla^2\mathcal L
=\begin{pmatrix}b^2&ab\\ab&a^2\end{pmatrix}.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

The largest eigenvalues at the original and rescaled parameter points are, respectively:

\[
\boxed{\lambda_{\max}=a^2+b^2,\qquad
\lambda_{\max}'=c^2a^2+\frac{b^2}{c^2}.}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

**Step 2: Form the realized training action using the original SAM definition.** The worst-case neighborhood loss objective is:

\[
\mathcal L_{\rm SAM}(\theta)
=\max_{\|\epsilon\|\le\rho}\mathcal L(\theta+\epsilon).
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

At \(g=\nabla\mathcal L(a,b)\ne0\), the original SAM algorithm uses a first-order perturbation and evaluates the gradient at the perturbed point:

\[
g=(ab-1)(b,a),\qquad
\epsilon\approx\rho\frac{g}{\|g\|},\qquad
\delta_{\rm SAM}=-\eta\nabla\mathcal L(\theta+\epsilon).
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

Let \(\tilde a=a+\epsilon_a\) and \(\tilde b=b+\epsilon_b\). The two realized update components are:

\[
\delta_a=-\eta(\tilde a\tilde b-1)\tilde b,\qquad
\delta_b=-\eta(\tilde a\tilde b-1)\tilde a.
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

**Step 3: Substitute into the TLI response [T]+[A]→[R].** Set the target readout to the original model output \(m_q=f(a,b)=ab\). Then:

\[
\begin{aligned}
R_q^{\rm SAM}
&=f(a+\delta_a,b+\delta_b)-f(a,b)\\
&=b\delta_a+a\delta_b+\delta_a\delta_b\\
&=\boxed{-\eta(\tilde a\tilde b-1)(b\tilde b+a\tilde a)
+\eta^2(\tilde a\tilde b-1)^2\tilde a\tilde b}.
\end{aligned}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

This is the exact one-step output difference after applying the update formed using the SAM perturbation approximation above. For comparison, ordinary SGD at the same receiving state produces:

\[
\delta_{\rm SGD}=-\eta(ab-1)(b,a).
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

Substitute again into the TLI response:

\[
\boxed{R_q^{\rm SGD}
=-\eta(ab-1)(a^2+b^2)+\eta^2(ab-1)^2ab.}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

**Derived conclusion.** At fitted points \(ab=1\), function-preserving reparameterization yields the same function with different parameter sharpness. At nonzero-gradient points, SAM and SGD produce different realized updates under their respective training rules, and the TLI response equation gives their distinct functional changes. The fitted-point Hessian calculation and the nonzero-gradient update calculation apply at their respective points in the same original model.

**Research references.** [Dinh et al., *Sharp Minima Can Generalize For Deep Nets*](https://arxiv.org/abs/1703.04933); [Foret et al., *Sharpness-Aware Minimization*, ICLR 2021](https://research.google/pubs/sharpness-aware-minimization-for-efficiently-improving-generalization/).

**Internal anchors.** TL-E03 (update and receiving state); TL-E04 (finite-step response); TL-E05 (target-update geometry).

### 5.2.13 Gradient Noise Scale: Stochastic-Gradient Noise in Target Functional Responses

**Derivation type.** Under the original independent minibatch-gradient sampling conditions, calculate variance in parameter space and functional space.

**Equation provenance.** <sup>[T]</sup> The response \(R_{t,q}=m_q(\theta_t+\delta_t)-m_q(\theta_t)\). <sup>[A]</sup> McCandlish et al.'s independent sample gradients under ordinary SGD: mean \(g\), covariance \(\Sigma_g\), batch size \(B\), where \(B\) denotes batch size rather than the TLI feedback variable \(B_t\). The action \(\delta=-\eta B^{-1}\sum_{i=1}^{B}g_i\) has exact covariance \(\operatorname{Cov}(\delta)=\eta^2\Sigma_g/B\). First-order expansion of the [T] response at the receiving state yields <sup>[R]</sup> \(\operatorname{Var}(R_{t,q})\approx\eta^2 j_q^\top\Sigma_gj_q/B\) and \(\operatorname{Cov}(\Delta f)\approx\eta^2 J\Sigma_gJ^\top/B\). The original gradient noise scale is \(\operatorname{tr}\Sigma_g/\|g\|^2\); functional variance is a local linearization approximation.

**TLI variables.** The realized action \(\delta_t\) acts on the current receiving state; the target response \(R_q(\theta_t,\delta_t)\) depends on that action and target.

**Original-study assumptions.** Independently sample \(B\) examples from one fixed training distribution; each gradient \(g_i\) has mean \(g\) and covariance \(\Sigma_g\). Use ordinary SGD and a small-step local linear approximation for the functional response.

**Derivation.** The minibatch mean gradient and covariance are:

\[
\hat g_B=\frac1B\sum_{i=1}^B g_i,\qquad
\mathbb E[\hat g_B]=g,\qquad
\operatorname{Cov}(\hat g_B)=\frac{\Sigma_g}{B}.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

The realized parameter update is \(\delta=-\eta\hat g_B\), hence

\[
\boxed{
\operatorname{Cov}(\delta)=\frac{\eta^2}{B}\Sigma_g.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

For a fixed target \(q\), define its readout parameter gradient as \(j_q=\nabla_\theta m_q(\theta)\). Then

\[
R_q(\theta,\delta)\approx j_q^\top\delta
=-\eta j_q^\top\hat g_B.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Consequently,

\[
\boxed{
\begin{aligned}
\mathbb E[R_q]&\approx-\eta j_q^\top g,\\
\operatorname{Var}(R_q)&\approx
\frac{\eta^2}{B}j_q^\top\Sigma_gj_q.
\end{aligned}}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

For an output vector \(f\) with Jacobian \(J\), likewise,

\[
\boxed{
\operatorname{Cov}(\Delta f)\approx
\frac{\eta^2}{B}J\Sigma_gJ^\top.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

**Derived conclusion.** Batch size changes update noise and, through the receiving model's target-sensitive directions, the **functional response noise of each task**. The original gradient noise scale \(\operatorname{tr}\Sigma_g/\|g\|^2\) characterizes its typical scale; the effective batch-size bottleneck is determined by the original optimization problem.

**Research reference.** [McCandlish et al., *An Empirical Model of Large-Batch Training*](https://arxiv.org/abs/1812.06162).

**Internal anchors.** TL-E03 (receiving state); TL-E05 (target-update geometry).

### 5.2.14 Double Descent: Explicit Risk Curves in the Original Gaussian Linear Model

**Derivation type.** Using the original isotropic Gaussian design and minimum-norm/least-squares solutions, derive the expected risk on either side of the interpolation threshold.

**Equation provenance.** <sup>[T]</sup> State update \(\theta_{t+1}=\theta_t+\delta_t\); write population test risk as a functional readout \(m_{\rm test}(L)\) of the final learned state, with stepwise response \(R_{t,\rm test}=m_{\rm test}(L_{t+1})-m_{\rm test}(L_t)\). <sup>[A]</sup> The original isotropic zero-signal Gaussian regression model of Hastie et al.: \(X_{ij}\sim N(0,1)\), \(y=\varepsilon\sim N(0,\sigma^2I_n)\), independent test covariance \(I_p\), and zero-initialized least-squares/minimum-norm solutions. Training converges to \(\hat\beta=(X^\top X)^{-1}X^\top\varepsilon\) for the underparameterized case or \(\hat\beta=X^\top(XX^\top)^{-1}\varepsilon\) for the overparameterized case. Substituting these into the original population-risk readout and applying inverse-Wishart expectations gives <sup>[R]</sup> \(\mathbb E R_{\rm test}=\sigma^2 p/(n-p-1)\) for \(p<n-1\) or \(\sigma^2 n/(p-n-1)\) for \(p>n+1\). This is **excess risk from noise**, excluding irreducible test-label noise; its quantitative form follows from the original Gaussian conditions.

**TLI variables.** Model size \(p\) changes the available parameterized function space; training selects a final parameter solution, and test error is a functional readout of that solution on new inputs.

**Original-study assumptions.** In the classical pure-noise isotropic linear model, \(X\in\mathbb R^{n\times p}\) has independent \(N(0,1)\) entries, \(y=\varepsilon\) with \(\varepsilon\sim N(0,\sigma^2I_n)\), and the test input \(x\sim N(0,I_p)\) is independent of training. Ordinary least squares applies for \(p<n\); minimum-norm interpolation applies for \(p>n\). The calculated test excess prediction risk excludes irreducible noise in a new label.

**Derivation: Underparameterized regime \(p<n-1\).**

\[
\hat\beta=(X^\top X)^{-1}X^\top\varepsilon.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Taking expectations over training noise and an independent test input,

\[
\mathbb E R
=\sigma^2\,\mathbb E_X
\operatorname{tr}[(X^\top X)^{-1}].
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Using the inverse-Wishart expectation for the original Gaussian design gives

\[
\boxed{\mathbb ER=\sigma^2\frac{p}{n-p-1},\quad p<n-1.}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

**Derivation: Overparameterized regime \(p>n+1\).**

\[
\hat\beta=X^\top(XX^\top)^{-1}\varepsilon,\qquad
\mathbb E R=\sigma^2\mathbb E_X
\operatorname{tr}[(XX^\top)^{-1}],
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Therefore,

\[
\boxed{\mathbb ER=\sigma^2\frac{n}{p-n-1},\quad p>n+1.}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

Near the interpolation threshold, these inverse-matrix expectations diverge. Farther into the overparameterized regime, the second expression decreases as \(p\) grows, giving the **rise-to-peak-and-decline** double-descent risk curve.

**Derived conclusion.** The curve follows from the original linear-regression solution and the joint training/test distribution. For nonzero signals or general covariance, the bias–variance decomposition in §5.2.5 and the corresponding original-study conditions provide the broader formulation.

**Research references.** [Hastie, Montanari, Rosset, and Tibshirani, *Annals of Statistics*, 2022](https://doi.org/10.1214/21-AOS2133); Belkin et al.'s interpolation-threshold work.

**Internal anchors.** TL-E03 (parameter updates and receiving state); TL-E08 (target-dependent readout).
