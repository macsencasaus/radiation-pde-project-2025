from src.mesh import Mesh
from src.input_data import InputData
from src.fixed_point import source_iteration
from src.dsa import diffusion_synthetic_acceleration
from src.plotting import plot_sphere, obtain_psi_mu, animate_sphere_gif, animate_sphere_with_phi
from utils.args import Args

if __name__ == "__main__":
    args = Args("Generate sphere plot and gif")

    inp = InputData(args.benchmark_file)
    m = Mesh(inp)

    if args.method == "DSA":
        psi, phi, _, _ = diffusion_synthetic_acceleration(args.n_angles, m, inp, args.tol, args.max_iter)
    else:
        psi, phi, _, _ = source_iteration(args.n_angles, m, inp, args.tol, args.max_iter)

    psi_mu = obtain_psi_mu(psi, 775)
    #plot_sphere(psi_mu, save=True)
    #animate_sphere_gif(psi, m.gridpoints, gif_path="img/sphere.gif", fps=10)
    animate_sphere_with_phi(psi, m.gridpoints, phi, gif_path="phi_and_sphere.gif", fps=10)
