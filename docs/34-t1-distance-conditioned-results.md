# 34 — T1 exact-distance Pachner results

## Status

**T1 is rejected by A-023 on the measured generated distribution.**

T1 is a falsification experiment, not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security claim.

## Question

T0 failed because planted walk length did not control true quotient distance. T1 removes that defect by constructing the complete canonical quotient BFS ball around the deterministic burn-in state and choosing a target from the exact shell

~~~text
S_D = { R : d(R0,R) = D }.
~~~

The public bound is exactly `D`, and any legal Pachner path within the bound is accepted.

Target selection deliberately weakens the cheapest public lower bound: among states in `S_D`, it first maximizes slack

~~~text
D - |tetrahedra(R1) - tetrahedra(R0)|,
~~~

then minimizes capped shortest-path multiplicity before seeded tie-breaking.

## Exact-head measurements

Fixed seed:

~~~text
76120450aabbccddeeff001122334455
~~~

Python 3.12 dedicated CI:

| Set | D | Shell sizes | Ball | Target tet delta/slack | Shortest paths | Shortest predecessors | Bidir F/R visited | Bidir expanded | A* visited/expanded |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| t1-2 | 2 | 1/8/31 | 40 | 0/2 | 1 | 1 | 9/4 | **2** | 21/2 |
| t1-3 | 3 | 1/8/31/83 | 123 | 1/2 | 1 | 1 | 9/14 | **5** | 119/36 |

Detailed `t1-3` shell construction:

~~~text
exact distance/public bound:        3/3
shell sizes:                        (1, 8, 31, 83)
ball size/expanded:                 123/40
raw moves/unique neighbors:         639/420
local neighbor collisions:          219
revisit hits:                       298
max shell frontier:                 83
tetrahedron histograms:
  d=0: ((17,1),)
  d=1: ((18,8),)
  d=2: ((17,4),(19,27))
  d=3: ((18,14),(20,69))
mean tetrahedron slack by shell:    (0, 0, 0.2581, 0.3373)
target tetrahedron delta/slack:     1/2
max-slack candidates:               14
min-path finalists:                 1
target shortest paths:              1
shortest predecessors:              1
reference witness valid:            yes

BFS:
  distance:                          3
  visited/expanded/frontier:         119/36/84

bidirectional BFS:
  distance:                          3
  forward/reverse visited:           9/14
  expanded:                          5

public tetrahedron-count A*:
  distance:                          3
  visited/expanded/frontier:         119/36/72
~~~

Wall-clock values are omitted from the interpretation because they are runner-dependent; exact distances and state counts are the evidence.

## A-023 — exact-distance bidirectional recovery

T1 successfully fixes T0's immediate generator bug: the published target really is at the promised quotient distance, and the chosen `t1-3` target has a unique shortest path under the measured cap.

That does **not** create useful generated-instance resistance. Bidirectional search reaches the exact target after only five quotient-state expansions at `D=3`. At `D=2` it needs only two expansions.

This triggers T1's pre-declared rejection condition that bidirectional search remains tiny even for exact-distance-conditioned targets.

The failure is especially informative because the selected target is not nearly certified by tetrahedron count: at `D=3` its tetrahedron-count lower bound is only 1, leaving slack 2. The simple A* heuristic therefore gives no advantage over BFS on the measured instance, yet generic bidirectional search is still tiny.

## Decision

**Reject the current BTTS/Pachner generated-distribution direction. Do not add `t1-4` merely to obtain larger numbers.**

This result is not a theorem that bounded Pachner reconfiguration is easy, nor does it contradict worst-case NP-hardness results for related bistellar-move problems. It shows only that the current small canonical 3-sphere distribution does not provide evidence of average-case cryptographic hardness.

Because the first decisive rejection condition already fired, the remaining heavier T1 gates (industrial bounded planning/SAT/CP-SAT, richer degree/link heuristics, and larger-depth interaction measurements) are not prerequisites for rejecting this generator. They remain attack requirements for any future BTTS distribution that first survives the cheap exact and bidirectional gates.

## Next frontier

Return to the K2.4 ranking and test **HGES — Hidden Gluing Equivalence Search** next.

The first HGES experiment should intentionally use a family with a known canonical decomposition and verify that the public attack harness recovers the assembly. That experiment is a negative control. Only after the canonical-decomposition attack is validated should a noncanonical/overlapping gluing distribution be considered.

No security or post-quantum claim exists.
