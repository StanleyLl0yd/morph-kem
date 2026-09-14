from __future__ import annotations

import hashlib
import unittest

from morph_kem.tdc_decoder_work import planted_error_mask, syndrome
from morph_kem.tdc_lee_brickell import (
    TDC3CError,
    TDC3CParameters,
    TDC3C_PARAMETER_SETS,
    build_basis_coordinate_map,
    generate_tdc3c_instance,
    lee_brickell_decode,
    recover_tdc3c_weight,
    solve_with_basis_map,
)
from morph_kem.tdc_prange_isd import information_set


def digest(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class TDC3CLeeBrickellTests(unittest.TestCase):
    def test_parameter_grid_is_fixed(self) -> None:
        self.assertEqual(set(TDC3C_PARAMETER_SETS), {"tdc3c-n8", "tdc3c-n9", "tdc3c-n10"})
        with self.assertRaises(TDC3CError):
            TDC3CParameters("bad", "tdc3-n8", (2, 4, 8)).validate()
        with self.assertRaises(TDC3CError):
            TDC3CParameters("bad", "tdc3-n8", (1, 4, 16), (0, 1)).validate()
        with self.assertRaises(TDC3CError):
            TDC3CParameters("bad", "missing").validate()

    def test_basis_coordinate_map_solves_public_syndromes(self) -> None:
        params = TDC3C_PARAMETER_SETS["tdc3c-n8"]
        instance = generate_tdc3c_instance(params, digest("TDC3c basis map unit v1"))
        code = instance.pair.topology
        planted = planted_error_mask(instance, 3)
        target = syndrome(code, planted)

        basis = None
        selected = None
        for trial in range(64):
            candidate = information_set(code, target, trial)
            mapped = build_basis_coordinate_map(code, candidate)
            if mapped.full_rank:
                selected = candidate
                basis = mapped
                break
        self.assertIsNotNone(selected)
        self.assertIsNotNone(basis)
        assert selected is not None and basis is not None

        local = solve_with_basis_map(basis.inverse_rows, target)
        expanded = 0
        for local_index, column_index in enumerate(selected):
            if (local >> local_index) & 1:
                expanded |= 1 << column_index
        self.assertEqual(syndrome(code, expanded), target)

        for row_index in range(code.row_count):
            unit = 1 << row_index
            local_unit = solve_with_basis_map(basis.inverse_rows, unit)
            expanded_unit = 0
            for local_index, column_index in enumerate(selected):
                if (local_unit >> local_index) & 1:
                    expanded_unit |= 1 << column_index
            self.assertEqual(syndrome(code, expanded_unit), unit)

    def test_success_grid_is_monotone_in_order_and_budget(self) -> None:
        params = TDC3C_PARAMETER_SETS["tdc3c-n9"]
        instance = generate_tdc3c_instance(params, digest("TDC3c monotone grid unit v1"))
        planted = planted_error_mask(instance, 4)
        code = instance.pair.topology
        target = syndrome(code, planted)
        result = lee_brickell_decode(code, target, 4)
        grid = {(order, budget): ok for order, budget, ok in result.success_grid}
        for order in (0, 1, 2):
            self.assertLessEqual(int(grid[(order, 1)]), int(grid[(order, 4)]))
            self.assertLessEqual(int(grid[(order, 4)]), int(grid[(order, 16)]))
        for budget in (1, 4, 16):
            self.assertLessEqual(int(grid[(0, budget)]), int(grid[(1, budget)]))
            self.assertLessEqual(int(grid[(1, budget)]), int(grid[(2, budget)]))
        self.assertEqual(tuple(cp.budget for cp in result.work_by_budget), (1, 4, 16))

    def test_public_recovery_verifies_when_accepted(self) -> None:
        params = TDC3C_PARAMETER_SETS["tdc3c-n10"]
        instance = generate_tdc3c_instance(params, digest("TDC3c public recovery unit v1"))
        planted = planted_error_mask(instance, 5)
        code = instance.pair.topology
        target = syndrome(code, planted)
        result = lee_brickell_decode(code, target, 5)
        if result.accepted:
            self.assertEqual(syndrome(code, result.recovered_error_mask), target)
            self.assertLessEqual(result.recovered_weight, 5)
            self.assertIsNotNone(result.first_success_trial)
            self.assertIsNotNone(result.first_success_outside_order)
            self.assertIsNotNone(result.first_success_work)

    def test_pair_recovery_uses_planted_only_for_public_targets_and_post_metric(self) -> None:
        params = TDC3C_PARAMETER_SETS["tdc3c-n8"]
        instance = generate_tdc3c_instance(params, digest("TDC3c pair recovery unit v1"))
        result = recover_tdc3c_weight(instance, 2)
        self.assertEqual(result.planted_weight, 2)
        for recovery, code in (
            (result.topology, instance.pair.topology),
            (result.matched_random, instance.pair.matched_random),
        ):
            if recovery.accepted:
                planted = planted_error_mask(instance, 2)
                target = syndrome(code, planted)
                self.assertEqual(syndrome(code, recovery.recovered_error_mask), target)
                self.assertLessEqual(recovery.recovered_weight, 2)


if __name__ == "__main__":
    unittest.main()
