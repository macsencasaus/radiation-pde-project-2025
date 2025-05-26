from radiation.mesh import Mesh
import numpy as np
from input_data import InputData

def assemble_source(alpha: float, mu: float, mesh: Mesh, data: InputData) -> np.ndarray:
    bs = np.zeros(mesh.n_points)
    for i in range(1, mesh.n_points - 1):
        left_side = data.source[mesh.mat_id[i - 1]] * mesh.h[i - 1]
        right_side = data.source[mesh.mat_id[i]] * mesh.h[i]
        bs[i] = (left_side + right_side) / 2

    if mu < 0:
        bs[0] = mesh.h[0] * data.source[0] / 2
        bs[-1] = alpha
    else:
        bs[0]  = alpha
        bs[-1] = mesh.h[-1] * data.source[-1] / 2
    return bs

