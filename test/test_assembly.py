import unittest

from radiation.assembly_system import assemble_source
from radiation.input_data import InputData
from radiation.mesh import Mesh


class TestAssemblySystem(unittest.TestCase):

    def test_assembly_source(self):
        input_dir = "test/test-inputs/input2.json"

        inp = InputData(input_dir)
        m = Mesh(inp)

        bs = assemble_source(inp.boundary_values[0], 1, m, inp)

        print(bs)
