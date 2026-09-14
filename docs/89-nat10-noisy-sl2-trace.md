# 89 — NAT10 noisy SL(2,p) trace-sketch control

## Status

**NAT10 is a falsification experiment in progress.** NAT9 shows that an exact but lossy coarse `A5` observable hides the planted representation while creating many cheap verifier-equivalent solutions. NAT10 therefore introduces actual bounded noise and a larger matrix-group target while preserving the same equivalent-solution attack semantics.

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

Generation deterministically samples nonidentity matrices until the exact surface relator holds.

The exact matrices are never published and are reference-only after public recovery.

## Noisy public trace sketch

For a fixed public word list, compute the exact modular trace and add bounded noise

```text
y_w = tr(rho(w)) + e_w mod p,
e_w in {-1,0,+1}.
```

The noise radius is fixed at one before measurement. The verifier accepts a recovered representation when the surface relator holds exactly and every recovered trace is within cyclic modular distance one of the public center.

Three parameter sets are fixed:

```text
nat10-p5-G4: p=5, traces A/B/C/D
nat10-p5-X8: p=5, traces A/B/C/D/AB/CD/AC/BD
nat10-p7-X8: p=7, traces A/B/C/D/AB/CD/AC/BD
```

No parameter set is chosen after observing recovery.

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

Raw accepted quadruples include simultaneous-conjugacy copies. To avoid overstating solution multiplicity, NAT10 also records a rigorous lower bound on the number of simultaneous-conjugacy orbits.

For odd `p`, the center `{±I}` of `SL(2,p)` acts trivially by conjugation, so any simultaneous-conjugacy orbit has size at most

```text
|PSL(2,p)| = |SL(2,p)| / 2.
```

Therefore

```text
ceil(accepted quadruples / |PSL(2,p)|)
```

is a public lower bound on the number of inequivalent orbits. This does not require expensive full canonicalization.

## Declared measurement

Run all three parameter sets over eight deterministic seeds. Record:

- generation attempts;
- generator trace-window candidate sizes;
- pair enumeration and pruning;
- relator joins;
- verifier tests;
- accepted-representation multiplicity;
- conjugacy-orbit lower bound;
- first-recovered/planted equality only after public success.

## Rejection gate

Reject a NAT10 parameter set if the trace-filter/relator CSP routinely produces a verifier-accepted representation with small explicit public work, even if the planted representation remains hidden.

Noise is not considered beneficial merely because planted equality becomes rarer. The actual inversion objective is the public verifier.

## Survival gate

Only if increasing `p` and the fixed noisy sketch produces measurable public attack-work growth while accepted-solution multiplicity remains controlled should a successor investigate larger targets or non-exhaustive trace algebra attacks.

No security claim.
