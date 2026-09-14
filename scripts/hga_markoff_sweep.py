from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict

from morph_kem.hga_markoff_action import (
    HGA1_PARAMETER_SETS,
    generate_hga1_instance,
    recover_hga1,
)


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM HGA-R1 sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    parser.add_argument("--params", choices=sorted(HGA1_PARAMETER_SETS), default=None)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 32:
        raise SystemExit("--seeds must be in 1..32")

    params_list = (
        (HGA1_PARAMETER_SETS[args.params],)
        if args.params is not None
        else tuple(HGA1_PARAMETER_SETS[name] for name in sorted(HGA1_PARAMETER_SETS))
    )

    print(
        "set,seed,points,orbit,retries,bfs_ok,bfs_len,bfs_discovered,bfs_expanded,bfs_edges,"
        "bfs_planted,bidir_ok,bidir_len,bidir_discovered,bidir_expanded,bidir_edges,bidir_planted,"
        "transporter,stabilizer"
    )

    summary: dict[str, dict[str, int]] = defaultdict(lambda: {
        "cases": 0,
        "bfs_ok": 0,
        "bidir_ok": 0,
        "bfs_planted": 0,
        "bidir_planted": 0,
        "min_shortest": 10**9,
        "max_shortest": 0,
        "min_orbit": 10**9,
        "max_orbit": 0,
        "max_bfs_discovered": 0,
        "max_bidir_discovered": 0,
        "max_bfs_edges": 0,
        "max_bidir_edges": 0,
        "min_transporter": 10**30,
        "max_transporter": 0,
        "min_stabilizer": 10**30,
        "max_stabilizer": 0,
    })

    for params in params_list:
        for index in range(args.seeds):
            instance = generate_hga1_instance(params, seed_for(params.name, index))
            result = recover_hga1(instance)
            print(
                f"{params.name},{index},{instance.markoff_point_count},{result.orbit_size},"
                f"{instance.generation_retries},{int(result.bfs.accepted)},{result.bfs.recovered_length},"
                f"{result.bfs.states_discovered},{result.bfs.states_expanded},{result.bfs.edge_scans},"
                f"{int(result.bfs_equals_planted_after_public_success)},"
                f"{int(result.bidirectional.accepted)},{result.bidirectional.recovered_length},"
                f"{result.bidirectional.states_discovered},{result.bidirectional.states_expanded},"
                f"{result.bidirectional.edge_scans},"
                f"{int(result.bidirectional_equals_planted_after_public_success)},"
                f"{result.multiplicity.transporter_reduced_words_leq_bound},"
                f"{result.multiplicity.stabilizer_nonempty_reduced_words_leq_bound}"
            )

            row = summary[params.name]
            row["cases"] += 1
            row["bfs_ok"] += int(result.bfs.accepted)
            row["bidir_ok"] += int(result.bidirectional.accepted)
            row["bfs_planted"] += int(result.bfs_equals_planted_after_public_success)
            row["bidir_planted"] += int(result.bidirectional_equals_planted_after_public_success)
            if result.bfs.accepted:
                row["min_shortest"] = min(row["min_shortest"], result.bfs.recovered_length)
                row["max_shortest"] = max(row["max_shortest"], result.bfs.recovered_length)
            row["min_orbit"] = min(row["min_orbit"], result.orbit_size)
            row["max_orbit"] = max(row["max_orbit"], result.orbit_size)
            row["max_bfs_discovered"] = max(row["max_bfs_discovered"], result.bfs.states_discovered)
            row["max_bidir_discovered"] = max(row["max_bidir_discovered"], result.bidirectional.states_discovered)
            row["max_bfs_edges"] = max(row["max_bfs_edges"], result.bfs.edge_scans)
            row["max_bidir_edges"] = max(row["max_bidir_edges"], result.bidirectional.edge_scans)
            transporter = result.multiplicity.transporter_reduced_words_leq_bound
            stabilizer = result.multiplicity.stabilizer_nonempty_reduced_words_leq_bound
            row["min_transporter"] = min(row["min_transporter"], transporter)
            row["max_transporter"] = max(row["max_transporter"], transporter)
            row["min_stabilizer"] = min(row["min_stabilizer"], stabilizer)
            row["max_stabilizer"] = max(row["max_stabilizer"], stabilizer)

    print(
        "summary,set,cases,bfs_ok,bidir_ok,bfs_planted,bidir_planted,min_shortest,max_shortest,"
        "min_orbit,max_orbit,max_bfs_discovered,max_bidir_discovered,max_bfs_edges,max_bidir_edges,"
        "min_transporter,max_transporter,min_stabilizer,max_stabilizer"
    )
    for name in sorted(summary):
        row = summary[name]
        print(
            f"summary,{name},{row['cases']},{row['bfs_ok']},{row['bidir_ok']},"
            f"{row['bfs_planted']},{row['bidir_planted']},{row['min_shortest']},{row['max_shortest']},"
            f"{row['min_orbit']},{row['max_orbit']},{row['max_bfs_discovered']},"
            f"{row['max_bidir_discovered']},{row['max_bfs_edges']},{row['max_bidir_edges']},"
            f"{row['min_transporter']},{row['max_transporter']},"
            f"{row['min_stabilizer']},{row['max_stabilizer']}"
        )


if __name__ == "__main__":
    main()
