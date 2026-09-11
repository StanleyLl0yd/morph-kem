# 57 — HGA0 hidden-action trivialization controls

## Status

**HGA0 is an attack-harness calibration in progress.** The two families in this document are deliberately weak and must be rejected publicly before any less trivial hidden-action candidate is interpreted.

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

This control must be rejected immediately because the public representation is faithful and linear:

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

## HGA-A001 calibration gate

The harness must show across deterministic multi-seed sweeps that:

1. the linear control is recovered exactly with one XOR;
2. the dihedral control is recovered by at most `2n` tested group elements;
3. the recovered public element verifies without reference data;
4. reference comparison is performed only after public success;
5. the dihedral public stabilizer remains one for the generated controls.

If these deliberately weak families do not fail deterministically, HGA0 must not proceed to more interesting geometric actions.

## Next HGA candidate gate

After calibration, HGA1 should test a nontrivial action whose public endpoints do not admit either:

- a faithful low-dimensional linear quotient recovering the action, or
- a small canonical orbit search / short normal form.

Candidate families remain subject to canonicalization, stabilizer/equivalent-secret multiplicity, quotient representations, abelianization, MITM/BFS, generated-role leakage and quantum hidden-shift/subgroup screening.

No security claim.
