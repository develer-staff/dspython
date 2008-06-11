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

from vector import vec3

class AbstractLocalSpace:
	def __init__(self):
		pass
	def side(self):
		""" """
		pass
	
	def setSide(self):
		""" """
		pass
	
	def up(self):
		""" """
		pass
	
	def setUp(self,u):
		""" """
		pass
	
	def forward(self):
		""" """
		pass
	
	def setForward(self,f):
		""" """
		pass
	
	def position(self):
		""" """
		pass
	
	def setPosition(self,p):
		""" """
		pass
	
	def rightHanded(self):
		""" """
		pass
	
	def resetLocalSpace(self):
		""" """
		pass
	
	def localizeDirection(self,globalDirection):
		""" """
		pass
	
	def localizePosition(self,globalPosition):
		""" """
		pass
	
	def globalizePosition(self,localPosition):
		""" """
		pass
	
	def globalizeDirection(self,localDirection):
		""" """
		pass
	
	def setUnitSideFromForwardAndUp(self):
		""" """
		pass
	
	def regenerateOrthonormalBasisUF(self,newUnitForward):
		""" """
		pass

	
	def regenerateOrthonormalBasis(self,newForward,newUp=None):
		""" """
		pass
	
	def localRotateForwardToSide(self,v):
		""" """
		pass
	
	def globalRotateForwardToSide(self,globalForward):
		""" """
		pass

class LocalSpaceMixin:
	def __init__(self, Side=None, Up=None, Forward=None,Position=None):
			
		# upward-pointing unit basis vector
		if Up:
			self._up = Up
		else:
			self._up = vec3()
			
		# forward-pointing unit basis vector
		if Forward:
			self._forward =Forward
		else:
			self._forward = vec3()

		# origin of local space
		if Position:
			self._position = Position
		else:
			self._position = vec3()

		# side-pointing unit basis vector
		if Side:
			self._side = Side
		else:
			self._side = vec3()
			self.setUnitSideFromForwardAndUp()

		if (not Side) & (not Up) & (not Forward) & (not Position):
			self.resetLocalSpace()
			
	def side(self):
		""" """
		return self._side
		
	def up(self):
		""" """
		return self._up
		
	def forward(self):
		""" """
		return self._forward
		
	def position(self):
		""" """
		return self._position
		
	def setSide(self,s):
		""" """
		_side=s
		return s
		
	def setUp(self,u):
		""" """
		_up=u
		return u
		
	def setForward(self,f):
		""" """
		_forward=f	
		return f
		
	def setPosition(self,p):
		""" """
		_position=p
		return p
	
	def rightHanded(self):
		""" 
		switch to control handedness/chirality: should
		LocalSpace use a left- or right-handed coordinate system?  This can be
		overloaded in derived types (e.g. vehicles) to change handedness.
		"""
		return true

class LocalSpace(AbstractLocalSpace, LocalSpaceMixin):
	def __init__(self):
		AbstractLocalSpace.__init__(self)
		LocalSpaceMixin.__init__(self)


gGlobalSpace = LocalSpace()



