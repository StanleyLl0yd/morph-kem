import unittest

from morph_kem.path import (
    PATH_PARAMETER_SETS,
    PathParameters,
    exhaustive_path_recover,
    generate_path_instance,
    mitm_path_recover,
    path_forward,
    support_metrics,
)

MASTER_SEED = bytes.fromhex("102132435465768798a9bacbdcedfe0f")


class PathExperimentTests(unittest.TestCase):
    def test_generation_is_byte_deterministic(self) -> None:
        params = PATH_PARAMETER_SETS["path-12"]
        a = generate_path_instance(params, MASTER_SEED)
        b = generate_path_instance(params, MASTER_SEED)
        self.assertEqual(a.encode(), b.encode())

    def test_branch_support_is_global(self) -> None:
        params = PATH_PARAMETER_SETS["path-12"]
        instance = generate_path_instance(params, MASTER_SEED)
        metrics = support_metrics(instance)
        required = 15
        self.assertGreaterEqual(metrics.branch_min, required)
        self.assertGreaterEqual(metrics.relative_min, required)

    def test_small_instance_has_distinct_outputs(self) -> None:
        params = PathParameters("test-path-8", layers=8, vertices=16)
        instance = generate_path_instance(params, MASTER_SEED)
        outputs = {path_forward(instance, seed).encode() for seed in range(1 << 8)}
        self.assertEqual(len(outputs), 1 << 8)

    def test_exhaustive_recovers_small_path(self) -> None:
        params = PathParameters("test-path-8", layers=8, vertices=16)
        instance = generate_path_instance(params, MASTER_SEED)
        seed = 0b10110110
        target = path_forward(instance, seed)
        self.assertEqual(exhaustive_path_recover(instance, target), (seed,))

    def test_mitm_recovers_path16(self) -> None:
        params = PATH_PARAMETER_SETS["path-16"]
        instance = generate_path_instance(params, MASTER_SEED)
        seed = 0xB6D3
        target = path_forward(instance, seed)
        result = mitm_path_recover(instance, target)
        self.assertIn(seed, result.preimages)
        self.assertEqual(result.forward_states, 1 << 8)
        self.assertEqual(result.reverse_states, 1 << 8)
        self.assertLess(result.forward_states + result.reverse_states, 1 << 16)

    def test_reverse_branches_are_always_syntactically_valid(self) -> None:
        params = PATH_PARAMETER_SETS["path-12"]
        instance = generate_path_instance(params, MASTER_SEED)
        target = path_forward(instance, 0xA53)
        result = mitm_path_recover(instance, target, split_layer=6)
        self.assertIn(0xA53, result.preimages)
        self.assertEqual(result.reverse_states, 64)


if __name__ == "__main__":
    unittest.main()
