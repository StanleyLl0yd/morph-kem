from __future__ import annotations

import argparse

from morph_kem.nat_s3 import NAT2_PARAMETER_SETS, generate_nat2_instance, recover_nat2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(NAT2_PARAMETER_SETS), default="nat2-F36")
    args = parser.parse_args()
    params = NAT2_PARAMETER_SETS[args.params]
    seed = b"MORPH-KEM NAT2 fixed baseline seed v1"
    print(f"parameters: {params.name}")
    for weight in params.noise_weights:
        public, reference = generate_nat2_instance(params, seed, weight)
        result = recover_nat2(public, reference=reference)
        print(
            "noise={weight} V/E/F={v}/{e}/{f} sign_syndrome={syndrome} sign_tjoin={tjoin} "
            "sign_dp={dp} sign_pairs={pairs} sign_noise_match={sign_noise} sign_hidden_match={sign_hidden} "
            "csp_nodes={nodes} csp_backtracks={backtracks} accepted_states={accepted}/{cap} cap_hit={cap_hit} "
            "first_accepted={first} first_hidden_match={hidden} first_noise_edges={noise_edges} rejected_flips={rejected}".format(
                weight=weight,
                v=result.vertices,
                e=result.edges,
                f=result.triangles,
                syndrome=result.sign_syndrome_weight,
                tjoin=result.sign_tjoin_weight,
                dp=result.sign_tjoin_dp_states,
                pairs=result.sign_tjoin_pair_tests,
                sign_noise=result.sign_matches_planted_noise_after_public_success,
                sign_hidden=result.sign_matches_hidden_vertex_parity_after_public_success,
                nodes=result.csp_nodes,
                backtracks=result.csp_backtracks,
                accepted=result.accepted_states,
                cap=result.accepted_state_cap,
                cap_hit=result.accepted_state_cap_hit,
                first=result.first_state_accepted,
                hidden=result.first_state_matches_hidden_after_public_success,
                noise_edges=result.first_state_noise_edges,
                rejected=reference.rejected_flip_proposals,
            )
        )


if __name__ == "__main__":
    main()
