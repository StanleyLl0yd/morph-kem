# 28 — K2.3 three-dimensional kernel-coherence calibration

## Status

K2.3 is an executable falsification experiment following K2.2.

It is not a KEM, one-way function, trapdoor primitive, or security candidate.

## Why the experiment moves to dimension three

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

K2.3 therefore uses a real 3-dimensional simplicial scaffold rather than pretending that a new independent 3-cell relation exists on the old 2-complex.

## Scaffold

The first calibration is the boundary of a 4-simplex, constructed directly as the five tetrahedra on five vertices.

The implementation checks:

~~~text
V/E/F/T = 5/10/10/5
Euler characteristic = 0
every triangular face lies in exactly two tetrahedra
~~~

These are executable combinatorial invariants, not hardness assumptions.

## Public face fibers

For every triangular face f, the public object contains a boundary value in `im(partial)`.

A deterministic public canonical lift is chosen as the smallest Q8 element in that boundary fiber. Because the kernel has order two, every valid lift has the form

~~~text
h_f = (-1)^z_f * h_f^0
z_f in GF(2).
~~~

The planted face values are reference data only.

## Tetrahedral coherence

Every tetrahedron imposes one parity equation on its four incident triangular faces.

Over GF(2), orientation signs disappear, so the complete residual relation is

~~~text
A z = b
~~~

where:
- one variable z_f is attached to each of the ten faces;
- one equation is attached to each of the five tetrahedra;
- A is the public tetrahedron/face incidence matrix;
- b is the public coherence syndrome.

Generation chooses a planted z and derives b. Verification accepts any face-lift vector whose kernel bits satisfy the public equations.

## Mandatory attack K-A06

The public attack performs deterministic Gaussian elimination over GF(2):

1. canonicalize every public Q8 boundary fiber;
2. encode the two lifts as one kernel bit;
3. build the five-by-ten public incidence matrix;
4. row-reduce the affine system;
5. set free variables to zero to choose one public representative;
6. lift the resulting bits back to Q8 face values;
7. verify the resulting higher-coherence witness exactly.

The attack reports rank, nullity, dependent equations, row-XOR count, and the exact number of equivalent witnesses.

## Expected disposition

The boundary of the 4-simplex has one visible row dependency because every triangular face belongs to two tetrahedra. The executable baseline is expected to obtain rank 4 and nullity 6, hence 64 equivalent solutions for any consistent generated syndrome.

If CI confirms this, K2.3 is rejected exactly: adding a 3-dimensional coherence equation over the residual central C2 kernel gives ordinary affine linear algebra, not a new cryptographic asymmetry.

A successor must not repair this by increasing the number of tetrahedra. It must first define a complete public-evaluation/trapdoor-recovery relation whose hard component is not an abelian cochain, ordinary cohomology, a linear-code syndrome, bounded-local CSP, or hidden gauge.

## Security status

No one-wayness, average-case hardness, post-quantum security, IND-CPA, IND-CCA, KEM, or production-security claim exists.
