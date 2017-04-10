# Cook et al. 2017 - Matplotlib moficatoions

This is a work in progress - program dump.

All code should be taken as work in progress.

Comments/Problems email neil.james.cook@gmail.com

## Related Formatter

Taken and edited from http://www.baryons.org/RelatedTicker/

Additions: TimeFormatter function

  ### class TimeFormatter(Formatter):
        takes transformation function and time format string and converts
        axis to time formatted axis
        
        the transformation function must return the time in decimal hours
        
        Formats currently allowed:
        
            "H"       format is 16h
            "H.H"     format is 16.1h
            "H.HH"    format is 16.12
            "HM"      format is 16h 7m
            "HM.M"    format is 16h 7.4m
            "HM.MM"   format is 16h 7.41m
            "HMS"     format is 16h 7m 24s
            "HMS.S"   format is 16h 7m 24.4s
            "HMS.SS"  format is 16h 7m 24.44s

  #### Example use
  
      import matplotlib.pyplot as plt
      from .RelatedFormatter import TimeFormatter as TimeFormatter
      from .RelatedLocator import RelatedLocator as Locator

      def deg_to_hours(x):
        """
        Converts degress in to hours for right ascension
        x [deg] = x*24.0/360.0 = x/15.0
        :param x: right ascension position in degrees
        :return x/15.0: right ascnesion position in hours
        """
        return x/15.0

      fig, ax = plt.subplots(ncols=1, nrows=1)
      ax.scatter([0, 90, 180, 270, 360], [-10, -12, -10, -12, -10])
      xax = ax.xaxis
      xax.set_major_locator(Locator(deg_to_hours, 0.25))
      xax.set_major_formatter(TimeFormatter(deg_to_hours, "HMS"))
      ax.set(xlabel="Right Ascension", ylabel="Declination")
      plt.show()
      plt.close()
 
  ## Related Locator
  
  Taken from http://www.baryons.org/RelatedTicker/   (Unedited but here for ease of use)
  
  
  ## Right Asencion Axis
  
  ### ra_axis(frame, axis_format='HMS.SS')
  
  Converts the right ascension axis from degrees into hours/hours minutes/
    hours/minutes/seconds
    :param frame: matplotlib axis (ax), i.e. plt.subplot(111) plt.gca()
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

  #### Example of use
  
    import numpy as np
    import matplotlib.pyplot as plt

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
  
  ## Rainbow text
  
  Extended version of http://matplotlib.org/examples/text_labels_and_annotations/rainbow_text.html
  
  ### rtext(x, y, strings, colors, ax=None, orientation='horizontal', **kw)
  
    Take a list of ``strings`` and ``colors`` and place them next to each
    other, with text strings[i] being shown in colors[i].
    This example shows how to do both vertical and horizontal text, and will
    pass all keyword arguments to plt.text, so you can set the font size,
    family, etc.
    The text will get added to the ``ax`` axes, if provided, otherwise the
    currently active axes will be used.
    from:
    http://matplotlib.org/examples/text_labels_and_annotations/rainbow_text.html
    :param x: float, location on the plot (see plt.text)
    :param y: float, location on the plot (see plt.text)
    :param strings: list of strings, containing the words to color
    :param colors: list of strings, containing the colour of each word
    :param ax: plt.gca() axis or frame
    :param orientation: string, "h"/"horizontal" or "v"/"vertical"
    :param kw: dictionary, keyword arguments to be passed to plt.text
    :return:
    
    
