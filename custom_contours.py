#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 11/05/17 at 3:04 PM

@author: neil

Program description here

Version 0.0.0
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.table import Table
from astropy import units as u
from tqdm import tqdm
import matplotlib.mlab as ml
import matplotlib.patches as mpatch
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib.path as mplPath


# =============================================================================
# Define variables
# =============================================================================


# -----------------------------------------------------------------------------



# =============================================================================
# Define functions
# =============================================================================
def densityPlot(frame, x, y, color, label=None, **kwargs):

    # deal with keyword arguments
    binx = kwargs.get('binx', 128)
    biny = kwargs.get('biny', 128)
    cmap = kwargs.get('cmap', None)
    outliers = kwargs.get('outliers', True)
    fill = kwargs.get('fill', True)
    outmarker = kwargs.get('outmarker', 'o')
    outsize = kwargs.get('outsize', 1)
    alpha = kwargs.get('alpha', 1)
    # deal with keyword arguments specific to contour/contourf
    plotkwargs = dict()
    keys = ['interpolation', 'alpha', 'fill', 'zorder', 'vmin', 'vmax',
            'origin', 'antialiased', ]
    for key in keys:
        if key in kwargs:
            plotkwargs[key] = kwargs[key]

    if frame is None:
        frame = plt.subplot(111)

    # get 2d histogram
    H, xedges, yedges = np.histogram2d(y, x, bins=(binx, biny))
    # get extent
    extent = [yedges[0], yedges[-1], xedges[0], xedges[-1]]
    # get contour levels
    levels = get_contour_levels(1, H.max())
    # get contour colours
    colours = get_contour_colours(levels, cmap)
    # plot contour/contour f
    if fill:
        im = frame.contourf(H, extent=extent, levels=levels, colors=colours,
                            **plotkwargs)
    else:
        im = frame.contour(H, extent=extent, levels=levels, colors=colours,
                           **plotkwargs)
    # plot outliers if True
    if outliers:
        mask = get_outliers(im, x, y)
        frame.scatter(x[mask], y[mask], color=color, label=label,
                      marker=outmarker, s=outsize, zorder=0, alpha=alpha)
        im2 = frame.contourf(H, extent=extent, levels=levels, colors='w',
                             alpha=1, zorder=0)

    return frame


def get_contour_levels(minimum, maximum):
    low = int(round(np.log10(minimum)))
    high = int(round(np.log10(maximum)))
    levels = []
    for i in range(low, high+1):
        levels.append(pow(10, low + i))
        levels.append(5 * pow(10, low + i))
    if len(levels) <= 4:
        levels = []
        for i in range(low, high+1):
            levels.append(pow(10, low + i))
            levels.append(2 * pow(10, low + i))
            levels.append(5 * pow(10, low + i))
    return levels


def get_contour_colours(levels, cmap=None):
    # add colours based on number of levels
    if cmap is None:
        cmap = 'Greys'
    colours = []
    cNorm = colors.Normalize(vmin=-2, vmax=len(levels))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cmap)
    for j in range(len(levels)):
        colorVal = scalarMap.to_rgba(j)
        colours.append(colorVal)
    return colours


# =============================================================================
# Outlier functions
# =============================================================================
def get_outliers(im, x, y):
    """
    From a matplotlib.contour.QuadContourSet (im) find those points in x and y
    that lay outside the contours
    :param im: matplotlib.contour.QuadContourSet from e.g. plt.contourf()
    :param x: array of float, horizontal axis values
    :param y: array of float, vertical axis values
    :return:
    """
    polygons, pin = make_polygons(im)
    # subsequently alter the total_mask (i.e. search all points for the inner
    # most polygon and then search the remaining points thereafter)
    total_mask = np.ones_like(x, dtype=bool)
    for p, polygon in enumerate(polygons[::-1]):
        inmask = mask_from_polygons(x[total_mask], y[total_mask], [polygon],
                                    None)
        total_mask[total_mask] &= ~inmask
    return total_mask


def make_polygons(im):
    """
    Makes a set of polygons from matplotlib.contour.QuadContourSet (im)
    and returns a list of polygon objects, a polygon collection
    :param im: matplotlib.contour.QuadContourSet from e.g. plt.contourf()
    :return polygons: the list or array of polygons, each polygon should be
                      a list of arrays that contain a set of vertices each
                      with a list of (x, y) coordinates:
                      polygons = [polygon1, polygon2, ... , polygonN]
                      where:
                      polygon1 = [vertexlist1, vertexlist2, ..., vertexlistN]
                      vertexlist1 = [(x0, y0), (x1, y1), ...., (xN, yN)]
                      i.e. a single polygon (a square) could be:
                          [[[(0, 0), (1, 0), (1, 1), (0, 1)]]]
    :return polygons_in: Array of bools Same shape as polygons
                         (except no vertices). This controls whether a polygon
                         is "inside" another polygon if include_holes is False
                         we assume any polygon with polygon_in = True is a hole
                         and thus the count should take these points as NOT
                         being in the polygons.
                         polygons_in = None
                         polygons_in = [polygon_in1, polygon_in2, ...,
                                       polygon_inN]
                         where:
                         polygon_in = [True, False, ..., True]
    """
    # get outer contour and plot outliers
    polygons = np.zeros(len(im.collections), dtype=object)
    # define threshold in x and y directions
    # loop around contour object collections
    for i in range(len(im.collections)):
        cs = im.collections[i]
        polygon = []
        # loop around contour object collection paths
        for j in range(len(cs.get_paths())):
            cspath = cs.get_paths()[j]
            polygon.append(cspath.vertices)
        polygons[i] = polygon
    # check if any of the polygons are contained within another polygon
    polygons_in = np.zeros(len(im.collections), dtype=object)
    for k in range(len(polygons)):
        polygon, polygon_in = polygons[k], []
        for i in range(len(polygon)):
            poly1 = mplPath.Path(polygon[i])
            contained = False
            for j in range(len(polygon)):
                if i != j:
                    poly2 = mplPath.Path(polygon[j])
                    contained |= bool(poly2.contains_path(poly1))
            polygon_in.append(contained)
        polygons_in[k] = polygon_in
    return polygons, polygons_in


def mask_from_polygons(xarr, yarr, polygons, polygons_in):
    """
    Takes a polygons set, and a polygon inside set with some x points and
    y points and returns a mask of of any inside the polygons set
    :param xarr: array of floats, x data points
    :param yarr: array of floats, y data poitns
    :param polygons: list of polygon objects, a polygon collection: this is
                     the list or array of polygons, each polygon should be
                     a list of arrays that contain a set of vertices each
                     with a list of (x, y) coordinates:
                     polygons = [polygon1, polygon2, ... , polygonN]
                     where:
                     polygon1 = [vertexlist1, vertexlist2, ..., vertexlistN]
                     vertexlist1 = [(x0, y0), (x1, y1), ...., (xN, yN)]
                     i.e. a single polygon (a square) could be:
                         [[[(0, 0), (1, 0), (1, 1), (0, 1)]]]
    :param polygons_in: Array of bools Same shape as polygons
                        (except no vertices). This controls whether a polygon
                        is "inside" another polygon if include_holes is False
                        we assume any polygon with polygon_in = True is a hole
                        and thus the count should take these points as NOT
                        being in the polygons.
                        polygons_in = None
                        polygons_in = [polygon_in1, polygon_in2, ...,
                                       polygon_inN]
                        where:
                        polygon_in = [True, False, ..., True]
    :return: mask of poitns inside polygons (len of xarr and yarr)
    """
    xyarr = np.array(list(zip(xarr, yarr)))
    falsearray = np.array([False] * len(xarr), dtype=bool)
    insideany = falsearray.copy()
    for k in range(len(polygons)):
        polygon = polygons[k]
        # +++++++++++++++++++++++++++++++++++++++++++++
        # deal with annoying contained polygons
        if polygons_in is None:
            polygon_in = None
        else:
            polygon_in = polygons_in[k]
        # +++++++++++++++++++++++++++++++++++++++++++++
        for j in range(len(polygon)):
            poly = polygon[j]
            # mask out the points outside the poly clip box
            pmax_x, pmax_y = np.max(poly, axis=0)
            pmin_x, pmin_y = np.min(poly, axis=0)
            mask1 = (xarr > pmin_x) & (xarr < pmax_x)
            mask2 = (yarr > pmin_y) & (yarr < pmax_y)
            mask = mask1 & mask2
            # if no points inside poly clip box then don't bother counting
            if np.sum(mask) == 0:
                continue
            # -----------------------------------------------------------------
            # deal with annoying contained polygons
            if polygon_in is None:
                poly_in = False
            else:
                poly_in = polygon_in[j]
            # -----------------------------------------------------------------
            # Creates a mask for points (xs, ys) based on whether they are
            # inside a polygon poly from http://stackoverflow.com/a/23453678
            if not poly_in:
                bbPath = mplPath.Path(poly)
                inside = falsearray.copy()
                inside[mask] = bbPath.contains_points(xyarr[mask])
                # --------------------------------------------------------------
                # if polygon is inside another polygon (as defined by poly_in)
                # do not count it as inside
                insideany |= inside
            # -----------------------------------------------------------------
    return insideany


# =============================================================================
# Start of code
# =============================================================================
# Main code here
if __name__ == "__main__":
    # ----------------------------------------------------------------------
    # Code here
    # ----------------------------------------------------------------------
    pass

# =============================================================================
# End of code
# =============================================================================
