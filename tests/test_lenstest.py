import unittest

# Import the code you want to test
import lenstest
import numpy as np

class TestLensTest(unittest.TestCase):

  def test_sagitta(self):
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
      result = lenstest.lenstest.sagitta(*x)
#      self.assertEqual(result, expected_output)


  def test_draw_circle(self):
    inputs = [
      (100, 0, 0, 'black'),  # Test a circle with default X0, Y0, and color values
      (100, 50, 50, 'red'),  # Test a circle with non-default X0, Y0, and color values
      (100, -50, -50, 'blue'),  # Test a circle with negative X0 and Y0 values
    ]

    for x in inputs:
      result = lenstest.lenstest.draw_circle(*x)
      self.assertIsNone(result)


  def test_XY_test_points(self):
    inputs = [
      (100, 100000, True),  # Test the function with default values
      (100, 100000, False),  # Test the function with non-random points
      (100, 5, True),  # Test the function with a smaller number of points
    ]

    for x in inputs:
      result = lenstest.lenstest.XY_test_points(*x)
#      self.assertEqual(result, expected_output)


  def test_knife_polygon(self):
    inputs = [
      (10, 0, 0),  # Test the function with default values
      (10, np.pi / 2, 0),  # Test the function with a non-zero phi value
      (10, 0, 5),  # Test the function with a non-zero dx value
    ]

    for x in inputs:
      result = lenstest.lenstest.knife_polygon(*x)
#      self.assertEqual(result, expected_output)


  def test_circle_polygon(self):
    inputs = [
      (100, 0, 0),  # Test the function with default values
      (100, 50, 50),  # Test the function with non-default X0 and Y0 values
      (100, -50, -50),  # Test the function with negative X0 and Y0 values
    ]

    for x in inputs:
      result = lenstest.lenstest.circle_polygon(*x)
#      self.assertEqual(result, expected_output)

# Run the test case
if __name__ == '__main__':
  unittest.main()
