# 58 — TDC0 incidence-derived cycle-code negative control

## Status

**TDC0 calibration succeeds by rejecting the raw incidence-derived cycle code.** Public topology exposes exact weight-three codewords and trivial single-edge syndrome decoding on every measured instance. This validates the first TDC attack gates; it is not evidence that a stronger topology-derived code is hard.

TDC0 is not a KEM, one-way function, post-quantum assumption, or production-security construction.

## Construction

Take the public triangulated torus from the existing surface generator and define a binary cycle code on public edges. The parity-check matrix is the public vertex-edge incidence matrix over GF(2).

A binary edge vector is a codeword exactly when every public vertex has even selected-edge degree.

Toy sets:

- `tdc0-4x4`;
- `tdc0-6x6`;
- `tdc0-8x8`.

For an `r x c` torus:

```text
V = rc
E = 3rc
F = 2rc
rank(H) = V - 1
k = E - rank(H) = 2rc + 1
```

## TDC-A001 calibration break

### Weight-three codewords

Every public triangle boundary contains exactly three public edges and has even incidence at all three vertices. It is therefore a weight-three codeword.

Because the public graph is simple, no nonzero cycle-code word can have weight one or two. Thus the code has exact minimum distance

```text
d_min = 3.
```

This is direct structural leakage from the topology, not a decoder artifact.

### Single-edge syndrome lookup

A one-edge error has syndrome equal to its two public endpoints. Since the public graph has no parallel edges, every edge has a unique weight-two syndrome. A public lookup table with one entry per edge therefore recovers every planted one-edge error exactly.

Reference data is used only after the public recovery has already succeeded.

## Measured result

Exact Python 3.12 fixed `tdc0-8x8`:

```text
public V/E/F:                    64/192/128
parity rank:                     63
code dimension:                 129
code rate:                      0.671875
row weight histogram:           ((6,64),)
column weight histogram:        ((2,192),)
public triangle codewords:      128
triangle word weight histogram: ((3,128),)
exact minimum distance:         3
single-edge syndrome weight:    2
single-edge lookup entries:     192
public recovery accepted:       yes
matches reference after success: yes
```

Python 3.12 sweep over all three sets × eight deterministic seeds gives **24/24** exact structural failures:

- `tdc0-4x4`: `V/E/F=16/48/32`, rank `15`, dimension `33`, rate `0.6875`, `32` public weight-three triangle codewords, lookup size `48`;
- `tdc0-6x6`: `36/108/72`, rank `35`, dimension `73`, rate `0.675925926`, `72` public weight-three triangle codewords, lookup size `108`;
- `tdc0-8x8`: `64/192/128`, rank `63`, dimension `129`, rate `0.671875`, `128` public weight-three triangle codewords, lookup size `192`.

Every run has exact `d_min=3`, syndrome weight two for the planted one-edge error, accepted public recovery, and post-success reference match.

The dedicated TDC0 workflow passes on Python 3.11, 3.12 and 3.13.

## Result

**TDC0 is rejected as intended.** A raw surface cycle space is unsuitable as a candidate decoding foundation: the topology itself publishes a large family of constant-weight codewords and a one-error decoder with a direct public lookup.

The lesson is narrower than “topological codes are easy”: TDC1 must alter the code construction so bounded-size cells do not automatically become bounded-weight codewords, and it must be compared against matched random sparse ensembles rather than judged in isolation.

## Next TDC gate

TDC1 must stop using a raw surface cycle space as the code. A stronger candidate should obscure or remove constant-weight topological cycles and must be compared against matched random sparse matrices for rate, distance, low-weight multiplicity, decoding curves, automorphisms, separators and quotient/cover leakage.

A natural next control is a lifted/cover-derived sparse parity-check ensemble in which local cells no longer directly define codewords. The first attacks remain cover recovery, automorphism detection, low-weight search, sparse decoding and matched-random comparison.

No security claim.
