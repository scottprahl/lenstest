# pylint: disable=invalid-name
"""
Utility routines for lens testing.

Documentation and examples are available at <https://lenstest.readthedocs.io>
"""

import numpy as np
import matplotlib.pyplot as plt

__all__ = ('XY_test_points',
           'knife_polygon',
           'circle_polygon',
           'draw_circle',
           'sagitta',
           'draw_lens',
           'conic_string')


def sagitta(RoC, conic, X, Y, A1=0):
    """
    Calculate sagitta for conic surface at points X,Y.

    This assumes that the point source of light is located at the center
    of the mirror radius of curvature.

    The Ronchi grating is located at RoC + z_offset and oriented so lines
    are perpendicular to the x-axis

    The conic section is specified by conic:
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
        A1: spherical aberration

    Returns:
        sagitta at each (x,y) point
    """
    # find the x value where the ray passes through the Ronchi ruling
    Pr_sqr = X**2 + Y**2
    heights = Pr_sqr / (RoC + np.sqrt(RoC * RoC - (1 + conic) * Pr_sqr))
    heights += A1 * Pr_sqr**2
#    print(A1, X[1]**2+Y[1]**2,heights[1])
    return heights


def draw_circle(R, X0=0, Y0=0, color='black'):
    """Draw a circle."""
    theta = np.linspace(0, 2 * np.pi, 100)
#    plt.gca().set_aspect('equal')
    plt.plot(X0 + R * np.sin(theta), Y0 + R * np.cos(theta), color=color)


def XY_test_points(D, N=100000, random=True):
    """
    Generate test points for lens test.

    Args:
        D: diameter of mirror [mm]
        N: number of points to generate
        random: if False generate points on a grid

    Returns:
        X,Y: arrays of test points
    """
    if random:
        U1 = np.random.uniform(size=N)
        U2 = np.random.uniform(size=N)
        X = D / 2 * np.sqrt(U2) * np.cos(2 * np.pi * U1)
        Y = D / 2 * np.sqrt(U2) * np.sin(2 * np.pi * U1)
    else:
        gridpts = np.linspace(-D / 2, D / 2, int(np.sqrt(N)))
        x_grid, y_grid = np.meshgrid(gridpts, gridpts)
        r_mask = x_grid**2 + y_grid**2 > D * D / 4
        X = np.ma.masked_where(r_mask, x_grid)
        Y = np.ma.masked_where(r_mask, y_grid)
    return X, Y


def knife_polygon2(r, phi, dx):
    """
    Create a polygon for a rotated knife edge.
    
    The polygon is a square that has been rotated by an
    angle phi from the verticle and then 

    Args:
        r: radius of mirror [mm]
        phi: rotation from vertical (positive ==> CCW) [radians]
        dx: horizontal offset [mm]
    Returns:
        x, y: coordinates of polygon
    """
    r *= 1.5
    rad = phi + np.pi / 2

    x = np.full(5, (dx + r) * np.cos(phi))
    y = np.full(5, (dx + r) * np.sin(phi))
    
    rad = rad + np.pi / 2
    x[1] = x[0] + 2 * r * np.cos(rad)
    y[1] = y[0] + 2 * r * np.sin(rad)

    rad = rad + np.pi / 2
    x[2] = x[1] + r * np.cos(rad)
    y[2] = y[1] + r * np.sin(rad)

    rad = rad + np.pi / 2
    x[3] = x[2] + 2 * r * np.cos(rad)
    y[3] = y[2] + 2 * r * np.sin(rad)

#    rad = rad + np.pi / 2
#    x[4] = x[3] + r * np.cos(rad)
#    y[4] = y[3] + r * np.sin(rad)
    
    # x[5] = x[0] and y[5] = y[0]
    return x, y


def knife_polygon(s, phi, ds):
    """
    Create a polygon for a rotated knife edge.
    
    The polygon is a vertical 1:2 rectangle that is shifted and
    then rotated counter clockwise.  
    
    When the shift is zero, then the edge of the knife edge is at the origin.
    Specifing a shift translates the knife edge across the origin.

    Args:
        s: short side of the rectangle [mm]
        phi: CCW rotation              [radians]
        ds: shift of knife edge        [mm]
    Returns:
        x, y: coordinates of polygon
    """
    # vertical s x 2s rectangle with center of edge shifted by dx
    xp = np.array([0,s,s,0,0]) + ds
    yp = np.array([s,s,-s,-s,s])
    
    # rotate rectangle CCW
    alpha = phi + np.pi
    x = xp * np.cos(alpha) - yp * np.sin(alpha)
    y = xp * np.sin(alpha) + yp * np.cos(alpha)
    
    return x,y


def circle_polygon(R, X0=0, Y0=0):
    """Create a polygon for a circle."""
    theta = np.linspace(0, 2 * np.pi, 100)
#    plt.gca().set_aspect('equal')
    return X0 + R * np.sin(theta), Y0 + R * np.cos(theta)


def draw_lens(D, RoC):
    """Draw one face of a lens or mirror."""
    theta_max = np.arctan2(D/2, RoC)
    theta = np.linspace(-theta_max,theta_max, 51)
    x = -RoC * np.cos(theta)
    y = -RoC * np.sin(theta)
    plt.plot(x,y,'b')


def conic_string(conic):
    """String that describes a conic value."""
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
