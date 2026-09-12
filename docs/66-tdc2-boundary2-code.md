# 66 — TDC2 non-graphic boundary-2 code control

## Status

**This first TDC2 non-graphic boundary family is rejected by TDC-A003.** Leaving the ordinary graphic cycle-code class removes the T-join reduction, but the simplicial chain complex exposes deterministic weight-four tetrahedron-boundary codewords through `∂2∂3=0`.

TDC2 remains an open research track: issue #122 now requires a successor non-graphic construction in which bounded public 3-cell boundaries do not survive as constant-weight kernel words.

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

## TDC-A003 — higher-dimensional structural attack

The complete 2-skeleton contains all four triangular faces of every public four-vertex set. Their GF(2) boundaries cancel:

```text
∂2(abc + abd + acd + bcd) = 0.
```

Equivalently this is the chain-complex identity `∂2 ∂3 = 0` for an abstract tetrahedron boundary.

The public attack does not need hidden vertex labels after relabeling. It hashes every pairwise column syndrome; two disjoint column pairs with the same syndrome identify a weight-four kernel word. Exact four-column supports are deduplicated. Before weight four, the implementation exhaustively checks for weight-one, weight-two and weight-three codewords.

## Fixed Python 3.12 result

For `tdc2-n8`:

```text
rows / columns:                         28 / 56
topology rank / dimension / rate:      21 / 35 / 0.625000000
row-weight histogram:                  ((6,28),)
column-weight histogram:               ((3,56),)
minimum codeword weight <=3:           none
weight-4 topology codewords:           70
expected tetrahedron boundaries:       C(8,4) = 70
pair-syndrome collision buckets:       210
maximum pair-syndrome bucket:          2
non-graphic column-weight obstruction: yes

matched-random rank / dimension / rate: 28 / 28 / 0.500000000
matched-random weight-4 codewords:       2
matched-random pair-collision buckets:   6
matched-random generation retries:       284
```

The topology-derived code therefore has exact minimum distance `4`: weights 1–3 are absent, and the attack publicly exhibits 70 weight-four kernel words.

## Deterministic sweep

Python 3.12 tested `n=6,7,8` over eight deterministic public relabeling/random-control seeds each.

Topology-derived matrices show the exact same structural law on **24/24** instances:

```text
n=6: rank 10, dimension 10, weight-4 codewords 15 = C(6,4)
n=7: rank 15, dimension 20, weight-4 codewords 35 = C(7,4)
n=8: rank 21, dimension 35, weight-4 codewords 70 = C(8,4)
```

No topology instance has a codeword of weight at most three. Therefore every measured topology code has exact `d_min = 4`.

The degree-matched random controls have the same public row/column counts and exact row/column weight histograms but behave very differently:

- all measured random controls are full row rank (`15/21/28` respectively);
- their dimensions are only `5/14/28`;
- no measured random control has a weight-1/2/3 codeword;
- random weight-four multiplicity ranges only from `0` to `2`, versus deterministic `15/35/70` for the topology family.

This matched-random gap makes the failure specifically attributable to chain-complex structure rather than merely to sparse weight-three columns.

Dedicated TDC2 CI passes on Python 3.11, 3.12 and 3.13; the common exact-head CI also passes.

## Result

**The complete-2-skeleton TDC2 boundary family is rejected by TDC-A003 before decoder work.** It successfully leaves the graphic-code class, but higher-dimensional topology simply moves the forced local kernel relation from triangle weight three to tetrahedron-boundary weight four.

Increasing only `n` cannot repair this family: every four public vertices continue to expose a constant-weight codeword, so the distance remains exactly four.

## Successor gate inside TDC2

Issue #122 remains open. The next non-graphic TDC2 candidate must remove bounded-size public cell-boundary codewords, most naturally through a sparse lift/quotient where base 3-cell boundaries do not project to constant-weight public kernel words. Before interpreting decoding performance it must face:

- exact low-weight kernel search;
- quotient/base-role recovery;
- graphic/cographic/matroid reduction tests;
- Tanner short-cycle analysis;
- BP/bit-flipping;
- bounded OSD/ISD/MITM and generic exact decoding;
- matched-random sparse controls.

No security claim.
