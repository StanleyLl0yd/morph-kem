# MORPH-F0: common-neighbor recovery of hidden random 2-lift fibres

**2026-10-22. Source-exact attack on a regular-base graph-cover class not handled by 1-WL-discrete color recovery.** This is a scoped combinatorial source theorem and a full-original-verifier accepted-witness attack for H=K_n, **not independent mathematical priority, new cryptographic foundation, or a polynomial inverter for all graph coverings**. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD, TI FROZEN comparator, D0 DEFER, D1 HOLD, N1-60 unallocated. No new code, source campaign, benchmark, F0-K or A-ID.

## 1. Unfiltered original source and the actual witness condition

Let H be a **public explicit n-vertex simple graph**. Construct an honestly sampled **two-sheet random lift G** with vertices (u,i), u∈V(H), i∈{0,1}; for every unordered edge {u,v} of H, choose one independent uniform bit \(\sigma_{uv}\) and place edges
\[
\{(u,i),(v,i\oplus\sigma_{uv})\},\quad i=0,1.
\]
Optionally independently apply a polynomial-time vertex permutation or a random-swap relabeling, hiding the sheet labels, the voltage bits and the natural covering projection \(\pi\). Publish P=(H,G), **not \(\pi\)**. Do not condition on regularity of the lift, codegree outcomes or a particular hidden projection: **every random choice is a valid original honest source output**. Sampling n and H by an independent polynomial-time generator is also allowed; all finite guarantees below condition on the exact H.

The complete **original public verifier** accepts any explicit mapping \(\rho:V(G)\to V(H)\) iff \(\rho\) is surjective, preserves every edge, and for every x the restriction \(N_G(x)\to N_H(\rho(x))\) is a bijection. The attack target is **any accepted covering**, not the actual sampled sheet assignment or \(\pi\).

## 2. Exact common-neighbor law on the original random lift

Let \(C_G(x,y)=|N_G(x)\cap N_G(y)|\), computable **solely from the entire public unlabeled G**.

**Lemma 1 (true fibres, deterministic).** For each u, the two distinct lift vertices (u,0),(u,1) satisfy
\[
\boxed{C_G((u,0),(u,1))=0}
\]
for **every** edge-sign pattern, because each base neighbor w contributes distinct lift neighbors in the fibre over w. This remains true after any relabeling.

For distinct u,v∈V(H), let \(c_{uv}=|N_H(u)\cap N_H(v)|\), public base co-degree. For fixed lift vertices x=(u,i), y=(v,j), each common base neighbor w contributes one common lift neighbor **iff**
\[
\sigma_{uw}\oplus\sigma_{vw}=i\oplus j.
\]
Since the edge signs involved for different w are independent uniform bits, their XORs are independent fair bits. Therefore, **conditional on every fixed public base H**,
\[
\boxed{C_G((u,i),(v,j))\sim\operatorname{Binomial}(c_{uv},1/2).}
\]
This is a **precommitted pair** law used only by a union bound; it makes **no false independence assertion** across many selected vertex pairs in one G.

**Lemma 2 (one base-pair false-matching event).** If \(c_{uv}\ge1\), among the four cross-fibre vertex pairs between the two fibres, at least one has \(C_G=0\) exactly when the \(c_{uv}\) independent bits \(\sigma_{uw}\oplus\sigma_{vw}\) are **all equal**. Hence
\[
\boxed{\Pr[\exists\,i,j:C_G((u,i),(v,j))=0\mid H]=2^{1-c_{uv}}.}
\]
If \(c_{uv}=0\), the event is certain, not probability 2. Nothing about these events for different u,v is assumed independent.

## 3. Exact public fibre-recovery algorithm and finite-source bound

Construct the public **zero-common-neighbor graph Z(G)** on V(G), connecting distinct x,y iff \(C_G(x,y)=0\), by adjacency intersections or the off-diagonal entries of \(A_G^2\), in polynomial time.

Define the source-good event
\[
\mathcal E(H,G)=
\{\forall u\ne v,\ \forall i,j,\ C_G((u,i),(v,j))>0\}.
\]
On \(\mathcal E\), Lemma 1 shows **Z(G) consists of exactly the n disjoint genuine fibre pairs**, i.e. a perfect matching. Thus **the unlabeled partition of G into hidden pairs is recovered deterministically and exactly**, without \(\pi\), the sheet bits, or a base-graph isomorphism oracle.

**Theorem 1 (source-faithful pairing attack).** If all public base co-degrees satisfy \(c_{uv}\ge1\), the above public algorithm returns the true fibre partition with conditional probability at least
\[
\boxed{
1-\sum_{\{u,v\}\subset V(H)}2^{1-c_{uv}}
}
\]
(clipped below by zero), and in particular at least \(1-\binom n2 2^{1-\mu}\) for \(\mu=\min_{u\ne v}c_{uv}\ge1\). Work is polynomial in n and \(|E(H)|\), even under arbitrary polynomial-time relabeling of the lift vertices.

**Proof.** True pairs always give Z-edges. On the complementary event to the union of all Lemma 2 cross-fibre false-pair events, no other Z-edges exist. A union bound over the \(\binom n2\) unordered base-fibre pairs bounds the probability of a bad event exactly as stated, with no inter-pair independence assumption. Forming adjacency intersections and finding the isolated matching edges is polynomial. QED.

**Original-verifier WARNING:** for an arbitrary base H, merely recovering the **unlabeled fibre partition** does **not automatically** recover a covering map to the **labeled public H**. The contracted quotient graph Q formed by those pairs is isomorphic to H, but constructing that isomorphism may itself require a nontrivial graph-isomorphism algorithm. Claiming a full original-verifier any-witness inverter from Theorem 1 alone for arbitrary H would be wrong. A separate polynomial constructive isomorphism of Q and H must be supplied where needed.

## 4. Full original any-witness attack on complete, totally 1-WL-invisible bases

Now **fix H=K_n** as the public base, n≥3. The source samples all \(\binom n2\) independent fair 2-lift signs, optionally scrambles all 2n public lift vertices, and publishes (K_n,G). Every G vertex has degree n−1, as does every K_n vertex. **Thus ordinary uncolored joint 1-WL on K_n⊔G starts and remains constant**; the previous [1-WL-discrete base attack](F0-graph-cover-color-refinement-section.md) has **no information** in this source.

But \(c_{uv}=n-2\) for every pair u≠v, so Theorem 1 yields
\[
\boxed{
\Pr_{G\mid K_n}[\text{exact hidden-fibre pairing found}]
\ \ge\ 1-\binom n2 2^{3-n}
\ =1-\frac{n(n-1)}{2^{n-2}}.
}
\]
For n growing with the security parameter, this tends to **one**.

**Theorem 2 (full original verifier accepted witness).** On the above source-good event, the public algorithm reads the n genuine pairs from Z(G), assigns them **arbitrarily bijectively** to the n labeled public vertices of K_n, and outputs the induced map \(\rho:V(G)\to V(K_n)\). That map is surjective and locally bijective: each lift vertex has exactly **one** neighbor in each other recovered fibre and no neighbor in its own, exactly matching its K_n neighborhood. The **unchanged full original verifier** therefore accepts. Hence the unconditional uniform-sign honest-source probability of finding **some accepted cover map** in deterministic polynomial work is at least
\[
\boxed{\max\{0,1-n(n-1)/2^{n-2}\}.}
\]
The attack never needs to recover the sampled assignment of a particular fibre to a particular labeled K_n vertex. This distinction between **any verifier witness** and sampled \(\pi\) is essential.

This is a genuinely different **second-order public statistic** from 1-WL; the high-probability result is not a claim that arbitrary 1-WL-indistinguishable sources are easy. Moreover the verifier here tests a **graph covering**, not any arbitrary isomorphism of a hidden graph label or a parameter-dependent shortcut.

## 5. Independent finite arithmetic controls (not crypto benchmarks)

Exactly enumerating the **edge-bit patterns only** for the small complete bases shows:
- K_5 has \(2^{10}=1024\) sign patterns; the zero-common-neighbor graph Z equals exactly the planted five fibre pairs for **192** patterns.
- K_6 has \(2^{15}=32768\) sign patterns; Z equals exactly the planted six pairs for **6144** patterns.

In both cases the exact pairing success fraction is **3/16**. These are finite scratch exhaustive **voltage-pattern** controls of the stated event, not enumerations of all shuffled labeled public graphs, committed repository attack programs, measured attack runtime, source datasets, cryptographic security levels or asymptotic empirical evidence. The union bound is intentionally conservative and is vacuous for such tiny n. The asymptotic high-success claim follows from the theorem, not these controls.

## 6. Source/literature boundary and next admission gate

The **random 2-lift/source itself is classic**, see [Bilu–Linial, *Ramanujan Signing of Regular Graphs*, Combinatorics, Probability and Computing (2004)](https://doi.org/10.1017/S0963548304006509), and [Amit–Linial–Matoušek, *Random Lifts of Graphs* (2002)](https://doi.org/10.1002/rsa.10003). Graph-cover verification and complexity are covered by [Bok–Fiala–Jedličková–Kratochvíl–Seifrtová, *Computational Complexity of Covering Colored Mixed Multigraphs with Simple Degree Partitions*](https://arxiv.org/abs/2502.20151) (2025 preprint/2026 journal). The proof above is an elementary public common-neighbor/source-counting calculation; **no independent priority claim** is made for this statistic or theorem. Worst-case covering NP-hardness does not justify planted-lift average-case hardness.

If public H has small/zero pair co-degrees, the fibre-recovery estimate can be vacuous; failure then is **not proof of hardness**. If H has large co-degree but lacks efficient explicit quotient-to-H isomorphism, only unlabeled fibre pairing is proved. Additional colored-edge rules, k>2 sheets, nonhonest G or hidden H are different original relations; no attack is automatically transferred.

**Disposition: D2 dense/codegree 2-lift pairing screen** and **K_n complete-base any-cover inversion** are **ANALYTIC REJECT** under their precise original-source conditions. This adds a strong negative attack family *outside the reach of vertex 1-WL alone*, but does not nominate any cryptographic foundation or justify another sequence of increasing k/degree/graph size. Nontrivial base isomorphism residuals and genuinely different prior-art-supported mathematical objects require an independent MORPH-R0 Field-15 gate before any samples or implementation.
