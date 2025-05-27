from src.mesh import Mesh
import numpy as np
from src.input_data import InputData
from scipy.sparse import csr_matrix

def assemble_source(mu: float, mesh: Mesh, data: InputData, tau: np.ndarray) -> np.ndarray:
    # b = \int_a^b q(x)*(v(x)+tau*mu*v'(x))dx
    
    # tau = np.zeros(mesh.n_points)
    # for i in range(len(tau)):
    #     tau[i] = data.supg_tuning_value * (max(abs(mu) * (mesh.h[i])**(-1), data.sigma_t[i]))**(-1)

    bs = np.zeros(mesh.n_points)
    for i in range(1, mesh.n_points - 1):
        left_side = data.source[mesh.mat_id[i - 1]] * mesh.h[i - 1] \
            + data.source[mesh.mat_id[i - 1]] * tau[i - 1] * mu / mesh.h[i - 1]
        right_side = data.source[mesh.mat_id[i]] * mesh.h[i] \
            - data.source[mesh.mat_id[i]] * tau[i] * mu / mesh.h[i]
        bs[i] = (left_side + right_side) / 2

    bs[0] = mesh.h[0] * data.source[0] / 2 + (0.5 * (np.abs(mu) + mu) * data.boundary_values[0]) \
        - data.source[0] * tau[0] * mu / mesh.h[0]
    bs[-1] = mesh.h[-1] * data.source[-1] / 2 + (0.5 * (np.abs(mu) - mu) * data.boundary_values[1]) \
        + data.source[-1] * tau[-1] * mu / mesh.h[-1]

    return bs

def generate_sparse_pattern(mesh: Mesh) -> tuple[np.ndarray, np.ndarray]:
    rows = np.zeros(3 * (mesh.n_points) - 2) 
    cols = np.zeros(3 * (mesh.n_points) - 2) 
    rowsIdx, colsIdx = 0, 0
    
    for i in range(mesh.n_points):
        if i == 0:
            rows[rowsIdx + 0] = i
            rows[rowsIdx + 1] = i

            cols[colsIdx + 0] = i
            cols[colsIdx + 1] = i + 1

            colsIdx += 2
            rowsIdx += 2
        elif i == mesh.n_points - 1:
            rows[rowsIdx + 0] = i
            rows[rowsIdx + 1] = i

            cols[colsIdx + 0] = i - 1
            cols[colsIdx + 1] = i

            colsIdx += 2
            rowsIdx += 2
        else:
            rows[rowsIdx + 0] = i
            rows[rowsIdx + 1] = i
            rows[rowsIdx + 2] = i

            cols[colsIdx + 0] = i - 1
            cols[colsIdx + 1] = i
            cols[colsIdx + 2] = i + 1

            colsIdx += 3
            rowsIdx += 3

    return rows, cols
    
# Petrov-Galerkin method
def assemble_transport_matrix(mu: float, mesh: Mesh, data: InputData, tau: np.ndarray) -> csr_matrix:
    # A = \int_a^b (mu*u'(x)+sigma_t*u(x))*(v(x)+tau*mu*v'(x))dx
    rows, cols = generate_sparse_pattern(mesh)

    # tau = np.zeros(mesh.n_points)
    # for i in range(len(tau)):
    #     tau[i] = data.supg_tuning_value * (max(abs(mu) * (mesh.h[i])**(-1), data.sigma_t[i]))**(-1)

    matrix_data = np.zeros(3 * (mesh.n_points) - 2) 
    dataIdx = 0
    for i in range(mesh.n_points):
        if i == 0:
            # diagonal (first entry) (i == j == 0)
            matrix_data[dataIdx] = -mu / 2 + (1 / 3) * data.sigma_t[0] * mesh.h[0] \
                + (abs(mu) + mu)/2 \
                + (mu * mu) * tau[0] / mesh.h[0] - data.sigma_t[0] * tau[0] * mu / 2
            # upper diagonal (i == j - 1)
            matrix_data[dataIdx + 1] = mu / 2 + data.sigma_t[0] * mesh.h[0]/6 \
                - (mu * mu) * tau[0] / mesh.h[0] - data.sigma_t[0] * tau[0] * mu / 2
            dataIdx += 2
            pass
        elif i == mesh.n_points - 1:
            # lower diagonal (i == j + 1)
            matrix_data[dataIdx] = -mu / 2 + data.sigma_t[-1] * mesh.h[-1] / 6 \
                - (mu * mu) * tau[-1] / mesh.h[-1] + data.sigma_t[-1] * tau[-1] * mu / 2
            # diagonal (last entry) (i == j == -1)
            matrix_data[dataIdx + 1] = mu / 2 + (1 / 3) * data.sigma_t[-1] * mesh.h[-1] \
                + (abs(mu) - mu)/2 \
                + (mu * mu) * tau[-1] / mesh.h[-1] + data.sigma_t[-1] * tau[-1] * mu / 2
            pass
        else:
            # lower diagonal (i == j + 1)
            matrix_data[dataIdx] = -mu / 2 + data.sigma_t[mesh.mat_id[i - 1]] * mesh.h[i - 1] / 6 \
                - (mu * mu) * tau[i - 1] / mesh.h[i - 1] + data.sigma_t[mesh.mat_id[i - 1]] * tau[i - 1] * mu / 2
            # diagonal (i == j)
            matrix_data[dataIdx + 1] = (1/3) * (mesh.h[i] * data.sigma_t[mesh.mat_id[i]] + mesh.h[i - 1] * data.sigma_t[mesh.mat_id[i - 1]]) \
                + tau[i] * (mu * mu) / (mesh.h[i]) + tau[i - 1] * (mu * mu) / (mesh.h[i - 1]) \
                - tau[i - 1] * mu * data.sigma_t[mesh.mat_id[i - 1]] / 2 + tau[i] * mu * data.sigma_t[mesh.mat_id[i]] / 2 
            # upper diagonal (i == j - 1)
            matrix_data[dataIdx + 2] = mu / 2 + data.sigma_t[mesh.mat_id[i]] * mesh.h[i]/6 \
                - (mu * mu) * tau[i] / mesh.h[i] - data.sigma_t[mesh.mat_id[i]] * tau[i] * mu / 2
            dataIdx += 3

    matrix = csr_matrix((matrix_data, (rows, cols)), shape = (mesh.n_points, mesh.n_points))
    return matrix

# Regular Galerkin method
def assemble_transport_matrix_galerkin(mu: float, mesh: Mesh, data: InputData) -> csr_matrix:
    rows, cols = generate_sparse_pattern(mesh)

    matrix_data = np.zeros(3 * (mesh.n_points) - 2) 
    dataIdx = 0
    for i in range(mesh.n_points):
        if i == 0:
            # diagonal (first entry) (i == j == 0)
            matrix_data[dataIdx] = -mu / 2 + (1 / 3) * data.sigma_t[0] * mesh.h[0] + (abs(mu) + mu)/2
            # upper diagonal (i == j - 1)
            matrix_data[dataIdx + 1] = mu / 2 + data.sigma_t[0] * mesh.h[0]/6
            dataIdx += 2
            pass
        elif i == mesh.n_points - 1:
            # lower diagonal (i == j + 1)
            matrix_data[dataIdx] = -mu / 2 + data.sigma_t[-1] * mesh.h[-1] / 6
            # diagonal (last entry) (i == j == -1)
            matrix_data[dataIdx + 1] = mu / 2 + (1 / 3) * data.sigma_t[-1] * mesh.h[-1] + (abs(mu) - mu)/2
            pass
        else:
            # lower diagonal (i == j + 1)
            matrix_data[dataIdx] = -mu / 2 + data.sigma_t[mesh.mat_id[i - 1]] * mesh.h[i - 1] / 6
            # diagonal (i == j)
            matrix_data[dataIdx + 1] = (1/3) * (mesh.h[i] * data.sigma_t[mesh.mat_id[i]] + mesh.h[i - 1] * data.sigma_t[mesh.mat_id[i - 1]])
            # upper diagonal (i == j - 1)
            matrix_data[dataIdx + 2] = mu / 2 + data.sigma_t[mesh.mat_id[i]] * mesh.h[i]/6
            dataIdx += 3

    matrix = csr_matrix((matrix_data, (rows, cols)), shape = (mesh.n_points, mesh.n_points))
    return matrix

# Regular Galerkin method
def assemble_source_galerkin(mu: float, mesh: Mesh, data: InputData) -> np.ndarray:
    bs = np.zeros(mesh.n_points)
    for i in range(1, mesh.n_points - 1):
        left_side = data.source[mesh.mat_id[i - 1]] * mesh.h[i - 1]
        right_side = data.source[mesh.mat_id[i]] * mesh.h[i]
        bs[i] = (left_side + right_side) / 2

    bs[0] = mesh.h[0] * data.source[0] / 2 + (0.5 * (np.abs(mu) + mu) * data.boundary_values[0])
    bs[-1] = mesh.h[-1] * data.source[-1] / 2 + (0.5 * (np.abs(mu) - mu) * data.boundary_values[1])

    return bs
