#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter

from morph_kem.gluing import GluingPublicInstance, gluing_incidence
from morph_kem.gluing_cycle import recover_cycle_gluing_by_k4_exact_cover
from morph_kem.gluing_stellar import (
    G2_PARAMETER_SETS,
    _center_star_exact_covers,
    _enumerate_global_center_stars,
    generate_stellar_gluing_instance,
    recover_stellar_gluing_by_center_contraction,
    stellar_reference_partition_matches,
    validate_stellar_gluing_witness,
)


def _vertex_star_histogram(public: GluingPublicInstance) -> tuple[tuple[int, int], ...]:
    counts: Counter[int] = Counter()
    for tetrahedron in public.tetrahedra:
        for vertex in tetrahedron:
            counts[vertex] += 1
    return tuple(sorted(Counter(counts.values()).items()))


def _contracted_macro_incidence(public: GluingPublicInstance) -> tuple[int, int, int, int]:
    candidates = _enumerate_global_center_stars(public)
    covers, _, _ = _center_star_exact_covers(len(public.tetrahedra), candidates, 64)
    if not covers:
        return 0, 0, 0, 0
    macros = tuple(candidates[index].macro_tetrahedron for index in covers[0])
    macro_public = GluingPublicInstance(
        name=f"{public.name}-baseline-contracted",
        piece_count=public.piece_count,
        tetrahedra=macros,
    )
    incidence = gluing_incidence(macro_public)
    return incidence.vertices, incidence.edges, incidence.faces, incidence.tetrahedra


def main() -> int:
    parser = argparse.ArgumentParser(description="Run MORPH G2 stellar-contraction negative control.")
    parser.add_argument("--params", choices=sorted(G2_PARAMETER_SETS), default="g2-8")
    parser.add_argument(
        "--master-seed",
        default="76120450aabbccddeeff001122334455",
        help="hex deterministic generation seed",
    )
    parser.add_argument(
        "--old-a028",
        action="store_true",
        help="also run the old exhaustive G1 four-tetrahedron attack (best kept to g2-4)",
    )
    args = parser.parse_args()

    params = G2_PARAMETER_SETS[args.params]
    public, reference = generate_stellar_gluing_instance(params, bytes.fromhex(args.master_seed))
    incidence = gluing_incidence(public)
    recovery = recover_stellar_gluing_by_center_contraction(public)
    reference_validation = validate_stellar_gluing_witness(public, reference.groups)
    matches = stellar_reference_partition_matches(reference, recovery.groups)
    center_set = set(recovery.candidate_centers)
    reference_centers = set(reference.center_vertices)
    false_centers = len(center_set - reference_centers)
    missed_centers = len(reference_centers - center_set)
    macro_veft = _contracted_macro_incidence(public)

    print(f"parameters: {params.name}")
    print(f"pieces: {params.piece_count}")
    print(
        "public micro V/E/F/T: "
        f"{incidence.vertices}/{incidence.edges}/{incidence.faces}/{incidence.tetrahedra}"
    )
    print(f"Euler characteristic: {incidence.euler_characteristic}")
    print(f"boundary faces/max face incidence: {incidence.boundary_faces}/{incidence.max_face_incidence}")
    print(f"micro dual vertices/edges: {incidence.tetrahedra}/{recovery.micro_dual_edges}")
    print(f"micro dual bridges: {recovery.micro_bridge_count}")
    print(f"micro articulation points: {len(recovery.micro_articulation_points)}")
    print(f"micro two-vertex separator pairs: {recovery.micro_two_vertex_separator_pairs}")
    print(f"micro face occurrences: {recovery.micro_face_occurrences}")
    print(f"vertex-star histogram (tetrahedra per vertex -> vertices): {_vertex_star_histogram(public)}")
    print(f"candidate stellar centers: {recovery.center_star_candidates}")
    print(f"candidate-center false positives/misses: {false_centers}/{missed_centers}")
    print(
        "center exact-cover solutions/cap: "
        f"{recovery.center_cover_solutions}/{recovery.center_cover_solution_cap}"
    )
    print(f"center exact-cover cap hit: {recovery.center_cover_cap_hit}")
    print(f"center exact-cover nodes/backtracks: {recovery.center_cover_nodes}/{recovery.center_cover_backtracks}")
    print(f"reconstructed macro tetrahedra: {recovery.reconstructed_macro_tetrahedra}")
    print(f"contracted macro V/E/F/T: {macro_veft[0]}/{macro_veft[1]}/{macro_veft[2]}/{macro_veft[3]}")
    print(f"contracted macro dual edges: {recovery.macro_dual_edges}")
    print(f"macro K4 candidates: {recovery.macro_k4_candidates}")
    print(f"macro allowed-piece candidates: {recovery.macro_allowed_piece_candidates}")
    print(f"macro exact-cover solutions: {recovery.macro_cover_solutions}")
    print(f"macro exact-cover nodes/backtracks: {recovery.macro_cover_nodes}/{recovery.macro_cover_backtracks}")
    print(f"reference witness accepted: {reference_validation.valid}")
    print(f"A-029 public witness accepted: {recovery.validation.valid}")
    print(f"A-029 partition equals planted up to group order: {matches}")

    old_attack_ok = True
    if args.old_a028:
        old_attack = recover_cycle_gluing_by_k4_exact_cover(public)
        old_attack_ok = not old_attack.validation.valid
        print(f"old A-028 micro K4 candidates: {old_attack.dual_k4_candidates}")
        print(f"old A-028 allowed 4-tet candidates: {old_attack.allowed_piece_candidates}")
        print(f"old A-028 piece-level witness accepted: {old_attack.validation.valid}")

    return 0 if (
        reference_validation.valid
        and recovery.validation.valid
        and matches
        and center_set == reference_centers
        and recovery.micro_bridge_count == 0
        and not recovery.micro_articulation_points
        and old_attack_ok
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
