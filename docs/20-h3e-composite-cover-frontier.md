# 20 — H3-E1 composite-cover public-key adaptation frontier

## Status

**Decision: reject the naive public-key adaptation before implementation.**

This is not an impossibility theorem for all graph-cover cryptography.

It is a precise interface failure of the obvious attempt to turn a known common-key composite-cover construction into a public-key trapdoor relation.

No KEM or security claim is made.

## 1. Prior art: Negami composite-cover cryptography

Seiya Negami proposes a graph-covering prototype cryptosystem in:

- *Composite coverings of graphs and cryptography*, Yokohama Mathematical Journal Vol. 70; received 2024, repository publication 2025:
  https://ynu.repo.nii.ac.jp/records/2001753

The construction is explicitly described as a **common key cryptosystem**.

At a high level:

1. sender and receiver share a connected graph G and spanning tree T;
2. message bits select cotree edges and therefore a particular double covering of G;
3. sender further hides that double cover inside an odd-degree composite covering;
4. receiver uses the shared G,T information and a structural theorem to recover the encoded double-cover data.

This is valuable prior art, but its interface is fundamentally different from public-key encapsulation.

## 2. Public-key interface requirement

A KEM-like public-key experiment would eventually need:

~~~text
(pk, sk) <- KeyGen()
(ct, K)  <- Encaps(pk; randomness)
K'       <- Decaps(sk, ct)
~~~

with:

~~~text
K' = K
~~~

for honest ciphertexts.

The sender must not need sk.

This simple requirement eliminates several superficially appealing graph-cover variants.

## 3. Naive adaptation A — publish the common-key base

Suppose the Negami-style base graph and tree are:

~~~text
pk = (G, T)
~~~

so anyone can construct the same message-dependent intermediate covers as the original sender.

Then the structural decoding information that was previously a common secret is public too.

The attacker can run the same decoding procedure.

This converts the common-key mechanism into a public encoding format, not a public-key trapdoor.

**Rejected.**

## 4. Naive adaptation B — keep the base/tree secret

Suppose:

~~~text
sk = (B, T)
pk = G
~~~

where public G is a larger graph related to secret B by a hidden covering/factorization.

Now the untrusted sender can manipulate public G but does not know B or T.

If the value being encapsulated depends on selecting a secret-base cotree subset or a particular intermediate cover of B, the sender cannot perform that selection.

The original encoding algorithm has therefore ceased to be public.

**Rejected as a complete public-key interface.**

## 5. Naive adaptation C — sender constructs an outer cover of public G

Try instead:

1. pk contains public G;
2. sender samples a covering projection

[
q:H	o G;
]

3. sender knows the planted projection/voltage data and derives K from it;
4. ciphertext transmits a relabeled H;
5. secret lower factorization

[
pi:G	o B
]

is supposed to help the receiver recover q or equivalent data.

This is the first adaptation that at least lets Encaps use pk alone.

But it exposes the central unresolved problem.

## 6. Ciphertext dilemma

### Include q / voltage data

If ct contains an explicit covering projection q, fiber partition, or permutation-voltage description sufficient to reconstruct q, then the attacker receives the same planted covering data that the sender used.

Hashing that public data cannot create a receiver-only secret.

### Omit q / voltage data

Then both receiver and attacker receive only:

~~~text
public G
+
unlabeled/canonically relabeled H
~~~

and need some covering projection:

[
q':H	o G.
]

That is a public search relation.

The receiver's additional secret is the lower factorization:

[
pi:G	o B.
]

For this to be a trapdoor, one must provide an actual algorithm:

~~~text
TrapdoorRecover(pi, H, G) -> q'
~~~

that is substantially easier than the best public recovery algorithm.

No such algorithm has been defined in H3-E1.

Without it, "knowing a lower cover probably helps" is not a cryptographic construction.

## 7. Why unique composite-cover structure is not enough

Negami proves a uniqueness property for certain odd-over-double composite coverings.

That theorem is useful when the relevant base/common-key structure is known.

For a public-key primitive we still need all three properties simultaneously:

1. sender can generate ct using pk only;
2. receiver can exploit sk to recover the sender's shared value;
3. attacker cannot obtain an equivalent accepted recovery from pk and ct.

A uniqueness theorem does not automatically provide a trapdoor algorithm satisfying these roles.

## 8. H-Cover hardness warning

The graph-cover decision problem has NP-complete regimes.

For example, classical results show NP-completeness for broad families of fixed regular target graphs.

Recent work continues to refine H-Cover complexity.

But this does not establish the required assumption.

The cryptographic experiment would use **generated positive instances** H that are deliberately constructed as covers of public G.

Therefore the relevant question is average-case **search**:

> given a sampled positive pair (G,H), find any covering projection H -> G.

Worst-case decision hardness is insufficient.

## 9. Tractable cover regimes also exist

Regular-cover structure can make instances easier.

For example, work of Fiala, Klavik, Kratochvil, and Nedela gives:

- FPT algorithms for regular covers on planar inputs under natural parameterizations;
- polynomial-time cases under additional connectivity/ratio conditions.

References:

- *Algorithmic Aspects of Regular Graph Covers*:
  https://arxiv.org/abs/1609.03013
- related graph-cover complexity literature is summarized in docs/19-h3e-lifted-atlas.md.

Thus symmetry/regularity is not automatically an asset for security.

## 10. Search relation is still constraint-like

Finding a covering projection assigns each ciphertext-graph vertex to a public-base vertex subject to:

- incidence preservation;
- local neighborhood bijection;
- global surjectivity/fiber consistency.

This is a structured constraint problem / locally bijective homomorphism problem.

An H3-E successor must therefore be attacked with:

- local signature propagation;
- color refinement / WL-style refinement;
- exact CSP/SAT;
- automorphism decomposition;
- fiber-size constraints;
- canonical labeling;
- positive-instance planted-structure recovery.

## 11. Public-key adaptation matrix

| Variant | Sender can use pk only? | Receiver advantage defined? | Attacker gets equivalent data? | Result |
|---|---|---|---|---|
| Publish base/tree | yes | no | yes | reject |
| Keep base/tree secret | no for Negami-style encoding | yes/common-key | n/a | reject |
| Publish explicit H->G projection | yes | no | yes | reject |
| Send only unlabeled H | yes | **not yet defined** | public cover-search remains | incomplete/reject |
| Hidden lower factorization G->B | yes | only conjectural | unknown | no trapdoor yet |

## 12. What a real H3-E successor would need

Before more code, define a **trapdoor positive distribution**.

Working abstract interface:

~~~text
(pk, td) <- CoverTrapdoorGen(1^lambda)
(H, w)   <- SamplePositive(pk; r)
w'       <- TrapdoorRecover(td, pk, H)
~~~

where:

- w is a planted covering projection or equivalent witness known to the sampler;
- w' may be any accepted equivalent projection;
- TrapdoorRecover must be demonstrably efficient;
- public recovery must be the explicit attack target.

Only after such an algorithm exists can one ask whether public recovery appears hard on the generated distribution.

## 13. Necessary evidence before cryptography

A future H3-E2 must provide:

1. exact generated distribution;
2. exact public witness relation;
3. deterministic trapdoor recovery algorithm;
4. proof of trapdoor correctness;
5. evidence that trapdoor information is not derivable from pk;
6. positive-instance public attack harness;
7. comparison against CSP/canonicalization/automorphism methods;
8. only then a one-wayness experiment.

Without items 1–4 there is no primitive to attack.

## 14. H3-E1 decision

**Naive public-key adaptation rejected before implementation.**

The useful outcome is an interface constraint:

> graph-cover complexity is irrelevant until we have a secret that gives the receiver a concrete algorithmic advantage while leaving Encaps public.

This is now the gate for any future cover-based MORPH direction.

## Security status

No one-wayness, post-quantum, IND-CPA, IND-CCA, or concrete-security claim exists.
