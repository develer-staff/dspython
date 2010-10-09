def BIT(n):
	return 1 << n

def POLY_ALPHA(n):
	return n << 16
	
GL_ANTIALIAS       = BIT(4)

GL_TRIANGLES      = 0
GL_QUADS          = 1
GL_TRIANGLE_STRIP = 2
GL_QUAD_STRIP     = 3

GL_PROJECTION     = 0
GL_POSITION       = 1
GL_MODELVIEW      = 2
GL_TEXTURE        = 3

POLY_CULL_NONE       = (3<<6)

cdef extern from "nds/arm9/videoGL.h":
	void c_glInit "glInit" ()
	void c_glEnable "glEnable" (int bits)
	void c_glClearColor "glClearColor" (unsigned char red, unsigned char green, unsigned char blue, unsigned char alpha)
	void c_glClearPolyID "glClearPolyID" (unsigned char ID)
	void c_glClearDepth "glClearDepth" (unsigned short depth)
	void c_glFlush "glFlush" (unsigned int mode)
	void c_glLoadIdentity "glLoadIdentity" ()
	void c_glTranslatef "glTranslatef" (float x, float y, float z)
	void c_glRotateX "glRotateX" (float angle)
	void c_glRotateY "glRotateY" (float angle)
	void c_glBegin "glBegin" (int mode)
	void c_glViewport "glViewport" (unsigned char x1, unsigned char y1, unsigned char x2, unsigned char y2)
	void c_glMatrixMode "glMatrixMode" (int mode)
	void c_gluPerspective "gluPerspective" (float fovy, float aspect, float zNear, float zFar)
	void c_glOrthof32 "glOrthof32" (signed int left, signed int right, signed int bottom, signed int top, signed int zNear, signed int zFar)
	void c_glPolyFmt "glPolyFmt" (unsigned int params)
	void c_glColor3f "glColor3f" (float r, float g, float b)
	void c_glVertex3f "glVertex3f" (float x, float y, float z)
	void c_glVertex3v16 "glVertex3v16" (short int x, short int y, short int z)
	void c_glEnd "glEnd" ()
	void c_glPushMatrix "glPushMatrix" ()
	void c_glPopMatrix "glPopMatrix" (int num)
	void c_gluLookAt "gluLookAt" (float eyex, float eyey, float eyez, float lookAtx, float lookAty, float lookAtz, float upx, float upy, float upz)

def glInit():
	c_glInit()
def glEnable(int bits):
	c_glEnable(bits)
def glClearColor(red, green, blue, alpha):
	c_glClearColor(red, green, blue, alpha)
def glClearPolyID(ID):
	c_glClearPolyID(ID)
def glClearDepth(unsigned short depth):
	c_glClearDepth(depth)
def glFlush(unsigned int mode):
	c_glFlush(mode)
def glLoadIdentity():
	c_glLoadIdentity()
def glTranslatef(float x, float y, float z):
	c_glTranslatef(x, y, z)
def glRotateX(float angle):
	c_glRotateX(angle)
def glRotateY(float angle):
	c_glRotateY(angle)
def glBegin(int mode):
	c_glBegin(mode)
def glViewport(x1, y1, x2, y2):
	c_glViewport(x1, y1, x2, y2)
def glMatrixMode(int mode):
	c_glMatrixMode(mode)
def gluPerspective(float fovy, float aspect, float zNear, float zFar):
	c_gluPerspective(fovy, aspect, zNear, zFar)
def glOrthof32(signed int left, signed int right, signed int bottom, signed int top, signed int zNear, signed int zFar):
	c_glOrthof32(left, right, bottom, top, zNear, zFar)
def glPolyFmt(unsigned int params):
	c_glPolyFmt(params)
def glColor3f(float r, float g, float b):
	c_glColor3f(r, g, b)
def glVertex3f(float x, float y, float z):
	c_glVertex3f(x, y, z)
def glVertex3v16(short int x, short int y, short int z):
	c_glVertex3v16(x, y, z)
def glEnd():
	c_glEnd()
def glPushMatrix():
	c_glPushMatrix()
def glPopMatrix(int num):
	c_glPopMatrix(num)
def gluLookAt(float eyex, float eyey, float eyez, float lookAtx, float lookAty, float lookAtz, float upx, float upy, float upz):
	c_gluLookAt(eyex, eyey, eyez, lookAtx, lookAty, lookAtz, upx, upy, upz)
