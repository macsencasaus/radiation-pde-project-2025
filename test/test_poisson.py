import unittest

from src.input_data import InputData
from src.mesh import Mesh
from src.poisson import fish
import numpy as np
import matplotlib.pyplot as plt
import sys
import copy


def exact_fish(mesh: Mesh, inputs: InputData):
    import math 
    x0 = 0.
    x1 = 0.5
    q1 = inputs.source[0]
    s1 = inputs.sigma_t[0]
    q2 = inputs.source[1]
    s2 = inputs.sigma_t[1]
    a = -(3*q1*s1*s1+6*q1*s1*s2+3*q2*s1*s2)/(4*(s1+s2))
    b =  (3*q1*s1*s2+6*q2*s1*s2+3*q2*s2*s2)/(4*(s1+s2))
    s = np.zeros(mesh.n_points)
    i0 = 0
    n = 0
    s[0] = 0.
    for l in range(0, inputs.n_cells[n]): ###zone 0
        i = i0+l+1
        s[i] = -(3 * s1 * q1 * mesh.gridpoints[i] ** 2 / 2 + a * mesh.gridpoints[i])
       
    i0 = i0 + inputs.n_cells[n]
    n = 1
    for l in range(0,inputs.n_cells[n]): ###zone 1
        i = i0+l+1
        s[i] = -(3*s2*q2*(mesh.gridpoints[i]-1)**2/2 + b*(mesh.gridpoints[i]-1))
            
    return s

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

        # exact_solution = [exact_sol(x) for x in m.gridpoints]
        # plt.plot(m.gridpoints, exact_fish(m, inp), label = "exact", color = "green", alpha = 0.8, linewidth = 1)
        # plt.plot(m.gridpoints, solution, label = "fish", color = "blue", alpha = 0.8, linewidth = 1)
        # plt.legend()
        # plt.show()

        np.testing.assert_array_almost_equal(solution, exact_fish(m, inp))
