# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
"""
Generate ronchigrams for lens testing.

Documentation and examples are available at <https://lenstest.readthedocs.io>
"""

import numpy as np
import matplotlib.pyplot as plt
import lenstest

__all__ = ('ronchi_mask',
           'ronchigram',
           'ronchi_plot')


def ronchi_mask(RoC, lpm, z_offset, conic, X, Y, mask=False, phi=0):
    """
    Create Ronchigram with random points.

    This assumes that the point source of light is located at the center
    of the mirror madius of curvature, RoC.

    The Ronchi grating is located at RoC + z_offset and oriented so lines
    are perpendicular to the x-axis

    The conic section is specified by conic:
          conic = ∞ for surface that is flat
          conic > 0 for surface that is an oblate spheroid
          conic = 0 for surface that is a sphere
          0<conic<-1 for surface that is a prolate spheroid
          conic = -1 for surface that is a paraboloid
          conic < -1 for surface that is a hyperboloid

    Args:
        D: diameter of mirror [mm]
        RoC: radius of curvature of mirror [mm]
        lpm: line pairs per mm [1/mm]
        z_offset: axial z_offset of grating from center of mirror's RoC [mm]
        conic: conic constant or Schwartzchild constant [-]
        X, Y: grid of points to evaluate
        invert: boolean to draw dark or light areas

    Returns:
        x, y: masked listed of points to plot
    """
    if mask:
        sagitta = 0
    else:
        sagitta = lenstest.lenstest.sagitta(RoC, conic, X, Y)

    # find the x value where the ray passes through the Ronchi ruling
    Xr = X * np.cos(phi) + Y * np.sin(phi)
    Lx = Xr * (-z_offset - sagitta * conic) / (RoC + sagitta * conic)

    # create mask for Ronchi Ruling
    T = (np.abs(2 * lpm * Lx) + 0.5).astype(int)

    T_mask = T % 2 == 0

    return T_mask


def ronchigram(D, RoC, lpm, z_offset, conic, phi=0,
               N=100000, invert=False, random=True, mask=False):
    """
    Create Ronchigram for points on a grid or randomly selected.

    This assumes that the point source of light is located at the center
    of the mirror madius of curvature, RoC.

    The Ronchi grating is displaced from the center of the mirror by z_offset.
    The Ronchi rulings are oriented so lines are perpendicular to the x-axis

    The conic section is specified by conic:
          conic = ∞ for surface that is flat
          conic > 0 for surface that is an oblate spheroid
          conic = 0 for surface that is a sphere
          0<conic<-1 for surface that is a prolate spheroid
          conic = -1 for surface that is a paraboloid
          conic < -1 for surface that is a hyperboloid

    Args:
        D: diameter of mirror [mm]
        RoC: radius of curvature of mirror [mm]
        lpm: line pairs per mm [1/mm]
        z_offset: axial z_offset of grating from true focus [mm]
        conic: conic constant or Schwartzchild constant [-]
        N: number of points to generate
        invert: boolean to draw dark or light areas
        random: if False generate points on a grid

    Returns:
        x, y: masked listed of points to plot
    """
    X, Y = lenstest.lenstest.XY_test_points(D, N=N, random=random)

    T_mask = ronchi_mask(RoC, lpm, z_offset, conic, X, Y, mask=mask, phi=phi)

    if invert:
        T_mask = np.logical_not(T_mask)

    # hide all points that should be dark
    x_mask = np.ma.masked_where(T_mask, X)
    y_mask = np.ma.masked_where(T_mask, Y)

    if mask:
        x_mask *= abs(z_offset / RoC)
        y_mask *= abs(z_offset / RoC)

    return x_mask, y_mask


def ronchi_plot(D, RoC, lp_per_mm, z_offset, conic, phi=0, init=True):
    """Plot the Surface Ronchigram."""
    x, y = ronchigram(D, RoC, lp_per_mm, z_offset, conic, phi=phi)

    if init:
        plt.subplots(1, 2, figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.gca().set_facecolor("black")
    plt.plot(x, y, 'o', markersize=0.1, color='white')
    plt.gca().set_aspect('equal')
    lenstest.lenstest.draw_circle(D / 2, color='green')
    plt.ylim(-D / 2 * 1.2, D / 2 * 1.2)
    plt.xlim(-D / 2 * 1.2, D / 2 * 1.2)
    plt.title("D=%.1fmm, RoC=%.1fmm, K=%.2f" % (D, RoC, conic))
    plt.xlabel("Mirror/Lens Plane (mm)")
    plt.ylabel("Mirror/Lens Plane (mm)")

    x, y = ronchigram(D, RoC, lp_per_mm, z_offset, conic, phi=phi, mask=True)
    plt.subplot(1, 2, 2)
    plt.gca().set_facecolor("black")
    plt.plot(x, y, 'o', markersize=0.6, color='white')
    r_spot = D / 2 / RoC * z_offset
    lenstest.lenstest.draw_circle(r_spot, color='green')
    plt.gca().set_aspect('equal')
    plt.xlabel("Ronchi Ruling Plane (mm)")

    size = r_spot * 1.2
    plt.ylim(-size, size)
    plt.xlim(-size, size)

    plt.title('Δz=%.2fmm, %.0f lp/mm' % (z_offset, lp_per_mm))
