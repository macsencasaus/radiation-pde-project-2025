from src.mesh import Mesh
from src.assemble_system import generate_sparsity_pattern
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve

def fish(mesh: Mesh, sig_s: np.ndarray, sig_a: np.ndarray,  forcing: np.ndarray, alpha: float, beta: float) -> np.ndarray:
    sparseMatrix = assemble_lhs_fish(mesh, sig_s, sig_a)
    b = assemble_rhs_fish(mesh, forcing, alpha, beta)

    soln = spsolve(sparseMatrix, b, permc_spec=None, use_umfpack=True)
    # print(soln)
    return soln

def fish_scattered(mesh: Mesh, sig_s: np.ndarray, sig_a: np.ndarray,  forcing: np.ndarray, alpha: float, beta: float) -> np.ndarray:
    sparseMatrix = assemble_lhs_fish(mesh, sig_s, sig_a)
    b = assemble_rhs_fish_scattered(mesh, forcing, alpha, beta)

    soln = spsolve(sparseMatrix, b, permc_spec=None, use_umfpack=True)
    # print(soln)
    return soln

def assemble_rhs_fish(mesh: Mesh, forcing: np.ndarray, alpha: float, beta: float) -> np.ndarray:
    # sig_s and forcing are cell indexed
    h = mesh.h
    b = np.zeros(mesh.n_points)

    # b[0] = forcing[0] * h[0] / 2
    # strong boundary condition enforcement
    b[0] = alpha
    for i in range(1, mesh.n_points - 1):
        b[i] = forcing[i - 1] * h[i - 1] / 2 + forcing[i] * h[i] / 2
    # b[-1] = forcing[-1] * h[-1] / 2
    # strong boundary condition enforcement
    b[-1] = beta

    # print(b)
    return b

def assemble_rhs_fish_scattered(mesh: Mesh, sig_s: np.ndarray, forcing: np.ndarray, alpha: float, beta: float) -> np.ndarray:
    # sig_s cell indexed
    # forcing point indexed
    h = mesh.h
    b = np.zeros(mesh.n_points)

    # b[0] = forcing[0] * h[0] / 2
    # strong boundary condition enforcement
    b[0] = alpha
    for i in range(1,mesh.n_points-1):
        b[i] = \
            + forcing[i] * h[i - 1] * sig_s[i - 1] / 3      \
            + forcing[i] * h[i] * sig_s[i] / 3              \
            + forcing[i - 1] * h[i - 1] * sig_s[i - 1] / 2  \
            + forcing[i + 1] * h[i] * sig_s[i] / 2
    # b[-1] = forcing[-1] * h[-1] / 2
    # strong boundary condition enforcement
    b[-1] = beta

    # print(b)
    return b

def assemble_lhs_fish(mesh: Mesh, sig_s: np.ndarray, sig_a: np.ndarray) -> csr_matrix:
    # sig_s, forcing, and sig_t are cell indexed
    N = mesh.n_points
    matrix_data = np.zeros(3*N-2)

    h = mesh.h

    # matrix_data[0] =                    \
    #     + 1 / (h[0] * 3 * sig_s[0])     \
    #     + h[0] / (3 * sig_s[0])         \
    #     + h[0] * sig_a[0] / 9
    # matrix_data[1] =                    \
    #     - 1 / (h[0] * 3 * sig_s[0])     \
    #     - h[0] / (3 * sig_s[0])         \
    #     + h[0] * sig_a[0] / 9
    # p = 1

    # strong boundary condition enforcement
    matrix_data[0] = 1
    matrix_data[1] = 0
    p = 1
    for i in range(1, N-1):
        p = p + 1
        matrix_data[p] =                    \
        - 1 / (3 * sig_s[i - 1] * h[i - 1]) \
        + sig_a[i - 1] * h[i - 1] / 6
        p = p + 1
        matrix_data[p] =                    \
        + 1 / (3 * sig_s[i - 1] * h[i - 1]) \
        + sig_a[i - 1] * h[i - 1] / 3       \
        + 1 / (3 * sig_s[i] * h[i])         \
        + sig_a[i] * h[i] / 3
        p = p + 1
        matrix_data[p] =                    \
        - 1 / (3 * sig_s[i] * h[i])         \
        + sig_a[i] * h[i] / 6

    # matrix_data[p+1] =                  \
    #     - 1 / (h[-1] * 3 * sig_s[-1])   \
    #     - h[-1] / (3 * sig_s[-1])       \
    #     + h[-1] * sig_a[-1] / 9
    # matrix_data[p+2] =                  \
    #     + 1 / (h[-1] * 3 * sig_s[-1])   \
    #     + h[-1] / (3 * sig_s[-1])       \
    #     + h[-1] * sig_a[-1] / 9

    # strong boundary condition enforcement
    matrix_data[p+1] = 0
    matrix_data[p+2] = 1
    [row, col] = generate_sparsity_pattern(mesh)
    sparseMatrix = csr_matrix((matrix_data, (row, col)),
                          shape = (mesh.n_points, mesh.n_points))
    # print(sparseMatrix.toarray())
    return sparseMatrix