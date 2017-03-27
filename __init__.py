from . import RelatedFormatter
from . import RelatedLocator
from . import rainbow_text
from . import right_ascension_axis

__author__ = "Neil Cook"
__email__ = 'neil.james.cook@gmail.com'
__version__ = '0.1'
__all__ = ['Formatter', 'Locator', 'TimeFormatter', 'RainbowText',
           'RightAscensionAxis']

Formatter = RelatedFormatter.RelatedFormatter
Locator = RelatedLocator.RelatedLocator
TimeFormatter = RelatedFormatter.TimeFormatter
RainbowText = rainbow_text.rtext
RightAscensionAxis = right_ascension_axis.ra_axis