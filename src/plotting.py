from src.quadrature import AngularQuadrature
from src.mesh import Mesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import Normalize
from matplotlib.animation import PillowWriter
import cmocean
from matplotlib.cm import ScalarMappable
from tqdm import tqdm

# To do
# --------
# Psi_bar vs x with color values on each segment

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
        cmap=cmocean.cm.matter
    )
    plt.colorbar(im)
    plt.xlabel(r"$\mu$")
    plt.ylabel("x")
    plt.title(r"Intensity $\psi(x, \mu)$")
    plt.tight_layout()
    plt.show()

def obtain_psi_mu(psi, x_index):
    values = psi[:, x_index]
    print(values.shape)
    return values

def plot_sphere(vector, save=False):
    n = len(vector)
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    theta = np.linspace(0, np.pi, n)
    phi = np.linspace(0, 2 * np.pi, 200)
    phi, theta = np.meshgrid(phi, theta)

    r = 1
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)

    vmin = 0
    vmax = 1.5
    cmap=cmocean.cm.matter
    norm = Normalize(vmin, vmax)
    color_vals = norm(vector)
    color_vals = np.tile(color_vals[:, None], (1, phi.shape[1]))
    surf = ax.plot_surface(x, y, z, facecolors=cmap(color_vals), linewidth=0, antialiased=False, shade=False)

    ax.set_box_aspect([1, 1, 1])
    ax.axis('off')

    mappable = ScalarMappable(cmap=cmap, norm=norm)
    mappable.set_array(vector)
    cbar = fig.colorbar(mappable, ax=ax, shrink=0.6, pad=0.1)
    cbar.set_label("Value")

    if save:
        plt.savefig("img/sphere.png", bbox_inches="tight")
    else:
        plt.show()


def animate_sphere_gif(psi, x_grid, gif_path="sphere.gif", fps=10):
    n_mu, n_x = psi.shape
    theta = np.linspace(0, np.pi, n_mu)
    phi = np.linspace(0, 2 * np.pi, 200)
    phi, theta_grid = np.meshgrid(phi, theta)

    x = np.sin(theta_grid) * np.cos(phi)
    y = np.sin(theta_grid) * np.sin(phi)
    z = np.cos(theta_grid)

    norm = Normalize(vmin=psi.min(), vmax=psi.max())
    cmap = cmocean.cm.matter

    fig = plt.figure(figsize=(18, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_box_aspect([1, 1, 1])
    ax.axis('off')

    # One persistent colorbar
    mappable = ScalarMappable(cmap=cmap, norm=norm)
    mappable.set_array(psi)
    cbar = fig.colorbar(mappable, ax=ax, shrink=0.6, pad=0.1)
    cbar.set_label("Value")

    writer = PillowWriter(fps=fps)

    with writer.saving(fig, gif_path, dpi=100):
        for i in tqdm(range(n_x), desc="Rendering frames"):
            for coll in reversed(ax.collections):
                coll.remove()

            ax.set_title(f"x = {x_grid[i]:.4f}")

            cbar.ax.set_ylabel(fr"$\Psi(x={x_grid[i]:.4f}, \mu)$", rotation=270, labelpad=20)
            values = norm(psi[:, i])
            color_vals = np.tile(values[:, None], (1, phi.shape[1]))
            ax.plot_surface(x, y, z, facecolors=cmap(color_vals),
                            linewidth=0, antialiased=False, shade=False)
            writer.grab_frame()

    print(f"GIF saved to {gif_path}")

def animate_sphere_with_phi(psi, x_grid, phi_vals, gif_path="phi_and_sphere.gif", fps=10):
    assert len(x_grid) == phi_vals.shape[0] == psi.shape[1], "Dimension mismatch"

    n_mu, n_x = psi.shape
    theta = np.linspace(0, np.pi, n_mu)
    phi_angle = np.linspace(0, 2 * np.pi, 200)
    phi_angle, theta_grid = np.meshgrid(phi_angle, theta)

    # Sphere coordinates
    x = np.sin(theta_grid) * np.cos(phi_angle)
    y = np.sin(theta_grid) * np.sin(phi_angle)
    z = np.cos(theta_grid)

    theta = -np.pi / 4 - np.pi/16
    x1 = z
    y1 = -y
    z1 = -x

    x_rot = x1 * np.cos(theta) - y1 * np.sin(theta)
    y_rot = x1 * np.sin(theta) + y1 * np.cos(theta)
    z_rot = z1

    norm = Normalize(vmin=psi.min(), vmax=psi.max())
    cmap = cmocean.cm.matter

    fig = plt.figure(figsize=(14, 6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.5])
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1], projection='3d')
    plt.subplots_adjust(wspace=0)

    ax2.set_box_aspect([1, 1, 1])
    ax2.axis('off')

    # Persistent colorbar
    mappable = ScalarMappable(cmap=cmap, norm=norm)
    mappable.set_array(psi)
    cbar = fig.colorbar(mappable, ax=ax2, shrink=0.6, pad=0.1)

    writer = PillowWriter(fps=fps)

    with writer.saving(fig, gif_path, dpi=100):
        for i in tqdm(range(n_x), desc="Rendering frames"):
            for coll in reversed(ax2.collections):
                coll.remove()
            ax1.clear()
            ax2.view_init(elev=0, azim=45)

            # Left plot: phi(x) with sliding indicator
            ax1.plot(x_grid, phi_vals, label=r"$\overline{\Psi(x)}$", color="black")
            ax1.axvline(x_grid[i], color="red", linestyle="--", label=fr"$x = {x_grid[i]:.4f}$")
            ax1.set_xlabel("x")
            ax1.set_ylabel(r"$\overline{\Psi(x)}$")
            ax1.grid(True)

            # Right plot: colored sphere with rotated orientation
            ax2.set_title(fr"$\Psi({x_grid[i]:.4f}, \Omega)$")
            values = norm(psi[:, i])
            color_vals = np.tile(values[:, None], (1, phi_angle.shape[1]))
            ax2.plot_surface(x_rot, y_rot, z_rot, facecolors=cmap(color_vals),
                             linewidth=0, antialiased=False, shade=False)
            writer.grab_frame()

    print(f"GIF saved to {gif_path}")

