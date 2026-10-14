# N1-58 - anchored symmetric principal minors (analytic no-go)

**Date:** 2026-10-14. **Global:** NO NOMINATION. **Outcome:** ANALYTIC REJECT before code; **0 empirical cases**.

Original complete 15-field research proof was recorded first as [#196 comment 6176025206](https://github.com/StanleyLl0yd/morph-kem/issues/196#issuecomment-6176025206). This document transcribes that source, not independent numerical revalidation. No new empirical sample, implementation, crypto candidate or rescue of historical partial research.

## N1-58 (2026-10-14): anchored principal-minor transcript - public signed-switching matrix section (ANALYTIC REJECT)

**New independent algebraic family:** determinant/principal-minor geometry of symmetric matrices, different from N1-56 cyclic bispectrum and N1-57 affine Radon tomography. The honest secret carries many independent off-diagonal signs, but the public accepted fibre contains an easy canonical representative. **Complete 15-field pre-code attack screen, no experiment and GLOBAL NO NOMINATION.**

### All 15 MORPH-R0 fields

1. **PublicInstance:** integer n>=3, public field F_5, labeled d_i for i in {0,...,n-1}, all 2x2 principal minors `p_ij` for 0<=i<j<n, and all 3x3 principal minors `t_0ij` for 1<=i<j<n, of a symmetric hidden matrix M over F_5. Only triangles **anchored at vertex 0** are published; no unreported full-minor assumption.
2. **Secret/Witness:** planted symmetric M with arbitrary diagonal entries d_i in F_5 and every off-diagonal m_ij in {+1,-1} subset F_5. Any symmetric matrix Y of **the same restricted domain** with all public minors equal is a valid witness.
3. **Generation distribution:** independently sample all d_i uniformly from F_5 and all m_ij for i<j uniformly from {1,4}; set m_ji=m_ij; compute all required exact determinant residues. No conditioning, hidden planted graph, rejection or resampling. Source, public output O(n^2) residues, determinant computation and exact verifier are polynomial in n and bitlength.
4. **Public verifier:** check n, symmetry, diagonal and off-diagonal domain; recalculate every d_i, every `det Y[{i,j}]` and every `det Y[{0,i,j}]` modulo 5; accept iff equal P. Runtime polynomial.
5. **Attacker-equivalence target:** `Equivalent(P)={Y symmetric over F_5, Y_ij in {+1,-1} for i!=j : all required 1/2/anchored-3 minors equal P}`. Any Y wins, NOT necessarily planted M.
6. **Stabilizer/fibre:** simultaneous row/column sign switch `M -> D M D` where D=diag(1,s_1,...,s_{n-1}) and every s_i∈{±1} leaves ALL principal minors unchanged because det(D_I)^2=1. All honest matrices have nonzero m_0i, so switches act freely. By the explicit reconstruction below, every accepted matrix is one of these switches, hence **exact fibre size 2^(n-1)**.
7. **Known algebraic representations:** symmetric principal minor assignment problem, determinant identities for 3x3 matrices, signed complete-graph switching equivalence, determinantal point process kernel equivalence; fully mature inverse-algebraic problem.
8. **PUBLIC CANONICAL SECTION:** construct Y_ii=d_i, `Y_0i=Y_i0=1`. For 1<=i<j<n, set
   `Y_ij=Y_ji= (t_0ij - d_0 d_i d_j + d_0 + d_i + d_j)/2 in F_5`.
   The expansion
   `det M[{0,i,j}] = d_0 d_i d_j - d_0 m_ij^2 - d_i m_0j^2 - d_j m_0i^2 + 2 m_0i m_ij m_0j`
   simplifies (all m^2=1) to `d_0 d_i d_j - d_0-d_i-d_j+2 m_0i m_ij m_0j`. Thus the public formula yields `Y_ij=m_0i m_ij m_0j ∈{±1}`; all 2-minors are `d_i d_j-1` and all anchored 3-minors match exactly. Equivalently Y=D M D for D_ii=m_0i (i>0), D_00=1. Inverse of 2 exists mod5. O(n^2) field operations return an ORIGINAL-VERIFIER accepted witness on every honest P.
9. **Local/low-weight:** each anchored triangle exposes its sign product `m_0i m_ij m_0j`; knowing a public spanning star fixes a gauge and lets the attacker reconstruct every remaining edge. Full determinant complexity is unnecessary.
10. **Noise/optimization:** no noise, only exact F_5 minors and hard off-diagonal {±1} domain. Zero edges, magnitude-unknown entries, sparse anchor graph or unconstrained non-symmetric matrices are different relations; cannot infer polynomial sections for all.
11. **Cover/base/fibre:** signed-graph switching is the explicit gauge quotient, with the star rooted at 0 providing a public section. This is not a secret lift, covering-space obstruction, or cryptographic trapdoor.
12. **Matched weak control:** singleton and pair minors of the SAME sampled M are a weak public control, hiding all 3-cycle sign products; no solver runs or claims about computational difficulty. Full anchored-triangle inverter succeeds identically.
13. **Validation:** ZERO source samples, frozen empirical slices or implementation. Algebraically rejected before source enumeration; N1-52 report of 593,305 exact heterogeneous cases plus 40 controls remains unchanged.
14. **Quantum:** classical deterministic polynomial any-witness inversion dominates, so no quantum hardness target survives in the specified domain.
15. **Independent Field-15 novelty:** **FAIL**. Symmetric principal-minor assignment and efficient canonical representative algorithms are well established: [Rising, Kulesza, Taskar, An efficient algorithm for the symmetric principal minor assignment problem, Linear Algebra Appl. 473 (2015)](https://doi.org/10.1016/j.laa.2014.04.019); [Griffin, Tsatsomeros, Principal minors Part II (2006)](https://doi.org/10.1016/j.laa.2006.04.009); [Brunel, Urschel, Recovering a magnitude-symmetric matrix from its principal minors (2024)](https://doi.org/10.1016/j.laa.2024.09.004). Our F_5, {±1}, anchored-three restriction and reconstruction identity are stated and proved **directly here**, not attributed as verbatim to these references.

### Scope and verdict

For honest P, all off-diagonal entries reconstructed by the formula lie in {±1}. The original M is in the accepted fibre but not necessary to recover; all 2^(n-1) switches pass. The root-normalized Y is the UNIQUE member with Y_0i=1. Public input/output and exact algebra are polynomial. No claim about general principal-minor systems with different field/domain/zero patterns, sparse measurements or unspecified matrix classes.

**N1-58 ANALYTIC REJECT, GLOBAL NO NOMINATION. Next independent positive Field-15 mathematical gate N1-59.** Do not code a KEM, PKE, trapdoor, claim OWF/PQ hardness, increment historical experiments, fix N1-19/23 PARTIAL, reclassify N1-26 HOLD or restart HEPMR #195 AP sweeps.