# 67 — HGA4 infinite Hurwitz action on free-group tuples

## Status

**The current HGA4 planted-word generator is rejected by HGA-A005-G, but the infinite Hurwitz action is not structurally rejected by this experiment.** Exact toy MITM recovers all deliberately short instances, as expected, while the measured exact-state balls grow substantially with depth. The fatal measured issue is instead generated-word non-geodesicity: half of the official instances admit an equivalent connector at least 25% shorter than the planted action.

HGA4 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Public action

Let `F(a,b)` be the rank-two free group. A public state is an ordered triple of exactly reduced free-group words `(g1,g2,g3)`.

The braid-group generators act by Hurwitz moves:

```text
p = sigma_1:      (x,y,z) -> (x y x^-1, x, z)
P = sigma_1^-1:   (x,y,z) -> (y, y^-1 x y, z)
q = sigma_2:      (x,y,z) -> (x, y z y^-1, y)
Q = sigma_2^-1:   (x,y,z) -> (x, z, z^-1 y z)
```

Generation samples three source words with distinct nonzero free abelianizations and a locally reduced planted braid word. The exact target tuple is obtained by applying the planted word.

Toy planted lengths are `8`, `12`, and `16`. The verifier accepts **any** braid word carrying the exact public source tuple to the exact public target tuple. Equality with the planted word is reference-only.

## Public invariants and quotient

The exact endpoint state space is infinite: reduced component lengths can grow without bound. Two cheap public invariants remain visible:

1. the reduced product `g1 g2 g3` is exactly Hurwitz-invariant;
2. component free abelianizations are only permuted.

Because the three source abelianization vectors are distinct, the target tuple exposes the induced public strand permutation in `S3`. On all measured instances this quotient agrees with the planted braid permutation, but it does **not** directly construct the full connector.

## HGA-A005 — exact bounded MITM

For public word bound `L`, exact bidirectional BFS enumerates the source ball to depth `floor(L/2)` and the target ball to depth `ceil(L/2)`. States are exact reduced free-group tuples, so inverse cancellation, braid relations and action stabilizers are reflected only through genuine state collisions. Every meet produces a connector that is resubmitted to the exact endpoint verifier.

Toy MITM success is deliberately **not** treated as a structural break here. The experiment instead measures whether work grows and whether generation plants strongly non-geodesic actions.

## Fixed Python 3.12 result

For `hga4-L16`:

```text
source component lengths:                (1,2,2)
target component lengths:                (119,156,34)
invariant product length / verified:      3 / yes
source abelianization:                    ((-1,0),(2,0),(0,2))
target abelianization:                    ((-1,0),(2,0),(0,2))
recovered strand permutation:             (0,1,2)
quotient matches planted:                 yes
planted word length:                      16
forward / backward depth:                 8 / 8
forward / backward states:                1356 / 2589
forward / backward transitions:           2624 / 4932
meet states:                              87
recovered connector length:               10
endpoint verified:                        yes
matches planted word:                     no
at least 25% shorter than planted:         yes
```

The large endpoint words therefore do not imply a large exact search ball: this particular endpoint has a length-10 equivalent action despite a planted length of 16.

## Deterministic sweep

Python 3.12 tested planted lengths `8`, `12`, and `16` over eight deterministic seeds each.

All **24/24** instances have an exact publicly verified connector within the planted bound. This is expected for the deliberately bounded MITM experiment and is not by itself a rejection result.

The generated-word distribution is problematic:

- only **1/24** recovered shortest connectors equal the planted word exactly;
- **12/24** instances have a connector at least 25% shorter than planted;
- `L=8`: recovered lengths `4–8`, with 7/8 materially shorter;
- `L=12`: recovered lengths `6–12`, with 3/8 materially shorter;
- `L=16`: recovered lengths `10–16`, with 2/8 materially shorter.

At the same time, the exact state-ball sizes show clear growth rather than a constant-size orbit collapse. Typical symmetric half-balls are approximately:

```text
planted L=8,  half-depth 4:  115 states / side, 188 transitions
planted L=12, half-depth 6:  577 states / side, 1052 transitions
planted L=16, half-depth 8:  2589 states / side, 4932 transitions
```

Some instances have smaller one-sided balls because the exact action state has additional collisions/stabilizers, but no Euclidean-style direct connector or HGA3-style linear kernel solver was observed in this gate.

Dedicated HGA4 CI passes on Python 3.11, 3.12 and 3.13.

## Result

**HGA-A005-G rejects the current locally reduced random planted-word generator/distribution, not the underlying infinite Hurwitz action family.** Local inverse cancellation is far too weak a generation criterion: equivalent action relations make the planted words frequently non-geodesic.

This is still fatal to the current candidate. Scaling planted length while keeping the same generator would only hide more reducible action history and is not an acceptable repair.

Conversely, the measured growth `115 -> 577 -> 2589` is evidence only that this particular exact-search baseline grows on the toy distribution. It is **not** a hardness, one-wayness, asymptotic, classical-security, or post-quantum claim.

## HGA4b successor gate

The next HGA4 control should keep the same action but replace planted-word sampling with an explicit constructive state-space generator that avoids silently conditioning on attack failure. A suitable control is a deterministic self-avoiding action-state walk: at each step choose among generators whose next exact public state has not appeared earlier in the generated path, with an explicit terminal/failure rule rather than unbounded rejection.

HGA4b must then rerun:

- exact product and abelianization quotient diagnostics;
- bounded MITM growth at increasing lengths;
- shortest-equivalent-connector measurements;
- stabilizer/state-collision statistics;
- finite quotient representations;
- canonical/Garside-style reductions where applicable;
- explicit quantum hidden-shift/subgroup screening before any later cryptographic interpretation.

No security claim.
