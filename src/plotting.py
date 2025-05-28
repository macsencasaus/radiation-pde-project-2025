from src.quadrature import AngularQuadrature
from src.mesh import Mesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import interp1d

def quad_sweep(psi: np.ndarray, n_angles: int, mesh: Mesh):
    quad = AngularQuadrature(n_angles)
    angles = quad.angles
    fig, ax = plt.subplots()
    line, = ax.plot([], [])
    title = ax.set_title("")
    ax.set_xlabel("x")
    ax.set_ylabel(r"$\psi$")
    def update_plot(index):
        line.set_data(mesh.gridpoints, psi[index])
        ax.set_xlim(mesh.gridpoints[0], mesh.gridpoints[-1])
        ax.set_ylim(np.min(psi), np.max(psi))
        title.set_text(f"Angle index {index}, mu = {angles[index]:.4f}")
        fig.canvas.draw_idle()
    index = [0]
    update_plot(index[0])
    def on_key(event):
        if event.key == 'right':
            index[0] = (index[0] + 1) % n_angles
        elif event.key == 'left':
            index[0] = (index[0] - 1) % n_angles
        update_plot(index[0])
    fig.canvas.mpl_connect('key_press_event', on_key)
    plt.show()
    psi_avg = quad.average_over_quadrature(psi)

    plt.plot(mesh.gridpoints, psi_avg, label = "Psi", color = "blue", alpha = 0.8, linewidth = 1)

    plt.figure(figsize=(6, 6))
    im = plt.imshow(
        psi.T,
        aspect='auto',
        extent=[angles[0], angles[-1], mesh.gridpoints[0], mesh.gridpoints[-1]],
        origin='lower',
        cmap='viridis'
    )
    plt.colorbar(im)
    plt.xlabel(r"$\mu$")
    plt.ylabel("x")
    plt.title(r"Intensity $\psi(x, \mu)$")
    plt.tight_layout()
    plt.show()

def plot_rings_on_sphere(psi, n_angles, x_index: int):
    """
    Plot psi(mu, x_index) as colored rings on the unit sphere.
    Each ring lies at polar angle theta = arccos(mu), latitude ring at fixed z.
    """
    quad = AngularQuadrature(n_angles)
    mu = quad.angles
    values = psi[:, x_index]  # shape (n_angles,)

    # Set up a dense spherical grid
    theta = np.linspace(0, np.pi, 200)       # polar angle
    phi = np.linspace(0, 2 * np.pi, 200)     # azimuthal angle
    theta_grid, phi_grid = np.meshgrid(theta, phi)

    # Compute spherical coordinates
    x = np.sin(theta_grid) * np.cos(phi_grid)
    y = np.sin(theta_grid) * np.sin(phi_grid)
    z = np.cos(theta_grid)

    # Interpolate psi(mu) → psi(cos(theta)) for smooth mapping
    interp = interp1d(mu, values, kind='linear', fill_value="extrapolate")
    color_grid = interp(np.cos(theta_grid))

    # Plot the sphere
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    sphere = ax.plot_surface(
        x, y, z,
        facecolors=plt.cm.viridis((color_grid - np.min(values)) / (np.ptp(values))),
        rstride=1, cstride=1,
        antialiased=False, shade=False
    )

    # Plot setup
    ax.set_title(rf"Smooth Colored Sphere for $\psi(\mu, x_{{{x_index}}})$")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_box_aspect([1, 1, 1])

    # Add colorbar
    mappable = plt.cm.ScalarMappable(cmap='viridis')
    mappable.set_array(values)
    fig.colorbar(mappable, ax=ax, shrink=0.5, label=rf"$\psi(\mu, x_{{{x_index}}})$")
    plt.show()