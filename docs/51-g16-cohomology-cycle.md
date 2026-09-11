# 51 — G16 nonlocal cohomology-paired cycle negative control

## Status

**G16 is an attack calibration in progress.** It is the first post-G15 control that changes the witness predicate itself from bounded-radius local pieces to a globally defined simple cycle with nontrivial cohomological pairing.

G16 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G15 gives a clean carrier/witness separation: long bistellar mixing can substantially disrupt the previous complete reverse-stacking inverse, yet the local P3 witness relation remains a tiny public exact-cover/SAT problem. G16 therefore stops redesigning the carrier and asks whether a genuinely nonlocal topological predicate helps.

The carrier reuses an irregular edge-flipped torus. The public instance also contains a nontrivial GF(2) 1-cocycle `alpha` on primal edges. A witness is any simple primal edge cycle `z` satisfying

```text
<alpha,z> = 1 mod 2.
```

This verifier is global: simple-cycle connectivity is not a fixed-radius candidate predicate and the pairing is a global cohomological invariant.

## Carrier

Use the same sizes and flip counts as the G12 irregular-torus family, but **without P3-cover conditioning**:

```text
g16-6x6: 36 vertices, 108 edges, 72 triangles, 36 flips
g16-6x9: 54 vertices, 162 edges, 108 triangles, 54 flips
g16-8x9: 72 vertices, 216 edges, 144 triangles, 72 flips
```

Every final carrier is a closed torus with `chi = 0`; legal flips preserve the simplicial surface and an independent global relabel removes construction labels.

## Public cocycle

Index public primal edges. The implementation builds the triangle-edge coboundary equations over GF(2), computes the cocycle nullspace, computes the vertex-coboundary rowspace, and chooses a deterministic cocycle basis vector not contained in the coboundary space.

For a connected triangulated torus with `V/E/F` as above, the expected dimensions are

```text
rank(partial_1) = V - 1
cycle dimension = E - V + 1
rank(delta_1) = F - 1
cocycle dimension = E - F + 1 = V + 1
coboundary rank = V - 1
dim H^1 = 2
```

These identities are measured in CI rather than assumed as security evidence.

The public key-like experiment data explicitly contains `alpha`. A hidden seeded spanning-tree ordering is used only to retain one accepted reference cycle for post-attack comparison.

## Public verifier

A witness is a canonical set of public primal edges. The verifier requires:

1. at least three distinct public edges;
2. every touched witness vertex has degree exactly two;
3. the selected subgraph is connected, hence one simple cycle;
4. the public cocycle pairing is odd.

The verifier never asks for the hidden reference cycle. Any accepted simple cycle is attacker success.

## A-043 — public fundamental-cycle basis recovery

The initial design proposed a generic affine GF(2) solve. Attack-first analysis yields a cheaper structural attack.

Choose any public spanning tree `T` of the connected primal graph. Every non-tree edge `e` defines a simple fundamental cycle

```text
C_e = e + path_T(e).
```

The `E-V+1` fundamental cycles form a basis of the public cycle space. If `alpha` paired evenly with every `C_e`, it would vanish on the whole cycle space and therefore belong to the graph cut/coboundary space, contradicting the declared nontrivial cohomology class. Consequently at least one fundamental simple cycle is guaranteed to have odd pairing.

The primary public attack therefore:

1. builds a deterministic BFS spanning tree from public labels;
2. scans public non-tree edges in canonical order;
3. constructs each fundamental simple cycle;
4. evaluates public `alpha`;
5. submits the first odd cycle to the exact verifier.

Record tree/non-tree edges, cycles tested, total tree-path edge scans and selected cycle length.

## Independent affine cross-check

A second path independently builds the vertex-edge cycle equations

```text
partial_1 z = 0
<alpha,z> = 1
```

and solves them by Gauss-Jordan elimination. The resulting support is Eulerian but may contain multiple cycles. Rather than weakening the verifier, the attack builds a spanning forest of that support, scans its fundamental-cycle basis, extracts one odd simple constituent, and submits it to the same exact verifier.

Record affine rank/nullity, row-XOR work, support size, support cycles tested and extracted cycle length.

## Rejection gate

If the public fundamental-cycle scan routinely returns an accepted odd cycle, **reject G16 by A-043**. The affine path is then only an independent semantic and algebraic cross-check.

This would demonstrate that making the verifier genuinely global and cohomological is still insufficient when the accepted relation is linear on the public cycle space. Do not repair by increasing torus size or flip count.

## G17 gate

If G16 fails, G17 must require more than affine membership in homology/cohomology. The next controlled relation may couple multiple global cycles through nonlinear geometric constraints such as disjointness or intersection, but it must immediately face public symplectic homology bases, flow/matching reductions, ILP/SAT/CP-SAT, low-width methods, normalization and equivalent-witness enumeration.

No trapdoor/KEM work begins before those gates survive.

No security claim.
