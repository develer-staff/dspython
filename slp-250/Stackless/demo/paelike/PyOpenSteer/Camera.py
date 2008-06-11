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
import vector
import LocalSpace

class Camera(LocalSpace.LocalSpace):
	def __init__(self):
		self.reset()

	def modeName(self):
		"""string naming current camera mode, used by SteerTest"""
		pass
	def reset(self):
		"""reset all camera state to default values"""
		# reset camera's position and orientation
		self.resetLocalSpace()
		
		# "look at" point, center of view
		self.target = vec3(0.0)    
		# vehicle being tracked
		self.vehicleToTrack = None
		    
		# aim at predicted position of vehicleToTrack, this far into thefuture
		self.aimLeadTime = 1.0
		
		# make first update abrupt
		self.smoothNextMove = False
		
		# relative rate at which camera transitions proceed
		self.smoothMoveSpeed = 1.5
		
		# select camera aiming mode
		self.mode = cmFixed
		
		# "constant distance from vehicle" camera mode parameters
		self.fixedDistDistance = 1.0
		self.fixedDistVOffset = 0.0
		
		# "look straight down at vehicle" camera mode parameters
		self.lookdownDistance = 30
		
		# "static" camera mode parameters
		self.fixedPosition = vec3(75.0, 75.0, 75.0)
		self.fixedTarget = vec3(0.0)
		self.fixedUp = vec3(vector.up)
	
		# "fixed local offset" camera mode parameters
		self.fixedLocalOffset = vec3(5.0, 5.0, -5.0)
		
		# "offset POV" camera mode parameters
		self.povOffset = vec3(0.0, 1.0, -3.0)
	
	def update(self,currentTime,elapsedTime,simulationPaused=False):
		"""per frame simulation update"""
		pass
	
	def constDistHelper(self,elapsedTime):
		"""helper function for "drag behind" mode"""
		pass
	
	def smoothCameraMove(self, newPosition, newTarget, newUp,elapsedTime):
		"""Smoothly move camera ..."""
		pass
	
	def doNotSmoothNextMove(self):
		""" """
		self.smoothNextMove = False
	
	def smoothNextMove(self):
		""" """
		pass
	
	def smoothMoveSpeed(self):
		""" """
		pass
	
	def mouseAdjustOffset(self):
		""" """
		pass
	
	def mouseAdjust2(self):
		""" """
		pass
	
	def mouseAdjustPolar(self):
		""" """
		pass
	
	def mouseAdjustOrtho(self):
		""" """
		pass
	
	def selectNextMode(self):
		"""select next camera mode, used by SteerTest"""
		pass
	
	def successorMode(self):
		"""the mode that comes after the given mode (used by selectNextMode)"""
		pass
	



def xxxls(self):
	"""
	# xxx since currently (10-21-02) the camera's Forward and Side basis
	# xxx vectors are not being set, construct a temporary local space for
	# xxx the camera view -- so as not to make the camera behave
	# xxx differently (which is to say, correctly) during mouse adjustment.
	"""
	return LocalSpace.LocalSpace().regenerateOrthonormalBasis (target - position(), up())


# marks beginning of list
cmStartMode = 0

# fixed global position and aimpoint
cmFixed = 1

# camera position is directly above (in global Up/Y) target
# camera up direction is target's forward direction
cmStraightDown = 2

# look at subject vehicle, adjusting camera position to be a
# constant distance from the subject
cmFixedDistanceOffset = 3

# camera looks at subject vehicle from a fixed offset in the
# local space of the vehicle (as if attached to the vehicle)
cmFixedLocalOffset = 4

# camera looks in the vehicle's forward direction, camera
# position has a fixed local offset from the vehicle.
cmOffsetPOV = 5

# cmFixedPositionTracking # xxx maybe?

# marks the end of the list for cycling (to cmStartMode+1)
cmEndMode = 6
