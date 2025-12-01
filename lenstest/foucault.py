"""
Generate Foucault Knife Edge images (Foucaugrams) for mirror/lens testing.

Documentation and examples are available at <https://lenstest.readthedocs.io>
"""

import numpy as np
import matplotlib.pyplot as plt
import lenstest.lenstest

__all__ = ("gram", "plot_gram", "plot_knife_and_screen", "plot_lens_layout", "plot_mirror_layout")


def _transmitted(RoC, x_offset, z_offset, X, Y, conic=0, phi=0, mask=False, A=0):
    """
    Determine if X, Y points are transmitted past knife edge.

    This assumes that the point source of light is located at the center
    of the mirror madius of curvature, RoC (or two focal lengths from a lens).

    Args:
        RoC: radius of curvature of mirror [mm]
        x_offset: transverse knife edge displacement from optical axis [mm]
        z_offset: axial knife edge offset from paraxial focus [mm]
        X: grid of points to evaluate [mm]
        Y: grid of points to evaluate [mm]
        conic: conic constant or Schwartzchild constant [-]
        phi: CCW rotation of knife edge from vertical [radians]
        mask: show knife edge without lens/mirror effects
        A: coefficient of spherical aberration

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


def gram(D, RoC, x_offset, z_offset, conic=0, phi=0, N=100000, invert=False, on_grid=False, A=0, mask=False):
    """
    Create points that miss the knife edge.

    This assumes that the point source of light is located at the center
    of the mirror madius of curvature, RoC.

    The knife edge is displaced from the center of the mirror by x_offset.

    The knife edge is oriented its edge is vertical when phi=0.

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
        x_offset: transverse knife edge displacement from optical axis [mm]
        z_offset: axial knife edge offset from paraxial focus [mm]
        conic: conic constant or Schwartzchild constant [-]
        phi: CCW rotation of knife edge from vertical [radians]
        N: number of points to generate
        invert: boolean to draw dark or light areas
        on_grid: if False generate points on a grid
        mask: show Ronchi ruling without lens/mirror effects
        A: spherical aberration [1/mm³]

    Returns:
        x, y: masked listed of points to plot
    """
    X, Y = lenstest.lenstest.XY_test_points(D, N=N, on_grid=on_grid)

    T_mask = _transmitted(RoC, x_offset, z_offset, X, Y, conic=conic, phi=phi, A=A, mask=mask)

    if invert:
        T_mask = np.logical_not(T_mask)

    # hide all points that will appear dark
    x_image = np.ma.masked_where(T_mask, X)
    y_image = np.ma.masked_where(T_mask, Y)
    return x_image, y_image


def plot_gram(D, RoC, x_offset, z_offset, conic=0, phi=0, A=0, on_grid=False):
    """
    Plot the Foucault knife edge image.

    The idea is to graph both the beam on the knife edge and the expected
    projection on a screen located at the radius-of-curvature away from
    the focus.  This allows rapid visualization or roughly how much
    of the knife edge interacts with the screen.

    The beam size is limited by the diffraction focus limit of the beam
    (assuming a 1000nm wavelength).

    Args:
        D: diameter of mirror [mm]
        RoC: radius of curvature of mirror [mm]
        x_offset: transverse knife edge offset from optical axis [mm]
        z_offset: axial knife edge offset from paraxial focus [mm]
        conic: conic or Schwartzchild constant [-]
        phi: CCW rotation of Ronchi ruling from vertical [radians]
        A: spherical aberration [1/mm³]
        init: set to False to allow updating plots
        on_grid: if False generate points on a grid
        invert: set to True to invert ruling

    Returns:
        fig: matplotlib Figure object representing the plot
        ax: matplotlib Axes object representing the plot
    """
    x, y = gram(D, RoC, x_offset, z_offset, conic=conic, phi=phi, A=A, on_grid=on_grid)

    lenstest.lenstest.draw_circle(D / 2, color="blue")
    plt.plot(x, y, "o", markersize=0.1, color="white")
    plt.ylim(-D / 2 * 1.2, D / 2 * 1.2)
    plt.xlim(-D / 2 * 1.2, D / 2 * 1.2)
    plt.xlabel("(mm)")
    plt.ylabel("(mm)")
    plt.text(
        0.5,
        0.97,
        "Mirror/Lens is %s " % lenstest.lenstest.conic_string(conic),
        color="white",
        ha="center",
        va="top",
        transform=plt.gca().transAxes,
    )
    plt.title("Screen is %.0f mm from Focus" % RoC)
    plt.gca().set_aspect("equal")
    plt.gca().set_facecolor("black")


def plot_knife_and_screen(D, RoC, x_offset, z_offset, conic=0, phi=0, init=True, A=0, on_grid=False):
    """
    Plot the Foucault knife edge image.

    The idea is to graph both the beam on the knife edge and the expected
    projection on a screen located at the radius-of-curvature away from
    the focus.  This allows rapid visualization or roughly how much
    of the knife edge interacts with the screen.

    The beam size is limited by the diffraction focus limit of the beam
    (assuming a 1000nm wavelength).

    Args:
        D: diameter of mirror [mm]
        RoC: radius of curvature of mirror [mm]
        x_offset: transverse knife edge offset from optical axis [mm]
        z_offset: axial knife edge offset from paraxial focus [mm]
        conic: conic or Schwartzchild constant [-]
        phi: CCW rotation of Ronchi ruling from vertical [radians]
        init: set to False to allow updating plots
        A: spherical aberration [1/mm³]
        on_grid: if False generate points on a grid

    Returns:
        fig: matplotlib Figure object representing the plot
        ax: matplotlib Axes object representing the plot
    """
    if init:
        fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    else:
        fig, ax = None, None

    # plot in the plane of the knife edge
    plt.subplot(1, 2, 1)
    plt.gca().set_aspect("equal")

    # draw the knife
    x, y = lenstest.lenstest.knife_polygon(D / 2, phi, x_offset)
    plt.fill(x, y, color="silver", alpha=0.8)
    plt.plot(0, 0, "b+", markersize=5)

    # Draw circle showing spotsize in the knife edge plane
    r_geometric = abs(D / 2 / RoC * z_offset)  # mm
    r_diffraction = 0.5 * 1e-6 * (RoC / 2) / D  # mm
    r_spot = max(r_geometric, r_diffraction)
    lenstest.lenstest.draw_circle(r_spot, color="blue")

    # we always want to see the edge of the knife
    size = max(r_spot * 2.2, abs(2 * x_offset))
    plt.ylim(-size, size)
    plt.xlim(-size, size)

    #    plt.text(0.5, 0.96,
    #             'Δx=%.2fmm, ϕ=%.0f°' % (x_offset, np.degrees(phi)),
    #             color='white',
    #             ha='center', va='top',
    #             transform=plt.gca().transAxes
    #    )

    # label the plot
    plt.xlabel("Knife x (mm)")
    plt.ylabel("Knife y (mm)")
    ks = "at"
    if z_offset < 0:
        ks = "%.3fmm before" % abs(z_offset)
    if z_offset > 0:
        ks = "%.3fmm after" % z_offset
    plt.title("%s focus" % ks)

    # plot in the plane of the screen
    plt.subplot(1, 2, 2)
    plt.gca().set_facecolor("black")
    plt.gca().set_aspect("equal")

    # knife edge result
    x, y = gram(D, RoC, x_offset, z_offset, conic=conic, phi=phi, A=A, on_grid=on_grid)
    plt.plot(x, y, "o", markersize=0.1, color="white")

    # the circle for the projected circle from mirror
    lenstest.lenstest.draw_circle(D / 2, color="blue")
    size = D / 2 * 1.2
    plt.ylim(-size, size)
    plt.xlim(-size, size)

    # add labels
    plt.title("D=%.1fmm, RoC=%.1fmm, K=%.2f" % (D, RoC, conic))
    plt.xlabel("Screen x (mm)")
    plt.ylabel("Screen y (mm)")
    cs = lenstest.lenstest.conic_string(conic)
    plt.text(
        0.5,
        0.97,
        "Mirror/Lens is %s " % cs,
        color="white",
        ha="center",
        va="top",
        transform=plt.gca().transAxes,
    )
    plt.title("%.0fmm from Focus" % RoC)

    return fig, ax


def plot_lens_layout(D, RoC, x_offset, z_offset):
    """
    Plot the Foucault knife edge experiment.

    Args:
        D: diameter of mirror or lens [mm]
        RoC: radius of curvature of mirror [mm]
        x_offset: transverse knife edge offset from optical axis [mm]
        z_offset: axial knife edge offset from paraxial focus [mm]

    Returns:
        fig: matplotlib Figure object representing the plot
        ax: matplotlib Axes object representing the plot
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    # slope of marginal ray and ray touching knife
    m2 = (D / 2) / RoC
    if z_offset == 0:
        m = 0
    else:
        m = x_offset / z_offset

    # account for knife completely missing or blocking beam
    m = min(m, m2)
    m = max(m, -m2)

    # marginal rays
    plt.plot([-2 * RoC, -RoC, RoC], [0, D / 2, -D / 2], color="black", linewidth=1)
    plt.plot([-2 * RoC, -RoC, RoC], [0, -D / 2, D / 2], color="black", linewidth=1)
    plt.plot(-2 * RoC, 0, "ok", markersize=5)

    # ray touching the knife edge
    plt.plot([-2 * RoC, -RoC, RoC], [0, -m * RoC, m * RoC], color="black", linewidth=1, linestyle="--")

    # shade blocked light
    if z_offset < 0:
        plt.fill_between([z_offset, RoC], [m * z_offset, m * RoC], [z_offset * m2, D / 2], color="darkgray")
    else:
        plt.fill_between([z_offset, RoC], [m * z_offset, m * RoC], [-z_offset * m2, -D / 2], color="darkgray")

    # draw the lens
    lenstest.lenstest.draw_lens(D, RoC, -RoC)
    plt.text(-RoC, -D / 2, "lens / mirror", ha="right", rotation=90, color="blue", clip_on=True)

    # focus plane
    #    plt.text(0, D / 2, ' focus', ha='left')
    #    plt.axvline(0, color='black', linewidth = 1)

    # optical axis
    plt.axhline(0, color="blue", linewidth=1)
    plt.text(
        -RoC * 0.96,
        0,
        "optical axis ",
        ha="left",
        va="center",
        color="blue",
        bbox={"facecolor": "white", "edgecolor": "white"},
        clip_on=True,
    )

    # knife
    #    plt.axvline(z_offset, color='black', linewidth = 0.5)
    plt.plot([z_offset, z_offset], [x_offset, -D / 2], lw=2, color="black")
    plt.text(
        z_offset,
        -D / 2,
        "knife",
        ha="center",
        rotation=90,
        color="black",
        bbox={"facecolor": "white", "edgecolor": "white"},
        clip_on=True,
    )

    # screen
    plt.axvline(RoC, color="blue", linewidth=2)
    plt.text(RoC, -D / 2, "projection screen", ha="left", rotation=90, color="blue", clip_on=True)

    plt.xlabel("Distance from focus (mm)")
    plt.ylabel("Height above optical axis (mm)")
    plt.title("Foucault Knife Test Showing Shading of Screen")
    return fig, ax


def plot_mirror_layout(D, RoC, x_offset, z_offset):
    """
    Plot the Foucault knife edge experiment.

    Args:
        D: diameter of mirror or lens [mm]
        RoC: radius of curvature of mirror [mm]
        x_offset: transverse offset of knife edge from optical axis [mm]
        z_offset: axial knife edge offset from paraxial focus [mm]

    Returns:
        fig: matplotlib Figure object representing the plot
        ax: matplotlib Axes object representing the plot
    """
    # slope of marginal ray and ray touching knife
    fig, ax = plt.subplots(figsize=(10, 5))

    m2 = (D / 2) / RoC
    if z_offset == 0:
        m = 0
    else:
        m = x_offset / z_offset

    # account for knife completely missing or blocking beam
    m = min(m, m2)
    m = max(m, -m2)

    # marginal rays
    plt.plot(0, D / 20, "ok", markersize=5)
    plt.plot([0, -RoC, RoC], [D / 20, D / 2, -D / 2], color="black", linewidth=1)
    plt.plot([0, -RoC, RoC], [D / 20, -D / 2, D / 2], color="black", linewidth=1)

    # ray touching the knife edge
    plt.plot([0, -RoC, RoC], [D / 20, -m * RoC, m * RoC], color="black", linewidth=1, linestyle="--")

    # shade blocked light
    if z_offset < 0:
        plt.fill_between([z_offset, RoC], [m * z_offset, m * RoC], [z_offset * m2, D / 2], color="darkgray")
    else:
        plt.fill_between([z_offset, RoC], [m * z_offset, m * RoC], [-z_offset * m2, -D / 2], color="darkgray")

    # draw the lens
    lenstest.lenstest.draw_mirror(D, RoC, vertex=-RoC)
    plt.text(-RoC, -D / 2, "lens / mirror", ha="right", rotation=90, color="blue", clip_on=True)

    # focus plane
    #    plt.text(0, D / 2, ' focus', ha='left')
    #    plt.axvline(0, color='black', linewidth = 1)

    # optical axis
    plt.axhline(0, color="blue", linewidth=1)
    plt.text(
        -RoC * 0.96,
        0,
        "optical axis ",
        ha="left",
        va="center",
        color="blue",
        bbox={"facecolor": "white", "edgecolor": "white"},
        clip_on=True,
    )

    # knife
    #    plt.axvline(z_offset, color='black', linewidth = 0.5)
    plt.plot([z_offset, z_offset], [x_offset, -D / 2], lw=2, color="black")
    plt.text(
        z_offset,
        -D / 2,
        "knife",
        ha="center",
        rotation=90,
        color="black",
        bbox={"facecolor": "white", "edgecolor": "white"},
        clip_on=True,
    )

    # screen
    plt.axvline(RoC, color="blue", linewidth=2)
    plt.text(RoC, -D / 2, "projection screen", ha="left", rotation=90, color="blue", clip_on=True)

    plt.xlabel("Distance from focus (mm)")
    plt.ylabel("Height above optical axis (mm)")
    plt.title("Foucault Knife Test Showing Shading of Screen")
    return fig, ax
