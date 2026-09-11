# 61 — HGA1 Heisenberg Nielsen-action negative control

## Status

**HGA1 is rejected by HGA-A002.** The first genuinely noncommutative HGA action remains publicly invertible on the generated distribution by a small abelianized quotient plus bounded bidirectional endpoint search.

HGA1 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Public action

Use the finite Heisenberg group over `F_p`:

```text
(x,y,z) * (x',y',z') =
(x+x', y+y', z+z' + x*y') mod p.
```

A public state is an ordered pair `(g,h)`. The action generators are elementary Nielsen moves:

```text
L:  (g,h) -> (g*h, h)
l:  (g,h) -> (g*h^-1, h)
R:  (g,h) -> (g, h*g)
r:  (g,h) -> (g, h*g^-1)
```

The source has abelianized basis coordinates and independently seeded central coordinates. Generation applies a reduced planted word with no immediate inverse cancellation.

Toy sets:

```text
hga1-p5:  p=5,  word length 8
hga1-p7:  p=7,  word length 10
hga1-p11: p=11, word length 12
```

The verifier is simply public endpoint equality after applying a submitted action word. Any equivalent connecting word is attacker success.

## Public quotient

Abelianization forgets the central `z` coordinates. The four public endpoint coordinates `(gx,gy,hx,hy)` evolve under the same elementary Nielsen moves.

The generated source lies in the determinant-one orbit. The attack enumerates this entire public quotient orbit and records its size and shortest quotient connector length.

This is not itself enough to recover the central residual, but it measures how much of the action is exposed by the cheapest public quotient.

## HGA-A002 — quotient + bidirectional endpoint recovery

The public endpoint attack is:

1. enumerate the full abelianized quotient orbit and shortest quotient distance;
2. BFS from the full nonabelian source to half the public planted-word bound;
3. BFS from the full nonabelian target to the complementary half using the symmetric generator set;
4. intersect the two public state tables;
5. combine a source-to-meet word with the inverse of the target-to-meet word;
6. verify the recovered connector by applying it to the public source.

The recovered word is **not required to match the planted word**. Equality is recorded only after public success.

## Measured HGA-A002 result

Exact Python 3.12 fixed `hga1-p11`:

```text
prime / group size:                    11 / 1331
planted word length:                   12
abelianized quotient orbit size:       1320
quotient BFS transitions:              5280
quotient shortest connector length:       6
MITM forward / backward states:        532 / 532
MITM transitions:                      2088
MITM meet states:                       221
recovered connector length:               6
recovered connector:                    Lrrrrl
public endpoint verification:          yes
matches planted word after success:    no
```

Python 3.12 sweep over all three primes × eight deterministic seeds gives **24/24** accepted public connectors within the planted public word bound.

Measured orbit/search structure is highly stable:

- `p=5`: quotient orbit `120`, forward/backward full-state tables `91/91`, `344` MITM transitions, recovered lengths `2–6` versus planted length `8`;
- `p=7`: quotient orbit `336`, tables `221/221`, `888` transitions, recovered lengths `4–6` versus planted `10`;
- `p=11`: quotient orbit `1320`, tables `532/532`, `2088` transitions, recovered lengths `6–9` versus planted `12`.

Every recovered connector differs from the planted generation word: **0/24 planted-word matches after public success**. Meet-state multiplicity is already large (65–72 for `p=5`, 136–170 for `p=7`, 167–228 for `p=11`).

The dedicated HGA1 workflow passes on Python 3.11, 3.12 and 3.13.

## Result

**HGA1 is rejected by HGA-A002.** Noncommutativity at the object level is not enough when the action factors through a small enumerable quotient and the full endpoint orbit is shallow under the public generators.

The especially important negative result is equivalent-action multiplicity: the public attacker never recovered the planted word in the measured sweep, yet every alternate connector mapped the exact public source to the exact public target. Therefore hiding one action word is not a useful primitive when many short equivalent connectors exist.

Increasing only the secret word length would be cosmetic while the finite quotient/orbit and shallow Cayley/Schreier geometry remain publicly enumerable.

## Advancement gate

HGA2 must move beyond a small finite Nielsen orbit or provide a structural reason why canonical quotients and MITM do not dominate. A next candidate should have a substantially larger or effectively infinite public orbit, while still exposing efficient public action evaluation.

Any HGA2 candidate must immediately face:

- abelianization and low-dimensional quotient representations;
- character/trace-style invariants where applicable;
- stabilizers and equivalent-action multiplicity;
- normal forms/canonicalization;
- bidirectional endpoint search and generic MITM;
- finite quotient projections;
- generated-role leakage;
- quantum hidden-shift/hidden-subgroup reducibility screening.

No security claim.
