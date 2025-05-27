from src.mesh import Mesh
from src.input_data import InputData
from src.fixed_point import source_iteration

import matplotlib.pyplot as plt
import numpy as np
import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: solve_radiation_transport.py <json>")
        exit(1)

    input_dir = sys.argv[1]
    inp = InputData(input_dir)
    m = Mesh(inp)

    n_angles = 100
    start_phi = np.zeros(m.n_points)
    phi = source_iteration(start_phi, n_angles, m, inp, 0.0001, 1000)

    # print("Transport mat:", transport_mat.toarray(), sep="\n")
    # print("rhs:", b, sep="\n")

    plt.plot(m.gridpoints, phi, label = "FEM", color = "blue", alpha = 0.8, linewidth = 1)

    # we have an exact solution for the case of three zones,
    # mu = 1, and homogeneous boundary data
    # if (inp.n_zones == 3 and mu == 1 and inp.boundary_values[0] == 0):
        #plt.plot(m.gridpoints, [exact(x, inp) for x in m.gridpoints], label= "exact", color = "red", alpha = 0.8)

    plt.legend()
    plt.show()
