#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 27/03/17 at 3:47 PM

@author: neil

Program description here

Version 0.0.0
"""

from .RelatedFormatter import TimeFormatter as TimeFormatter
from .RelatedLocator import RelatedLocator as Locator
from matplotlib.ticker import MultipleLocator

# =============================================================================
# Define variables
# =============================================================================
def deg_to_hours(x):
    """
    Converts degress in to hours for right ascension

    x [deg] = x*24.0/360.0 = x/15.0

    :param x: right ascension position in degrees
    :return x/15.0: right ascnesion position in hours
    """
    return x/15.0


def ra_axis(frame, axis_format='HMS.SS'):
    """
    Converts the right ascension axis from degrees into hours/hours minutes/
    hours/minutes/seconds

    :param frame: matplotlib axis, i.e. plt.subplot(111) plt.gca()
    :param axis_format: string, format of the ra_axis currently supported are:

    For ra = 241.85184 degrees

            "H"       format is 16h
            "H.H"     format is 16.1h
            "H.HH"    format is 16.12
            "HM"      format is 16h 7m
            "HM.M"    format is 16h 7.4m
            "HM.MM"   format is 16h 7.41m
            "HMS"     format is 16h 7m 24s
            "HMS.S"   format is 16h 7m 24.4s
            "HMS.SS"  format is 16h 7m 24.44s

    default is "HMS.SS"

    :return:
    """
    if axis_format == 'H':
        kind = '{0:.0f}h'
    elif axis_format == 'H.H':
        kind = '{0:.1f}h'
    elif axis_format == 'H.HH':
        kind = '{0:.2f}h'
    elif axis_format == 'HM':
        kind = '{0:.0f}h {1:.0f}m'
    elif axis_format == 'HM.M':
        kind = '{0:.0f}h {1:.1f}m'
    elif axis_format == 'HM.MM':
        kind = '{0:.0f}h {1:.2f}m'
    elif axis_format == 'HMS':
        kind = '{0:.0f}h {1:.0f}m {2:.0f}s'
    elif axis_format == 'HMS.S':
        kind = '{0:.0f}h {1:.0f}m {2:.1f}s'
    else:
        kind = '{0:.0f}h {1:.0f}m {2:.2f}s'

    # flip the x axis
    frame.set_xlim(frame.get_xlim()[::-1])
    # format x axis to be in hours and minutes separated by 0.25 hours
    xax = frame.xaxis
    xax.set_major_locator(Locator(deg_to_hours, 0.25))
    xax.set_major_formatter(TimeFormatter(deg_to_hours, kind))
    # add minor ticks at 5 min intervals on x axis
    xax.set_minor_locator(Locator(deg_to_hours, 5.0/60))
    # add minor ticks to the y axis
    frame.yaxis.set_minor_locator(MultipleLocator(0.5))
    return frame




# =============================================================================
# Define functions
# =============================================================================



# =============================================================================
# Start of code
# =============================================================================
# Main code here
if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    # ----------------------------------------------------------------------
    # make fake data
    ra = np.random.randint(2300000, 2500000, 1000)
    dec = np.random.randint(250000, 350000, 1000)
    ra = np.array(ra, dtype=float)/10000
    dec = np.array(dec, dtype=float)/10000
    # plot data
    plt.close()
    fig, frame = plt.subplots(ncols=1, nrows=1)
    frame.scatter(ra, dec)
    # change x-axis
    frame = ra_axis(frame)
    # set labels
    frame.set_xlabel('Right Ascension')
    frame.set_ylabel('Declination')
    # show and close
    plt.show()
    plt.close()




# =============================================================================
# End of code
# =============================================================================
