from src.mesh import Mesh
from src.input_data import InputData
from src.fixed_point import source_iteration
#from src.plotting import quad_sweep, plot_sphere, obtain_psi_mu, animate_sphere_gif
from src.dsa import diffusion_synthetic_acceleration

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

    #FIXME: make a input file (setup) that reads in problem set up.
    # it tells us what n_angles should be, if we should do
    # source iteration or DSA, what the tuning parameter should be,
    # what benchmark to use, what the max iter should be, and what 
    # the tolerance should be...

    n_angles = 50

    #psi, phi = source_iteration(n_angles, m, inp, 1e-10, 1000)
    psi, phi = diffusion_synthetic_acceleration(n_angles, m, inp, 1e-10, 1000)

    plt.figure()
    plt.plot(m.gridpoints, phi * 2, label = "FEM", color = "blue", alpha = 0.8, linewidth = 1)
    plt.ylabel(r'$2\overline{\psi}(x)$')
    plt.xlabel(r'$x$')
    plt.legend()
    plt.show()

   
    # FIXME: move to another script
    #psi_mu = obtain_psi_mu(psi_diffusion, 775)
    #plot_sphere(psi_mu)
    #animate_sphere_gif(psi_diffusion, gif_path="sphere1.gif", fps=10)
