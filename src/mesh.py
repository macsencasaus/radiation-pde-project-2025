from src.input_data import InputData
import numpy as np


class Mesh:
    """
    A class to represent a 1D computational mesh.

    Attributes
    ----------
    n_points : int
        Total number of grid points.
    n_cells : int
        Total number of cells.
    length : float
        Physical length of the domain.
    cells : list[int]
        List of cell indices from 0 to n_cells - 1.
    gridpoints : list[float]
        Physical coordinates of the grid points.
    h : list[float]
        Cell sizes (lengths), indexed by cell.
    mat_id : list[int]
        Material zone ID for each cell.
    """

    def __init__(self, input_data: InputData):
        self.n_cells = sum(input_data.n_cells)
        self.n_points = self.n_cells + 1
        self.length = sum(input_data.zone_length)
        self.cells = list(range(self.n_cells))
        self.gridpoints = [0.0]
        self.h = []
        self.mat_id = []

        for zone_idx in range(input_data.n_zones):
            zone_len = input_data.zone_length[zone_idx]
            zone_cells = input_data.n_cells[zone_idx]
            dx = zone_len / zone_cells

            for _ in range(zone_cells):
                self.h.append(dx)
                self.mat_id.append(zone_idx)
                self.gridpoints.append(self.gridpoints[-1] + dx)