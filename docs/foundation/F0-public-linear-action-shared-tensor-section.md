# MORPH-F0: public linear-decomposition completion of commuting tensor actions

**2026-10-22. Source-faithful negative screen of a published 2026 tensor-action proposal, not a new hardness assumption or cryptographic construction.** Research only. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD, D0 DEFER, D1/D2/D3/D4 screened, planted-TI FROZEN comparator. No new N1/F0-K/A-ID, OWF/PKE/KEM, experiment, implementation or security claim.

## 1. Independently published origin, not MORPH priority

[Chen and Wang, *Tensor--Action Ko--Lee Cryptography: A Framework and Structural Cryptanalysis of Commuting Subgroup Constructions*, arXiv:2608.15030 (15 August 2026)](https://arxiv.org/abs/2608.15030) explicitly show that public finite generating sets for commuting matrix-action subgroups permit deterministic polynomial **shared-tensor** recovery without recovering either secret. The general linear-decomposition/algebraic-span attack predates 2026: [Myasnikov–Roman'kov, *A linear decomposition attack*, arXiv:1412.6401 (2014)](https://arxiv.org/abs/1412.6401). The present note supplies an independently checkable full-public, exact-honest-source *completion relation* and a short proof of that known mechanism. It is **not** a new attack-priority claim, a claim about all tensor isomorphism, or independent MORPH-R0 Field 15.

## 2. Original published-data source and public acceptance relation

Let V=\(\mathbb F_q^N\) be explicitly represented, with \(N\) and \(\log q\) polynomial in the security parameter, and let \(\mathcal A=(A_1,\ldots,A_r)\) and \(\mathcal B=(B_1,\ldots,B_s)\) be **public** efficiently represented invertible \(N\times N\) matrices satisfying **cross commutation**
\[
\boxed{A_iB_j=B_jA_i\quad\text{for every }i,j.}
\]
Members within \(\mathcal A\) or within \(\mathcal B\) need **not** commute. Honest polynomial-time source chooses an explicitly polynomial-length word a in the A generators (possibly using publicly computable inverses) and similarly b in the B generators, chooses x by any polynomial-time distribution on V, and publishes
\[
P=(q,\mathcal A,\mathcal B,x,y=ax,z=bx),
\]
while withholding a, b and the purported shared tensor \(k=az=by\). The entire unfiltered source is admitted; no conditioning on ranks, generic x, orbit dimension, eigenstructure, algebraic independence or tensor strength. Every source draw is a valid transcript.

For a strictly polynomial *unconditional example*, let \(N=4\), choose \(\mathbb F_3\), take public \(A=X\otimes I_2\), \(B=I_2\otimes Y\) for invertible unipotent \(2\times2\) matrices X,Y, and sample fixed-polynomial words and x from explicitly generated field bits. A constant toy shows interface consistency, **not** scalable candidate security. More generally, any polynomial generator outputting validated cross-commuting explicit matrices suffices; a rejection sampler that might fail exponentially is **not** silently assumed polynomial.

**Original publicly verifiable completion target.** Define from public A generators and x,z the *canonical orbit-pair closure* as in §3, yielding two public matrices \(U,V_{\rm orb}\) with equal column count R and linearly independent columns of U. The **full original acceptance verifier**, fixed for this screen, accepts **any candidate** \(c\in V\) exactly when
\[
\boxed{\exists\,\alpha\in\mathbb F_q^R:\ U\alpha=y,\quad V_{\rm orb}\alpha=c.}
\]
It checks all equations and the public transcript, not a planted secret word. It is a deterministic polynomial-time verifier: compute U,V_orb, Gaussian-solve Uα=y, and check V_orb α=c. Because U has independent columns the α, and hence accepted c, is unique for every honestly generated tuple. This makes a rigorously **public-verifier MORPH screen for the shared-tensor completion task**. Native Ko--Lee key-agreement transcripts do not necessarily expose this artificial public verifier; the separate shared-key **prediction** attack below nevertheless does not require it. Do not confuse this public completion test with a proof of security of any encrypted-message protocol.

## 3. Polynomial public orbit-pair closure and exact shared tensor

Start with an empty basis, and process the candidate **paired vectors** \((x,z)\). Maintain a list \((u_i,v_i)\) where there exists a publicly recorded A-generator word \(g_i\) satisfying \(u_i=g_ix\), \(v_i=g_iz\). Add the pair only if its first component u_i increases the rank of the list of first components. For every newly accepted pair and **each** public generator \(A_j\) (and inverse \(A_j^{-1}\) if secret words allow inverses), queue \((A_j u_i,A_j v_i)\). Continue until no first-coordinate rank extension is possible. Starting at x=0 yields the zero-dimensional closure (y=z=k=0), handled directly.

**Lemma 1 (closure and bounded size).** The resulting first-coordinate basis spans
\[
W=\mathrm{span}_{\mathbb F_q}\{g x:\ g\text{ any word in the public A generators}\}.
\]
It has R≤N columns and the queue examines at most \(O(rN)\) generator transitions (times a polynomial number of field operations). **Proof:** each accepted vector increases the rank, so at most N are accepted. At termination the span contains x and is invariant under each chosen A generator. Hence it contains every semigroup word action on x; inverses explicitly included when required. Conversely each basis vector is a word action. QED.

**Lemma 2 (paired-vector consistency).** If \(\sum_i\alpha_i u_i=0\), then \(\sum_i\alpha_i v_i=0\). **Proof:** the hidden honest B word b commutes with every A generator and its inverse. Thus \(v_i=g_i(bx)=b(g_ix)=bu_i\), and \(\sum\alpha_i v_i=b\sum\alpha_i u_i=0\). This proof uses b only to establish correctness; **the algorithm never knows b**. QED.

**Theorem (deterministic full-public accepted witness and shared secret).** Solve
\[
 U\alpha=y
\]
publicly; the linear system is consistent on **every** honest source because y=ax belongs to W. Output
\[
\boxed{c=V_{\rm orb}\alpha.}
\]
By Lemma 2 this is independent of representation and equals
\[
V_{\rm orb}\alpha=b(U\alpha)=by=ba x=abx=az=k.
\]
Thus it is exactly the **shared tensor**, recovered without solving for a or b; and the complete public completion verifier in §2 accepts c. Construction is deterministic polynomial in N, number of public generators, word-independent public tensor dimension and \(\log q\). Its success over the **unfiltered** honestly generated transcript source is exactly 1, not merely generic-parameter or random-instance success. No tensor-isomorphism solver, discrete-log oracle, group-word recovery, factorization, computational hardness assumption or hidden-secret extraction is required.

The theorem remains true when V is the vectorization of a cubic d×d×d tensor with \(N=d^3\), provided each public action is an explicitly computable linear map on V (including the modewise \(GL_d^3\) action). Its bound is polynomial in the actual public tensor bitlength, **not in a hypothetically compressed exponential ambient space**.

## 4. Complete tiny finite control and exactly what it does NOT establish

Over \(\mathbb F_3\), choose
\[
X=\begin{pmatrix}1&1\\0&1\end{pmatrix},\quad
Y=\begin{pmatrix}1&0\\1&1\end{pmatrix},\quad
A=X\otimes I_2,\quad B=I_2\otimes Y
\]
and public x=(1,0,1,1) in ordered tensor-product coordinates. Choose hidden a=A² and b=B². The public transcript is y=a x=(0,2,1,1), z=b x=(1,2,1,0). The public paired orbit vectors for A^0,A^1,A^2 suffice; y equals the A² orbit vector, so the recovered key is
\[
\boxed{c=A^2z=(0,2,1,0)=B^2y.}
\]
These are exact four-dimensional mod-3 scratch arithmetic controls, not any committed code, benchmark, cryptographic source measurement, security parameter or meaningful proof of new hardness.

**Failure boundaries:** publicly missing matrix-action generators; succinctly represented exponentially large modules; nonlinear actions lacking an efficient public faithful representation; secret action outside the generated subgroup; only approximately commuting cross-actions; a changed verifier testing secret word recovery or a different ciphertext/CCA game. Such changed relations are **not thereby secure**; only this public linear-decomposition theorem stops applying. Information-theoretic/cryptographic challenges with noisy approximate commutation are outside scope. No claim that *all* tensor-action or tensor-isomorphism problems are easy.

## 5. Final program disposition

**Public finitely-generated commuting linear-action shared-tensor completion: ANALYTIC REJECT** for the exact full-public interface above. Its native shared-secret computation is broken pointwise as described in independently published 2026 cryptanalysis, a reincarnation of earlier linear-decomposition attacks. Increasing matrix or tensor dimension, entropy of secret generator words, or algebraic complexity of the underlying subgroup cannot repair this specific finite-generator **linear** public transcript. A *different* mathematical inverse relation with polynomial original honest sampler, full verifier, available quantum algorithms and positive independent MORPH-R0 Field 15 would be required before any new MORPH experiment or candidate. GLOBAL NO NOMINATION and all historical negative work remain unchanged.
