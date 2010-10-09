POWER_LCD=1
POWER_2D_A=2
POWER_MATRIX=4
POWER_3D_CORE=8
POWER_2D_B=512
POWER_SWAP_LCDS=32768

POWER_ALL_2D=(POWER_LCD |POWER_2D_A |POWER_2D_B)

POWER_ALL=(POWER_ALL_2D | POWER_3D_CORE | POWER_MATRIX)

cdef extern from "nds/system.h":
	void c_powerOn "powerOn" (int on) 
	void c_lcdMainOnBottom "lcdMainOnBottom" () 

def powerOn(on):
	c_powerOn(on)
def lcdMainOnBottom():
	c_lcdMainOnBottom()