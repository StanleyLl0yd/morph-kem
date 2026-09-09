import unittest

from morph_kem import (
    TOY_PARAMETER_SETS,
    NoPreimageError,
    SimplicialComplex,
    accept,
    direct_public_recover,
    exhaustive_recover,
    forward,
    invert_with_trapdoor,
    keygen,
)

MASTER_SEED = bytes.fromhex("00112233445566778899aabbccddeeff")


class ToyRelationTests(unittest.TestCase):
    def test_keygen_is_byte_deterministic(self) -> None:
        params = TOY_PARAMETER_SETS["toy-8"]
        pk1, sk1 = keygen(params, MASTER_SEED)
        pk2, sk2 = keygen(params, MASTER_SEED)
        self.assertEqual(pk1.encode(), pk2.encode())
        self.assertEqual(sk1.encode(), sk2.encode())

    def test_different_master_seed_changes_key(self) -> None:
        params = TOY_PARAMETER_SETS["toy-8"]
        pk1, _ = keygen(params, MASTER_SEED)
        pk2, _ = keygen(params, b"different deterministic seed")
        self.assertNotEqual(pk1.encode(), pk2.encode())

    def test_all_toy8_seeds_round_trip(self) -> None:
        params = TOY_PARAMETER_SETS["toy-8"]
        pk, sk = keygen(params, MASTER_SEED)
        seen = set()
        for seed in range(1 << params.seed_bits):
            ct = forward(pk, seed)
            encoded = ct.encode()
            self.assertNotIn(encoded, seen)
            seen.add(encoded)
            self.assertTrue(accept(pk, seed, ct))
            self.assertEqual(invert_with_trapdoor(pk, sk, ct), seed)
            self.assertEqual(direct_public_recover(pk, ct), seed)

    def test_exhaustive_recovery_toy8(self) -> None:
        params = TOY_PARAMETER_SETS["toy-8"]
        pk, _ = keygen(params, MASTER_SEED)
        seed = 0b10110110
        ct = forward(pk, seed)
        self.assertEqual(exhaustive_recover(pk, ct), seed)

    def test_ciphertext_is_canonical_bytes(self) -> None:
        params = TOY_PARAMETER_SETS["toy-8"]
        pk, _ = keygen(params, MASTER_SEED)
        ct = forward(pk, 173)
        self.assertEqual(SimplicialComplex.decode(ct.encode()), ct)

    def test_trapdoor_rejects_extra_foreign_vertex(self) -> None:
        params = TOY_PARAMETER_SETS["toy-8"]
        pk, sk = keygen(params, MASTER_SEED)
        ct = forward(pk, 13).add_facets([(999, 1000)])
        with self.assertRaises(NoPreimageError):
            invert_with_trapdoor(pk, sk, ct)

    def test_trapdoor_is_bound_to_public_key(self) -> None:
        params = TOY_PARAMETER_SETS["toy-8"]
        pk1, _ = keygen(params, MASTER_SEED)
        _, sk2 = keygen(params, b"other")
        with self.assertRaises(ValueError):
            invert_with_trapdoor(pk1, sk2, forward(pk1, 1))

    def test_malformed_coordinate_is_rejected(self) -> None:
        params = TOY_PARAMETER_SETS["toy-8"]
        pk, sk = keygen(params, MASTER_SEED)
        ct = forward(pk, 0)
        malformed = ct.add_facets([pk.choices[0][1]])
        with self.assertRaises(NoPreimageError):
            invert_with_trapdoor(pk, sk, malformed)
        with self.assertRaises(NoPreimageError):
            direct_public_recover(pk, malformed)


if __name__ == "__main__":
    unittest.main()
