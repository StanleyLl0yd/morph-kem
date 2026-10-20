# MORPH-F0: complete overlap-class residual gate law and exact seed posterior

**2026-10-20. Full honest-source finite counting theorem; GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** This unifies the [fixed-true-seed quotient law](F0-planted-ti-seeded-residual-support-attack.md), the [unrestricted-null rank gate](F0-planted-ti-null-residual-rank-gate.md), and the [precommitted disjoint-false-seed law](F0-planted-ti-disjoint-false-seed-residual-law.md) for **every possible overlap dimension** j=dim(T∩H). It gives the exact first moment of **all public rank-gate passing t-planes inside planted instances**, plus the exact posterior overlap distribution for **one independently uniform seed when only its gate result is observed**. It is not a polynomial extractor, adaptive-seed posterior, new security assumption, sampled attack, or improvement over the generic external planted-TI attack class. The underlying planted-TI problem is due to [Liu–Qiao–Tang–Zhang (2026)](https://arxiv.org/abs/2609.31256).

## 1. Original unconditional source and public event

Let q>=2 be a prime power; let V=F_q^n, 2<=d<n, c=n-d, and m>=1. The original planted source draws H from **any prior independently of the forms**, then publishes m independent uniform alternating forms A_i annihilating H×H. There is no rank postselection. The unchanged original any-witness verifier accepts an arbitrary d-plane L iff all the forms vanish on L×L. The unrestricted null source consists of m independent unconstrained uniform alternating forms.

Fix a public seed dimension \(1\le t<d\) and the full-row **residual rank-gate** range

\[
0<mt<c,\qquad \ell=c-mt,\qquad u=d-t,\qquad
0<\ell<u,\quad D=u+\ell=n-t-mt.
\]

For any public t-plane T, its publicly computed gate event \(\mathcal G(T,A)\) requires:

1. T is simultaneously isotropic;
2. the public T-to-V/T contraction matrix has **full mt row rank**;
3. every induced alternating form on the public quotient \(S_A(T)/T\) has rank at most \(2\ell\).

This is **not** the original any-witness verifier; it can pass false seeds. It can be calculated in polynomial time given a seed, while enumerating all public t-planes takes up to \(\operatorname{poly}(n,m,\log q){n\brack t}_q\) operations. Define \(G_t(A)=\sum_{T\in\operatorname{Gr}(t,V)}\mathbf1_{\mathcal G(T,A)}\).

## 2. Exact fixed-seed planted block law for every overlap j

Fix H and a t-plane T **before** drawing the forms, and put

\[
j=\dim(T\cap H),\quad
J=T\cap H,\quad H=J\oplus H_0,\quad T=J\oplus T_0,
\]

so \(\dim H_0=d-j=:h_0\), \(\dim T_0=t-j\), and one may choose a complement C_0 giving

\[
V=J\oplus H_0\oplus T_0\oplus C_0,\qquad
\dim C_0=c-t+j=:v.
\]

All coordinates in this decomposition are **proof-only**: no actual public algorithm knows H or J. The public T-isotropy event forces exactly \(m({t\choose2}-{j\choose2})\) independent uniform coefficients to vanish, because the j-by-j H-contained alternating block was already zero. Hence

\[
\boxed{p_{\rm iso}(j)
=q^{-m({t\choose2}-{j\choose2})}.}
\]

Conditional on this event, stack the m slices' public T-contraction rows against \(H_0\oplus C_0\). With \(a=mj\) and \(b=m(t-j)\), the resulting mt-by-(n-t) matrix has the **structured** law

\[
\boxed{
M=\begin{pmatrix}
0_{a\times h_0} & X_{a\times v}\\
Y_{b\times h_0} & Z_{b\times v}
\end{pmatrix},
}
\]

where every displayed free coefficient of X,Y,Z is independent uniform, also across slices. The blocks remaining on \(H_0\oplus C_0\) are **independent** of X,Y,Z and are independently uniform alternating forms vanishing on \(H_0\times H_0\).

**Proof.** Expand the original alternating coordinates in \(J,H_0,T_0,C_0\). Vanishing on H×H forces the J×J, J×H_0 and H_0×H_0 blocks to zero. Conditional T-isotropy further forces J×T_0 and T_0×T_0 to zero. All distinct remaining free alternating coefficients have independent uniform laws; they split precisely into the indicated T-to-(H_0+C_0) blocks and the untouched alternating blocks on H_0+C_0. This remains true in characteristic two with diagonal zero. QED.

For any resulting M let K=ker M inside \(H_0\oplus C_0\). On the isotropy event,

\[
S_A(T)=T\oplus K,\qquad S_A(T)/T\cong K,\qquad
F=K\cap H_0=\ker Y\subset H_0.
\]

In particular

\[
\boxed{\dim F=h_0-\operatorname{rank}Y
=d-j-\operatorname{rank}Y.}
\]

Exactly as in the prior disjoint-seed proof, restriction of an independent uniform alternating block annihilating H_0×H_0 onto K is **surjective onto the alternating forms annihilating F×F**. Thus conditional on the entire M, the residual m forms are independent uniform **planted-F** forms on K. This is an exact finite source statement for every overlap j, not a law assigned to a tensor-adaptive T.

## 3. Exact joint full-rank and residual gate probability

Let \(\pi_{p,s}(r)\) be the exact rank-r mass of a uniform p-by-s field matrix,

\[
\pi_{p,s}(r)=q^{-ps}{p\brack r}_q{s\brack r}_q
|\mathrm{GL}_r(q)|.
\]

For nonnegative integers v,z define \(F_v(z)=\prod_{i=0}^{z-1}(1-q^{i-v})\) when \(0\le z\le v\), and zero otherwise. In particular F_v(0)=1. Let \(\Phi_{D,k,\ell,q}\) be the **exact** rank<=2ell probability of a D-dimensional alternating form conditioned to vanish on a fixed k-plane, as derived by the independent cross-rank and alternating-corank mixture in the [preceding disjoint-seed theorem](F0-planted-ti-disjoint-false-seed-residual-law.md#2-exact-false-seed-rank-gate-by-a-finite-matrix-rank-mixture). No hidden k-plane is given to the public algorithm.

**Theorem 1 (exact unconditional planted fixed-overlap public gate).** Under the original unfiltered planted distribution, conditional on **any fixed H,T** with overlap dimension j, the public rank-gate event has exact probability

\[
\boxed{\begin{aligned}
P_j&=\Pr_{\rm planted}[\mathcal G(T,A)\mid H,T],\\
&=q^{-m({t\choose2}-{j\choose2})}
 F_v(a)\sum_{r=0}^{\min(b,h_0)}
 \pi_{b,h_0}(r)\,
 F_{v-a}(b-r)\,
 \Phi_{D,h_0-r,\ell,q}^{\,m},\\
&a=mj,\ b=m(t-j),\ h_0=d-j,\ v=c-t+j.
\end{aligned}}
\]

The formula is defined with F_v(a)=0 when a>v and requires **no sampling, subset oracle, full hidden-H recovery, rank postselection, or unverified witness**.

**Proof.** First force T isotropic at the displayed probability. To make M have all \(a+b=mt\) rows independent, the top X block must have full row rank a, an event of probability F_v(a). Conditional on this, quotient the v-dimensional C_0 coordinate space by the a independent X rows. The bottom b rows then consist of the untouched uniform Y block of width h_0 and an independent uniform projected Z block of width v-a. The exact probability that Y has rank r is \(\pi_{b,h_0}(r)\), and conditional on this, the fresh v-a random columns must span the remaining b-r row dimensions, with probability \(F_{v-a}(b-r)\). The events over r are disjoint. Under this M, K has dimension D and F=K∩H_0 has dimension h_0-r. The prior restriction-surjectivity theorem gives independent uniform residual planted-F forms, so all m pass rank<=2ell with probability \(\Phi_{D,h_0-r,\ell,q}^m\). Sum over r, multiply by p_iso(j), and do not assume independence across different public T. QED.

An independent simplification (without the residual gate) is the exact conditional public **full-row probability**

\[
\boxed{\Pr[\operatorname{rank}M=mt\mid I_T,H,T]
=F_v(a)\,F_{h_0+v-a}(b).}
\]

This follows because after X has full row rank, all b projected bottom rows are uniform in dimension \(h_0+v-a\). The law is **not** a general uniform mt-by-(n-t) matrix when j>0.

**Endpoint checks.**

- \(j=0\) (precommitted disjoint false seed): a=0, b=mt, h_0=d, v=c-t, and the displayed formula reduces exactly to the [rank-mixture of the preceding note](F0-planted-ti-disjoint-false-seed-residual-law.md#2-exact-false-seed-rank-gate-by-a-finite-matrix-rank-mixture).
- \(j=t\) (precommitted genuine seed T<=H): a=mt, b=0, h_0=d-t=u, v=c, and the formula reduces to \(P_t=F_c(mt)=p_{\rm row}\), because **every** residual form has rank<=2ell when it annihilates an isotropic u-plane in a D=u+ell ambient space. This is the exact fixed-true-seed public rank-gate rate, not the smaller probability that the residual support algorithm reconstructs H.
- The null fixed-seed formula remains the **separate** unrestricted-null law \(P_0^{\rm null}=q^{-m{t\choose2}}F_{n-t}(mt)\tau_{D,\ell,q}^m\). In general \(P_{j=0}\) for a planted H-disjoint false seed is **not equal** to this null probability.

## 4. Exact planted number of all public passing seeds

For a fixed hidden H, the number of t-planes T with \(\dim(T\cap H)=j\) is the standard Grassmann intersection count

\[
\boxed{
N_j={d\brack j}_q{c\brack t-j}_q
q^{(d-j)(t-j)},\qquad
\sum_{j=0}^{t}N_j={n\brack t}_q.
}
\]

**Proof.** Choose the j-plane J inside H, choose the (t-j)-plane image U in V/H, then represent T/J as the graph of any linear map from U into H/J; there are \(q^{(t-j)(d-j)}\) such graphs. QED.

**Theorem 2 (exact first moment of the *actual public* rank gate, any H prior).** Without sampling or searching for hidden-H membership,

\[
\boxed{
\mathbb E_{\rm planted}[G_t(A)\mid H]
=\sum_{j=0}^{t}N_jP_j
\quad\text{for every fixed H.}
}
\]

The same exact expression holds after averaging over **any** prior on H chosen independently of the forms. The expected genuine passing count is \({d\brack t}_q p_{\rm row}\); the expected **incorrect passing-seed count** is the remaining sum over j<t.

**Proof.** Expand G_t as an indicator sum over **all publicly enumerated t-planes** T, group by fixed overlap dimension j, use Theorem 1 individually for each **precommitted** T and the exact N_j multiplicities. Linearity of expectation requires no independence between public gate events and no assumption about tensor-adaptive seed selection by the eventual enumeration algorithm. Since the result is independent of the particular H, average over any honest H-prior. QED.

The formula is a polynomial-size finite rational **probability evaluator** (rank masses, alternating-corank finite sums and Grassmann counts have polynomial bitlength). It does **not** polynomially evaluate G_t(A) on a particular full public tensor or find a passing T.

## 5. Exact one-independent-seed membership posterior — strictly rank-gate-only

Let T be **uniform on all public t-planes independently** of H and the entire original planted tensor, with any independent H-prior. Reveal **only whether** T passed the public rank gate, not the full tensor, the specific T coordinates, individual contraction rows, nor any subsequent adaptively chosen seed. Then the prior overlap probabilities are N_j/[n choose t]_q for every H, and the gate likelihood conditional on overlap j is the exact P_j. Bayes' rule gives

\[
\boxed{
\Pr[\dim(T\cap H)=j\mid\mathcal G(T,A)]
=\frac{N_jP_j}{\sum_{k=0}^{t}N_kP_k}.
}
\]

In particular, the chance a **single independent gate-passing seed is genuinely contained in H** is

\[
\boxed{
\Pr[T\subseteq H\mid\mathcal G(T,A)]
=\frac{{d\brack t}_q\,p_{\rm row}}{
 \mathbb E_{\rm planted}G_t(A)}.
}
\]

This exact posterior ratio is a **strictly marginalized single-seed event**. It is NOT a posterior conditioned on the complete public tuple, a visible nonuniform H prior at a specified T, an adversarially tensor-adaptive T, or the event that an algorithm has scanned all t-planes and selected one.

## 6. Independently checked finite controls

Take GF(2), n=10, d=c=5, m=2, t=2. Then ell=1, u=3, D=4 and the possible overlaps are j=0,1,2. Exact independent Grassmann enumeration counts and block-law gate rates are:

| j | number N_j of public t-planes | exact P_j |
|---|---:|---:|
| 0 | 158720 | 2822085/33554432 |
| 1 | 15376 | 390285/4194304 |
| 2 | 155 | 9765/16384 |

The plane counts sum to \({10\brack2}_2=174251\). The exact planted expected number of all public gate-passers is

\[
\boxed{\mathbb E_{\rm planted}G_2
=\frac{3898666485}{262144}\approx14872.23238.}
\]

Of these, the expected **genuine H-contained** seed count is \(1513575/16384\approx92.38129\); the remainder, approximately **14779.85109**, comes from wrong seeds. By contrast, under unrestricted null the prior theorem yields \(\mathbb E_0G_2=892701866226555/68719476736\approx12990.52188\), a *different* first moment. These two expectations are **not** exact probabilities of existence or a claim of a polynomial distinguisher.

For the independent uniform T conditioned **only** on its gate flag,

\[
\boxed{
\Pr[T\subseteq H\mid\mathcal G]
=\frac{80}{12879}\approx0.00621166;
\quad
\Pr[T\subseteq H]=\frac5{5621}\approx0.00088952.
}
\]

Thus in this small controlled case the rank gate provides about **6.98-fold enrichment**, but only **0.62%** of gate-passing independent public 2-planes are genuine, even though the gate tests every original public slice on a quotient. This is a **finite negative control**, not an asymptotic cryptographic-rate estimate.

**Independent intermediate-rank enumeration (GF(2) and GF(3)):** in the j=1 block, condition on full row rank of X, then Y has 2 rows and 4 columns; its projected companion Z has 2 rows and 2 columns. Exhausting the ordered Y,Zproject pairs gives full-bottom-rank cases by rank(Y):

- Over GF(2): **6, 540, 3360** at ranks r=0,1,2 among \(2^{12}=4096\) ordered pairs, matching \(\pi_{2,4}(r)F_2(2-r)\) exactly.
- Over GF(3): **48, 23040, 505440** among \(3^{12}=531441\) ordered pairs, matching \(\pi_{2,4}(r)F_2(2-r)\) exactly. The independent GF(3) finite residual-rank mixture gives j=1 rate \(667563520/31381059609\). This is an odd-characteristic control, not a sampled cryptographic experiment.

Together with the already independently enumerated alternating planted-k rank tails in the disjoint-false-seed paper, these checks exercise the new intermediate-overlap block calculation without enumerating full 10-dimensional honest tensor tuples. They are scratch exact arithmetic; **no committed executable attack, source corpus, benchmark or empirical success estimate**.

## 7. Interpretation, limitations, next target

- This is the exact **first moment for all public short seeds**, not a source-concentration theorem. Expectation alone does not prove that a passing false seed exists, is efficiently locatable, or is absent; there is no invalid independent-seed approximation.
- The false-seed distribution **varies with j**; replacing it with unrestricted null for all planted wrong seeds is demonstrably false. The j=0 case and the j=t genuine case remain exact specializations of one consistent original conditional source law.
- The one-independent-uniform-seed posterior conditions **only on the gate bit**, not on the full tensor or tensor-adaptive seed selection. A stronger posterior requires accounting for what the algorithm actually observes.
- The rank gate can be a mathematically sound necessary event for the seeded support solver while admitting many incorrect seeds. This is **not** a contradiction with the exhaustive any-witness attack: only a lifted d-plane accepted by the **entire original verifier** is a successful attack output.
- The next nontrivial attack-first objective remains a polynomial-time algorithm using all public coefficients to **find a promising true short T** (or another accepted d-plane) with a proved unconditional honest-source advantage. A finite rational probability evaluator does not do this.
- No KEM/PKE/OWF, new Field-15 foundation, N1-60/F0-K/A-ID reservation, source experiment, quantum implementation, security claim, README expansion or stage-registry alteration.

**Disposition:** EXACT ALL-OVERLAP PUBLIC RANK-GATE SOURCE FIRST MOMENT / INDEPENDENT-SEED POSTERIOR / FINITE FALSE-SEED NEGATIVE CONTROL. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; HEPMR BENCHMARK ONLY.
