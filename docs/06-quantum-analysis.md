# 06 — Quantum analysis

## Status

No post-quantum security proof exists.

"Shor's algorithm does not obviously apply" is not a security argument.

## Baseline

If inversion were an unstructured search over an (ell)-bit seed, Grover-style search would suggest a square-root reduction in generic exhaustive-search cost.

That observation provides only a baseline. It does not account for exploitable structure.

## Questions to analyze

1. Can the generated reduction graph be searched by a quantum walk more efficiently than generic Grover search?
2. Does the public transformation family encode a hidden-subgroup or hidden-shift structure after an unexpected reformulation?
3. Can topological invariants needed by an attack be estimated quantumly faster?
4. Can collision or claw-finding algorithms improve meet-in-the-middle attacks?
5. Does quantum access to public evaluation change the effective attack game?
6. Are there parameter regimes where classical memory-hard attacks become substantially cheaper quantumly?

## Rule

No parameter set may be called "post-quantum secure." At most, future documents may state measured resistance against a specified set of known classical and quantum attacks.

## MORPH-N1 research admission (2026-10-14)

Field 14 of [MORPH-R0](97-morph-r0-cross-line-postmortem.md#11-re-entry-gate-for-any-new-morph-family) requires checking hidden shift/subgroup structure, finite quotients, quantum search/walk and relevant known quantum algorithms **for the proposed exact public relation**. Field 15 separately demands nontrivial mathematical novelty. For the N1-51 fixed-k/public-low-width example, a polynomial classical public DP already exists; quantum resistance is not reached as a question. See [N1-52](100-morph-n1-status-2026-10-14.md). No quantum-security claim follows from a search timeout or absent specialized attack.
