# 02 — Candidate hard problems

The names in this document are provisional research labels, not established complexity assumptions.

## Historical labels

### HMCP — Hidden Morse Coordinate Problem

Given a generated public object, recover a hidden coordinate or equivalent preimage accepted by the public relation.

M0 showed that a coordinate-based realization can leak those coordinates directly.

### HMRP — Hidden Morse Reduction Path Problem

Given a generated complex, find a useful reduction path or discrete-Morse witness satisfying the public relation.

M2 showed that insisting on the generator's particular planted residual can create artificial verifier hardness.

### HMCR — Hidden Morse Conjugacy Recovery

Recover a hidden representation or equivalent structural decomposition from related public transforms.

M1 remains a warning that common hidden structure can create easier algebraic or isomorphism attacks.

## EMWP — Equivalent Morse Witness Problem

M3 introduces the more honest current research form.

**Input:**

- finite simplicial complex X;
- target critical vector c.

**Search output:**

any acyclic matching M on codimension-one Hasse incidences such that unmatched simplex counts equal c.

The attacker is not required to recover a planted matching, planted core, planted reduction order, or secret relabeling.

Any accepted matching is a success.

## M3 generated-family result

The general EMWP is not claimed easy or hard here.

The specific M3 distribution is easy because its instances are elementary 2D expansions of connected graphs.

A-016 constructs a witness by public edge/triangle collapses to any graph residual followed by a public spanning-tree matching.

Therefore M3 rejects its generated distribution, not the equivalent-witness security principle.

## Required future definitions

Any successor hard problem must specify:

- exact input encoding;
- exact generated distribution;
- exact success relation;
- all accepted equivalent witnesses;
- search versus decision form;
- classical cost model;
- quantum cost model;
- parameter scaling;
- distributional, not merely worst-case, hardness evidence.

## Explicit non-claim

Known worst-case hardness results for discrete-Morse optimization or collapsibility do not establish average-case cryptographic hardness for any MORPH-KEM generated distribution.
