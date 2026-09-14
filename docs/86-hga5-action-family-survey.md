# 86 — HGA5 action-family literature gate

## Status

**No HGA5 implementation candidate is selected yet.** HGA4 is frozen after HGA4d/e/f: the exact-distance Hurwitz action on free-group tuples remains strongly finite-representation-leaky under held-out and adaptive public quotient attacks.

HGA5 therefore changes the action family rather than training generation against more quotients.

This document is a pre-implementation falsification gate, not a security claim.

## Failure classes already closed by HGA1–HGA4f

A new action is not worth implementing if it immediately falls into one of these classes:

1. **small finite orbit / generic MITM** — HGA1;
2. **public canonical endpoint reduction** — HGA2;
3. **public linear intertwiner/kernel solve** — HGA3;
4. **abundant small finite representations giving strong admissibility filters** — HGA4d/e/f;
5. **generator work asymmetry or non-geodesic planted histories** — HGA4b/c.

The verifier semantics remain unchanged: any action element that maps the public source to the public target is attacker success. Recovering the planted secret is unnecessary.

## Candidate-family screen

### 1. Braid-group / conjugacy-style platforms — reject before implementation

Braid groups provide efficient Garside-type normal forms and faithful linear representations, and decades of group-based cryptanalysis have repeatedly shown that generic hard group problems do not automatically produce hard generated cryptographic instances.

A 2024 survey of braid root-extraction cryptosystems concludes that the surveyed authentication/signature proposals are generally insecure and gives attacks for them. Earlier braid-cryptography literature likewise documents attacks tied to generated-instance weakness.

This is too close to HGA2/HGA3/HGA4 failure modes: canonicalization, linear representations and instance-generation leakage are all first-class attack surfaces.

**Decision:** do not use braid groups as the HGA5 primary platform.

### 2. Thompson-style groups — reject before implementation

Thompson's group `F` has an efficiently computable classical normal form; the original cryptographic literature emphasizes near-linear normal-form computation. That is useful algebraically but exactly the wrong first property for HGA5, where public endpoint canonicalization must not manufacture an obvious connector or strongly collapse orbit search.

**Decision:** not a primary HGA5 platform.

### 3. Polycyclic / metabelian conjugacy platforms — reject before implementation

The group-based cryptography literature contains linear-decomposition, representation and simultaneous-conjugacy attacks against several such platform families. HGA3 already demonstrates the MORPH-specific version of the same anti-pattern: a formally nonlinear action can invert by ordinary linear algebra in the hidden action variable.

**Decision:** reject platform families with an immediate faithful linear-decomposition route.

### 4. Abelian class-group actions / CSIDH-style GAIP — benchmark, not MORPH novelty

Class-group actions are a serious and mature cryptographic research direction. CSIDH is explicitly built around an ideal-class-group action on supersingular elliptic curves, and current work continues to study implementations, side channels and group-action inverse problems.

However, the action is abelian and the inverse problem can be formulated as a quantum hidden-shift problem. Kuperberg-style algorithms therefore give a subexponential quantum attack framework; recent work continues to refine concrete estimates.

This does **not** mean class-group actions are useless. It means adopting a CSIDH-like action would be entering an existing mature assumption family rather than creating a genuinely new MORPH mathematical assumption.

**Decision:** retain as a benchmark/reference family, not the default HGA5 candidate.

### 5. Supersingular/quaternion/isogeny groupoids — serious reference direction, not a copy target

Isogeny/quaternion mathematics remains an active post-quantum research area. As of September 2026, SQIsign is in NIST's third round for additional digital signatures. That is evidence that isogeny-based mathematics remains a serious research direction after the SIDH break, but it is not evidence for a new MORPH KEM assumption.

SQIsign-style constructions use much richer quaternion/isogeny structure than an abstract action endpoint problem. Copying that machinery would neither be novel nor simplify our attack-first objective.

**Decision:** study its design lessons — especially hiding useful paths while keeping verification possible — but do not repackage SQIsign or claim novelty from quaternion ideals alone.

### 6. Finite nonabelian simple groups — insufficient by themselves

Finite simple groups are actively discussed as possible post-quantum algebraic platforms, but a bare finite group action recreates HGA1 at toy scale: full orbit/Schreier enumeration is the first attack. Hidden-subgroup and representation-theoretic structure must also be screened.

**Decision:** finite simplicity alone is not an HGA5 hardness mechanism.

## Most promising unresolved design space

The remaining interesting space is not "pick a harder group". It is an action or groupoid with all of the following properties:

- source/target equality is public and cheap;
- applying a secret action is efficient;
- public equality does not expose a complete normal form for a connector;
- the action does not linearize in the unknown action element;
- small finite representations do not routinely prune most of the exact state space;
- the useful public object is deliberately coarser than a full exact connection/decomposition;
- the relation has a clear average-case generated distribution, not only a worst-case hard problem.

Two research directions survive this literature gate provisionally:

### HGA5-A — arithmetic groupoid action on moduli objects with coarse public representation

Investigate an arithmetic groupoid where a secret morphism moves between equivalent moduli objects, but the public representation intentionally forgets the internal path/morphism data.

Candidate ingredients may involve ideal classes, oriented structures, covers or local systems, but the first attack must search for:

- character/trace invariants;
- linear/cohomological representations;
- finite reductions;
- canonical representatives;
- equivalent-morphism multiplicity.

This is a **research template**, not yet a concrete assumption.

### HGA5-B — nonabelian local-system/moduli action with lossy observable

Investigate actions on nonabelian local systems or character-like moduli where the public value is a lossy observable rather than the full connection. NAT7/NAT8 show why the full exact connection is unacceptable: tree normalization exposes the residual representation directly.

The main danger is that trace/character coordinates or finite quotients may again provide a cheap complete or near-complete invariant.

This direction is retained only for a deeper invariant-theory survey before code.

## Quantum screen

Any commutative or effectively abelian action must be tested against hidden-shift algorithms before implementation. Any nonabelian candidate must be checked for hidden-subgroup reductions, efficient Fourier/representation attacks, and whether public finite quotients create a smaller hidden-shift/subgroup instance.

"No known Shor reduction" is not an adequate post-quantum argument.

## Literature checkpoints used for this gate

- CSIDH literature and reviews: ideal class-group action on supersingular elliptic curves; extensive classical/quantum analysis.
- Recent quantum-security analyses of class-group actions: GAIP/CSIDH inverse problems admit hidden-shift formulations and Kuperberg-style subexponential quantum attacks.
- NIST Additional Digital Signatures Round 3 (2026): SQIsign remains an isogeny-signature candidate, showing that isogeny/quaternion methods remain an active specialized field.
- 2024 braid root-extraction cryptography survey: surveyed braid authentication/signature proposals are generally insecure under known attacks.
- Group-based cryptography surveys: representation, length-based, linear-decomposition and generated-instance attacks remain central concerns.

These references motivate kill-gates; they are not evidence that any retained HGA5 direction is secure.

## Decision

**Do not implement HGA5 yet.** The next HGA task is a deeper survey of HGA5-A/HGA5-B until one candidate has explicit objects, actions, equality semantics and no immediate HGA1–HGA4f collapse.

Meanwhile TDC and NAT can continue independently with their own measured gates.

No trapdoor primitive, KEM, one-wayness, post-quantum, IND-CPA/CCA, or production-security claim exists.