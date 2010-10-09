cdef extern from "nds/arm9/keyboard.h":
	ctypedef struct Keyboard:
		pass
	Keyboard* c_keyboardDemoInit "keyboardDemoInit" ()
	void c_keyboardShow "keyboardShow" ()
	int c_keyboardUpdate "keyboardUpdate" ()
	
def keyboardDemoInit():
	c_keyboardDemoInit()
def keyboardShow():
	c_keyboardShow()
def keyboardUpdate():
	return c_keyboardUpdate()