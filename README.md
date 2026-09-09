# MORPH-KEM

**MORPH-KEM** is an exploratory post-quantum public-key cryptography research project based on hidden discrete Morse reductions and combinatorial topology.

> **Research only. Not for production use. Not a security claim.**
>
> MORPH-KEM is an unproven construction under active cryptanalysis. Do not use it to protect real data, credentials, communications, or systems.

## Research goal

Investigate whether a useful trapdoor primitive can be built around hidden global reduction structure: reduction is efficient when a secret discrete-Morse certificate is known, while recovering an equivalent useful reduction structure from the public representation is conjectured to be hard.

The project deliberately separates three questions:

1. Is the underlying mathematical problem well-defined and interesting?
2. Is it hard on the generated-instance distribution, including against quantum algorithms?
3. Can a secure and practical KEM eventually be reduced to that problem?

A positive answer to one does **not** imply a positive answer to the others.

## Current status

**Stage: M1 attack experiment.**

Two deliberately attack-first models now exist:

- **M0:** exact simplicial-complex object model, canonical bytes, deterministic planted collapse relation, and trapdoor inversion. It is completely broken by A-000 direct public coordinate recovery.
- **M1:** replaces local coordinate markers with globally supported public transformations on one shared scaffold. It removes the exact A-000 leak but is broken by A-008 generic meet-in-the-middle recovery in about `2^(ell/2)` forward/reverse path states.

Current conclusions:

- local obscurity is not enough;
- global transformation support is not inversion asymmetry;
- a public low-branching path of efficiently invertible transformations is unsuitable;
- average-case hardness remains unknown;
- quantum hardness remains unknown;
- no KEM security proof exists;
- no production parameter set exists.

## Repository map

- `src/morph_kem/` — executable research objects and experiments
- `tests/` — correctness, rejection, collision, and attack tests
- `scripts/` — reproducible experiment entry points
- `docs/00-overview.md` — project scope and research rules
- `docs/01-mathematical-foundation.md` — mathematical objects and notation
- `docs/02-hard-problems.md` — HMCP / HMRP / HMCR
- `docs/03-construction.md` — provisional construction
- `docs/04-security-model.md` — target security notions and assumptions
- `docs/05-cryptanalysis.md` — attacks, failures, distinguishers, negative results
- `docs/06-quantum-analysis.md` — quantum threat analysis
- `docs/07-parameters.md` — experiment parameter tracking
- `docs/08-open-questions.md` — unresolved research questions
- `docs/09-toy-model.md` — exact M0 executable relation
- `docs/10-m1-path-experiment.md` — M1 non-local path model and MITM break
- `spec/morph-kem-v0.1.md` — evolving future specification draft
- `notes/research-log.md` — chronological research log

## Run experiments locally

No runtime dependencies outside the Python standard library are required.

~~~bash
PYTHONPATH=src python -m unittest discover -s tests -v

# M0
PYTHONPATH=src python scripts/exhaustive_baseline.py --params toy-8 --seed 0xA5

# M1
PYTHONPATH=src python scripts/mitm_baseline.py --params path-16 --seed 0xB6D3
PYTHONPATH=src python scripts/collision_scan.py --params path-12
~~~

## Research principles

- Do not invent new symmetric ciphers, hashes, PRNGs, or ad-hoc arithmetic primitives.
- Treat worst-case NP-hardness as insufficient for cryptographic hardness.
- Treat planted/generated-instance structure as adversarially visible.
- Record successful and failed attacks.
- Prefer falsifiable claims, explicit assumptions, reproducible experiments, and test vectors.
- Never describe the construction as secure merely because no attack is currently known.

## Planned phases

1. **M0:** executable toy relation and attack harness — complete; broken by A-000.
2. **M1:** non-local public branching-path experiment — implemented; broken by A-008 meet-in-the-middle recovery.
3. **M2:** introduce a genuinely asymmetric reduction/predecessor structure tied more directly to hidden discrete-Morse certificates.
4. Attack M2 with greedy reduction, canonicalization, SAT/MILP, treewidth, bidirectional search, statistical and learned distinguishers.
5. Only if a primitive survives: investigate reductions, quantum attacks, and larger parameters.
6. Only after substantial independent review: consider whether a KEM security claim is even plausible.

## Naming

MORPH-KEM is a working research name. The acronym currently refers to **Morse Obfuscated Reduction Path KEM**.

## Citation

Citation metadata is maintained in `CITATION.cff`. Stable archival releases may later be deposited in a DOI-issuing research archive.

## License

No license has been granted yet. Until a license is added, normal copyright law applies.
