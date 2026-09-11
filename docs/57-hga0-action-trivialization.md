# 57 — HGA0 hidden-action trivialization controls

## Status

**HGA0 calibration succeeds by rejecting both deliberately weak action families.** The public trivialization harness recovers every generated control instance across the measured sweep. This validates the first HGA attack gates; it is not evidence that a stronger HGA candidate is hard.

HGA0 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Architectural pivot

HGES G0–G22 treats a secret as an exact structural witness. That line repeatedly fails because public topology supplies equivalent accepted witnesses or collapses to ordinary graph/algebra/CSP structure.

HGA changes the primitive shape. A secret now acts on a public object:

```text
s <- SecretSample
x <- ObjectSample
y <- Act(s, x)
```

The attack target is any equivalent public action taking `x` to `y`. Merely hiding one particular action word is not enough.

## Control A — GF(2) translation action

Public objects are `n`-bit vectors. The secret is a sparse translation mask `s` and

```text
y = x XOR s.
```

This control is rejected immediately because the public representation is faithful and linear:

```text
s = x XOR y.
```

The attack therefore uses one XOR operation and recovers the exact action element.

Toy sets:

- `hga0-linear-8`, secret weight 3;
- `hga0-linear-16`, secret weight 5;
- `hga0-linear-24`, secret weight 7.

This is the HGA analogue of a quotient/abelianization failure.

## Control B — dihedral polygon action

The public object is a cyclic ordering of unique labels. The secret is an element of the dihedral group: rotation plus optional reflection.

The public attacker enumerates all `2n` elements, applies each to the public source ordering, and selects the unique element matching the public target ordering. Because labels are unique, the public stabilizer has size one.

Toy sets:

- `hga0-dihedral-9`;
- `hga0-dihedral-17`;
- `hga0-dihedral-25`.

This control represents a candidate family with a tiny canonical normal-form/orbit search.

## Measured HGA-A001 calibration

Exact Python 3.12 fixed baseline:

```text
linear parameters:                         hga0-linear-24
linear dimension:                          24
linear recovered word weight:              7
linear representation rank:                24
linear XOR operations:                     1
linear accepted:                           yes
linear matches reference after success:    yes

dihedral parameters:                       hga0-dihedral-25
dihedral polygon size:                     25
dihedral candidate elements tested:        50
dihedral label checks:                     75
dihedral matching elements:                1
dihedral stabilizer size:                  1
dihedral recovered element:                rotation=8, reflected=0
dihedral accepted:                         yes
dihedral matches reference after success:  yes
```

Python 3.12 deterministic sweep covers all six toy sets × eight seeds:

- linear controls: **24/24** exact public recoveries with exactly one XOR; recovered weights are always the configured `3/5/7`;
- dihedral controls: **24/24** exact public recoveries; sizes `9/17/25` require exactly `18/34/50` tested group elements and `27/51/75` label checks respectively;
- every dihedral instance has exactly one matching public action element and stabilizer size one;
- all **48/48** recovered actions verify, and all match the generation reference only in post-success comparison.

The dedicated HGA0 workflow passes on Python 3.11, 3.12 and 3.13.

## Result

**Both HGA0 controls are rejected as intended.** The calibration establishes two mandatory kill-gates for future hidden-action candidates:

1. a faithful low-dimensional public representation that exposes the acting element is fatal;
2. a small public orbit with a canonical/cheap normal-form search is fatal.

A later HGA candidate receives no positive interpretation unless both attacks fail for structural reasons rather than parameter size.

## Next HGA candidate gate

HGA1 should test a nontrivial nonabelian action whose public endpoints do not admit either:

- a faithful low-dimensional linear quotient recovering the action, or
- a small canonical orbit search / short normal form.

A suitable first control is a Nielsen/automorphism action on a small nonabelian representation tuple, with mandatory attacks through abelianization, trace/character-style invariants where available, quotient representations, stabilizers, and meet-in-the-middle endpoint recovery.

Candidate families remain subject to canonicalization, stabilizer/equivalent-secret multiplicity, quotient representations, abelianization, MITM/BFS, generated-role leakage and quantum hidden-shift/subgroup screening.

No security claim.
