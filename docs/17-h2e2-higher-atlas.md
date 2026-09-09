# 17 — H2-E2 higher-order Escher atlas

## Status

H2-E2 is an executable attack-first experiment.

It is not a KEM, trapdoor primitive, or security candidate.

H2-E1 represented local geometry by one relative scalar per edge and collapsed to gain-graph cycle balance. H2-E2 deliberately moves to **higher-order local charts**.

## 1. Public atlas

There are Boolean global variables:

[
x_0,ldots,x_{n-1}.
]

Each chart touches three distinct variables and contains three public negation bits.

For chart:

[
C=((i,j,k),(a,b,c)),
]

define effective local values:

[
x_ioplus a,quad x_joplus b,quad x_koplus c.
]

The chart accepts iff these three values are **not all equal**.

Thus each chart is a signed NAE-3 relation.

## 2. Why this is closer to the Escher idea

A chart is one locally coherent "view."

The paradox is not encoded as one number around an edge loop.

Instead many 3-variable local views overlap.

H2-E2 explicitly requires:

- each chart has local solutions;
- every pair of charts has at least one joint solution on their union;
- the complete public atlas has no global solution before seams are allowed.

So local compatibility extends beyond single adjacencies.

## 3. Pairwise compatibility is intentionally weak

For NAE-3, one clause rejects only 2 of the 8 assignments on its three variables.

For any two clauses, over the union of their variables, each excludes at most one quarter of assignments. By a union bound, at least half of assignments remain candidates for satisfying both.

The implementation still audits every chart pair explicitly.

This illustrates an important lesson:

> pairwise local consistency can be almost automatic even when global consistency is computationally nontrivial.

## 4. Generator

Deterministically from a master seed:

1. choose a hidden Boolean assignment;
2. choose unique variable triples;
3. generate ordinary signed NAE charts conditioned to accept the hidden assignment;
4. regenerate until the normal atlas has only the hidden assignment up to global complement symmetry;
5. generate planted seam charts conditioned to reject the hidden assignment;
6. sort all charts canonically and discard role information from the public object;
7. require the full atlas to have no zero-seam global section.

Reference data stores:

- hidden assignment;
- planted seam-chart indices.

It is evidence for generation only.

## 5. Equivalent witness

A witness is:

[
(S,x),
]

where:

- (S) is a sorted set of chart indices;
- (|S|le k), for public seam budget (k);
- (x) is a full Boolean assignment.

The verifier accepts iff every chart outside (S) accepts (x).

Any equivalent repair is attacker success.

## 6. Prior-art classification

This relation is a Boolean constraint satisfaction / Max-CSP problem.

NAE-3SAT is a standard NP-complete satisfiability family. Schaefer's Boolean CSP dichotomy is foundational prior art:

- Thomas J. Schaefer, *The complexity of satisfiability problems*, STOC 1978:
  https://doi.org/10.1145/800133.804350

Restricted NAE-3SAT variants remain NP-complete; for example:

- Darmann and Döcker, *On simplified NP-complete variants of Not-All-Equal 3-Sat and 3-Sat*:
  https://arxiv.org/abs/1908.04198

The local-to-global CSP/sheaf connection is also prior art:

- Abramsky and Brandenburger:
  https://arxiv.org/abs/1102.0264
- Ó Conghaile, *Cohomology in Constraint Satisfaction and Structure Isomorphism*:
  https://arxiv.org/abs/2206.15253

Therefore H2-E2 is not presented as a new hard problem merely because NAE-CSP can be difficult in the worst case.

## 7. H-E03 exact repair attack

The attacker minimizes the number of violated charts.

For a complete assignment (x), define:

[
S(x)={C_i : C_i(x)=	ext{false}}.
]

Then (x) gives an accepted repair exactly when:

[
|S(x)|le k.
]

The exact solver uses branch-and-bound.

### Symmetry

NAE satisfaction is invariant under complementing every global variable, so:

[
xmapsto xoplus 1
]

is a global symmetry.

The solver fixes (x_0=0).

### Lower bound

For a partial assignment the attack counts:

- charts already fully assigned and violated;
- for each unassigned variable, conflicting one-variable requirements induced by charts whose other two effective literals are equal.

If one variable is simultaneously required to be 0 by (r_0) charts and 1 by (r_1) charts, at least:

[
min(r_0,r_1)
]

of those charts must become seams.

These contributions give a pruning lower bound.

### Variable order

Variables are ordered primarily by chart incidence.

Branch values are tried in projected lower-bound order.

## 8. Planted-role diagnostic

H2-E2 also measures a deliberately cheap public chart signature:

- number of negated literals;
- sorted incidence degrees of the three variables.

For every planted seam chart it asks whether the same signature also occurs among normal charts.

This is only a baseline distinguisher. A unique signature is bad evidence; signature overlap is not evidence of secrecy.

## 9. Toy ladder

| Set | Variables | Charts | Planted budget |
|---|---:|---:|---:|
| atlas-8 | 8 | 18 | 1 |
| atlas-10 | 10 | 24 | 1 |
| atlas-12 | 12 | 30 | 2 |
| atlas-14 | 14 | 36 | 2 |
| atlas-16 | 16 | 42 | 3 |

These are experiment sizes, not security parameters.

## 10. Exit criteria

Reject H2-E2 if fixed-seed evidence shows:

- exact equivalent repair remains tiny across this ladder;
- minimum repair is often smaller than the planted budget;
- simple public signatures identify planted charts;
- the construction provides no useful asymmetry beyond a standard planted/deletion CSP.

Even if toy exact solving becomes expensive, worst-case NP-completeness is not evidence of cryptographic average-case hardness.

## 11. Security status

No one-wayness, post-quantum, IND-CPA, IND-CCA, or concrete-security claim exists.


## 12. Measured H2-E2 result

Fixed seed on the Python 3.12 CI runner.

### atlas-12 baseline

~~~text
variables/charts/budget: 12/30/2
pairwise chart compatibility: 435/435
reference witness valid: yes

exact attack:
  found: yes
  witness valid: yes
  minimum seams: 1
  nodes: 37
  backtracks: 18
  best updates: 1
  proven minimum: yes
  node cap exhausted: no

simple planted-role signature:
  seam signatures also seen among normal charts: 0/2
  unique seam signatures: 2
~~~

So every pair of local charts is compatible, yet one public chart deletion suffices to produce a global section.

That is a mathematically valid local/global paradox, but it does not give the desired asymmetry.

### Scaling sweep

| Set | Variables | Charts | Planted budget | All pairs compatible | Minimum seams | Nodes | Backtracks | Seam signatures seen among normal |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| atlas-8 | 8 | 18 | 1 | yes | 1 | 43 | 21 | 1/1 |
| atlas-10 | 10 | 24 | 1 | yes | 1 | 41 | 20 | 0/1 |
| atlas-12 | 12 | 30 | 2 | yes | 1 | 37 | 18 | 0/2 |
| atlas-14 | 14 | 36 | 2 | yes | 1 | 73 | 36 | 0/2 |
| atlas-16 | 16 | 42 | 3 | yes | 1 | 281 | 138 | 1/3 |

The attack proves the minimum in every tested set.

## 13. Why H2-E2 fails

### Failure A: equivalent repair is easier than planted repair

The generator plants up to three seam charts, but every tested public instance admits a one-chart repair.

This is not an implementation bug: equivalent-witness semantics intentionally count that as attacker success.

### Failure B: planted distribution leaks public role signatures

The baseline signature uses only:

- number of negated literals in a chart;
- incidence degrees of its three public variables.

Despite being extremely weak, it uniquely identifies every planted seam signature in atlas-10, atlas-12 and atlas-14.

Thus the planted and normal chart distributions are not sufficiently role-indistinguishable.

### Failure C: the relation is a standard deletion-CSP

Even if the two empirical failures above were repaired, signed NAE-3 constraints plus "delete a few violated charts" remain a standard Max/deletion-CSP family.

Worst-case NP-completeness cannot serve as evidence that this planted average-case distribution is cryptographically hard.

## 14. H2-E2 disposition

**H2-E2 is rejected.**

Do not repair it by:

- increasing variable count;
- adding more NAE charts;
- increasing seam budget;
- replacing the exact solver with a slower implementation.

Those changes do not address the structural problem.

## 15. H2-E3 gate

A third Escher experiment, if pursued, should remove "small deletion set" from the witness semantics entirely.

A more interesting target would be:

- all public charts remain present;
- each chart has multiple local coordinate systems;
- overlaps require selecting compatible transition maps;
- every radius-r neighborhood has an extension for a chosen r;
- the global witness is a coherent choice of chart states/transitions, not a set of discarded constraints;
- generation does not mark a small exceptional subset;
- exact k-consistency, cohomological relaxation, treewidth, and CSP attacks are mandatory.

This would test the stronger Escher idea: **the same visible pieces must all remain, but choosing locally plausible interpretations everywhere becomes globally difficult.**
