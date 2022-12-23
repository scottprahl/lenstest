# pylint: disable=invalid-name
# pylint: disable=unused-variable
# pylint: disable=no-self-use
"""Test functionality of utility routines found in lenstest.py."""

import unittest
import numpy as np
from lenstest import lenstest

class TestLensTest(unittest.TestCase):
    """Evaluate all the functions."""

    def test_sagitta(self):
        """Ensure basic execution with different parameters."""
        inputs = [
            (100, 0, 0, 0),  # Test a flat surface
            (100, 1, 0, 0, 0),  # Test a sphere
            (100, -0.5, 0, 0, 0),  # Test a prolate spheroid
            (100, -1, 0, 0, 0),  # Test a paraboloid
            (100, -2, 0, 0, 0),  # Test a hyperboloid
            (100, 0, 5, 10, 0),  # Test the function with non-zero X and Y values
            (100, 0, 5, 10, 0.1),  # Test the function with a non-zero offset
            (100, 1, np.array([1,2]), np.array([0,3]), 0),  # Test with an array
        ]

        for x in inputs:
            result = lenstest.sagitta(*x)


    def test_draw_circle(self):
        """Ensure basic execution with different parameters."""
        inputs = [
            (100, 0, 0, 'black'),  # Test a circle with default X0, Y0, and color values
            (100, 50, 50, 'red'),  # Test a circle with non-default X0, Y0, and color values
            (100, -50, -50, 'blue'),  # Test a circle with negative X0 and Y0 values
        ]

        for x in inputs:
            lenstest.draw_circle(*x)


    def test_XY_test_points(self):
        """Ensure basic execution with different parameters."""
        inputs = [
            (100, 100000, True),  # Test the function with default values
            (100, 100000, False),  # Test the function with non-random points
            (100, 5, True),  # Test the function with a smaller number of points
        ]

        for x in inputs:
            result = lenstest.XY_test_points(*x)


    def test_knife_polygon(self):
        """Ensure basic execution with different parameters."""
        inputs = [
            (10, 0, 0),  # Test the function with default values
            (10, np.pi / 2, 0),  # Test the function with a non-zero phi value
            (10, 0, 5),  # Test the function with a non-zero dx value
        ]

        for x in inputs:
            result = lenstest.knife_polygon(*x)


    def test_circle_polygon(self):
        """Ensure basic execution with different parameters."""
        inputs = [
            (100, 0, 0),  # Test the function with default values
            (100, 50, 50),  # Test the function with non-default X0 and Y0 values
            (100, -50, -50),  # Test the function with negative X0 and Y0 values
        ]

        for x in inputs:
            result = lenstest.circle_polygon(*x)

    def test_sagitta_values(self):
        """
        Test calculations against Table 1 in Benjamin & Rosenblum.

        --- "Radii of Curvature and Sagittal Depths of Conic Sections,"
        ICLC, Vol. 19, pp. 76-83, March/April 1992

        The eccentricity for the first column was changed from -0.45 to 0.504j
        this gives the values of sagitta at all heights.

        I believe that there was a typo for results[8,3].  This is fixed.
        """
        e = np.array([0.504j,0,0.45,1,2])
        conic_constant = (-e*e).real

        # table from the paper
        results = np.array([[1.0,0.016,0.016,0.016,0.016,0.016],
                            [2.0,0.064,0.064,0.064,0.064,0.063],
                            [3.0,0.146,0.146,0.145,0.144,0.140],
                            [4.0,0.262,0.261,0.260,0.256,0.245],
                            [5.0,0.414,0.412,0.409,0.401,0.374],
                            [6.0,0.606,0.600,0.595,0.577,0.524],
                            [7.0,0.842,0.829,0.820,0.785,0.693],
                            [8.0,1.128,1.104,1.086,1.026,0.878],
                            [9.0,1.472,1.429,1.400,1.298,1.076],
                            [10.0,1.890,1.813,1.761,1.603,1.285],
                            [11.0,2.403,2.269,2.183,1.939,1.504],
                            [12.0,3.061,2.816,2.673,2.308,1.731]])

        #Sagittal Depths Given for a Spherical Surface Having a Radius of Curvature of 7.80 mm,
        RoC = 7.8
        y = (results[:,0]/2).flatten()
        x = np.zeros_like(y)

        for i, K in enumerate(conic_constant):
            sag = lenstest.sagitta(RoC, K, x, y)
            print(sag)
            table_sag = (results[:,i+1]).flatten()
            print(table_sag)
            np.testing.assert_allclose(sag, table_sag, atol=3e-3, rtol=3e-3)


# Run the test case
if __name__ == '__main__':
    unittest.main()
