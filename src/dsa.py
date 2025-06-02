from src.assemble_system import assemble_scattered_source, assemble_source, assemble_transport_matrix
from src.poisson import assemble_lhs_fish, assemble_rhs_fish_scattered, assemble_rhs_fish
from src.quadrature import AngularQuadrature
from src.mesh import Mesh
from src.input_data import InputData
from src.fixed_point import compute_initial_guess, compute_initial_guess, compute_psi_star, compute_delta
import numpy as np
from scipy.sparse.linalg import spsolve
from tqdm import tqdm


def diffusion_synthetic_acceleration(n_angles: int, mesh: Mesh, data: InputData, tol: float, max_iter: int) -> tuple[np.ndarray, np.ndarray, float, float]:
    quad = AngularQuadrature(n_angles)
    angles = quad.angles
    As, psi_star = compute_psi_star(angles, mesh, data)
    start_phi = compute_initial_guess(mesh, data)
    psi_zero = np.zeros((len(angles), mesh.n_points))

    relative_error = tol + 1
    iter = 0
    phi_n = start_phi
    error_scale = np.linalg.norm(phi_n, 1) 
    while relative_error > tol and iter < max_iter:
        for l, angle in tqdm(enumerate(angles)):
            A = As[l]
            b = assemble_scattered_source(angle, mesh, data, phi_n)
            psi_zero[l] = spsolve(A, b, permc_spec=None, use_umfpack=True)
        phi_half = quad.average_over_quadrature(psi_zero + psi_star)
        delta = compute_delta(phi_n, phi_half, mesh, data)
        phi_np1 = phi_half + delta
        relative_error = float(np.linalg.norm(phi_np1-phi_n, 1)/error_scale)
        phi_n = phi_np1
        iter += 1
    return psi_zero+psi_star, phi_n, relative_error, iter

