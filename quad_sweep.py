from src.dsa import diffusion_synthetic_acceleration
from src.fixed_point import source_iteration
from src.input_data import InputData
from src.mesh import Mesh
from src.plotting import quad_sweep
from utils.args import Args

if __name__ == "__main__":
    args = Args("Illustrates quad sweep")

    inp = InputData(args.benchmark_file)
    m = Mesh(inp)

    if args.method == "DSA":
        psi, phi, _, _ = diffusion_synthetic_acceleration(
            args.n_angles, m, inp, args.tol, args.max_iter
        )
    else:
        psi, phi, _, _ = source_iteration(args.n_angles, m, inp, args.tol, args.max_iter)

    quad_sweep(psi, args.n_angles, m)
