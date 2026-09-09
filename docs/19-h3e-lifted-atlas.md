# 19 — H3-E0 lifted atlas: covering-space trapdoor feasibility

## Status

H3-E0 is an algebraic/executable calibration.

It is not a KEM and makes no security or post-quantum claim.

The question is narrower:

> Can the hidden sheet coordinates of a finite graph covering provide a trapdoor if an untrusted sender is given enough public information to evaluate path-lift-derived operations?

For the naive permutation-voltage model, the answer is **no**.

## 1. Prior art: graph coverings are established cryptographic material

Graph coverings are a classical part of topological graph theory and can be represented combinatorially through voltage/permutation-voltage assignments.

A direct cryptographic precedent now exists:

- Seiya Negami, *Composite coverings of graphs and cryptography*, Yokohama Mathematical Journal Vol. 70, 2024; repository publication 2025:
  https://ynu.repo.nii.ac.jp/records/2001753

Negami proposes a prototype **common-key cryptosystem** based on composite graph coverings.

This is not a public-key KEM and is not treated as evidence for MORPH security. It does establish that "use graph covers for cryptography" is not itself a novelty claim.

Negami and Sato also describe voltage/permutation-voltage constructions of arbitrary finite graph coverings:

- *Note on graph coverings with voltage assignments*:
  https://ynu.repo.nii.ac.jp/records/2000034

## 2. Covering representation

Let:

[
B=(V,E)
]

be a connected public base graph.

A k-sheet covering can be represented by a permutation on every oriented base edge:

[
ho_{uv}in S_k,
qquad
ho_{vu}=ho_{uv}^{-1}.
]

A lifted vertex is:

[
(v,s),
qquad
sin{0,ldots,k-1}.
]

Traversing base edge u -> v maps:

[
(u,s)mapsto(v,ho_{uv}(s)).
]

The public evaluator therefore needs enough transition information to perform these sheet updates.

## 3. Fiber gauge

A different naming of sheets above every base vertex gives an equivalent description of the same cover.

Let:

[
phi_vin S_k
]

be the secret relabeling of the fiber over vertex v.

Then canonical transition rho becomes public transition:

[
T_{uv}
=
phi_v
ho_{uv}
phi_u^{-1}.
]

This looks superficially like a hidden coordinate system.

But it is gauge, not a trapdoor.

## 4. Public spanning-tree normalization

Choose any public spanning tree T of B and root r.

Define public gauge h recursively.

Set:

[
h_r=I.
]

For a tree edge traversed parent p -> child c with public oriented transition T_pc, set:

[
h_c=h_p T_{pc}^{-1}.
]

Now transform every public edge by:

[
T'_{uv}
=
h_v T_{uv} h_u^{-1}.
]

For every tree edge:

[
T'_{uv}=I.
]

The attack uses only public transitions.

## 5. Exact collapse of the secret gauge

Assume the hidden canonical voltage representation was already tree-normalized:

[
ho_e=I
]

for all spanning-tree edges e.

Because:

[
T_{pc}=phi_cphi_p^{-1}
]

on tree edges, induction gives:

[
h_v=phi_rphi_v^{-1}.
]

For any edge u -> v:

[
egin{aligned}
T'_{uv}
&=
h_v T_{uv} h_u^{-1}\
&=
(phi_rphi_v^{-1})
(phi_vho_{uv}phi_u^{-1})
(phi_rphi_u^{-1})^{-1}\
&=
phi_rho_{uv}phi_r^{-1}.
end{aligned}
]

Therefore the attacker obtains the entire canonical cover up to one global conjugation:

[
ho_{uv}
sim
phi_rho_{uv}phi_r^{-1}.
]

That remaining ambiguity is one common relabeling of all sheets.

It is an equivalent cover.

## 6. Why equivalent-cover semantics matter

Suppose the secret contains all per-vertex fiber labels:

[
(phi_v)_{vin V}.
]

H-E05 removes all of them except one global root permutation.

If the cryptographic witness accepts any equivalent cover/coordinate system, the attack has already succeeded.

If the application instead insists that the exact original sheet names are secret, there is a different problem:

> an untrusted public sender does not know those exact secret sheet names either.

Encoding information into the arbitrary original gauge therefore conflicts with public evaluability.

## 7. Public-evaluation dilemma

The naive Lifted Atlas has two cases.

### Publish edge transitions

Then anyone can:

- lift paths;
- normalize the cover;
- recover all fundamental chord monodromies in a public gauge;
- reproduce path behavior.

The hidden fiber coordinates disappear.

### Hide edge transitions

Then an untrusted sender cannot evaluate path lifts or any forward operation that depends on them.

So the cover may remain secret, but it no longer gives the required public-key interface.

This is the H3-E0 public-evaluation dilemma.

## 8. Fundamental-cycle reduction

After spanning-tree normalization:

- every tree transition is identity;
- only non-tree/chord transitions remain.

Their count is the cycle rank:

[
|E|-|V|+1.
]

They encode the cover's fundamental monodromy in the chosen root gauge.

For abelian voltage groups this often linearizes further through first homology.

For general permutation voltages it remains group-valued, but it is still public once path lifting is public.

## 9. Graph-cover algorithmic warning

Worst-case graph-cover recognition cannot be used directly as a cryptographic assumption.

The literature contains both hard and tractable regimes.

For example:

- Kratochvil, Proskurowski, Telle, *Covering Regular Graphs*, JCTB 1997: H-Cover is NP-complete for infinite families of fixed regular target graphs.
- Fiala, Klavik, Kratochvil, Nedela, *Algorithmic Aspects of Regular Graph Covers*, 2016/2017: regular covering has FPT algorithms for planar inputs and polynomial-time cases under additional structural conditions.
- graph-cover complexity remains an active area, including 2025/2026 work on regular trees/multigraphs.

Consequences:

1. worst-case NP-hardness is not average-case one-wayness;
2. the generated distribution matters;
3. a trapdoor must do more than select a known easy cover instance;
4. public regularity/symmetry may make recovery easier, not harder.

## 10. Executable H3-E0 calibration

The repository implements:

- deterministic cycle-rich base graph;
- connected k-sheet canonical permutation-voltage cover;
- canonical tree voltages equal to identity;
- independent secret fiber gauges;
- public gauged transitions;
- public spanning-tree normalization;
- path-lift equivalence check;
- secret/reference comparison only for experiment evaluation.

The attacker function:

~~~text
canonicalize_public_cover(public)
~~~

uses no secret.

The reference evaluator verifies that the attack output is the canonical hidden cover up to one global conjugation.

## 11. Exit criterion

The following idea is rejected:

> the trapdoor is the hidden naming/coordinate system of fibers of a cover whose transition maps are public.

To proceed, H3-E1 would need a public evaluator derived from hidden topological data where:

- public evaluation is possible;
- public normalization does not recover an equivalent inversion structure;
- the secret is not merely gauge;
- the construction does not reduce to local-function/CSP, public group action, or hidden conjugacy already seen in M1/H1.

No such H3-E1 construction is currently defined.

## 12. Security status

No one-wayness, post-quantum, IND-CPA, IND-CCA, or concrete-security claim exists.
