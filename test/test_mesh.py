import unittest

from src.input_data import InputData
from src.mesh import Mesh


class TestInputData(unittest.TestCase):

    def test_constructor(self):
        input_dir = "test/test-inputs/input1.json"
        inp = InputData(input_dir)

        _ = Mesh(inp)

    def test_values(self):
        expected = {
            "n_points": 16,
            "n_cells": 15,
            "length": 15,
            "cells": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
            "gridpoints": [
                0.0,
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
                6.0,
                7.0,
                8.0,
                9.0,
                10.0,
                11.0,
                12.0,
                13.0,
                14.0,
                15.0,
            ],
            "h": [
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
            ],
            "mat_id": [0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4],
        }

        input_dir = "test/test-inputs/input1.json"
        inp = InputData(input_dir)

        m = Mesh(inp)

        for key, v in expected.items():
            self.assertEqual(getattr(m, key), v, key)
