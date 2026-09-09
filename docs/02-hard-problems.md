# 02 — Candidate hard problems

The names in this document are provisional research labels, not established complexity assumptions.

## HMCP — Hidden Morse Coordinate Problem

Let (mathcal D_lambda) generate a public description (pk), a trapdoor (td), and a family of public forward maps. A seed (s) selects a path through hidden binary coordinates, producing a public object (C).

**Search form:** given ((pk,C)), recover (s) or an equivalent preimage accepted by the decapsulation relation.

The relevant hardness target is average-case hardness over

[
(pk,td)leftarrowoperatorname{KeyGen}(1^lambda),quad
sleftarrow{0,1}^ell.
]

## HMRP — Hidden Morse Reduction Path Problem

Given a generated public object (X), find a reduction path or acyclic Morse matching that reaches the designated canonical core while satisfying the acceptance relation.

This problem matters because an attacker need not recover the original trapdoor if any equivalent reduction certificate is enough.

## HMCR — Hidden Morse Conjugacy Recovery

The provisional public construction exposes several transformations derived from one hidden representation. HMCR asks whether the shared hidden representation, coordinate system, or an equivalent structural decomposition can be recovered from the family of public transformations.

This is currently considered the most dangerous structural attack class.

## Required future definitions

Each problem must eventually specify:

- exact input encoding;
- generated distribution;
- success relation;
- search vs decision variants;
- parameter scaling;
- classical cost model;
- quantum cost model;
- whether equivalent witnesses are accepted.

## Explicit non-claim

Known hardness results for discrete-Morse optimization or collapsibility do not by themselves establish HMCP, HMRP, or HMCR as cryptographic assumptions.
