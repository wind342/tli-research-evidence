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

### 5.2.6 Scaling Laws与Chinchilla：TLI功能响应和计算最优配置

**推导类型：把原Chinchilla经验损失律代入TLI功能响应，先得到固定模型规模下增加训练Token的边际功能收益，再结合原研究的模型规模项和计算预算约束，恢复其计算最优配置。经验幂律和指数仍来自原研究，不由TLI单独预设或证明。**

**逐式来源标记。** <sup>[T]</sup> TLI原状态转移和功能响应；<sup>[A]</sup> 原研究的经验损失律及计算预算；<sup>[R]</sup> 具体功能响应、边际收益、最优配置和损失标度。

**TLI原方程 [T]。** 实际训练动作改变学习状态，目标功能响应是前后状态读出之差：

\[
Z_{t+1}=\mathcal T(Z_t,A_t),\qquad
\theta_{t+1}=\theta_t+\delta_t.
\qquad {}^{\scriptscriptstyle\text{[T]}}
\]

\[
R_{t,q}=m_q(L_{t+1})-m_q(L_t).
\qquad {}^{\scriptscriptstyle\text{[T]}}
\]

**原研究条件 [A]。** Hoffmann等采用的经验损失律及计算量近似：

\[
\mathcal L(N,D)=E+AN^{-\alpha}+BD^{-\beta},\quad
A,B,\alpha,\beta>0,\qquad C=6ND.
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

其中 \(N\) 是参数规模、\(D\) 是训练Token量、\(C\) 是计算量。固定模型规模 \(N\)，用累计训练Token数 \(D_t\) 索引该模型训练达到的状态；将该状态上的训练损失取负，作为TLI连续功能读出：

\[
m_{\ell}(L_t)=-\mathcal L(N,D_t)\qquad(N\ \text{固定}).
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

**第一步：将原损失律实际代入TLI功能响应 [T]+[A]→[R]。**

\[
\begin{aligned}
R_{t,\ell}
&=m_\ell(L_{t+1})-m_\ell(L_t)\\
&=-\mathcal L(N,D_{t+1})+\mathcal L(N,D_t)\\
&=B\left(D_t^{-\beta}-D_{t+1}^{-\beta}\right).
\end{aligned}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

令 \(D_{t+1}=D_t+\Delta D\)，得到固定模型规模下的Token边际功能收益：

\[
\lim_{\Delta D\to0}\frac{R_{t,\ell}}{\Delta D}
=\frac{\partial m_\ell}{\partial D}
=\beta BD^{-\beta-1}.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

这一步用到TLI前后功能差分和原经验损失函数，而不是仅在规模律旁列出TLI符号。

**第二步：结合原研究已有的计算预算和模型规模效应。** 沿固定计算预算配置有：

\[
D=\frac{C}{6N},\qquad
\left.\frac{dD}{dN}\right|_C=-\frac DN.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

从原经验损失律得模型规模方向的边际收益 \(\partial m_\ell/\partial N=\alpha AN^{-\alpha-1}\)。同第一步得到的Token边际收益一起代入预算约束：

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

在最优配置令上式为零，得到：

\[
\boxed{\alpha AN^{-\alpha}=\beta BD^{-\beta}.}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

所以：

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

原损失律在最优配置下变为：

\[
\boxed{\mathcal L_\star(C)-E\propto C^{-\alpha\beta/(\alpha+\beta)}.}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

**推得的结论。** TLI功能响应经原Chinchilla条件具体化后，给出训练Token的边际功能收益；结合原模型规模收益及预算约束，得到计算最优条件。模型规模 \(N\) 的导数比较不同计算配置；经验损失幂律及其指数来自Hoffmann等的拟合条件[A]。

**研究对照。** [Hoffmann等，Training Compute-Optimal Large Language Models (2022)](https://arxiv.org/abs/2203.15556)；Kaplan等的经验规模规律。

**内部锚点。** TL-E03（实际动作与接收状态）；TL-E04（功能响应）；TL-E07（持续重组）；跨架构TLI测试。

### 5.2.E1（探索性，不计入14项）Scaling Laws：从TLI功能支撑、能力与损失到谱模型规模关系

**状态：EXPLORATORY / 探索性数学外推（第14项之后的独立研究笔记）。** 5.2.6代入Hoffmann等的经验损失律求计算最优分配；本节使用**经典高斯序列/正交谱学习特例**，先计算实际功能支撑贡献，再推得该特例的损失与规模渐近关系。结论的模型条件是高斯序列观测、正交特征、平方损失与相应谱假设；证据性质为解析推导。

**逐式来源标记。** <sup>[T]</sup> 为当前ICML论文的统一动力学方程组及其组件干预测量（见[统一动力学方程](TLI_UNIFIED_DYNAMICS.md)）；<sup>[A]</sup> 为本节使用的高斯序列观测、正交特征、谱衰减、梯度下降及相应的谱截断/预算条件；<sup>[R]</sup> 为代入计算得到的关系。本节将回归任务能力读出与Shapley联盟值具体化为TLI一般公式的特例。

**TLI方程入口 [T]。** 对持久学习状态、实际动作、目标响应、干预支撑、能力和冻结推理，使用

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

本节采用监督训练，不使用反馈闭环；这不改变TLI的反馈方程定义。具体损失与能力的关系由任务的原生输出和读出规则计算，**不将能力等同于参数数目、模式数或损失本身**。

**经典可求解条件 [A]。** 在高斯正交基上取独立 \(x_k\sim N(0,1)\)，真实目标函数为 \(y=f^*(x)=\sum_{k\ge1}a_kx_k\)，并要求 \(\sum_ka_k^2<\infty\)。参数规模为 \(N\) 的此特例最多表示前 \(N\) 个模式；实际启用 \(M\le N\) 个模式。冻结推理将模式的已学习输出调用并组合：

\[
\Pi_x(L^*)=(z_1,\ldots,z_M),\quad z_k=\theta_kx_k,\qquad
H_x(\Pi_x(L^*))=\widehat y(x)=\sum_{k=1}^{M}z_k.
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

为了可精确计算训练数据的影响，采用**高斯序列观测模型**：每个启用模式的观测系数 \(\widetilde a_{k,D}=a_k+\sigma D^{-1/2}\xi_k\)，其中 \(\xi_k\) 独立同分布为 \(N(0,1)\)，且独立于测试输入。这里 \(D\) 表示每个系数的**有效观测规模**，不是未经额外论证即可等同于真实语言模型训练Token数；这个观测模型也不自动等同于直接对普通i.i.d.样本做最小二乘。训练使用系数平方目标 \(Q_M(\theta)=\frac12\sum_{k\le M}(\theta_k-\widetilde a_{k,D})^2\)，零初始化、步长 \(0<\eta<2\)。

**第一步：用固定联盟干预将TLI功能支撑连到能力与损失 [T]+[A]→[R]。** 对目标 \(q=(x,y)\)，指定容许回归误差 \(\varepsilon>0\)，取此任务的功能读出与能力判定为

\[
m_q(L)=\varepsilon^2-(y-\widehat y)^2,\qquad
C_q(L)=\mathbf1[m_q(L)>0].
\qquad {}^{\scriptscriptstyle\text{[T]}}
\]

按固定干预协议 \(\mathcal J_q\) 对注册模式执行全部联盟 \(S\subseteq\{1,\ldots,M\}\)，其联盟读出是

\[
v_q(S;L)=\varepsilon^2-\left(y-\sum_{k\in S}z_k\right)^2.
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

以论文的联盟Shapley测量定义有符号功能贡献 \(\varphi_{k,q}\)。Shapley的联盟边际平均及完备性给出**精确等式**：

\[
\boxed{\varphi_{k,q}=z_k(2y-\widehat y),\qquad
\sum_{k=1}^{M}\varphi_{k,q}=2y\widehat y-\widehat y^2.}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\tag{E1}
\]

若全关闭的基线 \(b_q=v_q(\varnothing;L)=\varepsilon^2-y^2\)，则
\(m_q(L)=b_q+\sum_k\varphi_{k,q}(L)\)。对固定目标 \(q\) 在实际训练前后比较，\(b_q\) 不变，故TLI实际功能响应为

\[
\boxed{
R_{t,q}=\sum_k\Delta\varphi_{t,k,q},\qquad
\Delta\ell_{t,q}=-\tfrac12 R_{t,q}
=-\tfrac12\sum_k\Delta\varphi_{t,k,q}.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\tag{E2}
\]

这里的任务平方损失与能力读出由**同一完整支撑分解**给出：

\[
\boxed{
\ell_q(L)=\tfrac12(y-\widehat y)^2
=\tfrac12\left(y^2-\sum_k\varphi_{k,q}(L)\right),\qquad
C_q(L)=\mathbf1\left[\sum_k\varphi_{k,q}(L)>y^2-\varepsilon^2\right].
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\tag{E3}
\]

这些等式需要**保留全部有符号贡献、全关闭基线和同一固定联盟协议**，不能把仅含正贡献的归一化支撑占比代入。此简化模型的前向输出是加性的，联盟读出的非加性交互来自**平方读出**；它不声称已在该模型中复现真实深度网络内部的一切非加性组件机制。

**第二步：用TLI实际训练转移计算支撑贡献的演化 [T]+[A]→[R]。** 经典梯度动作实例化为
\(\delta_{t,k}=-\eta(\theta_{t,k}-\widetilde a_{k,D})\)。
代入 \(\theta_{t+1,k}=\theta_{t,k}+\delta_{t,k}\)，令 \(s_t=1-(1-\eta)^t\)，则

\[
\boxed{\theta_{t,k}=s_t\widetilde a_{k,D}.}
\qquad {}^{\scriptscriptstyle\text{[A]}}
\tag{E4}
\]

由(E1)，先对独立高斯测试输入求期望，再对系数观测噪声求期望：

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

所以训练充分收敛时（\(s_t\to1\)）：

\[
\boxed{\mathbb E[\varphi_{\infty,k}]=a_k^2-\sigma^2/D.}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\tag{E6}
\]

**这里由训练后的实际支撑贡献进入损失计算，而不是先输入一个经验损失幂律。** 期望功能贡献可以为负；这代表此固定平方读出下该模式的净贡献被估计误差抵消，并不是“存在负的能力实体”。

**第三步：从功能支撑求出平均损失，再代入经典谱条件 [T]+[A]→[R]。** 在任意训练时刻，由(E3)精确得到

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

在收敛极限，取经典幂律谱条件 \(a_k^2=\Lambda k^{-(1+\alpha)}\)，其中 \(\Lambda>0,\alpha>0\)，则

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

这里**谱幂律属于目标函数的经典条件 [A]；损失幂律是把它代入TLI支撑—损失计算后得到的结果 [R]**。若把全部 \(N\) 个模式训练至收敛，即 \(M=N\)，直接得到

\[
\boxed{
\mathbb E\mathcal L_\infty(N,D)
\sim\frac{\Lambda}{2\alpha}N^{-\alpha}
+\frac{\sigma^2N}{2D}.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\tag{E9}
\]

(E9)是一个显式的模型—数据规模关系，**但不是**Chinchilla的可分离加性拟合形式。

**第四步：只在引入经典最优谱截断时，得到Chinchilla型双变量幂律数量级 [A]→[R]。** 将 \(M\) 视为可选的有效学习模式数，并受限于 \(M\le N\)。对(E8)求驻点，

\[
M_D=\left(\frac{\Lambda D}{\sigma^2}\right)^{1/(\alpha+1)},\qquad
M_*=\min\{N,M_D\}
\quad\text{（连续近似；整数模式取邻近值）}.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

当 \(N,D\) 共同增长、\(\sigma^2>0\) 且采用这一截断规则时，分情况比较表示误差与估计误差得到

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

(E10)的意义是**两个规模变量的幂律数量级**；它不主张原Chinchilla的经验系数、指数或严格可分离等式已经被重现，也不把最优截断当作任意网络训练都会自行发生的事实。

**第五步：从同一冻结功能状态计算能力—损失关系 [T]+[A]→[R]。** 固定训练后状态 \(L\)，在独立测试输入上，预测误差是高斯变量，

\[
e(x;L)=f^*(x)-\widehat y(x)\mid L\sim N(0,V(L)),
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

\[
V(L)=\sum_{k\le M}(a_k-\theta_k)^2+\sum_{k>M}a_k^2,\qquad
\overline{\mathcal L}(L)=\tfrac12V(L).
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

因此，对于上述预先指定的回归容许误差边界 \(\varepsilon>0\)，

\[
\boxed{
\Pr_x(C_q=1\mid L)
=\Pr_x(|e|<\varepsilon\mid L)
=\operatorname{erf}\left(\frac{\varepsilon}{2\sqrt{\overline{\mathcal L}(L)}}\right).
}
\qquad {}^{\scriptscriptstyle\text{[A]}}
\tag{E11}
\]

这是**固定学习状态下**的精确能力成功率—平均平方损失关系；\(V(L)=0\) 时按极限取成功率1。若再对训练噪声平均，不能直接把 \(\mathbb E_L[\overline{\mathcal L}(L)]\) 填进非线性的 \(\operatorname{erf}\) 并称为精确等式。它也不是一般分类能力或语言模型交叉熵的通用公式。

**第六步：可选的计算最优关系 [A]→[R]。** 只分析**全部 \(N\) 个模式参与计算和训练**的(E9)，采用该特例的预算近似 \(\mathcal K=\kappa ND\)，代入 \(D=\mathcal K/(\kappa N)\)：

\[
\mathbb E\mathcal L_\infty(N,\mathcal K)
\sim\frac{\Lambda}{2\alpha}N^{-\alpha}
+\frac{\sigma^2\kappa}{2\mathcal K}N^2.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

对 \(N\) 求导令零，得到

\[
\boxed{
N_*\asymp\mathcal K^{1/(\alpha+2)},\qquad
D_*\asymp\mathcal K^{(\alpha+1)/(\alpha+2)},\qquad
\mathcal L_*(\mathcal K)\asymp\mathcal K^{-\alpha/(\alpha+2)}.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\tag{E12}
\]

这一预算计算没有偷换到(E10)的截断训练条件；其指数也不需要与Chinchilla实测指数一致。

**探索所得与适用边界。** (E1)–(E3)把TLI的干预支撑、功能响应、冻结推理和目标能力/损失读出精确连接起来；(E4)–(E8)给出实际训练动作形成支撑贡献并产生平均损失的计算链条；(E9)–(E12)在明确经典谱及训练选择条件下得到可检验的规模关系。**这里已经实现的是TLI方程组织下的可求解特例外推，而不是从TLI方程单独固定普遍指数。** 原特例是Gaussian sequence/linear orthogonal features、干净教师测试目标、平方损失；它不等同于Transformer的全训练动态、交叉熵、多Token条件分布或真实语料统计。本节没有新增运行验证，也不改变5.2.6对于原Chinchilla损失律的输入地位。

**校核说明。** (E1)–(E3)已用四组件全联盟枚举作独立代数数值核对，Shapley贡献与直接平方损失在浮点精度内相等；(E4)–(E12)是公开可逐步复核的解析推导，尚未通过独立实验检验其对真实规模曲线的预测。

**研究对照（不把本例冒称为原论文的完整模型）。** [Bahri等，Explaining neural scaling laws，PNAS 2024，DOI:10.1073/pnas.2311878121](https://doi.org/10.1073/pnas.2311878121)（随机特征与谱结构的规模律研究）；[Bordelon、Atanasov与Pehlevan，A Dynamical Model of Neural Scaling Laws，ICML 2024](https://proceedings.mlr.press/v235/bordelon24a.html)（可求解随机特征训练动力学）；[Hoffmann等，Training Compute-Optimal Large Language Models，2022](https://arxiv.org/abs/2203.15556)（经验Chinchilla律，与本特例作对照）。

**内部实验锚点（并非本节新验证）。** TL-E03/04（真实更新与有限响应）；TL-E06/07（干预定义的功能支撑及重组）；TL-E08（能力边界）；INF-E01及INF-G01/G02（冻结推理与已训练组件版本）。这些实验支持TLI各关系本身；**不被当作本节(E8)–(E12)谱指数的直接实测证据**。

### 5.2.7 Dynamical Isometry：深层网络的动作—响应传输

**推导类型：由原网络的分层复合与链式法则直接推出。**

**逐式来源标记。** <sup>[T]</sup> 原功能响应 \(R_q=m_q(\theta+\delta\theta)-m_q(\theta)\)，其局部形式是 \(R_q\approx\nabla_\theta m_q^\top\delta\theta\)。<sup>[A]</sup> 原分层网络 \(h^{\ell+1}=F_\ell(h^\ell,\theta_\ell)\) 与可微链式法则，层间Jacobian记为 \(J_{L\leftarrow\ell+1}\)。逐层传播 \(\delta h^{\ell+1}=B_\ell\delta\theta_\ell\)，得 <sup>[R]</sup> \(\delta f\approx\sum_\ell J_{L\leftarrow\ell+1}B_\ell\delta\theta_\ell\)。这里是**局部一阶响应**；动态等距仅约束对应 Jacobian 的奇异值传输，不单独保证所有更新具有良好泛化效果。若矩阵有非零核空间，**全空间**范数下界为零，不能把仅对非零奇异子空间有效的下界误写成对所有输入成立。

**TLI作用对象。** 一个实际参数更新\(\delta\theta\)改变输出\(f_\theta\)，其局部功能响应由当前接收状态决定。

**使用的原理论条件。** 可微的分层网络\(h^{\ell+1}=F_\ell(h^\ell,\theta_\ell)\)，以及Dynamical Isometry研究所考察的跨层雅可比及其奇异值。

**逐步推导。** 对第\(\ell\)层参数做微小改动，首先有

\[
\delta h^{\ell+1}\approx
B_\ell\delta\theta_\ell,\qquad
B_\ell=\frac{\partial F_\ell}{\partial\theta_\ell}.
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

余下层以链式法则传递，令\(J_{L\leftarrow\ell+1}=\partial h^L/\partial h^{\ell+1}\)，于是

\[
\boxed{\delta f\approx
\sum_{\ell}J_{L\leftarrow\ell+1}B_\ell\delta\theta_\ell.}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

同时，对从第\(\ell\)层发出的激活扰动\(v\)，有

\[
\|J_{L\leftarrow\ell}v\|
\in[\sigma_{\min}^{\mathrm{all}}(J)\|v\|,\ \sigma_{\max}(J)\|v\|]
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

其中\(\sigma_{\min}^{\mathrm{all}}(J)=\inf_{\|v\|=1}\|Jv\|\)，当\(J\)有非零核空间时严格为0；只有限制在与核空间正交的有效子空间，才可以使用最小非零奇异值作下界。。反传梯度沿相应转置雅可比传递。若相关非零奇异值集中于1附近，则这些方向上的信号与梯度跨层传输不发生大的范数放大或衰减；若谱极端偏离1，则出现明显的方向性放大或衰减。

**推得的结论。** Dynamical Isometry描述的是固定当前状态上**计算和梯度的传输条件**，由原网络复合结构直接推出。它不是对每个实际参数更新必然高效的承诺，因为局部参数映射\(B_\ell\)也参与实际功能响应。

**研究对照。** [Pennington、Schoenholz与Ganguli，NeurIPS 2017](https://arxiv.org/abs/1711.04735)。

**内部锚点。** TL-E03（接收状态）；TL-E04（实际更新路径）；TL-E05（更新几何）。

### 5.2.8 Dropout：随机特征屏蔽为什么等价于自适应正则化

**推导类型：使用Dropout研究自身的独立Bernoulli特征屏蔽与广义线性模型（GLM）条件，直接推出标签无关的正则项；在原GLM包含的高斯线性回归中，精确推出数据依赖的对角二次正则化，以及它怎样改变真实训练动作。**

**逐式来源标记。** <sup>[T]</sup> 原训练动作 \(\theta_{t+1}=\theta_t+\delta_t\) 与功能响应 \(R_{t,q}=m_q(\theta_{t+1})-m_q(\theta_t)\)。<sup>[A]</sup> Wager 等的独立Bernoulli特征遮蔽、倒置缩放 \(\tilde x_j=z_jx_j/r\)、GLM对数配分函数 \(A(u)\) 凸。对遮蔽取期望，标签线性项不变，得到 <sup>[R]</sup> \(\overline L_{\rm drop}=L_0+\frac1n\sum_i\{\mathbb E_zA(w^\top\tilde x_i)-A(w^\top x_i)\}\ge L_0\)。原高斯线性特例 \(A(u)=u^2/2\) 时，该差值精确等于 \((1-r)/(2r)\sum_j s_j^2w_j^2\)。**[T→A]** 代回更新得 \(\mathbb E_z[\delta_t\mid w_t]=-\eta\nabla\overline L_{\rm drop}\)，单次抽到的实际动作并不等于该期望。对非线性网络不能把测试期望等同关系当成精确恒等式。

**TLI作用对象。** 式(1)–(2)把实际训练写为\(A_t=\mathcal U(Z_t,B_t)\)、\(\theta_{t+1}=\theta_t+\delta_t\)。训练时随机屏蔽特征，直接改变实际动作的形成；式(3)再测量该动作对任一固定目标的连续功能响应。式(4)区分训练时的随机屏蔽和冻结模型的推理调用。

**使用的原理论条件。** Wager、Wang与Liang（NeurIPS 2013）研究广义线性模型的**独立特征Dropout**。令保留概率\(r\in(0,1]\)，各掩码\(z_{ij}\)独立服从\(\operatorname{Bernoulli}(r)\)，并使用原研究的倒置缩放\(\widetilde x_{ij}=x_{ij}z_{ij}/r\)，因此\(\mathbb E_z[\widetilde x_i]=x_i\)。GLM的单样本负对数似然为

\[
\ell_i(w;x_i,y_i)=A(w^\top x_i)-y_iw^\top x_i-\log h(y_i),
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

其中\(A\)是原GLM的凸对数配分函数；不引入其他正则项或新的特征噪声模型。

**第一步：由原Dropout屏蔽机制计算目标函数。** 令\(L_0(w)=n^{-1}\sum_i\ell_i(w;x_i,y_i)\)。对屏蔽变量取期望：

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

最后的不等式来自\(A\)凸、\(\mathbb E_z[\widetilde x_i]=x_i\)以及Jensen不等式。由于标签项对屏蔽取期望后不变，**\(\mathcal R_{\rm drop}\)不包含\(y_i\)**。这是原GLM条件下的精确分解，而不是额外猜测Dropout会产生何种惩罚。

**第二步：在原GLM包含的高斯线性回归中算出正则项。** 对固定方差的高斯线性模型，归一化单位方差后\(A(u)=u^2/2\)，对应平方损失\(\ell_i=\tfrac12(y_i-w^\top x_i)^2+\mathrm{const}\)。因为独立屏蔽，

\[
\operatorname{Var}_z(w^\top\widetilde x_i)
=\frac{1-r}{r}\sum_{j=1}^d w_j^2x_{ij}^2.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

令\(s_j^2=n^{-1}\sum_i x_{ij}^2\)，则

\[
\boxed{
\overline L_{\rm drop}(w)
=L_0(w)+\frac{1-r}{2r}\sum_{j=1}^d s_j^2w_j^2.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

**这就是Dropout与数据依赖的对角\(L_2\)正则化之间的精确关系。** 特征坐标的惩罚系数由该坐标在训练数据中的平方均值和原始Dropout保留率决定。

**第三步：代回TLI实际更新，得到功能响应。** 对上述期望目标使用原有的梯度下降训练动作（单次随机掩码SGD的条件期望梯度也等于下式梯度），记\(D_s=\operatorname{diag}(s_1^2,\ldots,s_d^2)\)，则

\[
\boxed{
\begin{aligned}
\mathbb E_z[\delta_t\mid w_t]
&=-\eta\nabla_w\overline L_{\rm drop}(w_t)\\
&=-\eta\left[\nabla L_0(w_t)+\frac{1-r}{r}D_sw_t\right].
\end{aligned}}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

这里的期望指**固定接收状态和训练数据、只平均Dropout掩码**；一次真实训练使用的仍是实际抽到的掩码所形成的动作\(\delta_t\)。

对于线性模型，在固定查询\(x_q\)上的连续功能读出\(m_q(w)=w^\top x_q\)，TLI功能响应恰好为

\[
\boxed{
R_{t,q}
=m_q(w_t+\delta_t)-m_q(w_t)
=x_q^\top\delta_t.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

所以随机屏蔽通过改变训练动作，使不同查询产生不同的目标功能响应；其期望更新含有上述自适应收缩项。**正则化并不是另一个独立的学习过程，而是原有随机训练机制对状态更新施加的确定性平均效应。**

**第四步：训练与冻结推理的关系。** 对这一线性模型，因\(\mathbb E_z[\widetilde x]=x\)，

\[
\boxed{
\mathbb E_z[f_w(\widetilde x)]=f_w(x)=w^\top x.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

故训练时随机子模型预测的平均值，与冻结权重、关闭屏蔽后的线性推理**精确相同**。原Dropout论文在非线性深网中的测试时权重缩放/模型平均属于近似，不把线性模型的等式推广为所有非线性网络的恒等式。

**推得的核心关系。** 在原广义线性模型与独立Dropout条件下，**随机特征屏蔽 \(\Rightarrow\) 标签无关的非负正则项**；在原高斯线性特例下进一步得到**精确的自适应二次惩罚 \(\Rightarrow\) 改变的实际梯度更新 \(\Rightarrow\) 查询相关的功能响应**。这与TLI的训练—学习—冻结推理链直接衔接。

**独立研究对照。** [Srivastava等，Dropout: A Simple Way to Prevent Neural Networks from Overfitting，JMLR 2014](https://www.jmlr.org/papers/v15/srivastava14a.html)；[Wager、Wang与Liang，Dropout Training as Adaptive Regularization，NeurIPS 2013](https://papers.nips.cc/paper_files/paper/2013/hash/38db3aed920cf82ab059bfccbd02be6a-Abstract.html)。

**内部实验锚点。** TL-E03（形成的实际动作及接收状态影响功能响应）；TL-E04（有限幅度功能响应）；INF-E01（固定学习状态上的查询相关推理）。

### 5.2.9 Catastrophic Forgetting：旧目标失效的精确边界

**推导类型：直接由TLI功能响应和正确性读出式推出，SGD梯度解释采用遗忘理论原条件。**

**逐式来源标记。** <sup>[T]</sup> 原响应 \(R_{t,q}=m_q(L_{t+1})-m_q(L_t)\) 与能力读出 \(C_{t,q}=\mathbf1[m_q(L_t)>0]\)。精确求和得 \(m_q(L_T)=m_q(L_0)+\sum_{t<T}R_{t,q}\)，故对最初 \(m_q(L_0)>0\) 的目标，<sup>[R]</sup> 失效当且仅当 \(\sum_{t<T}R_{t,q}\le-m_q(L_0)\)。<sup>[A]</sup> 原持续学习分析的SGD更新 \(\delta_t=-\eta\nabla L_{\rm new}(\theta_t)\) 和可微读出，另外给出**一阶近似** \(R_{t,q}\approx-\eta\nabla m_q^\top\nabla L_{\rm new}\)；旧任务损失的相应变化为 \(\Delta L_{\rm old}\approx-\eta g_{\rm old}^\top g_{\rm new}\)。请区分前一条精确边界与后一条局部近似。

**TLI作用对象。**

\[
R_{t,q}=m_q(\theta_{t+1})-m_q(\theta_t),\qquad
C_{t,q}=\mathbf1[m_q(\theta_t)>0].
\qquad {}^{\scriptscriptstyle\text{[T]}}
\]

**第一步：精确累计，不需要线性近似。**

\[
\boxed{
m_q(\theta_T)=m_q(\theta_0)+\sum_{t=0}^{T-1}R_{t,q}.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

对于初始已正确的旧目标\(m_q(\theta_0)>0\)，在时刻\(T\)的目标失败当且仅当

\[
\boxed{
\sum_{t=0}^{T-1}R_{t,q}\leq-m_q(\theta_0).
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

同一个公式还描述保持与恢复：后续的正向功能响应可以使间隔重新跨过零边界，重新得到正确结果。

**第二步：代入被研究对象采用的SGD。** 若新任务的损失为\(L_{\rm new}\)，其更新为\(\delta_t=-\eta g_{\rm new}\)。在可微读出和局部小步长条件下，

\[
R_{t,q}\approx-\eta\nabla_\theta m_q(\theta_t)^\top g_{\rm new}.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

如果旧目标采用可微损失\(L_{\rm old}\)，则

\[
\boxed{
\Delta L_{\rm old}
\approx-\eta g_{\rm old}^\top g_{\rm new}.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

梯度点积为负时，当前新任务更新使旧损失的一阶变化为正；为正时则为负。多个任务共享同一批参数，所以一次动作可同时改变许多目标的间隔。

**推得的结论。** 遗忘首先是旧目标函数的计算结果越过正确性边界；它不是“能力实体”从参数中消失。保护旧任务的方法本质上是在改变旧目标上累计的功能响应轨迹。

**研究对照。** Kirkpatrick等的EWC；Lopez-Paz与Ranzato的GEM；梯度投影与经验回放研究。

**内部锚点。** TL-E03、TL-E07、TL-E08；[RL-E06](experiments/gfg_rl_selective_positive_feedback_dose_recovery_v1/RESULTS.md)（先掌握、后退化、再恢复）。

### 5.2.10 Grokking：训练/测试读出的不同跨界时间

**推导类型：使用被外推Grokking可解研究的线性教师—学生模型、实际梯度流与随机矩阵谱，直接推出训练/测试损失轨迹以及延迟泛化时间。**

**逐式来源标记。** <sup>[T]</sup> 原状态更新 \(\theta_{t+1}=\theta_t+\delta_t\) 在原研究的梯度流极限中给出连续状态 \(D(t)\)；TLI响应 \(R_{t,q}=m_q(L_{t+1})-m_q(L_t)\)，能力读出 \(C_{t,q}=\chi_q(m_q(L_t))\)。<sup>[A]</sup> Levi、Beck与Bar-Sinai的标量输出（\(d_{\rm out}=1\)）高斯线性教师—学生模型、零权重衰减、平方损失梯度流、训练协方差 \(\Sigma_{\rm tr}\)、总体协方差 \(I\)，以及原文使用的Marčenko–Pastur谱和同一正确率阈值。代入更新得 \(D(t)=e^{-2\eta_0\Sigma_{\rm tr}t}D_0\)，同一状态的两个连续读出分别是 \(L_{\rm tr}(t)=D_0^\top e^{-4\eta_0\Sigma_{\rm tr}t}\Sigma_{\rm tr}D_0\) 与 \(L_{\rm gen}(t)=D_0^\top e^{-4\eta_0\Sigma_{\rm tr}t}D_0\)。对**原研究的**准确率阈值 \(L=\epsilon/4\)，可等价选择TLI读出 \(m_q=\epsilon/4-L_q\)、\(\chi_q(m)=\mathbf1[m\ge0]\)。由原谱边缘渐近得到 <sup>[R]</sup> \(\Delta t_{\rm grok}\simeq-\ln(1-\sqrt\lambda)/[2\eta_0(1-\sqrt\lambda)^2]\)，其中 \(0<\lambda<1\)。这个时间公式属于**特定渐近区域的结果**，不是仅由TLI形式方程独立确定的常数。

**TLI作用对象。** 式(2)的实际参数更新及式(3)的连续功能响应与离散能力读出。训练集目标和测试分布目标是**同一个学习状态**的两类读出；正确性可以先后跨越各自的阈值。

**使用的原理论条件。** Levi、Beck、Bar-Sinai（ICLR 2024）的无偏置线性教师—学生设定：输入\(x\sim\mathcal N(0,I_d)\)，教师参数\(T\)、学生参数\(S_t\)；平方损失，标量输出，\(n\)个固定训练样本，零权重衰减，梯度流；训练协方差\(\Sigma_{\rm tr}=\frac1n\sum_jx_jx_j^\top\)，总体协方差为\(I_d\)，高维极限\(d,n\to\infty\)，\(\lambda=d/n\in(0,1)\)固定；原论文的Marčenko–Pastur谱、各向同性初始化，以及误差阈值\(\epsilon\)。

**第一步：由TLI更新代入原模型的优化动作。** 记\(D_t=S_t-T\)，训练与测试的两个连续读出为

\[
L_{\rm tr}(D)=D^\top\Sigma_{\rm tr}D,\qquad
L_{\rm gen}(D)=D^\top D.
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

原梯度流在时间尺度\(\eta_0\)下满足

\[
\dot D(t)=-2\eta_0\Sigma_{\rm tr}D(t),\qquad
\boxed{D(t)=e^{-2\eta_0\Sigma_{\rm tr}t}D_0}.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

代入同一状态的两个读出，得**精确**损失演化：

\[
\boxed{
\begin{aligned}
L_{\rm tr}(t)&=D_0^\top e^{-4\eta_0\Sigma_{\rm tr}t}\Sigma_{\rm tr}D_0,\\
L_{\rm gen}(t)&=D_0^\top e^{-4\eta_0\Sigma_{\rm tr}t}D_0.
\end{aligned}}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

**第二步：代入原论文使用的协方差谱。** 设\(\nu\)遵循\(\lambda=d/n\)下的Marčenko–Pastur谱，在原论文的各向同性初始方向及大维度近似下：

\[
L_{\rm tr}(t)\approx\mathbb E_\nu[\nu e^{-4\eta_0\nu t}],\qquad
L_{\rm gen}(t)\approx\mathbb E_\nu[e^{-4\eta_0\nu t}].
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

其正谱下端为\(\nu_-=(1-\sqrt\lambda)^2\)。当\(\eta_0t\gg\sqrt\lambda/(1-\sqrt\lambda)^2\)时，原论文的谱端点渐近给出

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

**第三步：用原论文的正确率读出计算迟发时间。** 每个输入的正确性由误差是否小于\(\epsilon\)定义：

\[
C_x(t)=\mathbf1[(D(t)^\top x)^2<\epsilon].
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

在相应高斯读出近似下

\[
A(t)=\operatorname{erf}\!\left(\sqrt{\frac{\epsilon}{2L(t)}}\right).
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

原论文用\(A=\operatorname{erf}(\sqrt2)\approx95.45\%\)作为跨界标准，对应\(L(t^*)=\epsilon/4\)。分别求\(L_{\rm tr}(t_{\rm tr}^*)\)和\(L_{\rm gen}(t_{\rm gen}^*)\)到达该阈值的时间，在小\(\epsilon\)渐近下：

\[
\boxed{
\Delta t_{\rm grok}=t_{\rm gen}^*-t_{\rm tr}^*
\simeq-\frac{\ln(1-\sqrt\lambda)}
{2\eta_0(1-\sqrt\lambda)^2}>0,\quad 0<\lambda<1.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

**核心结论。** 训练、测试都从同一条连续参数轨迹得到；在原模型的两种读出几何及同一正确性阈值下，测试正确率可远晚于训练正确率跃升。时间差不仅存在，而且由原研究的\(\lambda,\eta_0\)条件定量给出。整个过程无需假设外部读出跃升时突然生成独立“能力”。

**研究对照。** [Levi、Beck与Bar-Sinai，Grokking in Linear Estimators—A Solvable Model that Groks without Understanding，ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/8c0a85ee3eddb1858d9142f0d51d67b2-Abstract-Conference.html)；[Žunkovič与Ilievski，Grokking phase transitions in learning local rules with gradient descent，JMLR 2024](https://www.jmlr.org/papers/v25/22-1228.html)。

**内部实验锚点。** TL-E03（接收状态决定响应）；TL-E07（训练继续时支撑可重组）；TL-E08（连续间隔与离散边界）；TL-P01（目标边界预测）。

### 5.2.11 μP：宽度增长时保持非退化功能更新

**推导类型：使用Tensor Programs IV的原MLP参数化与SGD条件，直接得到更新量级和输出稳定性；进一步使用该论文的第一层修改，说明各层特征学习的条件。**

**逐式来源标记。** <sup>[T]</sup> 原实际动作 \(\theta_{t+1}=\theta_t+\delta_t\) 和功能响应 \(R_{t,q}=m_q(\theta_t+\delta_t)-m_q(\theta_t)\)。<sup>[A]</sup> Yang与Hu《Tensor Programs IV》附录E.1的线性MLP参数化、输出缩放 \(f=n^{-1/2}v\bar h\)、相关权重尺度与学习率 \(\eta_n\propto n^{-c}\)。对该论文的**同一SGD动作**按链式法则计算中间特征变化和输出响应，得到 <sup>[R]</sup> \(\Delta\bar h_j=\Theta(n^{-c})\)、\(\Delta f=\Theta(n^{-c})\)；当 \(c=0\) 时单步两者均为 \(\Theta(1)\)。这是原附录的**单步、特定参数化量级**；不据此直接声称完整μP所有层及μTransfer定理都已由此独立证明。

**TLI作用对象。** 式(2) \(\theta_{t+1}=\theta_t+\delta_t\)和式(3) \(R_q(\theta,\delta)=m_q(\theta+\delta)-m_q(\theta)\)。跨宽度比较必须检查实际参数动作在**功能/表征空间**造成的响应，而不能只比较参数增量数值。

**使用的原理论条件。** Yang与Hu（ICML 2021，Tensor Programs IV）附录E的两隐藏层线性MLP演示及其SGD宽度极限：隐藏宽度\(n\to\infty\)，\(h=U\xi\)、\(\bar h=Wh\)，\(h^\top h=\Theta(n)\)，中间层与输出层原始高斯初始化尺度为\(n^{-1/2}\)，损失对输出的导数\(\chi=\mathcal L'(f,y)=\Theta(1)\)。该附录给出输出缩放\(f=n^{-1/2}v\bar h\)，学习率\(\eta_n\propto n^{-c}\)，并研究固定输入上的单次实际SGD动作。

**第一步：把原参数化与动作代入TLI响应。** 对中间层的一个SGD动作，该论文附录E.1直接按链式求导得到

\[
\Delta\bar h
=-n^{-c-1/2}\chi\,v^\top(h^\top h),\qquad
\Delta f
=-n^{-c-1}\chi(vv^\top)(h^\top h).
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

在它自己的初始化尺度下，每个\(v_j=\Theta(n^{-1/2})\)、\(vv^\top=\Theta(1)\)、\(h^\top h=\Theta(n)\)，故

\[
\boxed{
\Delta\bar h_j=\Theta(n^{-c}),\qquad
\Delta f=\Theta(n^{-c}).
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

若\(c>0\)，固定步数内特征与输出更新趋零；若\(c=0\)，则

\[
\boxed{\Delta\bar h_j=\Theta(1),\qquad \Delta f=\Theta(1).}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

这从原前向计算和实际反向更新直接给出**宽度增长但功能更新仍非退化**的量级条件。

**第二步：为什么必须连输出缩放一起调整。** 原论文将上述\(n^{-1/2}\)的输出缩放与标准参数化对照：按原标准输出缩放、却让隐藏特征发生\(\Theta(1)\)的更新时，输出权重与已更新特征的相关项可使logit达到\(\Theta(\sqrt n)\)并失去稳定性；采用附录E.1的μP输出缩放时该项为\(\Theta(1)\)。因此不能只要求某一层“大幅更新”，还要同时控制输出的稳定量级。

**第三步：第一层也参与特征学习。** 原论文进一步把第一层参数化指数改为\(a_1=-1/2,b_1=1/2\)（并在输出层取\(a_{L+1}=1/2,c=0\)），使输入层的实际更新传入隐藏特征也保持非退化；不同层须分别满足相应的初始化和更新缩放条件。该条件来自Tensor Programs IV的参数化定义与证明，而不是额外假设各层采用相同学习率。

**核心结论。** μP的核心关系是：**在参数宽度增加时，调整各层的实际更新与前向缩放，使学习形成的功能变化保持有限而不消失、同时不导致logit发散。** 上述原MLP例子完成了这一关系的量级推导。Tensor Programs V的μTransfer进一步研究此参数化下最优超参数跨宽度的稳定性，其完整参数族证明与实测迁移效果仍属于原研究的进一步结果，不把“\(\Theta(1)\)响应”直接等同于“任意超参数必然可迁移”。

**研究对照。** [Yang与Hu，Tensor Programs IV: Feature Learning in Infinite-Width Neural Networks，ICML 2021](https://proceedings.mlr.press/v139/yang21c.html)，特别是[附录E](https://proceedings.mlr.press/v139/yang21c/yang21c-supp.pdf)；[Yang等，Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer，NeurIPS 2021](https://proceedings.nips.cc/paper_files/paper/2021/hash/8df7c2e3c3c3be098ef7b382bd2c37ba-Abstract.html)。

**内部实验锚点。** TL-E03（接收状态决定实际功能响应）；TL-E04（有限幅度更新的非线性）；TL-E05（目标与动作几何）。

### 5.2.12 Sharpness与SAM：参数几何、实际动作与功能响应

**推导类型：在Dinh等的函数保持重参数化思想及Foret等的SAM训练规则下，把实际SAM动作代入TLI功能响应，明确计算SGD和SAM产生的单步目标变化。**

**逐式来源标记。** <sup>[T]</sup> TLI状态更新与功能响应；<sup>[A]</sup> 原乘积模型/平方损失、函数保持变换、SAM邻域目标和更新规则；<sup>[R]</sup> Hessian特征值及具体SGD/SAM目标功能响应。SAM扰动采用原算法一阶近似；对所选更新动作，乘积输出的单步响应是代数精确式。

**TLI原方程 [T]。**

\[
\theta_{t+1}=\theta_t+\delta_t,\qquad
R_q(\theta,\delta)=m_q(\theta+\delta)-m_q(\theta).
\qquad {}^{\scriptscriptstyle\text{[T]}}
\]

**原研究条件 [A]。** 使用Dinh等函数保持重参数化思想的二参数乘积特例和平方损失：

\[
f(a,b)=ab,\qquad \mathcal L(a,b)=\tfrac12(ab-1)^2.
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

**第一步：函数不变而参数锐度改变。** 对任意 \(c>0\)，变换 \((a,b)\mapsto(ca,b/c)\) 保持 \(f=ab\) 不变。在拟合点 \(ab=1\)，Hessian为：

\[
H=\nabla^2\mathcal L
=\begin{pmatrix}b^2&ab\\ab&a^2\end{pmatrix}.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

它在原参数点与重标定后参数点的最大特征值分别是：

\[
\boxed{\lambda_{\max}=a^2+b^2,\qquad
\lambda_{\max}'=c^2a^2+\frac{b^2}{c^2}.}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

**第二步：用原SAM定义形成实际训练动作。** 原邻域最坏损失目标为：

\[
\mathcal L_{\rm SAM}(\theta)
=\max_{\|\epsilon\|\le\rho}\mathcal L(\theta+\epsilon).
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

在 \(g=\nabla\mathcal L(a,b)\ne0\) 处，原SAM算法用一阶近似扰动并在扰动点计算梯度：

\[
g=(ab-1)(b,a),\qquad
\epsilon\approx\rho\frac{g}{\|g\|},\qquad
\delta_{\rm SAM}=-\eta\nabla\mathcal L(\theta+\epsilon).
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

设 \(\tilde a=a+\epsilon_a\)、\(\tilde b=b+\epsilon_b\)，得到两个实际更新分量：

\[
\delta_a=-\eta(\tilde a\tilde b-1)\tilde b,\qquad
\delta_b=-\eta(\tilde a\tilde b-1)\tilde a.
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

**第三步：直接代入TLI响应 [T]+[A]→[R]。** 取目标读出为该原模型输出 \(m_q=f(a,b)=ab\)，则：

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

这是**采用上述SAM近似扰动所形成的具体更新后**，输出的精确单步差。对比普通SGD在同一接收状态形成的更新：

\[
\delta_{\rm SGD}=-\eta(ab-1)(b,a).
\qquad {}^{\scriptscriptstyle\text{[A]}}
\]

再次代入TLI响应：

\[
\boxed{R_q^{\rm SGD}
=-\eta(ab-1)(a^2+b^2)+\eta^2(ab-1)^2ab.}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

**推得的结论。** 函数保持重参数化在拟合点 \(ab=1\) 给出相同函数与不同参数锐度；在梯度非零位置，SAM与SGD按原训练算法产生不同实际更新，经TLI响应方程得到明确不同的功能变化。这两种观察在原模型中各自成立，不要求Hessian拟合点与SAM非零梯度点重合。没有增加额外假设。

**研究对照。** [Dinh等，Sharp Minima Can Generalize For Deep Nets](https://arxiv.org/abs/1703.04933)；[Foret等，SAM，ICLR 2021](https://research.google/pubs/sharpness-aware-minimization-for-efficiently-improving-generalization/)。

**内部锚点。** TL-E03（动作和接收状态）；TL-E04（有限幅度响应）；TL-E05（目标与更新几何）。

### 5.2.13 Gradient Noise Scale：随机梯度如何变成目标功能响应噪声

**推导类型：沿用原批量梯度独立采样条件，直接计算参数与功能空间方差。**

**逐式来源标记。** <sup>[T]</sup> 原响应 \(R_{t,q}=m_q(\theta_t+\delta_t)-m_q(\theta_t)\)。<sup>[A]</sup> McCandlish等使用的独立样本梯度与普通SGD条件：\(g_i\) 的均值 \(g\)，协方差 \(\Sigma_g\)，批量大小 \(B\)；此处 \(B\) 是**batch size**，不同于TLI反馈变量 \(B_t\)。由 \(\delta=-\eta B^{-1}\sum_{i=1}^{B}g_i\) 得精确的参数动作协方差 \(\operatorname{Cov}(\delta)=\eta^2\Sigma_g/B\)。再将 <sup>[T]</sup> 的 \(R\) 在接收点一阶展开，<sup>[R]</sup> \(\operatorname{Var}(R_{t,q})\approx\eta^2 j_q^\top\Sigma_gj_q/B\)，\(\operatorname{Cov}(\Delta f)\approx\eta^2 J\Sigma_gJ^\top/B\)；原梯度噪声尺度是 \(\operatorname{tr}\Sigma_g/\|g\|^2\)。这里的功能方差关系是**线性化近似**。

**TLI作用对象。** 实际动作\(\delta_t\)作用于当前接收状态，目标响应\(R_q(\theta_t,\delta_t)\)由该动作和目标决定。

**使用的原理论条件。** 从同一固定训练分布独立抽取\(B\)个样本；单样本梯度\(g_i\)有均值\(g\)、协方差\(\Sigma_g\)；采用普通SGD、小步长局部线性近似。这是梯度噪声规模分析的基础条件。

**逐步推导。** 平均梯度及其协方差：

\[
\hat g_B=\frac1B\sum_{i=1}^B g_i,\qquad
\mathbb E[\hat g_B]=g,\qquad
\operatorname{Cov}(\hat g_B)=\frac{\Sigma_g}{B}.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

实际参数更新为\(\delta=-\eta\hat g_B\)，故

\[
\boxed{
\operatorname{Cov}(\delta)=\frac{\eta^2}{B}\Sigma_g.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

对一个固定目标\(q\)，令其功能读出的参数梯度为\(j_q=\nabla_\theta m_q(\theta)\)，则

\[
R_q(\theta,\delta)\approx j_q^\top\delta
=-\eta j_q^\top\hat g_B.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

因而

\[
\boxed{
\begin{aligned}
\mathbb E[R_q]&\approx-\eta j_q^\top g,\\
\operatorname{Var}(R_q)&\approx
\frac{\eta^2}{B}j_q^\top\Sigma_gj_q.
\end{aligned}}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

对输出向量\(f\)及其雅可比\(J\)，同理得到

\[
\boxed{
\operatorname{Cov}(\Delta f)\approx
\frac{\eta^2}{B}J\Sigma_gJ^\top.
}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

**推得的结论。** 批量大小不仅改变更新噪声，还通过当前模型的目标敏感方向，改变**具体任务的功能响应噪声**。原研究中的梯度噪声规模可由\(\operatorname{tr}\Sigma_g/\|g\|^2\)表征其典型量级；是否为有效批量瓶颈仍由原优化问题决定。

**研究对照。** [McCandlish等，An Empirical Model of Large-Batch Training](https://arxiv.org/abs/1812.06162)。

**内部锚点。** TL-E03（接收状态）；TL-E05（目标—更新几何）。

### 5.2.14 Double Descent：高斯线性原模型中的显式风险曲线

**推导类型：只采用原研究的各向同性高斯设计和最小范数/最小二乘解，直接推导插值边界两侧的期望风险。**

**逐式来源标记。** <sup>[T]</sup> 原状态更新 \(\theta_{t+1}=\theta_t+\delta_t\)；将测试总体风险记作同一最终学习状态的功能读出 \(m_{\rm test}(L)\)，其步间变化由 \(R_{t,\rm test}=m_{\rm test}(L_{t+1})-m_{\rm test}(L_t)\) 给出。<sup>[A]</sup> Hastie等各向同性零信号高斯回归的原始模型 \(X_{ij}\sim N(0,1)\)、\(y=\varepsilon\sim N(0,\sigma^2I_n)\)、独立测试协方差 \(I_p\)、零初始化最小二乘/最小范数解。通过原训练动作收敛到对应解：欠参数 \(\hat\beta=(X^\top X)^{-1}X^\top\varepsilon\)，过参数 \(\hat\beta=X^\top(XX^\top)^{-1}\varepsilon\)。代入**原模型的**总体风险读出并使用Wishart逆期望，得到 <sup>[R]</sup> \(\mathbb E R_{\rm test}=\sigma^2 p/(n-p-1)\)（\(p<n-1\)）或 \(\sigma^2 n/(p-n-1)\)（\(p>n+1\)）。这是噪声**超额风险**而非包含不可约噪声的总MSE；曲线的定量形式来自原高斯设定，不由TLI单独给出。

**TLI作用对象。** 模型规模\(p\)改变可选的参数化函数空间；训练动作选择一个最终参数解；测试误差是该解对新输入的功能读出。它不是独立的“能力实体”。

**使用的原理论条件。** 取经典Double Descent研究中的纯噪声各向同性线性模型：\(X\in\mathbb R^{n\times p}\)各元素独立服从\(N(0,1)\)，\(y=\varepsilon\)且\(\varepsilon\sim N(0,\sigma^2I_n)\)，测试\(x\sim N(0,I_p)\)与训练独立；\(p<n\)用普通最小二乘，\(p>n\)用最小范数插值解。此处计算的是测试**超额预测风险**，不包含新标签自身的不可约噪声。

**逐步推导：欠参数区间\(p<n-1\)。**

\[
\hat\beta=(X^\top X)^{-1}X^\top\varepsilon.
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

对训练噪声与独立测试输入取期望，

\[
\mathbb E R
=\sigma^2\,\mathbb E_X
\operatorname{tr}[(X^\top X)^{-1}].
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

利用该原高斯设计的Wishart逆矩阵期望，得到

\[
\boxed{\mathbb ER=\sigma^2\frac{p}{n-p-1},\quad p<n-1.}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

**逐步推导：过参数区间\(p>n+1\)。**

\[
\hat\beta=X^\top(XX^\top)^{-1}\varepsilon,\qquad
\mathbb E R=\sigma^2\mathbb E_X
\operatorname{tr}[(XX^\top)^{-1}],
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

从而

\[
\boxed{\mathbb ER=\sigma^2\frac{n}{p-n-1},\quad p>n+1.}
\qquad {}^{\scriptscriptstyle\text{[R]}}
\]

在插值阈值附近，这些逆矩阵期望发散；远离阈值、\(p\)继续增大后，第二式下降。这样便直接得到**先升至峰值、再下降**的Double Descent风险形状。

**推得的结论。** 这个反常曲线是原线性回归的解与训练/测试分布共同确定的计算结果；无需另加“参数变多后噪声支撑必然重新分配”的新假设。对非零真实信号或一般协方差，可继续使用5.2.5的偏差—方差分解及原研究条件。

**研究对照。** [Hastie、Montanari、Rosset与Tibshirani，Annals of Statistics 2022](https://doi.org/10.1214/21-AOS2133)；Belkin等的插值阈值研究。

**内部锚点。** TL-E03（参数更新与状态）；TL-E08（目标依赖读出）。
