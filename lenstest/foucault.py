# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
"""
Generate Foucaugrams (Foucault Knife Edge images) for lens testing.

Documentation and examples are available at <https://lenstest.readthedocs.io>
"""

import numpy as np
import matplotlib.pyplot as plt
import lenstest.lenstest

__all__ = ('foucault_mask',
           'foucaugram',
           'foucault_plot'
           )


def foucault_mask(RoC, x_offset, z_offset, conic, X, Y, phi=0, A1=0):
    """
    Create Foucault knife edge image with specified points.

    This assumes that the point source of light is located at the center
    of the mirror madius of curvature, RoC.

    The Ronchi grating is located at RoC + offset and oriented so lines
    are perpendicular to the x-axis

    The conic section is specified by conic:
          conic = ∞ for surface that is flat
          conic > 0 for surface that is an oblate spheroid
          conic = 0 for surface that is a sphere
          0<conic<-1 for surface that is a prolate spheroid
          conic = -1 for surface that is a paraboloid
          conic < -1 for surface that is a hyperboloid

    Args:
        RoC: radius of curvature of mirror [mm]
        lines_per_mm: line pairs per mm [1/mm]
        offset: axial offset of grating from center of mirror's RoC [mm]
        conic: conic constant or Schwartzchild constant [-]
        X, Y: grid of points to evaluate

    Returns:
        array of points blocked by knife edge
    """
    sagitta = lenstest.lenstest.sagitta(RoC, conic, X, Y, A1=A1)

    # find the x value where the ray passes through the Ronchi ruling
    Xr = X * np.cos(phi) + Y * np.sin(phi)
    Lx = Xr * (-z_offset - sagitta * conic) / (RoC + sagitta * conic)

    # create mask for Knife Edge
    T_mask = Lx < x_offset

    return T_mask


def foucaugram(D, RoC, x_offset, z_offset, conic,
               phi=0, N=100000, invert=False, random=True, A1=0):
    """
    Create Ronchigram for points on a grid or randomly selected.

    This assumes that the point source of light is located at the center
    of the mirror madius of curvature, RoC.

    The Ronchi grating is displaced from the center of the mirror by offset.
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
        lines_per_mm: line pairs per mm [1/mm]
        offset: axial offset of grating from true focus [mm]
        conic: conic constant or Schwartzchild constant [-]
        N: number of points to generate
        invert: boolean to draw dark or light areas
        random: if False generate points on a grid

    Returns:
        x, y: masked listed of points to plot
    """
    X, Y = lenstest.lenstest.XY_test_points(D, N=N, random=random)

    T_mask = foucault_mask(RoC, x_offset, z_offset, conic, X, Y, phi=phi, A1=A1)

    if invert:
        T_mask = np.logical_not(T_mask)

    # hide all points that will appear dark
    x_image = np.ma.masked_where(T_mask, X)
    y_image = np.ma.masked_where(T_mask, Y)
    return x_image, y_image


def foucault_plot(D, RoC, x_offset, offset, conic, phi=0, init=True, figsize=(10, 5), A1=0):
    """Plot the Foucault knife edge image."""
    x, y = foucaugram(D, RoC, x_offset, offset, conic, phi=phi, A1=A1)

    if init:
        plt.subplots(1, 2, figsize=figsize)

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

    plt.subplot(1, 2, 2)
    x, y = lenstest.lenstest.knife_polygon(D / 2, phi, x_offset)
    r_spot = abs(offset * D / 2 / RoC)
    lenstest.lenstest.draw_circle(r_spot, color='green')
    plt.gca().set_aspect('equal')
    plt.fill(x, y, color='black', alpha=0.8)
    plt.xlabel("Knife Edge Plane (mm)")

    size = r_spot * 4
    plt.ylim(-size, size)
    plt.xlim(-size, size)

    phid = np.degrees(phi)
    plt.title('Δz=%.2fmm, Δx=%.2fmm, ϕ=%.0f°' % (offset, x_offset, phid))
