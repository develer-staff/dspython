from wrap_console import *
from wrap_system import *
from wrap_video import *
from wrap_interrupts import *
from wrap_videoGL import *
from wrap_touch import *
from wrap_input import *
from wrap_bios import *

powerON(POWER_ALL)
consoleDemoInit()

videoSetMode(MODE_0_3D)
lcdMainOnBottom()
irqInit()
irqSet(IRQ_VBLANK, 0)
glInit()
glEnable(GL_ANTIALIAS)
glClearColor(0,0,15,31)
glClearPolyID(63)
glClearDepth(0x7FFF)
glViewPort(0,0,255,191)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(35, 256.0 / 192.0, 0.1, 100)
gluLookAt(0.0, 0.0, 1.0, \
		0.0, 0.0, 0.0, \
		0.0, 1.0, 0.0)

rotateX = 0.0
rotateY = 0.0

print "dspython v0.1"

while 1:

	pos = touchReadXY()
	x, y = float(pos[2]), float(pos[3])
	
	x = (x * 5) / 256
	y = (y * 3) / 192
	
	x -= 2.5
	y -= 1.5

	scanKeys()
	keys = keysHeld()

	if keys & KEY_UP:
		rotateX += 3
	if keys & KEY_DOWN:
		rotateX -= 3
	if keys & KEY_LEFT:
		rotateY += 3
	if keys & KEY_RIGHT:
		rotateY -= 3

	glPushMatrix()

	glTranslatef(0, 0, -1.0)
    
	glRotateX(rotateX)
	glRotateY(rotateY)

	#Set the current matrix to be the model matrix
	glMatrixMode(GL_MODELVIEW)

	#ds specific, several attributes can be set here	
	glPolyFmt(POLY_ALPHA(31) | POLY_CULL_NONE)

	#draw the obj
	glBegin(GL_TRIANGLES)

	glColor3f(1.0,0,0)
	glVertex3f(-1.0,-1.0,0)

	glColor3f(0,1.0,0)
	glVertex3f(1.0, -1.0, 0)

	glColor3f(0,0,1.0)
	glVertex3f(0, 1.0, 0)

	glEnd()

	glLoadIdentity()
	#glTranslatef(-1.5,0.0,-6.0)
	glTranslatef(x,-y,-3.0)
	glBegin(GL_TRIANGLES)
	glVertex3f( 0.0, 1.0, 0.0)
	glVertex3f(-1.0,-1.0, 0.0)
	glVertex3f( 1.0,-1.0, 0.0)
	glEnd()

	glPopMatrix(1)

	glFlush(0)
	swiWaitForVBlank()
