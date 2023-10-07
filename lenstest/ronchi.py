# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=consider-using-f-string
# pylint: disable=too-many-locals
"""
Generate ronchigrams for lens testing.

Documentation and examples are available at <https://lenstest.readthedocs.io>
"""

import numpy as np
import matplotlib.pyplot as plt
import lenstest

__all__ = ('gram',
           'plot_gram',
           'plot_ruling_and_screen',
           'plot_lens_layout',
           'plot_mirror_layout')


def _transmitted(RoC, lpm, z_offset, X, Y, conic=0, mask=False, phi=0):
    """
    Determine if X, Y points are transmitted through Ronchi ruling.

    This assumes that the one of the opaque lines of the ruling is centered on
    the optical axis.

    This also assumes that the point source of light is located at the center
    of the mirror's madius of curvature.

    The lines of the ruling are vertical when phi=0.

    Finally, the ruling is located at RoC + z_offset.  Negative values indicate
    that the ruling is located in front of the focus of the mirror.

    If `mask==True` then the mirror parameters are ignored.  This is useful
    for creating a plot for light at the Ronchi ruling.

    Args:
        RoC: radius of curvature of mirror [mm]
        lpm: line pairs per mm [1/mm]
        z_offset: axial z_offset of grating from center of mirror's RoC [mm]
        X, Y: grid of points to evaluate [mm]
        conic: conic constant or Schwartzchild constant [-]
        mask: show Ronchi ruling without lens/mirror effects
        phi: CCW rotation of Ronchi ruling from horizontal [radians]
    Returns:
        1D boolean array describing points blocked by Ronchi ruling
    """
    if mask:
        sagitta = 0
    else:
        sagitta = lenstest.lenstest.sagitta(RoC, conic, X, Y)

    # rotate points
    Xr = X * np.cos(phi) + Y * np.sin(phi)

    # x values of rays intersecting Ronchi ruling plane
    Lx = Xr * (-z_offset - sagitta * conic) / (RoC + sagitta * conic)

    # scale so even values pass through ruling
    T = (np.abs(4 * lpm * Lx) + 0.5).astype(int)

    # True/False array that designates if points pass through ruling
    T_mask = T % 2 == 0

    return T_mask


def gram(D, RoC, lpm, z_offset, conic=0, phi=0,
         N=100000, invert=False, on_grid=False, mask=False):
    """
    Create points that pass through a Ronchi ruling.

    When plotted these points will be a Ronchigram.

    This assumes that the point source of light is located at the center
    of the mirror madius of curvature, RoC.

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
        phi: CCW rotation of Ronchi ruling from vertical
        N: number of points to generate
        invert: boolean to draw dark or light areas
        on_grid: if False generate points on a grid
        mask: show Ronchi ruling without lens/mirror effects

    Returns:
        x, y: masked listed of points to plot
    """
    X, Y = lenstest.lenstest.XY_test_points(D, N=N, on_grid=on_grid)

    T_mask = _transmitted(RoC, lpm, z_offset, X, Y, conic=conic, mask=mask, phi=phi)

    if invert:
        T_mask = np.logical_not(T_mask)

    # hide all points that should be dark
    x_mask = np.ma.masked_where(T_mask, X)
    y_mask = np.ma.masked_where(T_mask, Y)

    if mask:
        x_mask *= abs(z_offset / RoC)
        y_mask *= abs(z_offset / RoC)

    return x_mask, y_mask


def plot_gram(D, RoC, lpm, z_offset, conic=0, phi=0, on_grid=False, invert=False):
    """
    Plot cross-sections on projection screen at a distance of RoC.

    Args:
        D: diameter of mirror [mm]
        RoC: radius of curvature of mirror [mm]
        lpm: line pairs per mm [1/mm]
        conic: conic or Schwartzchild constant [-]
        phi: CCW rotation of Ronchi ruling from vertical [radians]
        on_grid: if False generate points on a grid
        invert: set to True to invert ruling

    Returns:
        Nothing.
    """
    # generate and plot all the points
    x, y = gram(D, RoC, lpm, z_offset, conic=conic, phi=phi, invert=invert, on_grid=on_grid)
    plt.plot(x, y, 'o', markersize=0.1, color='white')

    # Draw circle showing spotsize on projection screen
    lenstest.lenstest.draw_circle(D / 2, color='green')

    # limit plot to slightly larger than the beam size
    size = D / 2 * 1.2
    plt.ylim(-size, size)
    plt.xlim(-size, size)
    plt.gca().set_facecolor("black")
    plt.gca().set_aspect('equal')
    plt.xlabel("(mm)")
    plt.ylabel("(mm)")


def plot_ruling_and_screen(D, RoC, lpm, z_offset,
                           conic=0, phi=0, init=True, on_grid=False, invert=False):
    """
    Plot cross-sections at Ronchi ruling and projection screen.

    The idea is to graph both the beam on the ruling and the expected
    projection on a screen located at the radius-of-curvature away from
    the focus.  This allows rapid visualization or roughly how much
    of the Ronchi ruling interacts with the screen.

    The beam size is limited by the diffraction focus limit of the beam
    (assuming a 1000nm wavelength).

    Args:
        D: diameter of mirror [mm]
        RoC: radius of curvature of mirror [mm]
        lpm: line pairs per mm [1/mm]
        z_offset: axial z_offset of grating from true focus [mm]
        conic: conic or Schwartzchild constant [-]
        phi: CCW rotation of Ronchi ruling from vertical [radians]
        init: set to False to allow updating plots
        on_grid: if False generate points on a grid
        invert: set to True to invert ruling

    Returns:
        fig: matplotlib Figure object representing the plot
        ax: matplotlib Axes object representing the plot
    """
    if init:
        fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    else:
        fig, ax = None, None

    # create plot in plane of Ronchi Ruling with beam size
    plt.subplot(1, 2, 1)
    plt.gca().set_facecolor("black")
    plt.gca().set_aspect('equal')

    # generate and plot all the points
    x, y = gram(D, RoC, lpm, z_offset, conic=conic,
                phi=phi, on_grid=on_grid, mask=True, invert=invert)
    plt.plot(x, y, 'o', markersize=0.6, color='white')

    # Draw circle showing spotsize at location of ruling
    r_geometric = abs(D / 2 / RoC * z_offset)        # mm
    r_diffraction = 0.5 * 1e-6 * (RoC / 2) / D       # mm
    r_spot = max(r_geometric, r_diffraction)
    lenstest.lenstest.draw_circle(r_spot, color='blue')
    if invert:
        plt.plot(0, 0, 'k+', markersize=5)
    else:
        plt.plot(0, 0, 'w+', markersize=5)

    # limit plot to slightly larger than the beam size
    size = r_spot * 1.2
    plt.ylim(-size, size)
    plt.xlim(-size, size)
    ks = 'at'
    if z_offset < 0:
        ks = '%.3fmm before' % abs(z_offset)
    if z_offset > 0:
        ks = '%.3fmm after' % z_offset
    plt.title("%s focus" % ks)
    plt.xlabel("Ruling Plane x (mm)")
    plt.ylabel("Ruling Plane y (mm)")

    # create plot in plane of the projection screen
    plt.subplot(1, 2, 2)
    plt.gca().set_facecolor("black")
    plt.gca().set_aspect('equal')

    # generate and plot all the points
    x, y = gram(D, RoC, lpm, z_offset,
                conic=conic, phi=phi, on_grid=on_grid, mask=False, invert=invert)
    plt.plot(x, y, 'o', markersize=0.1, color='white')

    # Draw circle showing spotsize on projection screen
    lenstest.lenstest.draw_circle(D / 2, color='green')

    # limit plot to slightly larger than the beam size
    size = D / 2 * 1.2
    plt.ylim(-size, size)
    plt.xlim(-size, size)
    plt.title('%.0fmm from Focus)' % RoC)
    plt.xlabel("Screen x (mm)")
    plt.ylabel("Screen y (mm)")

    return fig, ax


def plot_lens_layout(D, f, z_offset):
    """
    Plot the Ronchi Lens Test Layout (4f system).

    Args:
        D: diameter of mirror or lens [mm]
        f: focal length of lens [mm]
        z_offset: axial offset of knife edge from true focus [mm]
    Returns:
        fig: matplotlib Figure object representing the plot
        ax: matplotlib Axes object representing the plot
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    RoC = f          # for lens assuming n=1.5 and biconvex lens

    # point source
    plt.text(-4 * f, D * 0.05, 'point source', ha='left', rotation=90, color='blue')

    # marginal rays with lens at -2f
    DD = 0.8 * D
    plt.plot([-4 * f, -2 * f, 2 * f], [0, DD / 2, -DD / 2], color='black', linewidth=1)
    plt.plot([-4 * f, -2 * f, 2 * f], [0, -DD / 2, DD / 2], color='black', linewidth=1)
    plt.plot([-4 * f, -2 * f, 2 * f], [0, DD / 4, -DD / 4], color='black', linewidth=1)
    plt.plot([-4 * f, -2 * f, 2 * f], [0, -DD / 4, DD / 4], color='black', linewidth=1)

    # draw the lens
    lenstest.lenstest.draw_lens(D, RoC, -2 * f)
    plt.text(-2 * f, D / 2, 'lens under test', ha='left', color='blue')

# focus plane
#    plt.text(0, D / 2, ' focus', ha='left')
#    plt.axvline(0, color='black', linewidth=1)

    # optical axis
    plt.axhline(0, color='blue', linewidth=1)
#    plt.text(-RoC * 0.9, 0, 'optical axis ', ha='left', va='center', color='blue',
#             bbox={"facecolor": "white", "edgecolor":"white"})

    # Ronchi
#    plt.axvline(z_offset, color='black', linewidth = 0.5)
    plt.plot([z_offset, z_offset], [D / 2, -D / 2], ls='--', lw=2, color='black')
    plt.text(z_offset, D / 2, ' Ronchi Ruling', ha='left', color='black')

    # screen
    plt.axvline(2 * f, color='blue', linewidth=2)
    plt.text(2 * f * 1.02, -D / 2, 'projection screen', ha='left', rotation=90, color='blue')

    plt.xlabel('Distance from focus (mm)')
    plt.ylabel('Height above optical axis (mm)')
    plt.title('Ronchi Ruling Lens Test')
    return fig, ax


def plot_mirror_layout(D, RoC, z_offset):
    """
    Plot the Ronchi Mirror Test Layout.

    Args:
        D: diameter of mirror or lens [mm]
        RoC: radius of curvature of mirror [mm]
        z_offset: axial offset of knife edge from true focus [mm]
    Returns:
        fig: matplotlib Figure object representing the plot
        ax: matplotlib Axes object representing the plot
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    # initial height offset
    yo = D / 8

    # point source
    plt.text(0, yo, ' point source', ha='left', va='center', color='blue')

    # marginal rays with mirror at -RoC
    DD = 0.8 * D
    y_screen = -yo - (DD / 2 + yo) / RoC * D
    plt.plot([0, -RoC, 0, D], [yo, DD / 2, -yo, y_screen], color='blue', linewidth=1)
#    plt.plot([0, -RoC, 0], [yo, DD / 4, -yo], color='black', linewidth=1)
#    plt.plot([0, -RoC, 0], [yo, -DD / 4, -yo], color='black', linewidth=1)
    y_screen = -yo - (DD / 2 - yo) / RoC * D
    plt.plot([0, -RoC, 0, D], [yo, -DD / 2, -yo, -y_screen - 2 * yo], color='black', linewidth=1)

    # draw the mirror
    lenstest.lenstest.draw_mirror(D, RoC, -RoC)
    plt.text(-RoC, D / 2, 'mirror under test', ha='left', color='blue')

# focus plane
#    plt.text(0, D / 2, ' focus', ha='left')
#    plt.axvline(0, color='black', linewidth = 1)

    # optical axis
    plt.axhline(0, color='blue', linewidth=1)
#    plt.text(-RoC * 0.9, 0, 'optical axis ', ha='left', va='center', color='blue',
#             bbox={"facecolor": "white", "edgecolor":"white"})

    # Ronchi
#    plt.axvline(z_offset, color='black', linewidth = 0.5)
    plt.plot([z_offset, z_offset], [0, -D / 2], ls='--', lw=2, color='black')
    plt.text(z_offset, -D / 2, ' Ronchi Ruling', ha='right', color='black')

    # screen
    plt.axvline(D, color='blue', linewidth=2)
    plt.text(D * 1.02, -D / 2, 'projection screen', ha='left', rotation=90, color='blue')

    plt.xlabel('Distance from focus (mm)')
    plt.ylabel('Height above optical axis (mm)')
    plt.title('Ronchi Ruling Lens Test')
    return fig, ax
