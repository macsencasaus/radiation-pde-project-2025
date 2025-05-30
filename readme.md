# Radiation Transport Solver

This project implements a numerical solver for the **radiation transport equation** using both **source iteration** and **Diffusion Synthetic Acceleration (DSA)**. The solver handles piecewise-constant media and boundary conditions, discretized via a **Petrov-Galerkin finite element method** with SUPG stabilization.

We consider the steady-state **radiation transfer (linear Boltzmann) equation** for a single energy group.
Specifically, for some $D\subset \mathbb{R}^3$ we want to find $\psi : D \times \mathbb{S}^2 \rightarrow \R$ such that
$$
\Omega \cdot \nabla_\mathbf{x} \psi(\mathbf{x}, \Omega) + \sigma^t(\mathbf{x}) \psi(\mathbf{x}, \Omega) = \frac {\sigma^s(\mathbf{x})} {|\mathbb{S}^2|} \int_{\mathbb{S}^2} \psi(\mathbf{x}, \Omega') \ d \Omega' + q(\mathbf{x}), \quad \text{in } D \times \mathbb{S}^2
$$
$$
\psi(\mathbf{x}, \Omega) =  \alpha^\partial(\mathbf{x}),\quad \text{on } \{\mathbf{x} \in \partial D,\: \Omega \in \mathbb{S}^2 \ | \ n_\mathbf{x} \cdot \Omega < 0 \}.
$$
Here $\sigma^t$ is the total cross section, $\sigma^s$ is the scattering cross section, and $\sigma^a = \sigma^t - \sigma^s$ is the absorption cross section, and $q$ is some external source. The function $\psi$ represents the intensity of the radiation at location $\mathbf{x}\in \R^3$ and in the direction $\Omega\in \mathbb{S}^2$.

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
