# 61 — HGA1 Heisenberg Nielsen-action negative control

## Status

**HGA1 is an attack calibration in progress.** It is the first HGA candidate whose public objects and action are genuinely noncommutative. No hardness conclusion is permitted until exact-head CI measures HGA-A002.

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

Abelianization forgets the central `z` coordinates. The four public endpoint coordinates `(gx,gy,hx,hy)` evolve under the same elementary row/column-style Nielsen moves.

The generated source lies in the determinant-one orbit. The attack enumerates this entire public quotient orbit and records its size and shortest quotient connector length.

This is not itself enough to recover the central residual, but it measures how much of the action is exposed by the cheapest public quotient.

## HGA-A002 — quotient + bidirectional endpoint recovery

The primary endpoint attack is public bidirectional search:

1. enumerate the full abelianized quotient orbit and shortest quotient distance;
2. BFS from the full nonabelian source to half the public planted-word bound;
3. BFS from the full nonabelian target to the complementary half using the symmetric generator set;
4. intersect the two public state tables;
5. combine a source-to-meet word with the inverse of the target-to-meet word;
6. verify the recovered connector by applying it to the public source.

The recovered word is **not required to match the planted word**. Equality is recorded only after public success.

## Measurements

Record at least:

- `p` and group size `p^3`;
- planted word length;
- abelianized orbit size and BFS transitions;
- shortest quotient connector length;
- forward/backward full-state counts;
- MITM transitions and meet-state multiplicity;
- recovered connector length;
- exact public endpoint verification;
- post-success planted-word equality;
- deterministic all-size / multi-seed sweep.

## Rejection gate

If bounded public MITM routinely recovers any valid connector within the public word bound, **reject HGA1**. A mismatch with the planted word is not a defense; it is evidence of equivalent-action multiplicity.

Do not repair by increasing only the word length while the finite orbit and quotient remain publicly enumerable.

## Advancement gate

HGA2 must move beyond a small finite Nielsen orbit or provide a structural reason why canonical quotients and MITM do not dominate. Any next candidate must still face abelianization, character/trace-style invariants where applicable, stabilizers, finite quotient representations, canonical forms, endpoint MITM and quantum hidden-shift/subgroup screening.

No security claim.
