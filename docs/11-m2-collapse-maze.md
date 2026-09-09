# 11 — M2 collapse-maze experiment

## Status

M2 is a completed attack experiment. It is not a KEM and not a security candidate.

It was designed to answer one question left open by M1:

> Does replacing a reversible public path with genuine elementary-collapse branching create a useful trapdoor asymmetry?

M2 demonstrates that the branching can be real. It also demonstrates a stronger failure: the planted generator exposes a much easier structural core-recovery problem.

## Hidden core

M2 starts from a connected 3-regular graph on an even number of vertices, represented as a one-dimensional simplicial complex.

Because every vertex has degree 3, the core has no free vertex-edge collapse.

Generation starts from a cycle plus a deterministic perfect matching that avoids cycle edges. A final secret vertex permutation removes the original label pattern before publication.

## Elementary expansions

An M2 expansion selects a triangle whose three edges currently have:

~~~text
2 present edges
1 missing edge sigma
~~~

and whose triangle tau is absent.

The generator requires at least one of the two present edges to be a current facet. It then applies the inverse elementary collapse:

~~~text
X <- X union {sigma, tau}
~~~

All other proper faces of tau are already present.

The pair (sigma, tau) is recorded. Reversing the expansion list gives a valid planted collapse certificate.

Later expansions may reuse earlier edges, so the final free-collapse relation is not a set of independent gadgets.

## Publication model

After all expansions, M2 applies a secret vertex permutation.

Public:

- experiment parameters;
- relabeled 2D target complex;
- SHA-256(domain || canonical_hidden_core).

Trapdoor:

- exact relabeled hidden core;
- planted reverse-collapse certificate;
- binding to the public-instance fingerprint.

The digest gives a public exact verifier without publishing the core simplices.

## Baseline branching result

For deterministic maze-6:

~~~text
target simplices:             42
hidden core simplices:        30
planted steps:                 6
initial free pairs:           18
planted free pairs min:        3
planted free pairs mean:      10.50
planted free pairs max:       18
mean planted lexicographic rank: 3.83
~~~

This is qualitatively different from M1: there is no single public inverse branch at each layer.

## Greedy reduction result

For the same target:

~~~text
lex greedy:
    collapses:          6
    residual simplices: 30
    core digest hit:    no

reverse greedy:
    collapses:          6
    residual simplices: 30
    core digest hit:    no

16 deterministic random trials:
    core hits:          0
    unique residuals:  16
    residual size:     30 in every trial
~~~

A local choice really can select a different terminal residual.

This validates the "maze" behavior, but it also creates the equivalent-witness question: why should one same-sized residual be cryptographically privileged?

## A-013: bounded collapse DFS

A public attacker can use the digest as a success oracle while exploring free-collapse states.

The implementation:

- enumerates deterministic free-collapse pairs;
- canonicalizes every intermediate complex;
- deduplicates visited states;
- knows the expected hidden-core simplex count from the public generator;
- prunes states that are already too small.

maze-6:

~~~text
core found:       yes
nodes:            1095
visited states:   1150
maximum frontier:   58
~~~

This proves only that the small instance is searchable, not an asymptotic result.

## A-014: generator-structure recovery

The decisive break does not search collapse states.

Every M2 non-core edge is created together with a filled triangle. Therefore:

~~~text
triangle-incidence(edge) == 0
    => edge must belong to hidden core
~~~

The hidden core is also known to be 3-regular.

The implemented attacker:

1. extracts the target 1-skeleton;
2. marks zero-triangle-incidence edges as forced core edges;
3. enumerates only spanning subgraphs completing every vertex to degree 3;
4. tests each candidate against the public core digest.

### maze-6

~~~text
forced edges:          6
optional edges:       18
search nodes:         59
3-regular candidates:  4
core recovered:      yes
~~~

### Fixed-seed sweep

| Set | Nodes | Candidate cores | Forced edges | Optional edges | Found |
|---|---:|---:|---:|---:|---:|
| maze-4 | 13 | 1 | 7 | 12 | yes |
| maze-6 | 59 | 4 | 6 | 18 | yes |
| maze-8 | 520 | 14 | 2 | 24 | yes |
| maze-10 | 51 | 1 | 5 | 29 | yes |
| maze-12 | 441 | 5 | 2 | 34 | yes |

This is a complete structural break of the current generated distribution for these experiment instances.

## Why vertex relabeling did not help

The final secret permutation hides labels, not semantics.

Properties such as vertex degree, triangle incidence, regularity, graph-factor constraints, homology, and automorphism structure remain available to an attacker.

The M2 failure is therefore a direct example of why cryptographic obfuscation cannot be obtained by renaming combinatorial objects.

## What M2 establishes

Positive research result:

- valid elementary expansions/collapses are executable;
- a planted reverse-collapse certificate is exact and reproducible;
- the public reduction state space genuinely branches;
- greedy choices reach many different terminal residuals.

Negative research result:

- the generator family leaks a much easier constrained-subgraph problem;
- the planted core is not intrinsically singled out by reduction minimality;
- a public digest makes candidate validation exact;
- parameter inflation cannot repair the model.

## Requirements for a successor

A successor must not be "M2 with more vertices."

Before implementation it should specify how it avoids:

1. a fixed regular-degree hidden-core family;
2. cells that are provably core/non-core from local incidence;
3. a simple graph-factor or matching formulation;
4. independent low-width expansion gadgets;
5. arbitrary privileging of one among many equivalent terminal residuals.

A promising next direction is a higher-dimensional, incidence-balanced generated distribution in which the hidden Morse certificate is not equivalent to recovering a simple planted subcomplex.

That direction remains experimental and must be attacked before any KEM wrapper.
