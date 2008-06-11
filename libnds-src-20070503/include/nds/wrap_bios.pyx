cdef extern from "nds/bios.h":
	void swiWaitForVBlank()

def wswiWaitForVBlank():
	swiWaitForVBlank()
