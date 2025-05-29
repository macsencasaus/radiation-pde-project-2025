from src.mesh import Mesh
from src.input_data import InputData
from src.fixed_point import source_iteration
from src.dsa import diffusion_synthetic_acceleration
from src.plotting import plot_sphere, obtain_psi_mu, animate_sphere_gif
from utils.args import Args

if __name__ == "__main__":
    args = Args("Generate sphere plot and gif")

    inp = InputData(args.benchmark_file)
    m = Mesh(inp)

    if args.method == "DSA":
        psi, phi = diffusion_synthetic_acceleration(args.n_angles, m, inp, args.tol, args.max_iter)
    else:
        psi, phi = source_iteration(args.n_angles, m, inp, args.tol, args.max_iter)

    psi_mu = obtain_psi_mu(psi, 775)
    plot_sphere(psi_mu, save=True)
    animate_sphere_gif(psi, gif_path="img/sphere.gif", fps=10)
