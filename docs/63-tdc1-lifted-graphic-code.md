# 63 — TDC1 lifted graphic-code negative control

## Status

**TDC1 is a falsification experiment in progress.** It removes TDC0's forced triangle codewords by replacing the raw triangulation cycle space with a sparse graph lift, then asks whether the resulting public code is still structurally easy.

TDC1 is not a KEM, one-way function, post-quantum assumption, or production-security construction.

## Construction

The topology-derived family is an `L`-sheet graph cover of `K4`. Every base edge receives an independently seeded public permutation of the `L` sheets. The resulting connected cubic graph has

```text
V = 4L
E = 6L
rank(H) = V - 1
k = E - V + 1 = 2L + 1
```

where `H` is the public vertex-edge incidence matrix over GF(2). A final global relabel removes the generation role labels.

Toy sets:

```text
tdc1-L8:  V=32, E=48, error weights 1..4
tdc1-L12: V=48, E=72, error weights 1..4
tdc1-L18: V=72, E=108, error weights 1..5
```

For every topology-derived instance, generation also constructs a connected simple random cubic graph with exactly the same `V/E` and degree sequence. Rejection counts for both generators are explicit.

## TDC-A002 attack 1 — graphic-code decoding

The lifted code is still a public **graphic cycle code**. Its minimum distance is exactly the graph girth, and syndrome decoding has a direct graph interpretation.

For a public edge-error vector:

1. compute the odd-incidence syndrome vertices;
2. run BFS from every syndrome vertex;
3. build the complete defect metric;
4. solve exact minimum defect pairing by bitmask DP;
5. XOR canonical shortest paths to obtain a minimum T-join;
6. verify that the recovered edge set has exactly the public syndrome.

Any syndrome-equivalent correction is attacker success. Equality with the planted error is recorded only after public success.

This attack applies equally to the lifted family and to a matched random graphic code. Therefore even if topology does not make decoding *easier* than random, remaining inside the graphic-code class can itself be fatal for a cryptographic decoding assumption.

## TDC-A002 attack 2 — public quotient recovery

The planted lift is a locally bijective cover of `K4`: vertices admit four equal-size role classes, and every vertex has exactly one neighbor in each of the other three classes.

After global relabeling the attacker tries to recover any such quotient by constrained 4-coloring:

- fix one public vertex to color 0;
- try the six permutations of colors 1/2/3 on its three neighbors;
- enforce proper coloring, class-size `L`, and the local rainbow-neighborhood constraint;
- use deterministic MRV backtracking;
- accept any complete locally bijective projection to `K4`.

A recovered partition need not match generation sheet labels. Any public quotient is structural leakage.

## Matched-random structural control

Measure the lifted and random cubic graphs side by side:

- exact girth;
- triangle count;
- four-cycle count;
- parity-check rank, code dimension and rate;
- cubic degree histogram;
- generation retries.

The matched-random control is not a security baseline. It only separates generic graphic-code weakness from additional cover-specific leakage.

## Measurements

Record at least:

- `L`, `V/E`, rank/dimension/rate;
- lift/random generation retries;
- lift/random girth and short-cycle counts;
- public quotient recovery, search nodes and backtracks;
- decoding curve over every declared error weight;
- syndrome weight, BFS work, matching-DP states/pair tests;
- minimum correction weight;
- exact public syndrome verification;
- post-success equality with planted error;
- deterministic all-size / multi-seed sweep.

## Rejection gate

Reject TDC1 if either:

1. public quotient recovery routinely reconstructs a `K4` covering partition; or
2. public graphic-code T-join decoding routinely returns accepted syndrome-equivalent corrections with small work.

Do not repair by increasing only the lift factor while the code remains graphic or while the same quotient projection is recoverable.

## Advancement gate

TDC2 must leave the ordinary graphic cycle-code class. A successor should use a genuinely higher-dimensional or non-graphic sparse code construction where public decoding does not collapse to minimum T-join, and must still face low-weight search, quotient/cover recovery, BP/bit-flipping, ISD/MITM and matched-random comparisons.

No security claim.
