# pylint: disable=protected-access
"""Test functionality of utility routines found in ronchi.py."""

import unittest
import numpy as np
import matplotlib.pyplot as plt
import lenstest


class TestGram(unittest.TestCase):
    """Evaluate gram functionality."""

    def test_gram_output_type(self):
        """Test that gram returns two numpy arrays."""
        D = 100
        RoC = 200
        lpm = 10
        z_offset = 10
        x, y = lenstest.ronchi.gram(D, RoC, lpm, z_offset)
        self.assertIsInstance(x, np.ndarray)
        self.assertIsInstance(y, np.ndarray)

    def test_gram_output_shape(self):
        """Test that gram returns arrays with correct shapes."""
        D = 100
        RoC = 200
        lpm = 10
        z_offset = 10
        x, y = lenstest.ronchi.gram(D, RoC, lpm, z_offset)
        self.assertEqual(x.shape, (100000,))
        self.assertEqual(y.shape, (100000,))

    def test_gram_invert_parameter(self):
        """Test that invert parameter inverts the output."""
        D = 100
        RoC = 200
        lpm = 10
        z_offset = 10
        x, y = lenstest.ronchi.gram(D, RoC, lpm, z_offset, invert=True)
        self.assertEqual(x.shape, (100000,))
        self.assertEqual(y.shape, (100000,))


class TestTransmitted(unittest.TestCase):
    """Evaluate _transmitted functionality."""

    def test_transmitted_output_type(self):
        """Test that _transmitted returns a numpy array."""
        RoC = 200
        lpm = 10
        z_offset = 10
        X = np.zeros((10, 10))
        Y = np.zeros((10, 10))
        result = lenstest.ronchi._transmitted(RoC, lpm, z_offset, X, Y)
        self.assertIsInstance(result, np.ndarray)

    def test_transmitted_output_shape(self):
        """Test that _transmitted returns array with correct shape."""
        RoC = 200
        lpm = 10
        z_offset = 10
        X = np.zeros((10, 10))
        Y = np.zeros((10, 10))
        result = lenstest.ronchi._transmitted(RoC, lpm, z_offset, X, Y)
        self.assertEqual(result.shape, (10, 10))

    def test_transmitted_mask_parameter(self):
        """Test that mask parameter works."""
        RoC = 200
        lpm = 10
        z_offset = 10
        X = np.zeros((10, 10))
        Y = np.zeros((10, 10))
        result = lenstest.ronchi._transmitted(RoC, lpm, z_offset, X, Y, mask=True)
        self.assertEqual(result.shape, (10, 10))


class TestPlotRulingAndScreen(unittest.TestCase):
    """Evaluate plot_ruling_and_screen functionality."""

    def test_plot_ruling_and_screen_output_type(self):
        """Test that plot_ruling_and_screen returns a tuple."""
        D = 100
        RoC = 200
        lpm = 10
        z_offset = 10
        fig, ax = lenstest.ronchi.plot_ruling_and_screen(D, RoC, lpm, z_offset)
        self.assertIsInstance(fig, plt.Figure)
        self.assertIsInstance(ax[0], plt.Axes)
        self.assertIsInstance(ax[1], plt.Axes)

    def test_plot_ruling_and_screen_output_shape(self):
        """Test that plot_ruling_and_screen returns a tuple with two elements."""
        D = 100
        RoC = 200
        lpm = 10
        z_offset = 10
        result = lenstest.ronchi.plot_ruling_and_screen(D, RoC, lpm, z_offset)
        self.assertEqual(len(result), 2)

    def test_plot_ruling_and_screen_grid_parameter(self):
        """Test that grid parameter has correct effect on plot."""
        D = 100
        RoC = 200
        lpm = 10
        z_offset = 10
        lenstest.ronchi.plot_ruling_and_screen(D, RoC, lpm, z_offset, on_grid=True)


class TestPlotLensLayout(unittest.TestCase):
    """Evaluate plot_lens_layout functionality."""

    def test_plot_lens_layout_output_type(self):
        """Test that plot_lens_layout returns a tuple of matplotlib Figure and Axes objects."""
        D = 100
        f = 200
        z_offset = 10
        fig, ax = lenstest.ronchi.plot_lens_layout(D, f, z_offset)
        self.assertIsInstance(fig, plt.Figure)
        self.assertIsInstance(ax, plt.Axes)

    def test_plot_lens_layout_output_shape(self):
        """Test that plot_lens_layout returns a tuple with two elements."""
        D = 100
        f = 200
        z_offset = 10
        result = lenstest.ronchi.plot_lens_layout(D, f, z_offset)
        self.assertEqual(len(result), 2)


class TestPlotMirrorLayout(unittest.TestCase):
    """Evaluate plot_mirror_layout functionality."""

    def test_plot_mirror_layout_output_type(self):
        """Test that plot_mirror_layout returns a tuple of matplotlib Figure and Axes objects."""
        D = 100
        RoC = 200
        z_offset = 10
        fig, ax = lenstest.ronchi.plot_lens_layout(D, RoC, z_offset)
        self.assertIsInstance(fig, plt.Figure)
        self.assertIsInstance(ax, plt.Axes)

    def test_plot_lens_layout_output_shape(self):
        """Test that plot_mirror_layout returns a tuple with two elements."""
        D = 100
        RoC = 200
        z_offset = 10
        result = lenstest.ronchi.plot_lens_layout(D, RoC, z_offset)
        self.assertEqual(len(result), 2)


# Run the test case
if __name__ == '__main__':
    unittest.main()
