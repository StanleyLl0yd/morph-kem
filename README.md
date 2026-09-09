# MORPH-KEM

**MORPH-KEM** is an exploratory post-quantum public-key cryptography research project based on hidden discrete Morse reductions and combinatorial topology.

> **Research only. Not for production use. Not a security claim.**
>
> MORPH-KEM is an unproven construction under active cryptanalysis. Do not use it to protect real data, credentials, communications, or systems.

## Research goal

Investigate whether a useful trapdoor primitive can be built around hidden global reduction structure: reduction is efficient when a secret discrete-Morse certificate is known, while recovering an equivalent useful reduction structure from the public representation is difficult on the generated distribution.

The project deliberately separates three questions:

1. Is the underlying mathematical problem well-defined and interesting?
2. Is it hard on the generated-instance distribution, including against quantum algorithms?
3. Can a secure and practical KEM eventually be reduced to that problem?

A positive answer to one does **not** imply a positive answer to the others.

## Current status

**Stage: M2 attack experiment completed; next model not yet accepted.**

Three attack-first models have now been implemented and broken:

- **M0:** exact simplicial-complex object model, canonical bytes, deterministic planted collapse relation, and trapdoor inversion. Broken by **A-000** direct public coordinate recovery in linear time.
- **M1:** globally supported public transformations on one shared scaffold. M0's exact local leak disappears, but **A-008** meet-in-the-middle recovery reduces path search to roughly 2^(ell/2) forward/reverse states.
- **M2:** genuine elementary expansions/collapses with a hidden 3-regular non-collapsible core, a planted reverse-collapse certificate, secret vertex relabeling, and only a public core digest. The reduction space really branches, but M2 is broken by **A-014** structural core recovery: zero-triangle-incidence edges leak part of the hidden core and the remaining core is recovered as a digest-verified 3-regular spanning subgraph.

For the deterministic CI baseline maze-6, A-014 recovers the hidden core in **59 search nodes**, compared with **1095 nodes** for generic bounded collapse DFS. The scaling sweep also recovers maze-4, maze-6, maze-8, maze-10, and maze-12 within at most 520 backtracking nodes for the fixed experiment seed.

Current conclusions:

- local obscurity is not enough;
- global transformation support is not inversion asymmetry;
- non-invertible collapse branching is real, but a planted generator family can leak a much easier reconstruction problem;
- increasing parameters cannot repair a structural generator invariant;
- average-case hardness remains unknown;
- quantum hardness remains unknown;
- no KEM security proof exists;
- no production parameter set exists.

## Repository map

- src/morph_kem/ — executable research objects, constructions, and attacks
- tests/ — correctness, rejection, collision, and attack tests
- scripts/ — reproducible experiment and scaling entry points
- docs/00-overview.md — project scope and research rules
- docs/01-mathematical-foundation.md — mathematical objects and notation
- docs/02-hard-problems.md — provisional HMCP / HMRP / HMCR labels
- docs/03-construction.md — provisional long-term construction direction
- docs/04-security-model.md — target security notions and assumptions
- docs/05-cryptanalysis.md — attacks, failures, distinguishers, negative results
- docs/06-quantum-analysis.md — quantum threat analysis
- docs/07-parameters.md — experiment parameter tracking
- docs/08-open-questions.md — unresolved research questions
- docs/09-toy-model.md — exact M0 relation
- docs/10-m1-path-experiment.md — M1 non-local path model and MITM break
- docs/11-m2-collapse-maze.md — M2 collapse maze and structural break
- spec/morph-kem-v0.1.md — evolving future specification skeleton
- notes/research-log.md — chronological research log

## Run experiments locally

No runtime dependencies outside the Python standard library are required.

~~~bash
PYTHONPATH=src python -m unittest discover -s tests -v

# M0
PYTHONPATH=src python scripts/exhaustive_baseline.py --params toy-8 --seed 0xA5

# M1
PYTHONPATH=src python scripts/mitm_baseline.py --params path-16 --seed 0xB6D3
PYTHONPATH=src python scripts/collision_scan.py --params path-12

# M2
PYTHONPATH=src python scripts/maze_baseline.py --params maze-6 --trials 16 --search-nodes 10000
PYTHONPATH=src python scripts/maze_core_sweep.py --max-nodes 2000000
~~~

## Research principles

- Do not invent new symmetric ciphers, hashes, PRNGs, or ad-hoc arithmetic primitives.
- Treat worst-case NP-hardness as insufficient for cryptographic hardness.
- Treat planted/generated-instance structure as adversarially visible.
- Record successful and failed attacks.
- Prefer falsifiable claims, explicit assumptions, reproducible experiments, and test vectors.
- Never describe the construction as secure merely because no attack is currently known.
- When a model is structurally broken, preserve the break and redesign the model instead of inflating parameters.

## Planned phases

1. **M0:** executable toy relation — complete; broken by A-000.
2. **M1:** non-local reversible path — complete; broken by A-008.
3. **M2:** non-invertible collapse maze — complete; generic branching demonstrated, then broken by A-014 core-structure recovery.
4. **Next:** remove low-complexity planted-core invariants and local incidence leakage before testing a higher-dimensional hidden-Morse construction.
5. Attack every new generated distribution with structural, greedy, canonicalization, CSP/SAT, graph-factor, treewidth, statistical, and learned methods before scaling.
6. Only if a primitive survives: investigate reductions, quantum attacks, and larger parameters.
7. Only after substantial independent review: consider whether a KEM security claim is even plausible.

## Naming

MORPH-KEM is a working research name. The acronym currently refers to **Morse Obfuscated Reduction Path KEM**.

## Citation

Citation metadata is maintained in CITATION.cff. Stable archival releases may later be deposited in a DOI-issuing research archive.

## License

No license has been granted yet. Until a license is added, normal copyright law applies.
