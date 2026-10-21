# F0: complete dual-number singular any-witness fibre screen

**2026-10-21. Bounded analytic D0 negative gate, no new cryptographic foundation.** Follows the [finite-ring smooth lifting theorem](F0-deformation-tower-public-lift-screen.md) and the [foundation pivot](F0-independent-foundation-pivot-2026-10-21.md). GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; N1-60 unallocated; no source experiments or implementations.

## Exact complete-source original-verifier relation

Over \(R=\mathbb F_q[\epsilon]/(\epsilon^2)\), with effective finite field and explicitly polynomial-size public arithmetic circuit \(F:R^v\to R^w\), the *unconditional* polynomial honest generator samples \(s\) by any specified distribution, publishes \(P=(F,b=F(s))\) and the original verifier accepts **any** \(y\in R^v\) satisfying \(F(y)=b\). The attacker need not recover s. The theorem is for the full affine domain, not extra subgroup restrictions; other domains require separate lift closure and full verification.

Write \(b=b_0+\epsilon b_1\), \(y=z+\epsilon u\), with \(z,u\in\mathbb F_q^v\). Let \(\bar F(z)=F(z)\bmod\epsilon\); \(c_F(z)=[\epsilon]F(z)\) for the canonical constant lift; and \(J_z=D\bar F(z)\in\mathbb F_q^{w\times v}\). All of these are publicly polynomial-time computable for any supplied z.

**Theorem (full fibre identity, arbitrary singular Jacobian):**
\[
\boxed{\operatorname{Equivalent}(F,b)=\bigsqcup_{\bar F(z)=b_0}
\{z+\epsilon u:J_zu=b_1-c_F(z)\}.}
\]
In particular,
\[
\boxed{\#\operatorname{Equivalent}(F,b)=
\sum_{\bar F(z)=b_0}
{\bf1}\{b_1-c_F(z)\in\operatorname{im}J_z\}
q^{v-\operatorname{rank}J_z}.}
\]
**Proof:** Since \(\epsilon^2=0\), each polynomial circuit has an *exact* linearization \(F(z+\epsilon u)=F(z)+\epsilon J_zu\). Matching coefficients of \(1,\epsilon\) is necessary and sufficient for the complete original verifier. Every full-ring vector has a unique pair \((z,u)\); the solution space of a consistent rank-r linear system over \(\mathbb F_q\) has exactly \(q^{v-r}\) members. Sum the disjoint residue fibres. QED.

**Unseeded public inversion corollary:** if an explicit public polynomial-time procedure outputs a polynomial-size **complete list** of residue roots \(z\) to \(\bar F(z)=b_0\) on honestly generated inputs (or an incomplete list guaranteed to contain at least one root whose displayed affine lift system is solvable), attempt each z, solve the linear system and verify every original equation. The attacker then finds **some accepted witness on every such input**, including when *all* residue Jacobians are singular. If this list guarantee applies to an unconditional honest-source event of probability at least \(1-\delta\), success is at least \(1-\delta\). The theorem does **not** construct an efficient list of roots for arbitrary hard residue systems; a small output list is a substantive precondition, not a consequence of the planted generator.

**Small complete finite counterexample:** Over \(\mathbb F_2[\epsilon]/\epsilon^2\), choose \(F(x)=x^2(x-1)\), \(b=\epsilon=F(1+\epsilon)\). The residue equation has two roots z=0 and z=1. At z=0, \(J_0=0,c_F(0)=0\), and \(0\cdot u=1\) has no solution; at z=1, \(J_1=1,c_F(1)=0\), and u=1 is the unique correction. Hence the exact full-ring accepted fibre has **one** element despite two field roots. Independent scratch enumeration of all four ring elements gives \(F^{-1}(0)\) of size three and \(F^{-1}(\epsilon)\) of size one; no repository test/benchmark or experimental cryptographic sample was made.

## Prior art, failure boundaries and research stop rule

This is *standard square-zero/Hensel linearization*, not an independent mathematical discovery: [Grochow, rectangular multivariate Hensel lifting](https://doi.org/10.1080/00029890.2024.2440297), [Stacks Project, formal smoothness](https://stacks.math.columbia.edu/tag/02GZ) and [Kamche–Kalachi, equations over finite commutative rings](https://link.springer.com/article/10.1007/s00200-024-00652-8). Existing nearby algebra/isomorphism problems have substantial independent prior work: [Grochow–Qiao, Tensor Isomorphism-completeness](https://doi.org/10.1137/21M1441110), [Grochow–Qiao–Stange–Sun, Tensor/Group/Polynomial Isomorphism V: **Over Commutative Rings**, STOC 2025](https://doi.org/10.1145/3717823.3718286), [Li et al. 2026 average-case algorithms](https://arxiv.org/abs/2604.00591), and [Gerstenhaber, deformation theory (1964)](https://doi.org/10.2307/1970484). No affirmative Field-15 distinction follows from encoding familiar isomorphism/CSP problems over local rings.

The exact global fibre formula is **specific to depth two**. At depth \(k\ge3\), choices among singular first-order lifts may affect later solvability; one cannot independently multiply per-stage counts. The [previous full-row theorem](F0-deformation-tower-public-lift-screen.md) still applies to arbitrary polynomial depth. Absence of a short residue-root list is **not** proof of average-case difficulty or post-quantum security.

**D0: HOLD / DEFER; bounded local-ring screen complete.** Do not produce another nilpotent-depth/rank-parameter variant without a **specific independently sourced mathematical obstruction** passing explicit polynomial source and public bitlength, original any-witness equivalence, all public normal forms, literature reduction/quantum screen and positive MORPH-R0 Field 15. Otherwise prioritize a genuinely different object, not a disguised TI-complete problem. No OWF/PKE/KEM, no new canonical N1 stage, no further local-ring experiment campaign.
