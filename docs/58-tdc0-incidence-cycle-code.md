# 58 — TDC0 incidence-derived cycle-code negative control

## Status

**TDC0 is an attack-harness calibration in progress.** The first family is intentionally transparent and should be rejected because public topology exposes very low-weight codewords and trivial single-edge syndrome decoding.

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

Two public failures are deliberate.

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

## Calibration gate

Across all toy sizes and deterministic public relabeling seeds, require:

- rank `V-1`;
- `F` public triangle codewords of weight three;
- exact `d_min = 3`;
- column weight exactly two for every edge;
- every planted single-edge error recovered from public syndrome;
- post-success equality with reference.

If any of these expected breaks fails, the TDC harness is not ready for stronger code families.

## Next TDC gate

TDC1 must stop using a raw surface cycle space as the code. A stronger candidate should obscure or remove constant-weight topological cycles and must be compared against matched random sparse matrices for rate, distance, low-weight multiplicity, decoding curves, automorphisms, separators and quotient/cover leakage.

No security claim.
