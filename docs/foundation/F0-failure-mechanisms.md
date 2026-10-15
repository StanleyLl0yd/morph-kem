# MORPH-F0: structural failure map and three exact public kill gates

**Date:** 2026-10-15. **State:** research methodology / negative-control mathematics, **GLOBAL NO NOMINATION**. This document is NOT a new cryptographic candidate, attack benchmark, general complexity theorem or implementation. It reports **zero new source instances, experiments or cases**. Tracker: [foundation-first #208](https://github.com/StanleyLl0yd/morph-kem/issues/208). Canonical MORPH-N1 numbering remains in [#196](https://github.com/StanleyLl0yd/morph-kem/issues/196), latest N1-59; N1-60 is not allocated here.

## 1. Quantified inversion problem (not planted-secret recovery)

Let a security-size index \(\lambda\) be given. An **unconditional polynomial sampler** \(\mathrm{Gen}(1^\lambda;r)\) produces a polynomial-size public instance \(P\) and optionally a planted source \(s\), with public input distribution \(D_\lambda\). A deterministic polynomial-time public verifier \(V(P,y)\) tests an encoded candidate of polynomial size. The true attack target is

\[
E(P)=\{y:\text{candidate-domain}(P,y)\land V(P,y)=1\}.
\]

An attacker \(A(P)\) succeeds when \(A(P)\in E(P)\), **not** when it recovers the sampled secret \(s\). Report \(\Pr_{P\sim D_\lambda,A}[A(P)\in E(P)]\) on the *unconditional* honest input distribution. A complexity result for another distribution, a planted-to-original reconstruction task or worst-case hardness does not establish cryptographic one-wayness. In particular, the sampler's bit complexity, its entropy sources and the public representation length must be explicit. This formalization is consistent with [Goldreich, *Foundations of Cryptography*, volume 1](https://doi.org/10.1017/CBO9780511546891.003) and with the [MORPH-R0 15-field gate](../97-morph-r0-cross-line-postmortem.md#11-re-entry-gate-for-any-new-morph-family).

## 2. What the negative corpus actually supports

The following is a **representative mechanism map**, not an assertion that every N1-01..59 or legacy line was independently re-executed for this note. Issue-only historical case counts are not reproduced here.

| Failure mechanism | Anchored project evidence | What it eliminates | Explicit limit |
| --- | --- | --- | --- |
| Universal public accepted section / normal form | [N1-46 Euler/de Bruijn](https://github.com/StanleyLl0yd/morph-kem/issues/196#issuecomment-6167863224); [N1-47 projective frame](https://github.com/StanleyLl0yd/morph-kem/issues/196#issuecomment-6167918238); [N1-53 Laplacian](../101-morph-n1-53-resistance-no-go.md); [N1-55 digit trie](../103-morph-n1-55-adic-trie-no-go.md) | Need to recover original planted object or its hidden coordinates | Only the stated public transcript and verifier |
| Algebraic factorization / public quotient or gauge | [N1-54 Hankel](../102-morph-n1-54-hankel-realization-no-go.md), [N1-56 cyclic bispectrum](../104-morph-n1-56-finite-bispectrum-no-go.md), [N1-57 Walsh-Radon](../105-morph-n1-57-radon-walsh-no-go.md), [N1-58 principal minors](../106-morph-n1-58-principal-minors-no-go.md), [supplemental S1/S2](../supplemental/README.md) | Hidden basis/sign/orientation entropy mistaken for inversion hardness | No conclusion for missing measurements, distinct constrained domains or altered forward maps |
| Small frontier / bounded-width attack | [N1-51 count-frontier DP](https://github.com/StanleyLl0yd/morph-kem/issues/196#issuecomment-6168144976); [N1-44 small-basis recovery](https://github.com/StanleyLl0yd/morph-kem/issues/196#issuecomment-6167358961) | Local complexity mistaken for globally unbounded interaction | N1-51 statement applies to frozen fixed k and public low-width ordering, not arbitrary growing width |
| Mature representation or generic planted CSP | [N1-22 Boolean network profile](https://github.com/StanleyLl0yd/morph-kem/issues/196#issuecomment-6164370730); [MORPH-R0 cross-line failures](../97-morph-r0-cross-line-postmortem.md) | Novel visual packaging or difficult planted recovery mistaken for an independent new problem | Mature CSP identification does NOT imply the stated source distribution has an easy inverter |
| Forward or verification cost / source conditioning | [N1-40 linear-extension count](https://github.com/StanleyLl0yd/morph-kem/issues/196#issuecomment-6167055471); [MORPH-R0](../97-morph-r0-cross-line-postmortem.md) | Expensive hidden computation relabeled an efficient public map | A different efficient observable is a different relation needing a new audit |
| Evidence, scope and leakage discipline | [N1-13 exact PLPST leakage](https://github.com/StanleyLl0yd/morph-kem/issues/196#issuecomment-6163286270); [N1-52 provenance](../100-morph-n1-status-2026-10-14.md); [#199 archive blocker](https://github.com/StanleyLl0yd/morph-kem/issues/199) | Treating high information leakage, many exact toy cases or unknown missing archives as proof of hardness | N1-19 PARTIAL 19/30, N1-23 PARTIAL 9/12, N1-26 HOLD/BENCHMARK remain unchanged |

For the entire corpus, source of truth is the immutable per-stage protocol or result in [#196](https://github.com/StanleyLl0yd/morph-kem/issues/196). This map is **not** a new measurement and does not add to the reported N1-52 total of 593,305 completed heterogeneous cases plus 40 controls. Original ZIP bytes remain missing and are not reproduced or synthesized.

## 3. F0-K1: large conditional secret entropy does not imply any-witness hardness

**Proposition (self-contained counterexample).** For every integer \(n\ge2\), sample \(S\in\mathbb F_2^n\) uniformly and publish \(P=\bigoplus_{i=1}^n S_i\in\mathbb F_2\). Define \(V(P,y)=1\) iff \(\bigoplus_i y_i=P\), for \(y\in\mathbb F_2^n\).

For either public \(P\), the fibre \(E(P)\) has \(2^{n-1}\) members. Conditioned on \(P\), the original sampled \(S\) is uniform over that fibre, so both conditional Shannon and conditional min-entropy equal \(n-1\) bits. Yet the deterministic attacker outputs \(A(P)=(P,0,\ldots,0)\), which passes the ORIGINAL verifier for **every** generated instance in \(O(n)\) time. Thus arbitrarily large hidden conditional entropy is consistent with trivial public any-witness inversion. This elementary illustration is NOT a newly discovered cryptographic theorem, just an exact screening counterexample.

**Gate:** never promote a family based on secret entropy, many equivalent solutions, uniqueness/injectivity of the planted parameterization, or information-theoretic leakage alone. Measure the existence and cost of a public section of \(E(P)\).

## 4. F0-K2: stacking polynomially many public linear views remains linear

**Proposition.** Let \(x\in\mathbb F_q^n\) be sampled by any distribution. For public, explicitly represented matrices \(L_j\in\mathbb F_q^{m_j\times n}\) and offsets \(b_j\), publish \(P_j=L_jx+b_j\), with \(\sum_j m_j=\mathrm{poly}(n,\log q)\). Suppose accepted witnesses are **all** vectors \(y\in\mathbb F_q^n\) such that \(L_jy+b_j=P_j\) for every \(j\). A deterministic public inverter stacks \(L_j\) and \(P_j-b_j\) into one linear system, performs Gaussian elimination and outputs any solution. It succeeds for every honest input, using polynomial field operations and bit complexity for effectively represented finite fields.

**Proof.** The original planted x is a solution, so the public system is consistent. Row reduction constructs a particular solution y; by construction it satisfies every original equality. No recovery of x or rank assumption is required. **Boundary:** secret L, nonlinear observations, an extra sparse/integer/positivity witness restriction, or superpolynomial public length are outside this claim, not counterexamples. Known textbook linear algebra; **not a new hardness reduction**.

**Gate for coupled observations:** a plurality of individually different *linear* projections, bases or public matrix labels cannot generate a new inversion barrier merely by being jointly published.

## 5. F0-K3: local constraints on a public low-width primal graph have a public section

**Proposition.** Consider a finite-domain CSP with \(N\) variables, public alphabet of size \(q\), public extensional constraints (membership test polynomial in their explicit encoding), and a **given public tree decomposition** of the primal constraint graph of width \(w\). If an honest generator produces a satisfiable instance, a dynamic program over the decomposition returns a full satisfying assignment using at most \(\mathrm{poly}(N,M,\lvert P\rvert)\,q^{O(w+1)}\) elementary public operations for M constraints (in the usual nice-decomposition/table representation). Every constraint scope forms a clique in the primal graph and therefore fits some bag.

**Proof sketch.** Enumerate all assignments to each bag (at most \(q^{w+1}\)); mark rows locally satisfying assigned constraints; pass projections/compatible rows across separator intersections, and backtrack from an accepted root row to build an assignment. Since the honestly generated instance is satisfiable, a root row exists. All checks are public. This is the standard treewidth CSP algorithm, see [Freuder (1990)](https://cdn.aaai.org/AAAI/1990/AAAI90-001.pdf) and [Samer-Szeider, *Constraint Satisfaction with Bounded Treewidth Revisited*](https://doi.org/10.1016/j.jcss.2009.04.003).

**Bit-complexity nuance:** with constant q and \(w=O(\log N)\), the displayed cost is polynomial. With polynomially bounded q and **constant** w, it is polynomial. This proposition does **not** prove polynomial time when both q grows polynomially and w grows logarithmically, or when a suitable decomposition is neither provided nor efficiently found. Width of a convenient presentation is only an upper bound; nonobvious quotients may reduce actual width further.

**Gate for local-to-global proposals:** complex local interactions alone are no evidence of difficult any-witness inversion if their public dependency graph has a low-width decomposition.

## 6. Required distinction from established research

- For finite fixed constraint languages, tractability/NP-completeness is described by the independent [Bulatov CSP dichotomy](https://arxiv.org/abs/1703.03021) and [Zhuk's CSP dichotomy](https://arxiv.org/abs/1704.01914). This is about **worst-case** CSP complexity, not the average-case inverse distribution proposed for MORPH.
- [Abramsky-Brandenburger (2011)](https://arxiv.org/abs/1102.0264) already frame certain local-to-global section obstructions in sheaf theory. An obstruction to global consistency is **not** evidence of hardness on an honest, always globally consistent generated instance.
- [Random local functions](https://eccc.weizmann.ac.il/report/2025/139/) and the established Goldreich-function literature mean a generic planted local predicate graph cannot be called mathematically new by attaching geometric language.
- [Akavia et al., *On Basing One-Way Functions on NP-Hardness*](https://www.wisdom.weizmann.ac.il/~oded/PSX/aggm1.pdf) reinforce that worst-case NP-hardness must not be substituted for distributional inversion hardness.

## 7. Research status after this audit

**Proved (within explicit hypotheses):** F0-K1 parity entropy counterexample, F0-K2 stacked public linear-view inverter, F0-K3 public-decomposition low-width CSP inverter. These are well-known mechanisms, not new mathematical inventions.

**Not proved:** that every coupled nonlinear relation reduces to CSP in a tractable form; that every large-width honest distribution is hard; that nontrivial sheaf obstruction yields average-case one-wayness; that any current MORPH-F0 hypothesis is new or PQ secure.

**Next:** apply these exact no-go tests to [three HOLD hypotheses](F0-hypothesis-ledger.md) before any new source samples. Full per-family [15 fields](../97-morph-r0-cross-line-postmortem.md#11-re-entry-gate-for-any-new-morph-family), independent positive Field 15 and unconditional honest distribution are still mandatory. No trapdoor/PKE/KEM or implementation branch.
