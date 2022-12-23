# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=consider-using-f-string
# pylint: disable=too-many-locals

"""
Generate Foucault Knife Edge images (Foucaugrams) for mirror/lens testing.

Documentation and examples are available at <https://lenstest.readthedocs.io>
"""

import numpy as np
import matplotlib.pyplot as plt
import lenstest.lenstest

__all__ = ('gram',
           'plot_ruling_and_screen',
           'plot_lens_layout',
           'plot_mirror_layout')


def _transmitted(RoC, x_offset, z_offset, X, Y, conic=0, phi=0, mask=False, A=0):
    """
    Determine if X,Y points are transmitted past knife edge.

    This assumes that the point source of light is located at the center
    of the mirror madius of curvature, RoC (or two focal lengths from a lens).

    Args:
        RoC: radius of curvature of mirror [mm]
        x_offset: knife edge displacement from optical axis [mm]
        z_offset: axial distance from from true focus [mm]
        X, Y: grid of points to evaluate [mm]
        conic: conic constant or Schwartzchild constant [-]
        phi: CCW rotation of knife edge from horizontal [radians]
        mask: show knife edge without lens/mirror effects
        A1: coefficient of spherical aberration
    Returns:
        1D boolean array describing points blocked by knife edge
    """
    if mask:
        sagitta = 0
    else:
        sagitta = lenstest.lenstest.sagitta(RoC, conic, X, Y, A=A)

    # rotate points
    Xr = X * np.cos(phi) + Y * np.sin(phi)

    # x values of rays intersecting plane of knife edge
    Lx = Xr * (-z_offset - sagitta * conic) / (RoC + sagitta * conic)

    # True/False array if points miss knife edge
    T_mask = Lx < x_offset

    return T_mask


def gram(D, RoC, x_offset, z_offset,
         conic=0, phi=0, N=100000, invert=False, on_grid=False, A=0, mask=False):
    """
    Create a Foucogram for points on a grid or randomly selected.

    This assumes that the point source of light is located at the center
    of the mirror madius of curvature, RoC.

    The knife edge is displaced from the center of the mirror by offset.

    The knife edge is oriented so lines are perpendicular to the x-axis

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
        x_offset: knife edge displacement from optical axis [mm]
        z_offset: axial distance from from true focus [mm]
        conic: conic constant or Schwartzchild constant [-]
        phi: CCW rotation of knife edge from horizontal [radians]
        N: number of points to generate
        invert: boolean to draw dark or light areas
        on_grid: if False generate points on a grid
        mask: show Ronchi ruling without lens/mirror effects
        A: spherical aberration [1/mm³]

    Returns:
        x, y: masked listed of points to plot
    """
    X, Y = lenstest.lenstest.XY_test_points(D, N=N, on_grid=on_grid)

    T_mask = _transmitted(RoC, x_offset, z_offset, X, Y,
                          conic=conic, phi=phi, A=A, mask=mask)

    if invert:
        T_mask = np.logical_not(T_mask)

    # hide all points that will appear dark
    x_image = np.ma.masked_where(T_mask, X)
    y_image = np.ma.masked_where(T_mask, Y)
    return x_image, y_image


def plot_ruling_and_screen(D, RoC, x_offset, z_offset,
                           conic=0, phi=0, init=True, A=0, on_grid=False):
    """Plot the Foucault knife edge image."""
    x, y = gram(D, RoC, x_offset, z_offset, conic=conic, phi=phi, A=A, on_grid=on_grid)

    if init:
        fig, ax = plt.subplots(1, 2, figsize=(10,4))
    else:
        fig, ax = None, None

    plt.subplot(1, 2, 2)
    plt.gca().set_facecolor("black")
    plt.plot(x, y, 'o', markersize=0.1, color='white')
    plt.gca().set_aspect('equal')
    lenstest.lenstest.draw_circle(D / 2, color='blue')
    plt.ylim(-D / 2 * 1.2, D / 2 * 1.2)
    plt.xlim(-D / 2 * 1.2, D / 2 * 1.2)
    plt.title("D=%.1fmm, RoC=%.1fmm, K=%.2f" % (D, RoC, conic))
    plt.xlabel("Projection Plane Coordinates (mm)")
    plt.ylabel("Projection Plane Coordinates (mm)")
    cs=lenstest.lenstest.conic_string(conic)
    plt.text(0.5, 0.97,
             "Mirror/Lens is %s " % cs,
             color='white',
             ha='center', va='top',
             transform=plt.gca().transAxes
    )
    plt.title("Screen is %.0f mm from Focus" % RoC)

    x, y = gram(D, RoC, x_offset, z_offset, phi=phi, mask=True, on_grid=on_grid)
    plt.subplot(1, 2, 1)
    x, y = lenstest.lenstest.knife_polygon(D / 2, phi, x_offset)
    r_spot = abs(z_offset * D / 2 / RoC)
    lenstest.lenstest.draw_circle(r_spot, color='blue')
    plt.gca().set_aspect('equal')
    plt.fill(x, y, color='black', alpha=0.8)
    plt.plot(0, 0, 'bo')
    plt.xlabel("Knife Plane Coordinates (mm)")
    plt.ylabel("Knife Plane Coordinates (mm)")

    size = max(r_spot * 4, abs(2*x_offset))
    plt.ylim(-size, size)
    plt.xlim(-size, size)

#    plt.text(0.5, 0.96,
#             'Δx=%.2fmm, ϕ=%.0f°' % (x_offset, np.degrees(phi)),
#             color='white',
#             ha='center', va='top',
#             transform=plt.gca().transAxes
#    )

    ks = 'at'
    if z_offset < 0:
        ks = '%.3fmm before' % abs(z_offset)
    if z_offset > 0:
        ks = '%.3fmm after' % z_offset
    plt.title("Knife edge is %s focus" % ks)
    return fig, ax


def plot_lens_layout(D, RoC, x_offset, z_offset):
    """
    Plot the Foucault knife edge experiment.

    Args:
        D: diameter of mirror or lens [mm]
        RoC: radius of curvature of mirror [mm]
        x_offset: transverse offset of knife edge from optical axis [mm]
        z_offset: axial offset of knife edge from true focus [mm]
    Returns:
        fig: matplotlib Figure object representing the plot
        ax: matplotlib Axes object representing the plot
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    # slope of marginal ray and ray touching knife
    m2 = (D/2)/RoC
    if z_offset == 0:
        m = 0
    else:
        m = x_offset/z_offset

    # account for knife completely missing or blocking beam
    m = min(m, m2)
    m = max(m,-m2)

    # marginal rays
    plt.plot([-RoC, RoC], [D/2,-D/2], color='black', linewidth=1)
    plt.plot([-RoC, RoC], [-D/2,D/2], color='black', linewidth=1)

    # ray touching the knife edge
    plt.plot([-RoC, RoC], [-m*RoC, m*RoC], color='black', linewidth=1, linestyle='--')

    # shade blocked light
    if z_offset < 0:
        plt.fill_between([z_offset, RoC], [m*z_offset, m*RoC],
                         [z_offset*m2, D/2], color='darkgray')
    else:
        plt.fill_between([z_offset, RoC], [m*z_offset, m*RoC],
                         [-z_offset*m2, -D/2], color='darkgray')

    # draw the lens
    lenstest.lenstest.draw_lens(D, RoC)
    plt.text(-RoC, -D/2, 'lens/mirror', ha='right', rotation=90, color='blue')

# focus plane
#    plt.text(0, D/2, ' focus', ha='left')
#    plt.axvline(0, color='black', linewidth = 1)

    # optical axis
    plt.axhline(0, color='blue', linewidth = 1)
    plt.text(-RoC*0.96, 0, 'optical axis ', ha='left', va='center', color='blue',
             bbox={"facecolor": "white", "edgecolor":"white"})

    # knife
#    plt.axvline(z_offset, color='black', linewidth = 0.5)
    plt.plot([z_offset, z_offset],[x_offset, -D/2], lw=2, color='black')
    plt.text(z_offset, -D/2, 'knife', ha='center', rotation=90, color='black',
             bbox={"facecolor": "white", "edgecolor":"white"})

    # screen
    plt.axvline(RoC, color='blue', linewidth = 2)
    plt.text(RoC, -D/2, 'projection screen', ha='left', rotation=90, color='blue')

    plt.xlabel('Distance from focus (mm)')
    plt.ylabel('Height above optical axis (mm)')
    plt.title('Foucault Knife Test Showing Shading of Screen')
    return fig, ax



def plot_mirror_layout(D, RoC, x_offset, z_offset):
    """
    Plot the Foucault knife edge experiment.

    Args:
        D: diameter of mirror or lens [mm]
        RoC: radius of curvature of mirror [mm]
        x_offset: transverse offset of knife edge from optical axis [mm]
        z_offset: axial offset of knife edge from true focus [mm]
    Returns:
        fig: matplotlib Figure object representing the plot
        ax: matplotlib Axes object representing the plot
    """
    # slope of marginal ray and ray touching knife
    fig, ax = plt.subplots(figsize=(10, 5))

    m2 = (D/2)/RoC
    if z_offset == 0:
        m = 0
    else:
        m = x_offset/z_offset

    # account for knife completely missing or blocking beam
    m = min(m, m2)
    m = max(m,-m2)

    # marginal rays
    plt.plot([-RoC, RoC], [D/2,-D/2], color='black', linewidth=1)
    plt.plot([-RoC, RoC], [-D/2,D/2], color='black', linewidth=1)

    # ray touching the knife edge
    plt.plot([-RoC, RoC], [-m*RoC, m*RoC], color='black', linewidth=1, linestyle='--')

    # shade blocked light
    if z_offset < 0:
        plt.fill_between([z_offset, RoC], [m*z_offset, m*RoC],
                         [z_offset*m2, D/2], color='darkgray')
    else:
        plt.fill_between([z_offset, RoC], [m*z_offset, m*RoC],
                         [-z_offset*m2, -D/2], color='darkgray')

    # draw the lens
    lenstest.lenstest.draw_lens(D, RoC)
    plt.text(-RoC, -D/2, 'lens/mirror', ha='right', rotation=90, color='blue')

# focus plane
#    plt.text(0, D/2, ' focus', ha='left')
#    plt.axvline(0, color='black', linewidth = 1)

    # optical axis
    plt.axhline(0, color='blue', linewidth = 1)
    plt.text(-RoC*0.96, 0, 'optical axis ', ha='left', va='center', color='blue',
             bbox={"facecolor": "white", "edgecolor":"white"})

    # knife
#    plt.axvline(z_offset, color='black', linewidth = 0.5)
    plt.plot([z_offset, z_offset],[x_offset, -D/2], lw=2, color='black')
    plt.text(z_offset, -D/2, 'knife', ha='center', rotation=90, color='black',
             bbox={"facecolor": "white", "edgecolor":"white"})

    # screen
    plt.axvline(RoC, color='blue', linewidth = 2)
    plt.text(RoC, -D/2, 'projection screen', ha='left', rotation=90, color='blue')

    plt.xlabel('Distance from focus (mm)')
    plt.ylabel('Height above optical axis (mm)')
    plt.title('Foucault Knife Test Showing Shading of Screen')
    return fig, ax
