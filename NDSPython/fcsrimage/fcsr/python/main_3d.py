from wrap_console import *
from wrap_system import *
from wrap_video import *
from wrap_interrupts import *
from wrap_videoGL import *
from wrap_touch import *
from wrap_input import *
from wrap_bios import *

wpowerON(POWER_ALL)
wconsoleDemoInit()

wvideoSetMode(MODE_0_3D)
wlcdMainOnBottom()
wirqInit()
wirqSet(IRQ_VBLANK, 0)
wglInit()
wglEnable(GL_ANTIALIAS)
wglClearColor(0,0,15,31)
wglClearPolyID(63)
wglClearDepth(0x7FFF)
wglViewPort(0,0,255,191)
wglMatrixMode(GL_PROJECTION)
wglLoadIdentity()
wgluPerspective(35, 256.0 / 192.0, 0.1, 100)
wgluLookAt(0.0, 0.0, 1.0, \
		0.0, 0.0, 0.0, \
		0.0, 1.0, 0.0)

rotateX = 0.0
rotateY = 0.0

print "dspython v0.1"

while 1:

	pos = wtouchReadXY()
	x, y = float(pos[2]), float(pos[3])
	
	x = (x * 5) / 256
	y = (y * 3) / 192
	
	x -= 2.5
	y -= 1.5

	wscanKeys()
	keys = wkeysHeld()

	if keys & KEY_UP:
		rotateX += 3
	if keys & KEY_DOWN:
		rotateX -= 3
	if keys & KEY_LEFT:
		rotateY += 3
	if keys & KEY_RIGHT:
		rotateY -= 3

	wglPushMatrix()

	wglTranslatef(0, 0, -1.0)
    
	wglRotateX(rotateX)
	wglRotateY(rotateY)

	#Set the current matrix to be the model matrix
	wglMatrixMode(GL_MODELVIEW)

	#ds specific, several attributes can be set here	
	wglPolyFmt(POLY_ALPHA(31) | POLY_CULL_NONE)

	#draw the obj
	wglBegin(GL_TRIANGLES)

	wglColor3f(1.0,0,0)
	wglVertex3f(-1.0,-1.0,0)

	wglColor3f(0,1.0,0)
	wglVertex3f(1.0, -1.0, 0)

	wglColor3f(0,0,1.0)
	wglVertex3f(0, 1.0, 0)

	wglEnd()

	wglLoadIdentity()
	#wglTranslatef(-1.5,0.0,-6.0)
	wglTranslatef(x,-y,-3.0)
	wglBegin(GL_TRIANGLES)
	wglVertex3f( 0.0, 1.0, 0.0)
	wglVertex3f(-1.0,-1.0, 0.0)
	wglVertex3f( 1.0,-1.0, 0.0)
	wglEnd()

	wglPopMatrix(1)

	wglFlush(0)
	wswiWaitForVBlank()
