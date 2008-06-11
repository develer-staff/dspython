from wrap_console import *
from wrap_system import *
from wrap_video import *
from wrap_interrupts import *
from wrap_videoGL import *
from wrap_touch import *
from wrap_input import *
from wrap_bios import *

import math

def insideBox(p, p1, p2, p3, p4):
	#XXX horrible
	return p1[0] < p[0] < p2[0] and p2[1] < p[1] < p3[1]

def resizeGL(width, height):
	if height==0:
		height=1
	wglViewPort(0, 0, width - 1, height - 1)
	wglMatrixMode(GL_PROJECTION)
	wglLoadIdentity()
	wglOrthof32(0, width, height, 0, 0, 1)
	wglMatrixMode(GL_MODELVIEW)
	wglLoadIdentity()

def initGL():
	#glShadeModel(GL_SMOOTH)
	wglInit()
	wglEnable(GL_ANTIALIAS)
	wglClearColor(0, 0, 0, 0)
	wglClearDepth(0x7FFF)
	#glClearDepth(1.0)
	#glEnable(GL_DEPTH_TEST)
	#glDepthFunc(GL_LEQUAL)
	#glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
	#glLightfv( GL_LIGHT1, GL_AMBIENT, LightAmbient )
	#glLightfv( GL_LIGHT1, GL_DIFFUSE, LightDiffuse )
	#glLightfv( GL_LIGHT1, GL_POSITION, LightPosition )
	#glEnable( GL_LIGHT1 )

def initDS():
	wpowerON(POWER_ALL)
	wconsoleDemoInit()

	wvideoSetMode(MODE_0_3D)
	wlcdMainOnBottom()
	wirqInit()
	wirqSet(IRQ_VBLANK, 0)

class Squirrel(object):
	states = {"HIDDEN": 100,
				"GOINGUP": 30,
				"EXPOSED": 10,
				"RETIRING": 20}

	next_state = {"HIDDEN": "GOINGUP",
					"GOINGUP": "EXPOSED",
					"EXPOSED": "RETIRING",
					"RETIRING": "HIDDEN"}

	hit_threshold = 0.25

	def __init__(self, pos):
		self.pos = pos
		self._hit = False

		self.setState("HIDDEN")

	def setState(self, state, timer=None):
		assert state in self.states
		self.state = state
		if timer is not None:
			self.timer = timer
		else:
			self.timer = self.states[state]

		if state == "HIDDEN":
			self._hit = False

	def exposement(self):
		maxtimer = self.states[self.state]
		if self.state == "GOINGUP":
			return (maxtimer - self.timer) / float(maxtimer)

		if self.state == "EXPOSED":
			return 1.0

		if self.state == "RETIRING":
			return (self.timer - maxtimer) / float(maxtimer)

	def hit(self, p):
		if self._hit:
			# Can't hit if the squirrel has already been hit
			return False

		if self._wasHit(p) and self.exposement() > self.hit_threshold:
			self._hit = True
			self.setState("RETIRING", timer=10)
			return True

	def _wasHit(self, p):
		return insideBox(p, *self.boundingBox())

	def update(self):
		self.timer -= 1

		if self.timer == 0:
			self.setState(self.next_state[self.state])

	def _height(self):
		maxtimer = self.states[self.state]
		if self.state == "HIDDEN":
			return 0
		elif self.state == "EXPOSED":
			return 1.0
		elif self.state == "GOINGUP":
			return (maxtimer - self.timer) / float(maxtimer)
		elif self.state == "RETIRING":
			return (self.timer) / float(maxtimer)

		assert False

	def boundingBox(self):
		height = self._height()
		return ((self.pos[0] - 20, self.pos[1] - int(height * 40)),
				(self.pos[0] + 20, self.pos[1] - int(height * 40)),
				(self.pos[0] + 20, self.pos[1]),
				(self.pos[0] - 20, self.pos[1]),
				)
			
	def draw(self):

		color_state = {"HIDDEN": (0.0, 0.0, 0.0),
						"GOINGUP": (0.0, 1.0, 0.0),
						"EXPOSED": (0.0, 1.0, 0.0),
						"RETIRING": (0.0, 1.0, 0.0)}

		color = color_state[self.state]
		maxtimer = self.states[self.state]

		if self.state == "GOINGUP":
			color = tuple([c * (maxtimer - self.timer)/float(maxtimer) for c in color])
		elif self.state == "RETIRING":
			color = tuple([c * (self.timer)/float(maxtimer) for c in color])

		if self._hit:
			color = (1.0, 0.0, 0.0)

		height = self._height()
		p1, p2, p3, p4 = self.boundingBox()

		wglBegin(GL_QUADS)
		wglColor3f(color[0], color[1], color[2])
		wglVertex3v16(p1[0], p1[1], 0)
		wglVertex3v16(p2[0], p2[1], 0)
		wglVertex3v16(p3[0], p3[1], 0)
		wglVertex3v16(p4[0], p4[1], 0)
		wglEnd()

class Game(object):
	pos_squirrels = [(50, 50), (150, 150), (50, 150), (150, 50)]

	def __init__(self):
		self.squirrels = [Squirrel(p) for p in self.pos_squirrels]

	def hammer(self, p):
		hit = False
		for sq in self.squirrels:
			rv = sq.hit(p)
			if rv:
				hit = True
		return hit

	def update(self):
		for sq in self.squirrels:
			sq.update()

	def draw(self):
		for sq in self.squirrels:
			sq.draw()

initDS()
initGL()
resizeGL(256, 192)

print "*** Crush ***"
print ""
print "Crush the squirrels with your hammer when they come out of their holes!!!"
print ""
print "Touch the screen to start a new game..."

while 1:

	x = 0
	y = 0
	while x == 0 and y == 0:
		pos = wtouchReadXY()
		x, y = float(pos[2]), float(pos[3])
		wswiWaitForVBlank()

	print "Game start!"
		
	game = Game()

	frames = 0
	points = 0
	gameover = False

	while not gameover:

		pos = wtouchReadXY()
		x, y = float(pos[2]), float(pos[3])

		if x != 0 and y != 0:
			rv = game.hammer((x, y))
			if rv:
				points += 1

		wglPolyFmt(POLY_ALPHA(31) | POLY_CULL_NONE)
		game.update()
		game.draw()

		frames += 1
		if frames > 20*50:
			gameover = True

		#wscanKeys()
		#keys = wkeysHeld()

		#if keys & KEY_UP:
			#rotateX += 3
		#if keys & KEY_DOWN:
			#rotateX -= 3
		#if keys & KEY_LEFT:
			#rotateY += 3
		#if keys & KEY_RIGHT:
			#rotateY -= 3

		wglFlush(0)
		wswiWaitForVBlank()
	
	print "You scored", points, "points!"
	print "Touch the screen to try again."