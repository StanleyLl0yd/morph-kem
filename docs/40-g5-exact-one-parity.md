# 40 — G5 nonlinear exact-one parity-projection negative control

## Status

**G5 is an attack calibration in progress.** Pre-code structural analysis already found that every signed exact-one-of-three clause exposes a necessary affine GF(2) equation. Exact-head CI must confirm whether the proposed full-rank templates let that cheaper projection recover a witness accepted by the original nonlinear verifier.

G5 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G4 used explicit pairwise XOR phase constraints and collapsed to binary synchronization. G5 changes the visible predicate to signed ternary exact-one constraints over the same locally ambiguous G3 matching phases.

The important attack-first observation is immediate:

~~~text
exactly one of l1,l2,l3 is true
    implies
l1 XOR l2 XOR l3 = 1.
~~~

For signed literals `l_t = x_t XOR n_t`, every public clause therefore exposes

~~~text
x_i XOR x_j XOR x_k = 1 XOR n_i XOR n_j XOR n_k.
~~~

Thus a nonlinear-looking verifier can still leak an affine quotient.

## Construction

Each Boolean variable is one independently relabelled `g3-3` gadget. The gadget has six public tetrahedra and exactly two accepted perfect-match decompositions. Canonical public ordering maps those decompositions to phase `0` and phase `1`.

For `g` gadgets, use two deterministic 3-uniform clause families:

~~~text
(i, i+1, i+3) mod g
(i, i+2, i+5) mod g
~~~

for every `i`, with each triple sorted canonically.

For `g = 12,18,24`, the resulting `2g` triples are distinct, every variable has degree six, and the bipartite factor graph is connected. The unsigned GF(2) incidence matrices have full rank `g`.

Generation derives a hidden reference phase vector from the master seed. For each public triple it chooses one target literal position deterministically and publishes negation bits such that the reference makes exactly that one signed literal true.

Toy sets:

~~~text
g5-12  12 gadgets   24 clauses   72 public tetrahedra
g5-18  18 gadgets   36 clauses  108 public tetrahedra
g5-24  24 gadgets   48 clauses  144 public tetrahedra
~~~

## Public relation

A witness chooses one accepted G3 matching for every gadget. The verifier derives the corresponding canonical phase bits and checks every signed exact-one clause using ordinary integer sum, not parity.

The hidden reference phase vector is never required. Any accepted phase assignment and local matching witness is attacker success.

## A-032 — public exact-one parity projection

A-032 uses only public gadgets and signed clauses:

1. enumerate and canonically order the two accepted G3 matchings for each gadget;
2. project every exact-one clause to its necessary affine GF(2) equation;
3. perform public Gauss-Jordan elimination;
4. record rank, nullity and row-XOR work;
5. if the affine system has a unique solution, lift that phase vector to local matching witnesses;
6. submit the lifted witness to the original nonlinear exact-one verifier;
7. compare with the hidden reference only after public acceptance.

If the full-rank projection recovers an accepted witness, G5 is rejected immediately. DPLL/SAT would be a strictly heavier attack and is not needed to falsify the distribution.

## Structural controls

The implementation records:

- variable degree histogram;
- factor-graph connected-component count;
- bipartite factor-graph cycle rank;
- local G3 matching counts and search work;
- projected equation/variable count;
- GF(2) rank/nullity and row-XOR work;
- affine solution count;
- exact nonlinear clause checks;
- public witness acceptance;
- post-attack comparison with the hidden reference.

The regular clause template deliberately avoids isolated or unusually low-degree variables. That prevents an easy role-leak explanation from being confused with the parity-projection attack.

## Rejection gate

Reject G5 if A-032 recovers an accepted nonlinear witness from the public affine quotient. Do not increase `g` or clause density as a repair when the coefficient family remains full rank.

Worst-case exact-one-3-SAT hardness is irrelevant if this generated family publishes a solver-complete affine quotient.

## G6 gate

A successor must use an accepted predicate whose cheap quotient is not already sufficient to recover a verifier-valid witness. It must still face quotient/abelianization tests, CSP/SAT, low-width algorithms, normalization, equivalent-witness multiplicity, and generated-role leakage before any trapdoor work.

No security claim.
