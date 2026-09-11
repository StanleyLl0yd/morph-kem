# 47 — G12 irregular-torus P3 hypercover negative control

## Status

**G12 is rejected by A-039 on the measured generated distribution.** Irregularizing the torus destroys G11's uniform local-role profile, but public P3 candidate extraction followed by generic exact cover or MiniSat still recovers accepted witnesses cheaply.

G12 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G11 removed the ordinary graph-matching reduction by moving to three-triangle P3 pieces, but its carrier remained a perfectly periodic torus. Public candidate roles were completely uniform and generic exact cover / MiniSat recovered many accepted equivalent covers.

G12 tests the most immediate alternative explanation: perhaps A-038 was easy only because of periodic translation symmetry. The carrier is therefore irregularized by many legal `2 <-> 2` edge flips before the P3 candidate relation is formed.

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

A deterministic seeded walk performs exactly the configured number of successful flips. The result is independently globally relabelled.

Toy sets:

```text
g12-6x6: 72 triangles, 36 successful flips
g12-6x9: 108 triangles, 54 successful flips
g12-8x9: 144 triangles, 72 successful flips
```

The final public object contains only the irregular simplicial complex and verifier semantics. Periodic coordinates, flip history, and reference cover are post-attack diagnostics only.

## Satisfiability conditioning

G12 does **not** preserve a pre-existing G11 cover while flipping. After irregularization, generation enumerates the valid final P3 candidate family and uses a hidden ordering only to choose one exact cover as reference evidence.

If the final irregular carrier has no P3 exact cover, generation retries only the deterministic flip seed up to an explicit cap. The number of failed attempts is recorded as `generation_retries`.

On the fixed Python 3.12 baseline and all 24 measured sweep instances, `generation_retries = 0`. Thus the measured break does not depend on aggressive rejection sampling.

## Public relation

A witness partitions every public triangle into groups of three. Every group must form the exact three-triangle P3 disk predicate.

The verifier never asks for the reference cover, flip history, original coordinates, or local roles. Any accepted equivalent cover is attacker success.

## Structural diagnostics

The irregularization gate succeeds strongly on the fixed `g12-8x9` baseline:

```text
successful flips / generation retries:      72/0
public V/E/F:                               72/216/144
Euler characteristic:                       0
edge triangle incidence min/max:            2/2
primal vertex-degree histogram:             3:8 / 4:9 / 5:14 / 6:12 /
                                            7:13 / 8:10 / 9:3 / 10:2 / 12:1
dual vertices/edges:                        144/216
dual degree histogram:                      ((3,144),)
dual bipartite:                             no
bridges / articulation points:              0/0
dual triangle / four-cycle counts:          8/9
local signature classes:                    82
signature class-size histogram:             1:46 / 2:24 / 3:5 / 4:4 / 5:2 / 9:1
normalization-improving legal flips:         59
```

This is no longer G11's uniform periodic carrier. The public degree and radius-one/radius-two signature distributions are highly nonuniform, the dual is non-bipartite, and many legal flips publicly reduce degree irregularity toward the regular torus.

## A-039 — irregular-carrier candidate extraction + exact cover / SAT

### Exact-cover path

A-039 derives edge/triangle incidence from the final irregular complex, builds the final triangle-dual graph, enumerates every induced dual P3, applies the exact simplicial disk predicate, and solves the public candidate/triangle incidence hypergraph with deterministic MRV Algorithm-X-style exact cover.

Fixed Python 3.12 `g12-8x9`:

```text
P3 public candidates:                       408
candidate memberships per triangle:        6:24 / 9:120
candidate overlap-degree histogram:        11:4 / 13:2 / 14:44 / 15:42 /
                                            17:32 / 18:284
candidate/triangle incidence size:          1224
exact-cover solutions / cap:                64/64
exact-cover cap hit:                        yes
exact-cover nodes / decisions / backtracks: 456/119/119
accepted public solutions:                  64
accepted non-reference solutions:          64
```

Every returned exact-cover witness passes the original nonlinear simplicial verifier, and all first 64 differ from the reference cover.

### Deterministic sweep

Python 3.12 tested `g12-6x6`, `g12-6x9`, and `g12-8x9` over eight independently derived deterministic seeds each.

All **24/24** instances:

- perform exactly the configured number of successful flips;
- need zero generation retries;
- remain closed genus-one surfaces with connected 3-regular dual graphs and zero bridges/articulations;
- become non-bipartite;
- expose multiple primal degree classes and many local signature classes;
- have a nonuniform P3 candidate-membership profile;
- reach the 32-solution exact-cover cap;
- return 32/32 accepted public covers, all 32 non-reference.

Measured exact-cover nodes remain small. Maxima over the sweep are:

```text
g12-6x6:  276 nodes
g12-6x9:  366 nodes
g12-8x9:  761 nodes
```

The candidate count is no longer the fixed regular `3F` value from G11. Across measured seeds it varies with the irregular carrier: roughly 201–213, 309–315, and 408–420 candidates respectively.

### Independent MiniSat cross-check

Fixed Python 3.12 `g12-8x9` encoding:

```text
SAT variables / clauses:                  408/4824
DIMACS bytes:                             58551
restarts:                                 2
conflicts:                                105
decisions:                                807
propagations:                             4699
solver elapsed seconds:                   0.005333
selected candidate pieces:                48
decoded accepted witness:                 yes
matches reference after public success:   no
```

MiniSat independently confirms that the irregular public candidate hypergraph remains easy to satisfy.

## Normalization probe

A complete inverse-flip canonicalizer is unnecessary for rejection because A-039 is already fatal. Nevertheless, the fixed baseline has 59 legal public flips that strictly reduce squared deviation of primal vertex degrees from six. This provides an additional public simplification direction rather than evidence that irregularization hides the carrier.

## Result

**G12 is rejected by A-039.**

The negative result is stronger than G11's periodicity explanation. Many legal edge flips genuinely destroy translation symmetry and local role uniformity, but the exact P3 candidate hypergraph remains easy for generic public exact cover and SAT. Equivalent-witness multiplicity remains severe.

Do not repair G12 by increasing flip count, torus dimensions, or retry depth. Those changes do not alter the measured computational relation.

This is a generated-distribution falsification, not a theorem that arbitrary irregular topology or arbitrary hypergraph exact cover is easy.

## G13 gate

A successor must abandon the periodic-torus-plus-local-flips carrier family rather than stack more cosmetic irregularization. It must immediately face canonicalization/isomorphism, separator/treewidth analysis, candidate extraction, exact cover/set packing, SAT/CP-SAT, simplification/normalization, equivalent-witness multiplicity and generated-role leakage.

Only after both carrier recovery and the resulting candidate hypergraph survive these public attacks could the project consider any trapdoor interface.

No security claim.
