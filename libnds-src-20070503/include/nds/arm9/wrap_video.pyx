def RGB15(int r, int g, int b):
	return ((r)|((g)<<5)|((b)<<10))

def RGB5(int r, int g, int b):
	return ((r)|((g)<<5)|((b)<<10))

def RGB8(int r, int g, int b):
	return (((r)>>3)|(((g)>>3)<<5)|(((b)>>3)<<10))

MODE_0_2D=      0x10000
MODE_1_2D=      0x10001
MODE_2_2D=      0x10002
MODE_3_2D=      0x10003
MODE_4_2D=      0x10004
MODE_5_2D=      0x10005

ENABLE_3D=    (1<<3)

DISPLAY_BG0_ACTIVE=    (1 << 8)
DISPLAY_BG1_ACTIVE=    (1 << 9)
DISPLAY_BG2_ACTIVE=    (1 << 10)
DISPLAY_BG3_ACTIVE=    (1 << 11)
DISPLAY_SPR_ACTIVE=    (1 << 12)
DISPLAY_WIN0_ON=       (1 << 13)
DISPLAY_WIN1_ON=       (1 << 14)
DISPLAY_SPR_WIN_ON=    (1 << 15)

MODE_0_3D=(MODE_0_2D | DISPLAY_BG0_ACTIVE | ENABLE_3D)

MODE_FB0=(0x00020000)
MODE_FB1=(0x00060000)
MODE_FB2=(0x000A0000)
MODE_FB3=(0x000E0000)

VRAM_A_LCD=0

cdef extern from "nds/arm9/video.h":
	void videoSetMode(int mode)
	void vramSetBankA(int a)

def wvideoSetMode(int mode):
	videoSetMode(mode)

def wvramSetBankA(int a):
	vramSetBankA(a)

def wvramAPutPixel(int x, int y, int color):
	cdef unsigned short *VRAM_A
	VRAM_A=<unsigned short *>0x6800000
	VRAM_A[x + 256 * y] = color