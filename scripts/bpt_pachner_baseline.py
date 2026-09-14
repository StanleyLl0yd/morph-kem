from __future__ import annotations

import argparse
import hashlib

from morph_kem.bpt_pachner import BPT_WEAK_PARAMETER_SETS, generate_bpt_weak_instance, recover_bpt_weak


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(BPT_WEAK_PARAMETER_SETS), default="bptw0-d3")
    args = parser.parse_args()
    params = BPT_WEAK_PARAMETER_SETS[args.params]
    seed = hashlib.sha256(f"MORPH-KEM BPT-W0 fixed {params.name} v1".encode()).digest()
    public, reference = generate_bpt_weak_instance(params, seed)
    result = recover_bpt_weak(public, reference=reference)
    print(f"parameters: {params.name}")
    print(f"source/target vertices: {len(public.source.vertices)}/{len(public.target.vertices)}")
    print(f"source/target tetrahedra: {len(public.source.facets)}/{len(public.target.facets)}")
    print(f"move bound / recovered: {public.move_bound}/{result.recovered_length}")
    print(f"source/target simplify steps: {result.source_simplification_steps}/{result.target_simplification_steps}")
    print(f"vertex scans: {result.source_vertex_scans + result.target_vertex_scans}")
    print(f"legal moves seen: {result.source_legal_moves_seen + result.target_legal_moves_seen}")
    print(f"simplification path counts: {result.source_simplification_paths}/{result.target_simplification_paths}")
    print(f"accepted path multiplicity lower bound: {result.accepted_path_multiplicity_lower_bound}")
    print(f"accepted: {result.accepted}")
    print(f"matches planted after public success: {result.matches_planted_after_public_success}")


if __name__ == "__main__":
    main()
