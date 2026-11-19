# Historical FoCM inference example — English working note

**Document role:** Historical FoCM draft, now expressed in English. The canonical wording used in the current TLI/ICML paper is [Section 5, *This Is a Simple Theory*](https://github.com/wind342/tli-paper/blob/icml-final/icml/sections/simple.tex). The current paper is *Unified Dynamics of Training, Learning, and Inference in Neural Networks* (TLI).

This note records the elementary ReLU-gating and version-rollback example developed during the earlier FoCM drafting process. The source example is a mathematical illustration, with INF-E01 and cross-system experiments supplying empirical evidence.

### Inference recruits and combines learned computation

Consider a single nonlinear neuron with two learned input weights:

$$
f_\theta(x)=\operatorname{ReLU}(ax_1+bx_2).
$$

At the fixed learned state $\theta^*=(2,1)$, the two component contributions are $s_1(x)=2x_1$ and $s_2(x)=x_2$, and inference produces

$$
Y_x=\operatorname{ReLU}(s_1(x)+s_2(x)),
\qquad \Delta_{\mathrm{inf}}L=0.
$$

The same learned components contribute differently under different inputs. Their combination can also be non-additive. To measure this, introduce reversible component gates $g_1,g_2\in\{0,1\}$ and evaluate

$$
f_{g_1,g_2}(x)=
\operatorname{ReLU}(2g_1x_1+g_2x_2).
$$

For $x=(-1,1)$, the four gated outputs $(f_{11},f_{10},f_{01},f_{00})$ are $(0,0,1,0)$, giving the exact interaction

$$
I_{12}=f_{11}-f_{10}-f_{01}+f_{00}=-1.
$$

For $x=(1,1)$, the same interaction is zero. Thus query-dependent functional contributions and non-additive component effects arise from elementary nonlinear computation with unchanged learned parameters.

Inference also depends on the versions formed through learning. Replacing the trained first-component weight $a^*=2$ with a pre-learning version $a_{\mathrm{pre}}=1$ changes the output at $x=(1,1)$ from $3$ to $2$; exact restoration recovers the original result. The gates and version replacements are diagnostic interventions, distinct from ordinary inference.

These calculations illustrate the TLI inference relation: a fixed learned state supplies functional components, the current input determines their contributions, and nonlinear computation combines them into an output. No persistent learning update is required.

### Feedback closes the loop

When the consequences of inference enter subsequent training, they can change the next training action and thereby the learned computation available to later inference:

$$
Y_t\longrightarrow B_{t+1}
\longrightarrow A_{t+1}\longrightarrow Z_{t+2}.
$$

Inference preserves the current learned state; feedback-driven training can change the learned state used by future inference.

## Historical editing context

- Harmonize symbol use, section numbering, and equation references with the destination manuscript.
- The component gates and parameter-version substitutions are measured interventions.
- The current TLI manuscript already contains the ReLU example and a feedback-to-subsequent-training relation. Refer to the canonical LaTeX source for its final wording.

