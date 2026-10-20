# MORPH-KEM research log

## 2026-10-20 - Randomized greedy public flags: stronger finite-source search attack

[Randomized full-public tensor isotropic-flag search](../docs/foundation/F0-planted-ti-randomized-flag-search.md) uses public uniform projective extensions inside S_A(U)/U and applies the original full any-witness verifier to terminal completions. Instead of postselection of an adaptively drawn T, the proof averages uniform mt-by-c rank tails over **all precommitted true flags**. At most delta=t*C_q*q^(-(r+1)^2)+q^(-s)/(q-1) of their expected fraction fail prefix/terminal rank screens; the actual public algorithm hits a good true flag with probability >=G(A,H)*q^(-E_t-(r+1)t), E_t=sum_{k<t}(c-mk)_+. Markov on the bad-flag fraction plus independent public restarts gives high honest-source success after explicitly bounded work. Fixed q, d/n->alpha<1/2,m~n/logn: upper leading work exponent c²/(2m)+o(n²/m), versus (cn-c²/2)/m of prior deterministic flag enumeration, **still q^(O(nlogn)), not polynomial or proven novel against all existing generic methods**. Independent exact toy GF(2),n4,d2,m2 flag-landing probability 93/896 (all 1024 honest tuples, scratch only); no committed code/corpus. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; no A-ID/N1-60/F0-K reservation or candidate.

## 2026-10-20 - Public isotropic-flag seed search: exact source-aware enumeration bound

[Isotropic-flag full-tensor attack refinement](../docs/foundation/F0-planted-ti-isotropic-flag-search.md) traverses only public simultaneously isotropic subspace flags, extending U by lines of S_A(U)/U; every terminal completion is checked by the unchanged full any-witness verifier. For each dimension k the traversal has exactly F_k Z_k nodes, where Z_k counts valid k-planes and F_k is the number of internal complete flags. A finite Gaussian-intersection sum gives E_honest Z_k exactly for every hidden-H prior. Fixed-seed completion yields the same unconditional honest-source success bound as PR #243; the new expected-work bound is poly*sum_k F_k E Z_k. At fixed q,d/n->alpha<1/2,m~n/logn,t~c/m the **upper leading q-exponent** drops from cn/m to (cn-c²/2)/m, still q^(O(nlogn)), not a polynomial inverter or a new complexity class. Independent scratch GF(2) exact tuple enumeration checks (n,d,m)=(4,2,1),(4,2,2),(5,2,1); no committed code/tests/attack samples. No new candidate, N1/A-ID/F0-K or positive Field 15. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.



## 2026-10-20 - Full-public-tensor planted tangent rigidity and exact wrong-witness incidence

[Full-source algebraic geometry screen](../docs/foundation/F0-planted-ti-global-incidence-and-tangent-rigidity.md) computes the exact conditional probability q^(-m r(2d-r-1)/2) that a fixed rank-r tangent deformation lies in the Jacobian kernel; the number of such maps is [d choose r]_q [c choose r]_q |GL_r(q)|. For each different d-plane meeting H in dimension d-r, the exact acceptance probability has **the same** exponent and there are [d choose r]_q [c choose r]_q q^(r²) such planes. Thus the exact wrong-witness first moment and tangent-kernel first moment share a rank-by-rank incidence penalty. If Delta=m(d-1)/2-(n-1)>0, both nonuniqueness and tangent degeneracy probabilities are at most O(q^(-Delta)); for fixed q, d~alpha*n< n/2, m~n/logn, this is q^(-Omega(n²/logn)). This refines earlier #208 uniqueness work; it is **not** a polynomial full-public-tensor inverter, hardness result, source benchmark or novel Field-15 basis. Exact tiny GF(2) arithmetic cross-check, no committed code. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.

## 2026-10-20 - Public full-tensor seed-completion algorithm and exact source success

[Source-first full-public seed-completion attack](../docs/foundation/F0-planted-ti-public-seed-completion.md) gives a genuine any-witness algorithm: enumerate every public t-plane T, form S_A(T) as the simultaneous kernel of mt pairing equations, and emit it only if dim S=d and the entire original verifier accepts. For any *fixed seed* T<=H independent of the conditioned form draws, the quotient kernel is uniform mt-by-c, and its exact full-rank probability is prod_{j=0}^{c-1}(1-q^(j-mt)); the full rank distribution is also derived. Enumerating all [n choose t]_q seeds gives unconditioned honest-source success at least that probability for every H-prior and cost poly*[n choose t]_q. With d~n/C for C>=3 and m~n/logn and t=ceil((c+Omega(n))/m)=Theta(logn), success is 1-q^(-Omega(n)) at q^(O(nlogn)) cost, **the already known generic complexity class of Liu-Qiao-Tang-Zhang (2026), not a new polynomial-time inverse**. Tensor-adaptive T invalidates fixed-T conditional rank claims but not full-verifier certification. Exact GF(2) rank arithmetic only, no committed test or code. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.
This is the active compact chronological research log.

## 2026-10-19 - Rank-sensitive adaptive bivector-oracle query lower bound

[Source-first F0 adaptive linear-bivector query theorem](../docs/foundation/F0-planted-ti-adaptive-linear-bivector-probe-tv.md) strengthens the pair-query carrier result to oracle queries of arbitrary (even nondecomposable) bivectors. For any honest H-prior, full transcript TV <= Pr_null,H[L_null cap Lambda^2H != 0]. With uniform H, each projective query-space direction x of alternating rank s>=2 has containment probability [d choose s]_q/[n choose s]_q<=q^(-cs); rank-sensitive union bounds yield TV <= min(1,q^(Q-2c)) for <=Q adaptive m-vector queries. Thus constant oracle-only distinguishing advantage requires Q>=2c-O_q(1). Exact single-query TV=(1-q^(-m))*Pr_H(support(x)<=H). Independent toy GF(2),n=4,d=2,m=1 checks: rank-2 TV 1/70, rank-4 TV 0, two rank-2 directions joint TV 1/70. **Not** a theorem about an attacker given complete public matrices, any-witness inversion, or computational hardness; no actual attack corpus/code, new A-ID or N1 number. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.

## 2026-10-19 - Adaptive pair-oracle transcripts: null-carrier coupling and sparse TV bound

[New F0 adaptive query-span theorem](../docs/foundation/F0-planted-ti-adaptive-oracle-span-tv.md): for any prior pi on the hidden d-plane H and any adaptive algorithm seeing **only queried** alternating pair evaluations, full transcript TV is bounded by the null-run probability that the span of all queried vectors intersects an independent H in dimension >=2. For uniform H, this is a Gaussian intersection probability even though the query carrier is selected adaptively from answers; if the carrier is always <=u<=c=n-d, TV<= [d choose2]_q*[u choose2]_q/[n choose2]_q <= (4/9)q^(-2(c-u)). Independent exact tiny GF(2),n=4,d=2,m=1 adaptive example has TV=3/140 and bound 1/5. **This excludes full-public-tensor preprocessing, tensor-derived public kernels, and any original-verifier inversion claim.** No code, source instance, N1/A-ID/F0-K or novel Field-15 basis. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.

## 2026-10-19 - Joint TV of precommitted GL-invariant local views via their span

[Precommitted multi-view local-TV bound](../docs/foundation/F0-planted-ti-precommitted-multiview-span-tv.md) extends the prior exact one-random-T conditional law to a tuple of **GL-invariant** jointly sampled public subspaces independent of H and A. The entire joint list of restrictions is postprocessing of the full tensor restriction to their span S; conditional on dim S the span is uniform, so the **real** observation TV is at most the Gaussian-binomial augmented-H TV averaged over dim S. If dim S<=u<=c=n-d almost surely, TV<=(4/9)*q^(-2(c-u)), for any unconditional H-prior. In particular k independent uniform 2-plane probes are jointly quiet for 2k<=c-s, and arbitrary adaptive probing **within an initial independent random carrier S** is covered. This does **not** include selecting S from the published full tensor; a deterministic carrier equal to a known H can have TV near one. No full-tensor TV, original verifier inversion, new stage or crypto evidence. GLOBAL NO NOMINATION, H-A/H-B/H-C HOLD.

## 2026-10-19 - Exact TV for precommitted random TI tensor restrictions

[Random local-view theorem](../docs/foundation/F0-planted-ti-random-restriction-exact-tv.md) gives the exact **conditional** distribution of all m alternating forms restricted to a uniform random t-plane T independent of the public tuple: for fixed H and j=dim(T cap H), planted restriction is uniform on the codimension-binomial(j,2) space annihilating T cap H, while null restriction is uniform unrestricted. The exact augmented-H TV is the Gaussian intersection sum of (1-q^(-m*binom(j,2))), bounding the real (T,full restricted tuple) TV. For t<=c=n-d it is at most (4/9)*q^(-2(c-t)); every postprocessing of **one** such precommitted local view inherits this bound. At t=2 the **real public** TV is exactly (1-q^(-m))*[d choose2]_q/[n choose2]_q and an elementary public local isotropy test attains it. **No** adaptive/global full-tensor TV claim, polynomial multi-query amplification, full-verifier inverter, candidate or crypto evidence. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; N1-60 unallocated.

## 2026-10-19 - Exact planted third centered bivector moment and four quotient-line types

[Exact planted-source third-moment theorem](../docs/foundation/F0-dual-bivector-planted-third-central-moment.md) extends PR #236's null third-moment correction and the previous planted quotient-line fibre variance: quotient projective lines with three supported directions fall into exactly four types (Segre A, same-P affine rank-one, same-P affine rank-two, compatible transverse-pencil). Weighted ordered collinear triples yield a finite **closed Gaussian-binomial expression** for the planted Z2 third centered moment for all q,n,2<=d<n,m>=1 and every unconditional H-prior. In fixed-q,d/n<1/2,m=o(n), the planted/null third moments agree to relative error q^(-Omega(n)), dominated by lifted transverse-pencil lines. Exhaustive scratch checks match for GF(2) n4/5 and GF(3) n4, including affine rank-two and varying-P cases. This is **not** TV closeness, a Gaussian law, feasible public counting, any-witness inversion, new Field-15 novelty or a crypto claim. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD. N1-60 remains unallocated.

## 2026-10-19 - Exact null third central moment for decomposable 2-plane counts

[Higher-moment negative control](../docs/foundation/F0-dual-bivector-null-third-central-moment.md) proves the exact **third centered null moment** of X=Z2: T*p*(1-p)*(1-2p) + [n choose1]_q*[n-1 choose2]_q*(q+1)*q*(q-1)*p^2*(1-p), T=[n choose2]_q,p=q^(-m). Dependent triples correspond precisely to projective Plücker lines indexed by flags of dimensions (1,3), exposing genuine third-order dependencies despite pairwise independence. At fixed q,m=o(n), standardized null skew is Theta_q(q^(-m/2)); no Gaussian/TV inference. Independent tiny GF(2),n=4 exhaustive scratch arithmetic agrees for m=1 (315/4) and m=2 (525/16), not committed as an attack benchmark. Planted third moment, feasible public counting, full verifier inversion and security remain unresolved. NO NOMINATION; H-A/H-B/H-C HOLD; N1-60 free.

## 2026-10-19 - Exact null-orthogonal three-plane contrast and single-slice pointwise identity

[New scoped F0 Z3-minus-Z2 analysis](../docs/foundation/F0-isotropic-three-plane-orthogonal-contrast.md) gives the exact null projection coefficient B=[n-2 choose1]_q*q^(-2m) for D3=Z3-B Z2. With p=q^(-m) and F=(1-p)(1-q p)(1+(q+1)p), proves Var_0(D3)=[n choose3]_q*p^3*F and E_pl(D3)-E_0(D3)=[d choose3]_q*F under the entire conditional-uniform planted source and any unconditional H-prior. For m=1, F=0 and the **pointwise** identity [n-2 choose1]_q*Z2=(q+1)*[n choose3]_q+q^2*Z3 holds for every alternating form; previously documented one-slice public inversion retains priority. For fixed q, d/n<1/2 and 2<=m=o(n), the standardized residual mean signal is q^(-Omega(n)), not TV closeness, hardness, or a public counter. Tiny GF(2),n=4,d=3,m=2 conditional/unconditional enumerations independently match exact fractions. No numbered stage or construction. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.

## 2026-10-19 - Mixed-dimensional isotropic counts: exact covariance and rank-one null fluctuations

[All-(r,k) finite-field covariance result](../docs/foundation/F0-isotropic-subspace-mixed-covariance-rank-one.md) extends the just-merged same-r source moments: under unrestricted iid alternating slices, Cov(Z_r,Z_k) is an exact Gaussian-binomial sum by s=dim(J cap K). Under fixed planted H, an exact nonnegative mixed covariance kernel uses quotient exterior-square ranks. For fixed field q and fixed r,k>=2 with m=o(n), the null covariance matrix is asymptotically rank one: Cov(Z_r,Z_k)~B_r B_k Var(Z_2), B_j=[n-2 choose j-2]_q*q^(-m*(binom(j,2)-1)), and Corr(Z_r,Z_k)->1. This describes **leading null fluctuations only**; planted covariance, residual linear contrasts, growing r, computability, TV, inversion and hardness remain open. Tiny GF(2),n=4,m=1 cross-covariance 105/16 checked independently. No source changes, N1 number, A-ID, implementation or crypto claim. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.

## 2026-10-19 - All-r isotropic-subspace null variance and planted covariance kernel

[Source-first second-moment boundary](../docs/foundation/F0-isotropic-subspace-second-moment-boundaries.md) gives an exact Gaussian-binomial **null variance for every r** and an exact **fixed-H planted covariance kernel** via ranks of the images of Lambda^2 J and Lambda^2 K in (Lambda^2 V)/(Lambda^2 H). At fixed q,r, d/n -> alpha in (0,1/2), m=o(n), the planted-to-null mean shift divided by **null** standard deviation is Theta(q^(2d-n+m/2)) = q^(-Omega(n)), uniformly in the choice of unconditional planted H-prior. The s=2 intersection term dominates null variance for every fixed r>=2; no claim for growing r, TV closeness, efficient counting or inversion. Arithmetic cross-checked for q=2,n=4,m=1,r=2/3. No new A-ID or N1-60 allocation. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.

## 2026-10-19 - All-r planted-TI isotropic-subspace mean hierarchy and sparse low-r bound

[Exact source-first F0 all-r first-moment theorem](../docs/foundation/F0-isotropic-subspace-first-moment-hierarchy.md): for each r<=d and unrestricted null, E[Z_r]=[n choose r]_q*q^(-m*binom(r,2)); the conditionally uniform planted source has an exact sum by t=dim(J intersect H), counting [d choose t]_q*[c choose r-t]_q*q^((d-t)(r-t)) terms at survival probability q^(-m*(binom(r,2)-binom(t,2))). For fixed q, d≈n/C,C>=3,m≈n/logn, the planted/null **relative expectations** agree to 1+q^(-Omega(n)) for r<= (2-epsilon)c/m. This is only an expectation-level negative control, not TV closeness, an efficient counter/inverter or a cryptographic security claim. Previously proved full-r size-bias/null d-witness rarity is credited to [#208 comment 6215551334](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6215551334), and the rank-two variance remains PR #231. No data/code/stage allocation. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.

## 2026-10-19 - Exact planted/null projective bivector-kernel expectation and variance

[New F0 dual-bivector source-moment theorem](../docs/foundation/F0-dual-bivector-kernel-exact-source-moments.md) exactly counts expected projective decomposable rank-two bivectors surviving all public alternating forms and derives **both variances**: null `T p(1−p)`; planted `p(1−p)(q^(2d−2)*[d choose1]_q*[c choose1]_q+q^(2d)*[c choose2]_q)`, with `p=q^(−m)`, `T=[n choose2]_q`, `c=n−d`. The planted mean is `S+(T−S)p`, `S=[d choose2]_q`. Its covariance proof classifies projective quotient fibres by 2-planes meeting H in dimensions 0, 1, 2. In sparse external `d≈n/C,C≥3,m≈n/logn` the planted mean shift is exponentially smaller than null sigma, **without claiming TV closeness, detector impossibility or polynomial counting**. The previous arbitrary-c dense full-span inverter was **already proved in issue #208 comment 6215130941** and is credited, not renominated. No novel Field-15 foundation, samples, code, stage allocation or PQ security claim. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.

## 2026-10-19 - All-rank ternary matroid public inversion by induced-cycle sign constraints

[F0 GF(3) proof](../docs/foundation/F0-matroid-realization-boundaries.md#9-all-honest-ternary-matroids-polynomial-public-reconstruction-from-independence-queries) gives pointwise deterministic polynomial **independence-oracle any-witness inversion for all honest ternary matroids of arbitrary rank**. Basis replacements expose the bipartite support of `[I|D]`. Each chordless even cycle determines a binary sign-product equation from one exact public determinant independence test. Decomposition of a fundamental cycle basis into chordless cycles takes polynomial work; binary linear algebra recovers edge signs up to row/column gauges, hence reproduces **all original labelled ranks**. Established Seymour 1979 and Truemper 1982 priority, no new Field-15 novelty, crypto claims, numbered N1/F0-K stage, sample cases or implementation. The oracle result does not assert efficient exhaustive verification of an arbitrary succinct rank oracle or solve GF(q≥4). GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.

## 2026-10-19 - Binary matroids: universal public basis-exchange representation at any rank

[Strengthened matroid no-go (§8)](../docs/foundation/F0-matroid-realization-boundaries.md#8-all-honest-binary-matroids-exact-public-standard-representation-by-basis-exchanges) supersedes the fixed-projective-enumeration approach **when q=2**: for any honest binary rank-table or exact rank-oracle instance, select a public independent basis B and query each replacement set `(B−b_j)+x`; its rank determines the corresponding GF(2) column bit **exactly**. This reconstructs a complete standard binary representation in **O(nr) exact public rank or independence queries**, even for growing rank, with pointwise correctness for the full original rank relation. Classical uniqueness/fundamental-circuit representation, not new mathematical novelty. A succinct oracle does not automatically imply polynomial *full verifier* complexity; fields q>2 are not handled by this rank-bit argument. This proof strengthens the simultaneously documented fixed-q/r projective enumeration; no crypto or Field-15 claim, N1-60 allocation or new measured cases. GLOBAL NO NOMINATION, H-A/H-B/H-C HOLD.

## 2026-10-19 - Pointwise complete matroid rank-table inversion at fixed finite field and rank

[Updated F0 matroid realization boundaries](../docs/foundation/F0-matroid-realization-boundaries.md#7-all-fixed-field-fixed-rank-labelled-matroids-finite-projective-point-enumeration) prove a **source-independent full-original-verifier any-witness inverter** for *every* honest complete labelled rank table at **fixed q and fixed r**, by compressing zero/parallel column classes and exhaustively assigning their at most `M=(q^r−1)/(q−1)` projective directions. The runtime is `M!·poly(L,n,r,log q)` against the **explicit public table**, with pointwise success one. In particular GF(2), rank three, has at most seven directions and `7!=5040` assignments even for arbitrarily many labelled parallels. This **does not** give polynomial inversion over growing fields, growing rank or succinct rank oracles; no new source samples, code, N1/F0-K stage, independent Field-15 novelty or crypto claim. GLOBAL NO NOMINATION, H-A/H-B/H-C HOLD.

## 2026-10-19 - Sparse planted-TI individual rank-vector TV and high-corank MinRank null controls

[Source-first F0 rank-profile note](../docs/foundation/F0-sparse-planted-ti-rank-profile-minrank-screen.md) extends [#208's coefficient-rank/common-radical exclusions](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6215891446) to the **complete vector of individual public alternating-slice ranks**, via exact conditioned-cross-block rank mixtures and classic Fulman–Goldstein random-alternating-rank counts. For fixed q, `m=ceil(n/log n)` and `d=ceil(n/C), C>=3`, its joint planted-vs-null rank-profile TV is negligible; additionally on **both laws**, with overwhelming probability **no** projective linear combination has corank `>=ceil(2 sqrt(m))+2`. This is a **narrow anti-overclaim** result: smaller-threshold adaptive MinRank and any-witness inversion remain unresolved, and there are zero experiments/code/new N1/F0-K cases or security claims. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.

## 2026-10-16 - Binary-field rank-two Plücker kernel: exact any-witness decision and fibre count

[Unnumbered F0 Plücker kernel-plane proof](../docs/foundation/F0-plucker-two-dimensional-kernel-section.md) gives deterministic polynomial pointwise **decision and full-original-verifier search** over `GF(2^e)` at **fixed c=n−d**, whenever the public exterior wedge map has nullity ≤2. In the nullity-two case, restrict classical quadratic Grassmann–Plücker equations to the public projective kernel line. Either all restrictions vanish (all `q+1` projective points accepted), or one nonzero quadratic confines every witness to at most **two** rational roots. Solve degree-two/Artin–Schreier equations by deterministic binary linear algebra, verify every original form, and count exact accepted d-spaces (0,1,2 or q+1), times `|GL_d(q)|` bases. **No source probability or high-nullity inversion is inferred.** Classical projective geometry, no Field-15 novelty, code, new numbered stages or PQ claims; GLOBAL NO NOMINATION, H-A/H-B/H-C HOLD.

## 2026-10-16 - Adaptive multislice support intersection: exact Möbius probability for every d>c

[Unnumbered F0 adaptive support note](../docs/foundation/F0-adaptive-multislice-support-intersection.md) generalizes the two-slice high-d no-go: select **public rank-2c slices** of any honest conditional-uniform alternating tuple, intersect their covector images, and output a full-original-verifier witness if the intersection has dimension c. Rank-deficient slices are **not** removed from the public verifier or honest distribution. An exact source success probability follows from Möbius inversion on the finite-field subspace lattice, uniformly for any original H-distribution. For **every d>c** and q≥2, success ≥`max(0,1−((q^d−1)/(q−1))·(3/4)^m)`, hence near one for `m=O(d log q + log(1/δ))`. Fully specified bounded binary-field generator retains exact conditional uniformity without sample filtering. The known conjectural low-d (`d<c`) planted-TI regime remains outside scope. No empirical runs, numbered stage, candidate or cryptographic novelty/security claim. H-A/H-B/H-C HOLD; GLOBAL NO NOMINATION.

## 2026-10-16 - Two-slice public image-support intersection breaks high-d planted TI

[Unnumbered F0 two-slice support-intersection proof](../docs/foundation/F0-two-slice-public-row-support-intersection.md) shows a **deterministic pointwise public full-original-verifier section** whenever two alternating slices have rank `2c` each and their public covector images intersect in exactly dimension c, for any honest `d=n−c` planted YES input. Their intersection is the planted annihilator, which reconstructs the accepted d-space by Gaussian elimination. For **two independent uniform conditioned planted slices** with `d≥2c`, this certificate holds with **exact unconditioned probability** `prod(j=0..2c−1)(1−q^(j−d))`, ≥1/4 at `d=2c`, >1−q^(−t)/(q−1) at `d=2c+t`, even if c grows with n. Binary-field strict bounded-time honest generation (including fallback) retains the same exact probability without filtering. This strengthens the prior fixed-c full-span gate in a **different high-dimensional regime**, not the paper's conjectural low-d sparse-m regime. No experimental cases, code, new N1/F0-K stage, independent Field-15 novelty or PQ/OWF claim. GLOBAL NO NOMINATION, H-A/H-B/H-C HOLD.

## 2026-10-16 - Fixed-codimension full-span wedge rigidity and exact honest-law inversion probability

[Unnumbered exterior-kernel F0 note](../docs/foundation/F0-fixed-codimension-wedge-kernel-section.md) proves a pointwise polynomial **full-original-verifier** section whenever fixed-`c` public wedge nullity is one; for any planted `d=n−c≥2` subspace H, the common wedge-annihilator of the **entire** space of alternating forms vanishing on H is exactly its one-dimensional annihilator Plücker line. For m independently uniform conditional forms from that `D=binom(n,2)−binom(d,2)`-dimensional space, full-span and verified inversion succeed with exact unconditioned probability `∏(j=0..D−1)(1−q^(j−m))` for `m≥D`, ≥1/4 at m=D, >1−q^(−t)/(q−1) at m=D+t. A strictly worst-case polynomial binary-field generator includes low-rank-row fallback; its **actual** full-source success has the same exact probability, without postselection. General wedge kernels of dimension >1 and `c=Θ(n)` remain outside scope. No empirical draws, source cases, cryptographic claim or N1/F0-K number. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.

## 2026-10-16 - Arbitrarily many alternating slices: hyperplane inverse linearization and public distribution distinguisher

[Multislice hyperplane F0 note](../docs/foundation/F0-multislice-isotropic-hyperplane-linearization.md) proves **pointwise deterministic decision-and-search** for the full rank-`n−1` TI verifier over **every finite field and any number m of alternating slices**, via the public linear kernel of `α↦(α∧A_i)_i`. Every accepted hyperplane is one projective point of this kernel: the exact fibre count and ideal uniform planted/null likelihood ratio depend only on its dimension. A polynomial distinguisher has ideal planted detection 1 and unrestricted uniform null false-positive probability at most `((q^n−1)/(q−1))*q^(−m·binom(n−1,2))`; a strict worst-case bounded binary-field source with fallback has an explicit TV bound and still provides an accepted witness on **every** run. Classical exterior/Koszul/Plücker principles; does not solve codimension ≥2 and does not constitute new Field-15 evidence. No code, experiments or stage numbers; GLOBAL NO NOMINATION, H-A/H-B/H-C HOLD.

## 2026-10-16 - Public regular alternating pencils: common Lagrangian and honest constant-probability inverter

[Regular-pencil F0 note](../docs/foundation/F0-regular-alternating-pencil-public-section.md) proves a **deterministic original-verifier public section** for **all** alternating tuples whose matrix span is ≤2-dimensional and includes a nondegenerate original-field combination (even n, d≤n/2). A cyclic T-stable isotropic subspace and symplectic quotient recursion work in characteristic two without factoring. For two independent uniformly conditioned forms, a fixed planted S gives an exact per-slice nonsingularity product; the event at least one slice is nonsingular has probability ≥**455/2304** on the full honest law, with strict worst-case PPT exact generation on binary finite fields. No source filtering, code, numeric samples, new F0-K/N1 label, or Field-15 novelty. H-A/H-B/H-C HOLD, GLOBAL NO NOMINATION.

## 2026-10-16 - Single alternating slice: exact TI inverter and rank-only planted detector

[Unnumbered F0 note](../docs/foundation/F0-one-alternating-form-rank-screen.md) proves **pointwise polynomial any-witness inversion for every feasible d** against a single public alternating form over every finite field, including characteristic two and degenerate forms: maximal TI dimension is `n−rank(A)/2`. For the distinct **ideal uniform Grassmannian planted law**, the posterior solution count is an explicit polynomial-computable function of public matrix rank, and rank is a sufficient statistic for the exact optimal planted-vs-null detector; the source-bound caveat is explicit. Classical symplectic geometry, not original Field-15 evidence or general multi-slice inversion. No empirical cases/code or new N1/F0-K ID; GLOBAL NO NOMINATION, H-A/H-B/H-C HOLD.

## 2026-10-16 - Rank-three matroid public sections beyond intersection closure

The [F0 finite-field matroid note](../docs/foundation/F0-matroid-realization-boundaries.md#6-rank-three-extension-frame-free-near-pencil-and-core-anchored-lines) now proves two further **paper-only, source-independent, full-original-verifier** public sections: (i) every simple rank-three frame-free pattern is a near-pencil and invertible over every finite field; (ii) when `q>n²`, a publicly reconstructed core whose unresolved collinear triples are supported on core-spanned lines admits a deterministic greedy line/conic section, including unresolved points on singly prescribed lines. Scope excludes unsupported residual incidences and does not imply generic rank-three representation. See [F0 #208](https://github.com/StanleyLl0yd/morph-kem/issues/208). No code, runs, new N1/F0-K numbers, crypto nomination or positive Field 15. H-A/H-B/H-C HOLD and GLOBAL NO NOMINATION remain.

## 2026-10-16 - Git branch-history preservation and housekeeping

After PR #217/#218 and verified 109-branch cleanup, eight divergent/closed-unmerged historical heads remained. The [strict provenance manifest](../docs/archive/retired-branch-provenance-2026-10-16.md) lists their exact commit SHAs and creates durable archival Git tags **before** deleting branch refs. Replacements do not imply byte-identical source or proof. The one-time action is operational repository maintenance, **not** new research evidence, code experiments, a stage number or a cryptographic claim. Actual deletion/tag success must be verified against GitHub Actions logs; a merged PR alone is not proof of archival success.

## 2026-10-16 - F0 source-first matroid realization screen and README compaction

[Finite-field matroid note](../docs/foundation/F0-matroid-realization-boundaries.md) transfers [#208 analytic proof](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6216134094) into repository documentation: rank-two full-pattern public sections, a scoped frame-generated rank-three projective closure, and high-probability Vandermonde/MDS any-witness sections for fixed-rank large-field unconditional sources. All proofs are analytical, with explicit full-original-verifier checks; no Field-15 originality, new cases or code. The old verbose README historical section was preserved in [legacy snapshot](../docs/archive/README-legacy-2026-10-14.md) and README reduced to status/navigation. Owner workflow now requires **durable GitHub file updates after each pass**. GLOBAL NO NOMINATION, H-A/B/C HOLD; N1-60 unallocated.

## 2026-10-16 - F0-HAC residualization and F0-K9 acyclic join section

[Foundational note](../docs/foundation/F0-residual-core-and-acyclic-join.md) gives a **distribution-preserving exact any-witness equivalence** between public coupled H-A inversion and inversion of the residual second map when a public full first-fibre chart is available. This neither invents nor inverts that residual relation. It also records **F0-K9 ANALYTIC REJECT** for explicit polynomial-size join-tree / α-acyclic hypergraph constraints, by classical Yannakakis semijoin + witness reconstruction even at large primal width. [Original H-A project proof](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6210012660); [original F0-K9 proof](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6210050665). H-A/H-B/H-C remain **HOLD**, GLOBAL NO NOMINATION; zero empirical cases, no coding or new N1 stage.

## 2026-10-16 - MORPH-F0 K7/K8: perfect permutation CSPs and publicly affine marginal fibres

[F0-K7](../docs/foundation/F0-failure-mechanisms.md#11-f0-k7-fully-satisfiable-permutation-constraints-on-an-explicitly-enumerable-alphabet) is the known *perfectly satisfiable Unique Games* section: on an explicitly enumerable polynomial alphabet, try each spanning-tree root label, propagate permutations, and accept only after checking **all** original constraints. The exact fibre is the product of common holonomy fixed-point counts; unlike F0-K4, not every arbitrary root value is valid. Classical source: Trevisan, [*Approximation Algorithms for Unique Games* (2005)](https://eccc.weizmann.ac.il/report/2005/034/download). [F0-K8](../docs/foundation/F0-failure-mechanisms.md#12-f0-k8-public-affine-parametrization-of-one-entire-fibre-kills-nonlinear-two-view-inversion) shows that a public bijective parameterization of **the entire** first-view fibre plus a second view affine in those coordinates yields a Gaussian joint any-witness inverter and exact fibre count. [Formal project proofs](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6209881636). **Both scoped ANALYTIC REJECT, no experiments, no candidate, no new N1 stages or security claims.** H-A/H-B/H-C HOLD; GLOBAL NO NOMINATION.

## 2026-10-15 - MORPH-F0 K6: Frobenius and public triangular-normal-form collapse

[F0-K6](../docs/foundation/F0-failure-mechanisms.md#10-f0-k6-coupled-frobenius-polynomial-observations-with-a-public-shared-normal-form-remain-linear) formalizes a known algebraic trap for H-A/H-B: all public Frobenius-polynomial views over \(F_{q^k}\) become one base-\(\mathbb F_q\) linear system, even after an efficiently reversible public nonlinear coordinate change. An exact Gaussian section passes the original joint verifier and gives fibre cardinality \(q^{nk-r}\), conditional only on the stated full-domain/public-normal-form hypotheses. Established prior art: Berson (2014). [Scoped proof #208](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6190211208). **No experimental cases, nominated family, positive Field 15, N1-60 allocation or PQ/OWF claims.** H-A/H-B/H-C HOLD; GLOBAL NO NOMINATION.

## 2026-10-15 - MORPH-F0 K4a/K5: coupling neither guarantees hardness nor originality

Two precise follow-on analytical screens extend [F0 failure map](../docs/foundation/F0-failure-mechanisms.md). [F0-K4a](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6187744006) proves that two independently canonicalizable nonabelian group edge-transport views of the same hidden vertex assignment jointly invert by spanning forest on their union graph; even incompatible choices of marginal gauges cause no hard inverse problem. [F0-K5](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6187822455) proves a **different** universal re-encoding: for arbitrary polynomial h, f(x,r)=r and g(x,r)=r XOR h(x) each have trivial public sections, but their paired inverse problem is *exactly average-case equivalent* to h-inversion under a one-time-mask source. The reverse reduction checks the original pair verifier before projecting the witness, preserving attack-success probability. **F0-K5 does not invert an arbitrary h, does not show any concrete pair is hard, and cannot establish mathematical novelty.** H-A remains HOLD and demands a genuinely independent relation; no numeric cases, crypto claims or N1 stage changes.


## 2026-10-15 - MORPH-F0 foundation-first pivot: structural no-go gates and hypothesis triage

After canonical N1-59 ANALYTIC REJECT, opened [MORPH-F0 #208](https://github.com/StanleyLl0yd/morph-kem/issues/208) without consuming N1-60. The [failure map](../docs/foundation/F0-failure-mechanisms.md) links representative N1 and legacy negative mechanisms and initially gave three self-contained exact counter-gates: F0-K1 large planted-secret conditional entropy with trivial public accepted witness; F0-K2 all publicly linear coupled views collapse to one polynomial Gaussian solve; F0-K3 honest satisfiable finite-domain CSPs with **given public** bounded-treewidth decomposition admit public dynamic-programming witnesses. A fourth analytic [F0-K4](../docs/foundation/F0-failure-mechanisms.md#7-f0-k4-nonabelian-global-edge-relations-invert-even-at-maximal-treewidth) now formalizes exact nonabelian group-valued edge-transport inversion by spanning-tree gauge, even for complete graphs of treewidth n-1. This refutes any naive hope that high width, many cycles or noncommutativity alone prevents a public section. These are known/easily proved mechanisms, **not** new security results or new measured attacks.

[Three structural hypotheses](../docs/foundation/F0-hypothesis-ledger.md) remain HOLD: H-A coupled incompatible quotients; H-B local-to-global patches; H-C noncommuting histories. None has positive independently sourced Field-15 novelty or a complete 15-field candidate, so **no new samples, code, N1 stage, KEM/PKE/trapdoor, OWF/PQ claim or parameter series**. Keep global NO NOMINATION and strategy 80/20. HEPMR #195 BENCHMARK ONLY through AP103; N1-19 19/30 and N1-23 9/12 remain PARTIAL, N1-26 HOLD; historical N1-52 593,305 +40 unchanged; original archive issue #199 blocked.


## 2026-10-14 - N1-59 rational hyperbolic-geodesic cosine distances: ANALYTIC REJECT

[The complete 15-field source proof](../docs/107-morph-n1-59-hyperbolic-geodesic-no-go.md) fixes a 1D H^1 hyperbolic geodesic, rational cosh-distances and an anchored, integer-supported parameter t_0=1, t_i>1. A public anchor row suffices: `t_i=C_0i+sqrt(C_0i^2-1)`; every honest radicand is an exact rational square, so the original verifier accepts the recovered planted tuple in polynomial bit time. This does **not** prove arbitrary higher-dimensional hyperbolic inverse embeddings easy; the category is already established h-MDS/Lorentz Gramian prior art (Sala et al. 2018, Tabaghi/Dokmanic 2020). [Original N1-59 proof comment](https://github.com/StanleyLl0yd/morph-kem/issues/196#issuecomment-6176155839), [prior-art preliminary caution](https://github.com/StanleyLl0yd/morph-kem/issues/196#issuecomment-6176123156).

**GLOBAL NO NOMINATION, zero new empirical cases.** Keep frozen N1-52 counts 593,305 +40 (unrecovered original ZIPs [#199](https://github.com/StanleyLl0yd/morph-kem/issues/199)), N1-19 and N1-23 PARTIAL, N1-26 HOLD/BENCHMARK, HEPMR #195 BENCHMARK ONLY. Next: N1-60 distinct positive Field-15 screen before any code or sampling.


## 2026-10-14 - N1-56, N1-57, N1-58: three independent analytical REJECT decisions

- **[N1-56](../docs/104-morph-n1-56-finite-bispectrum-no-go.md)**: full cyclic bispectrum over F_(2^k), n=2^k-1; a public bispectrum power slice yields a recurrence reconstructing all nonzero Fourier coefficients up to cyclic shift. Exact fibre n shifts, polynomial any-witness inverse. Classical bispectrum completeness/translation invariant prior art fails Field 15. [Original issue proof](https://github.com/StanleyLl0yd/morph-kem/issues/196#issuecomment-6175990737).
- **[N1-57](../docs/105-morph-n1-57-radon-walsh-no-go.md)**: complete labeled binary-affine hyperplane sums with values in F_3; taking bin differences yields all Walsh coefficients and exact inverse Walsh transform. Classical finite Radon/tomography prior art fails Field 15. [Original issue proof](https://github.com/StanleyLl0yd/morph-kem/issues/196#issuecomment-6176006953).
- **[N1-58](../docs/106-morph-n1-58-principal-minors-no-go.md)**: signed symmetric F_5 matrix, all one/two minors plus anchored size-three minors. Triangle determinants expose signed switching invariants; normalize public star to +1 and reconstruct every other edge in O(n^2) field work. Classical symmetric principal-minor assignment/signed graph switching prior art fails Field 15. [Original issue proof](https://github.com/StanleyLl0yd/morph-kem/issues/196#issuecomment-6176025206).

**Research only, NO NOMINATION, 0 new source/protocol cases**. N1-52 reported 593,305 complete heterogeneous toy cases +40 controls is unchanged; the original N1-46/47/51 ZIPs are NOT in repository ([#199](https://github.com/StanleyLl0yd/morph-kem/issues/199) remains blocked). N1-19 PARTIAL 19/30, N1-23 PARTIAL 9/12, N1-26 HOLD/BENCHMARK and HEPMR #195 BENCHMARK ONLY through AP103 remain. No KEM/PKE/trapdoor, OWF/PQ claim or HEPMR broad scan. **This N1-59 pointer is superseded by the later N1-59 analytical result above; next gate N1-60.**


## 2026-10-14 - N1-54 and N1-55: two independent analytical REJECT decisions

- [N1-54](../docs/102-morph-n1-54-hankel-realization-no-go.md) specifies all 15 MORPH-R0 fields for exact 2n public finite-field moments `h_t=cA^t b`. Planted diagonal eigenvalues with nonzero weights make the Hankel matrix nonsingular. A public linear recurrence and companion realization recover a verifier-accepted triple in polynomial field operations; hidden GL_n basis entropy is a gauge orbit. Classical Ho-Kalman/system-identification prior art defeats Field 15. [Issue proof](https://github.com/StanleyLl0yd/morph-kem/issues/196#issuecomment-6171154797).
- [N1-55](../docs/103-morph-n1-55-adic-trie-no-go.md) independently specifies a full labeled `v_2(x_i-x_j)` matrix for random distinct residues mod `2^m`. Public equivalence-class partitions at all bit depths determine a binary trie; canonical 0/1 child labels produce a verifier-valid alternative number vector in polynomial time. Classical ultrametric/dendrogram and p-adic tree representation defeats Field 15. [Issue proof](https://github.com/StanleyLl0yd/morph-kem/issues/196#issuecomment-6171176966).

**No new empirical cases, scripts, corpus or rerun of N1-52:** 593,305 exact fully enumerated source/protocol cases and 40 controls stay historical, with [artifact provenance blocker #199](https://github.com/StanleyLl0yd/morph-kem/issues/199) still open. N1-19 PARTIAL 19/30, N1-23 PARTIAL 9/12, N1-26 HOLD/BENCHMARK unchanged. HEPMR #195 BENCHMARK ONLY through AP103. **GLOBAL NO NOMINATION; this N1-56 pointer is historical, superseded by N1-59 above.** No PKE/KEM/trapdoor or OWF/PQ claim.


## 2026-10-14 - MORPH-N1 #196 checkpoint N1-52 synchronized into repository

**GLOBAL NO NOMINATION.** Research-only split ~80% new relation discovery, ~20% bounded HEPMR closure, not implementation. Active N1 issue #196 reached checkpoint [6168184843](https://github.com/StanleyLl0yd/morph-kem/issues/196#issuecomment-6168184843). HEPMR #195 stays BENCHMARK ONLY through AP103; do not restart AP104+.

The N1-46 Euler/de Bruijn spectrum attack accepted 81,672/81,672 cases; N1-47 public Möbius-frame inversion accepted 229,200/229,200; N1-51 fixed-k coupled-spectrum frontier DP accepted 4,064/4,064 while single-view Euler accepted both constraints only 2,179/4,064. N1-48/49 were analytic redundancy results without additional enumerations. All three exact families REJECT, not cryptographic confirmations.

Cumulative reported numbers since N1-34: **593,305 full exact toy source/protocol enumerations + 40 replay controls**. N1-19 PARTIAL 19/30, N1-23 PARTIAL 9/12, N1-26 HOLD/BENCHMARK unchanged. The original scripts/ZIP bundles remain conversation-local and are **not** imported or rerun in this documentation synchronization. See [docs/100-morph-n1-status-2026-10-14.md](../docs/100-morph-n1-status-2026-10-14.md) for sources, limitations and N1-53 gate.

**Decision:** no candidate and no trapdoor/PKE/KEM, OWF or PQ claim. Documentation catch-up does not change the research result.


The prior detailed log through 2026-09-11 is preserved verbatim in `notes/research-log-through-2026-09-11.md`.

## 2026-10-14 - N1-53 full effective-resistance inverse: analytic REJECT

An independent, complete 15-field screen of exact labeled weighted-graph **effective resistance** (not shortest-path distance) yielded the public reconstruction identity `L^+=-JRJ/2`, then `L=(L^+ + 11^T/n)^{-1}-11^T/n`. Every edge conductance is publicly recovered from `-L_ij` in polynomial exact bit complexity. Field 15 fails classical electrical-network inverse prior art. **No N1-53 source enumeration, code or security claim.** [Proof and all fields](../docs/101-morph-n1-53-resistance-no-go.md); [issue result](https://github.com/StanleyLl0yd/morph-kem/issues/196#issuecomment-6169028746). **Superseded next-gate reference: see N1-54/55 above; GLOBAL NO NOMINATION.**
 Repository commits and the numbered research documents remain the authoritative detailed evidence for individual experiments.

## 2026-09-14 — HGA4 finite-representation line frozen

The HGA4 Hurwitz/free-group endpoint line was pushed through exact-distance generation, held-out finite quotients and finally an adaptive endpoint-independent library of small finite representations. HGA4f recovered all measured exact endpoints while retaining fewer exact states than ordinary MITM on every declared endpoint. Training-conditioned generation had already failed to generalize to held-out representations.

**Decision:** freeze the HGA4 Hurwitz/free-group lineage. Do not condition generation against a growing representation library.

## 2026-09-14 — HGA re-entry survey ends with no nomination

A separate action-family literature gate was applied after HGA4. A finite Markoff-surface action was implemented only as a negative control and was recovered publicly on 72/72 declared instances. The subsequent binding-action survey found no candidate that cleared the HGA1–HGA4f failure classes strongly enough to justify another implementation.

**Decision:** HGA-R2 ends with **NO NOMINATION**. Trapdoor/KEM gate remains closed.

## 2026-09-14 — NAT residual-representation line frozen

NAT7/NAT8 showed that public tree normalization removes vertex-gauge secrecy and exposes the complete residual connection / free-generator representation. NAT9 then tested lossy `A5` observables; a public finite-domain CSP still recovered verifier-valid equivalent representations. NAT10 replaced exact/lossy publication with noisy `SL(2)` trace sketches, but public relator CSP again recovered large accepted representation families.

**Decision:** freeze the current NAT residual-representation family. Hiding the planted representation is irrelevant when public verification accepts many recoverable alternatives.

## 2026-09-14 — TDC current ensemble frozen after predeclared Lee–Brickell gate

The TDC2g common-overlay ensemble removed the earlier bounded low-weight word signal and survived matched decoder-work, reliability and bounded Prange/ISD checks. The predeclared TDC3c Lee–Brickell checkpoint then produced the declared topology-easier failure at the fixed comparison point. Aggregate evidence remained mixed, but the checkpoint rule had been fixed before measurement.

**Decision:** freeze the exact current TDC2g-derived ensemble. No parameter rescue by changing size, weights, overlay count, seeds or attack budget.

## 2026-09-14 — MORPH-R0 cross-line reset

The negative corpus across HGES, HGA, NAT and TDC was consolidated into `docs/97-morph-r0-cross-line-postmortem.md`.

Recurring failure classes were made explicit: verifier-equivalent witnesses, public canonicalization, low-dimensional/finite-quotient leakage, local topological relations, lift/base recovery, noise-to-polynomial reductions, generator-vs-action failure, matched-control discipline and no parameter rescue.

The original geometry inspirations—Möbius/nonorientable surfaces, Klein bottle, hyperbolic/Lobachevsky geometry and Escher/impossible-figure encodings—were re-screened against the measured attacks.

**Decision:** before any new implementation branch, require a complete mathematical re-entry specification including public relation, verifier/equivalence, known quotients, canonicalization attack, matched control, validation distribution, quantum screen and a concrete reason the proposal is not a renamed mature assumption. Trapdoor/KEM gate remains closed.

## 2026-09-14 — BPT-W0 harness bug found and corrected

The first BPT experiment was deliberately weak: stacked `S^3` endpoints generated with `1-4` moves, attacked by public `4-1` simplification.

The first exact-head CI failed two new BPT tests while 442/444 tests passed. The failure was in the attack harness, not evidence for the candidate. Greedy simplification can legally collapse an original root vertex, so source and target can simplify to differently labelled but combinatorially isomorphic boundary-of-4-simplex roots. The implementation incorrectly required literal root equality although the public verifier uses isomorphism equality.

The attack was corrected to recover a deterministic exact public root isomorphism, extend it to removed target vertices with fresh labels, transport the inverse target simplification path and splice the two public paths.

**Lesson:** canonicalization/equivalence semantics must be applied to the attack itself; generation labels are not part of the public relation.

## 2026-09-14 — BPT-W0 rejected by BPT-A000 as intended

After the label-invariant fix, the dedicated BPT workflow passes on Python 3.11/3.12/3.13.

Fixed Python 3.12 depth-three baseline:

```text
source/target vertices:                 8/8
source/target tetrahedra:               14/14
move bound / recovered length:          6/6
source/target simplification steps:     3/3
combined vertex scans:                  52
combined legal 4-1 moves seen:          13
source/target simplification paths:     8/12
accepted-path multiplicity lower bound: 96
public recovered path accepted:         yes
recovered path equals planted path:     no
```

The declared `d=1/2/3 × 8 seeds` sweep recovers accepted paths on **24/24** instances. Multiplicity lower bounds are 4, 16 and 64–96 by depth. Every recovered sweep path differs from the planted path after public success.

**Decision:** BPT-W0 is rejected exactly as required for a weak control. The BPT harness calibration passes through candidate failure. See `docs/98-bpt0-stacked-s3-weak-control.md` and BPT-A000 in `docs/05-cryptanalysis.md`.

## 2026-09-14 — prior Pachner corpus rediscovered as mandatory BPT inheritance

Repository-wide reconciliation found that ordinary `2-3 / 3-2` bounded Pachner transport had already been investigated in T0/T1.

T0/A-022: fixed `t0-8` plants an eight-move non-self-repeating path but has true quotient distance four; bidirectional recovery expands only 13 states.

T1/A-023: exact-distance shell generation repairs the planted-length defect, yet fixed `D=3` still falls to bidirectional recovery after only five expansions. The project explicitly declined to add a larger shell merely to inflate work.

**Decision:** T0/A-022 and T1/A-023 are inherited BPT negative controls. A future BPT proposal cannot re-enter as “the same `2-3 / 3-2` search at larger depth”.

## 2026-09-14 — BPT-R1 theorem/representation reconciliation

Issue #192 and `docs/99-bpt-r1-pachner-reconciliation.md` apply MORPH-R0 to the 2026 Tillmann–Tsvietkova NP-hardness result before more code is written.

Key findings:

- the theorem uses topological triangulations defined by tetrahedra with affine face pairings; quotient cells may have boundary self-identifications;
- MORPH's current `SimplicialComplex` is an abstract simplicial complex of unique vertex subsets and therefore does not faithfully represent that general category;
- the theorem's sparse degree-two collapse is narrower than a generic topology-preserving edge collapse;
- the hard family is obtained by a Karp reduction from modified planar Hamiltonian path, with graph-edge deletion represented by sparse collapses;
- Regina already exposes public isomorphism signatures, Pachner navigation, exhaustive simplification and topology-preserving edge-collapse machinery that must be treated as attacker capability;
- no BPT-specific quantum algorithm was identified in the screening pass, but generic Grover/quantum-walk speedups remain relevant and absence of a special algorithm is not post-quantum evidence.

**Decision: NO NOMINATION.**

Do not build a generalized face-pairing engine, theorem-reduction generator, BPT-R2 implementation, trapdoor, PKE or KEM from the current state. Re-open BPT only when a concrete generated relation is materially distinct from both T0/T1 and the Hamiltonian-path reduction family and clears the full MORPH-R0 specification on paper first.

No security claim.
