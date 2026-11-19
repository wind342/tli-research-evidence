> **TLI research hypothesis (pending empirical tests).** This note examines task horizon, training duration and cross-capability forgetting. The [current ICML paper-to-evidence map](../TLI_ICML_PAPER_EVIDENCE_MAP.md) identifies the already completed experiments. Predictions introduced here remain research hypotheses.

# TLI Research Note: Task Horizon, Training Duration, and Cross-Capability Forgetting

**Proposed:** November 6, 2026  
**Status:** A theoretical explanation and testable predictions derived from established TLI relations.  
**Question:** Why might forgetting appear particularly pronounced in real-world reinforcement learning (RL), compared with supervised fine-tuning (SFT)?

## 1. Main proposition

**Cross-capability interference can arise whenever training modifies shared model parameters; its underlying computation is common to RL and SFT.**

This note identifies two factors that may make forgetting appear more prominent in practical RL:

1. **Task-horizon effect:** Complex, long-horizon tasks often involve multiple stages and capabilities, recruiting broader distributed functional support. Training on the entire trajectory can form updates that affect a larger collection of shared functional relationships. Existing capabilities may consequently receive positive or negative target-specific responses.
2. **Training-duration effect:** Continued updates accumulate each previous target's functional responses. Observable forgetting occurs when the cumulative negative response to a formerly correct target crosses its capability boundary. RL is frequently applied through repeated long-horizon interaction, feedback and subsequent training, which may make these effects more prominent in practice.

The proposed explanation is that **RL and SFT share the same update–response mechanism, whereas their task-horizon distributions, training durations and update schedules may differ**.

When matched on task content and training conditions, RL and SFT might cause similar damage to previously acquired capabilities. That comparison is a **prediction to be tested**, rather than a result from a completed matched RL/SFT study.

## 2. Established TLI computational basis

The experimentally established relations among actual training updates, receiving-state-dependent functional responses, distributed support and capability readouts are described in the [TLI unified dynamics](../theory/TLI_UNIFIED_DYNAMICS.md) and the current paper's *This Is a Simple Theory* section.

For a target \(q\) evaluated in a shared learned state, the response to one realized update is

\[
R_{t,q}=m_q(L_{t+1})-m_q(L_t).
\]

The same update can produce responses of different signs for different targets, regardless of which training paradigm formed it. Applying **exactly the same realized update to exactly the same receiving state** produces the same immediate target responses. However, training paradigms presented with the same one-step task can form different realized updates. Similar forgetting under matched RL/SFT conditions is therefore a testable prediction, not an identity implied by task equivalence.

Over continued training, exact telescoping gives

\[
m_q(L_T)=m_q(L_0)+\sum_{t=0}^{T-1}R_{t,q}.
\]

For a previously correct target satisfying \(m_q(L_0)>0\), if

\[
\sum_{t=0}^{T-1}R_{t,q}\le -m_q(L_0),
\]

then the target crosses its correctness boundary and exhibits an observable capability loss. Thus **training duration** is mathematically linked to the **accumulated target response**. Whether that response remains negative depends on the actual training trajectory; individual updates need not damage previously acquired capabilities.

The support for a target is measured by \(P_{t,q}=\mathcal P_q(L_t;\mathcal J_q)\) under a fixed component-intervention protocol. Multi-stage task behavior and trajectory-level training provide a possible computational route for involving a broader collection of shared functional components. The relevant quantity is the **actual support recruited or affected by the updates**, rather than the nominal number of task steps alone.

## 3. Explanation for practical RL forgetting

**Common mechanism:** Both RL and SFT change the persistent learned state through actual updates. Both can improve the trained target while weakening other capabilities.

**Task-horizon effect:** A long-horizon task may require the coordination of multiple functions. Its training updates may act on more shared support. When previously mastered targets have negative responses along those update directions, the range of affected targets can increase. The same mechanism applies to long-horizon SFT.

**Duration effect:** Repeated updates allow negative responses to accumulate until a previously correct target crosses its decision boundary. Continued feedback influences the formation and allocation of future training actions; the direct mathematical mechanism remains actual updates, target-specific responses and capability readouts.

**Application-distribution effect:** If practical RL is used more frequently than SFT for complex long-horizon tasks or longer feedback-training schedules, the observed frequency or severity of RL forgetting may be greater. This separates the training **method** from **task horizon, training duration and the organization of realized updates**.

## 4. Existing experimental anchors

- **TL-E03–E05:** Receiving states and actual updates jointly determine target responses, including nonlinear and state-conditioned effects.
- **TL-E06–E07:** Different capabilities have distributed functional support that can interact and be reallocated.
- **TL-E08:** Continuous target-margin changes yield discrete capability changes when a target crosses its registered boundary.
- **Current paper, *This Is a Simple Theory*:** One update may improve target A while producing positive or negative responses in other targets, through shared computation.
- **[RL-E06 formal results](../experiments/gfg_rl_selective_positive_feedback_dose_recovery_v1/RESULTS.md):** Starting from a mastered four-skill GRU, 3,200 updates of concentrated correct feedback progressively changed support and the other skills' behavior. Under exclusive feedback, mean accuracy of the other skills fell from **88.89% at update 100** to **60.94% at update 3,200**. Rebalanced feedback raised their accuracy from **70.31% at the common update-800 fork** to **99.48%**. This experiment manipulated **feedback allocation and duration**; it did not perform a matched RL/SFT task-horizon comparison.

These experimental anchors support the underlying mechanistic relations. The proposed explanation for differences between practical RL and SFT is an **additional research prediction** based on those relations.

## 5. Specific testable predictions

Let \(H\) denote task horizon, \(T\) the number of training updates, \(M\in\{\mathrm{RL},\mathrm{SFT}\}\) the training method, and \(Q_{\rm old}\) the set of previously mastered targets. Compare matched runs beginning from the same parameters and optimizer state.

- **Matched short-task prediction:** On single-stage tasks, RL and SFT may cause similar damage to older capabilities when improvements on the trained target and realized-update conditions are comparable.
- **Matched long-task prediction:** On the same long task, with matched training duration and target improvement, RL and SFT may still show comparable forgetting. The breadth of affected support may explain more of the damage than the method label alone.
- **Horizon prediction:** As a task involves more distinct capability stages, the support recruited by training and the range of old targets receiving negative responses may increase.
- **Duration prediction:** For old targets receiving persistent negative responses, more updates increase cumulative margin loss and the chance of crossing a capability boundary. This can occur under either training method.
- **Practical-distribution prediction:** RL may display more prominent observed forgetting when its real-world task and duration distributions favor longer and more complex settings, even without an additional method-specific destructive mechanism.

A controlled comparison would vary \(H\) (e.g., 1, 5 and 10 stages) and \(T\) (multiple fixed update checkpoints) independently. RL and SFT would start from the same model, train on matched task content, and record new-target improvement, old-target correctness, continuous margins, realized updates and intervention-measured support changes. Training steps, trajectory/token budgets and achieved target performance should all be reported to separate method effects from unequal training intensity.

One possible old-capability failure rate is

\[
F(H,T,M)=\frac{1}{|Q_{\rm old}|}\sum_{q\in Q_{\rm old}}
\mathbf1\!\left[m_q(L_0)>0\ \land\ m_q(L_{H,T,M})\le0\right].
\]

Report continuous responses and support changes for each old target alongside endpoint correctness. The comparison can separate **task-horizon, training-duration and training-method effects, including their interactions**.

## 6. Relation to the current paper

This note combines three established ideas into a testable account of practical forgetting: **both RL and SFT can cause forgetting**, **complex long-horizon tasks may involve broader functional support**, and **repeated updates accumulate target-specific functional responses**. The existing paper supplies the underlying equations and experimental anchors, while the matched RL/SFT hypotheses remain to be tested.

**Summary:** In the TLI account, forgetting follows from the responses of existing targets to shared-parameter updates. The prominence of forgetting in practical RL may be driven partly by the combination of **task horizon and training duration**, rather than by an intrinsic destructive mechanism unique to RL.
