# N1-57 - finite-affine Walsh/Radon public inverse (analytic no-go)

**Date:** 2026-10-14. **Global:** NO NOMINATION. **Outcome:** ANALYTIC REJECT before code; **0 empirical cases**.

Original complete 15-field research proof was recorded first as [#196 comment 6176006953](https://github.com/StanleyLl0yd/morph-kem/issues/196#issuecomment-6176006953). This document transcribes that source, not independent numerical revalidation. No new script, experiment, case count or KEM code.

## N1-57 (2026-10-14): binary-affine hyperplane sum transcript - exact Walsh-Radon inverse (ANALYTIC REJECT)

**Independent mathematical family:** finite affine-geometric tomography / Radon transformation, not N1-56 cubic cyclic bispectrum, N1-55 p-adic valuation, N1-54 state-space realization. Entire observation vector has polynomial bitlength measured in its underlying signal support N=2^d. **Full 15-field pre-code screen, zero experimental cases. GLOBAL NO NOMINATION.**

### MORPH-R0 all 15 fields

1. **PublicInstance:** d>=2, N=2^d; all pairs of labeled ternary residues `H(u,b) in F_3`, indexed by every nonzero `u in F_2^d` and both `b in F_2`, generated as `H(u,b)=sum_{x in F_2^d: u·x=b} f(x) mod 3`. Source values live in F_3, directions in F_2: do **not** confuse their field characteristics.
2. **Secret/Witness:** planted table `f: F_2^d -> F_3`. Any candidate `g` with exactly equal hyperplane sums on every labeled (u,b) is accepted.
3. **Generation distribution:** independently sample all N values f(x) uniformly in F_3; compute all H(u,b). There is no rejection, conditioning or hidden solvability filter. A naive exhaustive evaluation uses O(N^2 d) elementary bit/field operations, polynomial in N and output size Theta(N), even though N is exponential in short parameter d. All output residues have constant bitlength.
4. **Public verifier:** check candidate table length N, each F_3 value, recompute all 2(N-1) exact mod-3 hyperplane sums; accept iff all equal public H. Runs in poly(N) time, no numeric tolerance.
5. **Equivalent(P):** `{g:F_2^d->F_3 : forall u!=0,b in F_2, sum_{x:u·x=b} g(x)=H(u,b) in F_3}`. Any such g is attacker success irrespective of planted source.
6. **Stabilizer/fibre:** complete labeled nonzero directions distinguish all Walsh components. Every honest instance has **exactly one** acceptable vector f, reconstructed by Field 8; no nontrivial hidden kernel or translation ambiguity.
7. **Known quotients/representations:** finite Radon/X-ray transform, Walsh-Hadamard Fourier transform on F_2^d, Fourier-slice theorem for affine hyperplane sums; classical inverse tomography.
8. **Public section/inverter:** for every u!=0, set `T(u)=H(u,0)-H(u,1) in F_3`. This equals `sum_x (-1)^{u·x} f(x)`, where -1 is the element 2 of **F_3**. Set `S=H(v,0)+H(v,1)` for any fixed public v!=0, so `T(0)=S`. Define for each x `g(x)=N^{-1} sum_{u in F_2^d}(-1)^{u·x}T(u) in F_3`. Since N=2^d is nonzero mod 3, N^-1 exists. Orthogonality `sum_u (-1)^{u·(x+y)}=N [x=y]` holds in F_3, so g=f **exactly**; original verifier accepts on every honestly generated instance. Direct O(N^2 d) bit/field work; fast Walsh transforms are not necessary.
9. **Local / low-weight:** each pair H(u,0),H(u,1) reveals one Walsh character sum and the shared total S; the full direction list is a complete public Fourier coordinate system.
10. **Noise:** none. Modulo-3 sums, rather than integer sums or inequalities, are part of the exact fixed relation; incomplete directions, nonlinear projection filters, missing rows or additive noise require a different 15-field test.
11. **Cover/base/fibre:** each hyperplane partition is public; the transforms reveal the full dual character basis, so no hidden covering space, lift or geometric secret remains.
12. **Matched weaker control:** one public direction v and its two H values from the exact same planted f is a natural incomplete-angle control; it has a large affine solution space. No empirical control run or hardness claim is made; the mandatory complete-direction inverse wins.
13. **Validation:** no samples, scripts, solver timeouts, counted cases or pre-registration runs, as Field 8 rejects analytically. Do not increment frozen N1-52 reported 593,305 exact heterogeneous cases +40 larger controls.
14. **Quantum:** polynomial exact classical inverse makes quantum inversion claims irrelevant for the stated public relation.
15. **Why-not-mature / novelty:** **FAIL**. Finite Radon transform is an established family with exact inverse algorithms and Fourier-slice method. Prior art: [Averbuch and Shkolnisky, 3D Fourier based discrete Radon transform, ACHA 2003](https://doi.org/10.1016/S1063-5203(03)00030-7); [Kingston and Svalbe, Discrete Radon transform has an exact, fast inverse, PNAS 2006](https://pmc.ncbi.nlm.nih.gov/articles/PMC1697830/); [Walsh transformation for binary spaces](https://link.springer.com/article/10.1007/s12095-021-00529-4). The F_3-on-F_2^d specialization above is proved directly; these citations establish established **mathematical family**, not necessarily this precise formula in verbatim form.

### Exact proof and boundary

Partition F_2^d into u·x=0 and u·x=1, subtract their ternary sums to obtain the Walsh coefficient. Recover the shared DC coefficient by adding the two bins. Inverse the full Walsh matrix in F_3 because its square is N I (N is a unit). No search, plant recovery oracle, probabilistic attack, sampling or special parameter trick is needed. The proof only covers **complete labeled affine hyperplane sums in characteristic 3 over binary affine space**; sparse-angle tomography and geometric threshold observations are not claimed easy.

**N1-57 ANALYTIC REJECT, GLOBAL NO NOMINATION.** Preserve N1-19/N1-23 PARTIAL, N1-26 HOLD/BENCHMARK and HEPMR #195 BENCHMARK ONLY through AP103. No cryptographic implementation, KEM/PKE/trapdoor, OWF/PQ/security claims. Next independent Field-15 screen N1-58.