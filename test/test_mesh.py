import unittest

from radiation.input_data import InputData
from radiation.mesh import Mesh


class TestInputData(unittest.TestCase):

    def test_constructor(self):
        input_dir = "test/test-inputs/input1.json"
        inp = InputData(input_dir)

        _ = Mesh(inp)
