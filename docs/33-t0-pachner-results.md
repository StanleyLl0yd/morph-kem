# 33 — T0 bounded Pachner search result

## Status

**T0 is rejected as a generated hardness candidate.**

T0 is an attack-first calibration of BTTS — Bounded Topological Transformation Search. It is not a KEM, trapdoor primitive, one-way function, post-quantum assumption, or production-security claim.

## Public relation

The public instance is `(R0, R1, L, params)` where `R0` and `R1` are finite closed 3-dimensional abstract simplicial complexes, quotient-normalized by exact vertex relabeling.

A witness is **any** legal sequence of state-dependent `2-3` / `3-2` Pachner moves of length at most `L` that transforms `R0` into a state isomorphic to `R1`.

The planted walk is reference evidence only.

## Exact implementation properties

- start states are obtained from the boundary of a 4-simplex by deterministic 1-4 burn-in;
- challenge moves are only legal `2-3` / `3-2` moves;
- every state is checked as a closed connected 3-pseudomanifold;
- canonicalization quotients vertex labels exactly within the toy residual bound;
- inverse `2-3` / `3-2` adjacency is tested in the quotient graph;
- BFS and bidirectional BFS work only on public canonical states;
- attacker success accepts any path within the public bound.

## A-022 — short equivalent Pachner path / bidirectional recovery

Fixed seed used by CI:

~~~text
48026490aabbccddeeff1029384756aa
~~~

Python 3.12 exact-head CI sweep:

| Set | Planted length | BFS distance | BFS visited | BFS expanded | Bidir distance | Bidir forward | Bidir reverse | Bidir expanded | Mean unique branching | Commuting fraction |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| t0-4 | 4 | 4 | 154 | 47 | 4 | 40 | 55 | 13 | 15.250 | 0.028319 |
| t0-6 | 6 | 6 | 588 | 316 | 6 | 149 | 187 | 75 | 18.667 | 0.019201 |
| t0-8 | 8 | **4** | 170 | 51 | **4** | 40 | 65 | 13 | 20.000 | 0.009336 |

The `t0-8` endpoint is therefore reachable in four moves although generation deliberately planted an eight-move non-self-repeating walk.

Detailed `t0-8` CI baseline:

~~~text
start vertices/tetrahedra:      9/17
target vertices/tetrahedra:     9/21
Euler start/target:             0/0
planted length/public bound:    8/8
planted moves 2-3 / 3-2:        6/2
branching initial/min/mean/max: 12/12/21.12/28
mean unique branching:          20.00
neighbor collisions:            9
commuting move pairs:           17/1821

BFS:
  distance:                     4
  visited:                      170
  expanded:                     51
  max frontier:                 119

bidirectional BFS:
  distance:                     4
  forward/reverse visited:      40/65
  expanded:                     13
  max forward/reverse frontier: 31/39
  recovered witness valid:      yes
~~~

The exact-head T0 workflow passed on Python 3.11, 3.12 and 3.13; eight T0 unit tests passed on each interpreter.

## Interpretation

The failure is not the M1 failure repeated verbatim. T0 has real state-dependent local moves, non-binary branching, canonical quotient states, and a low measured commuting-pair fraction. Nevertheless the generated random walk does not control the actual quotient reconfiguration distance.

The planted path length `L` is therefore not a hardness parameter.

For the fixed `t0-8` generated instance:

~~~text
planted length = 8
true public distance <= 4
bidirectional expansions = 13
~~~

This is enough to reject the T0 generator. It is not an asymptotic theorem about Pachner graphs or BTTS in general.

## Generator lesson

A successor must measure or certify properties of the **quotient reconfiguration graph**, not properties of generation history.

At minimum it should distinguish:

~~~text
planted walk length L
shortest quotient distance d(R0,R1)
number of short equivalent witnesses
bidirectional frontier growth
state-collision rate
move-support interaction
~~~

Parameter inflation from `L=8` is explicitly forbidden as a repair.

## T1 gate

T1 may proceed only as another falsification experiment. Its generator should sample endpoints conditioned on measured quotient distance and should deliberately avoid easy return paths.

Before any trapdoor claim, T1 must be attacked by:

- exact BFS / bidirectional BFS where feasible;
- A*/IDA* with admissible lower bounds when available;
- beam/random-restart search;
- automorphism-aware canonical hashing;
- path-multiplicity estimation;
- move-dependency and commuting-region decomposition;
- bounded SAT/CP-SAT/planning encoding;
- any public potential correlated with distance.

Even a T1 instance with a large measured shortest path would still not be a cryptographic primitive. A later phase would separately require a concrete secret `TrapdoorRecover` advantage on a generated positive distribution.
