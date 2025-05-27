import unittest
import numpy as np
from src.quadrature import AngularQuadrature

class TestAngularQuadrature(unittest.TestCase):

    def test_constructor_even(self):
        aq = AngularQuadrature(4)
        self.assertEqual(aq.n_angles, 4)
        self.assertEqual(len(aq.angles), 4)
        self.assertEqual(len(aq.weights), 4)
        np.testing.assert_almost_equal(np.sum(aq.weights), 1.0)

    def test_constructor_odd_raises(self):
        with self.assertRaises(ValueError):
            AngularQuadrature(3)

    def test_average_scalar(self):
        aq = AngularQuadrature(6)
        data = np.ones(6)  # scalar function: f(μ) = 1
        result = aq.average_over_quadrature(data)
        self.assertAlmostEqual(float(result), 1.0)

    def test_average_vector(self):
        aq = AngularQuadrature(8)
        data = np.tile(np.array([2.0, 4.0]), (8, 1))  # shape (8, 2)
        result = aq.average_over_quadrature(data)
        np.testing.assert_array_almost_equal(result, [2.0, 4.0])

    def test_average_invalid_shape(self):
        aq = AngularQuadrature(4)
        with self.assertRaises(ValueError):
            aq.average_over_quadrature(np.ones((3,)))  # wrong first dim

    def test_exactness_on_polynomial(self):
        n = 6
        aq = AngularQuadrature(n)
        poly = aq.angles ** (2 * n - 1)
        result = aq.average_over_quadrature(poly) * 2  # scale to match true integral
        self.assertAlmostEqual(float(result), 0.0, places=14)
if __name__ == "__main__":
    unittest.main()
