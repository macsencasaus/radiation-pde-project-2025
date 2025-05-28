import unittest

from src.input_data import InputData
from src.mesh import Mesh
from src.poisson import fish
import numpy as np
import matplotlib.pyplot as plt
import sys
import copy

class TestPoisson(unittest.TestCase):

    def test_poisson(self):
        input_dir = "test/test-inputs/input_test_fish2.json"
        inp = InputData(input_dir)
        m = Mesh(inp)

        sig_a = [inp.sigma_t[m.mat_id[cell]] - inp.sigma_s[m.mat_id[cell]] for cell in m.cells]
        sig_s = [inp.sigma_s[m.mat_id[cell]] for cell in m.cells]
        forcing = [inp.source[m.mat_id[cell]] for cell in m.cells]
        alpha = inp.boundary_values[0]
        beta = inp.boundary_values[1]

        solution = fish(m, sig_s, sig_a, forcing, alpha, beta)

        alpha=1/inp.sigma_s[1]
        c1 = -1/4/alpha + 1/alpha - 1/2/(alpha+1)
        exact = lambda x : -0.5*x**2 + 0.25*(3+alpha)/(1+alpha)*x  if x <0.5 else -(x**2)/2/alpha + c1*x + (0.5/alpha - c1)

        exact_solution = [exact(x) for x in m.gridpoints]
        plt.plot(m.gridpoints, exact_solution, label = "exact", color = "green", alpha = 0.8, linewidth = 1)
        plt.plot(m.gridpoints, solution, label = "fish", color = "blue", alpha = 0.8, linewidth = 1)
        plt.legend()
        plt.show()

        #np.testing.assert_array_almost_equal(solution, exact_solution)
