# 63 — TDC1 lifted graphic-code negative control

## Status

**TDC1 is rejected by TDC-A002.** The `K4` graph lift does not escape low-distance or polynomial graphic decoding, and its base quotient remains publicly recoverable on the calibrated lift size.

TDC1 is not a KEM, one-way function, post-quantum assumption, or production-security construction.

## Construction

The topology-derived family is an `L`-sheet graph cover of `K4`. Every base edge receives an independently seeded permutation of the `L` sheets, followed by global relabeling. The resulting public code is the binary cycle code of the connected cubic lift.

Toy sets:

```text
tdc1-L8:  V=32, E=48, error weights 1..4
tdc1-L12: V=48, E=72, error weights 1..4
tdc1-L18: V=72, E=108, error weights 1..5
```

Each topology-derived instance is paired with a simple connected random cubic graph of exactly the same `V/E` and degree sequence.

## TDC-A002 — graphic decoding

Because the public parity-check matrix is vertex-edge incidence, minimum-distance equals graph girth and syndrome decoding is a public minimum T-join problem. The attack computes syndrome vertices, all-pairs defect distances by BFS, exact minimum defect pairing by bitmask DP, and a syndrome-equivalent edge correction.

Any accepted correction is attacker success. It need not equal the planted error.

## TDC-A002 — quotient probe

The planted lift also admits a locally bijective projection to `K4`. A deterministic constrained four-coloring attack searches for four equal-size role classes after global relabeling. Exact exhaustive quotient recovery is treated as a secondary bounded structural probe, not as the decoding gate: the full eight-seed sweep is run at `L=8`; larger lifts are not allowed to turn CI runtime into a pseudo-hardness metric.

## Fixed Python 3.12 result

For `tdc1-L18`:

```text
lift factor:                         18
lift generation retries:              0
matched-random generation retries:   15
lift V/E/rank/dimension/rate:        72/108/71/37/0.342592593
random V/E/rank/dimension/rate:      72/108/71/37/0.342592593
lift girth / triangles / C4:          3 / 2 / 0
random girth / triangles / C4:        3 / 1 / 5
```

Thus the lifted code already has exact `d_min = 3` on the fixed largest toy instance.

Exact public decoding succeeds for planted error weights 1 through 5. At weight five the fixed attack uses only 89 matching-DP states and 332 pair tests and returns an accepted weight-five correction.

## Deterministic sweep

Python 3.12 tested all declared error weights over eight seeds for every lift:

- `L=8`: 32 decoding instances;
- `L=12`: 32 decoding instances;
- `L=18`: 40 decoding instances;
- total: **104/104** public syndromes receive an accepted T-join correction.

Three measured cases return a correction different from the planted error while still satisfying the exact public syndrome (`L8` seeds 0 and 7 at weight 4; `L12` seed 2 at weight 4). These are attacker successes and preserve equivalent-error evidence.

Across all **24/24** topology-derived lift samples the measured girth is exactly `3`, so every lifted code has `d_min=3`. Matched-random cubic controls sometimes reach girth 4, so the topology-derived family shows no structural improvement on this metric.

The bounded public quotient probe is attempted on all eight `L=8` samples and succeeds on **8/8** after global relabeling. Search work ranges from 8,499 to 153,589 nodes. The larger-lift quotient probe is intentionally not interpreted; the independent graphic decoding and distance failures already reject the family.

Dedicated TDC1 CI passes on Python 3.11, 3.12 and 3.13 after making the quotient-probe budget explicit.

## Result

**TDC1 is rejected by TDC-A002 for three independent reasons:**

1. all generated lift samples retain `d_min=3`;
2. the entire public code class is graphic, so syndrome decoding reduces to minimum T-join and succeeds on 104/104 measured errors;
3. the planted `K4` quotient is publicly recoverable on all calibrated `L=8` samples despite global relabeling.

Increasing only the lift factor is not a repair. TDC2 must leave the ordinary graphic cycle-code class completely.

## TDC2 gate

TDC2 uses a genuinely non-graphic lifted 2-complex sparse code and must face graphic/cographic reduction tests, low-weight search, quotient recovery, BP/bit-flipping, OSD/ISD/MITM, generic exact decoding and matched-random controls.

No security claim.
