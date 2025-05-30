<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Radiation Transport Solver</title>
  <script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
  <style>
    body {
      max-width: 800px;
      margin: auto;
      font-family: Arial, sans-serif;
      line-height: 1.6;
    }
    h1, h2, h3 {
      margin-top: 2em;
    }
    code {
      background-color: #f5f5f5;
      padding: 2px 4px;
      border-radius: 4px;
    }
    pre {
      background-color: #f5f5f5;
      padding: 10px;
      border-radius: 4px;
      overflow-x: auto;
    }
  </style>
</head>
<body>

<h1>Radiation Transport Solver</h1>

<p>
This project implements a numerical solver for the <strong>radiation transport equation</strong> using both <strong>source iteration</strong> and <strong>Diffusion Synthetic Acceleration (DSA)</strong>. The solver handles piecewise-constant media and boundary conditions, discretized via a <strong>Petrov-Galerkin finite element method</strong> with SUPG stabilization.
</p>

<p>
We consider the steady-state <em>radiation transfer (linear Boltzmann) equation</em> for a single energy group.
Specifically, for some \( D\subset \mathbb{R}^3 \), we want to find \( \psi : D \times \mathbb{S}^2 \rightarrow \mathbb{R} \) such that
</p>

\[
\Omega \cdot \nabla_\mathbf{x} \psi(\mathbf{x}, \Omega) + \sigma^t(\mathbf{x}) \psi(\mathbf{x}, \Omega) = \frac {\sigma^s(\mathbf{x})} {|\mathbb{S}^2|} \int_{\mathbb{S}^2} \psi(\mathbf{x}, \Omega') \, d \Omega' + q(\mathbf{x}), \quad \text{in } D \times \mathbb{S}^2
\]

\[
\psi(\mathbf{x}, \Omega) =  \alpha^\partial(\mathbf{x}),\quad 
\text{on } \{ \mathbf{x} \in \partial D,\: \Omega \in \mathbb{S}^2 \mid n_\mathbf{x} \cdot \Omega < 0 \}.
\]

<p>
Here \( \sigma^t \) is the total cross section, \( \sigma^s \) is the scattering cross section, and \( \sigma^a = \sigma^t - \sigma^s \) is the absorption cross section. The function \( q \) is an external source. The function \( \psi \) represents the intensity of the radiation at location \( \mathbf{x} \in \mathbb{R}^3 \) and in direction \( \Omega \in \mathbb{S}^2 \).
</p>

<h2>Primary Files</h2>
<ul>
  <li><code>src/mesh.py</code>: Mesh generation for 1D domains with heterogeneous media.</li>
  <li><code>src/input_data.py</code>: Parses and validates JSON data.</li>
  <li><code>src/assemble_system.py</code>: Assembles the linear system.</li>
  <li><code>src/fixed_point.py</code>: Implements the source iteration method.</li>
  <li><code>src/dsa.py</code>: Implements DSA for accelerated convergence.</li>
  <li><code>src/plotting.py</code>: Plotting and animation functions.</li>
  <li><code>src/poisson.py</code>: Solves auxiliary diffusion equations for DSA corrections.</li>
  <li><code>src/quadrature.py</code>: Performs Gauss-Legendre quadrature for angular integration.</li>
  <li><code>solve_radiation_transport.py</code>: Solves the transport equation with scattering.</li>
  <li><code>solve_transport.py</code>: Solves a scalar advection transport problem and compares with exact solutions (when applicable).</li>
</ul>

<h2>Installation</h2>

<p>It is strongly recommended to use a virtual environment:</p>

<pre><code>python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# or
.venv\Scripts\activate          # Windows
</code></pre>

<p>Install dependencies with:</p>

<pre><code>pip install -r requirements.txt
</code></pre>

<h2>Testing</h2>

<p>We use <code>pytest</code> for unit testing. Run tests with:</p>

<pre><code>pytest
</code></pre>

<p>The main script is <code>solve_radiation_transport.py</code>.</p>

</body>
</html>
