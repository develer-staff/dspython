import math,random

M_PI = math.pi

# copied from the c include
# don't know if this is correct
MAXFLOAT = 3.402823466e+38

def interpolate (alpha, x0, x1):
	return x0 + ((x1 - x0) * alpha)

frandom01 = random.random


def frandom2 (lowerBound, upperBound):
	random.uniform()

def clip (x, min, max):
	"""
	Constrain a given value (x) to be between two (ordered) bounds: min
	and max.  Returns x if it is between the bounds, otherwise returns
	the nearer bound
	"""
	if (x < min): return min
	if (x > max): return max
	return x


def remapInterval( x, in0, in1, out0, out1):
	"""
	remap a value specified relative to a pair of bounding values
	to the corresponding value relative to another pair of bounds.
	"""
	
	# uninterpolate: what is x relative to the interval in0:in1?
	relative = (x - in0) / (in1 - in0)
	
	# now interpolate between output interval based on relative x
	return interpolate(relative, out0, out1)

def remapIntervalClip( x, in0, in1, out0, out1):
	"""
	Like remapInterval but the result is clipped to remain between
	out0 and out1
	"""
	
	# uninterpolate: what is x relative to the interval in0:in1?
	relative = (x - in0) / (in1 - in0)
	
	# now interpolate between output interval based on relative x
	return interpolate (clip (relative, 0, 1), out0, out1)


def intervalComparison(x, lowerBound, upperBound):
	"""
	classify a value relative to the interval between two bounds:
	returns -1 when below the lower bound
	returns  0 when between the bounds (inside the interval)
	returns +1 when above the upper bound
	"""
	if (x < lowerBound): return -1
	if (x > upperBound): return 1
	return 0


def scalarRandomWalk(initial, walkspeed, min, max):
	next = initial + (((frandom01() * 2) - 1) * walkspeed)
	if (next < min): return min
	if (next > max): return max
	return next


def square(x):
	return x*x

#################################### Accumulator

class Accumulator(object):
	def __init__(self,initialvalue=0):
		self.set(initialvalue)
	def accumulate(self,value):
		self._value += value
		
	def set(self,val):
		self._value = val
		
	def get(self):
		return self._value
		

def blendIntoAccumulator(smoothRate, newValue, smoothedAccumulator):
	"""
	blends new values into an accumulator to produce a smoothed time series
	
	Modifies its third argument, a reference to the float accumulator holding
	the "smoothed time series."
	
	The first argument (smoothRate) is typically made proportional to "dt" the
	simulation time step.  If smoothRate is 0 the accumulator will not change,
	if smoothRate is 1 the accumulator will be set to the new value with no
	smoothing.  Useful values are "near zero".
	
	Usage:
			blendIntoAccumulator (dt * 0.4f, currentFPS, smoothedFPS);
	"""        

	#This is just plain wrong
	#rework this the python way
	pass
	#smoothedAccumulator.set(interpolate(clip(smoothRate, 0, 1), smoothedAccumulator.get(), newValue)
	