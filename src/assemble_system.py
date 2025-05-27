from src.mesh import Mesh
import numpy as np
from src.input_data import InputData
from scipy.sparse import csr_matrix

def assemble_source(mu: float, mesh: Mesh, data: InputData) -> np.ndarray:
    # b = \int_a^b q(x)*(v(x)+tau*mu*v'(x))dx
    
    tau = np.zeros(mesh.n_points)
    sigma_t = [data.sigma_t[mesh.mat_id[cell]] for cell in mesh.cells]
    h = mesh.h 
    #tau = [data.supg_tuning_value/(max(abs(mu)/h[cell], sigma_t[cell])) for cell in mesh.cells]
    tau = [data.supg_tuning_value for cell in mesh.cells]
    b = np.zeros(mesh.n_points)
    q    = np.zeros(mesh.n_points)
    for m in range(0,mesh.n_cells):
        q[m] = data.source[mesh.mat_id[m]]  
    b[0] = q[0]*mesh.h[0]/2 \
        +tau[0]*(-mu*mesh.h[0]*q[0])
    for i in range(1,mesh.n_points-1):
        b[i] = q[i-1]*mesh.h[i-1]/2+q[i]*mesh.h[i]/2 \
            + tau[i-1]*q[i-1]*mu*mesh.h[i-1]- tau[i]*q[i]*mu*mesh.h[i]
    b[-1] = q[-1]*mesh.h[-1]/2 \
        + tau[-1]*(q[-1]*mu*mesh.h[-1])


    n = -1
    alpha0 = data.boundary_values[0]
    b[0] = b[0] + alpha0*(abs(mu*n)-mu*n)/2
    
    n = 1
    alpha1 = data.boundary_values[1]
    b[-1] = b[-1] + alpha1*(abs(mu*n)-mu*n)/2
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
    
    sigma_t = [data.sigma_t[mesh.mat_id[cell]] for cell in mesh.cells]
    h = mesh.h 
    #tau = [data.supg_tuning_value/(max(abs(mu)/h[cell], sigma_t[cell])) for cell in mesh.cells]
    tau = [data.supg_tuning_value for cell in mesh.cells]

    matrix_data = np.zeros(3*mesh.n_points - 2)
    n = -1
    sigma_t = [data.sigma_t[mesh.mat_id[cell]] for cell in mesh.cells]
    h = mesh.h

    matrix_data[0] = -mu/2 + (abs(mu)-(mu*n))/2 + sigma_t[0]*h[0]*2/6 \
        + tau[0]*( mu*mu - mu*sigma_t[0]*h[0]/2)
    matrix_data[1] =  mu/2 + sigma_t[0]*h[0]*1/6 \
        + tau[0]*(-mu*mu - mu*sigma_t[0]*h[0]/2)
    p = 1
    for i in range(1, mesh.n_points-1):
        p = p + 1 
        matrix_data[p] = -mu/2 + sigma_t[i-1]*h[i-1]*1/6 \
            + tau[i-1]*(-mu**2 + mu*sigma_t[i-1]*h[i-1]/2)
        p = p + 1
        matrix_data[p] = (sigma_t[i-1]*h[i-1]+sigma_t[i]*h[i])*2/6 \
            + tau[i-1]*(mu*mu + mu*sigma_t[i-1]*h[i-1]/2)  + tau[i]*(mu*mu - mu*sigma_t[i]*h[i]/2)
        p = p + 1
        matrix_data[p] = mu/2 + sigma_t[i]*h[i]*1/6 \
            + tau[i]*(-mu*mu - mu*sigma_t[i]*h[i]/2)
        
    matrix_data[p+1] = -mu/2 + sigma_t[-1]*h[-1]*1/6 \
        + tau[-1]*(-mu**2 + mu*sigma_t[-1]*h[-1]/2)
    n = 1
    matrix_data[p+2] = mu/2 + (abs(mu)-(mu*n))/2 + sigma_t[-1]*h[-1]*2/6 \
        + tau[-1]*( mu**2 + mu*sigma_t[-1]*h[-1]/2)
    [row, col] = generate_sparsity_pattern(mesh)
    sparseMatrix = csr_matrix((matrix_data, (row, col)),  
                          shape = (mesh.n_points, mesh.n_points))
    return sparseMatrix

