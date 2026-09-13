from __future__ import annotations

import hashlib
import unittest

from morph_kem.tdc_sparse_mixing import (
    TDC2EError,
    TDC2EParameters,
    TDC2E_PARAMETER_SETS,
    generate_tdc2e_instance,
    recover_tdc2e,
)


def seed_for(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class TDC2ESparseMixingTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(TDC2EError):
            TDC2EParameters("bad", "missing", 2).validate()
        with self.assertRaises(TDC2EError):
            TDC2EParameters("bad", "tdc2b-n8", 5).validate()
        with self.assertRaises(TDC2EError):
            generate_tdc2e_instance(TDC2E_PARAMETER_SETS["tdc2e-n8"], b"short")

    def test_generation_is_deterministic(self) -> None:
        params = TDC2E_PARAMETER_SETS["tdc2e-n8"]
        seed = seed_for("tdc2e-deterministic")
        self.assertEqual(
            generate_tdc2e_instance(params, seed),
            generate_tdc2e_instance(params, seed),
        )

    def test_every_public_column_is_nonzero_unique_and_mixing_budget_is_exact(self) -> None:
        for params in TDC2E_PARAMETER_SETS.values():
            instance = generate_tdc2e_instance(params, seed_for(params.name + "-shape"))
            for mixed in (instance.topology, instance.matched_random):
                code = mixed.code
                self.assertTrue(all(code.columns))
                self.assertEqual(len(set(code.columns)), len(code.columns))
                self.assertEqual(
                    len(mixed.reference.operations),
                    params.mixing_rounds * len(code.columns),
                )

    def test_invertible_mixing_preserves_rank_and_dimension_pairing(self) -> None:
        for params in TDC2E_PARAMETER_SETS.values():
            instance = generate_tdc2e_instance(params, seed_for(params.name + "-rank"))
            recovery = recover_tdc2e(instance)
            for result in (recovery.topology, recovery.matched_random):
                self.assertEqual(result.dimension, result.columns - result.rank)
                self.assertGreater(result.rank, 0)
                self.assertGreater(result.columns, result.rank)

    def test_public_metrics_need_no_mixing_history(self) -> None:
        params = TDC2E_PARAMETER_SETS["tdc2e-n8"]
        instance = generate_tdc2e_instance(params, seed_for("tdc2e-public"))
        recovery = recover_tdc2e(instance)
        self.assertGreaterEqual(recovery.topology.tanner_four_cycles, 0)
        self.assertGreaterEqual(recovery.topology.singleton_weight3_columns, 0)
        self.assertGreaterEqual(recovery.topology.pair_weight3_occurrences, 0)
        self.assertGreaterEqual(recovery.topology.distinct_pair_weight3_atoms, 0)

    def test_declared_small_sweep_runs(self) -> None:
        for params in TDC2E_PARAMETER_SETS.values():
            for index in range(3):
                instance = generate_tdc2e_instance(
                    params, seed_for(f"{params.name}-{index}")
                )
                recovery = recover_tdc2e(instance)
                self.assertEqual(
                    recovery.topology.successful_mixing_operations,
                    params.mixing_rounds * recovery.topology.columns,
                )
                self.assertEqual(
                    recovery.matched_random.successful_mixing_operations,
                    params.mixing_rounds * recovery.matched_random.columns,
                )


if __name__ == "__main__":
    unittest.main()
