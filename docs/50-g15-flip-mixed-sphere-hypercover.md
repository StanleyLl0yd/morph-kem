# 50 — G15 flip-mixed icosahedral sphere hypercover negative control

## Status

**G15 is an attack calibration in progress.** It tests a constructive non-toroidal sphere carrier after a long bistellar/edge-flip mixing walk, with both the G14 local-inverse regression and the public P3 exact-cover/SAT attack enabled.

G15 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G14 fixed G13's unhealthy generator by using stacked spheres, but the construction was completely reversible through public degree-three stellar-center contraction. G15 deliberately separates two questions:

1. can a long legal flip walk destroy that bounded-local reverse-stacking ancestry?;
2. if so, does the witness relation nevertheless remain an ordinary easy public P3 hypergraph exact-cover problem?

This distinction matters. Defeating A-041 is not positive hardness evidence if A-042 still constructs equivalent accepted witnesses cheaply.

## Carrier

The seed surface is a fixed combinatorial icosahedron boundary:

```text
V/E/F = 12/30/20
all primal vertex degrees = 5
chi = 2
```

To reach the target size, G15 performs seeded `1 -> 3` face subdivisions, then a long public-semantics-preserving `2 <-> 2` flip walk. Unlike G12's torus descendant, the starting carrier is a sphere with no stacked or toroidal ancestry.

Toy sets:

```text
g15-36:  8 growth steps,  720 successful flips
g15-54: 17 growth steps, 1080 successful flips
g15-72: 26 growth steps, 1440 successful flips
```

Each mixing proposal chooses an actual current public edge uniformly from a deterministic seeded stream. Illegal proposed flips are counted explicitly. Generation records both successful flips and rejected proposals.

After mixing, an independent global relabel is applied.

## Bounded P3-cover conditioning

A P3 witness relation requires at least one exact cover. The final mixed carrier is therefore tested for a public P3 exact cover after mixing. If absent, only the mixing/relabel attempt is retried, under a fixed bounded attempt cap. `generation_retries` is part of the measured output.

This conditioning is never hidden or interpreted as security evidence.

## Public relation

A witness partitions every public triangle into groups of three. Every group must be an exact three-triangle P3 disk under the same simplicial predicate used by G11/G12.

The verifier never asks for the icosahedral coordinates, growth history, flip history, or reference cover. Any accepted equivalent cover is attacker success.

## A-042 — mixed-sphere normalization + exact-cover / SAT recovery

### G14 regression

Run the exact public A-041 reverse-stacking attack on the final mixed carrier. Record initial degree-three vertices, legal reverse candidates, reverse move count, terminal complex, and whether the tetrahedron boundary is reached.

G15 only establishes a meaningful carrier change if A-041 no longer completely peels the sphere.

### Normalization probe

Enumerate all legal public `2 <-> 2` flips and count those that strictly reduce the squared deviation of primal vertex degrees from six. This is a cheap public normalization direction probe, not a security metric.

### Exact-cover path

1. derive public edge/triangle incidence;
2. enumerate every exact P3 disk candidate;
3. construct candidate/triangle incidence and overlap metrics;
4. run deterministic MRV Algorithm-X-style exact cover;
5. enumerate accepted covers up to an explicit cap;
6. submit every recovered cover to the exact verifier;
7. compare with reference evidence only after public acceptance.

### Independent SAT path

Use one Boolean variable per public P3 candidate. For every triangle encode exactly one incident candidate with one at-least-one clause plus pairwise at-most-one clauses. Run MiniSat on the fixed Python 3.12 baseline, decode the model, and check it again with the repository verifier.

## Rejection gate

Reject G15 if either:

- public normalization exposes a cheap canonical carrier reduction; or
- exact cover / MiniSat routinely recovers any accepted P3 witness.

If A-041 is defeated but A-042 exact cover remains cheap, that is a particularly important negative result: it shows that changing carriers further is unlikely to help while witness validity remains a fixed-radius P3 motif.

Do not repair by increasing only the number of mixing flips or sphere size.

## Measurements

Record at least:

- growth steps, successful mixing flips, rejected proposals and generation retries;
- public `V/E/F`, Euler characteristic and edge incidence range;
- primal degree histogram;
- initial degree-three/reverse candidate counts;
- A-041 reverse moves and terminal complex;
- normalization-improving legal flips;
- dual graph edges/degree histogram, bridges, articulations, bipartiteness and short cycles;
- local signature classes;
- P3 candidate count, membership and overlap histograms, candidate incidence;
- exact-cover nodes/decisions/backtracks, solution cap and cap-hit;
- accepted/non-reference covers;
- SAT variables/clauses, MiniSat conflicts/decisions/propagations and decoded verifier outcome;
- deterministic all-size/eight-seed sweep.

## G16 gate

If G15 confirms that flip mixing defeats the local carrier inverse but P3 exact cover remains fatal, G16 must change the **witness predicate**, not the carrier. Candidate validity should depend on genuinely nonlocal topological information rather than a bounded-radius dual motif, and must immediately face quotient/canonicalization, generic CSP/SAT/CP-SAT, separator/treewidth, normalization, equivalent-witness and generated-distribution attacks.

No trapdoor/KEM work begins before those gates survive.

No security claim.
