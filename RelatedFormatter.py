"""
Taken and edited from
http://www.baryons.org/RelatedTicker/

"""

from matplotlib.ticker import Formatter


class RelatedFormatter(Formatter):
    """ Formatter for second axis when plotting related axis """

    _transform_func = ''  # function to convert axis to transformed coordinates
    _format = ''  # format string for axis labels

    def __init__(self, transform_func, format='%.0f'):
        self._transform_func = transform_func
        self._format = format

    def __call__(self, a, pos=None):
        t = self.transform(a)
        return self._format % t if pos is not None else '%f' % t

    def transform(self, vals):
        return self._transform_func(vals)


class TimeFormatter(Formatter):
    """ Formatter for second axis when plotting related axis
        Specifically catches a time format
    """

    _transform_func = ''  # function to convert axis to transformed coordinates
    _format = ''  # format string for axis labels

    # Constructor
    def __init__(self, transform_func, format='HMS'):
        """
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
        """
        self._transform_func = transform_func
        self._format = format

    # Call used by matplotlib
    def __call__(self, a, pos=None):
        # transform the data
        t = self.transform(a)
        # convert to time based on format
        t1 = self.check_for_time(t)
        # if we are not dealing with a position do 
        # the transformation and format
        if pos is not None:
            return self._format.format(*t1)
        # else we are dealing with positional data
        # leave this in decimal format
        else:
            return str(t)
    # function to use the transformation function on values
    def transform(self, vals):
        return self._transform_func(vals)

    # function to use the format and return values in correct
    # format
    def check_for_time(self, t):
        cond1 = 'H' in self._format.upper()
        cond2 = 'M' in self._format.upper()
        cond3 = 'S' in self._format.upper()
        if cond1 and cond2 and cond3:
            return self.get_hms(t, return_type='HMS')
        elif cond1 and cond2:
            return self.get_hms(t, return_type='HM')
        elif cond1:
            return self.get_hms(t, return_type='H')
        else:
            return t

    # internal function to calculate Hours Minutes Seconds
    # based on the return type needed
    def get_hms(self, t, return_type='HMS'):
        hours = t // 1
        if return_type == 'HMS':
            minutes = ((t - hours) * 60) // 1
            seconds = (t - hours - minutes / 60) * 3600
            return hours, minutes, seconds
        elif return_type == 'HM':
            minutes = ((t - hours) * 60)
            return hours, minutes
        elif return_type == 'H':
            return hours
        else:
            return t
