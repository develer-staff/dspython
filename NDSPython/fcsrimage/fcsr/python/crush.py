#! /usr/bin/env python

import math
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame, pygame.image
from pygame.locals import *

LightAmbient  = ( (0.5, 0.5, 0.5, 1.0) );
LightDiffuse  = ( (1.0, 1.0, 1.0, 1.0) );
LightPosition = ( (0.0, 0.0, 2.0, 1.0) );

def dist(p1, p2):
    return math.sqrt(((p1[0] - p2[0])**2) + ((p1[1] - p2[1])**2))

def resizeGL((width, height)):
    if height==0:
        height=1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #gluPerspective(45, 1.0*width/height, 0.1, 100.0)
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def initGL():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glLightfv( GL_LIGHT1, GL_AMBIENT, LightAmbient )
    glLightfv( GL_LIGHT1, GL_DIFFUSE, LightDiffuse )
    glLightfv( GL_LIGHT1, GL_POSITION, LightPosition )
    glEnable( GL_LIGHT1 )

class Squirrel(object):
    states = {"HIDDEN": 200,
              "GOINGUP": 200,
              "EXPOSED": 200,
              "RETIRING": 100}
    
    next_state = {"HIDDEN": "GOINGUP",
                  "GOINGUP": "EXPOSED",
                  "EXPOSED": "RETIRING",
                  "RETIRING": "HIDDEN"}

    hit_dist = 50
    hit_threshold = 0.5

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
        if self.state == "GOINGUP":
            return (200.0 - self.timer) / 200.0

        if self.state == "EXPOSED":
            return 1.0

        if self.state == "RETIRING":
            return (self.timer - 100.0) / 100.0

    def hit(self, p):
        if self._hit:
            # Can't hit if the squirrel has already been hit
            return False

        if self._wasHit(p) and self.exposement() > self.hit_threshold:
            self._hit = True
            self.setState("RETIRING")
            return True

    def _wasHit(self, p):
        return dist(self.pos, p) < self.hit_dist

    def update(self):
        self.timer -= 1

        if self.timer == 0:
            self.setState(self.next_state[self.state])

    def draw(self):

        color_state = {"HIDDEN": (0.0, 0.0, 0.0),
                       "GOINGUP": (0.0, 1.0, 0.0),
                       "EXPOSED": (0.0, 1.0, 0.0),
                       "RETIRING": (0.0, 0.0, 1.0)}

        color = color_state[self.state]

        if self._hit:
            color = (1.0, 0.0, 0.0)

        if self.state == "GOINGUP":
            color = tuple([c * (200 - self.timer)/200.0 for c in color])
        elif self.state == "RETIRING":
            color = tuple([c * (self.timer)/100.0 for c in color])

        glBegin(GL_TRIANGLES)
        glColor3f(color[0], color[1], color[2])
        glVertex3f(self.pos[0], self.pos[1], 0.0)
        glVertex3f(self.pos[0] - 20, self.pos[1] - 40, 0)
        glVertex3f(self.pos[0] + 20, self.pos[1] - 40, 0)
        glEnd()

class Game(object):
    num_squirrels = 4
    pos_squirrels = [(200, 200), (400, 400), (400, 200), (200, 400)]

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

def main():

    width, height = 640, 480

    video_flags = OPENGL|DOUBLEBUF
    
    pygame.init()
    pygame.display.set_mode((width, height), video_flags)

    resizeGL((width, height))
    initGL()

    game = Game()

    frames = 0
    points = 0
    ticks = pygame.time.get_ticks()
    while 1:
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break
        if event.type == MOUSEBUTTONDOWN:
            hammer = pygame.mouse.get_pos()
            hammer = (hammer[0], height - hammer[1])
            rv = game.hammer(hammer)
            if rv:
                points += 1

        game.update()

        game.draw()
        frames += 1

        pygame.time.delay(10)
        pygame.display.flip()

    print "fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks))
    print "points: %d" % points

if __name__ == '__main__':
    main()
