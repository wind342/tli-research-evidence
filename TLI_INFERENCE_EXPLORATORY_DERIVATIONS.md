> **Exploratory TLI mathematics:** E-I01–E-I04 are separate from the current paper's fourteen formal mathematical recoveries. Their [T] starting point is the [current ICML unified system](https://github.com/wind342/tli-paper/blob/icml-final/icml/sections/dynamics_layout.tex). E-I04 uses the current feedback structure to derive its Jacobian and stability threshold.

# Four Exploratory Mathematical Deductions from TLI Inference Equations and Related Published Evidence

**Status:** EXPLORATORY — mathematical research notes separate from the fourteen formal recoveries
**Record date:** November 8, 2026
**Starting point:** The training, learning, capability-readout, frozen-inference and feedback relations established through TLI experiments
**Evidence type:** Mathematical deduction, explicitly conditioned examples and review of published external research as of November 8, 2026
**Scope:** Four mathematical explorations based on the current TLI equations and public literature; prior formal recoveries and frozen experimental records retain their own versions.

## 0. Overview and sources

These notes combine the **TLI inference relation \(\mathcal I\)** with the established state transitions and capability readouts to explore four mathematical consequences:

1. **Equivalent present behavior need not imply equivalent behavior after the same update:** Behavioral equivalence classes need not be closed under training transitions.
2. **Bayesian posterior updates with fixed persistent learned state:** Context-conditioned transient support recruitment can represent posterior predictions exactly.
3. **Inference compute under a fixed learned state can determine an output boundary crossing:** A contraction-map assumption gives a sufficient inference-step bound.
4. **The inference–feedback–training loop can have a computable stability threshold:** A specified two-dimensional linear case yields a critical equation relating feedback gain to decay.

**Research type and sources:** Established TLI equations and previous causal experiments provide the foundation; each exploration introduces explicit mathematical conditions. Published studies supply related theoretical or experimental precedents. This file records mathematical derivations and checks against public evidence.

Current TLI equations: [unified dynamics](TLI_UNIFIED_DYNAMICS.md). Frozen evidence: [experiment index](EXPERIMENT_INDEX.md), [cross-system chain](CROSS_SYSTEM_EVIDENCE_CHAIN.md) and [reinforcement evidence](RL_EVIDENCE_CHAIN.md).

## 1. [T] Common starting point: the TLI equations

The TLI-defined objects are kept distinct from the mathematical specializations below.

**Actual training action and state transition:**

$$
Z_t=(L_t,\omega_t),\qquad
A_t=\mathcal U(Z_t,B_t),\qquad
Z_{t+1}=\mathcal T(Z_t,A_t).
$$

In a parameterized implementation, the realized increment is

$$
\delta_t=\Psi(\theta_t,\omega_t,B_t),\qquad
\theta_{t+1}=\theta_t+\delta_t.
$$

**Learned functional support, realized response and capability readout:**

$$
P_{t,q}=\mathcal P_q(L_t;\mathcal J_q),\quad
\Delta P_{t,q}=P_{t+1,q}-P_{t,q},
$$

$$
R_{t,q}=m_q(L_{t+1})-m_q(L_t),\qquad
C_{t,q}=\chi_q\bigl(m_q(L_t)\bigr).
$$

**Frozen inference:**

$$
S_{x,c}^{\mathrm{active}}=\Pi_{x,c}(L^*),\qquad
Y_{x,c}=H_{x,c}\bigl(S_{x,c}^{\mathrm{active}}\bigr),\qquad
\Delta_{\mathrm{inf}}L=0.
$$

The composed inference map is

$$
\mathcal I(L^*,x,c)=H_{x,c}\bigl(\Pi_{x,c}(L^*)\bigr).
$$

Here \(\Pi\) means support recruitment, selection and combination; it is **not assumed linear**, and does not require an attention-based architecture.

**Feedback loop:**

$$
Y_t=\mathcal I(L_t,x_t,c_t),\quad
B_{t+x}=\mathcal B(Y_t,E_t),
$$

$$
A_{t+x}=\mathcal U(Z_{t+x},B_{t+x}),\quad
Z_{t+x+1}=\mathcal T(Z_{t+x},A_{t+x}),\quad x\ge1.
$$

These [T] equations form the common starting point for four explorations. Any additional assumptions and symbols appear under [A] within their respective examples.

---

## 2. Exploration E-I01: Equivalent current behavior does not ensure equivalent training dynamics

**Question.** If two persistent states implement the same inference function for every input and context, does that function alone determine the function obtained after the same training action?

### [T]

Define the complete behavioral map of a fixed state:

$$
F_L:(x,c)\mapsto \mathcal I(L,x,c).
$$

The training transition is \(\mathcal T(L,A)\); the following example omits optimizer memory and works directly with parameter states.

### [A] Mathematical conditions

Let distinct states \(L_1,L_2\) be **behaviorally equivalent over all inputs**, \(F_{L_1}=F_{L_2}\), and allow the same pre-specified increment \(A\) to be applied to both parameter states.

Consider the following one-dimensional model:

$$
\mathcal I(L,x)=L^2x,\qquad
L_1=1,\qquad L_2=-1,\qquad
\mathcal T(L,A)=L+A,\qquad A=0.1.
$$

This is a **controlled same-increment mathematical counterexample**. It specifies an intervention, rather than asserting that Adam or gradient descent would spontaneously produce the same increment in both states.

### [R] Derivation

Before the update, for every \(x\):

$$
F_{L_1}(x)=F_{L_2}(x)=x.
$$

After the update:

$$
F_{\mathcal T(L_1,A)}(x)=1.21x,\qquad
F_{\mathcal T(L_2,A)}(x)=0.81x.
$$

Therefore:

$$
\boxed{
F_{L_1}=F_{L_2}
\;\not\Longrightarrow\;
F_{\mathcal T(L_1,A)}=F_{\mathcal T(L_2,A)}.
}
$$

For the target margin \(m(L)=\mathcal I(L,1)-1.1\) at \(x=1\), and \(C(L)=\mathbf1[m(L)>0]\), both states are incorrect before the update, while only the successor of \(L_1\) becomes correct.

More generally, under \(L\sim L'\iff F_L=F_{L'}\), a closed transition on behavioral equivalence classes exists only if

$$
L\sim L'\Longrightarrow\mathcal T(L,A)\sim\mathcal T(L',A)
\quad\text{for every allowed action }A
$$

holds. Then the quotient-space transition \(\overline{\mathcal T}([L],A)\) can be defined uniquely by current behavior and action.

**Exploratory conclusion:** Even the full present input–output function may be insufficient to form a closed dynamical state for predicting future training responses. This is a stronger condition than the insufficiency of accuracy alone.

### Related published evidence

- Dinh et al., *Sharp Minima Can Generalize For Deep Nets* (ICML 2017), show that functionally equivalent parameterizations can have different parameter-space geometry. This is a mathematical precedent for **behavioral equivalence with distinct internal states**; [PMLR](https://proceedings.mlr.press/v70/dinh17b.html).
- *Exact learning dynamics of deep linear networks with prior knowledge* examines initialization-dependent trajectories and reports internal representation differences even when final functions or losses agree. It supplies related theory and experiments on **initialization and training-history dependence**; [full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC10955603/).

**Evidence interpretation:** The displayed counterexample follows exactly by algebra. The external papers provide adjacent theoretical and experimental precedents.

---

## 3. Exploration E-I02: Bayesian inference with a fixed learned state

### [T]

$$
Y_{x,c}=H_{x,c}(\Pi_{x,c}(L^*)),\qquad \Delta_{\mathrm{inf}}L=0.
$$

### [A] Mathematical conditions

Suppose \(L^*\) contains a finite hypothesis family \(h=1,\ldots,K\), positive priors \(\pi_h\), conditional likelihoods \(p_h(z)\), and predictive distributions \(p_h(y\mid x)\). Context samples \(c_n=(z_1,\ldots,z_n)\) are i.i.d. under the true hypothesis \(h^*\); the relevant likelihoods are positive and KL divergences are well defined.

Let the current inference recruitment return Bayesian weights:

$$
\Pi_{c_n}(L^*)_h
=
\frac{\pi_h\prod_{i=1}^n p_h(z_i)}
{\sum_{j=1}^{K}\pi_j\prod_{i=1}^n p_j(z_i)}.
$$

The map \(H\) then mixes the hypotheses' predictions.

### [R] Derivation

$$
\boxed{
\mathcal I(L^*,x,c_n)
=
\sum_{h=1}^{K}
\Pi_{c_n}(L^*)_h\,p_h(y\mid x)
}
$$

This is Bayesian posterior prediction by a fixed model.

For any competing hypothesis \(h\), the posterior-odds identity gives

$$
\log\frac{\Pr(h^*\mid c_n)}{\Pr(h\mid c_n)}
=
\log\frac{\pi_{h^*}}{\pi_h}
+\sum_{i=1}^{n}\log\frac{p_{h^*}(z_i)}{p_h(z_i)}.
$$

Taking expectation under \(z_i\sim p_{h^*}\),

$$
\boxed{
\mathbb E_{h^*}
\log\frac{\Pr(h^*\mid c_n)}{\Pr(h\mid c_n)}
=
\log\frac{\pi_{h^*}}{\pi_h}
+
nD_{\mathrm{KL}}(p_{h^*}\|p_h).
}
$$

If the KL divergence is positive, the **expected log posterior odds** of the true hypothesis against a competitor grow linearly with context length, while \(L^*\) remains fixed.

**Exploratory conclusion:** Context adaptation during inference can be implemented by recruitment from fixed persistent support. Changes in a Bayesian posterior need not update the model's persistent parameters. The example specifies a Bayesian inference model rather than a universal characterization of all in-context learning.

### Related published evidence

- Sang Michael Xie, Aditi Raghunathan, Percy Liang and Tengyu Ma, *An Explanation of In-context Learning as Implicit Bayesian Inference* (ICLR 2022), analyze inference over latent concepts and HMM mixtures and test relevant in-context phenomena on synthetic data; [arXiv:2111.02080](https://arxiv.org/abs/2111.02080).
- Madhur Panwar, Kabir Ahuja and Navin Goyal, *In-Context Learning through the Bayesian Prism* (ICLR 2024), find predictions approaching Bayesian baselines in tractable task families for sufficiently capable Transformers, as well as deviations; [arXiv:2306.04891](https://arxiv.org/abs/2306.04891), [ICLR paper](https://proceedings.iclr.cc/paper_files/paper/2024/file/d81cd83e7f6748af351485d73-Paper-Conference.pdf).

**Evidence interpretation:** Published theory and experiments support Bayesian-like inference through context under fixed model weights. The posterior-odds formula above follows algebraically from the specified probabilistic assumptions.

---

## 4. Exploration E-I03: Inference-step budget and a target boundary under a fixed state

### [T]

TLI distinguishes frozen inference from persistent learning and describes observable capability through continuous readouts and decision boundaries:

$$
\Delta_{\mathrm{inf}}L=0,\qquad C=\chi(m).
$$

### [A] Mathematical conditions

Fix \(L^*\), input and context. Let a transient inference workspace state, distinct from the persistent learned state, evolve according to

$$
w_{k+1}=F_{L^*,x,c}(w_k).
$$

Assume \(F\) is a contraction in the relevant complete metric space with \(0<\rho<1\) and fixed point \(w_\infty\). For a given target, define an **inference-budget-dependent readout** \(m_{q,k}=m_q(L^*,w_k)\). This is separate from the persistent training-time readout indexed by \(t\). Assume a Lipschitz constant \(M\) in \(w\), and \(m_q(L^*,w_\infty)\ge\gamma>0\).

### [R] Derivation

The contraction property yields

$$
\|w_k-w_\infty\|
\le \rho^k\|w_0-w_\infty\|.
$$

The Lipschitz condition gives

$$
m_q(L^*,w_k)
\ge\gamma-M\rho^k\|w_0-w_\infty\|.
$$

Consequently, if

$$
M\rho^k\|w_0-w_\infty\|<\gamma,
$$

then the output after inference budget \(k\) lies above the positive decision boundary. In particular, when the initial error bound exceeds the threshold, a sufficient condition is

$$
\boxed{
k>
\frac{\log\!\left(M\|w_0-w_\infty\|/\gamma\right)}
{\log(1/\rho)}.
}
$$

If the initial bound is already below \(\gamma\), \(k=0\) suffices. This is a **sufficient-step condition** for the specified contraction model, not an empirically fitted LLM compute law.

**Exploratory conclusion:** Transient inference iterations can change the budget-dependent output decision while the persistent learned state remains fixed. Persistent learning-time capability and the current output under a specified inference budget are different readouts.

### Related published evidence

- Charlie Snell, Jaehoon Lee, Kelvin Xu and Aviral Kumar, *Scaling LLM Test-Time Compute Optimally Can be More Effective than Scaling Parameters for Reasoning* (ICLR 2025), show that allocating test-time compute can improve reasoning, with some FLOP-matched comparisons favoring smaller models with additional inference computation; [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/1b623663fd9b874366f3ce019fdfdd44-Abstract-Conference.html).
- Wenkai Yang, Shuming Ma, Yankai Lin and Furu Wei, *Towards Thinking-Optimal Scaling of Test-Time Compute for LLM Reasoning* (NeurIPS 2025), observe cases in which excessive test-time reasoning degrades performance; [NeurIPS proceedings](https://papers.neurips.cc/paper_files/paper/2025/hash/3e22bea3b170f4c2aebb9c48d98ae64d-Abstract-Conference.html).

**Evidence interpretation:** Published experiments show that test-time compute changes performance, sometimes nonmonotonically. The contraction-map assumptions and sufficient-step bound above are a separate mathematical specialization.

---

## 5. Exploration E-I04: Stability conditions for the inference–feedback–training loop

### [T] Current TLI feedback equations

$$
Y_t=\mathcal I(L_t,x_t,c_t),\quad B_{t+x}=\mathcal B(Y_t,E_t),\quad
A_{t+x}=\mathcal U(Z_{t+x},B_{t+x}),\quad
Z_{t+x+1}=\mathcal T(Z_{t+x},A_{t+x}),\quad x\ge1.
$$

### [A] Synchronous one-step feedback specialization

Set \(x=1\) and index time by one training/feedback cycle. Fix the query and external information \(E\):

$$
Z_{t+1}=F(Z_t,B_t)=\mathcal T\bigl(Z_t,\mathcal U(Z_t,B_t)\bigr),\quad
B_{t+1}=\mathcal B\bigl(\mathcal I(L_t,x,c),E\bigr).
$$

在可微固定点附近，\(\mathcal I_Z\) 表示通过 \(Z\mapsto L\) 得到的导数。

### [R] 局部稳定Jacobian

$$
\boxed{
J_{\mathrm{loop}}=
\begin{pmatrix}
\mathcal T_Z+\mathcal T_A\mathcal U_Z&
\mathcal T_A\mathcal U_B\\
\mathcal B_Y\mathcal I_Z&0
\end{pmatrix}.
}
$$

偏导均在同一固定点、固定外部条件下求值。反馈规则 \(\mathcal B(Y_t,E_t)\) 不以先前 \(B_t\) 为独立参数，因此右下角为0。若谱半径 \(\rho(J_{\mathrm{loop}})<1\)，固定点局部渐近稳定；若有模大于1的特征值，线性化有增长方向。

### [A] 二维线性特例

考虑 \(Y_t=L_t\)、\(L_{t+1}=(1-\alpha)L_t+\beta B_t\)、\(B_{t+1}=\kappa Y_t\)，取 \(0<\alpha<1\)、\(\beta,\kappa\ge0\)。则

$$
J=\begin{pmatrix}1-\alpha&\beta\\\kappa&0\end{pmatrix},\quad
\det(I-J)=\alpha-\beta\kappa,
$$

$$
\lambda_\pm=\frac{(1-\alpha)\pm\sqrt{(1-\alpha)^2+4\beta\kappa}}2.
$$

因此矩阵的谱半径为 \(\lambda_+\)，从而

$$
\boxed{\rho(J)<1\iff\beta\kappa<\alpha,\quad
\rho(J)=1\iff\beta\kappa=\alpha.}
$$

此前记忆反馈模型 \(B_{t+1}=\gamma B_t+\kappa Y_t\) 的阈值是 \(\beta\kappa=\alpha(1-\gamma)\)；当前版本使用ICML论文的反馈输入形式，取无历史反馈项的特例。

### [R] 功能响应与能力边界

若 \(m_q\) 可微，反馈增量 \(\Delta B\) 在固定接收状态附近产生局部变化

$$
\Delta m_q\simeq\nabla_Zm_q^\top\mathcal T_A\mathcal U_B\,\Delta B.
$$

不同目标的响应方向由各自的读出梯度决定，累积响应是否跨越能力边界由TLI读出方程判定。这里的数值稳定阈值属于探索性二维线性模型，不是RL-E05/E06实验测得的阈值。

### 外部证据

- Vincent Liu、Han Wang、Ruo Yu Tao、Khurram Javed、Adam White、Martha White，*Measuring and Mitigating Interference in Reinforcement Learning*，CoLLAs 2023，报告干扰测量与控制性能不稳定之间的联系：[PMLR](https://proceedings.mlr.press/v232/liu23a.html)。
- Brahma S. Pavse 等人，*Learning to Stabilize Online Reinforcement Learning in Unbounded State Spaces*，ICML 2024，研究在线 RL 的策略稳定性，并采用稳定性方法：[PMLR](https://proceedings.mlr.press/v235/pavse24a.html)。
- Ali Saheb Pasand 等人，*Stable Deep Reinforcement Learning via Isotropic Gaussian Representations*，ICML 2026，分析非平稳学习目标下的表示稳定性与训练不稳定：[PMLR](https://proceedings.mlr.press/v306/pasand26a.html)。

**证据结论：** 外部研究支持 RL／反馈系统中干扰和稳定性问题的实际存在，但**没有直接验证本节的 TLI 局部 Jacobian 或特例阈值等式**。TLI 自身的 RL-E05/E06 提供反馈分配、功能支撑变化、其他能力损失与恢复的独立实验锚点，不能重标为本节新实验。

---

## 6. 数学推论、外部证据及现有 TLI 结果的对应表

| 探索 ID | 严格数学内容 | 外部证据的准确作用 | 记录性质 |
|---|---|---|---|
| E-I01 | 完整行为等价不蕴含同增量更新后的等价：明确代数反例；给出商空间转移的相容条件 | 函数等价表示与初始化依赖的相关理论／实验 | 新反例分析，未新增原生干预 |
| E-I02 | 指定假说模型下的贝叶斯预测及期望对数后验赔率恒等式 | 贝叶斯式 ICL 的已有理论与实验 | 原方程的概率模型特化 |
| E-I03 | 压缩推理迭代 + Lipschitz 读出下的能力边界充分步数 | 测试时计算的收益与非单调经验现象 | 条件性数学上界；非通用推理规模律 |
| E-I04 | 指定同步反馈闭环的 Jacobian、二维线性特例稳定阈值 | RL 干扰、策略／表示稳定性已有研究 | 条件性控制理论特化；非 GRU 实测阈值 |

**共同发现（探索性）：** TLI的状态—训练动作—持久功能组织—冻结推理—能力读出—反馈关系，在分别加入原研究的数学条件后，连接到行为可辨识性、贝叶斯后验、推理计算收敛和闭环稳定性。四项结果属于条件性数学特化；所引外部文献提供各领域的理论与实验参照。

## 7. 记录边界与出处

1. **已建立的 TLI 来源**： [TLI_UNIFIED_DYNAMICS.md](TLI_UNIFIED_DYNAMICS.md)；[实验导航](EXPERIMENT_INDEX.md)；[INF-E01 原生冻结推理](experiments/gfg_nanogpt_training_learning_inference_projection_v1/)；[INF-G01 跨系统无 Attention 冻结推理](experiments/gfg_cross_system_frozen_inference_projection_v1/)；[RL-E05/E06 证据链](RL_EVIDENCE_CHAIN.md)。
2. **本文内容**：四项条件性数学探索、对应公开研究与证据分类；研究性质为数学推导及文献核对。
3. **既有研究**：14项正式外推、冻结实验协议、历史数据、机器结果及独立检查器仍按各自的原始版本保存。

**简要结论：** TLI 的推理方程 \(\mathcal I\) 与此前已建立的训练、功能响应、能力读出及反馈方程联立后，在明确数学条件下，可以推导出四组可核查的关系，并与多个独立研究领域的已发表理论和实验形成可审查的对应。这是一次**探索性数学外推与文献核对记录**，而非正式论文的新实验证明。
