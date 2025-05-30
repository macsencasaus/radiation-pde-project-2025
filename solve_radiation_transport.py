from src.mesh import Mesh
from src.input_data import InputData
from src.fixed_point import source_iteration
#from src.plotting import quad_sweep, plot_sphere, obtain_psi_mu, animate_sphere_gif
from src.dsa import diffusion_synthetic_acceleration
from utils.args import Args

import matplotlib.pyplot as plt

# use: source ./.venv/Scripts/activate
# to activate virtual environment (must be in main folder)
# use: deactivate to leave
if __name__ == "__main__":
    args = Args("Solve radiation transport equation")

    inp = InputData(args.benchmark_file)
    m = Mesh(inp)

    if args.method == "DSA":
        psi, phi = diffusion_synthetic_acceleration(args.n_angles, m, inp, args.tol, args.max_iter)
    else:
        psi, phi = source_iteration(args.n_angles, m, inp, args.tol, args.max_iter)

    plt.figure()
    plt.plot(m.gridpoints, phi * 2, label = "FEM", color = "blue", alpha = 0.8, linewidth = 1)
    plt.ylabel(r'$2\overline{\psi}(x)$')
    plt.xlabel(r'$x$')
    plt.show()
