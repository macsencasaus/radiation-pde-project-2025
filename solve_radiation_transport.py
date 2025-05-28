from src.mesh import Mesh
from src.input_data import InputData
from src.fixed_point import source_iteration, source_iteration_diffusion
from src.plotting import quad_sweep, plot_sphere, obtain_psi_mu, animate_sphere_gif

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

    n_angles = 50
    # quad_sweep(n_angles, m, inp)
    #psi, phi = source_iteration(n_angles, m, inp, 0.00001, 1000)
    psi_diffusion, phi_diffusion = source_iteration_diffusion(n_angles, m, inp, 0.00001, 1000)

    plt.figure()
    plt.plot(m.gridpoints, phi_diffusion * 2, label = "FEM", color = "blue", alpha = 0.8, linewidth = 1)
    plt.legend()
    plt.show()

    quad_sweep(psi_diffusion, n_angles, m)

    psi_mu = obtain_psi_mu(psi_diffusion, 775)
    plot_sphere(psi_mu)
    animate_sphere_gif(psi_diffusion, gif_path="sphere1.gif", fps=10)
