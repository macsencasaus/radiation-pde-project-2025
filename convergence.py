from src.input_data import InputData
from src.mesh import Mesh
from src.poisson import fish
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

    u1 = q1 / s1 * (1 - np.exp(s1 * (x0 - x1)))
    u2 = u1 * np.exp(s2 *(x1 - x2))
    if x0 <= x and x <= x1:
        return q1 / s1 * (1 - np.exp(s1 * (x0-x)))
    elif x1 < x and x <= x2:
        return u1 * np.exp(s2 * (x1 - x))
    else:
        return u2 * np.exp(s3 * (x2 - x)) + q3 / s3 * (1 - np.exp(s3 * (x2 - x)))

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
    l2errors = []
    N_vals = []
    meshes = []

    inp = copy.deepcopy(base_inp)
    refinements = 10

    for _ in range(refinements):
        mesh = Mesh(inp)
        meshes.append(mesh)

        mu = 1

        # A = assemble_transport_matrix(mu, mesh, inp)
        # b = assemble_source(mu, mesh, inp)
        # u = spsolve(A, b)
        sig_a = [inp.sigma_t[mesh.mat_id[cell]] - inp.sigma_s[mesh.mat_id[cell]] for cell in mesh.cells]
        sig_s = [inp.sigma_s[mesh.mat_id[cell]] for cell in mesh.cells]
        forcing = [inp.source[mesh.mat_id[cell]] for cell in mesh.cells]
        alpha = inp.boundary_values[0]
        beta = inp.boundary_values[1]
        u = fish(mesh, sig_s, sig_a, forcing, alpha, beta)


        # error = compute_L2_error(mesh, u, inp)
        error = 0
        errors.append(error)

        # exact_vec = np.array([exact(x, inp) for x in mesh.gridpoints])
        exact_vec = exact_fish(mesh, inp)
        l2error = np.linalg.norm(u - exact_vec)
        l2errors.append(l2error)

        N_vals.append(mesh.n_cells)
        print(f"N={mesh.n_cells:4d}, L2 error = {error:.6e}, l2 error = {l2error:.6e}")

        # Refine each zone
        inp.n_cells = [2 * n for n in inp.n_cells]

    print("\nConvergence Table:")
    print("{:<8} {:<12} {:<8} {:<12} {:<8}".format("N", "L2 Error", "Rate", "ℓ2 Error", "Rate"))
    print("-" * 56)

    for i in range(len(N_vals)):
        n = N_vals[i]
        l2 = errors[i]
        d2 = l2errors[i]

        if i == 0:
            print(f"{n:<8d} {l2:<12.4e} {'-':<8} {d2:<12.4e} {'-':<8}")
        else:
            # rate_l2 = np.log(errors[i-1]/errors[i]) / np.log(2)
            rate_l2 = 0
            rate_d2 = np.log(l2errors[i-1]/l2errors[i]) / np.log(2)
            print(f"{n:<8d} {l2:<12.4e} {rate_l2:<8.2f} {d2:<12.4e} {rate_d2:<8.2f}")

    hs = [max(m.h) for m in meshes]

    plt.figure(figsize=(6, 4))
    plt.loglog(hs, errors, marker='o', linestyle='-', color='blue', label=r'$L^2$ error')
    plt.loglog(hs, l2errors, marker='x', linestyle='-', color='green', label=r'$\ell^2$ error')

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
