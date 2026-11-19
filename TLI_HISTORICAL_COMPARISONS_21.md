> **TLI research comparisons:** Twenty-one paired results from previously published research, used to examine the explanatory relationships provided by TLI. These are literature comparisons, separate from the nine nanoGPT experiments and fourteen formal mathematical recoveries.

## 5.1 Unified explanations of contrasting findings
### 5.1.1 Sharpness and SAM: Parameter geometry versus realized training effects

**Positive finding — SAM (Foret et al.).** Sharpness-aware minimization evaluates loss perturbations in a parameter neighborhood and uses elevated neighborhood loss to guide optimization. In the reported tasks, this training action improves generalization, demonstrating the practical value of local sensitivity as an optimization control.

**Contrasting finding — reparameterization of sharpness (Dinh et al.).** Function-preserving reparameterizations can markedly change sharpness measured in the original parameter coordinates. Identical input–output functions can therefore have different sharpness values; raw parameter sharpness alone does not determine generalization uniquely.

**TLI unification.** The studies measure different objects in the dynamical chain. Sharpness is a local geometric readout of the current parameter state; SAM uses that readout to form a realized training action. Applied to a concrete receiving state, the action produces finite-amplitude, target-specific functional responses. A geometry measure may change under reparameterization while interventions designed from that measure still affect training. The operative chain is **local geometry → formation of an actual action → functional response of the receiving state**.

**Internal anchors.** TL-E03: the same actual update produces different responses in different receiving states. TL-E04: finite-amplitude responses to actual updates can be nonlinear.

### 5.1.2 NTK and feature learning: Fixed-kernel dynamics and evolving representations

**Positive finding — Neural Tangent Kernel (Jacot et al.).** Under appropriate infinite-width and lazy-training conditions, network-output evolution can be described by fixed or nearly fixed kernel dynamics, giving a tractable kernel representation of the functional effects of local parameter changes.

**Contrasting finding — feature-learning parameterizations (Yang et al.).** Under parameterizations and training regimes that admit substantial feature evolution, internal representations change throughout training. Subsequent functional responses change with those representations, beyond the complete description offered by a fixed-kernel approximation.

**TLI unification.** These are different regimes of the receiving-state → actual-update → functional-response relation. NTK describes a regime with restricted changes in the functional map and its local responses. Feature learning describes a regime in which actual updates persistently reorganize internal function and substantially alter later receiving states. The common relation is that the current state determines an update's response, and each realized update changes the state available for later responses.

**Internal anchors.** TL-E03: receiving-state dependence. TL-E04: nonlinear finite-amplitude responses. TL-E07: persistent support reorganization through actual updates.

### 5.1.3 Grokking: Delayed observable capability and earlier internal formation

**Positive finding — Grokking (Power et al.).** Training accuracy may saturate well before test generalization, which can improve abruptly after a long delay, producing an apparent transition in externally measured capability.

**Contrasting finding — circuits underlying grokking (Nanda et al.).** Tracking internal computational circuits shows that the structures supporting generalization can form and reorganize continuously before the sudden test-accuracy transition. Internal learning may therefore precede the observed capability change.

**TLI unification.** Learning corresponds to persistent reorganization of functional support, whereas capability is the observable result of crossing a target-specific readout boundary. Support can change continuously even when correctness is determined by the sign of a target margin; crossing zero converts accumulated internal changes into a discrete observed transition. The two lines of research measure internal formation and external readout within the same process.

**Internal anchors.** TL-E06: distributed support measured by component interventions. TL-E07: actual updates reorganize support. TL-E08: capability transitions depend on readout boundaries. TL-P01: prediction of post-update target-boundary outcomes.

### 5.1.4 Neural Collapse: Saturated accuracy and continuing representation formation

**Positive observation — saturated correctness readout.** When all training examples are correctly classified and training error reaches zero, the discrete correct/incorrect metric reaches a plateau; subsequent updates do not increase the number of already-correct examples under that metric.

**Contrasting finding — Neural Collapse (Papyan et al.).** Even after zero training error, deep features and classifiers can continue evolving toward particular within-class concentration, between-class mean geometry and classifier-direction relationships.

**TLI unification.** Accuracy records which side of the target-specific decision boundary an output occupies, whereas learning concerns the persistent functional organization. Continued training can change margins, component allocations and feature geometry after discrete correctness has stabilized. The same training period can therefore show constant observed accuracy and changing internal structure.

**Internal anchors.** TL-E07: support can reorganize without a capability change. TL-E08: the readout boundary determines capability state. RL-E06: margins evolve before correctness declines.

### 5.1.5 Attention: Effective computation and the interpretation of attention weights

**Positive finding — attention computation (Vaswani et al.; Wiegreffe and Pinter).** Attention changes information weighting, routing and combination as a function of inputs and queries. Controlled comparisons also show that appropriately designed attention explanations can reveal aspects of model behavior.

**Contrasting finding — attention-weight interpretation counterexamples (Jain and Wallace).** Attention weights can disagree with gradient-based importance measures, and sharply different attention distributions can yield similar outputs. This exposes a measurable difference between weight values and complete functional causal effects.

**TLI unification.** A fixed learned state can recruit different functional support for different queries and combine recruited components into an output. Attention weights describe one instantaneous routing and weighting mechanism; full functional effects depend on the realized outputs of individual components and their interactions. Attention can be an effective computation while a single weight visualization remains an incomplete account of distributed causal support.

**Internal anchor.** INF-E01: frozen-inference component gating, paired interventions and version rollback reveal query-dependent support recruitment, non-additive interaction and dependence on learned component versions.

### 5.1.6 RLHF: Alignment gains and capability trade-offs

**Positive finding — preference feedback and instruction tuning (Ouyang et al.).** Further training with human preferences and feedback can improve instruction following, preference alignment and task-specific performance, illustrating the influence of feedback on the direction of learning.

**Contrasting finding — alignment tax.** Similar feedback-based training has also been associated with decreases on some prior benchmarks. Mixing more broadly distributed pretraining data into the training stream can mitigate such degradation, indicating a trade-off between target-directed feedback and the retention of other capabilities.

**TLI unification.** Feedback changes the distribution of subsequent training examples, rewards and realized updates. Applied to a shared receiving state, those updates redistribute support across capabilities. A concentrated target can gain support while other mastered capabilities first lose margin and later correctness; balanced feedback can redirect support and restore prior capabilities. Targeted gains and cross-capability trade-offs arise within the same feedback–training–learning loop.

**Internal anchor.** RL-E06: concentrated correct feedback reduces support and performance in other mastered skills, while rebalancing feedback produces recovery.

### 5.1.7 Reward-proxy overoptimization: Misbound objectives versus concentrated correct feedback

**Positive finding — reward models and preference optimization.** Where the real objective is difficult to express as a differentiable loss, reward models and preference signals supply executable optimization directions for policy training.

**Contrasting finding — Goodhart effects and reward overoptimization.** A reward model is a proxy for the underlying preference. Training can exploit differences between proxy and true objective, improving the proxy score while reducing real objective performance.

**TLI unification.** Feedback affects realized actions through two distinct relationships. First, **content and credit binding** determine which action and temporal position receive a reward and therefore which signal reaches the optimizer. Second, **feedback allocation** determines the long-term distribution of training actions: even fully correct feedback concentrated on a few targets can reorganize shared functional support. Proxy mismatch changes the objective assigned to actions; excessive concentration of correct feedback changes the sequence of actions. Both operate through **feedback → actual action → functional support and capability**, with distinct consequences.

**Internal anchors.** RL-E01/E02: feedback binding and causal credit alter training effects. RL-E06: concentrated correct feedback can also redistribute cross-skill support and reduce other capabilities.

### 5.1.8 Self-training: Pseudo-label gains and recursive model collapse

**Positive finding — Noisy Student and self-training (Xie et al.).** Pseudo-labels generated by a model can expand training data for a student, improving ImageNet classification and some robustness metrics. Generated data can therefore serve as beneficial feedback into learning.

**Contrasting finding — recursive model collapse (Shumailov et al.).** When successive models predominantly train on previous models' generated data, low-probability patterns and distribution tails can progressively disappear. Retaining genuine data across iterations (Gerstgrasser et al.) changes this long-term information-loss process.

**TLI unification.** Both studies use a feedback chain: inference outputs enter future training data, the data distribution shapes realized actions, and those actions change later learned states and inference distributions. Diverse, high-quality pseudo-labels can enlarge the effective training signal. Recursive replacement can diminish input for tail patterns and weaken the functional support they rely on; continual real-data input changes the training distribution and preserves learning opportunities for those patterns.

**Internal anchors.** TL-E07: training updates persistently reorganize support. RL-E06: feedback allocation changes support concentration and capability retention, with recovery after rebalancing.

### 5.1.9 Batch Normalization: Training gains and their mechanism

**Positive finding — Batch Normalization (Ioffe and Szegedy).** BN normalizes intermediate activations during training and improves speed and stability in various deep networks. The original explanation emphasized reduction of internal covariate shift.

**Contrasting finding — optimization smoothness (Santurkar et al.).** Later controlled studies found no necessary relation between BN's training benefit and the expected change in internal covariate shift. Changes to the loss landscape, gradient predictability and effective step size more directly affect optimization.

**TLI unification.** BN changes the receiving state and local functional mapping on which actual updates act, leading to different responses under nominally similar optimization settings. Internal activation statistics and local optimizer geometry are different readouts of a receiving state; training improvements emerge from the joint evolution of state, action and functional response. The original empirical gain and the later mechanism study characterize the intervention effect and its dynamical basis.

**Internal anchors.** TL-E03: identical formed updates act differently across receiving states. TL-E04: actual updates produce state-conditioned finite-amplitude responses.

### 5.1.10 Large-Batch Training: Generalization gap and training-strategy compensation

**Positive finding — large-batch generalization gap (Keskar et al.).** Some large-batch experiments report worse test performance than small-batch training and differences in the sharpness of learned solutions and optimization trajectories.

**Contrasting finding — learning-rate scaling and warmup (Goyal et al.; Hoffer et al.).** With suitable learning-rate choices, warmup, training duration and related adjustments, large-batch training can approach small-batch accuracy.

**TLI unification.** Batch size influences realized actions through sampled gradients, noise covariance and optimizer history. Learning-rate changes and warmup affect action magnitudes and receiving-state trajectories. The generalization gap and its mitigation through training strategy are therefore associated with different action distributions and paths of functional-support formation. The common chain is **sampling and optimization rules → actual action → response at the receiving state → learning outcome**.

**Internal anchors.** TL-E03: receiving-state dependence and optimizer-memory effects on action formation. TL-E05: target-specific update geometry F3 and receiving-state factors F5 condition responses.

### 5.1.11 Scaling Laws and Chinchilla: Scaling regularities versus compute-optimal allocation

**Positive finding — neural language model scaling laws (Kaplan et al.).** Under the training conditions studied, model size, data and compute exhibit stable empirical power-law relationships with cross-entropy loss, informing resource allocation.

**Contrasting finding — compute-optimal Chinchilla training (Hoffmann et al.).** Joint sweeps of parameters and training tokens show that, at fixed compute, a smaller model trained on more data can outperform a larger but undertrained model, yielding a different compute-optimal allocation.

**TLI如何统一。** 模型规模、数据暴露量和计算预算共同控制可达到的接收状态与训练动作序列。某一资源瓶颈占主导时可形成稳定的局部幂律；数据瓶颈与模型瓶颈的相对作用变化时，最优参数量和训练token分配随之变化。两类规律分别描述训练动力学在不同有效资源配置下的宏观表现。

**内部实验锚点。** TL-E03：接收状态影响更新响应；TL-E04：有限动作响应存在非线性；TL-E07：持续更新重组功能支撑；ResNet、Diffusion U-Net、Vision-MoE等跨系统实验：检验相同动力学角色在不同体系中的表达。

### 5.1.12 Lottery Ticket与Rewinding：初始子网络与早期训练历史

**正面理论／结果——Lottery Ticket Hypothesis（Frankle与Carbin）。** 适当稀疏子网络在保留特定初始权重时，能够通过重新训练达到与原网络相近的表现，显示初始化与网络结构对后续学习具有作用。

**反面理论／结果——Rewinding与早期训练状态（Frankle等；Renda等）。** 在更复杂的网络及训练条件中，将稀疏子网络恢复到训练早期的权重或优化状态，常能获得比直接回到最初初始化更稳定的训练结果。

**TLI如何统一。** 初始化确定最初接收状态，早期实际更新继续塑造参数与功能组织。Winning Ticket体现初始结构对可达学习路径的影响；Rewinding利用了早期更新形成的新接收状态。两者通过“初始状态→实际更新→接收状态演化→后续功能形成”的同一关系连接。

**内部实验锚点。** TL-E03：接收状态与优化器历史影响实际更新及其响应；TL-E07：更新带来持久功能支撑重组。

### 5.1.13 真实数据泛化与随机标签记忆：拟合能力和学习组织

**正面理论／结果——深度网络在真实任务上的泛化。** 高容量神经网络能够在自然数据上取得较高的训练与测试表现，说明训练可以形成适用于未见样本的预测功能。

**反面理论／结果——Rethinking Generalization（Zhang等）。** 同类高容量网络也能记忆随机标签，将训练误差降低至接近零；因此，相近的训练拟合能力可以伴随完全不同的测试泛化结果。

**TLI如何统一。** 网络容量给出可实现的功能空间，具体数据和实际训练动作决定最终形成的功能支撑。真实数据中的可迁移规律与随机标签中的样本特定关联，会引导不同的支撑组织与边界几何。训练集正确率相近时，已形成的学习状态与测试目标的功能响应仍可明显不同。

**内部实验锚点。** TL-E03：训练响应依赖实际接收状态；TL-E06：功能由分布式组件支撑；TL-E07：真实更新重组支撑；TL-E08：可观察能力取决于目标读出边界。

### 5.1.14 Classical Bias–Variance与Double Descent：复杂度曲线和插值阈值

**正面理论／结果——经典偏差—方差权衡。** 在经典统计学习条件下，模型复杂度上升可降低偏差，同时增加方差风险，测试误差常呈现先降后升的单谷结构。

**反面理论／结果——Double Descent（Belkin等；Nakkiran等）。** 在现代插值及过参数训练条件下，测试误差可在插值阈值附近上升，并在继续增大模型规模或训练程度后再次下降；模型、样本及训练轮次的不同控制轴均出现过相应现象。

**TLI如何统一。** 模型复杂度控制可达解空间，实际动作决定进入其中哪一类解；接近插值边界时，拟合噪声的高敏感方向可以放大测试响应。进一步增加冗余并改变隐式解选择后，噪声支撑可转移至对总体分布影响较小的方向。经典单谷区间与插值阈值之后的第二次下降，是接收状态、动作选择和泛化读出几何在不同区域的结果。

**内部实验锚点。** TL-E03与TL-E04：接收状态和有限动作决定功能响应；TL-E07：支撑结构随更新持续变化；TL-E08：能力由目标读出边界判定。

### 5.1.15 对抗鲁棒性：自然准确率与扰动下的能力权衡

**正面理论／结果——标准训练与对抗训练（Madry等）。** 标准训练可获得较高自然测试准确率；在给定扰动集合上实施对抗训练，则可增强模型抵抗相应扰动的能力。

**反面理论／结果——对抗脆弱性与鲁棒—准确率权衡（Tsipras等）。** 自然分布上的高准确率可以与小扰动下的错误预测并存；提高扰动鲁棒性的训练在部分任务中伴随自然准确率下降，并改变模型使用的特征。

**TLI如何统一。** 自然准确率测量原始目标的读出状态，鲁棒性测量邻域中一组目标的读出边界与间隔。训练目标及扰动分布改变实际更新，进而重组对自然与扰动输入的功能支撑。因此，高自然准确率、局部脆弱性以及对抗训练后的能力权衡对应不同目标集合和学习组织。

**内部实验锚点。** TL-E06：功能支撑具有组件依赖和协同结构；TL-E07：更新可重新分配支撑；TL-E08：目标读出边界决定正确性转变。

### 5.1.16 Shortcut Learning：IID准确率与纹理—形状偏好

**正面理论／结果——ImageNet CNN的高准确率。** 卷积神经网络能够利用训练数据中的预测特征，在同分布图像分类测试中取得较高准确率。

**反面理论／结果——Texture Bias与Stylized-ImageNet（Geirhos等）。** 多种CNN更依赖纹理而非形状线索；改变训练数据的视觉统计后，模型的形状偏好及分布外鲁棒性随之改变。

**TLI如何统一。** 同一正确预测可以依靠不同的分布式功能支撑实现。IID准确率记录了当前输入分布上的读出结果；纹理、形状等支撑路径由数据与实际更新共同形成。训练环境改变后，支撑结构可发生重组，由此改变模型在风格变化或分布迁移下的表现。

**内部实验锚点。** TL-E06：同一功能存在组件必要性、替代与协同；TL-E07：训练更新重组功能支撑；TL-E08：不同目标的边界状态决定可观察能力。

### 5.1.17 Emergent Abilities：规模跃迁与度量方式

**正面理论／结果——LLM Emergent Abilities（Wei等）。** 某些语言模型能力在规模增加时呈现陡峭的基准测试跃迁，尤其在采用正确／错误或通过率指标时具有明显的阈值表现。

**反面理论／结果——Emergence as a Mirage（Schaeffer等）。** 改用连续评分或其他合理度量后，一些表面上的突变可呈现更加平滑的性能变化，显示读出规则会影响跃迁的外观。

**TLI如何统一。** 学习状态与功能支撑随训练和规模条件演化，评价函数将这些内部状态投影为连续分数或离散能力结果。当目标间隔越过零边界时，正确率与通过率可以发生突变；连续度量则显示更细的功能变化。不同评价曲线对应同一功能形成过程的不同读出方式。

**内部实验锚点。** TL-E07：持续的内部支撑重组；TL-E08：目标边界跨越决定能力转变；TL-P01：利用更新前信息预测更新后的正确性类别。

### 5.1.18 长上下文：信息可访问与Lost in the Middle

**正面理论／结果——长上下文输入能力。** 长上下文模型可以将大量文本信息放入同一次推理的可访问输入范围，使回答有机会依赖远距离证据。

**反面理论／结果——Lost in the Middle（Liu等）。** 多文档检索与长上下文任务发现，模型对相关内容的利用受到其在上下文中位置的影响，位于中间位置的信息常比开头或末尾更难被有效使用。

**TLI如何统一。** 输入信息进入上下文后，还需经过查询依赖的支撑调用、路由、组合与目标绑定才能影响输出。位置变化会改变瞬时推理中的组件作用和信息组合路径。因此，“输入中存在证据”与“证据成为当前回答的有效功能支撑”对应不同的推理环节。

**内部实验锚点。** INF-E01：冻结学习状态下，组件效应依赖查询；成对干预揭示非加性交互；准确的历史组件回滚显示已学习版本对当前推理的作用。

### 5.1.19 Chain-of-Thought：推理收益与文本轨迹忠实性

**正面理论／结果——Chain-of-Thought Prompting（Wei等）。** 要求模型生成中间推理步骤，可以改善多步计算、符号处理等复杂任务的最终解答表现。

**反面理论／结果——Unfaithful Chain-of-Thought（Turpin等）。** 受控提示实验发现，输出的自然语言推理说明有时遗漏实际影响决策的偏置来源，说明可读推理文本与内部因果计算之间可以存在差别。

**TLI如何统一。** CoT提示改变冻结模型在当前查询中的瞬时计算、支撑调用和信息组合，因而能够影响答案；生成的文字步骤则是这些计算的一个可观察输出。有效的推理计算与文字说明的忠实程度，是推理过程中两个不同的功能测量对象。

**内部实验锚点。** INF-E01：冻结状态下的查询依赖组件门控、非加性支撑组合和历史版本回滚揭示推理行为的内部功能路径。

### 5.1.20 Test-time Compute：增加推理搜索与收益差异

**正面理论／结果——搜索与推理时计算（如Tree of Thoughts）。** 在固定模型参数的条件下，拓展候选路径、增加搜索和回溯步骤可以改善某些需要规划、检验或组合的任务。

**反面理论／结果——计算预算的任务依赖效应。** 额外搜索与采样的收益受任务类型、候选质量、路由和选择规则影响；增加计算预算时，部分任务的收益会减弱或出现无效分支。

**TLI如何统一。** 学习状态冻结后，推理仍能对已有功能支撑执行多轮调用、组合、评价与选择。额外计算扩大了瞬时探索范围；其实际收益取决于当前查询与被调用支撑之间的对应关系。因此，同样的计算增量在不同问题上产生不同结果，符合查询依赖的推理动力学。

**内部实验锚点。** INF-E01：冻结推理中的查询依赖调用、组件间非加性交互以及回滚与恢复实验。

### 5.1.21 持续学习：灾难性遗忘与EWC保护

**正面理论／结果——Catastrophic Forgetting。** 神经网络依次学习新任务时，后续训练会在某些情况下损害已掌握任务的表现，形成明显的旧能力遗忘。

**反面理论／结果——Elastic Weight Consolidation（Kirkpatrick等）。** EWC根据旧任务的Fisher信息估计参数重要性，对敏感方向的后续变化施加更强约束，从而在持续学习实验中缓解旧任务性能下降。

**TLI如何统一。** 新任务的实际更新作用于同时承载新旧能力的接收状态。更新与旧功能支撑敏感方向的重叠及响应符号，决定旧目标间隔是扩大还是收缩；累积收缩跨越边界后表现为遗忘。EWC通过改变实际动作的几何分布，降低旧功能高敏感方向上的不利响应。其他保护与恢复方法也通过改变动作及支撑重组发挥作用。

**内部实验锚点。** TL-E03：相同更新在不同接收状态产生不同旧目标响应；TL-E07：更新重新分配支撑；TL-E08：目标边界跨越决定能力损失；RL-E06：集中反馈导致旧能力间隔降低，重新平衡反馈后能力恢复。
