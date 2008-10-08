CONSOLE_USE_COLOR255 = 16

cdef extern from "nds/arm9/console.h":

	#/*! \fn void consoleDemoInit(void)
	#\brief Initialize the console to a default state for prototyping.
	#This function sets the console to use sub display, VRAM_C, and BG0 and enables MODE_0_2D on the
	#sub display.  It is intended for use in prototyping applications which need print ability and not actual
	#game use.  Print functionality can be utilized with just this call.
	#*/
	void c_consoleDemoInit "consoleDemoInit" ()

	#/*! \fn void consoleClear(void)
	#\brief Clears the screan by iprintf("\x1b[2J");
	#*/
	void c_consoleClear "consoleClear" ()

def consoleDemoInit():
	c_consoleDemoInit()
