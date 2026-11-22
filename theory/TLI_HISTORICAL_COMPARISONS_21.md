> **TLI research comparisons:** Twenty-one paired results from previously published research, used to examine the explanatory relationships provided by TLI. These are literature comparisons, separate from the eight core nanoGPT experiments and fourteen formal mathematical recoveries.

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

**Internal anchors.** TL-E03: receiving-state dependence. TL-E04: nonlinear finite-amplitude responses. TL-E06: persistent support reorganization through actual updates.

### 5.1.3 Grokking: Delayed observable capability and earlier internal formation

**Positive finding — Grokking (Power et al.).** Training accuracy may saturate well before test generalization, which can improve abruptly after a long delay, producing an apparent transition in externally measured capability.

**Contrasting finding — circuits underlying grokking (Nanda et al.).** Tracking internal computational circuits shows that the structures supporting generalization can form and reorganize continuously before the sudden test-accuracy transition. Internal learning may therefore precede the observed capability change.

**TLI unification.** Learning corresponds to persistent reorganization of functional support, whereas capability is the observable result of crossing a target-specific readout boundary. Support can change continuously even when correctness is determined by the sign of a target margin; crossing zero converts accumulated internal changes into a discrete observed transition. The two lines of research measure internal formation and external readout within the same process.

**Internal anchors.** TL-E05: distributed support measured by component interventions. TL-E06: actual updates reorganize support. TL-E07: capability transitions depend on readout boundaries. TL-P01: prediction of post-update target-boundary outcomes.

### 5.1.4 Neural Collapse: Saturated accuracy and continuing representation formation

**Positive observation — saturated correctness readout.** When all training examples are correctly classified and training error reaches zero, the discrete correct/incorrect metric reaches a plateau; subsequent updates do not increase the number of already-correct examples under that metric.

**Contrasting finding — Neural Collapse (Papyan et al.).** Even after zero training error, deep features and classifiers can continue evolving toward particular within-class concentration, between-class mean geometry and classifier-direction relationships.

**TLI unification.** Accuracy records which side of the target-specific decision boundary an output occupies, whereas learning concerns the persistent functional organization. Continued training can change margins, component allocations and feature geometry after discrete correctness has stabilized. The same training period can therefore show constant observed accuracy and changing internal structure.

**Internal anchors.** TL-E06: support can reorganize without a capability change. TL-E07: the readout boundary determines capability state. RL-E06: margins evolve before correctness declines.

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

**Internal anchors.** TL-E06: training updates persistently reorganize support. RL-E06: feedback allocation changes support concentration and capability retention, with recovery after rebalancing.

### 5.1.9 Batch Normalization: Training gains and their mechanism

**Positive finding — Batch Normalization (Ioffe and Szegedy).** BN normalizes intermediate activations during training and improves speed and stability in various deep networks. The original explanation emphasized reduction of internal covariate shift.

**Contrasting finding — optimization smoothness (Santurkar et al.).** Later controlled studies found no necessary relation between BN's training benefit and the expected change in internal covariate shift. Changes to the loss landscape, gradient predictability and effective step size more directly affect optimization.

**TLI unification.** BN changes the receiving state and local functional mapping on which actual updates act, leading to different responses under nominally similar optimization settings. Internal activation statistics and local optimizer geometry are different readouts of a receiving state; training improvements emerge from the joint evolution of state, action and functional response. The original empirical gain and the later mechanism study characterize the intervention effect and its dynamical basis.

**Internal anchors.** TL-E03: identical formed updates act differently across receiving states. TL-E04: actual updates produce state-conditioned finite-amplitude responses.

### 5.1.10 Large-Batch Training: Generalization gap and training-strategy compensation

**Positive finding — large-batch generalization gap (Keskar et al.).** Some large-batch experiments report worse test performance than small-batch training and differences in the sharpness of learned solutions and optimization trajectories.

**Contrasting finding — learning-rate scaling and warmup (Goyal et al.; Hoffer et al.).** With suitable learning-rate choices, warmup, training duration and related adjustments, large-batch training can approach small-batch accuracy.

**TLI unification.** Batch size influences realized actions through sampled gradients, noise covariance and optimizer history. Learning-rate changes and warmup affect action magnitudes and receiving-state trajectories. The generalization gap and its mitigation through training strategy are therefore associated with different action distributions and paths of functional-support formation. The common chain is **sampling and optimization rules → actual action → response at the receiving state → learning outcome**.

**Internal anchors.** TL-E03: receiving-state dependence and optimizer-memory effects on action formation.

### 5.1.11 Scaling Laws and Chinchilla: Scaling regularities versus compute-optimal allocation

**Positive finding — neural language model scaling laws (Kaplan et al.).** Under the training conditions studied, model size, data and compute exhibit stable empirical power-law relationships with cross-entropy loss, informing resource allocation.

**Contrasting finding — compute-optimal Chinchilla training (Hoffmann et al.).** Joint sweeps of parameters and training tokens show that, at fixed compute, a smaller model trained on more data can outperform a larger but undertrained model, yielding a different compute-optimal allocation.

**TLI unification.** Model size, exposure to data and compute budget jointly constrain reachable receiving states and training-action trajectories. A dominant resource bottleneck may yield a stable local power law; shifting data and model bottlenecks changes the compute-optimal allocation of parameters and tokens. These laws describe aggregate behavior of training dynamics under different effective resource configurations.

**Internal anchors.** TL-E03: receiving states condition response to updates. TL-E04: nonlinear finite-amplitude responses. TL-E06: sustained updates reorganize support. ResNet, diffusion U-Net and Vision-MoE cross-system tests: analogous dynamical roles in distinct architectures.

### 5.1.12 Lottery Tickets and Rewinding: Initial subnetworks and early training history

**Positive finding — Lottery Ticket Hypothesis (Frankle and Carbin).** Suitably chosen sparse subnetworks can, when retaining particular initial weights, retrain to performance close to the full network, demonstrating the influence of initialization and architecture on subsequent learning.

**Contrasting finding — rewinding and early training states (Frankle et al.; Renda et al.).** In more complex architectures and regimes, rewinding sparse subnetworks to early trained weights or optimizer states often gives more reliable training than returning them to the original initialization.

**TLI unification.** Initialization specifies the first receiving state, which early realized updates further shape in both parameters and functional organization. Lottery tickets show how initial structure affects reachable learning trajectories; rewinding exploits a newly formed receiving state after early updates. Both follow **initial state → actual update → receiving-state evolution → subsequent function formation**.

**Internal anchors.** TL-E03: receiving states and optimizer history affect action formation and response. TL-E06: persistent support reorganization.

### 5.1.13 Generalization on real data versus random-label memorization

**Positive finding — generalization on natural tasks.** Large-capacity neural networks can attain high training and test performance on natural datasets, showing that training can form predictive functions useful for unseen samples.

**Contrasting finding — Rethinking Generalization (Zhang et al.).** Similar high-capacity networks can memorize random labels with nearly zero training error. Comparable fitting capacity can therefore coexist with very different test generalization.

**TLI unification.** Network capacity determines a space of attainable functions; concrete data and realized training actions determine which supporting computation is formed. Transferable regularities in real data and example-specific associations in random labels favor different support organization and decision-boundary geometry. Similar training accuracy can thus mask distinct learned states and responses on test targets.

**Internal anchors.** TL-E03: response depends on the receiving state. TL-E05: distributed component support. TL-E06: update-driven reorganization. TL-E07: observed capability depends on target-specific readout boundaries.

### 5.1.14 Classical Bias–Variance and Double Descent: Complexity curves near interpolation

**Positive finding — classical bias–variance trade-off.** In classical statistical-learning regimes, increasing complexity may reduce bias while increasing variance risk, often yielding a single-valley test-error curve.

**Contrasting finding — Double Descent (Belkin et al.; Nakkiran et al.).** Under modern interpolation and overparameterization, test error can peak near the interpolation threshold and fall again as model size or training extent increases. Related behavior has been observed along model-, sample- and epoch-wise axes.

**TLI unification.** Complexity changes the space of reachable solutions, while actual training actions select a solution within that space. Near interpolation, sensitivity to fitted noise directions can amplify test response. With greater redundancy and different implicit solution selection, noise support can shift toward directions with smaller effects on the population distribution. The classical single-valley regime and the post-interpolation descent correspond to different receiving states, action-selection mechanisms and generalization-readout geometry.

**Internal anchors.** TL-E03/E04: state and finite-action dependence. TL-E06: support evolves during training. TL-E07: target-readout boundaries determine capability.

### 5.1.15 Adversarial Robustness: Natural accuracy and perturbation-induced trade-offs

**Positive finding — standard and adversarial training (Madry et al.).** Standard training can yield high natural test accuracy, while adversarial training over a registered perturbation set can improve resistance to those perturbations.

**Contrasting finding — adversarial fragility and robustness–accuracy trade-off (Tsipras et al.).** High accuracy on natural examples can coexist with failures under small perturbations. Training to improve robustness sometimes lowers natural accuracy and changes the features used by the model.

**TLI unification.** Natural accuracy measures readouts on original targets; robustness measures readout margins and decision boundaries for a neighborhood of perturbed targets. The loss objective and perturbation distribution change actual training actions and hence functional support for natural and perturbed inputs. Strong natural accuracy, local fragility and adversarial-training trade-offs therefore concern different target collections and learned organizations.

**Internal anchors.** TL-E05: component dependency and synergy. TL-E06: redistribution of support. TL-E07: target-specific boundary crossings.

### 5.1.16 Shortcut Learning: IID Accuracy and Texture–Shape Preferences

**Positive finding — accurate ImageNet CNN classification.** Convolutional networks can exploit predictive training features to achieve strong classification accuracy on in-distribution images.

**Contrasting finding — texture bias and Stylized-ImageNet (Geirhos et al.).** Many CNNs favor texture over shape cues. Altering the visual statistics of training data changes learned shape preferences and robustness to distribution shifts.

**TLI unification.** The same correct prediction can be realized through different distributed support. IID accuracy records a readout on the observed input distribution; texture and shape pathways are organized through training data and actual updates. Changing training environments can reorganize that support and thus alter performance under style or distribution shift.

**Internal anchors.** TL-E05: component necessity, substitution and synergy. TL-E06: training reorganizes support. TL-E07: separate targets' boundary states determine observed capabilities.

### 5.1.17 Emergent Abilities: Scaling transitions and measurement choices

**Positive finding — emergent abilities of LLMs (Wei et al.).** Some language-model capabilities show sharp benchmark changes as model scale increases, particularly under binary correctness or pass-rate measurements.

**Contrasting finding — emergence as a mirage (Schaeffer et al.).** With continuous scores or other reasonable measurements, some apparently abrupt performance changes become smoother, showing how readout choices affect the apparent transition.

**TLI unification.** Learned states and functional support evolve under training and scaling conditions, while evaluation functions map those states to continuous scores or discrete capability outcomes. Binary accuracy or pass rates can change abruptly when margins cross zero; continuous measures resolve finer functional changes. Different evaluation curves may therefore represent different readouts of the same underlying formation process.

**Internal anchors.** TL-E06: continuous internal support reorganization. TL-E07: capability changes at target-specific boundaries. TL-P01: post-update correctness classes predicted from pre-response information.

### 5.1.18 Long Context: Accessible Information and Lost in the Middle

**Positive finding — long-context input capacity.** Long-context models can place large amounts of text within the available inference input, allowing answers to draw on distant evidence.

**Contrasting finding — Lost in the Middle (Liu et al.).** Multi-document retrieval and long-context studies find that use of relevant material depends on its position. Middle-position information is often less effectively used than material near the beginning or end.

**TLI unification.** Accessible context must be processed through query-dependent recruitment, routing, combination and target binding before it affects output. Position changes alter component effects and information-combination paths in transient inference. **Evidence present in the input** and **evidence functioning as support for the current answer** are distinct inferential stages.

**Internal anchor.** INF-E01: frozen-state component effects depend on the query; paired interventions reveal non-additive interactions, and precise component-version rollback identifies learned contributions to inference.

### 5.1.19 Chain-of-Thought: Reasoning Gains and Faithfulness of Textual Traces

**Positive finding — Chain-of-Thought Prompting (Wei et al.).** Requesting intermediate reasoning steps can improve answers on multistep arithmetic, symbolic and other complex tasks.

**Contrasting finding — unfaithful Chain-of-Thought (Turpin et al.).** Controlled prompting studies find that generated natural-language explanations can omit sources of bias that influence actual decisions, demonstrating a possible gap between readable explanations and internal causal computation.

**TLI unification.** CoT prompting changes the transient computations, support recruitment and information combination performed by a frozen model for the current query, potentially improving its answer. The generated verbal steps are an observable output of those computations. Functional success and faithfulness of the textual explanation are distinct measurements within inference.

**Internal anchor.** INF-E01: query-dependent component gates, non-additive support combinations and historical-version rollback reveal internal functional paths during frozen inference.

### 5.1.20 Test-Time Compute: Search Budget and Variable Gains

**Positive finding — search and inference-time computation (e.g., Tree of Thoughts).** Expanding candidate paths, search and backtracking under fixed model parameters can improve tasks requiring planning, checking or composition.

**Contrasting finding — task-dependent returns to additional compute.** Extra search and sampling depend on task type, candidate quality, routing and selection rules; increased compute can yield diminishing gains or unproductive branches.

**TLI unification.** With a fixed learned state, inference can repeatedly recruit, combine, evaluate and select existing support. Additional computation expands transient exploration, but gains depend on the match between query and recruited functionality. The same increase in compute can therefore have different effects across problems, consistent with query-conditioned inference dynamics.

**Internal anchor.** INF-E01: query-conditioned recruitment, non-additive component interactions and rollback/restoration under frozen inference.

### 5.1.21 Continual Learning: Catastrophic Forgetting and EWC Protection

**Positive finding — catastrophic forgetting.** Sequentially training neural networks on new tasks can damage performance on previously mastered tasks, producing observable loss of old capabilities.

**Contrasting finding — Elastic Weight Consolidation (Kirkpatrick et al.).** EWC uses Fisher information from earlier tasks to estimate parameter importance and penalizes later changes along sensitive directions, mitigating loss of old-task performance in continual-learning experiments.

**TLI unification.** New-task realized updates act on receiving states that support both new and old capabilities. Overlap with old-support-sensitive directions and the sign of old-target response determine whether old margins expand or contract; accumulated contraction crossing a boundary produces forgetting. EWC reshapes actual update directions to reduce harmful responses along old-function-sensitive directions. Related protection and recovery methods also act by changing updates and support reorganization.

**Internal anchors.** TL-E03: identical updates produce different old-target responses in different receiving states. TL-E06: update-driven support redistribution. TL-E07: readout-boundary crossings determine loss. RL-E06: concentrated feedback reduces old-skill margins; rebalanced feedback restores capability.
