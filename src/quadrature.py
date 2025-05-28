from scipy.special import roots_legendre
import numpy as np

class AngularQuadrature:
    """
    A class to compute Gauss-Legendre quadrature over the sphere

    Attributes
    ----------
    n_angles : int
        Number of angles in discretization (must be even)
    angles : np.ndarray
        Quadrature points
    weights : np.ndarray
        Normalized quadrature weights (sum to 1).
    total_weight : float
        The total sum of the weights (should always be 1.0 due to normalization).

    Methods
    ----------
    average_over_quadrature(vectors)
        Computes the weighted average over the angular quadrature for a given
        set of values indexed by angle.
    """
    def __init__(self, n_angles: int):
        if n_angles % 2 != 0:
            raise ValueError("n_angles must be even")
        self.n_angles = n_angles
        angles, weights = roots_legendre(n_angles)
        self.angles = angles
        self.weights = weights / np.sum(weights)
        self.total_weight = np.sum(self.weights)

    def average_over_quadrature(self, vectors):
        """
        vectors: np.ndarray of shape (n_angles, ...) matching self.n_angles
        Returns: weighted average over angle axis
        """
        if vectors.shape[0] != self.n_angles:
           raise ValueError("First dimension of vectors must match n_angles")

        if vectors.ndim == 1:
            return np.sum(self.weights * vectors)
        else:
            weighted = self.weights[:, np.newaxis] * vectors
            return np.sum(weighted, axis=0)
