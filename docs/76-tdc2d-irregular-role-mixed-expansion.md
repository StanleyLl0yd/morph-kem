# 76 — TDC2d irregular role-mixed Tanner expansion

## Status

**TDC2d is a falsification experiment in progress.** TDC2c failed because a regular cyclic lift leaves exact equitable fiber classes that 1-WL reconstructs perfectly. TDC2d removes the common lift degree and exact cyclic sheet symmetry before testing low-weight structure.

TDC2d is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Construction

Start from each tetrahedron-free TDC2b base matrix and its degree-matched random control.

For every base check row, choose a deterministic seeded multiplicity in `{2,3}`. Every base variable receives exactly two clones. For each base incidence and each variable clone, connect it to exactly one clone of the corresponding base check using a seeded modular shift.

Consequences:

- there is no single public lift degree;
- check fibers have mixed sizes 2 and 3;
- each public variable column still has weight exactly 3;
- paired variable clones select different check clones, so the construction explicitly rejects duplicate columns;
- all public check and variable labels are globally relabeled.

The same check multiplicities are used for the topology and matched-random bases; incidence shifts are generated independently.

## TDC-A006 first gates

### Public 1-WL / equitable signatures

Run ordinary bipartite role+degree color refinement to stabilization. Record public class-size statistics. For calibration only, compare stabilized classes with planted row/column fibers **after** public refinement to measure whether exact fibers were recovered.

Failure to recover exact fibers is not hardness evidence; it merely means the TDC2c 1-WL shortcut no longer applies verbatim.

### Quotient-free low-weight search

Run the same exact binary kernel search through weight six directly on the expanded public matrices, without recovering any quotient:

- zero / duplicate columns;
- pair-syndrome weight 3/4 search;
- pair/triple collisions for weight 5;
- disjoint triple collisions for weight 6.

The identical search runs on the matched-random irregular expansion.

## Measurements

Record:

- public row/column counts;
- hidden check-multiplicity histogram for calibration;
- public row/column degree histograms;
- color-refinement rounds and class-size histogram;
- singleton and maximum color-class counts;
- post-refinement exact row/column fiber recovery counts;
- first public kernel weight through six and multiplicity;
- pair/triple syndrome collision counts;
- identical matched-random results;
- deterministic all-size/multi-seed curve.

## Gate

Reject TDC2d immediately if irregularity introduces routine bounded low-weight public codewords or if 1-WL still reconstructs most exact fibers cheaply.

If both first gates survive, **do not advance to a security claim**. The next required attacks are 2-WL/equitable pair signatures, explicit quotient/role CSP, automorphism/cover-isomorphism recovery, quotient-free trapping-set search, BP/bit-flipping and OSD/ISD/MITM with matched-random controls.

No security claim.
