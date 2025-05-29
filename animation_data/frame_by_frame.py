import os
import re
import numpy as np 
from matplotlib import pyplot as plt

mu_list = []
vector_list = []

file_pattern = re.compile(r'^reed_(\d+)\.dat$')

files = sorted(
    [
        f for f in os.listdir('.')
        if (match := file_pattern.match(f)) and 0 <= int(match.group(1)) <= 100
    ],
    key=lambda name: int(file_pattern.match(name).group(1))
)

for filename in files:
    with open(filename, 'r') as f:
        lines = f.readlines()

        mu_line = lines[0].strip()
        mu = float(mu_line.split('=')[1].strip())
        mu_list.append(mu)

        vector = [float(line.strip()) for line in lines[1:] if line.strip()]
        vector_list.append(vector)

def plot_one(psi):
    
    # has to be uniform for this to work... cringe
    reed_mesh = np.linspace(0, 8, len(vector_list[0]))

    plt.figure(figsize=(12, 6))

    plt.ylabel("psi")
    plt.plot(reed_mesh, psi)
    plt.xlabel("x")
    plt.show()

from mpl_toolkits.mplot3d import Axes3D

def plot_ring(mu):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))

    ax.plot_surface(x, y, z, color='lightblue', alpha=0.5, edgecolor='none')

    theta = np.linspace(0, 2 * np.pi, 200)
    r = np.sqrt(1 - mu**2)
    y_ring = r * np.cos(theta)
    z_ring = r * np.sin(theta)
    x_ring = np.full_like(theta, mu)

    ax.plot(x_ring, y_ring, z_ring, color='red', linewidth=2)

    ax.set_box_aspect([1,1,1])
    ax.set_xlim([-1.1, 1.1])
    ax.set_ylim([-1.1, 1.1])
    ax.set_zlim([-1.1, 1.1])
    ax.view_init(elev=10, azim=-90)
    ax.set_title(f'mu = {mu}')
    plt.tight_layout()
    #ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_xlabel('x')
    ax.set_ylabel('')
    ax.set_zlabel('')
    plt.show()


#for vector in vector_list:
#    plot_one(vector)

for mu in mu_list:
    print(mu)
    #plot_ring(mu)

