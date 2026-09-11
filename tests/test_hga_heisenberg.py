from __future__ import annotations

import unittest

from morph_kem.hga_actions import HGAError
from morph_kem.hga_heisenberg import (
    HGA1_PARAMETER_SETS,
    HGA1Parameters,
    apply_word,
    generate_hga1_instance,
    invert_word,
    recover_hga1,
)


MASTER_SEED = bytes.fromhex("99887766554433221100ffeeddccbbaa")


class HGA1HeisenbergTests(unittest.TestCase):
    def test_public_mitm_recovers_equivalent_connector(self) -> None:
        for name, params in HGA1_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_hga1_instance(params, MASTER_SEED)
                recovery = recover_hga1(public, reference=reference)
                self.assertTrue(recovery.accepted)
                self.assertLessEqual(recovery.recovered_length, params.secret_word_length)
                self.assertGreater(recovery.forward_states, 0)
                self.assertGreater(recovery.backward_states, 0)
                self.assertGreater(recovery.meet_states, 0)
                self.assertEqual(
                    apply_word(public.source, recovery.recovered_word, params.prime),
                    public.target,
                )

    def test_public_abelianized_orbit_is_small_sl2_orbit(self) -> None:
        for name, params in HGA1_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, _ = generate_hga1_instance(params, MASTER_SEED)
                recovery = recover_hga1(public)
                self.assertEqual(
                    recovery.quotient_orbit_size,
                    params.prime * (params.prime * params.prime - 1),
                )
                self.assertLessEqual(
                    recovery.quotient_shortest_length,
                    params.secret_word_length,
                )

    def test_recovered_connector_inverse_round_trip(self) -> None:
        params = HGA1_PARAMETER_SETS["hga1-p7"]
        public, _ = generate_hga1_instance(params, MASTER_SEED)
        recovery = recover_hga1(public)
        self.assertEqual(
            apply_word(public.target, invert_word(recovery.recovered_word), params.prime),
            public.source,
        )

    def test_break_is_stable_across_seeds(self) -> None:
        params = HGA1_PARAMETER_SETS["hga1-p11"]
        for seed_index in range(8):
            with self.subTest(seed=seed_index):
                seed = bytes([seed_index + 1]) * 32
                public, reference = generate_hga1_instance(params, seed)
                recovery = recover_hga1(public, reference=reference)
                self.assertTrue(recovery.accepted)
                self.assertLessEqual(recovery.recovered_length, params.secret_word_length)

    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(HGAError):
            HGA1Parameters("bad-prime", 13, 8).validate()
        with self.assertRaises(HGAError):
            HGA1Parameters("short", 5, 3).validate()
        with self.assertRaises(HGAError):
            generate_hga1_instance(HGA1_PARAMETER_SETS["hga1-p5"], b"short")


if __name__ == "__main__":
    unittest.main()
