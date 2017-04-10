from . import RelatedFormatter
from . import RelatedLocator
from . import rainbow_text
from . import right_ascension_axis
from . import core

__author__ = "Neil Cook"
__email__ = 'neil.james.cook@gmail.com'
__version__ = '0.1'
__all__ = ['Formatter', 'Locator', 'TimeFormatter', 'RainbowText',
           'RightAscensionAxis']

# =============================================================================
# Tick functions
# =============================================================================
Formatter = RelatedFormatter.RelatedFormatter
Locator = RelatedLocator.RelatedLocator
TimeFormatter = RelatedFormatter.TimeFormatter
# =============================================================================
# Misc functions
# =============================================================================
RainbowText = rainbow_text.rtext
RightAscensionAxis = right_ascension_axis.ra_axis
# =============================================================================
# Axis functions
# =============================================================================
EqualAxis = core.equal_axis

# =============================================================================
# Specific plot functions
# =============================================================================
XYHist = core.add_xy_hists
