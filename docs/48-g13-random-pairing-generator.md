# 48 — G13 random cubic-dual surface generator conditioning audit

## Status

**G13 first tests its carrier generator before any P3 hardness experiment.** No P3 exact-cover result is interpreted unless the raw configuration-pairing distribution produces honest simplicial closed surfaces at a healthy measured rate.

G13 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G12 showed that heavily irregularizing a periodic torus by legal edge flips does not make the public P3 hypercover hard. The obvious next idea is to abandon torus ancestry entirely and generate a closed surface from a random cubic triangle-dual graph.

That idea has a generator problem of its own. A generic random pairing of abstract triangle sides defines a random orientable map, not automatically an honest finite simplicial complex. Corner identifications can collapse vertices inside a triangle, duplicate quotient triangles, identify multiple abstract edges into one quotient edge, or create singular vertex links.

G13 therefore audits this conditioning **before** adding a witness relation. Silently rejection-sampling until a rare simplicial quotient appears would itself define a strongly conditioned public-key distribution and is not accepted as neutral setup.

## Raw distribution

For `F` abstract triangles:

1. create three labelled oriented side stubs per triangle;
2. deterministically shuffle the `3F` stubs;
3. pair consecutive stubs;
4. reject loops, parallel dual edges or disconnected dual graphs;
5. glue every paired side in orientation-reversing order;
6. quotient all abstract triangle corners by the side identifications;
7. validate the quotient as an honest closed simplicial surface.

The final quotient gate requires:

- every triangle has three distinct quotient vertices;
- all quotient triangles are distinct;
- exactly `3F/2` quotient edges exist and every edge belongs to exactly two triangles;
- every quotient vertex link is one connected degree-two cycle;
- Euler characteristic corresponds to a nonnegative integral orientable genus.

Every attempt stops at its first failure class. No failed sample is silently retried inside one attempt.

Toy sets:

```text
g13-36: F = 36
g13-54: F = 54
g13-72: F = 72
```

## A-040 — configuration-pairing generator-conditioning audit

The dedicated Python 3.12 audit runs 4096 deterministic attempts for each toy size. A second sweep uses eight independently derived seeds with 1024 attempts per seed and size.

Measured counters are:

```text
dual_loop
dual_parallel
dual_disconnected
degenerate_triangle
duplicate_triangle
bad_edge_incidence
bad_vertex_link
bad_genus
success
```

When an audit observes zero successes, it also records the elementary rule-of-three upper confidence proxy `3/N`. This is not a formal cryptographic bound; it makes the scale of an unobserved success probability explicit.

## Rejection gate

If no or only a vanishing fraction of raw attempts produce honest simplicial closed surfaces, the proposed G13 configuration-model carrier is rejected **at generation time**. The experiment must not proceed by hiding an unbounded rejection sampler.

If a healthy success rate is observed instead, G13 proceeds to the conditional P3 relation described in issue #86: public P3 candidate extraction, exact cover, and independent MiniSat.

## Successor gate

If the raw generator is rejected, G14 should switch to a constructive non-toroidal random simplicial-surface family whose validity is guaranteed by construction rather than rare conditioning. A natural negative control is a random stacked/Apollonian sphere, followed immediately by degree-three/canonical simplification attacks and the same P3 exact-cover/SAT recovery.

No security claim.
