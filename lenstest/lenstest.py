"""
Utility routines for lens testing.

Documentation and examples are available at <https://lenstest.readthedocs.io>
"""

import numpy as np
import matplotlib.pyplot as plt

__all__ = ('sagitta',
           'XY_test_points',
           'knife_polygon',
           'circle_polygon',
           'draw_circle',
           'draw_lens',
           'draw_mirror',
           'conic_string',
           )


def sagitta(RoC, conic, X, Y, A=0, D=0):
    """
    Calculate sagitta for conic surface at points X, Y.

    This assumes that the point source of light is located at the center
    of the mirror radius of curvature.

    The Ronchi grating is located at RoC + z_offset and oriented so lines
    are perpendicular to the x-axis

    The conic section is specified by conic::
        conic = ∞ for surface that is flat,
        conic > 0 for surface that is an oblate spheroid,
        conic = 0 for surface that is a sphere,
        0<conic<-1 for surface that is a prolate spheroid,
        conic = -1 for surface that is a paraboloid
        conic < -1 for surface that is a hyperboloid

    Args:
        RoC: radius of curvature of mirror [mm]
        conic: conic constant or Schwartzchild constant [-]
        X: x-value(s) of points [mm]
        Y: y-value(s) of points [mm]
        A: spherical aberration [1/mm³]
        D: defocus [1/mm]

    Returns:
        sagitta at each (x, y) point [mm]
    """
    # find the x value where the ray passes through the Ronchi ruling
    rho_sqr = X**2 + Y**2
    heights = rho_sqr / (RoC + np.sqrt(RoC * RoC - (1 + conic) * rho_sqr))
    heights += A * rho_sqr**2
    heights += D * rho_sqr
    return heights


def draw_circle(R, X0=0, Y0=0, color='black'):
    """
    Draw a circle.

    If the circle that is plotted should be round, then
    `plt.gca().set_aspect('equal')` so aspect ratio on both axes is equal.

    Args:
        R: radius of circle
        X0: x-value of center of circle
        Y0: y-value of center of circle
        color: color of the circle
    Returns:
        X, Y: arrays of test points
    """
    theta = np.linspace(0, 2 * np.pi, 100)
    plt.plot(X0 + R * np.sin(theta), Y0 + R * np.cos(theta), color=color)


def XY_test_points(D, N=100000, on_grid=False):
    """
    Generate test points for lens test.

    The generated points all fall within a circle of radius D.

    Args:
        D: diameter of mirror [mm]
        N: number of points to generate
        on_grid: if False generate points on a grid
    Returns:
        X, Y: arrays of test points
    """
    if on_grid:
        gridpts = np.linspace(-D / 2, D / 2, int(np.sqrt(N)))
        x_grid, y_grid = np.meshgrid(gridpts, gridpts)
        r_mask = x_grid**2 + y_grid**2 > D * D / 4
        X = np.ma.masked_where(r_mask, x_grid)
        Y = np.ma.masked_where(r_mask, y_grid)
    else:
        U1 = np.random.uniform(size=N)
        U2 = np.random.uniform(size=N)
        X = D / 2 * np.sqrt(U2) * np.cos(2 * np.pi * U1)
        Y = D / 2 * np.sqrt(U2) * np.sin(2 * np.pi * U1)

    return X, Y


def knife_polygon(s, phi, ds):
    """
    Create a polygon for a rotated knife edge.

    The polygon is a vertical 1:2 rectangle that is shifted and
    then rotated counter clockwise.

    When the shift is zero, then the edge of the knife edge is at the origin.
    Specifing a shift translates the knife edge across the origin.  Then the
    knife is rotated about the origin by an angle phi.

    Args:
        s: short side of the rectangle   [mm]
        phi: CCW rotation from vertical  [radians]
        ds: shift of knife edge          [mm]

    Returns:
        x, y: coordinates of knife polygon
    """
    # vertical s x 2s rectangle with center of edge shifted by ds
    xp = np.array([-s, -s, 0, 0, -s]) + ds
    yp = np.array([-s, s, s, -s, -s])

    # rotate rectangle CCW
    x = xp * np.cos(phi) - yp * np.sin(phi)
    y = xp * np.sin(phi) + yp * np.cos(phi)

    return x, y


def circle_polygon(R, X0=0, Y0=0):
    """
    Create a polygon for a circle.

    If you want to plot the circle then the aspect ratio for the axes should
    to be set to equal: `plt.gca().set_aspect('equal')` so that the circle is
    looks round.

    Args:
        R: radius of the circle
        X0: x-value of center of circle
        Y0: y-value of center of circle
    Returns:
        x, y: coordinates of polygon
    """
    theta = np.linspace(0, 2 * np.pi, 100)
    return X0 + R * np.sin(theta), Y0 + R * np.cos(theta)


def draw_lens(D, RoC, middle=0):
    """
    Draw and fill a biconvex lens shape.

    If the glass has an index of 1.5, then the radius-of-curvature
    will equal the focal length.

    The lens is drawn with its center at `center`

    Args:
        D: diameter of the lens
        RoC: x-value of center of circle
        middle: y-value of center of circle
    Returns:
        Nothing.  Use `plt.show()` to see result
    """
    theta_max = np.arctan2(D / 2, RoC)
    theta = np.linspace(-theta_max, theta_max, 11)
    x = -RoC * np.cos(theta)
    y = -RoC * np.sin(theta)
    dx = RoC + x
    dx -= dx[0]     # offset surface to center the lens on the vertex

    xx = np.concatenate((middle - dx, middle + dx))
    yy = np.concatenate((y, -y))

    plt.fill(xx, yy, color='gray', alpha=0.8)


def draw_mirror(D, RoC, vertex=0):
    """Draw one face of a mirror."""
    theta_max = np.arctan2(D / 2, RoC)
    theta = np.linspace(-theta_max, theta_max, 51)
    x = -RoC * np.cos(theta)
    y = -RoC * np.sin(theta)
    dx = RoC + x
    dx -= dx[0]     # offset surface to center the lens on the vertex

    xx_last = np.array([vertex - dx[0] - D / 10, vertex - dx[0] - D / 10, vertex - dx[-1]])
    yy_last = np.array([y[-1], y[0], y[0]])
    xx = np.concatenate((vertex + dx, xx_last))
    yy = np.concatenate((y, yy_last))

    plt.fill(xx, yy, color='gray', alpha=0.8)


def conic_string(conic):
    """Create string that describes a conic value."""
    if np.isinf(conic):
        return 'flat'

    if conic > 0:
        return "oblate spheroid"

    if conic == 0:
        return "sphere"

    if conic > -1:
        return "prolate spheroid"

    if conic == -1:
        return "paraboloid"

    return "hyperboloid"
