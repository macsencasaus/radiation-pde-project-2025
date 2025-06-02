# Radiation Transport Solver

This project implements a numerical solver for the **radiation transport equation** using both **source iteration** and **Diffusion Synthetic Acceleration (DSA)**. The solver handles piecewise-constant media and boundary conditions, discretized via a **Petrov-Galerkin finite element method** with SUPG stabilization.

We consider the steady-state **radiation transfer (linear Boltzmann) equation** for a single energy group.
Specifically, for some $D\subset \mathbb{R}^3$ we want to find $\psi : D \times \mathbb{S}^2 \rightarrow \mathbb{R}$ such that

$$\Omega \cdot \nabla_\mathbf{x} \psi(\mathbf{x}, \Omega) + \sigma^t(\mathbf{x}) \psi(\mathbf{x}, \Omega) = \frac {\sigma^s(\mathbf{x})} {|\mathbb{S}^2|} \int_{\mathbb{S}^2} \psi(\mathbf{x}, \Omega') \ d \Omega' + q(\mathbf{x}), \quad \text{in } D \times \mathbb{S}^2$$

$$\psi(\mathbf{x}, \Omega) =  \alpha^\partial(\mathbf{x}),\quad \text{on } \{\mathbf{x} \in \partial D,\: \Omega \in \mathbb{S}^2 \ | \ n_\mathbf{x} \cdot \Omega < 0 \}.$$

Here $\sigma^t$ is the total cross section, $\sigma^s$ is the scattering cross section, and $\sigma^a = \sigma^t - \sigma^s$ is the absorption cross section, and $q$ is some external source. The function $\psi$ represents the intensity of the radiation at location $\mathbf{x}\in \mathbb{R}^3$ and in the direction $\Omega\in \mathbb{S}^2$.

---

## Getting Started
See [Installation](#installation) for installing dependencies.
To solve the radiation transport equation, you can run the `solve_radiation_transport.py` script.
By default, this solves [Reed's problem](https://www.drryanmc.com/solutions-to-reeds-problem/), a common benchmark for solving this equation.

To change the parameters of problem, one can supply a JSON configuration file to the script as a command line argument.
The [default configuration](./config/default.json) is used when no configuration is supplied and solves Reed's problem.
The fields of the configuration file are as follows:

- **`n_angles`** *(int)*  
  Number of angular discretization points (ordinates) used in the quadrature for solving the transport equation.

- **`method`** *(string)*  
  Iterative method used for solving the transport equation. Options:  
  - `"DSA"` — Diffusion Synthetic Acceleration (faster convergence)  
  - `"source-iteration"` — Standard source iteration (slower but simpler)

- **`max_iter`** *(int)*  
  Maximum number of iterations allowed for the solver.

- **`tol`** *(float)*  
  Convergence tolerance. Iteration stops when the residual falls below this threshold.

- **`benchmark`** *(string)*  
  Path to a JSON file containing the physical and geometric parameters of the problem.

The `benchmark` file sets up physical quantities of the system.
The default configuration uses [reed.json](./benchmarks/reed.json).
The fields of the benchmark file are as follows:

- **`n_zones`** *(int)*  
  Number of distinct material zones in the domain.

- **`n_cells`** *(array of ints)*  
  Number of spatial cells in each zone. The length of this array must match `n_zones`.

- **`zone_length`** *(array of floats)*  
  Physical length of each zone. The sum defines the total domain length. Length must match `n_zones`.

- **`sigma_s`** *(array of floats)*  
  Scattering cross section for each zone. Represents the probability of scattering events.

- **`sigma_t`** *(array of floats)*  
  Total cross section for each zone — the sum of scattering and absorption cross sections.  
  \( \sigma_t = \sigma_s + \sigma_a \)

- **`source`** *(array of floats)*  
  External fixed source term in each zone.

- **`boundary_values`** *(array of two floats)*  
  Incoming angular flux at the left and right boundaries, respectively. Usually set to `0` for vacuum boundaries.

- **`supg_tuning_value`** *(float)*  
  Stabilization parameter for SUPG (Streamline Upwind Petrov–Galerkin) method, if used.

For more options regarding configuration, use the `-h` or `--help` flag on the `solve_radiation_transport.py` script.

---

## Primary Files
- `src/`
  - `mesh.py`: Mesh generation for 1D domains with heterogeneous media.
  - `input_data.py`: Parses and validates json data.
  - `assemble_system.py`: Assembles the linear system.
  - `fixed_point.py`: Implements the source iteration method.
  - `dsa.py`: Implements DSA for accelerated convergence.
  - `plotting.py`: Plotting and animation functions.
  - `poisson.py`: Solves auxiliary diffusion equations for DSA corrections.
  - `quadrature.py`: Performs Gauss-Legendre quadrature for angular integration.
- `solve_radiation_transport.py`: Solves the transport equation with scattering.
- `solve_transport.py`: Solves a scalar advection transport problem and compares with exact solutions (when applicable).

---

## Installation

It is strongly recommended to use a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# or
.venv\Scripts\activate          # Windows
```
Install dependencies with
```
pip install -r requirements.txt
```

## Testing
Pytest is used for unit testing and can be installed using pip on Windows or apt on Debian-based Linux distros. Run unit tests with
```
pytest
```
