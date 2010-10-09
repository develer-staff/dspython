def RGB15(int r, int g, int b):
	return ((r)|((g)<<5)|((b)<<10))

def RGB5(int r, int g, int b):
	return ((r)|((g)<<5)|((b)<<10))

def RGB8(int r, int g, int b):
	return (((r)>>3)|(((g)>>3)<<5)|(((b)>>3)<<10))
	
SCREEN_HEIGHT=192
SCREEN_WIDTH=256




BG_PALETTE =      (0x05000000)		#/**< \brief background palette memory*/
BG_PALETTE_SUB =  (0x05000400)		#/**< \brief background palette memory (sub engine)*/

SPRITE_PALETTE= (0x05000200) 		#/**< \brief sprite palette memory*/
SPRITE_PALETTE_SUB= (0x05000600)	#/**< \brief sprite palette memory (sub engine)*/

BG_GFX=			(0x6000000)	#	/**< \brief background graphics memory*/
BG_GFX_SUB=		(0x6200000)	#	/**< \brief background graphics memory (sub engine)*/
SPRITE_GFX=			(0x6400000)	#/**< \brief sprite graphics memory*/
SPRITE_GFX_SUB=		(0x6600000)	#/**< \brief sprite graphics memory (sub engine)*/

VRAM_0 =       (0x6000000)
VRAM =         (0x6800000)


VRAM_A  =      (0x6800000) #/*!< \brief pointer to vram bank A mapped as LCD*/
VRAM_B =       (0x6820000) #/*!< \brief pointer to vram bank B mapped as LCD*/
VRAM_C  =      (0x6840000) #/*!< \brief pointer to vram bank C mapped as LCD*/
VRAM_D  =      (0x6860000) #/*!< \brief pointer to vram bank D mapped as LCD*/
VRAM_E  =      (0x6880000) #/*!< \brief pointer to vram bank E mapped as LCD*/
VRAM_F  =      (0x6890000) #/*!< \brief pointer to vram bank F mapped as LCD*/
VRAM_G  =      (0x6894000) #/*!< \brief pointer to vram bank G mapped as LCD*/
VRAM_H  =      (0x6898000) #/*!< \brief pointer to vram bank H mapped as LCD*/
VRAM_I  =      (0x68A0000) #/*!< \brief pointer to vram bank I mapped as LCD*/

OAM     =      (0x07000000) #/*!< \brief pointer to Object Attribute Memory*/
OAM_SUB  =     (0x07000400) #/*!< \brief pointer to Object Attribute Memory (Sub engine)*/




ENABLE_3D=    (1<<3)
DISPLAY_ENABLE_SHIFT= 8
DISPLAY_BG0_ACTIVE=    (1 << 8)
DISPLAY_BG1_ACTIVE=    (1 << 9)
DISPLAY_BG2_ACTIVE=    (1 << 10)
DISPLAY_BG3_ACTIVE=    (1 << 11)
DISPLAY_SPR_ACTIVE=    (1 << 12)
DISPLAY_WIN0_ON=       (1 << 13)
DISPLAY_WIN1_ON=       (1 << 14)
DISPLAY_SPR_WIN_ON=    (1 << 15)

MODE_0_2D=      0x10000
MODE_1_2D=      0x10001
MODE_2_2D=      0x10002
MODE_3_2D=      0x10003
MODE_4_2D=      0x10004
MODE_5_2D=      0x10005
MODE_6_2D=      0x10006


MODE_0_3D=(MODE_0_2D| DISPLAY_BG0_ACTIVE | ENABLE_3D)
MODE_1_3D=(MODE_1_2D| DISPLAY_BG0_ACTIVE | ENABLE_3D)
MODE_2_3D=(MODE_2_2D| DISPLAY_BG0_ACTIVE | ENABLE_3D)
MODE_3_3D=(MODE_3_2D| DISPLAY_BG0_ACTIVE | ENABLE_3D)
MODE_4_3D=(MODE_4_2D| DISPLAY_BG0_ACTIVE | ENABLE_3D)
MODE_5_3D=(MODE_5_2D| DISPLAY_BG0_ACTIVE | ENABLE_3D)
MODE_6_3D=(MODE_6_2D| DISPLAY_BG0_ACTIVE | ENABLE_3D)


MODE_FIFO=(3<<16)
MODE_FB0=(0x00020000)
MODE_FB1=(0x00060000)
MODE_FB2=(0x000A0000)
MODE_FB3=(0x000E0000)

VRAM_A_LCD				= 0#					//!< maps vram a to lcd.
VRAM_A_MAIN_BG				= 1#					//!< maps vram a to main engine background slot 0.
VRAM_A_MAIN_BG_0x06000000		= 1 | 0<<3#	//!< maps vram a to main engine background slot 0.
VRAM_A_MAIN_BG_0x06020000		= 1 | 1<<3#	//!< maps vram a to main engine background slot 1.
VRAM_A_MAIN_BG_0x06040000		= 1 | 2<<3#	//!< maps vram a to main engine background slot 2.
VRAM_A_MAIN_BG_0x06060000		= 1 | 3<<3#	//!< maps vram a to main engine background slot 3.
VRAM_A_MAIN_SPRITE			= 2#					//!< maps vram a to main engine sprites slot 0.
VRAM_A_MAIN_SPRITE_0x06400000		= 2 | 0<<3#	//!< maps vram a to main engine sprites slot 0.
VRAM_A_MAIN_SPRITE_0x06420000		= 2 | 1<<3#	//!< maps vram a to main engine sprites slot 1.
VRAM_A_TEXTURE				= 3#					//!< maps vram a to 3d texture slot 0.
VRAM_A_TEXTURE_SLOT0			= 3 | 0<<3#	//!< maps vram a to 3d texture slot 0.
VRAM_A_TEXTURE_SLOT1			= 3 | 1<<3#	//!< maps vram a to 3d texture slot 1.
VRAM_A_TEXTURE_SLOT2			= 3 | 2<<3#	//!< maps vram a to 3d texture slot 2.
VRAM_A_TEXTURE_SLOT3			= 3 | 3<<3#	//!< maps vram a to 3d texture slot 3.
		
cdef extern from "nds/arm9/video.h":
	void c_videoSetMode "videoSetMode" (int mode)
	void c_vramSetBankA "vramSetBankA" (int a)
	void c_videoSetModeSub "videoSetModeSub" (int mode)

def videoSetMode(int mode):
	c_videoSetMode(mode)
	
def videoSetModeSub(int mode):
	c_videoSetModeSub(mode)

def vramSetBankA(int a):
	c_vramSetBankA(a)

def vramAPutPixel(int x, int y, int color):
	cdef unsigned short *pVRAM_A
	pVRAM_A=<unsigned short *>VRAM_A
	pVRAM_A[x + 256 * y] = color