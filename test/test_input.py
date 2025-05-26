import unittest

from radiation.input_data import InputData


class TestInputData(unittest.TestCase):

    def test_constructor(self):
        input_dir = "test/test-inputs/input1.json"
        _ = InputData(input_dir)

    def test_values(self):
        expected = {
            "n_zones": 5,
            "n_cells": [1, 2, 3, 4, 5],
            "zone_length": [1, 2, 3, 4, 5],
            "sigma_t": [3, 4, 5, 6, 7],
            "source": [9, 8, 7, 6, 5],
            "boundary_values": (1, 2),
        }

        input_dir = "test/test-inputs/input1.json"
        inp = InputData(input_dir)

        for key, v in expected.items():
            self.assertEqual(getattr(inp, key), v, key)
