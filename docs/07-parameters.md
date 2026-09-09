# 07 — Parameters

No security parameter set exists. All names below are experiment sizes only.

M0 is broken by A-000, M1 by A-008, M2 by A-014, M3 by A-016, and M4 by A-018.

## M4 closed-surface ladder

| Set | Vertices | Edges | Triangles | Total simplices | Target |
|---|---:|---:|---:|---:|---|
| torus-3x3 | 9 | 27 | 18 | 54 | (1,2,1) |
| torus-4x4 | 16 | 48 | 32 | 96 | (1,2,1) |
| torus-5x5 | 25 | 75 | 50 | 150 | (1,2,1) |
| torus-6x6 | 36 | 108 | 72 | 216 | (1,2,1) |
| torus-7x7 | 49 | 147 | 98 | 294 | (1,2,1) |

Every tested edge has two incident triangles and every tested target has zero free elementary-collapse pairs.

### A-018 fixed-seed results

| Set | Free pairs | Deterministic tree-cotree | Random accepted | Unique random matchings |
|---|---:|---:|---:|---:|
| torus-3x3 | 0 | accepted | 32/32 | 32 |
| torus-4x4 | 0 | accepted | 32/32 | 32 |
| torus-5x5 | 0 | accepted | 32/32 | 32 |
| torus-6x6 | 0 | accepted | 32/32 | 32 |
| torus-7x7 | 0 | accepted | 32/32 | 32 |

These are reproducible fixed-seed observations, not asymptotic estimates.

For torus-4x4, generic greedy Hasse matching hit the target 0/4 times and reached best total critical count 6; A-018 deterministically reaches target total 4.

## Security interpretation

Parameter inflation is never a response to a structural break. M0–M4 all fail before a security-parameter gate.

A future family may scale only after equivalent-witness semantics, constructive decomposition attacks, incidence/statistical distinguishers, greedy and exact solver attacks, width analysis, and a quantum threat model are in place.
