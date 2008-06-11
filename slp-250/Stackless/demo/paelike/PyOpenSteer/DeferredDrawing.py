"""
----------------------------------------------------------------------------

OpenSteer -- Steering Behaviors for Autonomous Characters

Copyright (c) 2002-2003, Sony Computer Entertainment America
Original author: Craig Reynolds <craig_reynolds@playstation.sony.com>

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.


----------------------------------------------------------------------------

PyOpenSteer -- Port of OpenSteer to Python

Copyright (c) 2004 Lutz Paelike <lutz@fxcenter.de>

The license follows the original Opensteer license but must include 
this additional copyright notice.
----------------------------------------------------------------------------
"""

import vector
from vector import vec3

index = 0
# lutz:
# is not really necessary to have a size limit in python
# as the list can dynamically grow
# we leave it for the moment to keep a maximum limit of deferred operations

# Deferred operations (like drawing) would be a perfect candidate for stackless python
size = 2000
deferredGraphicsArray = []

class DeferredLine:
	startPoint = vec3()
	endPoint = vec3()
	color = vec3()

class DeferredCircle:
	radius = 1.0
	axis=vec3()
	center=vec3()
	color=vec3()
	segments = 0
	filled = True
	in3d = True
    
def addDeferredLineToBuffer (s,e,c):
	global index, deferredLineArray, size
	if (index < size):
		deferredGraphicsArray[index] = DeferredLine()
		deferredGraphicsArray[index].startPoint = s
		deferredGraphicsArray[index].endPoint = e
		deferredGraphicsArray[index].color = c
		index+=1
	else:
		SteerTest.printWarning ("overflow in deferredDrawLine buffer")

def addDeferredCircleToBuffer(radius, axis, center, color,segments, filled, in3d):
	if (index < size):
		deferredGraphicsArray[index] = DeferredCircle()
		deferredGraphicsArray[index].radius   = radius
		deferredGraphicsArray[index].axis     = axis
		deferredGraphicsArray[index].center   = center
		deferredGraphicsArray[index].color    = color
		deferredGraphicsArray[index].segments = segments
		deferredGraphicsArray[index].filled   = filled
		deferredGraphicsArray[index].in3d     = in3d
		index+=1
	else:
		SteerTest.printWarning("overflow in deferredDrawCircle buffer")


def drawAll():
	"""draw all lines in the buffer"""
	global index, deferredLineArray
	for i in range(index):
		dg = deferredGraphicsArray[i]
		if isinstance(dg,DeferredLine):
			iDrawLine(dg.startPoint, dg.endPoint, dg.color)
		elif isinstance(dg,DeferredCircle):
			drawCircleOrDisk (dg.radius, dg.axis, dg.center, dg.color, dg.segments, dg.filled, dg.in3d)
		# reset buffer index
		index = 0
	
drawAllDeferredLines = drawAll
drawAllDeferredCirclesOrDisks = drawAll

deferredDrawLine = addDeferredLineToBuffer