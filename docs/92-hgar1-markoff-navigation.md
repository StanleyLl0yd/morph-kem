# 92 — HGA-R1 finite Markoff action navigation negative control

## Status

**HGA-R1 is rejected by HGA-R-A001.** The declared public Markoff/Schreier graph is directly navigable on every sampled instance: ordinary BFS and the bounded two-tree/bidirectional search recover verifier-accepted actions on all 72/72 cases.

The `R` suffix is deliberate. The repository already preserves the historical HGA1 Heisenberg/Nielsen negative control and its workflow. HGA-R1 is the first measured experiment in the post-NAT redesign line; it does not replace or reinterpret the historical HGA0/HGA1 corpus.

No hardness, novelty, one-wayness, post-quantum, KEM, signature, IND-CPA/CCA or production-security claim exists.

## Public object and action

For `p in {29,43,59}`, use the nonzero Markoff surface

```text
M_p = {(x,y,z) in F_p^3 : x^2 + y^2 + z^2 - xyz = 0} \ {(0,0,0)}.
```

The public involutory generators are

```text
V1(x,y,z) = (yz-x, y, z)
V2(x,y,z) = (x, xz-y, z)
V3(x,y,z) = (x, y, xy-z)
```

with all coordinates reduced modulo `p`. Each `Vi` preserves the Markoff equation and satisfies `Vi^2 = id`.

A word is **reduced** when adjacent generator labels differ. Public reduction only cancels adjacent equal involutions and never uses the planted action.

## Binding-action interface

Generation publishes

```text
X in M_p
Y = s(X)
L
```

where `s` is a planted reduced word of length exactly `L`. The verifier accepts a candidate word `w` iff

```text
1 <= len(w) <= L
w is reduced
w(X) = Y.
```

The attack objective is to recover **any** accepted word. Equality with the planted word is reference-only after public success.

Generation may resample the planted word only when it maps `X` to itself. It never observes attack output.

## Fixed grid

The grid was fixed before measurement:

```text
p in {29,43,59}
L in {8,16,24}
8 deterministic seeds per (p,L)
```

This is exactly 72 instances. No prime, word bound, seed count or attack budget was changed after inspecting recovery results.

Implementation parameter IDs retain the compact `hga1-pXX-LYY` spelling inside the isolated Markoff module, but the experiment name and workflow are **HGA-R1** to avoid collision with the preserved historical HGA1 Heisenberg experiment.

## HGA-R-A001 — public navigation attacks

### Ordinary shortest BFS

Deterministic BFS runs from `X` on the public generator graph, stopping when `Y` is first discovered or depth `L` is exhausted. It records states discovered/expanded, generator-edge scans, shortest recovered length and exact verifier acceptance.

### Bounded two-tree / bidirectional search

Public bounded BFS trees are built from `X` and `Y` with radii

```text
ceil(L/2)
floor(L/2).
```

An intersection minimizing total public depth is chosen. Because the generators are involutions, the right half is traversed back with the same labels. Adjacent equal labels created at the join are publicly cancelled before verification.

This implementation intentionally records its full bounded-tree work instead of claiming an optimized bidirectional stopping rule. Ordinary BFS alone is already sufficient for rejection.

### Full public orbit

The connected component of `X` is independently enumerated. In every measured case it equals the entire nonzero Markoff point set for the selected prime:

```text
p=29:   928 / 928
p=43:  1720 / 1720
p=59:  3304 / 3304
```

Thus all sampled public source/target pairs live in one directly traversable public component at each prime.

## Measured fixed baseline — `hga1-p59-L24`

```text
Markoff points / orbit:        3304 / 3304
orbit edge scans:              9912
BFS accepted:                  yes
BFS shortest length:           13
BFS discovered / expanded:     3106 / 2534
BFS edge scans:                7600
BFS equals planted:            no
bounded two-tree accepted:     yes
bounded two-tree length:       13
states discovered / expanded:  3288 / 4596
edge scans:                    13788
bidirectional equals planted:  no
transporter reduced words:     13982
nonempty stabilizer words:     17718
```

The bounded two-tree implementation can do more edge scans than full orbit enumeration because both depth-bounded trees are materialized. This is not evidence of hardness: ordinary BFS already recovers an accepted action with fewer scans than one full orbit traversal.

## Declared 72-instance sweep

Both public navigation attacks succeed on every case:

```text
ordinary BFS accepted:         72 / 72
bounded two-tree accepted:     72 / 72
```

Recovered shortest lengths range only from

```text
2 .. 13
```

across planted bounds `L=8,16,24`.

Equality with the planted word occurs on only

```text
9 / 72
```

cases for either navigation method. The nine matches are confined to the short `L=8` slice (`2/8` for `p=43`, `7/8` for `p=59`); all `L=16` and `L=24` cases recover different accepted words.

Per-set summary:

```text
set            BFS  two-tree  shortest   transporter range    stabilizer range
p29-L8         8/8    8/8       2..8          2..8                 3..8
p29-L16        8/8    8/8       3..10        87..317             276..479
p29-L24        8/8    8/8       7..13     32806..103664        58491..103890
p43-L8         8/8    8/8       4..8          1..4                 0..7
p43-L16        8/8    8/8       3..12        74..382             112..822
p43-L24        8/8    8/8       6..11     28076..30966         29650..59028
p59-L8         8/8    8/8       6..8          1..2                 0..3
p59-L16        8/8    8/8       6..12        43..75               56..106
p59-L24        8/8    8/8       4..13     14765..16138         15946..18068
```

## Reduced-word multiplicity interpretation

Dynamic programming over public states `(point,last_generator)` counts exactly, within the verifier language,

```text
T_L(X,Y) = #{reduced words of length <= L mapping X to Y}
S_L(X)   = #{nonempty reduced words of length <= L mapping X to X}.
```

These are counts of accepted **word representations**, not proven counts of distinct abstract mapping-class-group elements. Different reduced words can induce the same permutation/action.

That distinction does not rescue the construction: direct public navigation already finds an accepted witness on 72/72 cases. The large `L=24` word counts are additional evidence that the verifier relation is weakly binding at the word-representation level.

## Verdict

HGA-R1 is rejected as a hardness direction.

The redesigned binding-action harness behaves as intended:

1. it does **not** demand recovery of the planted action;
2. it accepts any verifier-equivalent transporter as attacker success;
3. it measures public orbit size and accepted-word multiplicity explicitly;
4. it rejects a topology/arithmetic action whose public Schreier graph can simply be traversed.

A successor must therefore change the action space, not increase `p` or planted word length in this same Markoff graph. In particular, scaling a publicly enumerable orbit is not an acceptable repair.

No security claim.
