from __future__ import annotations

import argparse

from morph_kem.nat_tjoin import NAT1_PARAMETER_SETS, generate_nat1_instance, recover_nat1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(NAT1_PARAMETER_SETS), default="nat1-72")
    args = parser.parse_args()
    params = NAT1_PARAMETER_SETS[args.params]
    seed = b"MORPH-KEM NAT1 fixed baseline seed v1"
    print(f"parameters: {params.name}")
    for weight in params.noise_weights:
        public, reference = generate_nat1_instance(params, seed, weight)
        result = recover_nat1(public, reference=reference)
        print(
            "noise={weight} V/E/F={v}/{e}/{f} syndrome={syndrome} "
            "bfs={bfs} pops={pops} scans={scans} dp_states={states} pair_tests={tests} "
            "matching_distance={distance} recovered_weight={recovered} accepted={accepted} "
            "matches_noise={match_noise} matches_hidden={match_hidden} rejected_flips={rejected}".format(
                weight=weight,
                v=result.vertices,
                e=result.edges,
                f=result.triangles,
                syndrome=result.syndrome_weight,
                bfs=result.pair_metric_bfs_runs,
                pops=result.pair_metric_queue_pops,
                scans=result.pair_metric_edge_scans,
                states=result.matching_dp_states,
                tests=result.matching_pair_tests,
                distance=result.matching_distance,
                recovered=result.recovered_noise_weight,
                accepted=result.accepted,
                match_noise=result.matches_planted_noise_after_public_success,
                match_hidden=result.matches_hidden_vertex_after_public_success,
                rejected=reference.rejected_flip_proposals,
            )
        )


if __name__ == "__main__":
    main()
