# 66 — TDC2 non-graphic boundary-2 code control

## Status

**TDC2 is a falsification experiment in progress.** It leaves the ordinary graphic cycle-code class before any more elaborate lifted-2-complex construction is interpreted.

TDC2 is not a KEM, one-way function, post-quantum assumption, or production-security construction.

## Construction

Take the complete 2-skeleton on `n` public vertices. Binary code variables are public triangles and parity checks are public edges. The parity-check matrix is the simplicial boundary operator

```text
∂2 : C2 -> C1
```

over GF(2): every triangle column contains exactly its three boundary edges.

Toy sets:

```text
tdc2-n6: rows C(6,2)=15, columns C(6,3)=20
tdc2-n7: rows 21, columns 35
tdc2-n8: rows 28, columns 56
```

Independent public row and column relabelings remove lexicographic generation labels.

This family is **not an ordinary binary graph-incidence code**: every nonzero column has weight three, whereas a graph vertex-edge incidence matrix has column weight two. Row/column permutations preserve that obstruction.

## Higher-dimensional structural attack

Leaving the graphic class is not enough. The complete 2-skeleton contains all four triangular faces of every public four-vertex set. Their GF(2) boundaries cancel:

```text
∂2(abc + abd + acd + bcd) = 0.
```

Equivalently this is the chain-complex identity `∂2 ∂3 = 0` for the abstract tetrahedron boundary.

Therefore every public four-vertex set immediately gives a weight-four codeword. The structural hypothesis is

```text
d_min = 4,
```

with exactly `C(n,4)` tetrahedron-boundary codewords at weight four.

The implementation does not rely on hidden vertex labels to count these words after relabeling. It builds all pairwise column syndromes; two disjoint column pairs with the same syndrome identify a weight-four kernel word. Exact four-column supports are deduplicated publicly.

Before weight four, the attack also checks exhaustively for weight-one, weight-two and weight-three codewords.

## Matched-random sparse control

For every topology-derived matrix, generation constructs a random simple bipartite incidence matrix with exactly the same:

- row count;
- column count;
- row degree `n-2`;
- column degree `3`.

The random generator uses explicit bounded rejection, records retries, requires distinct weight-three columns, and requires connected Tanner incidence.

The matched-random control is used only to separate generic sparse-matrix low-weight effects from the deterministic chain-complex leakage.

## Measurements

Record at least:

- row/column counts;
- exact rank/dimension/rate;
- row/column weight histograms;
- explicit non-graphic column-weight obstruction;
- minimum codeword weight if at most three;
- exact number of weight-four codewords;
- number/max-size of colliding pair-syndrome buckets;
- theoretical tetrahedron-boundary count `C(n,4)`;
- matched-random rank/dimension and low-weight counts;
- random-generation retries;
- deterministic all-size / multi-seed sweep.

## Rejection gate

If the topology-derived matrix has deterministic weight-four tetrahedron-boundary codewords across the generated distribution, **reject this TDC2 boundary family before decoder work**. A higher-dimensional construction that merely moves the forced local codeword from weight three to weight four has not created a useful distance mechanism.

Do not repair by increasing only `n` while every four public vertices still expose the same local kernel relation.

## Successor gate

A further non-graphic TDC candidate must remove bounded-size public cell-boundary codewords, for example through a sparse lift or quotient in which base 3-cell boundaries do not survive as constant-weight public kernel words. It must then face quotient recovery, low-weight search, BP/bit-flipping, OSD/ISD/MITM and matched-random decoding.

No security claim.
