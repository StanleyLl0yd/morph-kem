# 26 — K2.2 Q8 automorphism crossed-module calibration

## Status

K2.2 is an executable falsification experiment for genuinely two-level data.

It is not a KEM, one-way function, trapdoor primitive, or security candidate.

## Crossed module

The experiment uses the automorphism crossed module of the quaternion group:

~~~text
partial: Q8 -> Aut(Q8)
partial(q) = conjugation by q
~~~

with the natural action of Aut(Q8) on Q8.

The implementation constructs Q8 and all automorphisms directly and checks:

~~~text
|Q8| = 8
|Aut(Q8)| = 24
|ker(partial)| = 2
|im(partial)| = 4
|coker(partial)| = 6
~~~

It also exhaustively verifies both crossed-module identities.

References:
- GroupNames Q8: https://people.maths.bris.ac.uk/~matyd/GroupNames/1/Q8.html
- GAP XMod automorphism crossed modules: https://gap-packages.github.io/xmod/doc/chap2_mj.html

## Public 2-dimensional relation

The cell scaffold is exact N4:{6,4}_3.

Every primal edge carries an Aut(Q8) transport. For each hexagonal face f, the oriented boundary labels define a public holonomy H_f in Aut(Q8).

A face witness h_f in Q8 is accepted when:

~~~text
partial(h_f) = H_f.
~~~

Generation constructs edge labels so every H_f belongs to im(partial) and at least one face has non-identity curvature.

The planted h_f values are reference data only.

## Public attack

For each face independently:

1. compute H_f from public edge labels;
2. enumerate the eight Q8 elements;
3. collect every h with partial(h)=H_f;
4. choose any one public preimage.

Every non-empty boundary fiber is a coset of ker(partial), hence has two elements in this crossed module.

With four faces, fake-flatness alone therefore admits:

~~~text
2^4 = 16
~~~

equivalent face-lift witnesses.

The attack does not need the planted representative.

## Exit criterion

If CI confirms four independent fibers of size two and an accepted public lift, K2.2 is rejected.

The intended lesson is that putting variables on faces is not enough: fake-flatness alone may decompose into independent boundary-preimage problems.

A successor would need genuine coupling between face variables — for example a higher coherence/Postnikov/3-cell-style relation — and must still survive ordinary CSP/SAT and cohomological flattening attacks.

## Security status

No one-wayness, average-case hardness, post-quantum security, IND-CPA, IND-CCA, KEM, or production-security claim exists.
