from src.assemble_system import assemble_scattered_source, assemble_source, assemble_transport_matrix
from src.quadrature import AngularQuadrature
from src.mesh import Mesh
from src.input_data import InputData
import numpy as np
from scipy.sparse.linalg import spsolve


def source_iteration(start_phi : np.ndarray, n_angles: int, mesh: Mesh, data: InputData, tol: float, max_iter: int) -> np.ndarray:
    quad = AngularQuadrature(n_angles)
    angles = quad.angles

    As = [None] * len(angles)
    psi_star = np.zeros((len(angles), mesh.n_points))
    for l, angle in enumerate(angles):
        A = assemble_transport_matrix(angle, mesh, data)
        b = assemble_source(angle, mesh, data)

        psi_star[l] = spsolve(A, b, permc_spec=None, use_umfpack=True)
        As[l] = A

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
    return phi_n

