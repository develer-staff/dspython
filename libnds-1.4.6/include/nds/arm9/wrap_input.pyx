def BIT(n):
	return 1 << n

KEY_A      = BIT(0)  #!< Keypad A button.
KEY_B      = BIT(1)  #!< Keypad B button.
KEY_SELECT = BIT(2)  #!< Keypad SELECT button.
KEY_START  = BIT(3)  #!< Keypad START button.
KEY_RIGHT  = BIT(4)  #!< Keypad RIGHT button.
KEY_LEFT   = BIT(5)  #!< Keypad LEFT button.
KEY_UP     = BIT(6)  #!< Keypad UP button.
KEY_DOWN   = BIT(7)  #!< Keypad DOWN button.
KEY_R      = BIT(8)  #!< Right shoulder button.
KEY_L      = BIT(9)  #!< Left shoulder button.
KEY_X      = BIT(10) #!< Keypad X button.
KEY_Y      = BIT(11) #!< Keypad Y button.
KEY_TOUCH  = BIT(12) #!< Touchscreen pendown.
KEY_LID    = BIT(13) #!< Lid state.


cdef extern from "nds/touch.h":
	ctypedef struct touchPosition:
		short unsigned rawx
		short unsigned rawy
		short unsigned px
		short unsigned py
		short unsigned z1
		short unsigned z2

cdef extern from "nds/arm9/input.h":
	void c_scanKeys "scanKeys" ()
	unsigned int c_keysHeld "keysHeld" ()
	unsigned int c_keysCurrent "keysCurrent" ()
	unsigned int c_keysDown "keysDown" ()
	unsigned int c_keysDownRepeat "keysDownRepeat" ()
	void c_keysSetRepeat "keysSetRepeat" (unsigned char setDelay, unsigned char setRepeat)
	unsigned int c_keysUp "keysUp" ()
	void c_touchRead "touchRead" (touchPosition *data)
	
def scanKeys():
	c_scanKeys()

def keysHeld():
	return c_keysHeld()
	
def keysCurrent():
	return c_keysCurrent()
	
def keysDown():
	return c_keysDown()
	
def keysDownRepeat():
	return c_keysDownRepeat()
	
def keysSetRepeat(setDelay,setRepeat):
	c_keysSetRepeat(setDelay,setRepeat)
	
def keysUp():
	return c_keysUp()
	
def touchRead():
	cdef touchPosition data
	c_touchRead(&data)
	return (data.rawx,data.rawy,data.px,data.py,data.z1,data.z2)