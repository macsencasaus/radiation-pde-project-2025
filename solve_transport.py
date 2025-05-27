from src.mesh import Mesh
from src.input_data import InputData
from src.assemble_system import assemble_transport_matrix, assemble_source
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt
import numpy as np
import sys

def exact(x: float, data: InputData) -> float:
    zone_lengths = data.zone_length
    sigma_t = data.sigma_t
    source = data.source
    x0 = 0
    x1 = zone_lengths[0]
    x2 = zone_lengths[0] + zone_lengths[1]

    s1, s2, s3 = sigma_t
    q1, q2, q3 = source

    u1 = q1 / s1 * (1 - np.exp(s1 * (x0 - x)))
    u2 = u1 * np.exp(s2 *(x1 - x2))
    
    if x0 <= x and x <= x1:
        return q1 / s1 * (1 - np.exp(s1 * (x0-x)))
    elif x1 < x and x <= x2:
        return u1 * np.exp(s2 * (x1 - x))
    else:
        return u2 * np.exp(s3 * (x2 - x)) + q3 / s3 * (1 - np.exp(s3 * (x2 - x)))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: solve_transport.py <json>")
        exit(1)

    input_dir = sys.argv[1]
    inp = InputData(input_dir)
    m = Mesh(inp)

    mu = 1

    transport_mat = assemble_transport_matrix(mu, m, inp)
    b = assemble_source(mu, m, inp)

    u = spsolve(transport_mat, b, permc_spec=None, use_umfpack=True)

    # print("Transport mat:", transport_mat.toarray(), sep="\n")
    # print("rhs:", b, sep="\n")

    plt.plot(m.gridpoints, u, label = "FEM", color = "blue", alpha = 0.8, linewidth = 1)

    # we have an exact solution for the case of three zones,
    # mu = 1, and homogeneous boundary data 
    if (inp.n_zones == 3 and mu == 1 and inp.boundary_values[0] == 0):
        plt.plot(m.gridpoints, [exact(x, inp) for x in m.gridpoints], label= "exact", color = "red", alpha = 0.8)

    plt.legend() 
    plt.show()
