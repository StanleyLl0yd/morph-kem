# 85 — TDC2g common random parity-overlay control

## Status

**TDC2g survives TDC-A009's predeclared rank + bounded-low-weight gate on the largest measured toy family.** The old TDC2f `n10` topology excess (`8/32` versus `0/32` through weight eight) disappears after adding six common topology-independent random parity rows that are accepted only when they raise the rank of both paired matrices.

This is **not** a cryptographic hardness result. It is permission to proceed to matched decoding-work experiments for this toy ensemble.

TDC2g is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Construction

Start from a paired TDC2f topology/control instance. Both public matrices already have identical column count and rank.

Then sample a deterministic topology-independent sequence of binary parity rows over the public column coordinates. A candidate row is accepted only if it is linearly independent of the existing row space in **both** paired matrices. The exact same accepted row is appended to topology and control.

The generator adds exactly six such common rows.

This guarantees:

- the same rank increment in both families;
- identical final rank/dimension/rate inside each pair;
- no query to low-weight search, Tanner statistics, decoder output, or attack success;
- no per-instance rejection based on whether a weight-seven/eight word survives.

The only rejection condition is the declared algebraic requirement that the next common row raise both public ranks.

## TDC-A009 measurements

### Fixed Python 3.12 `tdc2g-n10`

```text
base / final rank:                 36 / 42
extra rows / overlay attempts:       6 / 6
rank profiles equal:                   yes
dimension profiles equal:              yes

public rows / columns:              42 / 68
rank / dimension / rate:       42 / 26 / 0.382353

topology minimum <=6:                  none
topology minimum <=8:                  none
random minimum <=6:                    none
random minimum <=8:                    none

topology Tanner four-cycles:         105388
random Tanner four-cycles:           116030
```

The common overlay therefore lowers the fixed n10 rate from the TDC2f regime to about `0.382353`. That cost is explicit and is a major reason this stage is only a diagnostic repair control.

### Eight-seed all-size sweep

Presence of a public kernel word of weight at most eight:

```text
size   topology   matched random
n8        1/8          0/8
n9        1/8          0/8
n10       0/8          0/8
```

The two surviving topology words occur at:

- `n8`, seed 1: weight 7;
- `n9`, seed 6: weight 8.

They do not form the growing largest-size excess seen in TDC2f. Rank and dimension profiles match on all 24 paired instances.

### Predeclared extended `n10 × 32` screen

Without changing the generator, six-row overlay, matrix dimensions, search bound, or attack logic:

```text
public kernel weight <=8:
  topology:             0 / 32
  matched random:       0 / 32
```

All 32 pairs retain exact rank/dimension equality. Thus the specific TDC2f n10 low-weight distinguisher does not survive this structural repair on the declared screen.

## Interpretation

TDC2g provides the first TDC stage in this lineage that **survives its predeclared cheap algebraic + bounded-low-weight gate at the largest tested size**.

The correct conclusion is narrow:

- TDC2f's n10 `<=8` excess was not robust to six common random parity constraints;
- the repair does not use per-instance attack-positive rejection;
- the paired controls remain rank/dimension/rate matched;
- the largest measured topology/control distributions are not separated by the declared exact search through weight eight.

The result does **not** show that topology-derived decoding is hard, that the code has cryptographic distance, or that the overlay construction is a good KEM candidate.

## Important limitation

Random parity overlays can buy distance by spending rate. Here six rows reduce the fixed n10 dimension from the TDC2f regime to 26 and the rate to about `0.382353`. Adding enough constraints would trivially drive any code toward a low-rate/high-distance regime.

Therefore the next stage must compare **decoding work at the matched final rate and error distribution**, not celebrate the disappearance of short words.

## Successor gate

Advance to a matched decoder-work control with the same public TDC2g paired ensemble. Predeclare and compare:

- belief propagation / bit flipping;
- bounded OSD;
- bounded ISD / meet-in-the-middle syndrome decoding;
- identical error-weight/rate curves on topology and controls;
- decoder failure/success rates and explicit work counters;
- a larger-size or larger-seed confirmation before interpreting any separation.

Any equivalent error/coset representative accepted by the public syndrome is attacker success.

Survival of decoder-work gates would still be toy evidence only. No security claim.