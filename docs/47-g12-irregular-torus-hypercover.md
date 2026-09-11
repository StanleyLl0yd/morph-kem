# 47 — G12 irregular-torus P3 hypercover negative control

## Status

**G12 is an attack calibration in progress. No hardness or security conclusion is permitted until exact-head CI records A-039.**

G12 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G11 removed the ordinary graph-matching reduction by moving to three-triangle P3 pieces, but its carrier remained a perfectly periodic torus. Public candidate roles were completely uniform and generic exact cover / MiniSat recovered many accepted equivalent covers.

G12 tests the most immediate alternative explanation: perhaps A-038 is easy only because of periodic translation symmetry. The carrier is therefore irregularized by many public-semantics-preserving legal `2 <-> 2` edge flips before the P3 candidate relation is formed.

The attack-first question is whether irregularization changes recovery at all, or simply makes the same public hypergraph less pretty while generic exact cover remains cheap.

## Construction

Start from the exact periodic torus triangulation already used by M4/G10/G11. A legal flip replaces

```text
(a,b,c), (a,b,d)
```

across edge `{a,b}` by

```text
(a,c,d), (b,c,d)
```

when the opposite edge `{c,d}` is absent and the replacement creates no duplicate or degenerate triangle.

A deterministic seeded walk performs exactly the configured number of successful flips. The result is then independently globally relabelled.

Toy sets:

```text
g12-6x6: 72 triangles, 36 successful flips
g12-6x9: 108 triangles, 54 successful flips
g12-8x9: 144 triangles, 72 successful flips
```

The final public object contains only the irregular simplicial complex and verifier semantics. Periodic coordinates, the flip history, and the eventual reference cover are not public witness data.

## Satisfiability conditioning

G12 deliberately does **not** preserve a pre-existing G11 cover while flipping. After irregularization, the generator publicly enumerates the valid final P3 candidate family and uses a secret ordering only to choose one exact cover as post-attack reference evidence.

If the final irregular carrier has no P3 exact cover, generation retries only the deterministic flip seed, up to an explicit bounded attempt cap. The number of failed attempts is recorded as `generation_retries` because conditioning itself is part of the generated-distribution attack surface.

The generator also requires that irregularization be visible in public diagnostics: the primal vertex-degree histogram and the combined primal/dual local-signature partition must both contain more than one class.

## Public relation

Exactly as in G11, a witness partitions every public triangle into groups of three. Every group must form the exact three-triangle P3 disk predicate.

The verifier never asks for the reference cover, flip history, original coordinates, or local roles. Any accepted equivalent cover is attacker success.

## Structural diagnostics

G12 records:

- public `V/E/F` and Euler characteristic;
- closed edge incidence range;
- exact successful flip count and generation retry count;
- primal vertex-degree histogram;
- final triangle-dual edge/degree data, bridges and articulations;
- whether the final dual remains bipartite;
- public dual triangle/four-cycle counts;
- number and class-size histogram of local signatures combining primal vertex degrees with radius-one/radius-two dual structure;
- number of legal public flips that strictly reduce squared deviation of primal vertex degrees from six;
- P3 candidate count, memberships, overlap-degree histogram and candidate/triangle incidence size.

These measurements test that the carrier is genuinely less regular and expose possible normalization directions. They are not security evidence.

## A-039 — irregular-carrier candidate extraction + exact cover / SAT

### Exact-cover path

1. derive public edge/triangle incidence from the final irregular complex;
2. build the public triangle-dual graph;
3. enumerate every induced dual P3;
4. filter each candidate through the exact simplicial disk predicate;
5. build candidate/triangle incidence and candidate overlap;
6. run deterministic MRV Algorithm-X-style exact cover;
7. enumerate covers up to an explicit cap;
8. submit every cover to the exact G12 verifier;
9. compare to the reference only after public acceptance.

### Independent SAT path

Use one Boolean variable per public P3 candidate. For every public triangle encode exactly one incident candidate with one at-least-one clause and pairwise at-most-one clauses. Run MiniSat on the fixed Python 3.12 baseline, decode the selected candidates, and submit them again to the exact repository verifier.

If custom exact cover already succeeds cheaply, MiniSat is an independent semantic cross-check rather than the reason for rejection.

## Normalization probe

A complete inverse-flip canonicalizer is intentionally not required for rejection. The implementation records short-cycle/signature structure and counts legal flips that move the public primal degree profile toward the regular degree-six torus. If A-039 already recovers an accepted cover, a heavier normalization attack adds no security-relevant conclusion.

## Rejection gate

If A-039 routinely recovers any accepted witness cheaply, **reject G12**. Do not increase flip counts, torus dimensions, or generation retries as a repair while the same candidate-extraction and exact-cover/SAT relation remains effective.

If satisfiable-instance conditioning requires many retries or correlates with simpler public signatures, record that as an additional generated-distribution failure.

## G13 gate

A successor must abandon the easy periodic-torus-plus-local-flips family rather than stacking more cosmetic irregularization. It must immediately face canonicalization/isomorphism, separator/treewidth analysis, candidate extraction, exact cover/set packing, SAT/CP-SAT, simplification/normalization, equivalent-witness multiplicity and generated-role leakage.

Only after both carrier recovery and the resulting candidate hypergraph survive these public attacks could the project consider any trapdoor interface.

No security claim.
