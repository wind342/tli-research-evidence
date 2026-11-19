# Scientific assessment

## Feedback concentration as an intervention coordinate

In the executed shared finite GRU, All updated branches started from the
same mastered parameter--AdamW state, used equal episode and update budgets,
and differed only in how exact positive feedback was distributed across the
four skills. In all 12 formal seeds, increasing concentration strictly increased
the reinforced skill's functional-support share and strictly decreased the
other skills' mean margin. The frozen exposure control preserved its initial
state exactly.

## Reward authority and controlled feedback

Every reward came from the exact terminal two-action task rule. The four updated
branches differed in how correct feedback was allocated among skills. The protocol
used the same initial parameter--AdamW state and episode/update budgets, and
included no learned reward model, entropy bonus or negative reward.

## Continuous margins and discrete capability loss

At the final dose endpoint, mild and high branches still achieved exact
discrete accuracy for the three other skills, while their mean margins were
already lower in strict dose order. The continuous target boundary state thus
detected graded erosion before the external correctness result necessarily
changed. Exclusive feedback then crossed many of those boundaries as its
duration increased.

## Recovery from the common update-800 state

Rebalancing feedback after the exact exclusive update-800 state
raised other-skill accuracy from 70.31% to 99.48%, an observed recovery of
29.17 percentage points, and retained the reinforced skill at 100% in every
seed. Its endpoint was 38.54 points above the matched branch that continued
exclusive feedback from update 800 to update 3,200 and ended at 60.94%. The
support profile moved toward the balanced reference in 12/12 seeds. The matched recovery interventions establish that the observed losses are
reversible through changes in feedback allocation.

The other-skills-only repair is informative in the opposite direction: it
restored the other skills to 99.83% but reduced the formerly reinforced skill
to 89.06%. Feedback direction therefore reorganized the shared functional
system both ways.

## Feedback mechanism within TLI

Inference projects functional support already formed by learning. When one
class of projected success repeatedly supplies the next training action, the
resulting positive feedback can further reorganize shared support toward that
class. This explains both sides of the loop: focused feedback can efficiently
strengthen a selected capability, but the same mechanism can reduce the margin
and eventual boundary reliability of capabilities omitted from feedback.

## Tested system and result

The registered evidence concerns a shared finite GRU, four mastered skills,
12 formal seeds and feedback schedules extending to 3,200 updates. In this
system, concentrating correct positive feedback produced dose- and
duration-dependent support and capability changes. Rebalancing feedback
causally reversed the observed trade-off.
