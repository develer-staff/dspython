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
	void glInit()
	void glEnable(int bits)
	void glClearColor(unsigned char red, unsigned char green, unsigned char blue, unsigned char alpha)
	void glClearPolyID(unsigned char ID)
	void glClearDepth(unsigned short depth)
	void glFlush(unsigned int mode)
	void glLoadIdentity()
	void glTranslatef(float x, float y, float z)
	void glRotateX(float angle)
	void glRotateY(float angle)
	void glBegin(int mode)
	void glViewPort(unsigned char x1, unsigned char y1, unsigned char x2, unsigned char y2)
	void glMatrixMode(int mode)
	void gluPerspective(float fovy, float aspect, float zNear, float zFar)
	void glOrthof32(signed int left, signed int right, signed int bottom, signed int top, signed int zNear, signed int zFar)
	void glPolyFmt(unsigned int params)
	void glColor3f(float r, float g, float b)
	void glVertex3f(float x, float y, float z)
	void glVertex3v16(short int x, short int y, short int z)
	void glEnd()
	void glPushMatrix()
	void glPopMatrix(int num)
	void gluLookAt(float eyex, float eyey, float eyez, float lookAtx, float lookAty, float lookAtz, float upx, float upy, float upz)

def wglInit():
	glInit()
def wglEnable(int bits):
	glEnable(bits)
def wglClearColor(red, green, blue, alpha):
	glClearColor(red, green, blue, alpha)
def wglClearPolyID(ID):
	glClearPolyID(ID)
def wglClearDepth(unsigned short depth):
	glClearDepth(depth)
def wglFlush(unsigned int mode):
	glFlush(mode)
def wglLoadIdentity():
	glLoadIdentity()
def wglTranslatef(float x, float y, float z):
	glTranslatef(x, y, z)
def wglRotateX(float angle):
	glRotateX(angle)
def wglRotateY(float angle):
	glRotateY(angle)
def wglBegin(int mode):
	glBegin(mode)
def wglViewPort(x1, y1, x2, y2):
	glViewPort(x1, y1, x2, y2)
def wglMatrixMode(int mode):
	glMatrixMode(mode)
def wgluPerspective(float fovy, float aspect, float zNear, float zFar):
	gluPerspective(fovy, aspect, zNear, zFar)
def wglOrthof32(signed int left, signed int right, signed int bottom, signed int top, signed int zNear, signed int zFar):
	glOrthof32(left, right, bottom, top, zNear, zFar)
def wglPolyFmt(unsigned int params):
	glPolyFmt(params)
def wglColor3f(float r, float g, float b):
	glColor3f(r, g, b)
def wglVertex3f(float x, float y, float z):
	glVertex3f(x, y, z)
def wglVertex3v16(short int x, short int y, short int z):
	glVertex3v16(x, y, z)
def wglEnd():
	glEnd()
def wglPushMatrix():
	glPushMatrix()
def wglPopMatrix(int num):
	glPopMatrix(num)
def wgluLookAt(float eyex, float eyey, float eyez, float lookAtx, float lookAty, float lookAtz, float upx, float upy, float upz):
	gluLookAt(eyex, eyey, eyez, lookAtx, lookAty, lookAtz, upx, upy, upz)
