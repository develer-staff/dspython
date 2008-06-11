cdef extern from "nds/jtypes.h":
	ctypedef int bool

cdef extern from "nds/arm9/rumble.h":
	bool isRumbleInserted()
	void setRumble(bool position)

def wisRumbleInserted():
	return isRumbleInserted()

def wsetRumble(position):
	setRumble(position)

def vibrate(int length):
	for i in range(0,length):
		wsetRumble(True)
		wsetRumble(False)