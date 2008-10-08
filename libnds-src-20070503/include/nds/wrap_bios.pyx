cdef extern from "nds/bios.h":
	void c_swiWaitForVBlank "swiWaitForVBlank" ()

def swiWaitForVBlank():
	c_swiWaitForVBlank()
