# 16 — H2-E Escher frustrated atlas

## Status

H2-E is an executable falsification experiment inspired by Escher/Penrose impossible figures.

It is **not** a KEM, trapdoor primitive, or security candidate.

The intended phenomenon is:

> every local relationship is individually realizable, but the complete atlas may fail to admit one global realization.

## 1. Prior art: the Escher intuition is already mathematical

The local-to-global framing is established mathematics.

### Sheaf/global-section viewpoint

Abramsky and Brandenburger formalize local compatible data and obstruction to global sections in a sheaf-theoretic framework:

- *The Sheaf-Theoretic Structure Of Non-Locality and Contextuality*:
  https://arxiv.org/abs/1102.0264

Related work explicitly connects cohomological methods to constraint satisfaction and structure isomorphism:

- Adam Ó Conghaile, *Cohomology in Constraint Satisfaction and Structure Isomorphism*:
  https://arxiv.org/abs/2206.15253

### Visual paradox / Escher viewpoint

Ghrist and Cooperband explicitly model visual paradox as locally coherent relative data that cannot globalize, using network torsors and sheaf cohomology:

- *Obstructions to Reality: Torsors & Visual Paradox*:
  https://arxiv.org/abs/2507.01226

They include non-abelian visual-paradox examples, so "make the Escher obstruction non-abelian" is not itself a novelty claim.

A 2026 geometry-processing representation of impossible objects also describes global impossibility through discrete differential/cohomological obstruction:

- Dodik et al., *Meschers: Geometry Processing of Impossible Objects*:
  https://arxiv.org/abs/2605.14960

### Gain/group-labelled graphs

An edge-labelled graph with relative group values and cycle balance is standard gain/voltage-graph machinery. Balancing sets and frustrated edges are established concepts.

Parameterized algorithms also exist for Group Feedback Vertex/Edge Set style problems; for example:

- Cygan, Pilipczuk, Pilipczuk, *On group feedback vertex set parameterized by the size of the cutset*:
  https://arxiv.org/abs/1112.6255
- Bandyapadhyay et al., *Subexponential Parameterized Algorithms for Cut and Cycle Hitting Problems on H-Minor-Free Graphs*:
  https://arxiv.org/abs/2111.14196

Therefore H2-E1 is best understood as a calibration against known local/global and gain-graph structure.

## 2. H2-E1 height atlas

Let the public connected graph be:

[
G=(V,E).
]

Every canonical oriented edge (e=(u,v)), with (u<v), carries a public increment

[
d_ein mathbb Z_q,
]

initially with (q=7).

A global height assignment is:

[
h:V	omathbb Z_q.
]

A non-seam edge is satisfied when:

[
h(v)-h(u)=d_e pmod q.
]

### Local consistency

Every single edge is always satisfiable: choose any (h(u)), then set

[
h(v)=h(u)+d_e.
]

Thus no isolated local edge is "impossible."

### Global frustration

For a closed oriented cycle (C), consistency requires the signed sum of edge increments to vanish:

[
sum_{ein C}pm d_e = 0 pmod q.
]

A non-zero cycle sum is the discrete impossible-staircase effect: following locally valid relative steps around the loop returns to the same place with a different implied height.

## 3. Generator

Deterministically from a master seed:

1. build a connected cycle-rich graph;
2. sample hidden vertex heights;
3. derive a globally exact edge-increment field from those heights;
4. choose a bounded planted seam set;
5. perturb those seam-edge increments by non-zero offsets;
6. discard generation history except reference heights/seams.

The public object contains only:

- graph;
- modulus;
- edge increments;
- seam budget.

The planted seams are not part of the public verifier target.

## 4. Equivalent-witness relation

A witness is:

[
(S,h)
]

where:

- (Ssubseteq E) is a canonically encoded seam set;
- (|S|le k), with public budget (k);
- (h:V	omathbb Z_q).

The verifier accepts iff every edge outside (S) satisfies the public height relation.

Any equivalent repair is accepted. Recovering planted seams is unnecessary.

There is also a global additive gauge:

[
h(v)mapsto h(v)+c.
]

The verifier accepts every such shifted representative.

## 5. H-E01 — public fundamental-cycle syndromes

Choose a public spanning tree (T).

Tree-edge increments determine one potential assignment after fixing a root gauge.

For every chord (e
otin T), compare the implied endpoint difference with the public edge increment. This produces one fundamental-cycle syndrome.

The number of such coordinates is:

[
|E|-|V|+1.
]

For this abelian model, the atlas is globally integrable with no seams iff every syndrome is zero.

So H2-E1's apparent geometric paradox is immediately compressed to ordinary cycle-space obstruction data.

## 6. H-E02 — exact equivalent seam repair

When a candidate seam set does not balance the atlas, public potential propagation returns an inconsistent cycle.

Every valid balancing seam set must remove at least one edge of that cycle.

The exact solver therefore branches on the cycle edges:

~~~text
find unbalanced cycle C
        |
   +----+----+--- ...
   |         |
 delete e1  delete e2 ...
   |         |
 recurse    recurse
~~~

The solver:

- uses iterative deepening in seam count;
- memoizes canonical deleted-edge sets;
- returns the first minimum-size accepted equivalent witness;
- records nodes, backtracks, maximum branch size, and edge checks.

This is not claimed as a new algorithm.

## 7. Toy parameter ladder

| Set | Vertices | Extra edges | Seam budget | Modulus |
|---|---:|---:|---:|---:|
| escher-8 | 8 | 4 | 1 | 7 |
| escher-10 | 10 | 5 | 2 | 7 |
| escher-12 | 12 | 6 | 2 | 7 |
| escher-16 | 16 | 8 | 3 | 7 |
| escher-20 | 20 | 10 | 4 | 7 |

These are experiment sizes only.

## 8. Interpretation gate

H2-E1 should be rejected as a new hardness direction if measurements confirm that:

- cycle syndromes expose the complete obstruction;
- equivalent seam repairs are found cheaply;
- the relation is simply a known gain-graph balancing/cycle-hitting problem.

A successor H2-E2 must then change the mathematical level:

- local charts with overlaps containing multiple variables;
- higher-order overlap constraints;
- obstruction not representable as a one-dimensional edge gain field;
- mandatory cohomological and exact-CSP attacks before scaling.

## 9. Security status

No one-wayness, post-quantum, IND-CPA, IND-CCA, or concrete-security claim exists.
