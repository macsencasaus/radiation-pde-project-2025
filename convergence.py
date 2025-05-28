from src.input_data import InputData
from src.mesh import Mesh
from src.assemble_system import assemble_transport_matrix, assemble_source
from scipy.sparse.linalg import spsolve
import numpy as np
import matplotlib.pyplot as plt
import sys
import copy

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
    
def compute_L2_error(mesh: Mesh, u_num: np.ndarray, data: InputData) -> float:
    error_sq = 0.0
    for i in range(mesh.n_cells):
        x0, x1 = mesh.gridpoints[i], mesh.gridpoints[i+1]
        xm = 0.5 * (x0 + x1)
        uh0, uh1 = u_num[i], u_num[i+1]
        uh = lambda x: uh0 + (uh1 - uh0) * (x - x0) / (x1 - x0)
        err = lambda x: (exact(x, data) - uh(x))**2
        error_sq += (x1 - x0) * (err(x0) + 4 * err(xm) + err(x1)) / 6  # Simpson's rule
    return np.sqrt(error_sq)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convergence.py <input_json>")
        exit(1)

    input_path = sys.argv[1]
    base_inp = InputData(input_path)

    errors = []
    N_vals = []
    meshes = []

    inp = copy.deepcopy(base_inp)
    refinements = 10

    for _ in range(refinements):
        mesh = Mesh(inp)
        meshes.append(mesh)

        mu = 1

        A = assemble_transport_matrix(mu, mesh, inp)
        b = assemble_source(mu, mesh, inp)
        u = spsolve(A, b)

        error = compute_L2_error(mesh, u, inp)
        errors.append(error)
        N_vals.append(mesh.n_cells)
        print(f"N={mesh.n_cells:4d}, L2 error = {error:.6e}")

        # Refine each zone
        inp.n_cells = [2 * n for n in inp.n_cells]

    print("\nEstimated convergence rates:")
    print(f"N={N_vals[0]}: err = {errors[0]:.2E}, rate = -")
    for i in range(1, len(errors)):
        rate = np.log(errors[i-1] / errors[i]) / np.log(2)
        print(f"N={N_vals[i]}: err = {errors[i]:.2E}, rate = {rate:.2f}")
    
    hs = [max(m.h) for m in meshes]

    plt.figure(figsize=(6, 4))
    plt.loglog(hs, errors, marker='o', linestyle='-', color='blue', label=r'$L^2$ error')

    ref_e = errors[3] * (np.array(hs) / hs[3])**2  # O(h^2)
    plt.loglog(hs, ref_e, 'k--', label='O(h)')

    plt.xlabel(r'$h_{\max}$ (max cell size)')
    plt.ylabel(r'$L^2$ Error')
    plt.title('FEM Convergence')
    plt.grid(True, which='both', linestyle='--', alpha=0.6)
    plt.legend()
    plt.gca().invert_xaxis()
    plt.tight_layout()
    plt.show()
    # plt.savefig("img/convergence.png")
