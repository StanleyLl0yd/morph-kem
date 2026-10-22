# 00 - Overview

## Current objective (2026-10-21)

MORPH-KEM is a **research-only, attack-first search for an independently motivated mathematical inversion relation** that is not just a renamed classical cryptographic assumption or a hard-looking encoding. Its original discrete Morse / topological KEM concepts are historical negative controls, **not an active candidate architecture**.

**GLOBAL NO NOMINATION.** No OWF, PQ-security, trapdoor, PKE or KEM claim. No implementation is authorized until a mathematical relation survives the [MORPH-R0 15-field entry gate](97-morph-r0-cross-line-postmortem.md#11-re-entry-gate-for-any-new-morph-family).

**Pivot 2026-10-21:** [decision, reopening gate and next milestones](foundation/F0-independent-foundation-pivot-2026-10-21.md). Existing planted-TI work is **FROZEN as an attack comparator**, not a nominated foundation. The first independent algebraic [finite-local-ring lifting no-go](foundation/F0-deformation-tower-public-lift-screen.md) proves a polynomial any-witness section given a public smooth residue section; its singular-obstruction frontier is **HOLD** and cannot be called new hardness. H-A/H-B/H-C HOLD, no candidate or new experiment.

**2026-10-22 independent H-B boundary:** [Explicit cellular-cochain public-section theorem](foundation/F0-cochain-public-section-null-distinction.md) rejects affine face-coboundary inversion even for complexes with large H²; this is standard linear algebra, not positive Field 15. Broad nonlinear H-B remains HOLD, D0 deferred, planted-TI frozen.

**2026-10-22 independent D1 boundary:** [Univariate permutation-polynomial dynamical inversion](foundation/F0-iterated-permutation-polynomial-public-section.md) is deterministically polynomial, even for many public iterations and a uniform planted/null public target law; expanding the iterate's algebraic degree is not a hardness argument. Nonpermutation dynamics remain unadmitted HOLD, not a candidate.

**2026-10-22 nonpermutation D1 boundary:** [Uniform iterated-fibre posterior and null TV](foundation/F0-dynamical-fibre-posterior-and-galois-boundary.md) are exact information-theoretic counts, not polynomial inversion or independent Field 15; fixed finite-field Galois tree action is Frobenius-generated and must not be confused with generic number-field arboreal automorphisms. D1 nonpermutation remains HOLD.

**2026-10-22 independent D2 screening:** [Graph-cover public 1-WL reconstruction](foundation/F0-graph-cover-color-refinement-section.md) inverts all honest lifts over color-discrete public base graphs, including unconditional dense random G(n,1/2) bases with high probability. Established graph covering/Weisfeiler-Leman prior art; non-discrete bases not yet eligible as a crypto candidate; D2 discrete-base ANALYTIC REJECT, global NO NOMINATION.

**2026-10-22 stronger D2 attack:** [Random complete-base 2-lift public common-neighbor recovery](foundation/F0-random-two-lift-codegree-recovery.md) is high-probability original any-cover inversion even though 1-WL sees no vertex distinctions. For arbitrary bases, recovered fibre matching is **not** itself a labeled accepted projection without quotient isomorphism. No positive Field 15, D2 K_n ANALYTIC REJECT.

**2026-10-22 D3 literature intake:** [High-dimensional-expander code original-verifier fork](foundation/F0-hdx-syndrome-original-verifier-fork.md) distinguishes Gaussian any-syndrome inversion from known bounded-weight syndrome decoding. New HDX coding constructions (CCC 2025; Annals 2026) are genuine mathematical prior art, not automatically an independently new crypto assumption; fixed weight is polynomially invertible, growing weight remains unadmitted code-based research. No Field-15 nomination.

## Current program

- ~80% genuinely new mathematics and public any-witness inversion attacks, recorded in [#196](https://github.com/StanleyLl0yd/morph-kem/issues/196).
- ~20% restricted HEPMR review through AP103 in [#195](https://github.com/StanleyLl0yd/morph-kem/issues/195); **BENCHMARK ONLY**, no wider scan.
- [N1-52 checkpoint](100-morph-n1-status-2026-10-14.md) records 593,305 exact toy protocol cases plus 40 controls since N1-34. The independent relations [N1-53](101-morph-n1-53-resistance-no-go.md) through [N1-59](107-morph-n1-59-hyperbolic-geodesic-no-go.md) all fail by exact polynomial public any-witness sections. New families: [N1-56 cyclic bispectrum](104-morph-n1-56-finite-bispectrum-no-go.md), [N1-57 Walsh-Radon tomography](105-morph-n1-57-radon-walsh-no-go.md), [N1-58 symmetric principal minors](106-morph-n1-58-principal-minors-no-go.md), and [N1-59 rational hyperbolic-geodesic cosh-distance](107-morph-n1-59-hyperbolic-geodesic-no-go.md). No new toy enumerations. N1-60 remains **unallocated**; no new stage without independent positive Field-15 evidence.

Additional independently developed no-go proofs were retained under [supplemental notes](supplemental/README.md): [Pauli symplectic Gram](supplemental/s1-pauli-symplectic-public-section.md) and [anchored phaseless integer minors](supplemental/s2-anchored-phaseless-minor-public-section.md). Their original issue labels collided with the canonical N1 timeline, which is unchanged; neither added empirical cases.

For every proposed public instance `P`, the attacker wins by producing **any** `candidate` satisfying `Verify(P,candidate)`; planted-source recovery is not required. Generated distribution, public bitlength, the fibre `Equivalent(P)`, polynomial verifier, known normal forms, classical/quantum attacks and Field-15 distinctness must be explicit *before* code.

**Foundation source-first update (2026-10-16):** [Finite-field matroid realization boundary](foundation/F0-matroid-realization-boundaries.md) proves full-original-verifier public sections for rank two, a scoped frame-generated rank-three class, and near-certain honest-law inversion for large-field uniform matroids of any fixed rank. This is **classical geometry/coding-theory prior art**, analytical only, **no positive Field 15**. The [active F0 programme #208](https://github.com/StanleyLl0yd/morph-kem/issues/208) supersedes treating unallocated N1-60 as an automatic source experiment.

## Historical materials

The older descriptions in `01` through `04`, `spec/morph-kem-v0.1.md`, and the M/H/K/G/HGA/NAT/TDC/BPT experiment files document **rejected research directions**. Preserve them for reproducibility; do not interpret historical `KeyGen`, `Decaps` or trapdoor sketches as a live roadmap.

Source of truth: [N1-59 analytic status](107-morph-n1-59-hyperbolic-geodesic-no-go.md), [N1-58 analytic status](106-morph-n1-58-principal-minors-no-go.md), [N1-57 analytic status](105-morph-n1-57-radon-walsh-no-go.md), [N1-56 analytic status](104-morph-n1-56-finite-bispectrum-no-go.md), [N1-55 analytic status](103-morph-n1-55-adic-trie-no-go.md), [N1-54 analytic status](102-morph-n1-54-hankel-realization-no-go.md), [N1-53 analytic status](101-morph-n1-53-resistance-no-go.md), [N1-52 numeric status](100-morph-n1-status-2026-10-14.md), [research log](../notes/research-log.md), [cryptanalysis ledger](05-cryptanalysis.md), [MORPH-N1 #196](https://github.com/StanleyLl0yd/morph-kem/issues/196).
