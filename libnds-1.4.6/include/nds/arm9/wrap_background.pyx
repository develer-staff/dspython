BgType_Text8bpp=0 #	//!< 8bpp Tiled background with 16 bit tile indexes and no allowed rotation or scaling
BgType_Text4bpp=1 #	//!< 4bpp Tiled background with 16 bit tile indexes and no allowed rotation or scaling
BgType_Rotation=2 #	//!< Tiled background with 8 bit tile indexes Can be scaled and rotated
BgType_ExRotation=3 # 	//!< Tiled background with 16 bit tile indexes Can be scaled and rotated
BgType_Bmp8=4 #	//!< Bitmap background with 8 bit color values which index into a 256 color palette
BgType_Bmp16=5 # 		//!< Bitmap background with 16 bit color values of the form aBBBBBGGGGGRRRRR (if 'a' is set the pixel will be rendered...if not the pixel will be transparent)


BgSize_R_128x128 =   (0 << 14)  #/*!< 128 x 128 pixel rotation background */
BgSize_R_256x256 =   (1 << 14)  #/*!< 256 x 256 pixel rotation background */
BgSize_R_512x512 =   (2 << 14)  #/*!< 512 x 512 pixel rotation background */
BgSize_R_1024x1024 = (3 << 14)  #/*!< 1024 x 1024 pixel rotation background */

BgSize_T_256x256 = (0 << 14) | (1 << 16)  #/*!< 256 x 256 pixel text background */
BgSize_T_512x256 = (1 << 14) | (1 << 16)  #/*!< 512 x 256 pixel text background */
BgSize_T_256x512 = (2 << 14) | (1 << 16)  #/*!< 256 x 512 pixel text background */
BgSize_T_512x512 = (3 << 14) | (1 << 16)  #/*!< 512 x 512 pixel text background */

BgSize_ER_128x128 = (0 << 14) | (2 << 16)  #/*!< 128 x 128 pixel extended rotation background */
BgSize_ER_256x256 = (1 << 14) | (2 << 16)  #/*!< 256 x 256 pixel extended rotation background */
BgSize_ER_512x512 = (2 << 14) | (2 << 16)  #/*!< 512 x 512 pixel extended rotation background */
BgSize_ER_1024x1024 = (3 << 14) | (2 << 16)  #/*!< 1024 x 1024 extended pixel rotation background */

BgSize_B8_128x128 =  ((0 << 14) | (1<<7) | (3 << 16))  # /*!< 128 x 128 pixel 8 bit bitmap background */
BgSize_B8_256x256 =  ((1 << 14) | (1<<7) | (3 << 16))  # /*!< 256 x 256 pixel 8 bit bitmap background */
BgSize_B8_512x256 =  ((2 << 14) | (1<<7) | (3 << 16))  # /*!< 512 x 256 pixel 8 bit bitmap background */
BgSize_B8_512x512 =  ((3 << 14) | (1<<7) | (3 << 16))  # /*!< 512 x 512 pixel 8 bit bitmap background */
BgSize_B8_1024x512 = (1 << 14) | (3 << 16)  #		    	/*!< 1024 x 512 pixel 8 bit bitmap background */
BgSize_B8_512x1024 = (0) | (3 << 16)  #					/*!< 512 x 1024 pixel 8 bit bitmap background */

BgSize_B16_128x128 = ((0 << 14) | (1<<7) | (1<<2) | (4 << 16))  # /*!< 128 x 128 pixel 16 bit bitmap background */
BgSize_B16_256x256 = ((1 << 14) | (1<<7) | (1<<2) | (4 << 16))  # /*!< 256 x 256 pixel 16 bit bitmap background */
BgSize_B16_512x256 = ((2 << 14) | (1<<7) | (1<<2) | (4 << 16))  # /*!< 512 x 512 pixel 16 bit bitmap background */
BgSize_B16_512x512 = ((3 << 14) | (1<<7) | (1<<2) | (4 << 16))  # /*!< 1024 x 1024 pixel 16 bit bitmap background */


LZ77=0 # 		//!< LZ77 decompression.
LZ77Vram=1 #	//!< vram safe LZ77 decompression.
HUFF=2 #	//!< vram safe huff decompression.
RLE=3 #		//!< run length encoded decompression.
RLEVram=4  #		//!< vram safe run length encoded decompression.

cdef extern from "nds/arm9/background.h":
	ctypedef enum BgType:
		pass
	ctypedef enum BgSize:
		pass
	int c_bgInit "bgInit" (int layer, BgType type_bg, BgSize size_bg, int mapBase, int tileBase)
	void c_bgSetCenter "bgSetCenter" (int id, int x, int y)
	void c_bgSetScroll "bgSetScroll" (int id, int x, int y)
	void c_bgSetRotateScale "bgSetRotateScale" (int id, int angle, int sx, int sy)
	void c_bgUpdate "bgUpdate" ()
cdef extern from "nds/arm9/decompress.h":
	ctypedef enum DecompressType:
		pass
		
cdef extern from "C:/devkitPro/dspython/NDSpython/arm9/source/extern.h":
	void c_decompress_file "decompress_file" (char *filename,unsigned int dst,DecompressType type_de)
	
def bgInit(layer,type_bg,size_bg,mapBase,tileBase):
	return c_bgInit(layer,type_bg,size_bg,mapBase,tileBase)
	
def bgSetCenter(id,x,y):
	c_bgSetCenter(id,x,y)
	
def bgSetScroll(id,x,y):
	c_bgSetScroll(id,x,y)
	
def bgSetRotateScale(id,angle,sx,sy):
	c_bgSetRotateScale(id,angle,sx,sy)
	
def bgUpdate():
	c_bgUpdate()
	
def decompress_file(filename,dst,type_de):
	c_decompress_file(filename,dst,type_de)







