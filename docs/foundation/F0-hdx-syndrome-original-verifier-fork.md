# MORPH-F0: higher-dimensional-expander code syndrome inversion is an old verifier fork

**2026-10-22. Independent source/literature intake of explicit recent coding-theory objects, NOT an independently novel cryptographic inverse problem.** This is an exact original any-witness screen and conditional source accounting, not the design or security proof of a code-based primitive. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; D0 DEFER, D1 HOLD, D2 graph-cover screened, planted-TI FROZEN; N1-60 unallocated. No new code, attack ID, tests, benchmarks, parameters or sample campaign.

## 1. Independently sourced object, fully specified public interface

Recent **mathematical code constructions** based on high-dimensional expanders include [Dinur–Liu–Zhang, *New Codes on High Dimensional Expanders*, CCC 2025](https://doi.org/10.4230/LIPIcs.CCC.2025.27), [Dinur–Evra–Livne–Lubotzky–Mozes, *Good Locally Testable Codes*, Annals of Mathematics, 2026](https://doi.org/10.4007/annals.2026.203.2.3), and [Oppenheim–Valentiner-Branth, *New cosystolic high-dimensional expanders from KMS groups*, 2025](https://arxiv.org/abs/2504.05823). Their results concern mathematical expansion, code distance/rate/testability and constructions; **none of these properties alone is an average-case inversion theorem or a new crypto hardness assumption**. The present theorem applies only after the relevant construction has been **explicitly represented by a publicly computable binary linear parity-check matrix**, and does NOT assert that every referenced code is binary or uniformly samplable at the desired security size.

Let an unconditional polynomial-time source choose a public binary matrix \(M\in\mathbb F_2^{m\times n}\), possibly computed from an explicit polynomial-size HDX/code construction; n,m and the bitlength of M are polynomial in the security parameter. Fix a public weight budget \(0\le w\le n\), and have the honest source choose a planted error \(e\in\mathbb F_2^n\) by **any explicitly declared polynomial-time distribution** supported on Hamming weight \(\mathrm{wt}(e)\le w\), then publish \(P=(M,b=Me,w)\). This is **unfiltered**: no rank conditioning or postselected syndromes; every source output is honestly satisfiable.

A completely explicit *strict-polynomial random-bit example* of such a source is n=2^a, independently select w a-bit indices \(I_1,\ldots,I_w\) uniformly, and let \(e=\sum_{j=1}^w\mathbf 1_{I_j}\) over \(\mathbb F_2\). Its weight is at most w, with collisions allowed and exactly accounted for by its true (not generally uniform fixed-weight) distribution. **Do not replace this honest law** by independent uniform weight-w errors without changing the source.

The **full original verifier must be fixed before any hardness claim**. Two distinct choices are:

1. \(V_{\mathrm{linear}}(P,y)=[y\in\mathbb F_2^n\ \land\ My=b]\): every consistent syndrome witness wins, **no weight check**.
2. \(V_{\mathrm{sparse}}(P,y)=[y\in\mathbb F_2^n\ \land\ My=b\ \land\mathrm{wt}(y)\le w]\): any small-weight witness wins, not necessarily the planted e.

These are **different inversion problems** on the same published data. The second is the standard bounded-weight **syndrome decoding search relation**, not a new relation created by topology.

## 2. Full public attacks and exact original accepted fibres

**Theorem 1 (unrestricted NO-GO).** For every unfiltered honest tuple \(P=(M,b,w)\), the public system \(My=b\) is consistent, so Gaussian elimination returns a **fully originally accepted** witness for \(V_{\mathrm{linear}}\) in polynomial time, regardless of code dimension, expansion, locally testable properties, girth, number of high-dimensional faces, or the distribution of e. For \(r=\operatorname{rank}_{\mathbb F_2}M\), the exact full unrestricted accepted fibre has
\[
\boxed{\#\{y:My=b\}=2^{n-r}}
\]
members on every honest instance. The attacker never needs to identify the planted e. This is the existing F0-K2 linear public-section mechanism, **not an independently novel theorem**.

**Theorem 2 (bounded weight is a genuinely different, already known task).** Under \(V_{\mathrm{sparse}}\), public Gaussian elimination **alone** is insufficient: it can output weight>w and be rejected. The complete accepted fibre is
\[
\boxed{\operatorname{Equivalent}_{\le w}(P)=
\{y\in\mathbb F_2^n: My=b,\ \mathrm{wt}(y)\le w\},}
\]
and finding any member is precisely bounded-weight syndrome decoding for the explicitly distributed public matrix M and honest reachable syndrome b. This is longstanding coding theory: [Berlekamp–McEliece–van Tilborg (1978)](https://doi.org/10.1109/TIT.1978.1055873) proved a worst-case NP-completeness result for the general decoding **decision** problem, which does **not** prove difficulty of this particular **planted** matrix/error distribution. Standard information-set decoding and modern code-based attacks must be compared for any such source.

**Fixed-weight easy boundary:** if w is a fixed constant independent of security size, enumerate each support \(S\subseteq[n]\) with \(|S|\le w\), solve the public restricted linear system \(M_Sy_S=b\), insert zeros elsewhere and run the entire sparse original verifier. Because a planted support is present, some S is feasible. The number of supports \(\sum_{j=0}^w\binom nj=O(n^w)\), and each solve is polynomial. Thus **all constant-weight honest sources of this interface are polynomially invertible**, even when M comes from a complicated high-dimensional expander. This statement covers no growing-weight security family.

## 3. Full honest-source posterior versus any accepted witness

For an **additional explicitly different** mathematical model, if the source chooses e uniformly among the \(\binom nw\) binary vectors of **exact** weight w, define
\[
 A_w(z)=\#\{e:\mathrm{wt}(e)=w,\ Me=z\}.
\]
Then
\[
\boxed{\Pr[b=z\mid M,w]=\frac{A_w(z)}{\binom nw}},\qquad
\boxed{\Pr[e=x\mid b=z,M,w]=
\frac{\mathbf1_{\{\mathrm{wt}(x)=w,\ Mx=z\}}}{A_w(z)}}
\]
for \(A_w(z)>0\). These are **the actual conditional source law** for that exact-weight source, not universal rates for the earlier with-replacement example. They do not provide a polynomial algorithm for finding any solution. The original bounded-\(\le w\) accepted fibre can be **larger** than the posterior support, because it additionally allows witnesses of smaller weight. A hardness argument about identifying the sampled exact-weight e therefore remains different from winning the original accepted-witness game.

**Null distinction:** under any honest sparse source, b always lies in the publicly computable image im M. If an independently specified comparison null samples b uniformly in **all** \(\mathbb F_2^m\), the polynomial row-reduction membership detector has honest true-positive one and null false-positive \(2^{r-m}\). This is only a **lower bound** \(1-2^{r-m}\) on full planted/null TV for arbitrary sparse sources, not an equality unless the planted b is uniform in im M. In particular, do not claim a secure pseudorandom output merely from expansion or high source entropy.

## 4. Independent tiny exact control (not a sample campaign)

Over \(\mathbb F_2\), take
\[
M=\begin{pmatrix}1&1&0&0\\0&1&1&0\end{pmatrix},\quad w=2.
\]
It has rank 2. The six exact-weight-two vectors map to the three nonzero syndromes 01,10,11 **with multiplicity exactly two each**; 00 receives no exact-weight-two input. Therefore the exact-weight posterior of e at any reachable b has two members, while the full unrestricted verifier accepts **four** linear solutions for each b (2^{4-2}=4). Moreover at b=00, the sparse-\(\le2\) verifier accepts y=0000 although that b is not generated by the uniform exact-weight-two source. This arithmetic control isolates the difference between a source's posterior support and a verifier's full accepted fibre. No experiment implementation, committed test, cryptographic benchmark or empirical attack success rate is claimed.

## 5. Literature prior art, disposition and actual positive gate

The 2025–2026 HDX/code publications above are substantial independent **coding-theory** developments. However the **inverse problem** “find a small-weight y with My=b” is the mature syndrome-decoding relation, regardless of whether M was described via triangles, stalks, KMS coset geometry or parity checks. **A new code ensemble is not automatically a new mathematical hardness assumption.** It may still have interesting **source-specific** decoding hardness or algebraic vulnerabilities requiring separate cryptanalysis, but neither worst-case hardness, code testability, local spectral expansion nor these source-fibre identities establishes post-quantum security or positive independent MORPH-R0 Field 15.

**D3 outcome:** verifier without weight **ANALYTIC REJECT** (Gaussian); sparse verifier with constant weight **ANALYTIC REJECT** (support enumeration); sparse verifier with growing weight **KNOWN CODE-BASED PROBLEM / NOT INDEPENDENTLY ADMITTED**, not declared either easy or secure. Do not allocate a new N1 stage, implement a new “topological” KEM, or propose larger weights as a novelty rescue. Re-entry requires a **mathematically distinct** public any-witness relation with complete original source and affirmative Field-15 literature differentiation, *not* merely a different source of code parity checks.
