import unittest

from radiation.input_data import InputData


class TestInputData(unittest.TestCase):

    def test_constructor(self):
        input_dir = "test/test-inputs/input1.json"
        _ = InputData(input_dir)
