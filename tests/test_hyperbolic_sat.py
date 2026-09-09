import unittest

from morph_kem.hyperbolic import generate_a5_instance, validate_a5_frames
from morph_kem.hyperbolic_sat import (
    decode_a5_sat_model,
    encode_a5_sat,
    frames_to_sat_literals,
    gauge_fix_a5_frames,
    sat_encoding_accepts_frames,
)

MASTER_SEED = bytes.fromhex("26457513110645905905016157536392")


class HyperbolicSatTests(unittest.TestCase):
    def test_exact_cnf_shape(self) -> None:
        public, _ = generate_a5_instance(MASTER_SEED)
        encoding = encode_a5_sat(public)
        self.assertEqual(encoding.variable_count, 24 * 60)
        self.assertEqual(len(encoding.clauses), 47_545)
        self.assertTrue(encoding.to_dimacs().startswith("p cnf 1440 47545\n"))

    def test_gauge_fixed_reference_satisfies_cnf(self) -> None:
        public, reference = generate_a5_instance(MASTER_SEED)
        frames = gauge_fix_a5_frames(reference.frames)
        self.assertTrue(validate_a5_frames(public, frames).accepted)

        encoding = encode_a5_sat(public)
        self.assertTrue(sat_encoding_accepts_frames(encoding, frames))

        model = decode_a5_sat_model(
            public,
            encoding,
            frames_to_sat_literals(encoding, frames),
        )
        self.assertTrue(model.accepted)
        self.assertEqual(model.frames, frames)


if __name__ == "__main__":
    unittest.main()
