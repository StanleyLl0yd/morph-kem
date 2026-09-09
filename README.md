# MORPH-KEM

**MORPH-KEM** is an exploratory post-quantum public-key cryptography research project based on discrete Morse theory and combinatorial topology.

> **Research only. Not for production use. Not a security claim.**
>
> MORPH-KEM is an unproven research direction under active cryptanalysis. Do not use it to protect real data, credentials, communications, or systems.

## Research goal

Investigate whether a useful public-key trapdoor primitive can be built around a hidden global discrete-Morse structure while **any** equivalent public witness remains difficult to construct without the trapdoor.

The project separates mathematical search complexity, generated-distribution hardness, primitive security, and eventual KEM security.

A positive result at one layer does not imply the next.

## Current status

**Stage: M3 completed and rejected; no candidate primitive exists.**

Four attack-first models have been implemented and broken:

- **M0:** coordinate-local planted relation — broken by **A-000** direct public recovery.
- **M1:** globally supported reversible path — broken by **A-008** meet-in-the-middle recovery.
- **M2:** genuine collapse maze around a hidden 3-regular graph — broken by **A-014** structural core reconstruction.
- **M3:** exact equivalent-witness discrete-Morse relation on variable-degree graph-expanded complexes — broken by **A-016** free-collapse plus spanning-tree witness construction.

M3 is an important correction rather than a regression: the verifier now accepts **any** valid acyclic Hasse matching with the public critical vector. Once artificial planted-core privilege is removed, the graph-expanded family is plainly easy.

Fixed-seed M3 sweep:

~~~text
morse-6:  lex yes, reverse yes, random 32/32, generic greedy 8/8
morse-8:  lex yes, reverse yes, random 32/32, generic greedy 5/8
morse-10: lex yes, reverse yes, random 32/32, generic greedy 3/8
morse-12: lex yes, reverse yes, random 32/32, generic greedy 3/8
morse-16: lex yes, reverse yes, random 32/32, generic greedy 4/8
~~~

Current conclusions:

- secrecy of a planted path is irrelevant if another accepted witness is easy;
- equivalent-witness semantics are mandatory;
- a complex that publicly collapses to an easy graph class is unsuitable for this target relation;
- changing graph degree distribution does not solve that issue;
- generic greedy acyclic matching is already a meaningful baseline attack;
- average-case hardness remains unknown;
- quantum hardness remains unknown;
- no KEM security proof exists;
- no production parameter set exists.

## Repository map

- src/morph_kem/ — research constructions and attacks
- tests/ — correctness, validator, rejection, and attack tests
- scripts/ — deterministic baselines and scaling sweeps
- docs/02-hard-problems.md — provisional problem formulations including EMWP
- docs/04-security-model.md — equivalent-witness security discipline
- docs/05-cryptanalysis.md — attack ledger
- docs/07-parameters.md — experimental parameter/results tables
- docs/08-open-questions.md — current research questions
- docs/09-toy-model.md — M0
- docs/10-m1-path-experiment.md — M1
- docs/11-m2-collapse-maze.md — M2
- docs/12-m3-equivalent-witness.md — M3
- spec/morph-kem-v0.1.md — future-spec skeleton
- notes/research-log.md — chronological record

## Run experiments locally

No runtime dependencies outside the Python standard library are currently required.

~~~bash
PYTHONPATH=src python -m unittest discover -s tests -v

PYTHONPATH=src python scripts/exhaustive_baseline.py --params toy-8 --seed 0xA5
PYTHONPATH=src python scripts/mitm_baseline.py --params path-16 --seed 0xB6D3
PYTHONPATH=src python scripts/maze_baseline.py --params maze-6 --trials 16 --search-nodes 10000
PYTHONPATH=src python scripts/maze_core_sweep.py --max-nodes 2000000
PYTHONPATH=src python scripts/morse_baseline.py --params morse-6 --collapse-trials 16 --greedy-trials 4
PYTHONPATH=src python scripts/morse_sweep.py --collapse-trials 32 --greedy-trials 8
~~~

## Research principles

- Do not invent bespoke symmetric ciphers, hashes, PRNGs, or entropy sources.
- Worst-case NP-hardness is not evidence of average-case cryptographic hardness.
- Generated/planted distributions are part of the attack surface.
- Any equivalent accepted witness counts as attacker success.
- Preserve successful attacks and negative results.
- Prefer falsifiable claims and deterministic experiments.
- Never repair a structural break by parameter inflation.
- Never describe the construction as secure merely because no attack is currently known.

## Planned direction

1. **M0:** rejected by A-000.
2. **M1:** rejected by A-008.
3. **M2:** rejected by A-014.
4. **M3:** rejected by A-016; equivalent-witness relation retained as the correct discipline.
5. **Next:** test a genuinely 2-dimensional generated family whose useful witness does not reduce to a public graph/spanning-tree construction.
6. Add SAT/CSP, greedy matching, structural, canonicalization, and width attacks before scaling.
7. Only if a primitive survives: formulate quantum attacks and concrete parameters.
8. Only after independent review: consider whether a KEM construction is justified.

## Naming

MORPH-KEM is a working research name: **Morse Obfuscated Reduction Path KEM**.

## Citation

Citation metadata is maintained in CITATION.cff.

## License

No license has been granted yet. Until a license is added, normal copyright law applies.
