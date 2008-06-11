cdef extern from "nds/jtypes.h":
	ctypedef struct touchPosition:
		short int x
		short int y
		short int px
		short int py
		short int z1
		short int z2

cdef extern from "nds/arm7/touch.h":
	touchPosition touchReadXY()

def wtouchReadXY():
	cdef touchPosition pos
	pos = touchReadXY()
	return (pos.x, pos.y, pos.px, pos.py, pos.z1, pos.z2)
