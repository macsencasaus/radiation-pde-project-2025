import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse.linalg import spsolve

from src.assemble_system import assemble_source, assemble_transport_matrix
from src.input_data import InputData
from src.mesh import Mesh
from utils.args import Args


def exact(x: float, data: InputData) -> float:
    zone_lengths = data.zone_length
    sigma_t = data.sigma_t
    source = data.source
    x0 = 0
    x1 = zone_lengths[0]
    x2 = zone_lengths[0] + zone_lengths[1]

    s1, s2, s3 = sigma_t
    q1, q2, q3 = source

    u1 = q1 / s1 * (1 - np.exp(s1 * (x0 - x1)))
    u2 = u1 * np.exp(s2 * (x1 - x2))

    if x0 <= x and x <= x1:
        return q1 / s1 * (1 - np.exp(s1 * (x0 - x)))
    elif x1 < x and x <= x2:
        return u1 * np.exp(s2 * (x1 - x))
    else:
        return u2 * np.exp(s3 * (x2 - x)) + q3 / s3 * (1 - np.exp(s3 * (x2 - x)))


if __name__ == "__main__":
    args = Args("Solve transport equation in one direction (mu = 1)")

    inp = InputData(args.benchmark_file)
    m = Mesh(inp)

    mu = 1

    transport_mat = assemble_transport_matrix(mu, m, inp)
    b = assemble_source(mu, m, inp)
    u = spsolve(transport_mat, b, permc_spec=None, use_umfpack=True)

    # print("Transport mat:", transport_mat.toarray(), sep="\n")
    # print("rhs:", b, sep="\n")

    plt.plot(m.gridpoints, u, label="FEM", color="blue", alpha=0.8, linewidth=1)

    # we have an exact solution for the case of three zones,
    # mu = 1, and homogeneous boundary data
    if inp.n_zones == 3 and mu == 1 and inp.boundary_values[0] == 0:
        plt.plot(
            m.gridpoints,
            [exact(x, inp) for x in m.gridpoints],
            label="exact",
            color="red",
            alpha=0.8,
        )

    plt.xlabel("x", fontsize=12)
    plt.ylabel(r"$\psi(x)$", fontsize=12)
    plt.grid(True, linestyle=":", linewidth=0.6, alpha=0.7)
    plt.legend(fontsize=10, loc="best")
    plt.tight_layout()

    plt.legend()
    plt.show()
