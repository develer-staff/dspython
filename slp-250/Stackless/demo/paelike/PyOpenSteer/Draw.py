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

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from vector import vec3
import vector

import sys

from Utilities import Accumulator

#####################################################
import SteerTest
#####################################################

from ColorDefs import gWhite

# global vars

appVersionName = 'PySteerTest 0.1'

WIN_SCALE = 0.8

# The number of our GLUT window
windowID = 0

gMouseAdjustingCameraAngle = False
gMouseAdjustingCameraRadius = False
gMouseAdjustingCameraLastX = 0
gMouseAdjustingCameraLastY= 0

gSmoothedFPS = Accumulator()
gSmoothedUsage = Accumulator()
gSmoothedTimerDraw = Accumulator()
gSmoothedTimerUpdate =Accumulator()
gSmoothedTimerOverhead = Accumulator()



############# colors ##############

from ColorDefs import *

###############################
def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glCallList(1)
	glutSwapBuffers()

def initGL():
	"""initialize GL mode settings"""
	
	# background = dark gray
	glClearColor(0.3, 0.3, 0.3, 0)
	
	# enable depth buffer clears
	glClearDepth (1.0)
	
	# select smooth shading
	glShadeModel(GL_SMOOTH)
	
	# enable  and select depth test
	glDepthFunc(GL_LESS);
	glEnable(GL_DEPTH_TEST)
	
	# turn on backface culling
	glEnable(GL_CULL_FACE)
	glCullFace(GL_BACK)
	
	# enable blending and set typical "blend into frame buffer" mode
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	
	# reset projection matrix
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()

skipCount =10

def drawDisplayFPS():
	global skipCount
	global gSmoothedFPS
	
	elapsedTime = SteerTest.clock.elapsedRealTime
	if (elapsedTime > 0):
		fps = 1/elapsedTime
	else:
		fps = 0
		
	if (gSmoothedFPS == 0):
		smoothRate = 1
	else:
		smoothRate = (elapsedTime * 0.4)
"""
	
	# skip several frames to allow frame rate to settle
	if (skipCount > 0):
		skipCount-=1
	else:
	    # is there a "fixed frame rate target" or is it as-fast-as-possible?
		targetFrameRate = (SteerTest.clock.targetFPS > 0)
	
	    # "smooth" instantaneous FPS rate: start at current fps the first
	    # time through, then blend fps into a running average thereafter
        blendIntoAccumulator(smoothRate, fps, gSmoothedFPS)
	
	    # convert smoothed FPS value into labeled character string
		if (SteerTest.clock.paused):
			pausedStr = " Paused"
		else:
			pausedStr = ""
	    fpsStr = "fps: %d%s" %  ( int(round (gSmoothedFPS)),pausedStr )

	
	    # draw the string in white at the lower left corner of the window
	    lh = 16
	    screenLocation1 = vec3(10, 10 + lh, 0)
	    draw2dTextAt2dLocation (fpsStr, screenLocation1, gWhite);
	
	    # add "usage" message if fixed target frame rate is specified
	    if (targetFrameRate)
	    {
	        # run time per frame over target frame time (as a percentage)
	        const float usage =
	            ((100 * SteerTest::clock.elapsedNonWaitRealTime) /
	             (1.0f / SteerTest::clock.targetFPS));
	
	        # blend new usage value into running average
	        blendIntoAccumulator (smoothRate, usage, gSmoothedUsage);
	
	        # create usage description character string
	        std::ostringstream usageStr;
	        usageStr << std::setprecision (0);
	        usageStr << std::setiosflags (std::ios::fixed);
	        usageStr << gSmoothedUsage << "% usage of 1/";
	        usageStr << SteerTest::clock.targetFPS << " time step";
	        usageStr << std::ends;
	
	        # display message in lower left corner of window
	        # (draw in red if the instantaneous usage is 100% or more)
	        const Vec3 screenLocation2 (10, 10 + 2*lh, 0);
	        const Vec3 color = (usage >= 100) ? gRed : gGray60;
	        draw2dTextAt2dLocation (usageStr, screenLocation2, color);
	    }
	
	    # get smoothed phase timer information
	    const float ptd = SteerTest::phaseTimerDraw();
	    const float ptu = SteerTest::phaseTimerUpdate();
	    const float pto = SteerTest::phaseTimerOverhead();
	    blendIntoAccumulator (smoothRate, ptd, gSmoothedTimerDraw);
	    blendIntoAccumulator (smoothRate, ptu, gSmoothedTimerUpdate);
	    blendIntoAccumulator (smoothRate, pto, gSmoothedTimerOverhead);
	
	    # display phase timer information
	    std::ostringstream timerStr;
	    timerStr << "update: ";
	    writePhaseTimerReportToStream (gSmoothedTimerUpdate, timerStr);
	    timerStr << "draw:   ";
	    writePhaseTimerReportToStream (gSmoothedTimerDraw, timerStr);
	    timerStr << "other:  ";
	    writePhaseTimerReportToStream (gSmoothedTimerOverhead, timerStr);
	    timerStr << std::ends;
	    const Vec3 screenLocation3 (10, lh * 7, 0);
	    draw2dTextAt2dLocation (timerStr, screenLocation3, gGreen);
"""



def displayFunc():
	""" Main drawing function for SteerTest application,
	drives simulation as a side effect"""

	# clear color and depth buffers
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	
	# run simulation and draw associated graphics
	SteerTest.updateSimulationAndRedraw ()
	
	# draw text showing (smoothed, rounded) "frames per second" rate
	#drawDisplayFPS ();
	
	# draw the name of the selected PlugIn
	drawDisplayPlugInName ()
	
	# draw the name of the camera's current mode
	drawDisplayCameraModeName ()
	
	# draw crosshairs to indicate aimpoint (xxx for debugging only?)
	drawReticle ()
	
	# check for errors in drawing module, if so report and exit
	# checkForDrawError ("SteerTest::updateSimulationAndRedraw")
	
	# double buffering, swap back and front buffers
	glFlush ()
	glutSwapBuffers()

# do all initialization related to graphics

def keyboardFunc(key, x, y):
	#std::ostringstream message;
	
	# ascii codes
	tab_key = 9;
	space_key = 32;
	esc_key = 27; # escape key
	"""
	# reset selected PlugIn
	if key=='r':
		SteerTest::resetSelectedPlugIn ();
		p"reset PlugIn "
				<< '"' << SteerTest::nameOfSelectedPlugIn () << '"'
				<< std::ends;
		SteerTest::printMessage (message);
	
	# cycle selection to next vehicle
	case 's':
		SteerTest::printMessage ("select next vehicle/agent");
		SteerTest::selectNextVehicle ();
		break;
	
	# camera mode cycle
	case 'c':
		SteerTest::camera.selectNextMode ();
		message << "select camera mode "
				<< '"' << SteerTest::camera.modeName () << '"' << std::ends;
		SteerTest::printMessage (message);
		break;
	
	# select next PlugIn
	case tab:
		SteerTest::selectNextPlugIn ();
		message << "select next PlugIn: "
				<< '"' << SteerTest::nameOfSelectedPlugIn () << '"'
				<< std::ends;
		SteerTest::printMessage (message);
		break;
	
	# toggle annotation state
	case 'a':
		SteerTest::printMessage (SteerTest::toggleAnnotationState () ?
								 "annotation ON" : "annotation OFF");
		break;
	
	# toggle run/pause state
	case space:
		SteerTest::printMessage (SteerTest::clock.togglePausedState () ?
								 "pause" : "run");
		break;
	
	# cycle through frame rate presets
	case 'f':
		message << "set frame rate to "
				<< selectNextPresetFrameRate () << std::ends;
		SteerTest::printMessage (message);
		break;
	
	# print minimal help for single key commands
	case '?':
		SteerTest::keyboardMiniHelp ();
		break;
	
	# exit application with normal status 
	case esc:
		glutDestroyWindow (windowID);
		SteerTest::printMessage ("exit.");
		SteerTest::exit (0);
	
	default:
		message << "unrecognized single key command: " << key;
		message << " (" << (int)key << ")";#xxx perhaps only for debugging?
		message << std::ends;
		SteerTest::printMessage ("");
		SteerTest::printMessage (message);
		SteerTest::keyboardMiniHelp ();
	}
	"""


def initializeGraphics(args):
	global appVersionName
	# initialize GLUT state based on command line arguments
	glutInit(args) 
	
	# display modes: RGB+Z and double buffered
	mode = GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE
	glutInitDisplayMode(mode)
	
	# create and initialize our window with GLUT tools
	# (center window on screen with size equal to "ws" times screen size)
	sw = glutGet(GLUT_SCREEN_WIDTH)
	sh = glutGet(GLUT_SCREEN_HEIGHT)
	ws = 0.8 # window_size / screen_size
	ww = int((sw * ws))
	wh = int((sh * ws))
	glutInitWindowPosition(int(sw * (1-ws)/2), int(sh * (1-ws)/2))
	glutInitWindowSize (ww, wh)
	windowID = glutCreateWindow (appVersionName)
	reshapeFunc (ww, wh)
	initGL()
	
	# register our display function, make it the idle handler too
	glutDisplayFunc(displayFunc) 
	glutIdleFunc(displayFunc)
	
	# register handler for window reshaping
	glutReshapeFunc(reshapeFunc)
	
	# register handler for keyboard events
	glutKeyboardFunc(keyboardFunc)
	glutSpecialFunc (specialFunc)
	
	# register handler for mouse button events
	glutMouseFunc (mouseButtonFunc)
	
	# register handler to track mouse motion when any button down
	glutMotionFunc (mouseMotionFunc)
	
	# register handler to track mouse motion when no buttons down
	glutPassiveMotionFunc (mousePassiveMotionFunc)
	
	# register handler for when mouse enters or exists the window
	glutEntryFunc (mouseEnterExitWindowFunc)


def specialFunc(key,x,y):
	pass
	

def reshapeFunc(width,height):
	#set viewport to full window
	glViewport(0, 0, width, height)
	# set perspective transformation
	glMatrixMode (GL_PROJECTION)
	#determine aspect ratio
	aRatio = 1
	if height!=0: aRatio = float(width)/float(height)	
	#load identity matrix to reset view
	glLoadIdentity()
	fieldOfViewY = 45.0
	zNear = 1
	zFar = 400
	gluPerspective (fieldOfViewY, aRatio, zNear, zFar)
	# leave in modelview mode
	glMatrixMode(GL_MODELVIEW)

####### mouse handlers ###########

def mouseButtonFunc(button, state, x, y):
	"""This is called (by GLUT) each time a mouse button pressed or released"""
	global gMouseAdjustingCameraAngle
	global gMouseAdjustingCameraRadius
	global gMouseAdjustingCameraLastX
	global gMouseAdjustingCameraLastY
	
	macosx = False
	
	# if the mouse button has just been released
	if (state == GLUT_UP):
		# end any ongoing mouse-adjusting-camera session
		gMouseAdjustingCameraAngle = False
		gMouseAdjustingCameraRadius = False

	# if the mouse button has just been pushed down
	if (state == GLUT_DOWN):
		# names for relevant values of "button" and "state"
		mods       = glutGetModifiers ()
		modNone    = (mods == 0)
		modCtrl    = (mods == GLUT_ACTIVE_CTRL)
		modAlt     = (mods == GLUT_ACTIVE_ALT)
		modCtrlAlt = (mods == (GLUT_ACTIVE_CTRL | GLUT_ACTIVE_ALT))
		mouseL     = (button == GLUT_LEFT_BUTTON)
		mouseM     = (button == GLUT_MIDDLE_BUTTON)
		mouseR     = (button == GLUT_RIGHT_BUTTON)

	
		# mouse-left (with no modifiers): select vehicle
		if (modNone & mouseL):	
			pass
			#<PH> SteerTest::selectVehicleNearestScreenPosition (x, y);

		
		# control-mouse-left: begin adjusting camera angle
		# (on Mac OS X control-mouse maps to mouse-right for "context menu",
		# this makes SteerTest's control-mouse work work the same on OS X as 
		# on Linux and Windows, but it precludes using a mouseR context menu)
		if ((modCtrl & mouseL) | (modNone & mouseR & macosx)):
			gMouseAdjustingCameraLastX = x
			gMouseAdjustingCameraLastY = y
			gMouseAdjustingCameraAngle = True

		
		# control-mouse-middle: begin adjusting camera radius
		# (same for: control-alt-mouse-left and control-alt-mouse-middle,
		# and on Mac OS X it is alt-mouse-right)
		if ((modCtrl    & mouseM) | 
			(modCtrlAlt & mouseL) | 
			(modCtrlAlt & mouseM) |
			(modAlt     & mouseR & macosx)):

			gMouseAdjustingCameraLastX = x
			gMouseAdjustingCameraLastY = y
			gMouseAdjustingCameraRadius = True
			
	########### Finish

def mouseMotionFunc(x, y):
	"""called when mouse moves and any buttons are down"""	
	global gMouseAdjustingCameraLastX
	global gMouseAdjustingCameraLastY
	
	# are we currently in the process of mouse-adjusting the camera?
	if (gMouseAdjustingCameraAngle | gMouseAdjustingCameraRadius):
		# speed factors to map from mouse movement in pixels to 3d motion
		dSpeed = 0.005
		rSpeed = 0.01
		
		# XY distance (in pixels) that mouse moved since last update
		dx = x - gMouseAdjustingCameraLastX
		dy = y - gMouseAdjustingCameraLastY
		gMouseAdjustingCameraLastX = x
		gMouseAdjustingCameraLastY = y
		
		cameraAdjustment = vec3()
		
		# set XY values according to mouse motion on screen space
		if (gMouseAdjustingCameraAngle):
			cameraAdjustment.x = dx * -1.0 * Speed
			cameraAdjustment.y = dy * + dSpeed

		# set Z value according vertical to mouse motion
		if (gMouseAdjustingCameraRadius):
			cameraAdjustment.z = dy * rSpeed;

		# pass adjustment vector to camera's mouse adjustment routine
		#<PH> SteerTest::camera.mouseAdjustOffset (cameraAdjustment);

def mousePassiveMotionFunc(x,y):
	SteerTest.mouseX = x
	SteerTest.mouseY = y

def mouseEnterExitWindowFunc(state):
	"""called when mouse enters or exits the window"""
	if (state == GLUT_ENTERED): SteerTest.mouseInWindow = True
	if (state == GLUT_LEFT): SteerTest.mouseInWindow = False

def drawDisplayPlugInName():

	h = glutGet(GLUT_WINDOW_HEIGHT)

	screenLocation = vec3(10, h-20, 0)
	draw2dTextAt2dLocation("Python Plugin", screenLocation, gWhite)

def drawDisplayCameraModeName():
	"""raw camera mode name in lower lefthand corner of screen"""
	message = "Camera %s\n" % (SteerTest.camera.modeName())

	screenLocation =vec3(10, 10, 0)
	draw2dTextAt2dLocation(message, screenLocation, gWhite)


def warnIfInUpdatePhase2(name):
    message= "use annotation (during simulation update, do not call %s)" % (name)
    SteerTest.printWarning (message);


################ drawing helper functions ######
def iglVertexVec3(v):
    glVertex3f (v.x, v.y, v.z)

glVertexVec3 = iglVertexVec3

#


def iDrawLine(startPoint, endPoint, color):
	"""draw 3d "graphical annotation" lines, used for debugging"""
	warnIfInUpdatePhase ("iDrawLine");
	glColor3f (color.x, color.y, color.z);
	glBegin (GL_LINES);
	glVertexVec3 (startPoint);
	glVertexVec3 (endPoint);
	glEnd ();


drawLine = iDrawLine


def drawLineAlpha(startPoint, endPoint, color,alpha):
	"""
	draw a line with alpha blending
	
	see also glAlphaFunc
	glBlendFunc (GL_SRC_ALPHA)
	glEnable (GL_BLEND)
	"""

	warnIfInUpdatePhase("drawLineAlpha")
	glColor4f (color.x, color.y, color.z, alpha)
	glBegin (GL_LINES)
	glVertexVec3(startPoint)
	glVertexVec3(endPoint)
	glEnd()

def iDrawTriangle(a,b,c,color):
	""" """
	warnIfInUpdatePhase("iDrawTriangle")
	glColor3f(color.x, color.y, color.z)
	glBegin(GL_TRIANGLES)

	glVertexVec3(a)
	glVertexVec3(b)
	glVertexVec3(c)

	glEnd()

def iDrawQuadrangle(a,b,c,d,color):
	"""Draw a single OpenGL quadrangle given four Vec3 vertices, and color."""
	warnIfInUpdatePhase("iDrawTriangle")
	glColor3f(color.x, color.y, color.z)
	glBegin(GL_QUADS)

	glVertexVec3(a)
	glVertexVec3(b)
	glVertexVec3(c)
	glVertexVec3(d)
	
	glEnd()

drawQuadrangle = iDrawQuadrangle




def beginDoubleSidedDrawing():
	"""
	Between matched sets of these two calls, assert that all polygons
	will be drawn "double sided", that is, without back-face culling
	"""
	glPushAttrib(GL_ENABLE_BIT)
	glDisable(GL_CULL_FACE)


def endDoubleSidedDrawing():
	glPopAttrib()


###################




def drawCircleOrDisk(radius, axis, center, color, segments, filled, in3d=True):
	"""
	General purpose circle/disk drawing routine.  Draws circles or disks (as
	specified by "filled" argument) and handles both special case 2d circles
	on the XZ plane or arbitrary circles in 3d space (as specified by "in3d"
	argument)
	"""
	ls = LocalSpace()
	if (in3d):
		# define a local space with "axis" as the Y/up direction
		# (XXX should this be a method on  LocalSpace?)
		unitAxis = axis.normalize()
		unitPerp = findPerpendicularIn3d(axis).normalize()
		ls.setUp(unitAxis)
		ls.setForward(unitPerp)
		ls.setPosition(center)
		ls.setUnitSideFromForwardAndUp()

	# make disks visible (not culled) from both sides 
	if (filled): beginDoubleSidedDrawing()
	
	# point to be rotated about the (local) Y axis, angular step size
	pointOnCircle = vec3(radius, 0, 0)
	step = (2 * M_PI) / segments
	
	# set drawing color
	glColor3f(color.x, color.y, color.z)
	
	# begin drawing a triangle fan (for disk) or line loop (for circle)
	if filled:
		glBegin (GL_TRIANGLE_FAN)
		# for the filled case, first emit the center point
		if in3d:
			iglVertexVec3(ls.position())
		else:
			iglVertexVec3(center)
		vertexCount = segments+1
	else:
		glBegin (GL_LINE_LOOP)
		vertexCount = segments


	# rotate p around the circle in "segments" steps
	sin=0.0
	cos=0.0

	for i in range(vertexCount):
		# emit next point on circle, either in 3d (globalized out
		# of the local space), or in 2d (offset from the center)
		if in3d:
			iglVertexVec3(ls.globalizePosition(pointOnCircle))
		else:
			iglVertexVec3((pointOnCircle + center))

		# rotate point one more step around circle
		# LP: changed interface to the python way
		pointOnCircle, sin, cos = pointOnCircle.rotateAboutGlobalY(step, sin, cos)

	
	# close drawing operation
	glEnd()
	if (filled): endDoubleSidedDrawing()

# python makes it not necessary to implement draw3dCircleOrDisk properly
# we just use default parameters and make it an alias 
draw3dCircleOrDisk = drawCircleOrDisk

def drawCircleOrDisk(radius, center, color, segments, filled):
	"""drawing utility used by both drawXZCircle and drawXZDisk"""
	
	#draw a circle-or-disk on the XZ plane
	drawCircleOrDisk (radius, vector.zero, center, color, segments, filled, False)



def drawBasic2dCircularVehicle(vehicle,color):
	"""a simple 2d vehicle on the XZ plane"""

	# "aspect ratio" of body (as seen from above)
	x = 0.5
	y = math.sqrt(1 - (x * x))
	
	# radius and position of vehicle
	r = vehicle.radius()
	p = vehicle.position()
	
	# shape of triangular body
	u = r * 0.05 * vector.up # slightly up
	f = r * vehicle.forward()
	s = r * vehicle.side() * x
	b = r * vehicle.forward() * -y
	
	# draw double-sided triangle (that is: no (back) face culling)
	beginDoubleSidedDrawing()
	iDrawTriangle( (p + f + u), (p + b - s + u), (p + b + s + u), color)
	endDoubleSidedDrawing()
	
	# draw the circular collision boundary
	drawXZCircle (r, p + u, gWhite, 20)

def drawBasic3dSphericalVehicle(vehicle, color):
	"""a simple 3d vehicle"""
	#"aspect ratio" of body (as seen from above)
	x = 0.5
	y = math.sqrt(1 - (x * x))

	# radius and position of vehicle
	r = vehicle.radius()
	p = vehicle.position()

	# body shape parameters
	f = r * vehicle.forward()
	s = r * vehicle.side() * x
	u = r * vehicle.up() * x * 0.5
	b = r * vehicle.forward() * -1.0 *y

	# vertex positions
	nose   = p + f
	side1  = p + b - s
	side2  = p + b + s
	top    = p + b + u
	bottom = p + b - u

	# colors
	j = 0.05
	k = -0.05
	color1 = color + Vec3 (j, j, k)
	color2 = color + Vec3 (j, k, j)
	color3 = color + Vec3 (k, j, j)
	color4 = color + Vec3 (k, j, k)
	color5 = color + Vec3 (k, k, j)
	
	# draw body
	iDrawTriangle(nose,  side1,  top,    color1)  # top, side 1
	iDrawTriangle(nose,  top,    side2,  color2)  # top, side 2
	iDrawTriangle(nose,  bottom, side1,  color3)  # bottom, side 1
	iDrawTriangle(nose,  side2,  bottom, color4)  # bottom, side 2
	iDrawTriangle(side1, side2,  top,    color5)  # top back
	iDrawTriangle(side2, side1,  bottom, color5)  # bottom back



def drawXZCheckerboardGrid (size, subsquares,center,color1,color2):
	half = float(size)/2
	spacing = float(size) / subsquares
	
	beginDoubleSidedDrawing()
	
	flag1 = false
	p = -half
	corner = vec3()
	for i in range(subsquares):
		flag2 = flag1
		q = -half
		for j in range(subsquares):
			corner.set (p, 0, q)
			corner += center
			if flag2:
				col = color1 
			else: 
				col = color2
			iDrawQuadrangle (corner, corner + Vec3 (spacing, 0, 0),
							corner + Vec3 (spacing, 0, spacing),
							corner + Vec3 (0, 0, spacing), col )
			flag2 = not flag2
			q += spacing
	
		flag1 = not flag1
		p += spacing
	
	endDoubleSidedDrawing()


def drawXZLineGrid(size,subsquares,center,color):
	"""
	draw a square grid of lines on the XZ (horizontal) plane.
	
	("size" is the length of a side of the overall grid, "subsquares" is the
	number of subsquares along each edge (for example a standard checkboard
	has eight), "center" is the 3d position of the center of the grid, lines
	are drawn in the specified "color".)
	"""

	warnIfInUpdatePhase ("drawXZLineGrid")
	
	half = size/2
	spacing = size / subsquares
	
	# set grid drawing color
	glColor3f (color.x, color.y, color.z)
	
	# draw a square XZ grid with the given size and line count
	glBegin(GL_LINES)
	q = -1 * half
	for i in range(subsquares + 1):
		x1 = vec3(q, 0, half) # along X parallel to Z
		x2 = vec3(q, 0, -1*half)
		z1 = vec3(half, 0, q) # along Z parallel to X
		z2 = vec3(-1*half, 0, q)
		
		iglVertexVec3 (x1 + center)
		iglVertexVec3 (x2 + center)
		iglVertexVec3 (z1 + center)
		iglVertexVec3 (z2 + center)
		
		q += spacing
	glEnd()




def drawAxes(ls,size,color):
	"""
	draw the three axes of a LocalSpace: three lines parallel to the
	basis vectors of the space, centered at its origin, of lengths
	given by the coordinates of "size".
	"""
	x = vec3(size.x / 2, 0, 0)
	y = vec3(0, size.y / 2, 0)
	z = vec3(0, 0, size.z / 2)
	
	iDrawLine(ls.globalizePosition(x), ls.globalizePosition (x * -1), color)
	iDrawLine(ls.globalizePosition(y), ls.globalizePosition (y * -1), color)
	iDrawLine(ls.globalizePosition(z), ls.globalizePosition (z * -1), color)


def drawBoxOutline(localSpace,size,color):
	"""
	draw the edges of a box with a given position, orientation, size
	and color.  The box edges are aligned with the axes of the given
	LocalSpace, and it is centered at the origin of that LocalSpace.
	"size" is the main diagonal of the box.
	
	use gGlobalSpace to draw a box aligned with global space
	"""

	s = size / 2.0 # half of main diagonal
	
	a = vec3(+s.x, +s.y, +s.z)
	b = vec3(+s.x, -1*s.y, +s.z)
	c = vec3(-1.0*s.x, -1.0*s.y, +s.z)
	d = vec3(-1.0*s.x, +s.y, +s.z)
	
	e = vec3(+s.x, +s.y, -1.0*s.z)
	f = vec3(+s.x, -1.0*s.y, -1.0*s.z)
	g = vec3(-1.0*s.x, -1.0*s.y, -1.0*s.z)
	h = vec3(-1.0*s.x, +s.y, -1.0*s.z)
	
	A = localSpace.globalizePosition (a)
	B = localSpace.globalizePosition (b)
	C = localSpace.globalizePosition (c)
	D = localSpace.globalizePosition (d)
	
	E = localSpace.globalizePosition (e)
	F = localSpace.globalizePosition (f)
	G = localSpace.globalizePosition (g)
	H = localSpace.globalizePosition (h)



def drawCameraLookAtCheck (cameraPosition,pointToLookAt,up):
	"""this comes up often enough to warrant its own warning function"""
	view = pointToLookAt - cameraPosition
	perp = view.perpendicularComponent (up)
	
	# LP: is this a test for object equality or for containin data
	if (perp == vector.zero):
		SteerTest.printWarning ("LookAt: degenerate camera")

def drawCameraLookAt (cameraPosition,pointToLookAt,up):
	"""
	Define scene's camera (viewing transformation) in terms of the camera's
	position, the point to look at (an "aim point" in the scene which will
	end up at the center of the camera's view), and an "up" vector defining
	the camera's "roll" around the "view axis" between cameraPosition and
	pointToLookAt (the image of the up vector will be vertical in the
	camera's view).
	"""
	# check for valid "look at" parameters
	drawCameraLookAtCheck (cameraPosition, pointToLookAt, up)
	
	# use LookAt from OpenGL Utilities
	glLoadIdentity()
	gluLookAt(cameraPosition.x, cameraPosition.y, cameraPosition.z,
		pointToLookAt.x,  pointToLookAt.y,  pointToLookAt.z,
		up.x,             up.y,             up.z)


def draw2dLine(startPoint, endPoint, color):
	"""draw 2d lines in screen space: x and y are the relevant coordinates"""
	originalMatrixMode = begin2dDrawing()
	try:
		iDrawLine(startPoint, endPoint, color)
	except:
		pass
	end2dDrawing (originalMatrixMode)

def drawReticle():
	"""
	draw a reticle at the center of the window.  Currently it is small
	crosshair with a gap at the center, drawn in white with black borders
	"""
	
	a = 10;
	b = 30;
	w = glutGet(GLUT_WINDOW_WIDTH)  * 0.5
	h = glutGet(GLUT_WINDOW_HEIGHT) * 0.5
	
	draw2dLine(vec3 (w+a, h,   0), vec3 (w+b, h,   0), gWhite)
	draw2dLine(vec3 (w,   h+a, 0), vec3 (w,   h+b, 0), gWhite)
	draw2dLine(vec3 (w-a, h,   0), vec3 (w-b, h,   0), gWhite)
	draw2dLine(vec3 (w,   h-a, 0), vec3 (w,   h-b, 0), gWhite)
	
	glLineWidth(3)
	draw2dLine(vec3 (w+a, h,   0), vec3 (w+b, h,   0), gBlack)
	draw2dLine(vec3 (w,   h+a, 0), vec3 (w,   h+b, 0), gBlack)
	draw2dLine(vec3 (w-a, h,   0), vec3 (w-b, h,   0), gBlack)
	draw2dLine(vec3 (w,   h-a, 0), vec3 (w,   h-b, 0), gBlack)
	glLineWidth(1)




def checkForGLError(locationDescription):
	"""OpenGL-specific routine for error check, report, and exit"""
	# normally (when no error) just return
	lastGlError = glGetError()
	if (lastGlError == GL_NO_ERROR): return
	
	# otherwise print vaguely descriptive error message, then exit
	
	if lastGlError==GL_INVALID_ENUM:
		errStr = "GL_INVALID_ENUM"
	elif lastGlError==GL_INVALID_VALUE:
		errStr = "GL_INVALID_VALUE"
	elif lastGlError==GL_INVALID_OPERATION:
		errStr = "GL_INVALID_OPERATION"
	elif lastGlError==GL_STACK_OVERFLOW:
		errStr = "GL_STACK_OVERFLOW"
	elif lastGlError==GL_STACK_UNDERFLOW:
		errStr = "GL_STACK_UNDERFLOW"
	elif lastGlError==GL_OUT_OF_MEMORY:
		errStr = "GL_OUT_OF_MEMORY"
	elif lastGlError==GL_TABLE_TOO_LARGE:
		errStr = "GL_TABLE_TOO_LARGE"
	
	
		
	if (locationDescription!=None & locationDescription!=""):
		ld =  " in " +locationDescription
	else:
		ld = ""
	
	print "SteerTest: OpenGL error ", errStr, ld
	
	SteerTest.exit(1)

def checkForDrawError(locationDescription):
	"""check for errors during redraw, report any and then exit"""
	checkForGLError (locationDescription)

def drawGetWindowHeight():
	"""accessors for GLUT's window dimensions"""
	return glutGet(GLUT_WINDOW_HEIGHT)
def drawGetWindowWidth():
	"""accessors for GLUT's window dimensions"""
	return glutGet(GLUT_WINDOW_WIDTH)

import DeferredLine
################ General OpenGL drawing helper functions ######

def begin2dDrawing():
	# store OpenGL matrix mode
	originalMatrixMode = glGetIntegerv (GL_MATRIX_MODE)
	
	# clear projection transform
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	
	# set up orthogonal projection onto window's screen space
	w = glutGet(GLUT_WINDOW_WIDTH)
	h = glutGet(GLUT_WINDOW_HEIGHT)
	glOrtho(0.0, w, 0.0, h, -1.0, 1.0)
	
	# clear model transform
	glMatrixMode(GL_MODELVIEW)
	glPushMatrix()
	glLoadIdentity()
	
	# return original matrix mode for saving (stacking)
	return(originalMatrixMode)

def end2dDrawing(originalMatrixMode):
	# restore previous model/projection transformation state
	glPopMatrix()
	glMatrixMode(GL_PROJECTION)
	glPopMatrix()
	
	# restore OpenGL matrix mode
	glMatrixMode(originalMatrixMode)


def draw2dTextAt3dLocation (text, location, color):
	import sys
	# XXX NOTE: "it would be nice if" this had a 2d screenspace offset for
	# the origin of the text relative to the screen space projection of
	# the 3d point.
	
	# set text color and raster position
	glColor3f(color.x, color.y, color.z)
	glRasterPos3f(location.x, location.y, location.z)
	
	# switch into 2d screen space in case we need to handle a new-line
	rasterPosition = glGetIntegerv(GL_CURRENT_RASTER_POSITION)
	#originalMatrixMode = begin2dDrawing()
	
	#xxx uncommenting this causes the "2d" version to print the wrong thing
	#xxx with it out the first line of a multi-line "3d" string jiggles
	#glRasterPos2i (rasterPosition[0], rasterPosition[1]);
	
	fontHeight = 15
	lines = 0
	for character in text:
		if character == '\n':
			glRasterPos2i(x, y-(lines*fontHeight))
			lines+=1
		else:
			glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(character));

	# loop over each character in string (until null terminator)
	
	# switch back out of 2d screen space
	#end2dDrawing(originalMatrixMode)


def draw2dTextAt2dLocation (text, location, color):
	originalMatrixMode = begin2dDrawing()
	#print "Start: ", originalMatrixMode
	
	# draw text at specified location (which is now interpreted as
	# relative to screen space) and color
	try:
		draw2dTextAt3dLocation (text, location, color)
	except:
		pass
	end2dDrawing(originalMatrixMode)
	#print "End: ", originalMatrixMode


def main():

	screen_width =  int(WIN_SCALE*glutGet(GLUT_SCREEN_WIDTH))
	screen_height = int(WIN_SCALE*glutGet(GLUT_SCREEN_HEIGHT))
	
	glutInitWindowSize(screen_width, screen_height)
	glutCreateWindow('PySteerTest')

	glutDisplayFunc(display)




def runGraphics():
	"""run graphics event loop"""
	glutMainLoop()

if __name__ == '__main__':
	try:
		GLU_VERSION_1_2
	except:
		print "Need GLU 1.2 to run this demo"
		sys.exit(1)
	main()
	glutMainLoop()

