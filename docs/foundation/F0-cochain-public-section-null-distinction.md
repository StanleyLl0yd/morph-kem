# MORPH-F0: exact public cochain section, large H² and null separation

**2026-10-22. Source-first attack on a precisely specified H-B subclass; ANALYTIC REJECT for this subclass, not for all local-to-global relations. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD as broad hypotheses; D0 HOLD/DEFER; planted-TI FROZEN comparator.** No N1-60/F0-K/A-ID, new crypto primitive, implemented attack suite or candidate parameterization.

## 1. Full public local-to-global inversion interface

Let \(\mathbb F_q\) be an effectively represented finite field with polynomial-bitlength arithmetic. The honest source outputs an explicitly listed finite oriented 2-dimensional simplicial complex \(K\) of polynomial size, with \(e\) edges and \(f\) oriented triangles. Its conditional generator then samples an edge 1-cochain \(x\in C^1(K;\mathbb F_q)\cong\mathbb F_q^e\) by **any** polynomial-time distribution, and publishes
\[
P=(K,b),\qquad b=\delta^1_K x\in C^2(K;\mathbb F_q)\cong\mathbb F_q^f.
\]
The public coboundary matrix \(D=\delta^1_K\) is the signed face-by-edge incidence matrix:
\[
 (Dy)_{[a,b,c]}=y_{[b,c]}-y_{[a,c]}+y_{[a,b]}.
\]
Orientations are public, and in characteristic two signs coincide as required. The **full original accepted-witness relation**, with no extra hidden compatibility or minimality tests, is
\[
\operatorname{Equivalent}(P)=\{y\in\mathbb F_q^e:Dy=b\}.
\]
The attacker wins with **any** accepted edge cochain, not necessarily the planted x. Every generator draw is admitted; no tensor conditioning, 2-cocycle rejection, promise of trivial topology or secret-dependent filter occurs. The public complex may be chosen by any polynomial generator independent of x or as part of a joint conditional source; the statements below are pointwise for **each** public K with b in its generated image.

## 2. Exact pointwise original-verifier public section

**Theorem 1 (explicit abelian gluing NO-GO).** For every public \(P=(K,b)\) in the **unfiltered honest image**, Gaussian elimination on \(Dy=b\) outputs a fully verifier-accepted y in time polynomial in \(e+f+\log q\). Let \(r=\operatorname{rank}_{\mathbb F_q}D\). The exact original accepted fibre is the affine coset \(y_0+\ker D\), with
\[
\boxed{|\operatorname{Equivalent}(P)|=q^{e-r}.}
\]
This holds even if K has arbitrarily large first- or second-cohomology groups, cycles, arbitrarily large graph treewidth, complicated 2-dimensional gluing, or many distinct gauge representatives.

**Proof.** By the honest law, \(b=Dx\) so the public system is consistent for every sample. Row reduction finds some y with Dy=b and the full verifier tests precisely this equality. Every accepted y differs from a solution y0 by a member of ker D. Rank-nullity yields \(\dim\ker D=e-r\). In particular \(\dim H^2(K;\mathbb F_q)\) does not obstruct the inverse task for a *published exact coboundary*. QED.

**Extensions with public constraints.** If the original verifier *also* checks explicitly represented public **affine-linear** edge conditions \(Ay=t\), and the honest generator publishes t=Ax, simply stack \([D;A]y=[b;t]\). The same argument gives an exact fibre of size \(q^{e-\operatorname{rank}[D;A]}\). Nonlinear admissible witness sets, quantum phases with nonlinear support, unexpanded succinct local alphabets, nonabelian constraints or a compressed exponentially large complex are **outside** this theorem.

## 3. Exact planted/null distribution and topology inversion warning

Suppose additionally, **conditional on the public K**, the honest generator samples x uniformly in \(\mathbb F_q^e\). Then \(b=Dx\) is exactly uniform on \(\operatorname{im}D\), a public r-dimensional subspace of \(\mathbb F_q^f\). Against a *different* null law in which b is uniform in **all** \(\mathbb F_q^f\), the exact total-variation distance conditional on K is
\[
\boxed{\operatorname{TV}(\operatorname{Unif}(\operatorname{im}D),
                       \operatorname{Unif}(\mathbb F_q^f))
=1-q^{r-f}.}
\]
The public membership test \(b\in\operatorname{im}D\), computable by the same Gaussian elimination, has **honest true-positive 1** and **null false-positive \(q^{r-f}\)**. The formula does **not** compare against a null law *already conditioned to be an exact coboundary*, nor against a hidden nonlinear globally feasible distribution. It establishes **easy detection** as well as exact full-verifier inversion for this specified source.

For an explicitly represented 2-dimensional complex, \(C^3=0\), so \(H^2(K;\mathbb F_q)=C^2/\operatorname{im}\delta^1\) and \(\dim H^2=f-r\). Thus when cohomology is large, the distance to the unrestricted null **increases**, yet finding an honestly generated accepted witness remains polynomial. Both conclusions follow from public linear algebra, not cryptographic hardness.

## 4. Tiny independently checkable finite control

Take K as the boundary of a tetrahedron, with vertices 0,1,2,3, six public oriented edges and four oriented triangular faces. Over \(\mathbb F_2\), its public incidence matrix in ordered edge basis (01,02,03,12,13,23) and face basis (012,013,023,123) is
\[
D=\begin{pmatrix}
1&1&0&1&0&0\\
1&0&1&0&1&0\\
0&1&1&0&0&1\\
0&0&0&1&1&1
\end{pmatrix}.
\]
It has rank r=3. Hence **each** of the \(2^3=8\) accepted face-vector targets b has exactly \(2^{6-3}=8\) accepted edge cochains. The eight image targets are exactly the four-bit vectors of even parity; a uniform unrelated null target among the \(2^4=16\) face vectors passes the image gate with probability 1/2, and conditional TV is 1/2. A separate finite scratch enumeration over all \(2^6=64\) binary edge vectors gave precisely 8 output values, each occurring 8 times. This is **small analytic arithmetic control**, not a committed attack implementation, validated crypto source campaign, measured runtime or security parameter.

## 5. Explicit prior art and limits

Cellular/finite cochain algorithms and chain-complex reductions are longstanding: [Kaczynski–Mischaikow–Mrozek, *Computational Homology* (2004)](https://link.springer.com/book/10.1007/b97315). Local-to-global / contextuality obstructions and their **linear-algebraic** treatment are established: [Abramsky–Brandenburger (2011)](https://arxiv.org/abs/1102.0264); [Abramsky–Mansfield–Barbosa (2011/2012)](https://arxiv.org/abs/1111.3620). For cohomology in finite-group extensions and more demanding nonabelian settings see [Grochow–Qiao, *Algorithms for Group Isomorphism via Group Extensions and Cohomology*](https://doi.org/10.1137/15M1009767) and [Flannery–O'Brien (2000)](https://doi.org/10.1080/00927870008826937). The finite affine cochain inversion statement is an **elementary corollary** of known linear algebra, and is also an F0-K2-type screen, **not a claim of mathematical priority**.

**Invalid inferences explicitly excluded:** (i) nontrivial H² for K does not mean honest exact b fails to lift; (ii) a cohomological *obstruction detecting absence of a global section* on some ungenerated profiles is not a hardness statement for searching on *generated* profiles; (iii) nonlinear compatibility, a nonabelian cocycle problem, succinct objects or large alphabet cannot be silently replaced by this linear model; (iv) hard planted-x recovery is irrelevant if some y accepted by Dy=b exists.

## 6. Disposition and remaining genuinely independent search burden

**Exact public affine/cochain H-B subclass: ANALYTIC REJECT. Broad H-B: HOLD.** Source-first finite-complex linear holonomy, explicit vector-space stalks and affine public restrictions do **not** supply an independent difficult inversion relation. Additional enlargements of genus, cohomology dimension, polynomial number of local patches, or graph width **without changing the original nonlinear verifier** are not a research opportunity.

The *next* substantive task is **not another scalar cochain variant**. Before reopening H-B, require an independently sourced **nonlinear** local-to-global object with polynomial honest generator, a full public original any-witness relation, exact public presentation (including the true alphabet and overlap costs), a proven absence of this affine public section *in the claimed class*, serious finite-CSP/group-cohomology/gauge and quantum screens, and independently supported MORPH-R0 Field 15. Until then H-B is HOLD and no experiments, N1 allocation, or KEM/OWF conjecture are authorized.
