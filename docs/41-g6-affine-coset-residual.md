# 41 — G6 affine-coset residual HGES negative control

## Status

**G6 is rejected by A-033.** Exact-head Python 3.12 confirms that the public parity projection leaves exactly four affine candidates at every declared size and exhaustive residual verification recovers one accepted nonlinear witness.

G6 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G5 used nonlinear signed exact-one clauses, but their public parity consequences had full rank and directly reconstructed the unique satisfying phase vector.

G6 asks the next narrower question:

> If the cheap affine quotient is deliberately incomplete, is the remaining nonlinear residual actually difficult?

The calibration chooses a clause family whose projected GF(2) nullity is exactly two at every declared size. Thus the public attacker receives four affine candidates rather than one.

## Construction

Each variable is one independently relabelled `g3-3` gadget with exactly two accepted public perfect-match phases. Canonical public ordering maps the two decompositions to Boolean phase bits.

For `g` gadgets, G6 uses two circulant scope families:

~~~text
(i, i+1, i+2) mod g
(i, i+1, i+5) mod g
~~~

for every `i`, canonicalizing each triple.

Toy sets:

~~~text
g6-12  12 gadgets   24 clauses   72 public tetrahedra
g6-18  18 gadgets   36 clauses  108 public tetrahedra
g6-24  24 gadgets   48 clauses  144 public tetrahedra
~~~

The intended structural controls are:

- `2g` distinct clause scopes;
- variable degree six;
- connected factor graph;
- GF(2) coefficient rank `g-2`;
- GF(2) nullity two;
- exactly four affine phase candidates.

Generation derives hidden reference phases and clause signs deterministically from the master seed so the reference satisfies every signed exact-one clause. Reference phases and local decompositions are not public.

## Public relation

The public verifier is the same nonlinear exact-one verifier used by G5. A witness chooses one accepted G3 matching phase per gadget and every signed three-literal clause must contain exactly one true literal under ordinary integer sum.

Any accepted equivalent witness is attacker success.

## A-033 — affine-coset residual enumeration

A-033 uses only public data:

1. enumerate and canonically order the two accepted G3 matchings for every gadget;
2. project every exact-one clause to its necessary GF(2) equation;
3. Gauss-Jordan reduce the affine system;
4. identify the free columns and enumerate every affine solution;
5. require the declared G6 family to expose nullity two / four affine candidates;
6. evaluate every one of the four phase candidates against **all** public nonlinear exact-one clauses;
7. lift every surviving phase candidate to local matching witnesses;
8. submit survivors to the exact nonlinear verifier;
9. compare to the hidden reference only after public acceptance.

The residual phase scan deliberately evaluates every public clause for every affine candidate rather than stopping at the first violation. This makes the work counter deterministic for the fixed clause family.

## Measured result

Fixed Python 3.12 `g6-24` baseline:

~~~text
gadgets:                               24
total public tetrahedra:              144
clauses:                               48
variable degree histogram:            ((6,24),)
factor components / cycle rank:       1/73
local matching nodes/backtracks:      168/0
projected equations/variables:        48/24
GF(2) rank/nullity:                   22/2
GF(2) row XORs:                       308
affine candidates:                      4
residual nonlinear clause checks:      192
accepted affine candidates:              1
exact verifier clause checks:           48
accepted non-reference candidates:       0
first accepted matches reference:       yes
~~~

Python 3.12 sweep over `g6-12`, `g6-18`, `g6-24` × eight deterministic seeds gives **24/24** instances with nullity two, four affine candidates, exactly one accepted nonlinear candidate, and zero accepted non-reference candidates. Per-size row-XOR work is `92`, `188`, `308`; full residual clause checks are `96`, `144`, `192`.

**Result: G6 rejected by A-033.** The affine quotient is not solver-complete, but its residual is only two bits. Exhaustive enumeration of four candidates is a constant-size public attack. Do not scale `g` while that residual dimension remains fixed.

## G7 gate

A successor must ensure that every cheap quotient leaves a residual search dimension that grows with the generated instance. That residual must then survive exact CSP/SAT, local consistency, low-width dynamic programming, normalization, equivalent-witness enumeration, and generated-role leakage attacks before any trapdoor work.

No security claim.
