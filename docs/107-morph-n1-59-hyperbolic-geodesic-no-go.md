# N1-59 - rational hyperbolic geodesic cosine-distance inversion (analytic no-go)

**Date:** 2026-10-14. **Status:** ANALYTIC REJECT; GLOBAL NO NOMINATION; **0 empirical cases**.

This document is a faithful transcription of the full 15-field specification, exact inversion identity and domain restrictions first published in [MORPH-N1 #196, comment 6176155839](https://github.com/StanleyLl0yd/morph-kem/issues/196#issuecomment-6176155839), following an earlier distinct literature-only screen. This is not source code or an independently executed run, and does not modify historical experiments.

## N1-59 (2026-10-14): rational Lobachevsky geodesic cosh-distance inverse - anchored exact public root (ANALYTIC REJECT)

**Complete 15-field MORPH-R0 test after prior-art pre-screen 6176123156**, independently specified for a **one-dimensional hyperbolic geodesic**, NOT a theorem about every higher-dimensional, incomplete or arithmetically constrained hyperbolic embedding. Continuous negative-curvature point geometry differs from graph shortest-path families N1-25..29, though both are mature inverse-distance subjects. **Zero experiments, research-only, GLOBAL NO NOMINATION.**

### Mandatory all 15 fields

1. **PublicInstance:** n>=3 and complete exact rational symmetric matrix C with `C_ij=cosh(d_H(p_i,p_j))` for n labeled points on a single geodesic of H^1. Public entries represented as reduced integer numerator/denominator pairs; n and its honest source support are known.
2. **Secret/Witness:** hidden integers `t_0=1` and independently varying `t_i∈{2,...,2n+1}` for i>=1. Map `t_i>0` to hyperboloid coordinates `p_i=((t_i+t_i^{-1})/2,(t_i-t_i^{-1})/2)`, satisfying `p_{i,0}^2-p_{i,1}^2=1` and future orientation. Any allowed integer tuple reproducing C is a verifier-valid witness; planted sampling coins irrelevant.
3. **Generation distribution:** t_0=1 fixed and t_1,...,t_{n-1} iid uniform on 2n integers {2,...,2n+1}, with repetitions allowed (no conditioning on distinctness or on public output). Compute all `C_ij=(t_i/t_j+t_j/t_i)/2` exactly. Bit cost and output size O(poly(n,log n)); inverse fractions have O(log n) individual bitlength.
4. **Public verifier:** check t_0=1, each other t_i within the specified integer range, reconstruct all exact rational C_ij by the displayed formula and compare numerator/denominator exactly. Polynomial integer-arithmetic bit cost, not floating-point approximate distances.
5. **Attacker-success target:** `Equivalent(P)={t∈Z^n: t_0=1, 2<=t_i<=2n+1 for i>0, forall i,j (t_i/t_j+t_j/t_i)/2=C_ij}`. ANY accepted t wins.
6. **Stabilizer/fibre:** fixed t_0 and restriction t_i>1 remove common hyperbolic translation and reflection. Each C_0i fixes unique t_i>1, so every honest P has **singleton** accepted fibre. Repeated t_i values are permitted, but labels and anchored recovery remain well-defined.
7. **Known quotient/representation:** hyperbolic line isometry, Lorentzian Gram matrix, hyperbolic multidimensional scaling (h-MDS), exact embedding from full hyperbolic point distances; not new geometry-based OWF.
8. **PUBLIC INVERTER:** set `t'_0=1`. For each i>0 compute `r_i=C_0i=(t_i+t_i^{-1})/2` and **`t'_i=r_i + sqrt(r_i^2-1)`**, choosing the positive rational square root. On honestly generated profiles, `r_i^2-1=((t_i-t_i^{-1})/2)^2`, so `sqrt(r_i^2-1)=(t_i-t_i^{-1})/2` as t_i>1 and **t'_i=t_i exactly**. Exact rational perfect-square test and integer square-root extraction are polynomial in input bitlength. Every C'_ij reproduces original P; even the anchor-only public row already recovers the source.
9. **Local/low-weight:** n-1 anchor values C_0i suffice to reconstruct all n(n-1)/2 off-diagonal published distances; most pairwise data redundant. The hidden Lorentz coordinate frame and non-Euclidean geometry do not hide an accepted witness.
10. **Noise:** none, EXACT rational cosh distances, no roundoff. Real-valued approximations, logarithmic distances, sparse edges, unknown anchor/frame or restrictions on a higher-dimensional lattice are different relations; no extrapolation.
11. **Cover/base/fibre:** the future-sheet hyperboloid and reference p_0=(1,0) are public by witness-domain definition. No hidden covering space or difficult gauge choice.
12. **Matched weak control:** full pairwise C with anchor row withheld is a lower-information counterpart for the identical generated source, but no benchmark is computed and no hardness claimed. Full C (in fact one row) admits a deterministic exact section.
13. **Validation:** **0 empirical cases**, no source samples, scripts, preregistered sweeps or verifier runs. Deterministic identity already kills the specified proposal. Preserve N1-52 historical 593,305 heterogeneous full cases +40 controls; no recounted controls.
14. **Quantum screen:** polynomial exact classical inversion solves every honest instance; no valid post-quantum hardness claim for this relation.
15. **Field-15 novelty:** **FAIL**. The broad method is classical hyperbolic distance geometry / h-MDS: [Sala et al., Representation Tradeoffs for Hyperbolic Embeddings, ICML 2018](https://proceedings.mlr.press/v80/sala18a.html) explicitly give exact hyperbolic point recovery from complete distances; [Tabaghi and Dokmanić, Hyperbolic Distance Matrices (2020)](https://arxiv.org/abs/2005.08672) give Lorentz Gramian/semidefinite and spectral factorization methods. This exact **1D rational anchored square-root special case is proved here**, not attributed as verbatim to those papers.

### Theorem and precise boundary

On this honest distribution the entire verifier-valid witness t is reconstructed from the public anchor row by n-1 rational perfect-square roots, each provably exact for t_i>1. This does not imply polynomial-bit exact recovery for *arbitrary* higher-dimensional algebraic hyperbolic point sets, unknown rationality domains or incomplete/nonchordal measurements. It does prove that the simple proposed *complete anchored geodesic cosh-distance* family is not a new inversion primitive.

**N1-59 ANALYTIC REJECT, GLOBAL NO NOMINATION; next independent Field-15 gate N1-60.** No KEM/PKE/trapdoor/OWF/PQ claims; no source code, trials, extra AP sweeps, parameter rescue, or historic partial backfill.