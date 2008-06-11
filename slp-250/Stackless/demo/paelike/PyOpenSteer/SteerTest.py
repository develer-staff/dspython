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

import sys
import cgtypes

from Clock import *
from Camera import *
from PlugIn import PlugIn
from AbstractVehicle import *

import Utilities
import ColorDefs

from DeferredDrawing import *
##### constants

DRAWPHASE = 2
UPDATEPHASE = 1
OVERHEADPHASE = 0


##### global vars (module level)

mouseX = 0
mouseY = 0
mouseInWindow = False

# some camera-related default constants
camera2dElevation = 8.0
cameraTargetDistance = 13.0
cameraTargetOffset = cgtypes.vec3(0.0,cameraTargetDistance,0.0)


##########  SteerTest phase

phaseStack = [0,0,0,0,0]
phaseStackSize = 5
phaseStackIndex = 0

# list of floats
phaseTimers = [0.0,0.0,0.0,0.0]
# list of floats
phaseTimerBase = 0.0



# keeps track of both "real time" and "simulation time"
clock = Clock()

# camera automatically tracks selected vehicle
camera = Camera()

# currently selected plug-in (user can choose or cycle through them)
selectedPlugIn = None

# currently selected vehicle.  Generally the one the camera follows and
# for which additional information may be displayed.  Clicking the mouse
# near a vehicle causes it to become the Selected Vehicle.
selectedVehicle = None
phase = OVERHEADPHASE
enableAnnotation = True


gDelayedResetPlugInXXX = False

def printPlugIn(plugin):
	print str(plugin)


def initialize():
	global selectedVehicle, phase, enableAnnotation, selectedPlugIn
	# list of ints


def updateSimulationAndRedraw():
	"""main update function: step simulation forward and redraw scene"""
	# update global simulation clock
	clock.update ()
	
	#  start the phase timer (XXX to accurately measure "overhead" time this
	#  should be in displayFunc, or somehow account for time outside this
	#  routine)
	initPhaseTimers()
	
	# run selected PlugIn (with simulation's current time and step size)
	updateSelectedPlugIn(clock.totalSimulationTime, clock.elapsedSimulationTime)
	                      
	# redraw selected PlugIn (based on real time)
	redrawSelectedPlugIn(clock.totalRealTime, clock.elapsedRealTime)

def errorExit(message):
	"""exit SteerTest with a given text message or error code"""
	print message
	sys.exit(10)

def exit(exitCode):
	"""just exit SteerTest"""
	sys.exit(exitCode)

##########  PlugIn interface ###########

def selectDefaultPlugIn():
	"""select the default PlugIn """
	PlugIn.sortBySelectionOrder()
	selectedPlugIn = PlugIn.findDefault();
	
def selectNextPlugIn():
	""" select the "next" plug-in, cycling through "plug-in selection order" """
	closeSelectedPlugIn()
	selectedPlugIn = selectedPlugIn.next()
	openSelectedPlugIn()
	
def functionKeyForPlugIn(keyNumber):
	"""handle function keys an a per-plug-in basis"""
	selectedPlugIn.handleFunctionKeys(keyNumber)

def nameOfSelectedPlugIn():
	""" return name of currently selected plug-in (string) """
	if selectedPlugIn:
		return selectedPlugIn.name()
	else:
		return "no PlugIn"

def openSelectedPlugIn():
	"""open the currently selected plug-in"""
	camera.reset()
	selectedVehicle = None
	selectedPlugIn.open()
	
def updateSelectedPlugIn(currentTime,elapsedTime):
	"""do a simulation update for the currently selected plug-in"""
	global selectedVehicle,selectedPlugIn,UPDATEPHASE
	#switch to Update phase
	pushPhase(UPDATEPHASE);

	# service queued reset request, if any
	doDelayedResetPlugInXXX()
	
	# if no vehicle is selected, and some exist, select the first one
	if (selectedVehicle == None):
		vehicles = allVehiclesOfSelectedPlugIn()
		if (vehicles):
			if(len(vehicles) > 0): 
				selectedVehicle = vehicles[0]
		
		
	# invoke selected PlugIn's Update method
	if selectedPlugIn:
		selectedPlugIn.update(currentTime, elapsedTime)
	
	# return to previous phase
	popPhase()

def redrawSelectedPlugIn(currentTime,elapsedTime):
	"""redraw graphics for the currently selected plug-in"""
	global selectedPlugIn, DRAWPHASE
	# switch to Draw phase
	pushPhase(DRAWPHASE)
	
	# invoke selected PlugIn's Draw method
	if selectedPlugIn: selectedPlugIn.redraw(currentTime, elapsedTime)
	
	# draw any annotation queued up during selected PlugIn's Update method
	drawAllDeferredLines()
	drawAllDeferredCirclesOrDisks ()
	
	# return to previous phase
	popPhase()

def closeSelectedPlugIn():
	"""close the currently selected plug-in"""
	global selectedPlugIn,selectedVehicle
	selectedPlugIn.close()
	selectedVehicle = None

def resetSelectedPlugIn():
	"""reset the currently selected plug-in"""
	selectedPlugIn.reset()

def queueDelayedResetPlugInXXX():
	global gDelayedResetPlugInXXX
	gDelayedResetPlugInXXX = True


def doDelayedResetPlugInXXX():
	global gDelayedResetPlugInXXX
	if (gDelayedResetPlugInXXX):
		resetSelectedPlugIn ()
		gDelayedResetPlugInXXX = False


def allVehiclesOfSelectedPlugIn():
	"""returns list object with a list of all Vehicles driven by the currently selected PlugIn"""
	global selectedPlugIn
	if selectedPlugIn:
		return selectedPlugIn.allVehicles()
	else:
		return None


def phaseIsDraw():
	""" """
	pass

def phaseIsUpdate():
	""" """
	pass

def phaseIsOverhead():
	""" """
	pass

def phaseTimerDraw():
	""" """
	pass

def phaseTimerUpdate():
	""" """
	pass

def phaseTimerOverhead():
	""" """
	pass

#################  delayed reset XXX

def queueDelayedResetPlugInXXX():
	""" """
	pass

def doDelayedResetPlugInXXX():
	""" """
	pass

#################  vehicle selection

def selectNextVehicle():
	""" """
	global selectedVehicle
	if (selectedVehicle):
		# get a container of all vehicles
		all = allVehiclesOfSelectedPlugIn ()
		first = all[0]
		last = all[-1]
		
		found = False
		for i, item in enumerate(all):
			if item == selectedVehicle:
				found = True
				if i+1<len(all):
					selectedVehicle = all[i+1]
					break
				elif (i+1)==len(all):
					selectedVehicle = all[0]
		if not found: selectedVehicle = None



def selectVehicleNearestScreenPosition():
	""" """
	global selectedVehicle
	selectedVehicle = findVehicleNearestScreenPosition(x, y)

#################  mouse support

def vehicleNearestToMouse():
	"""
	Find the AbstractVehicle whose screen position is nearest the current the
	mouse position.  Returns None if mouse is outside this window or if
	there are no AbstractVehicle.
	"""
	global mouseInWindow
	if mouseInWindow:
		return findVehicleNearestScreenPosition (mouseX, mouseY)
	else:
		return None

def findVehicleNearestScreenPosition(x,y):
	"""
	Find the AbstractVehicle whose screen position is nearest the
    given window coordinates, typically the mouse position.  Note
    this will return None if there are no AbstractVehicles.
	"""
	direction = directionFromCameraToScreenPosition (x, y)
	minDistance = Utilities.MAXFLOAT
	nearest = None
	vehicles = allVehiclesOfSelectedPlugIn()
	for item in vehicles:
		d = distanceFromLine (item.position(), camera.position(), direction)
		
		# if this vehicle-to-line distance is the smallest so far,
		# store it and this vehicle in the selection registers.
		if (d < minDistance):
			minDistance = d
			nearest = item
	return nearest

mouseX = 0
mouseY = 0
mouseInWindow = False

######################## camera utilities


def init2dCamera(selected):
	"""set a certain initial camera state used by several plug-ins (2d)"""
	pass

def init3dCamera(selected):
	"""set a certain initial camera state used by several plug-ins (3d)"""
	position3dCamera(selected)
	
	camera.fixedDistDistance = cameraTargetDistance
	camera.fixedDistVOffset = camera2dElevation
	
	camera.mode = Camera.cmFixedDistanceOffset

def position3dCamera(selected):
	"""set initial position of camera based on a vehicle"""
	global selectedVehicle
	selectedVehicle = selected
	if (selected):
		behind = selected.forward() * -1 * cameraTargetDistance
		camera.setPosition(selected.position() + behind)
		camera.target = selected.position()


def position2dCamera(selected):
	"""set initial position of camera based on a vehicle"""
	# position the camera as if in 3d:
	position3dCamera(selected)
	
	# then adjust for 3d
	position3d = vec3(camera.position())
	position3d.y += camera2dElevation;
	camera.setPosition(position3d)

def updateCamera(currentTime,elapsedTime,selected):
	"""camera updating utility used by several (all?) plug-ins
	   expected types: updateCamera(float,float, AbstractVehicle)
	"""
	global camera,clock
	camera.vehicleToTrack = selected
	camera.update(currentTime, elapsedTime,clock.paused)



##############  graphics and annotation

def initializeGraphics():
	"""do all initialization related to graphics"""
	pass

def gridUtility(gridTarget):
	"""
	ground plane grid-drawing utility used by several plug-ins
	round off target to the nearest multiple of 2 (because the
	checkboard grid with a pitch of 1 tiles with a period of 2)
	then lower the grid a bit to put it under 2d annotation lines
	"""
	gridCenter = vec3(  (round (gridTarget.x * 0.5) * 2),
						(round (gridTarget.y * 0.5) * 2) - 0.05,
						(round (gridTarget.z * 0.5) * 2))
	
	# colors for checkboard
	gray1 = vec3(0.27)
	gray2 = vec3(0.30)
	
	# draw 50x50 checkerboard grid with 50 squares along each side
	drawXZCheckerboardGrid (50, 50, gridCenter, gray1, gray2)
	
	# alternate style
	# drawXZLineGrid (50, 50, gridCenter, black);

def highlightVehicleUtility(vehicle):
	"""draws a gray disk on the XZ plane under a given vehicle"""
	if (vehicle):
		drawXZDisk(vehicle.radius(), vehicle.position(), ColorDefs.gGray60, 20)

def circleHighlightVehicleUtility(vehicle,radiusMultiplier,color):
	"""
	draws a colored circle (perpendicular to view axis) around the center
	of a given vehicle.  The circle's radius is the vehicle's radius times
	radiusMultiplier.
	"""
	global camera
	if (vehicle):
		cPosition = camera.position()
		draw3dCircle(v.radius() * radiusMultiplier,    # adjusted radius
                       v.position(),                   # center
                       v.position() - cPosition,       # view axis
                       color,                          # drawing color
                       20)
def drawBoxHighlightOnVehicle(vehicle,color):
	"""draw a box around a vehicle aligned with its local space"""
	if (vehicle):
		diameter = v.radius() * 2
		size = vec3(diameter, diameter, diameter)
		drawBoxOutline(v, size, color)

def drawCircleHighlightOnVehicle():
	"""draws a colored circle (perpendicular to view axis) around the center
	of a given vehicle.  The circle's radius is the vehicle's radius times
	radiusMultiplier.
	"""
	pass

def annotationIsOn():
	"""graphical annotation: master on/off switch"""
	pass

def setAnnotationOn():
	""" """
	pass

def setAnnotationOff():
	""" """
	pass

def printMessage(message):
	"""print a line on the console with "SteerTest: " then the given ending"""
	print "SteerTest: ", message

def printWarning():
	"""like printMessage but prefix is "SteerTest: Warning: """
	print "SteerTest: Warning: ", message

def keyboardMiniHelp():
	"""print list of known commands"""
	global selectedPlugIn
	help = """
	defined single key commands:
  r      restart current PlugIn.
  s      select next vehicle.
  c      select next camera mode.
  f      select next preset frame rate
  Tab    select next PlugIn.
  a      toggle annotation on/off.
  Space  toggle between Run and Pause.
  ->     step forward one frame.
  Esc    exit.

	"""
	print help
	#allow PlugIn to print mini help for the function keys it handles
	selectedPlugIn.printMiniHelpForFunctionKeys()

def pushPhase(newPhase):
	""" """
	global phaseStack,phaseStackIndex,phase
	# update timer for current (old) phase: add in time since last switch
	updatePhaseTimers()
	
	# save old phase
	phaseStack[phaseStackIndex] = phase
	phaseStackIndex+=1
	# set new phase
	phase = newPhase;
	
	# check for stack overflow
	if (phaseStackIndex >= phaseStackSize): errorExit("phaseStack overflow")

def popPhase():
	""" """
	global phaseStack,phaseStackIndex,phase
	#update timer for current (old) phase: add in time since last switch
	updatePhaseTimers()

	#restore old phase
	phaseStackIndex-=1
	phase = phaseStack[phaseStackIndex]

def initPhaseTimers():
	""" """
	# lutz: changed initialisation behaviour
	global phaseTimers,phaseTimerBase
	phaseTimers = [0.0,0.0,0.0]
	phaseTimerBase = clock.totalRealTime

def updatePhaseTimers():
	""" """
	global clock, phase, phaseTimers,phaseTimerBase
	currentRealTime = clock.realTimeSinceFirstClockUpdate()
	phaseTimers[phase] += currentRealTime - phaseTimerBase
	phaseTimerBase = currentRealTime

