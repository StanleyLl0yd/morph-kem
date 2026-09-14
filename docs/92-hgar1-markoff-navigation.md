# 92 — HGA-R1 finite Markoff action navigation negative control

## Status

**HGA-R1 is a predeclared negative-control falsification experiment.** It calibrates the post-NAT binding-action interface from `docs/91-hga0-binding-action-survey.md` on a topology/arithmetic action expected to be publicly navigable.

The `R` suffix is deliberate. The repository already preserves the historical HGA1 Heisenberg/Nielsen negative control and its workflow. HGA-R1 is the first experiment in the redesign line; it does not replace or reinterpret the historical HGA0/HGA1 corpus.

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

Before measurement:

```text
p in {29,43,59}
L in {8,16,24}
8 deterministic seeds per (p,L)
```

This is exactly 72 instances. No prime, word bound, seed count or attack budget may be changed after inspecting recovery results.

Implementation parameter IDs retain the compact `hga1-pXX-LYY` spelling inside the isolated Markoff module, but the experiment name and workflow are **HGA-R1** to avoid collision with the preserved historical HGA1 Heisenberg experiment.

## HGA-R-A001 — public navigation attacks

### Ordinary shortest BFS

Run deterministic BFS from `X` on the public generator graph, stopping when `Y` is first discovered or depth `L` is exhausted. Record:

- states discovered;
- states expanded;
- generator-edge scans;
- recovered shortest length;
- verifier result.

### Bidirectional BFS

Build public bounded BFS trees from `X` and `Y`, using radii

```text
ceil(L/2)
floor(L/2)
```

and choose an intersection minimizing total public depth. Because the generators are involutions, the right half is traversed back with the same labels. Adjacent equal labels created at the join are publicly cancelled before verification.

Record the same work metrics.

### Full public orbit

Independently enumerate the connected component of `X`. This provides a direct scale comparison for navigation work; orbit enumeration is not needed for verifier acceptance.

## Reduced-word multiplicity

Dynamic programming over public states `(point,last_generator)` counts exactly, within the verifier language,

```text
T_L(X,Y) = #{reduced words of length <= L mapping X to Y}
S_L(X)   = #{nonempty reduced words of length <= L mapping X to X}.
```

These are counts of accepted **word representations**. They are not claimed to be counts of distinct abstract mapping-class-group elements because different reduced words can induce the same permutation/action.

This distinction is mandatory: multiplicity is evidence about verifier binding, not a group-presentation theorem.

## Rejection gate

Reject HGA-R1 as a hardness direction if ordinary or bidirectional public graph navigation routinely recovers an accepted action with work on the scale of the small public orbit, independent of planted-word equality.

Large `T_L` or `S_L` is additional negative evidence. Rejection does not require proving transporter multiplicity large if direct public navigation already succeeds cheaply.

## Calibration expectation

The experiment is expected to reject. If the declared 72-instance sweep does not show routine public recovery, first inspect implementation and verifier semantics before interpreting the outcome as evidence of hardness.

A rejection is useful: it demonstrates that the redesigned binding-action harness catches a topology/arithmetic action whose public orbit graph remains directly navigable.

No security claim.
