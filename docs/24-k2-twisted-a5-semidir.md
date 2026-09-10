# 24 — K2.0 orientation-twisted A5 versus S5

## Status

K2.0 is an algebraic falsification calibration.

It asks whether a non-orientable local system with A5-valued state becomes a new computational relation when orientation-reversing transport acts through the non-trivial outer automorphism of A5.

It is not a KEM, one-way function, trapdoor primitive, or security candidate.

## 1. Prior-art facts

A5 is perfect, but its automorphism group is larger than A5:

~~~text
Aut(A5) ~= S5
Out(A5) ~= C2
~~~

Source:

https://people.maths.bris.ac.uk/~matyd/GroupNames/1/A5.html

The non-trivial extension is:

~~~text
A5 semidirect C2 ~= S5.
~~~

Source:

https://people.maths.bris.ac.uk/~matyd/GroupNames/97/e6/C2byA5.html

For orientation local systems and the orientation double cover, see MIT 18.905:

https://ocw.mit.edu/courses/18-905-algebraic-topology-i-fall-2016/resources/mit18_905f16_lec31/

## 2. Twisted transport

Fix one odd permutation r in S5.

For a in A5 define the orientation-reversing automorphism:

~~~text
alpha(a) = r a r^-1.
~~~

A twisted transport element is a pair:

~~~text
(a, b),  a in A5, b in C2.
~~~

Multiplication is:

~~~text
(a,b)(c,d)
  = (a alpha^b(c), b XOR d).
~~~

K2.0 embeds it into S5 by:

~~~text
Phi(a,b) = a r^b.
~~~

The implementation exhaustively checks all 120 elements and all 14,400 products.

## 3. K1 orientation character

K2.0 reuses exact N4:{6,4}_3 incidence.

Every dual edge has one public orientation bit w_e from the K1 orientation cocycle.

Each face also has an A5 frame x_f.

Generation chooses one A5 three-cycle c_e and constructs an A5 edge label t_e so that the twisted normalized edge value is:

~~~text
(x_g,0)(t_e,w_e)(x_f^-1,0)
    = (c_e,w_e).
~~~

## 4. S5 flattening

Under Phi, the public twisted edge is just one S5 permutation:

~~~text
E_e = Phi(t_e,w_e).
~~~

The A5 face frame becomes an even S5 permutation.

The exact twisted edge predicate is therefore equivalent to the ordinary S5 predicate:

~~~text
Phi(x_g,0) E_e Phi(x_f,0)^-1
    in { Phi(c,w_e) : c in C3 }.
~~~

The orientation bit is simply the parity of E_e.

K2.0 checks this equivalence for every edge and every pair of endpoint A5 frames.

For N4:{6,4}_3 that is:

~~~text
12 edges * 60 * 60 = 43,200
~~~

exact endpoint assignments.

## 5. Why this matters

The non-trivial orientation action is mathematically real.

But if all transport remains 1-dimensional and pairwise, semidirect completion absorbs the twist into one ordinary finite group.

Thus:

- A5 perfectness removes the H1 abelianization shortcut;
- non-orientability adds the C2 outer action;
- together they produce S5, not a new hardness relation.

This is a representation-level structural collapse, stronger than merely saying a SAT solver can encode the instance.

## 6. Exit criterion

Reject naive K2.0 if:

1. Phi is a bijective homomorphism onto S5;
2. the orientation bit equals S5 parity;
3. every public twisted edge predicate exactly matches its flattened S5 predicate.

If rejected, K2 proper must move beyond one group element per edge.

The next admissible direction must use genuinely higher-order 2-cell/face data and must be tested against:

- semidirect-product completion;
- orientation-double-cover reduction;
- crossed-module / 2-group reformulation;
- ordinary finite CSP/SAT extraction;
- Goldreich/local-function flattening;
- homology/cohomology and representation-theoretic projections.

## 7. Security status

No one-wayness, average-case hardness, post-quantum, IND-CPA, IND-CCA, KEM, or production-security claim exists.


## 8. Measured result

Fixed master seed `36026490a1b2c3d4e5f60718293a4b5c`, Python 3.12 CI runner.

~~~text
semidirect audit:
  twisted elements = 120
  S5 image elements = 120
  bijective = true
  homomorphic = true
  multiplication checks = 14,400
  orientation/parity checks = 120
  orientation component equals S5 parity = true

base:
  N4:{6,4}_3 V/E/F = 6/12/4
  orientable = false
  non-zero orientation syndromes = 6/9

exact verifier comparison:
  public dual edges = 12
  endpoint assignments checked = 43,200
  relation mismatches = 0
  public edge parity/orientation matches = 12/12
  planted twisted witness accepted = true
  planted flattened witness accepted = true
~~~

## 9. Disposition

**K2.0 is rejected algebraically.**

This result is stronger than a successful SAT attack: the supposedly new orientation-twisted pairwise relation is literally the same relation after an explicit bijective homomorphism into S5.

The following therefore do not constitute repairs:

- larger non-orientable maps;
- larger numbers of pairwise twisted A5 edges;
- hiding the A5/C2 split in another serialization;
- changing the odd representative r;
- treating S5 parity as secret.

K2.1 must examine genuinely higher-dimensional transport. The novelty bar is high because crossed modules/strict 2-groups and higher gauge theory are established mathematics, and crossed modules have already been proposed for cryptographic key exchange.
