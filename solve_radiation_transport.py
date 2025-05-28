from src.mesh import Mesh
from src.input_data import InputData
from src.fixed_point import source_iteration

import matplotlib.pyplot as plt
import numpy as np
import sys

# use: source ./.venv/Scripts/activate 
# to activate virtual environment (must be in main folder)
# use: deactivate to leave
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: solve_radiation_transport.py <json>")
        exit(1)

    input_dir = sys.argv[1]
    inp = InputData(input_dir)
    m = Mesh(inp)

    n_angles = 8
    start_phi = np.zeros(m.n_points)
    phi = source_iteration(start_phi, n_angles, m, inp, 0.00001, 1000)
    plt.plot(m.gridpoints, phi, label = "FEM", color = "blue", alpha = 0.8, linewidth = 1)

    plt.legend()
    plt.show()
