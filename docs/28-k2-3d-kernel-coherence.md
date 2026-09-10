# 28 — K2.3 three-dimensional kernel-coherence calibration

## Status

**K2.3 is implemented and rejected exactly.**

It is not a KEM, one-way function, trapdoor primitive, or security candidate.

## Why the experiment moved to dimension three

K2.2 used the automorphism crossed module

~~~text
partial: Q8 -> Aut(Q8)
~~~

and found that every public face boundary had exactly two lifts. The residual ambiguity is the central kernel

~~~text
ker(partial) = {+1,-1} ~= C2.
~~~

Crossed modules model homotopy 2-types; their standard invariant package includes a Postnikov class in degree three. The project-level source review is recorded in `docs/25-k2-crossed-module-frontier.md`, including the classical H^3 reference:

https://archive.intlpress.com/site/pub/files/_fulltext/journals/hha/1999/0001/0001/HHA-1999-0001-0001-a001.pdf

K2.3 therefore uses a genuine 3-dimensional simplicial scaffold rather than inventing an independent 3-cell equation on the old 2-complex.

## Scaffold

The calibration scaffold is the boundary of a 4-simplex, constructed directly as the five tetrahedra on five vertices.

Executable invariants:

~~~text
V/E/F/T = 5/10/10/5
Euler characteristic = 0
every triangular face lies in exactly two tetrahedra
~~~

These are combinatorial facts, not hardness assumptions.

## Public face fibers

For every triangular face f, the public object contains a boundary value in `im(partial)`.

A deterministic public canonical lift `h_f^0` is chosen as the smallest Q8 element in that boundary fiber. Because the kernel has order two, every valid lift is uniquely

~~~text
h_f = (-1)^z_f * h_f^0
z_f in GF(2).
~~~

The planted face values are reference data only.

## Tetrahedral coherence

Every tetrahedron imposes one parity equation on its four incident triangular faces. Over GF(2), orientation signs disappear, so the complete residual relation is

~~~text
A z = b
~~~

where one variable is attached to each of the ten faces and one public equation to each of the five tetrahedra.

## K-A06 — exact public attack

The attack:

1. canonicalizes every public Q8 boundary fiber;
2. encodes the two lifts as one kernel bit;
3. builds the public tetrahedron/face incidence matrix;
4. performs deterministic Gaussian elimination over GF(2);
5. sets free variables to zero to obtain one public representative;
6. lifts those bits back to Q8 face values;
7. verifies the resulting higher-coherence witness exactly.

## Exact reduction theorem for this model family

For any instance of the implemented K2.3 relation, after selecting one public lift in each two-element boundary fiber, the difference between any two valid face lifts is an element of the central kernel `C2`. The implemented tetrahedral coherence predicates depend only on products of those kernel elements. Therefore witness recovery is exactly an affine binary linear system.

This is stronger than an empirical small-instance observation: increasing the number of faces or tetrahedra while keeping this relation only increases the size of a publicly solvable linear system.

It is **not** an impossibility theorem for arbitrary higher-topological cryptography.

## Measured CI result

Fixed seed `2309425a6bc7d8e90123456789abcdef`, Python 3.12 CI:

~~~text
cells V/E/F/T:                    5/10/10/5
face tetrahedron degree set:       [2]
Euler characteristic:              0
public Q8 boundary fiber sizes:    (2,2,2,2,2,2,2,2,2,2)
reference accepted:                true
GF(2) equations/variables:         5/10
GF(2) rank/nullity:                4/6
dependent equations:               1
row XOR operations:                7
equivalent witnesses:              64
public attack accepted:            true
attack equals planted representative: false
elapsed seconds:                   0.000111
~~~

The rank is four because the XOR of all five tetrahedral rows is zero: every triangular face is incident to two tetrahedra. Nullity six therefore gives exactly `2^6 = 64` solutions for the generated consistent syndrome.

## Disposition

**K2.3 rejected.**

The successor must not be “more tetrahedra” or “a larger abelian kernel.” The next admissible direction must first expose a complete public-evaluation/trapdoor-recovery interface and must survive reduction to:

- abelian cochains and twisted cohomology;
- finite-module / linear-code syndrome solving;
- gauge normalization;
- ordinary finite-group synchronization;
- bounded-local CSP/SAT/CP-SAT;
- canonicalization/isomorphism.

The only higher-topological direction still worth testing is one in which an unknown `pi1`-level object is genuinely coupled to the `pi2` module/Postnikov layer and a secret changes recovery complexity on a generated positive distribution. That is a research gate, not a hardness claim.

## Security status

No one-wayness, average-case hardness, post-quantum security, IND-CPA, IND-CCA, KEM, or production-security claim exists.
