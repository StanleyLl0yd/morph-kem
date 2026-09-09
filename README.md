# MORPH-KEM

**MORPH-KEM** is an exploratory post-quantum key-encapsulation research project based on hidden discrete Morse reductions and combinatorial topology.

> **Research only. Not for production use. Not a security claim.**
>
> MORPH-KEM is an unproven construction under active cryptanalysis. Do not use it to protect real data, credentials, communications, or systems.

## Research goal

Investigate whether a useful trapdoor primitive can be built around a hidden global reduction structure: reduction is efficient when a secret discrete-Morse certificate is known, while recovering the useful reduction structure from the public representation is conjectured to be hard.

The project deliberately separates three questions:

1. Is the underlying mathematical problem well-defined and interesting?
2. Is it hard on the generated-instance distribution, including against quantum algorithms?
3. Can a secure and practical KEM be reduced to that problem?

A positive answer to one does **not** imply a positive answer to the others.

## Current status

**Stage: M0 executable research harness.**

- mathematical direction: combinatorial topology + discrete Morse theory;
- provisional problem families: HMCP, HMRP, HMCR;
- canonical finite simplicial-complex representation implemented;
- deterministic toy forward/accept/trapdoor relation implemented;
- toy-8 exhaustive correctness baseline implemented;
- M0 is deliberately and completely broken by A-000 public recipe recovery;
- average-case hardness is unknown;
- quantum hardness is unknown;
- no KEM security proof exists;
- no production parameter set exists.

The deliberate M0 break is a research result: the next model must remove coordinate-local public leakage before any stronger claim is considered.

## Repository map

- src/morph_kem/ — executable research objects and toy relation
- tests/ — canonicalization, correctness, rejection, and attack tests
- scripts/ — reproducible experiment entry points
- docs/00-overview.md — project scope and research rules
- docs/01-mathematical-foundation.md — mathematical objects and notation
- docs/02-hard-problems.md — HMCP / HMRP / HMCR
- docs/03-construction.md — provisional construction
- docs/04-security-model.md — target security notions and assumptions
- docs/05-cryptanalysis.md — attacks, failures, distinguishers, negative results
- docs/06-quantum-analysis.md — quantum threat analysis
- docs/07-parameters.md — experiment parameter tracking
- docs/08-open-questions.md — unresolved research questions
- docs/09-toy-model.md — exact M0 executable relation
- spec/morph-kem-v0.1.md — evolving future specification draft
- notes/research-log.md — chronological research log

## Run M0 locally

No runtime dependencies outside the Python standard library are required.

~~~bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python scripts/exhaustive_baseline.py --params toy-8 --seed 0xA5
~~~

## Research principles

- Do not invent new symmetric ciphers, hashes, PRNGs, or ad-hoc arithmetic primitives.
- Treat worst-case NP-hardness as insufficient for cryptographic hardness.
- Treat planted/generated-instance structure as adversarially visible.
- Record successful and failed attacks.
- Prefer falsifiable claims, explicit assumptions, reproducible experiments, and test vectors.
- Never describe the construction as secure merely because no attack is currently known.

## Planned phases

1. **M0:** exact executable toy relation and attack harness — implemented; deliberately broken by A-000.
2. **M1:** overlapping/non-local public transformations and first nontrivial generated-instance distribution.
3. Implement greedy, canonicalization, SAT/MILP, treewidth, meet-in-the-middle, statistical, and learned distinguishers.
4. Measure leakage and structural recovery on generated instances.
5. Only if a primitive survives: investigate reductions and larger parameters.
6. Only after substantial independent review: consider whether a KEM security claim is even plausible.

## Naming

MORPH-KEM is a working research name. The acronym currently refers to **Morse Obfuscated Reduction Path KEM**.

## Citation

Citation metadata is maintained in CITATION.cff. Stable archival releases may later be deposited in a DOI-issuing research archive.

## License

No license has been granted yet. Until a license is added, normal copyright law applies.
