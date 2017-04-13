#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 13/04/17 at 12:34 PM

@author: neil

Program description here

Version 0.0.0
"""

import matplotlib.pyplot as plt
from .core import add_xy_hists as XYHist
from matplotlib.patches import Ellipse
import numpy as np


# =============================================================================
# Define variables
# =============================================================================


# -----------------------------------------------------------------------------



# =============================================================================
# Define functions
# =============================================================================
def test_2d_dist_for_gauss(xdata, ydata, x50=None, y50=None, ex=None, ey=None,
                           **kwargs):
    """
    Plots a scatter plot of x vs y and compares distribution to a gaussian
    (with histograms for x and y axis)

    :param xdata: numpy array of float, the x axis data

    :param ydata: numpy array of float, the y axis data

    :param x50: float or None, the 50th percentile (median) x value, if None
                calculated from xdata using np.median(xdata)

    :param y50: float or None, the 50th percentile (median) y value, if None
                calculated from ydata using np.median(ydata)

    :param ex: float or None, the standard deviation (1 sigma) of the x data, if
               calcualted from xdata using np.std(xdata)

    :param ey: float or None, the standard deviation (1 sigma) of the y data, if
               calcualted from xdata using np.std(ydata)

    :param kwargs: key word arguments for plot

    :return:
    """
    # --------------------------------------------------------------------------
    G = np.array([xdata, ydata]).T
    if x50 is None:
        x = np.median(xdata)
    else:
        x = x50
    if y50 is None:
        y = np.median(ydata)
    else:
        y = y50
    if ex is None:
        ex = np.std(xdata)
    if ey is None:
        ey = np.std(ydata)
    # --------------------------------------------------------------------------
    # Load keyword args
    xlabel = kwargs.get('xlabel', 'X')
    ylabel = kwargs.get('ylabel', 'Y')

    # scatter plot
    scatterpoints_color = kwargs.get('scatterpointscolor', 'k')
    scatterpoint_size = kwargs.get('scatterpointsize', 3)
    scatterkwargs = dict(color=scatterpoints_color, s=scatterpoint_size)
    # 1 sigma lines
    onesigma_plot = kwargs.get('onesigma_plot', True)
    onesigma_color = kwargs.get('onesigma_color', 'g')
    onesigma_linestyle = kwargs.get('onesigma_linestyle', '--')
    onesigma_linewidth = kwargs.get('onesigma_linewidth', 0.5)
    onesigmakwargs = dict(color=onesigma_color, linestyle=onesigma_linestyle,
                          linewidth=onesigma_linewidth, zorder=5)
    # sigma ellipses
    ellipses_plot = kwargs.get('ellipses_plot', True)
    ellipses_sigma = kwargs.get('ellipses_sigma', [1, 2, 3])
    ellipses_colors = kwargs.get('ellipses_colors', ['red', 'magenta', 'orange'])
    ellipses_linestyle = kwargs.get('ellipses_linestyle', '--')
    ellipses_linewidth = kwargs.get('ellipses_linewidth', 0.5)

    # --------------------------------------------------------------------------
    # len of data
    num = len(G)
    # set up plots
    plt.close()
    shape = (5, 5)
    frame = plt.subplot2grid(shape, (0, 1), rowspan=4, colspan=4)
    frame1 = plt.subplot2grid(shape, (0, 0), rowspan=4, colspan=1)
    frame2 = plt.subplot2grid(shape, (4, 1), rowspan=1, colspan=4)
    # add proper motion scatter plot
    frame.scatter(G[:, 0], G[:, 1], **scatterkwargs)
    # add median and 1 sigma lines
    if onesigma_plot:
        frame.axhline(y, **onesigmakwargs)
        frame.axhline(y + ey, **onesigmakwargs)
        frame.axhline(y - ey, **onesigmakwargs)
        frame.axvline(x, **onesigmakwargs)
        frame.axvline(x + ex, **onesigmakwargs)
        frame.axvline(x - ex, **onesigmakwargs)
    frame.grid(False)
    # plot 1 sigma, 2 sigma, and 3 sigma ellipses
    if ellipses_plot:
        ellipse = [Ellipse(xy=(x, y), width=ii*ex*2, height=ii*ey*2)
                   for ii in ellipses_sigma]
        for ei, e in enumerate(ellipse):
            frame.add_artist(e)
            e.set_facecolor('None')
            e.set_edgecolor(ellipses_colors[ei])
            e.set_linestyle(ellipses_linestyle)
            e.set_linewidth(ellipses_linewidth)
    # set up title
    targs = [xlabel, x, '$\pm$', ex, ylabel, y, ey, num]
    frame.set(title='{0}={1:.3f}{2}{3:.3f}, '
                    '{4}={5:.3f}{2}{6:.3f}, N={7}\n'.format(*targs),
              xticklabels=[], yticklabels=[])
    # add histogram plots to sides
    frame1, frame2 = XYHist(G[:, 0], G[:, 1], frame, frame1, frame2,
                            bins=50, plot_gauss_fit=True, plot_grid=False)
    # set up y histogram
    frame1.set_ylabel(ylabel)
    if onesigma_plot:
        frame1.axhline(y, **onesigmakwargs)
        frame1.axhline(y + ey, **onesigmakwargs)
        frame1.axhline(y - ey, **onesigmakwargs)
    # set up x histogram
    frame2.set_xlabel(xlabel)
    if onesigma_plot:
        frame2.axvline(x, **onesigmakwargs)
        frame2.axvline(x + ex, **onesigmakwargs)
        frame2.axvline(x - ex, **onesigmakwargs)
    # show and close
    plt.subplots_adjust(hspace=0, wspace=0)
    plt.show()
    plt.close()

# =============================================================================
# Start of code
# =============================================================================
if __name__ == "__main__":

    # set up parameters
    x50, y50 = 40.0, 30.0
    ex, ey = 2.1, 4.3
    num = 512
    # make test data
    means = [x50, y50]
    cov = np.array([[ex**2, 0], [0, ey**2]])
    G = np.random.multivariate_normal(means, cov, num)
    # plot
    kwargs = dict(xlabel='X data', ylabel='Y data')
    test_2d_dist_for_gauss(G[:, 0], G[:, 1], x50=x50, y50=y50, ex=ex, ey=ey,
                               **kwargs)

# =============================================================================
# End of code
# =============================================================================
