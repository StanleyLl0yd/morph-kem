# 50 — G15 flip-mixed icosahedral sphere hypercover negative control

## Status

**G15 is rejected by A-042.** Long flip mixing changes the carrier enough that the fixed baselines and the official 24-instance sweep no longer completely reverse-stack to the tetrahedron boundary, but the unchanged P3 witness relation remains trivial for public exact cover and independent MiniSat.

G15 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G14 fixed G13's unhealthy generator by using stacked spheres, but the construction was completely reversible through public degree-three stellar-center contraction. G15 deliberately separates two questions:

1. can a long legal flip walk destroy that bounded-local reverse-stacking ancestry?;
2. if so, does the witness relation nevertheless remain an ordinary easy public P3 hypergraph exact-cover problem?

The measured answer is yes to both. This is stronger evidence against further carrier-only redesign while retaining a fixed-radius P3 witness predicate.

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

Each mixing proposal chooses an actual current public edge uniformly from a deterministic seeded stream. Illegal proposed flips are counted explicitly. Generation records both successful flips and rejected proposals. After mixing, an independent global relabel is applied.

## Bounded P3-cover conditioning

A P3 witness relation requires at least one exact cover. The final mixed carrier is tested for a public P3 exact cover after mixing. If absent, only the mixing/relabel attempt is retried, under a fixed bounded attempt cap. `generation_retries` is part of the measured output.

All measured fixed/sweep instances required **zero** generation retries.

## Public relation

A witness partitions every public triangle into groups of three. Every group must be an exact three-triangle P3 disk under the same simplicial predicate used by G11/G12.

The verifier never asks for the icosahedral coordinates, growth history, flip history, or reference cover. Any accepted equivalent cover is attacker success.

## A-042 — mixed-sphere normalization + exact-cover / SAT recovery

### Fixed Python 3.12 `g15-72` result

```text
growth steps:                              26
successful flips / rejected proposals:     1440 / 558
generation retries:                        0
public V/E/F:                              38 / 108 / 72
Euler characteristic:                      2
edge triangle incidence min/max:           2 / 2
primal degree histogram:                   ((3,10),(4,8),(5,6),(6,4),(7,3),
                                            (8,1),(9,2),(11,1),(12,2),(18,1))
initial degree-three vertices:              10
initial reverse-stacking candidates:       10
reverse-stacking moves:                    20
reverse terminal V/E/F:                    18 / 48 / 32
reached tetrahedron boundary:              no
normalization-improving legal flips:        39
dual vertices / edges:                     72 / 108
dual degree histogram:                     ((3,72),)
dual bipartite:                            no
bridges / articulation points:             0 / 0
dual triangle / four-cycle counts:         10 / 8
local signature classes:                   64
P3 public candidates:                      186
candidate memberships:                     6:30 / 9:42
candidate/triangle incidence:              558
exact-cover solutions / cap:               64 / 64
exact-cover nodes / decisions / backtracks:467 / 148 / 188
accepted public solutions:                 64
accepted non-reference solutions:          64
```

Thus the fixed carrier does what G15 intended structurally: A-041 is no longer a complete inverse. It stalls after 20 public reverse moves with 32 triangles still present. However, A-042 immediately finds 64 accepted alternative P3 covers.

### Deterministic sweep

Python 3.12 tested `g15-36`, `g15-54`, and `g15-72` over eight independently derived deterministic seeds each.

All **24/24** official sweep carriers:

- require zero P3-cover generation retries;
- do **not** reverse-stack completely to the tetrahedron boundary;
- reach the exact-cover cap `32/32`;
- return 32 accepted public covers;
- return 32 non-reference covers.

Maximum exact-cover work by size:

| Set | Max nodes | Max decisions | Max backtracks |
|---|---:|---:|---:|
| g15-36 | 202 | 56 | 86 |
| g15-54 | 260 | 84 | 125 |
| g15-72 | 427 | 128 | 288 |

Measured reverse terminal triangle counts range from 12–28 (`g15-36`), 20–40 (`g15-54`), and 42–54 (`g15-72`). Mixing therefore disrupts the complete stacked ancestry substantially on this sweep without making the witness relation difficult.

An auxiliary direct-byte regression seed outside the official sweep still completely reverse-stacks after mixing. That negative result is intentionally preserved: G15 does **not** establish that long flip walks universally defeat A-041. The generator never filters on this property.

### Independent MiniSat

Fixed `g15-72` public encoding:

```text
SAT variables / clauses:                  186 / 2034
DIMACS bytes:                             23382
restarts:                                 1
conflicts:                                55
decisions:                                234
propagations:                             1224
solver elapsed seconds:                   0.004067
selected candidate pieces:                24
decoded accepted witness:                 yes
matches reference after public success:   no
```

MiniSat independently confirms that the mixed-sphere candidate relation is easy and returns an accepted equivalent witness.

## Result

**G15 is rejected by A-042.**

This is the cleanest carrier/witness separation in the current G-series. Long bistellar mixing can defeat the obvious complete reverse-stacking attack on the measured main distribution, yet the bounded-radius P3 witness predicate still compiles to a tiny, highly multiply-solvable public exact-cover/SAT instance.

Further changes that only make the carrier more irregular are therefore not a justified repair. The next experiment must change what constitutes a valid witness.

## G16 gate

G16 must change the **witness predicate**, not merely the carrier. Candidate validity should depend on genuinely nonlocal topological information rather than a fixed-radius P3 motif.

Before any positive interpretation, the new relation must face:

- public quotient/normalization and canonicalization;
- compilation to generic finite-domain CSP;
- SAT/CP-SAT/exact-cover formulations where applicable;
- separator/treewidth and low-width dynamic programming;
- equivalent-witness enumeration;
- generated-role/statistical leakage;
- comparison of topology-aware and topology-free solver representations.

No trapdoor/KEM work begins before those gates survive.

No security claim.
