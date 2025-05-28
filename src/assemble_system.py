from src.mesh import Mesh
import numpy as np
from src.input_data import InputData
from scipy.sparse import csr_matrix

def assemble_scattered_source(mu: float, mesh: Mesh, data: InputData, cs: np.ndarray) -> np.ndarray:
    bs = np.zeros(mesh.n_points)

    sigma_t = [data.sigma_t[mesh.mat_id[cell]] for cell in mesh.cells]
    sigma_s = [data.sigma_s[mesh.mat_id[cell]] for cell in mesh.cells]

    tuning = data.supg_tuning_value
    tau = mu * tuning / max(abs(mu) / mesh.h[0], sigma_t[0])

    # j == 0
    # ------
    # i == 0
    bs[0] =  sigma_s[0] * cs[0] * mesh.h[0] / 3 - tau * mu * cs[0] * sigma_s[0] / 2
    # i == 1
    bs[0] += sigma_s[0] * cs[1] * mesh.h[0] / 3 - tau * mu * cs[1] * sigma_s[0] / 2

    tau = mu * tuning / max(abs(mu) / mesh.h[-1], sigma_t[-1])
    # j == -1
    # -------
    # i == -1
    bs[-1] =  sigma_s[-1] * cs[-1] * mesh.h[-1] / 6 + tau * mu * cs[-1] * sigma_s[-1] / 2
    # i == -2
    bs[-1] += sigma_s[-1] * cs[-2] * mesh.h[-1] / 6 + tau * mu * cs[-2] * sigma_s[-1] / 2

    # j =\= 0,-1
    for j in range(1, mesh.n_points-1):
        tau_left = mu * tuning / max(abs(mu) / mesh.h[j - 1], sigma_t[j - 1])
        tau_right = mu * tuning / max(abs(mu) / mesh.h[j], sigma_t[j])
        bs[j] = \
        sigma_s[j - 1] * cs[j - 1] * mesh.h[j - 1] / 6       + sigma_s[j - 1] * cs[j - 1] * tau_left * mu / 2 \
        + sigma_s[j - 1] * cs[j] * mesh.h[j - 1] / 3         + sigma_s[j - 1] * cs[j] * tau_left * mu / 2     \
        + sigma_s[j] * cs[j] * mesh.h[j] / 3                 - sigma_s[j] * cs[j] * tau_right * mu / 2        \
        + sigma_s[j] * cs[j + 1] * mesh.h[j] / 6             - sigma_s[j] * cs[j + 1] * tau_right * mu / 2
    return bs

def assemble_source(mu: float, mesh: Mesh, data: InputData) -> np.ndarray:
    # b = \int_a^b q(x)*(v(x)+tau*mu*v'(x))dx

    # first, we assemble our cell-wise constants
    sigma_t = [data.sigma_t[mesh.mat_id[cell]] for cell in mesh.cells]
    h = mesh.h
    tau = [data.supg_tuning_value/(max(abs(mu)/h[cell], sigma_t[cell])) for cell in mesh.cells]
    q = [data.source[mesh.mat_id[cell]] for cell in mesh.cells]
    
    b = np.zeros(mesh.n_points)
    b[0] = q[0]*(mesh.h[0]/2 - mu* tau[0])
    for i in range(1,mesh.n_points-1):
        left_part = q[i-1]*(h[i-1]/2 + mu * tau[i-1])
        right_part = q[i]*(h[i]/2 -mu*tau[i]) 
        b[i] = left_part + right_part
    b[-1] = q[-1]*(mesh.h[-1]/2 +mu*tau[-1])

    # Weak enforcement of boundary conditions:
    n = -1
    alpha0 = data.boundary_values[0]
    b[0] += alpha0*(abs(mu*n)-mu*n)/2

    n = 1
    alpha1 = data.boundary_values[1]
    b[-1] += alpha1*(abs(mu*n)-mu*n)/2

    return b

def generate_sparsity_pattern(mesh: Mesh) -> tuple[np.ndarray, np.ndarray]:
    N = mesh.n_points
    sten   = np.array([-1, 0, 1])
    col = np.zeros(3*N-2)
    row = np.zeros(3*N-2)
    row[0] = 0
    row[1] = 0
    col[0] = 0
    col[1] = 1
    p = 1
    for i in range(1,N-1):
        for k in range(0, 3):
            p = p + 1
            col[p] =  i + sten[k]
            row[p] =  i
    row[p+1] = N-1
    row[p+2] = N-1
    col[p+1] = N-2
    col[p+2] = N-1
    return row, col

# Petrov-Galerkin method
def assemble_transport_matrix(mu: float, mesh: Mesh, data: InputData) -> csr_matrix:
    # A = \int_a^b (mu*u'(x)+sigma_t*u(x))*(v(x)+tau*mu*v'(x))dx

    N = mesh.n_points
    matrix_data = np.zeros(3*N-2)

    # assembling cell-wise constants
    sigma_t = [data.sigma_t[mesh.mat_id[cell]] for cell in mesh.cells]
    h = mesh.h
    tuning = data.supg_tuning_value
    tau = [tuning/max(abs(mu)/h[cell], sigma_t[cell]) for cell in mesh.cells]

    p = 1
    for i in range(1, N-1):
        # T_i,i-1
        p = p + 1
        matrix_data[p] = -mu/2 + sigma_t[i-1]*h[i-1]*1/6 \
            + tau[i-1]*mu*(-mu/h[i-1] + sigma_t[i-1]/2)
       
       #T_i,i
        p = p + 1
        matrix_data[p] = (sigma_t[i-1]*h[i-1]+sigma_t[i]*h[i])*2/6 \
            + tau[i-1]*mu*(mu/h[i-1]+ sigma_t[i-1]/2) + tau[i]*mu*(mu/h[i] - sigma_t[i]/2)
        
        #T_i,i+1
        p = p + 1
        matrix_data[p] = mu/2 + sigma_t[i]*h[i]*1/6 \
            + tau[i]*mu*(-mu/h[i] - sigma_t[i]/2)
    
    # first row
    n = -1
    matrix_data[0] = -mu/2 + (abs(mu)-(mu*n))/2 + sigma_t[0]*h[0]*2/6 \
        + tau[0]*mu*( mu/h[0] -sigma_t[0]/2)
    matrix_data[1] =  mu/2 + sigma_t[0]*h[0]*1/6 \
        + tau[0]*mu*(-mu/h[0] - sigma_t[0]/2)
   
   # last row
    n = 1
    matrix_data[p+1] = -mu/2 +sigma_t[-1]*h[-1]*1/6 \
        + tau[-1]*mu*(-mu/h[-1] + sigma_t[-1]/2)
    matrix_data[p+2] = mu/2 + (abs(mu)-(mu*n))/2 + sigma_t[-1]*h[-1]*2/6 \
        + tau[-1]*mu*(mu/h[-1] + sigma_t[-1]/2)
    [row, col] = generate_sparsity_pattern(mesh)
    sparseMatrix = csr_matrix((matrix_data, (row, col)),
                          shape = (mesh.n_points, mesh.n_points))
    return sparseMatrix

