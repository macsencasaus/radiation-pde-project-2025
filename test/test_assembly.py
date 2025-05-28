import unittest

import numpy as np

from scipy.sparse import csr_matrix

from src.assemble_system import assemble_source, generate_sparsity_pattern, assemble_transport_matrix
from src.input_data import InputData
from src.mesh import Mesh


class TestAssembleSystem(unittest.TestCase):

    def test_assemble_source(self):
        input_dir = "test/test-inputs/input2.json"

        inp = InputData(input_dir)
        m = Mesh(inp)

        bs = assemble_source(1, m, inp)

        print(bs)

    def test_generate_sparce(self):
        input_dir = "test/test-inputs/input2.json"

        inp = InputData(input_dir)
        m = Mesh(inp)

        rows, cols = generate_sparsity_pattern(m)

        data = np.ones(3 * m.n_points - 2)

        sparse_mat = csr_matrix((data, (rows, cols)), shape=(m.n_points, m.n_points))

        print(sparse_mat.toarray())

    def test_assemble_matrix(self):
        input_dir = "test/test-inputs/input2.json"

        inp = InputData(input_dir)
        m = Mesh(inp)

        matrix = assemble_transport_matrix(1, m, inp)
        print(matrix.toarray())
