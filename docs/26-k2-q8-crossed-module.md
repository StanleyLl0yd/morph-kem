# 26 — K2.2 Q8 automorphism crossed-module calibration

## Status

K2.2 is an executable falsification experiment for genuinely two-level data.

It is not a KEM, one-way function, trapdoor primitive, or security candidate.

**Disposition: rejected.** The exact public face-lift attack constructs an accepted equivalent witness without the planted representative.

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

It also exhaustively verifies both crossed-module identities: 192 equivariance checks and 64 Peiffer checks.

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

## Measured CI result

Fixed master seed `40226490aabbccddeeff001122334455`, Python 3.12 CI:

~~~text
Q8 order:                         8
Aut(Q8) order:                   24
boundary kernel/image/cokernel:  2/4/6
crossed identity checks:         192/64
crossed identities hold:         true
base V/E/F:                      6/12/4
reference accepted:              true
boundary-image faces:            4/4
nonidentity face curvatures:     4
public fiber sizes:              (2,2,2,2)
equivalent fake-flat witnesses:  16
public attack accepted:          true
edge compositions:               24
Q8 preimage checks:              32
attack equals planted witness:   false
~~~

This is stronger than merely finding another witness: the verifier decomposes exactly into four independent public preimage problems. The attack performs 24 public edge compositions plus 32 Q8 boundary checks and deliberately returns a representative different from the planted one.

## Disposition

**K2.2 is rejected.**

Putting variables on faces is not sufficient to create useful higher-dimensional coupling. For this fake-flatness relation, each face can be solved independently and every solution fiber is exactly a coset of the public kernel `ker(partial) = C2`.

Increasing the number of faces or using a larger cellulation would only multiply independent kernel choices; it would not create a trapdoor.

The next admissible experiment must couple the face lifts through genuinely higher coherence. For this crossed module the remaining ambiguity lives in the abelian kernel C2, so the first mandatory successor attack is a GF(2)/cohomology reduction. Activating a genuine Postnikov-style 3-dimensional constraint likely requires moving from a 2-complex to a 3-complex; that dimensional move must be justified by an exact public/trapdoor relation, not by geometric complexity alone.

## Security status

No one-wayness, average-case hardness, post-quantum security, IND-CPA, IND-CCA, KEM, or production-security claim exists.
