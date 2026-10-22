# MORPH-F0: full-public any-reset inversion for synchronizing automata

**2026-10-22. Independent automata-theoretic attack-first screen, ANALYTIC REJECT for the specified complete-DFA any-reset verifier.** This is the classical *pair automaton* construction, not new mathematical priority, an OWF/PKE/KEM, an average-case cryptographic assumption, or a new stage. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; planted-TI FROZEN, D0 deferred, D1 nonpermutation HOLD, D2/D3 screened; N1-60 remains unallocated. Zero new committed attack programs, test samples, benchmarks or security parameters.

## 1. Strict original public source and complete verifier

Let a **complete deterministic finite automaton** be an explicitly represented triple A=(Q,Σ,δ), where n=|Q|≥2, alphabet Σ is explicitly listed and δ:Q×Σ→Q is a total public transition table, all polynomial-size. A word w acts on all states via the extended transition δ(Q,w)={δ(q,w):q∈Q}. An **unconditional strict-polynomial** honest source chooses a synchronizing DFA A, computes some polynomial-length reset word s via any declared procedure (a planted witness), **keeps s private**, and publishes P=(A,B), where the public accepted-word length budget is
\[
\boxed{B=(n-1)\binom n2.}
\]
The full original verifier accepts **any** explicitly spelled out word y∈Σ* with |y|≤B and
\[
\boxed{V(P,y)=[|\delta(Q,y)|=1].}
\]
It does **not** require the output state to have a given label, that y is shortest, or that y equal the planted secret s. Parsing and evaluating all n states under a word of length B are polynomial. Unconditional source means no postselection after an attack, and all honest published instances must have some accepted word.

**Concrete unconditional source without hidden oracle or rejection:** choose n=2^r≥4 with n polynomial in the security index, take the standard n-state Černý automaton on Q={0,...,n−1}, Σ={a,b}, with δ(i,a)=i+1 mod n and δ(i,b)=i except δ(n−1,b)=0. Relabel states by a cyclic shift from exactly r random bits; optionally swap a and b by one more random bit. The generator constructs a reset word via the public pair algorithm below (or a conventional polynomial source), checks it passes and withholds the word. All choices are exact finite random bits; **no conditioning** on an attack success, random permutation-rejection loop or hard-to-sample promise. The source is transparently vulnerable by design, as required for a negative control; it does not claim this supports all synchronizing automata or cryptographic unpredictability.

The theorem itself applies to **every** synchronizing explicitly represented complete DFA A, under **any** unconditional polynomial-time distribution supported on those A, not just Černý's.

## 2. Exact public pair-automaton lemma

Define the public directed pair graph with vertices all unordered distinct pairs {p,q}⊆Q, plus one absorbing symbol D for a merged pair. For each input letter a∈Σ,
\[
\{p,q\}\xrightarrow{a}
\begin{cases}
D,&\delta(p,a)=\delta(q,a),\\
\{\delta(p,a),\delta(q,a)\},&\text{otherwise}.
\end{cases}
\]
The absorbing D transitions to itself. It has at most \(\binom n2+1\) vertices and O(|Σ| n²) arcs, built directly from the public transition table.

**Lemma.** For a synchronizing A, **every** distinct pair {p,q} has a word u of length ≤\(\binom n2\) merging its two states.

**Proof.** There exists a reset word s, so its action merges p,q. Thus D is reachable from the pair vertex. A shortest path cannot repeat any distinct-pair vertex, so it has ≤\(\binom n2\) edges before first reaching D. BFS computes a shortest word using polynomial time and memory. No secret s is used and no shortest *global reset* is computed. QED.

## 3. Pointwise public section satisfying the original verifier

**Theorem (public original any-witness attack).** Starting with the full state set S=Q, while |S|≥2 choose **any** two distinct states p,q∈S, use the public pair graph and BFS to obtain a merging word u, append u to current output w and update S←δ(S,u). A deterministic transformation cannot increase |S| and this u merges two **current** states, so |δ(S,u)|<|S|. After at most n−1 iterations the state set is a singleton, hence w is an accepted reset word. Each appended word has length ≤\(\binom n2\), so
\[
\boxed{|w|\le(n-1)\binom n2=B.}
\]
The attacker invokes the **full original verifier** before returning w and succeeds on every honestly generated public P of this interface. Computing BFS from O(n²) pairs at most n−1 times and simulating states is deterministic polynomial time in n, |Σ|, and the transition table. It neither enumerates exponentially many subset states nor searches over all possible words.

**Source-law corollary.** For any unconditional polynomial-time honest source supported on explicitly represented synchronizing complete DFA A with this original B-budgeted any-reset verifier,
\[
\boxed{\Pr_{P\sim D}[V(P,\mathcal A(P))=1]=1.}
\]
The complexity of **shortest** reset words, source-secret recovery or the entropy of hidden planted words is irrelevant to this original accepted-witness relation.

## 4. Exact finite control and alternate verifiers that do NOT follow

For n=4 the Černý A above has a(i)=i+1 mod4 and b=(0,1,2,0) as images of states 0,1,2,3. A deterministic sorted-pair BFS and greedy reduction of S finds
\[
w=\mathtt{aaabaaabaaab},
\qquad |w|=12\le B=3\binom42=18.
\]
Directly applying the public transitions to all four states produces the same final state 0. On n=2,3,5,6,7,8 the same simple algorithm also returns accepted words of lengths respectively 1,6,20,30,42,56, all within B. These are **tiny scratch sanity calculations**, not a new repository regression suite, sampled cryptographic source, runtime measurement or new A-ID.

The theorem is **not** a polynomial shortest-reset-word algorithm. The decision problem for a reset word of length ≤L with **smaller user-specified L** is NP-complete in established automata literature; it does not follow from the public B-length acceptance above that a word meeting a shorter bound exists or can be found efficiently. A verifier that also fixes a **particular terminal state**, asks for a *simple/unique* history, constrains path penalties, uses partial transition maps with "careful" undefined transitions, or represents an exponentially large state set succinctly is a different relation. The generator must separately prove that the exact altered verifier has a polynomial witness under its unconditional law; a change of verifier is **not** a repair of the previous crypto claim.

## 5. Existing theory and disposition

Synchronizing DFAs, the polynomial pair-graph synchronizability criterion and greedy reconstruction are established: [Volkov, *Synchronization of finite automata*, Russian Mathematical Surveys 77(5), 2022](https://www.mathnet.ru/eng/rm10005), §2.1 and §3.2; [Eppstein, *Reset sequences for monotonic automata*, SIAM Journal on Computing 19(3), 1990](https://doi.org/10.1137/0219033) (separate restricted class and earlier synchronizing sequence literature); and [Szykuła, *Improving the Upper Bound on the Length of the Shortest Reset Word*, STACS 2018](https://doi.org/10.4230/LIPIcs.STACS.2018.56). The latter provides substantially **better** cubic general upper bounds, and the famous Černý quadratic bound remains a **conjecture**, not an established universal theorem. [Kisielewicz–Kowalski–Szykuła, *Computing the shortest reset words of synchronizing automata*, 2015](https://doi.org/10.1007/s10878-013-9682-0) addresses the hard shortest-word optimization task. None of this is independently new MORPH mathematics or a post-quantum one-way function.

**D4 full-public any-reset class: ANALYTIC REJECT.** Increasing n, hiding sampled state names, choosing a high-complexity Černý instance, enlarging the alphabet, or adding another public nonlinear-looking transformation does not defeat the pair-graph attack on this original verifier. Shortest-word variants belong to mature optimization/automata problems and are **not admitted** to MORPH as independent Field-15 evidence. Do not allocate N1-60, build a KEM, or embark on a toy experiment campaign. Leave H-C broad HOLD, and continue selection of genuinely independently motivated mathematical relations before any new original source.
