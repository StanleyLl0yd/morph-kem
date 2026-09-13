# 73 — TDC2c variable-degree cyclic Tanner lift

## Status

**TDC2c is rejected by TDC-A005 as a hidden-quotient construction.** A genuine cyclic lift removes the direct public base labels, but ordinary public color refinement reconstructs the exact fiber partition on every measured topology and matched-random lift. The recovered topology quotient immediately exposes the already-measured weight-six base relation.

TDC2c is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Construction

Take a generated TDC2b edge/triangle Tanner graph as a base. Replace every base incidence edge by one cyclic translation matching on `L` sheets. Declared toy sets are:

```text
tdc2c-n8-L2
tdc2c-n9-L3
tdc2c-n10-L4
```

Every lifted variable still has column weight three. Lifted row/column labels are independently globally permuted after construction.

The same lift construction is applied independently to the TDC2b degree-matched random sparse control.

## TDC-A005 attack 1 — public color-refinement quotient

The public Tanner graph is attacked without planted fiber labels. Initial colors contain only bipartite role and degree. Standard iterative color refinement replaces each node color by its previous color plus the multiset of neighbor colors until stabilization.

A candidate fiber partition is accepted only when every stabilized color class has exactly `L` nodes on one bipartite side. The induced quotient is then verified exactly:

- every lifted variable in one class sees the same quotient check classes;
- every quotient incidence contains exactly `L` lifted incidences;
- every quotient variable retains column weight three.

No planted fiber map is used by the recovery.

## TDC-A005 attack 2 — inherited base words

On the recovered quotient, search publicly for a kernel support through weight six. For every quotient support `S`, select **all** `L` lifted variable clones in the recovered fiber classes of `S` and recompute the full public lifted syndrome.

For a quotient kernel word this all-fiber selection has weight

```text
L * |S|.
```

A recovered topology quotient weight-six word therefore gives public lifted words of weight `12`, `18`, or `24` for `L=2,3,4` respectively.

Because `L` is varied, this is **not** described as a constant-distance theorem. The fatal result here is that the purportedly hidden base quotient is public under a very weak refinement attack.

## Fixed Python 3.12 result

For `tdc2c-n10-L4`:

```text
lifted rows / columns:                   180 / 272
lift degree:                             4

topology color rounds:                  5
topology stabilized classes:            113 classes, all size 4
topology recovered quotient rows/cols:  45 / 68
topology exact fiber partition:          yes
topology quotient verified:              yes
topology quotient kernel weight <=6:     6
topology lifted inherited weight:        24
topology lifted syndrome verified:       yes

random color rounds:                    5
random stabilized classes:              113 classes, all size 4
random exact fiber partition:            yes
random quotient verified:                yes
random quotient kernel weight <=6:       6
random lifted inherited weight:          24
random lifted syndrome verified:         yes
```

The fixed matched-random base happens to contain a weight-six word; the multi-seed comparison below separates that event from the topology law.

## Eight-seed / multi-lift sweep

Across three parameter sets × eight seeds there are **24 topology lifts** and **24 matched-random lifts**.

Measured Python 3.12 result:

- public color refinement recovers an exact size-`L` fiber partition on **24/24 topology lifts**;
- it also recovers exact fibers on **24/24 matched-random lifts**;
- every recovered partition passes exact public quotient-cover verification;
- stabilization takes only **4–6 rounds**;
- all stabilized color classes have size exactly the declared lift degree;
- **24/24 topology quotients** contain a weight-six kernel word;
- the corresponding all-fiber lifted support verifies publicly on **24/24**, with weight exactly `12`, `18`, or `24`;
- only **8/24 matched-random quotients** contain any kernel word through weight six in this sweep;
- whenever a matched-random quotient word exists, its all-fiber lift also verifies, as expected for a genuine cover.

Thus the cyclic cover itself is not what creates the topology low-weight relation. The public cover quotient faithfully exposes whether that relation was already present in the base.

## Interpretation

TDC2c fails as a hidden-base/lift architecture: global relabeling does not conceal the base roles because 1-dimensional color refinement alone recovers every fiber.

This result does **not** claim that weights `12/18/24` prove constant distance as lift degree grows. The inherited word weight scales as `6L`. A future lift could only be interesting if the quotient/fibers cease to be publicly recoverable and quotient-free decoding structure is then tested directly.

Making only `L` larger is not a repair for this cyclic construction while the equitable color classes remain exact fibers.

## Successor gate

A TDC successor must first destroy cheap fiber-role recovery—for example by using a non-regular/non-cyclic lift or by mixing roles in a way that does not leave exact equitable classes—then immediately face:

- stronger equitable-partition / Weisfeiler-Leman attacks;
- automorphism and covering-isomorphism recovery;
- quotient CSP / graph-isomorphism attacks;
- quotient-free low-weight and trapping-set search;
- Tanner girth/short-cycle measurements;
- BP / bit-flipping and OSD / ISD / MITM;
- matched-random controls.

No trapdoor primitive, KEM, one-wayness, post-quantum, IND-CPA/CCA, or production-security claim exists.
