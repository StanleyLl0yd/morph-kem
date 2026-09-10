# 25 — K2.1 crossed-module / finite-2-group frontier

## Status

K2.1 is a literature, algebraic-structure, and public-key-interface gate.

It does **not** introduce an executable cryptosystem.

The immediate question after K2.0 is:

> if pairwise orientation-twisted A5 transport is only S5, can genuinely two-dimensional transport on edges **and** faces create a distinct computational relation with a trapdoor?

The answer is not currently known. What is known is that the algebraic language itself is established and already has cryptographic prior art.

## 1. Why crossed modules are the natural next language

A strict 2-group can be represented by a crossed module:

~~~text
partial: E -> G
~~~

together with an action of G on E satisfying the crossed-module / Peiffer identities.

In higher gauge theory, this allows two levels of transport:

- G-valued data on edges;
- E-valued data on faces;
- compatibility between a face value and the product of its boundary edge values.

This is genuinely different from K2.0's one-group-element-per-edge model.

Sources:

- Baez & Schreiber, *Higher Gauge Theory*:
  https://arxiv.org/abs/math/0511710

- Bullivant, Faria Martins & Martin, finite 2-group higher gauge theory:
  https://intlpress.com/site/pub/files/_fulltext/journals/atmp/2019/0023/0007/ATMP-2019-0023-0007-a001.pdf

- Bochniak et al., *Study of a lattice 2-group gauge model*:
  https://arxiv.org/abs/2109.12097

## 2. This is not a new mathematical object

Crossed modules are classical algebraic-topology objects and models of homotopy 2-types.

A modern overview:

https://arxiv.org/abs/2403.15900

For a crossed module, the basic 2-type invariants are:

~~~text
pi1 ~= coker(partial)
pi2 ~= ker(partial)
~~~

and ker(partial) is abelian while im(partial) is normal.

A source explicitly recording the kernel/image facts and associated exact sequence:

https://pure.mpg.de/rest/items/item_3505925_5/component/file_3551727/content

The crossed module also carries the familiar Postnikov / H^3 layer. A classical account records a class:

~~~text
k_M in H^3(coker(partial), ker(partial)).
~~~

Source:

https://archive.intlpress.com/site/pub/files/_fulltext/journals/hha/1999/0001/0001/HHA-1999-0001-0001-a001.pdf

Therefore a candidate that merely renames ker, coker, an action, or a Postnikov class as a "secret topology" is not a new hardness assumption.

## 3. Crossed modules already have cryptographic prior art

Inassaridze and Khmaladze proposed a public-key-exchange framework based on "one-way crossed modules of groups":

https://iverieli.nplg.gov.ge/bitstream/1234/355832/1/AndriaRazmadzisMatematikisInstitutisShromebi_2019_Tomi-173_N2.pdf

The note presents the general framework and says concrete candidate one-way crossed modules are to be supplied separately.

For MORPH this means:

- "use a crossed module" is not a novelty claim;
- "one-way crossed module" cannot be used as an assumption without an exact generated distribution and attack model;
- a public-key interface must be demonstrated independently.

## 4. Immediate structural rejection matrix

Before any code, candidate crossed modules fall into several easy-to-classify buckets.

### 4.1 partial is an isomorphism

Then:

~~~text
ker(partial) = 1
coker(partial) = 1
~~~

so the represented 2-type is trivial.

A larger presentation does not create higher homotopy information.

### 4.2 partial is injective

Then:

~~~text
pi2 = ker(partial) = 1.
~~~

The genuinely 2-dimensional homotopy layer disappears. The remaining invariant is the ordinary quotient group coker(partial).

This case should be treated first as a group/extension problem, not as a new 2-dimensional hardness source.

### 4.3 partial is surjective

Then:

~~~text
pi1 = coker(partial) = 1
pi2 = ker(partial).
~~~

The remaining homotopy group is abelian.

This is a warning that the higher layer may reduce to abelian cohomology or a finite 2-form gauge problem.

### 4.4 both kernel and cokernel are non-trivial

This is the first class worth deeper study.

Even here the public structure exposes:

- the abelian group ker(partial);
- the quotient coker(partial);
- the induced action of coker(partial) on ker(partial);
- a standard Postnikov/cohomological class.

A candidate must explain why its trapdoor is not merely one of these standard invariants.

## 5. Gauge is not a trapdoor

K0, K1, K2.0, and H3-E0 all establish the same project-level warning in different settings:

> hiding a coordinate/gauge representative is useless when an attacker is allowed any equivalent witness.

A crossed-module construction therefore cannot use only:

- hidden vertex 1-gauge;
- hidden edge 2-gauge;
- hidden orientation trivialization;
- hidden names for E or G elements.

If public data determines the same 2-connection up to gauge, the secret is representational rather than cryptographic.

## 6. Public-key interface gate

No K2.2 implementation is justified until the following four algorithms can be written without circularity:

~~~text
(pk, td) <- TwoTypeTrapdoorGen(lambda)
y        <- PublicEval(pk, randomness/message)
w        <- TrapdoorRecover(td, pk, y)
accept   <- Verify(pk, y, w)
~~~

Correctness requires:

~~~text
Verify(pk, y, TrapdoorRecover(td, pk, y)) = true
~~~

for generated instances.

The public attack target is:

~~~text
find any w' such that Verify(pk, y, w') = true.
~~~

Recovery of the planted gauge/history must never be required.

## 7. Mandatory flattening attacks

Before claiming an executable successor is interesting, test in this order:

1. compute ker(partial), im(partial), coker(partial);
2. determine the coker action on ker;
3. reject trivial/injective/surjective degeneracies;
4. compute/identify the Postnikov/cohomology layer;
5. test orientation-double-cover reduction;
6. test semidirect/extension completion;
7. normalize all public 1-gauge and 2-gauge degrees of freedom;
8. extract a finite CSP/SAT factor graph;
9. measure treewidth/separators;
10. test Goldreich/random-local-function flattening;
11. test canonicalization and automorphisms;
12. compare with existing crossed-module cryptographic constructions.

A timeout in one attack is not evidence of one-wayness.

## 8. Current decision

**Naive K2.1 — "choose a crossed module and hide a higher gauge" — is rejected before code.**

This rejection is about the proposed *use* of the mathematics, not about crossed modules themselves.

The first potentially admissible K2.2 must satisfy all of these:

- ker(partial) non-trivial;
- coker(partial) non-trivial;
- non-trivial action and/or Postnikov layer that matters to the verifier;
- public evaluation does not reveal an equivalent 2-connection;
- secret trapdoor is invariantly useful rather than a gauge choice;
- generated positive instances have an explicit public attack target;
- the relation is not merely a bounded-local CSP in new notation.

Until such a relation is specified, there is no K2 cryptographic primitive to benchmark.

## 9. Security status

No one-wayness, average-case hardness, post-quantum security, IND-CPA, IND-CCA, KEM, or production-security claim exists.
