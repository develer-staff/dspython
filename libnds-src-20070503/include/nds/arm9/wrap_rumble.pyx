cdef extern from "nds/jtypes.h":
	ctypedef int bool

cdef extern from "nds/arm9/rumble.h":
	bool c_isRumbleInserted "isRumbleInserted" ()
	void c_setRumble "setRumble" (bool position)

def isRumbleInserted():
	return c_isRumbleInserted()

def setRumble(position):
	c_setRumble(position)

def vibrate(int length):
	for i in range(0, length):
		setRumble(True)
		setRumble(False)