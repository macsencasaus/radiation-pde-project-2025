from src.assemble_system import assemble_scattered_source, assemble_source, assemble_transport_matrix
from src.poisson import assemble_lhs_fish, assemble_rhs_fish_scattered, assemble_rhs_fish
from src.quadrature import AngularQuadrature
from src.mesh import Mesh
from src.input_data import InputData
import numpy as np
from scipy.sparse.linalg import spsolve

def compute_initial_guess(mesh: Mesh, data: InputData) -> np.ndarray:
    sig_s = [data.sigma_s[mesh.mat_id[cell]] + 1e-10 for cell in mesh.cells]
    r = [data.source[mesh.mat_id[cell]] + 1e-10 for cell in mesh.cells]
    sig_a = [data.sigma_t[mesh.mat_id[cell]] + 1e-10 - data.sigma_s[mesh.mat_id[cell]] for cell in mesh.cells]

    A = assemble_lhs_fish(mesh, sig_s, sig_a)
    b = assemble_rhs_fish(mesh, r, data.boundary_values[0], data.boundary_values[1])

    start_phi = spsolve(A, b, permc_spec=None, use_umfpack=True)
    return start_phi

def compute_delta(phi: np.ndarray, phi_half: np.ndarray, mesh: Mesh, data: InputData) -> np.ndarray:
    sig_s = [data.sigma_s[mesh.mat_id[cell]] + 1e-10 for cell in mesh.cells]
    sig_t = [data.sigma_t[mesh.mat_id[cell]] + 1e-10 for cell in mesh.cells]
    sig_a = [sig_t[i] - sig_s[i] + 1e-10 for i in range(len(sig_s))]

    residual = phi_half - phi
    A = assemble_lhs_fish(mesh, sig_s, sig_a)
    b = assemble_rhs_fish_scattered(mesh, sig_s, residual, data.boundary_values[0], data.boundary_values[1])

    delta = spsolve(A, b, permc_spec=None, use_umfpack=True)
    return delta

def compute_psi_star(angles, mesh: Mesh, data: InputData):
    As = [None] * len(angles)
    psi_star = np.zeros((len(angles), mesh.n_points))
    for l, angle in enumerate(angles):
        A = assemble_transport_matrix(angle, mesh, data)
        b = assemble_source(angle, mesh, data)
        psi_star[l] = spsolve(A, b, permc_spec=None, use_umfpack=True)
        As[l] = A
    return As, psi_star

def source_iteration_diffusion(n_angles: int, mesh: Mesh, data: InputData, tol: float, max_iter: int) -> np.ndarray:
    quad = AngularQuadrature(n_angles)
    angles = quad.angles
    As, psi_star = compute_psi_star(angles, mesh, data)
    start_phi = compute_initial_guess(mesh, data)
    psi_zero = np.zeros((len(angles), mesh.n_points))

    err = tol + 1
    iter = 0
    phi_n = start_phi
    while err > tol and iter < max_iter:
        for l, angle in enumerate(angles):
            A = As[l]
            b = assemble_scattered_source(angle, mesh, data, phi_n)
            psi_zero[l] = spsolve(A, b, permc_spec=None, use_umfpack=True)
        phi_half = quad.average_over_quadrature(psi_zero + psi_star)
        delta = compute_delta(phi_n, phi_half, mesh, data)
        phi_np1 = phi_half + delta 
        err = np.linalg.norm(phi_np1-phi_n, 1)
        phi_n = phi_np1
        iter += 1
    print(err, iter)
    return psi_zero+psi_star, phi_n

def source_iteration(n_angles: int, mesh: Mesh, data: InputData, tol: float, max_iter: int) -> np.ndarray:
    quad = AngularQuadrature(n_angles)
    angles = quad.angles
    As, psi_star = compute_psi_star(angles, mesh, data)
    start_phi = np.zeros(mesh.n_points)
    psi_zero = np.zeros((len(angles), mesh.n_points))

    err = tol + 1
    iter = 0
    phi_n = start_phi
    while err > tol and iter < max_iter:
        for l, angle in enumerate(angles):
            A = As[l]
            b = assemble_scattered_source(angle, mesh, data, phi_n)
            psi_zero[l] = spsolve(A, b, permc_spec=None, use_umfpack=True)
        phi_np1 = quad.average_over_quadrature(psi_zero + psi_star)
        err = np.linalg.norm(phi_np1-phi_n, 1)
        phi_n = phi_np1
        iter += 1
    print(err, iter)
    return psi_zero+psi_star, phi_n

