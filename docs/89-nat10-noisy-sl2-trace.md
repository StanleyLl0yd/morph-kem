# 89 — NAT10 noisy SL(2,p) trace-sketch control

## Status

**NAT10 is rejected by NAT-A012 on the declared toy distribution.** Bounded noisy trace sketches hide the planted exact `SL(2,p)` representation, but the public verifier admits very large families of alternative representations that a direct trace-window / surface-relator CSP recovers on every declared instance.

NAT10 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Hidden residual representation

Use the genus-two surface presentation

```text
<a,b,c,d | [a,b][c,d] = 1>
```

with a hidden quadruple

```text
A, B, C, D in SL(2, F_p).
```

Generation deterministically samples nonidentity matrices until the exact surface relator holds. The exact matrices are never published and are reference-only after public recovery.

## Noisy public trace sketch

For a fixed public word list, compute the exact modular trace and add bounded noise

```text
y_w = tr(rho(w)) + e_w mod p,
e_w in {-1,0,+1}.
```

The noise radius is fixed at one before measurement. The verifier accepts a recovered representation when the surface relator holds exactly and every recovered trace is within cyclic modular distance one of the public center.

The three predeclared parameter sets are

```text
nat10-p5-G4: p=5, traces A/B/C/D
nat10-p5-X8: p=5, traces A/B/C/D/AB/CD/AC/BD
nat10-p7-X8: p=7, traces A/B/C/D/AB/CD/AC/BD
```

No parameter set was selected after observing recovery.

## NAT-A012 public attack

The attack receives only `(p, radius, noisy trace centers)`.

1. Enumerate `SL(2,p)` exactly for toy calibration.
2. Filter each generator candidate set by its noisy trace window.
3. Enumerate `(A,B)` pairs, applying the `AB` trace window when published, and compute `[A,B]`.
4. Enumerate `(C,D)` pairs, applying `CD`, and bucket them by `[C,D]`.
5. Join pairs requiring `[C,D]=[A,B]^-1`.
6. Apply `AC` and `BD` noisy trace windows when published.
7. Run the exact public noisy verifier on every survivor.
8. Count every verifier-accepted representation.

Any accepted representation is attacker success. Equality with the planted quadruple is reference-only.

## Simultaneous-conjugacy multiplicity

Raw accepted quadruples include simultaneous-conjugacy copies. For odd `p`, the center `{±I}` of `SL(2,p)` acts trivially by conjugation, so any simultaneous-conjugacy orbit has size at most

```text
|PSL(2,p)| = |SL(2,p)| / 2.
```

Therefore

```text
ceil(accepted quadruples / |PSL(2,p)|)
```

is a rigorous public lower bound on the number of inequivalent simultaneous-conjugacy orbits.

## Fixed `nat10-p7-X8` baseline

The declared fixed baseline produced

```text
prime / group size:                 7 / 336
noise radius:                       1
generation attempts:                1044
generator candidate sizes:          147 / 147 / 147 / 146
left pairs considered / retained:   21609 / 9709
right pairs considered / retained:  21462 / 8442
relator join candidates:            269346
verifier candidates tested:         62202
accepted representations:           62202
conjugacy-orbit lower bound:         371
public recovery:                     yes
first recovered equals planted:      no
```

Thus even after all eight noisy trace constraints, one small public CSP produces tens of thousands of verifier-accepted quadruples and at least hundreds of inequivalent simultaneous-conjugacy orbits.

## Declared three-set × eight-seed sweep

All 24 declared instances were publicly inverted:

```text
set             recovery   first=planted   accepted reps / seed    orbit lower bound / seed
nat10-p5-G4       8/8          0/8           278580 .. 678321       4643 .. 11306
nat10-p5-X8       8/8          0/8            23520 ..  86760        392 ..  1446
nat10-p7-X8       8/8          0/8            46032 .. 134484        274 ..   801
```

Aggregate accepted-representation counts were

```text
nat10-p5-G4: 3,276,783
nat10-p5-X8:   455,340
nat10-p7-X8:   692,524
```

Overall public recovery is **24/24** and the first recovered representation equals the planted quadruple on **0/24**.

Increasing from `p=5` to `p=7` does increase raw pair/join work, but it does not control verifier-equivalent multiplicity: the strongest declared `p7-X8` sketch still leaves at least 274–801 inequivalent orbits per seed under the rigorous lower bound.

## Interpretation

NAT10 falsifies the idea that simply adding bounded noise to a lossy residual representation fixes NAT9. The noise does hide the planted exact representation, but the verifier itself becomes permissive enough that finding *some* accepted representation remains easy on the toy instances.

This is a stronger failure than planted-recovery failure alone: even after quotienting by simultaneous conjugation, the accepted-solution set remains provably large.

A successor must therefore change the semantics, not merely enlarge `p`, increase the word list, or widen/narrow the same trace windows. Any future noisy residual construction must predeclare and measure both attacker work and verifier-equivalent solution multiplicity. If multiplicity grows with noise, that is attacker freedom, not evidence of hardness.

No security claim.
