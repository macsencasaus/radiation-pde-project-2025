from src.quadrature import AngularQuadrature
from src.mesh import Mesh
from src.input_data import InputData
import numpy as np
import matplotlib.pyplot as plt


def test_quad_sweep(psi: np.ndarray, n_angles: int, mesh: Mesh, data: InputData):
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
        aspect='equal',
        extent=[angles[0], angles[-1], mesh.gridpoints[0], mesh.gridpoints[-1]],
        origin='lower',
        cmap='viridis'
    )
    plt.colorbar(im, label=r'$\psi(x, \mu)$')
    plt.xlabel(r"$\mu$")
    plt.ylabel("x")
    plt.title(r"Intensity $\psi(x, \mu)$")
    plt.tight_layout()
    plt.show()
