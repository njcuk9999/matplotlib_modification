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

    def __init__(self, transform_func, format='%.0f'):
        self._transform_func = transform_func
        self._format = format

    def __call__(self, a, pos=None):
        t = self.transform(a)
        t1 = self.check_for_time(t)
        if pos is not None:
            return self._format.format(*t1)
        else:
            return str(t)

    def transform(self, vals):
        return self._transform_func(vals)

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
