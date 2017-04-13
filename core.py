#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 28/03/17 at 10:53 AM

@author: neil

Program description here

Version 0.0.0
"""

import numpy as np
from scipy.optimize import curve_fit

# =============================================================================
# Define variables
# =============================================================================

# -----------------------------------------------------------------------------

# =============================================================================
# Define functions
# =============================================================================
def equal_axis(frame):
    """
    Sets axis equal by comparing the maximum and minimum in both axes

    :param frame: matplotlib axis, i.e. plt.subplot(111)

    :return:
    """
    limits = frame.axis()
    zmin = np.min([limits[0], limits[2]])
    zmax = np.max([limits[1], limits[3]])
    frame.set_xlim(zmin, zmax)
    frame.set_ylim(zmin, zmax)
    return frame


def add_xy_hists(x, y, frame0=None, frame1=None, frame2=None, **kwargs):


    # deal with keyword arguments
    bins = kwargs.get('bins', 100)
    plot_gauss_fit = kwargs.get('plot_gauss_fit', True)
    plot_grid = kwargs.get('plot_grid', True)

    # get limits
    if frame0 is None or frame1 is None or frame2 is None:
        raise ValueError("Must define frames")
    limits = frame0.axis()
    # plot hist
    histy, edgesy = np.histogram(y, bins=bins)
    histx, edgesx = np.histogram(x, bins=bins)
    centersy = edgesy[:-1] + 0.5 * (edgesy[1:] - edgesy[:-1])
    centersx = edgesx[:-1] + 0.5 * (edgesx[1:] - edgesx[:-1])

    frame1.hist(y, bins=bins, orientation='horizontal')
    frame2.hist(x, bins=bins, orientation='vertical')

    if plot_grid:
        frame1.grid(True)
        frame2.grid(True)

    frame1.set_xlim(0)
    frame1.set_ylim(limits[2], limits[3])
    frame1.xaxis.tick_top()
    frame1.xaxis.set_ticks_position('top')
    frame1.xaxis.set_label_position('top')
    frame1 = gaussfit(frame1, histy, centersy, fit='x')

    frame2.set_ylim(0)
    frame2.set_xlim(limits[0], limits[1])
    frame2.yaxis.tick_right()
    frame2.yaxis.set_ticks_position('right')
    frame2.yaxis.set_label_position('right')
    frame2 = gaussfit(frame2, centersx, histx, fit='y')

    return frame1, frame2


def gaussfit(frame, x, y, fit='y'):

    if fit == 'x':
        median, std = np.median(x), np.std(x)
        popt, pcov = curve_fit(__gaussian__, y, x, p0=[1, median, std])
        yfit = np.linspace(y.min(), y.max(), 10000)
        xfit = __gaussian__(yfit, *popt)
    else:
        median, std = np.median(y), np.std(y)
        popt, pcov = curve_fit(__gaussian__, x, y, p0=[1, median, std])
        xfit = np.linspace(x.min(), x.max(), 10000)
        yfit = __gaussian__(xfit, *popt)

    frame.plot(xfit, yfit, color='r')

    return frame


def __gaussian__(x, a, mu, sigma):
    return a*np.exp(-(x-mu)**2/(2*sigma**2))