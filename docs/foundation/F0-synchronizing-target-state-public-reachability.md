# MORPH-F0: prescribed-target reset words are a public reachability section

**2026-10-22. Final bounded D4 automata verifier clarification, ANALYTIC REJECT when the original length budget permits public pair compression plus a state path.** Extends the [any-reset public section](F0-synchronizing-automata-public-any-reset-section.md); standard deterministic-automata graph theory, no independent priority/hardness/primitive claim. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; TI FROZEN comparator; N1-60 unallocated. No code, benchmark, crypto source trial, F0-K/A-ID.

## 1. Distinct full original verifier, with no planted-word recovery

A complete deterministic finite automaton A=(Q,Σ,δ) is given by a public explicit polynomial-size transition table, n=|Q|≥2. The public instance is \(P=(A,t)\) where a **specific output state** t∈Q is published. Define
\[
 B=(n-1)\binom n2,\qquad B_t=B+n-1.
\]
The complete original verifier accepts **any** spelled-out word y∈Σ* such that
\[
\boxed{V_{\rm target}(P,y)=
[\,|y|\le B_t\ \land\ \delta(Q,y)=\{t\}\,].}
\]
The source must be an *unconditional* polynomial-time generator supported on synchronizing A and reachable reset targets t, and must produce no unsatisfiable published P. It can retain some planted reset-to-t word as a private witness, but finding that particular word is **not** the game.

A strict random-bit sample family: let n=2^r≥4 grow at most polynomially, construct the binary Černý automaton with a(i)=i+1 mod n and b(i)=i except b(n−1)=0, apply an r-bit sampled cyclic state renaming and optional letter swap, and choose **a public target t uniformly from Q using a separate r random bits**. Its a-letter acts transitively on Q, so every t is reachable from any reset state; all draws are valid, **without postselecting targets**. A planted witness can be computed by the honest polynomial procedure given below and withheld. This source is deliberately easy and not a cryptographic candidate.

## 2. Exact criterion and full-public constructive algorithm

Run the polynomial pair-state BFS/greedy-compression algorithm of the [D4 no-go](F0-synchronizing-automata-public-any-reset-section.md) on public A. It either establishes that A is not synchronizing or outputs a reset word w0 with \(|w_0|\le B\) and public final state \(r\) satisfying \(\delta(Q,w_0)=\{r\}\).

**Theorem (prescribed target section).** Conditional on A being synchronizing and fully represented, the following are equivalent for **any** publicly specified target t:
1. Some (possibly arbitrarily long) word v has \(\delta(Q,v)=\{t\}\).
2. State t is reachable from state r in the **public single-state transition graph** of A.
3. There is a reset word y to t of length \(|y|\le B_t\), publicly computable in deterministic polynomial time.

**Proof.** (1)→(2): since r∈Q, applying v to r yields δ(r,v)=t, so v labels a walk from r to t. (2)→(3): a shortest simple path from r to t in the n-vertex public transition graph has ≤n−1 edges and BFS returns its label u. The concatenation y=w0u maps **every** original state first to r and then to t. Its length is at most B+(n−1)=B_t, and the **full original verifier** checks and accepts it. (3)→(1) is immediate. The construction uses only the public transition table, pair-graph BFS and ordinary state-graph BFS; no hidden word or shortest-reset threshold is needed. QED.

**Source-law corollary.** On **every** published instance of **any** unconditional polynomial honest generator satisfying the original synchronizing + resettable-t support requirement, the attack outputs an accepted original witness with probability one. If a publicly specified target set \(T\subseteq Q\) replaces t and the verifier accepts a reset into **any t∈T**, a public BFS from r to T gives exactly the analogous existence criterion and witness bound B_t, provided some t∈T is resettable. This does NOT change the original single-target theorem.

**What is not proved:** an accepted reset word meeting a *smaller* prescribed length limit L, a shortest reset word, a reset ending in a state not publicly reachable from r, careful synchronization of partial transition systems, or exponential succinct state encodings. Lowering L changes the verifier and can reintroduce known NP-hard shortest/reset optimization problems. This theorem does not conclude that any differently constrained automata inverse problem is easy.

## 3. Tiny exact controls and false hardening attempt

For n=4 the public Černý pair attack produces \(w_0=\mathtt{aaabaaabaaab}\) of length 12, reset state r=0; a maps i→i+1 mod4. The demanded output t=2 is reached by public suffix u=\(\mathtt{aa}\), so the original full target verifier accepts \(\mathtt{aaabaaabaaabaa}\), length 14≤\(B_t=3\cdot6+3=21\). Under this source, uniform public t has \(\log_2 n\) bits of target entropy yet **does not increase any-witness hardness**.

Independent small *scratch* exhaustive control: among all \(3^{3\cdot2}=729\) complete two-letter three-state transition tables, 549 are synchronizing. These admit a total of 1173 distinct (A,t) resettable target pairs. The public pair-BFS + target-state BFS outputs a word accepted by the full targeted verifier for **all 1173**, each of length ≤8 (since B_t=(3−1)C(3,2)+2=8). This is exact tiny finite mathematical checking, **not** committed executable tests, a random honest crypto source distribution, calibrated performance or new attack ID.

**Feasibility counterexample:** Q={0,1}, alphabet {a,b}, a maps both states to 0, b fixes both. It is synchronizing (a resets to 0), but no transition sequence from reset state r=0 reaches 1. Thus the original verifier demanding terminal t=1 is **unsatisfiable**. Silently postselecting successful generated t or assuming every target is resettable would change the source and is not permitted.

## 4. Prior art, closure and actual research decision

The algebra of synchronizing automata, public state-pair tests, shortest reset word bounds and polynomial reset reconstruction are classical: [Volkov, *Synchronization of finite automata* (2022)](https://www.mathnet.ru/eng/rm10005), [Szykuła STACS 2018](https://doi.org/10.4230/LIPIcs.STACS.2018.56), and [Kisielewicz–Kowalski–Szykuła, *Computing the shortest reset words of synchronizing automata* (2015)](https://doi.org/10.1007/s10878-013-9682-0). The new display is only an elementary public graph-reachability corollary of these existing algorithms and claims no mathematical precedence. No independently distinct Field-15 inversion assumption or average-case post-quantum security arises from a hidden reset word, high-entropy target label, long permitted histories or a relabeled transition monoid.

**D4 any-reset AND prescribed-target bounded-length families: ANALYTIC REJECT.** Do not commission further letter-count/state-count/target-label variants without an independently identified relation and a substantial new source-first attack question. H-C remains **HOLD** as a broad conceptual hypothesis; the program should prioritize independent mathematical object selection, not serial automata extensions.
