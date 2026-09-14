# 91 — HGA-0 binding action-space survey

## Status

HGA-0 is a **design and falsification survey**, not a cryptographic primitive. It follows the NAT7–NAT10 negative results, where exact publication exposed residual structure and lossy/noisy publication hid the planted witness while creating many verifier-equivalent attacker witnesses.

The HGA redesign changes the public relation from

```text
find any hidden decomposition / representation satisfying a permissive verifier
```

to

```text
public X
secret action s
public Y = Apply(s, X)
recover any explicitly verifier-equivalent action taking X to Y
```

No one-wayness, post-quantum hardness, novelty, KEM, signature, IND-CPA/CCA, or production-security claim is made.

## Mandatory interface

Any HGA candidate must define before attack measurements:

```text
ObjectGen(params, seed) -> X
ActionGen(params, seed) -> s
Apply(s, X) -> Y
VerifyAction(X, Y, candidate) -> bool
EquivalentActions(X,Y) = {a : VerifyAction(X,Y,a)}
```

The planted action is reference-only. **Any accepted action is attacker success.**

A candidate must report or bound:

- `Stab(X)`;
- transporter size `{a : a·X = Y}` in the declared action representation;
- kernel of the represented action;
- quotient by unavoidable equivalences;
- public canonicalization/equality cost;
- whether shorter/easier equivalent actions exist;
- classical generic search cost;
- quantum structure exposed by the action.

A construction with a hidden planted action but a huge cheap transporter repeats the NAT9/NAT10 failure and is rejected.

## Literature filter

The goal here is not to copy an existing scheme. Existing group-action families are used to identify which structural properties are desirable and which are dangerous.

### A. Commutative class-group / CSIDH-style actions

**Binding quality: strong. Research novelty for MORPH: low. Quantum risk: explicit.**

Class-group actions on suitable isomorphism classes of elliptic curves are the canonical hard-homogeneous-space example. The intended action is free and transitive, so for two objects in the same torsor there is a unique group element taking one to the other. This is exactly the kind of binding semantics missing from NAT9/NAT10.

However, commutativity gives the attacker strong quantum structure. The action-recovery problem can be expressed as an abelian hidden-shift problem and admits Kuperberg/Regev-style subexponential quantum attacks. Concrete CSIDH security analysis therefore has to price the quantum action oracle rather than treating a generic group action as automatically post-quantum.

Useful references:

- Castryck, Lange, Martindale, Panny, Renes, *CSIDH: An Efficient Post-Quantum Commutative Group Action* (2018): https://csidh.isogeny.org/
- CSIDH security-analysis bibliography: https://csidh.isogeny.org/analysis.html
- Kuperberg, *A subexponential-time quantum algorithm for the dihedral hidden subgroup problem* (2003): https://arxiv.org/abs/quant-ph/0302112
- Smith, *Pre- and post-quantum Diffie-Hellman from groups, actions, and isogenies* (2018): https://arxiv.org/abs/1809.04803
- *Another Look at the Quantum Security of CSIDH* (2025): https://eprint.iacr.org/2025/376

**HGA-0 verdict:** retain the torsor/free-action idea as a design target, but do not use an abelian class-group action as a supposedly new MORPH assumption.

### B. General supersingular-isogeny / endomorphism relations

**Binding quality: not reducible to a simple free action. Research maturity: high. Implementation complexity: very high.**

Modern SQIsign is evidence that isogeny mathematics remains an active post-quantum research direction after the SIDH/SIKE break, but its assumptions and proofs are substantially more specialized than “recover a secret group-action word.” NIST advanced SQIsign to Round 3 of its additional-signature process in May 2026; this is evaluation status, not standardization.

NIST IR 8610 describes SQIsign as relying on the presumed hardness of supersingular-isogeny and endomorphism-ring problems and notes that the SIDH torsion-point attacks do not directly apply because SQIsign avoids the auxiliary information those attacks exploited. Recent proof work uses explicit endomorphism problems and hints, again emphasizing that the modern security relation is not a generic action inversion problem.

Useful references:

- NIST Round 3 page: https://csrc.nist.gov/projects/pqc-dig-sig/round-3-additional-signatures
- NIST IR 8610 (May 2026): https://doi.org/10.6028/NIST.IR.8610
- Aardal, Basso, De Feo, Patranabis, Wesolowski, *A Complete Security Proof of SQIsign* (CRYPTO 2025): https://research.ibm.com/publications/a-complete-security-proof-of-sqisign
- Aardal, Basso, Riepel, *The Algebraic Isogeny Model* (EUROCRYPT 2026): https://research.ibm.com/publications/the-algebraic-isogeny-model-a-general-model-with-applications-to-sqisign-and-key-exchanges

**HGA-0 verdict:** important reference architecture, but not a sensible place to claim MORPH novelty or to improvise a toy trapdoor.

### C. Linear-code equivalence actions

**Binding quality: potentially good for low-automorphism random objects. Public invariants/attacks: significant.**

Linear Code Equivalence (LCE) is a clean transporter problem: find the monomial transformation mapping one code to an equivalent code. This is close to the desired HGA interface, with code automorphisms giving the stabilizer.

The family is nevertheless already heavily studied. NIST IR 8610 reports a second-round attack on LESS that lowered concrete attack complexity by about 12–24 bits across its parameter sets and cites uncertainty about whether the submitted parameters met their targets. LESS did not advance to Round 3. Work in 2026 also continues to develop invariant/algebraic models for LCE.

Useful references:

- NIST IR 8610, section on LESS: https://doi.org/10.6028/NIST.IR.8610
- Alecci, D'Alconzo, *Linear Code Equivalence via Plücker Coordinates* (2026): https://arxiv.org/abs/2603.09869
- Dinh, Moore, Russell, *Quantum Fourier sampling, Code Equivalence, and the quantum security of the McEliece and Sidelnikov cryptosystems*: https://arxiv.org/abs/1111.4382

**HGA-0 verdict:** useful comparison/control and closely related to the TDC line, but not a compelling source of new MORPH mathematics.

### D. Lattice-isomorphism and other highly representable actions

**Binding quality: candidate-dependent. Linearity/reuse risk: high.**

Recent work studies lattice isomorphism explicitly as a cryptographic group action. More generally, representation-based cryptanalysis shows that if an action admits a sufficiently small linear representation, assumptions such as weak unpredictability can fail. This is exactly the sort of “public structure linearizes the secret” failure repeatedly seen in MORPH's older geometry line.

Useful references:

- Benčina, Budroni, Chi-Domínguez, Kulkarni, *Properties of Lattice Isomorphism as a Cryptographic Group Action*, PQCrypto 2024, DOI 10.1007/978-3-031-62743-9_6
- *Representations of group actions and their applications in cryptography*, Finite Fields and Their Applications 99 (2024), DOI 10.1016/j.ffa.2024.102476
- Zumbrägel, *Noncommutative Group Actions for Cryptography* (2024), which surveys word-length and linear-representation attacks.

**HGA-0 verdict:** any MORPH action with an obvious low-dimensional faithful representation is rejected before implementation unless the representation itself is demonstrably irrelevant to transporter recovery.

### E. Mapping-class actions on finite character / Markoff varieties

**Binding quality: unknown-to-poor until measured. Mathematical fit with MORPH: high. Falsification value: high.**

This is the most natural topology/arithmetic bridge for a first MORPH-specific HGA control.

For the once-punctured torus, trace coordinates for `SL(2)` representations lead to Markoff-type surfaces, and mapping-class/Nielsen moves act by explicit polynomial transformations. A standard Markoff level has Vieta involutions

```text
V1(x,y,z) = (yz - x, y, z)
V2(x,y,z) = (x, xz - y, z)
V3(x,y,z) = (x, y, xy - z)
```

on

```text
x^2 + y^2 + z^2 - xyz = 0  (mod p).
```

This is mathematically attractive but comes with an immediate warning: the public action is literally a bounded-degree graph on finite-field points. Modern results show that these Markoff mod-p graphs are connected for all but finitely many primes, and current work gives explicit algorithms for connectivity. Thus an attacker can attempt direct Schreier-graph/BFS navigation from `X` to `Y` without learning the planted mapping-class word.

Useful references:

- Brown, *An almost linear time algorithm testing whether the Markoff graph modulo p is connected* (Research in Number Theory, 2025): https://doi.org/10.1007/s40993-024-00592-9
- Martin, *A new proof of Chen's theorem for Markoff graphs* (Inventiones, 2025): https://doi.org/10.1007/s00222-025-01346-9
- Campos-Vargas, *Markoff triples and generating pairs of SL2(F_p)* (2025): https://arxiv.org/abs/2508.21671
- Golsefidy–Tamam, work on mapping-class orbit closures / character varieties, including the Markoff correspondence.

**HGA-0 verdict:** nominate this only as **HGA-1 negative-control calibration**, not as a hardness candidate. It directly tests whether the new binding discipline catches a topology-derived action whose public orbit graph is navigable.

## HGA-A000 generic attack checklist

Every HGA candidate must be attacked by at least:

1. canonical forms and normalization;
2. explicit stabilizer/kernel computation where feasible;
3. transporter multiplicity or rigorous bounds;
4. linear/permutation representations;
5. Schreier-graph BFS / bidirectional BFS;
6. meet-in-the-middle on action words;
7. public invariant partitioning;
8. shortest equivalent-action search;
9. hidden-shift/HSP reductions when the action is abelian or close to abelian;
10. verifier acceptance independent of planted equality.

The Group Action Inverse Problem should not be called NP-hard merely because a particular word problem looks combinatorial. D'Alconzo's complexity result places GAIP and related cryptographic group-action problems in a much subtler complexity regime unless the polynomial hierarchy collapses.

Reference: https://arxiv.org/abs/2202.13810

## Decision

HGA-0 does **not** nominate a production candidate.

It nominates one next falsification experiment:

```text
HGA-1 = finite Markoff / mapping-class action navigation control
```

Purpose:

- verify that the new `X -> Y` action interface is implemented correctly;
- measure stabilizer/transporter multiplicity rather than planted equality;
- establish a public BFS / bidirectional-BFS baseline;
- reject the family if action recovery is just graph navigation, as expected from the literature.

If HGA-1 collapses, that is a successful calibration of the new research discipline, not a failed attempt to salvage the old NAT architecture.

Only after HGA-1 should a genuinely less-navigable binding action be considered.

No security claim.
