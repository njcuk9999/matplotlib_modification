"""
Taken and edited from
http://www.baryons.org/RelatedTicker/

"""


from matplotlib.ticker import Locator,Base
import numpy as np

class RelatedLocator(Locator):
	"""
	Intended for mirrored axes.  Sets tick locations for an axes to be in multiples of a transformed coordinate system.
	"""
	_transform_func = ''	# the function to transform the first axis to the second
	_base = ''		# a ticker.base object for calculating multiples of the base

	def __init__( self, transform_func, base=1.0 ):

		self._transform_func = transform_func
		self._base = Base( base )

	def __call__( self ):

		'Return the locations of the ticks'
		amin, amax = self.axis.get_view_interval()
		if amax < amin:
			amin, amax = amax, amin
		if amin < 0:
			amin = 0

		# translate current axis to transformed coordinates
		( tmax, tmin ) = ( self.transform( amin ), self.transform( amax ) )
		if tmax < tmin:
			tmin, tmax = tmax, tmin

		# now figure out tick locations in transformed space (stolen from matplotlib.ticker.MultipleLocator)
		tmin = self._base.ge(tmin)
		base = self._base.get_base()
		n = (tmax - tmin + 0.001*base)//base
		t_locs = tmin + np.arange(n+1) * base

		# now we have to convert those back to original coordinate space
		# use interpolate so we don't need a back conversion
		xs = np.linspace( amin, amax, 100 )
		ts = np.asarray( [ self.transform( x ) for x in xs ] )
		# make sure to sort before interpolating
		sinds = ts.argsort()
		locs = np.interp( t_locs, ts[sinds], xs[sinds] )
		locs.sort()

		return self.raise_if_exceeds( locs.tolist() )

	def transform( self, vals ):
		return self._transform_func( vals )