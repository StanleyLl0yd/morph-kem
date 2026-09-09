# 12 — M3 equivalent-witness Morse experiment

## Status

M3 is a **rejected attack experiment**.

It corrects one conceptual error exposed by M2: the public relation no longer asks an attacker to recover one planted core or planted collapse certificate. Instead, **any** valid acyclic discrete-Morse matching with the declared public critical vector is accepted.

That more honest relation makes the present graph-expanded generated family constructively easy.

## Public relation

The public object contains a finite 2-dimensional simplicial complex X, a target critical vector c=(c0,c1,c2), and experiment parameters. There is no planted-core digest and no verifier for the original hidden core.

A witness is any set of Hasse-incidence pairs M={(sigma,tau)} such that:

1. sigma is a codimension-one face of tau;
2. no simplex occurs in more than one pair;
3. matched Hasse incidences are reversed and unmatched incidences point downward;
4. the resulting directed Hasse graph is acyclic;
5. unmatched-simplex counts equal the public critical vector.

The implementation checks all five conditions exactly.

## Generator

M3 uses a connected variable-degree graph core rather than M2's 3-regular graph. The graph is a cycle plus deterministic pseudorandom chords, so it has minimum degree at least two without a fixed regular-degree fingerprint.

Valid elementary edge/triangle expansions are then applied, followed by a final deterministic secret vertex relabeling.

The planted witness consists of every planted edge/triangle expansion pair plus a spanning-tree vertex/edge matching on the hidden graph core.

For a connected graph with n vertices and m edges, the graph matching leaves critical vector (1,m-n+1). Every 2D expansion contributes one matched edge/triangle pair, so the public M3 target is (1,beta1,0).

## A-016 — free-collapse plus spanning-tree witness

The attacker does not recover the planted graph.

1. Repeatedly choose any currently free edge/triangle collapse.
2. If all triangles disappear, obtain some connected graph residual G.
3. Choose any spanning tree of G.
4. Match every non-root tree vertex with its parent tree edge.
5. Combine those graph pairs with the edge/triangle collapse pairs already chosen.
6. Submit the resulting matching to the public validator.

If the collapse phase reaches a graph, the resulting witness has the target critical vector and is accepted.

Different graph residuals are valid equivalent witnesses rather than failures.

## Deterministic baseline

For morse-6:

~~~text
target simplices: 40
critical target: (1, 5, 0)
planted witness pairs: 17

lex collapse:     graph yes, accepted yes, 6 triangle collapses
reverse collapse: graph yes, accepted yes, 6 triangle collapses
initial/max public triangle choices: 18 / 18

16 random collapse trials:
  graph reached: 16/16
  accepted: 16/16
  unique graph residuals: 16
~~~

## Fixed-seed scaling sweep

Thirty-two deterministic random collapse trials and eight generic greedy-matching trials were run for every M3 experiment set:

| Set | Critical target | Simplices | Lex | Reverse | Random accepted | Unique residuals | Generic greedy target hits |
|---|---|---:|---:|---:|---:|---:|---:|
| morse-6 | (1,5,0) | 40 | yes | yes | 32/32 | 32 | 8/8 |
| morse-8 | (1,6,0) | 49 | yes | yes | 32/32 | 32 | 5/8 |
| morse-10 | (1,7,0) | 58 | yes | yes | 32/32 | 32 | 3/8 |
| morse-12 | (1,8,0) | 67 | yes | yes | 32/32 | 32 | 3/8 |
| morse-16 | (1,10,0) | 85 | yes | yes | 32/32 | 32 | 4/8 |

These are empirical fixed-seed observations, not asymptotic complexity claims.

## A-017 — generic greedy acyclic Hasse matching

M3 also randomizes all Hasse incidences and greedily adds a pair whenever neither simplex is already matched and the enlarged matching remains acyclic.

This generic procedure reaches the exact public critical target with non-zero probability on every tested set. The best critical count equals the target count in every tested set.

A-017 is secondary evidence. A-016 already rejects the generated family.

## Interpretation

**M3 is rejected as a security candidate.**

The failure is not equivalent-witness semantics. Allowing equivalent witnesses removes artificial verifier hardness.

The failure is the generated family: complexes created by elementary expansions from a connected graph remain easy whenever simple public collapses expose any graph residual.

The attacker never needs the planted graph, planted relabeling, planted spanning tree, or planted expansion order.

## Consequence for the next model

A successor must not merely hide a graph under more 2D decoration.

Before scaling it should require:

- genuinely 2-dimensional useful witnesses;
- no public collapse-to-graph solution;
- no target vector obtainable by an elementary spanning-tree construction;
- locally balanced planted/non-planted incidences;
- equivalent-witness acceptance;
- generic greedy Hasse matching measured first;
- no KEM wrapper.
