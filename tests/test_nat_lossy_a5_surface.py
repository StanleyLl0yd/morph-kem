from __future__ import annotations

import hashlib
import unittest

from morph_kem.nat_lossy_a5_surface import (
    NAT9Error,
    NAT9Parameters,
    NAT9_PARAMETER_SETS,
    generate_nat9_instance,
    recover_nat9,
    validate_nat9_representation,
)


def digest(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class NAT9LossyA5SurfaceTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(NAT9Error):
            NAT9Parameters("bad", ("zz",)).validate()
        with self.assertRaises(NAT9Error):
            generate_nat9_instance(NAT9_PARAMETER_SETS["nat9-C4"], b"short")

    def test_generation_is_deterministic_and_reference_verifies(self) -> None:
        params = NAT9_PARAMETER_SETS["nat9-X4"]
        seed = digest("NAT9 deterministic unit v1")
        first_public, first_reference = generate_nat9_instance(params, seed)
        second_public, second_reference = generate_nat9_instance(params, seed)
        self.assertEqual(first_public, second_public)
        self.assertEqual(first_reference, second_reference)
        self.assertTrue(
            validate_nat9_representation(first_public, first_reference.planted_generators)
        )

    def test_public_csp_recovers_without_reference(self) -> None:
        for name, params in NAT9_PARAMETER_SETS.items():
            public, reference = generate_nat9_instance(
                params, digest(f"NAT9 public CSP unit {name} v1")
            )
            recovery = recover_nat9(public)
            self.assertTrue(recovery.accepted)
            self.assertIsNotNone(recovery.recovered_generators)
            self.assertGreater(recovery.accepted_representations, 0)
            assert recovery.recovered_generators is not None
            self.assertTrue(
                validate_nat9_representation(public, recovery.recovered_generators)
            )
            with_reference = recover_nat9(public, reference=reference)
            self.assertEqual(recovery.recovered_generators, with_reference.recovered_generators)

    def test_small_declared_sweep_recovers(self) -> None:
        for name, params in NAT9_PARAMETER_SETS.items():
            for index in range(3):
                public, _ = generate_nat9_instance(
                    params, digest(f"NAT9 sweep unit {name} {index} v1")
                )
                recovery = recover_nat9(public)
                self.assertTrue(recovery.accepted)
                self.assertGreater(recovery.relator_join_candidates, 0)


if __name__ == "__main__":
    unittest.main()
