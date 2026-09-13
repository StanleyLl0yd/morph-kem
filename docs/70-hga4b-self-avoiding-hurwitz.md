# 70 — HGA4b self-avoiding Hurwitz action-state generator

## Status

**HGA4b is rejected as a planted-history generator by HGA-A006.** Exact self-avoidance removes literal repeated action states, but it does not make generated histories reliably near-geodesic. In addition, the declared greedy generator has an explicit deterministic dead-end on one official sweep sample.

HGA4b keeps the HGA4 infinite Hurwitz/free-group action, source distribution, public verifier and exact MITM attack unchanged. It changes only the planted-history generator.

HGA4b is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Generator

Reuse the HGA4 action of `B3` on triples of reduced words in `F(a,b)`. For requested lengths `L in {8,12,16,20}`:

1. sample exactly the same source-state distribution as the paired HGA4 control;
2. keep the exact action states already visited on the planted path;
3. at each step enumerate the four public Hurwitz generators in deterministic seeded order;
4. take the first successor not already on the current path;
5. if no successor exists, fail explicitly at that step; do not restart or inspect an attack result;
6. publish the endpoint after exactly `L` successful self-avoiding steps.

The generator never queries MITM distance, shortest connectors, canonical forms, quotient output, or any attack result.

## HGA-A006

The public attack is unchanged from HGA4:

- exact invariant total free-group product;
- free-abelianization quotient exposing the induced `S3` strand permutation;
- exact bidirectional BFS/MITM in reduced tuple states to the public word bound;
- shortest equivalent connector among public meet states;
- exact endpoint verification.

Planted-word equality is reference-only. Any equivalent connector is attacker success.

## Fixed Python 3.12 result

For `hga4b-L20`:

```text
requested / achieved length:             20 / 20
distinct planted path states:                 21
generator dead ends:                           0
source component lengths:                 (4,1,2)
target component lengths:          (968,709,1680)
forward / backward MITM depth:              10 / 10
forward / backward states:           11047 / 11047
forward / backward transitions:      21484 / 21484
meet states:                                  51
recovered connector length:                   16
endpoint verified:                           yes
matches planted word:                         no
>=25% shorter than planted:                   no
```

The fixed longer calibration therefore does **not** itself trigger the 25% shortening gate; its recovered connector is 20% shorter than planted.

## Eight-seed paired sweep

Across lengths 8/12/16/20 and eight declared seeds:

- **31/32** HGA4b samples generate the requested self-avoiding path successfully;
- `hga4b-L12`, seed 7 deterministically reaches a genuine generator dead end at **step 5**; this is preserved explicitly and no restart is allowed;
- all **31/31** successfully generated endpoints receive verifier-accepted public MITM connectors;
- **19/31** successful self-avoiding samples still have an equivalent connector at least **25% shorter** than the planted history;
- by length, material shortening occurs on `5/8`, `3/7`, `5/8`, and `6/8` successful HGA4b samples for L=8/12/16/20 respectively;
- every successful recovered connector is allowed to differ from the planted word; that is attacker success, not a mismatch failure;
- the paired original locally-reduced HGA4 control has material shortening on **21/32** measured samples.

Thus self-avoidance improves some endpoints but does not qualitatively remove non-geodesic planted histories. At L20 the exact half-ball reaches roughly 11,047 states per side on the full-depth samples, so the repository also preserves the fact that generic MITM state growth is becoming nontrivial on these toy calibrations. That growth is **not** a hardness claim.

## Interpretation

HGA4b fails for two independent generated-distribution reasons:

1. a deterministic local greedy self-avoiding rule can terminate early even though the underlying action orbit continues;
2. among successful samples, substantial equivalent shortening remains routine (`19/31`).

This does **not** structurally reject the infinite Hurwitz action family itself. It rejects this simple planted-history mechanism as a basis for advancing toward a primitive.

A successor must condition on a public constructive notion stronger than path self-avoidance without secretly querying the attack target. Candidate gates should include exact-distance shell construction on bounded calibrations, stabilizer/canonical-form probes, finite representation quotients and equivalent-connector multiplicity. Simply increasing `L` is not a repair.

No one-wayness, asymptotic hardness, post-quantum security, IND-CPA/CCA, or production-security claim exists.
