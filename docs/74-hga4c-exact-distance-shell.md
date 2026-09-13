# 74 — HGA4c exact-distance Hurwitz endpoint shell calibration

## Status

**HGA4c is rejected as an exact-shell endpoint generator by HGA-A007.** Exact shell selection successfully removes the planted-history artifact: every measured target has the declared exact action distance, unique measured shortest-path multiplicity, and no hidden shortening. But the generator must construct the full depth-`D` ball while ordinary public bidirectional recovery reaches the same endpoint using a rapidly shrinking fraction of that state work.

This rejects the bounded exact-shell generation mechanism, not the infinite Hurwitz action family.

HGA4c is not a scalable secret generator, trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Construction

Reuse the HGA4 action of `B3` on triples of reduced words in `F(a,b)`. Declared toy distances are `D=4,6,8`.

For each deterministic source:

1. build the complete action-state BFS ball through depth `D`;
2. retain the exact shell `S_D` of states first discovered at depth `D`;
3. choose the target that maximizes total reduced component length, breaking ties by a seeded public hash;
4. retain one shortest certificate and capped shortest-path multiplicity as generator evidence;
5. publish only source, target and public distance bound `D`.

The target is therefore certified to have exact action distance `D`. The generator never queries the later bidirectional recovery output.

## HGA-A007

The attacker runs the unchanged public HGA4 bidirectional recovery:

- build forward/backward balls to the split public bound;
- find meet states;
- construct any equivalent connector;
- verify the endpoint exactly.

Because the target comes from an exact shell, a connector shorter than `D` would indicate a generator/measurement error rather than an attack result.

## Fixed Python 3.12 result

For `hga4c-D8`:

```text
exact distance:                         8
generator ball / shell states:     2589 / 1356
generator transitions:                 4932
selected target total reduced length:  1566
shortest-path multiplicity:               1
attacker forward / backward states:   115 / 115
attacker forward / backward transitions: 188 / 188
meet states:                              1
recovered connector length:               8
endpoint verified:                       yes
matches retained certificate:            yes
attacker states / generator ball:     0.088837389
```

The exact-distance repair therefore works as intended: there is no shorter connector and the selected fixed endpoint has a unique measured shortest path. The fatal calibration result is instead the wrong work asymmetry: the exact-shell generator enumerates 2,589 states while the public meet-in-the-middle recovery needs only 230 stored states.

## Eight-seed sweep

Across `D=4,6,8` × eight deterministic seeds, all **24/24** targets satisfy:

- recovered connector length exactly equals the declared exact distance `D`;
- endpoint verification succeeds;
- measured shortest-path multiplicity is exactly **1**;
- exactly one meet state is observed;
- the recovered connector equals the retained generator certificate after public success.

The attacker-state fraction of the full generator ball decreases by depth:

```text
D=4: 0.295652 .. 0.363636
D=6: 0.162912 .. 0.204327
D=8: 0.088837 .. 0.134956
```

Representative full-ball sizes are `115`, `577`, and `2589` states at D=4/6/8, while balanced bidirectional recovery uses roughly the corresponding half-depth balls. The observed reduction is therefore the expected public meet-in-the-middle advantage, not a hidden canonical shortcut.

## Interpretation

HGA4c answers a useful question negatively. HGA4/HGA4b could be criticized because their planted paths were often non-geodesic. HGA4c removes that defect completely on the measured toy sets, yet it still does not create a useful generation/recovery asymmetry: producing an exact-distance target by public full-shell enumeration costs substantially more state exploration than recovering its connector by public bidirectional search.

That is enough to reject **this generator** as a route toward a primitive. It is **not** evidence that the infinite Hurwitz action has polynomial-time inversion, and it is not an asymptotic hardness statement.

A successor cannot justify itself merely by deeper exact shells: that preserves the same generator-versus-MITM asymmetry. Further HGA work would need a genuinely cheap public/trapdoor-like endpoint sampler whose distance is not certified by doing more generic search than the attacker, and it must still face finite representations, stabilizers, canonical forms and equivalent witnesses.

No one-wayness, post-quantum, IND-CPA/CCA, or production-security claim exists.
