from __future__ import annotations

import argparse
import hashlib

from morph_kem.hga_markoff_action import (
    HGA1_PARAMETER_SETS,
    generate_hga1_instance,
    recover_hga1,
)


def seed_for(name: str) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM HGA1 baseline {name} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--params",
        choices=sorted(HGA1_PARAMETER_SETS),
        default="hga1-p59-L24",
    )
    args = parser.parse_args()

    params = HGA1_PARAMETER_SETS[args.params]
    instance = generate_hga1_instance(params, seed_for(params.name))
    result = recover_hga1(instance)

    print(f"parameters: {params.name}")
    print(f"prime / word bound: {params.prime}/{params.word_bound}")
    print(f"Markoff point count: {instance.markoff_point_count}")
    print(f"generation retries: {instance.generation_retries}")
    print(f"source: {instance.source}")
    print(f"target: {instance.target}")
    print(f"public orbit size / edge scans: {result.orbit_size}/{result.orbit_edge_scans}")
    print(
        "BFS: "
        f"accepted={result.bfs.accepted} length={result.bfs.recovered_length} "
        f"discovered={result.bfs.states_discovered} expanded={result.bfs.states_expanded} "
        f"edge_scans={result.bfs.edge_scans} planted_match={result.bfs_equals_planted_after_public_success}"
    )
    print(
        "bidirectional: "
        f"accepted={result.bidirectional.accepted} length={result.bidirectional.recovered_length} "
        f"discovered={result.bidirectional.states_discovered} expanded={result.bidirectional.states_expanded} "
        f"edge_scans={result.bidirectional.edge_scans} "
        f"planted_match={result.bidirectional_equals_planted_after_public_success}"
    )
    print(
        "reduced-word multiplicity <= bound: "
        f"transporter={result.multiplicity.transporter_reduced_words_leq_bound} "
        f"stabilizer_nonempty={result.multiplicity.stabilizer_nonempty_reduced_words_leq_bound}"
    )


if __name__ == "__main__":
    main()
