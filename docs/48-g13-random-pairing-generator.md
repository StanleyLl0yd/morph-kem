# 48 — G13 random cubic-dual surface generator conditioning audit

## Status

**G13 is rejected at the carrier-generator gate by A-040.** Across every measured raw configuration-pairing attempt, the proposed distribution produced zero honest simplicial closed surfaces.

No P3 exact-cover experiment is run on a generator whose valid output would require extreme hidden rejection conditioning.

G13 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G12 showed that heavily irregularizing a periodic torus by legal edge flips does not make the public P3 hypercover hard. The obvious next idea was to abandon torus ancestry entirely and generate a closed surface from a random cubic triangle-dual graph.

That idea has a generator problem of its own. A generic random pairing of abstract triangle sides defines a random orientable map, not automatically an honest finite simplicial complex. Corner identifications can collapse vertices inside a triangle before later surface checks are even reached.

G13 therefore audits this conditioning **before** adding a witness relation. Silently rejection-sampling until a rare simplicial quotient appears is not accepted as neutral setup.

## Raw distribution

For `F` abstract triangles:

1. create three labelled oriented side stubs per triangle;
2. deterministically shuffle the `3F` stubs;
3. pair consecutive stubs;
4. reject loops, parallel dual edges or disconnected dual graphs;
5. glue every paired side in orientation-reversing order;
6. quotient all abstract triangle corners by the side identifications;
7. validate the quotient as an honest closed simplicial surface.

The quotient gate requires every triangle to have three distinct quotient vertices, distinct quotient facets, exact two-face edge incidence, connected cyclic vertex links, and a nonnegative integral orientable genus.

Toy sets are `g13-36`, `g13-54`, and `g13-72`.

## A-040 — configuration-pairing generator-conditioning audit

### Fixed Python 3.12 audit

4096 deterministic attempts per size:

| Set | Attempts | Dual loops | Dual parallel | Degenerate quotient triangle | Success | Rule-of-three upper scale |
|---|---:|---:|---:|---:|---:|---:|
| g13-36 | 4096 | 2027 | 1493 | 576 | **0** | 0.000732422 |
| g13-54 | 4096 | 2077 | 1459 | 560 | **0** | 0.000732422 |
| g13-72 | 4096 | 2119 | 1439 | 538 | **0** | 0.000732422 |

No attempt reached duplicate-triangle, bad-edge-incidence, bad-vertex-link, or genus rejection: every pairing that survived the simple-cubic dual checks already collapsed at least one abstract triangle to fewer than three quotient vertices.

### Multi-seed audit

Python 3.12 additionally tested eight independently derived seeds with 1024 attempts each for every size. All **24/24 audit batches** again observed zero successes. Per batch, the only terminal classes were dual loop, dual parallel edge, and degenerate quotient triangle.

Combining the fixed and multi-seed attempt budgets **within each size** gives 12,288 measured raw attempts per distribution:

| Set | Total attempts | Dual loops | Dual parallel | Degenerate triangle | Success | `3/N` scale |
|---|---:|---:|---:|---:|---:|---:|
| g13-36 | 12288 | 6170 | 4477 | 1641 | **0** | 0.000244141 |
| g13-54 | 12288 | 6234 | 4395 | 1659 | **0** | 0.000244141 |
| g13-72 | 12288 | 6308 | 4387 | 1593 | **0** | 0.000244141 |

The elementary `3/N` value is reported only as a scale for an unobserved raw success probability, not as a cryptographic theorem or rigorous asymptotic statement.

## Interpretation

**G13 fails before cryptanalysis of any witness relation begins.** The naive configuration-model idea is not a usable public-key carrier distribution under the repository's standards.

Roughly half of raw pairings already contain a cubic-dual loop; a large additional fraction contains a parallel dual edge; and every measured simple surviving pairing collapses triangle corners enough to make at least one quotient triangle degenerate.

It would be methodologically invalid to hide this behind an unbounded rejection loop and then study only the rare conditioned outputs as though they were generic random cubic surfaces.

No P3/Exact-Cover continuation is executed because the generator rejection gate has already fired.

## Result

**G13 random cubic-dual configuration pairing is rejected by A-040 at generation time.** This is a generated-distribution failure, not a theorem that random maps or random triangulations cannot be sampled efficiently by better constructive methods.

## G14 gate

G14 must use a constructive non-toroidal random simplicial-surface family whose validity is guaranteed by construction rather than rare conditioning. The next controlled baseline is a random stacked/Apollonian sphere: start from the tetrahedron boundary and repeatedly subdivide a randomly selected triangular face by a fresh vertex.

That family must immediately face its obvious public inverse—degree-three vertex / stellar-center contraction—plus canonicalization, P3 candidate extraction, exact cover, SAT, equivalent-witness multiplicity and generated-role leakage. If the stacked history is publicly reversible, reject before scaling.

No security claim.
