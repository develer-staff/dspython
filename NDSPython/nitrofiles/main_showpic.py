from wrap_input import *
from wrap_interrupts import *
from wrap_console import *
from wrap_background import *
from wrap_video import *

videoSetMode(MODE_5_2D)
videoSetModeSub(MODE_0_2D) #//sub bg 0 will be used to print text
vramSetBankA(VRAM_A_MAIN_BG)
bg3=bgInit(3, BgType_Bmp16, BgSize_B16_256x256, 0,0)
decompress_file("color.bin",BG_GFX,LZ77Vram)

angle = 0;

scrollX = 128;
scrollY = 128 ;


scaleX = 1 << 8;
scaleY = 1 << 8;


rcX = 128;
rcY = 128;


while 1:
    scanKeys()
    keys = keysHeld()

    if( keys & KEY_L ):
        angle=angle+20;
    if( keys & KEY_R ):
        angle=angle-20;
    if( keys & KEY_LEFT ):
        scrollX=scrollX+1;
    if( keys & KEY_RIGHT ):
        scrollX=scrollX-1;
    if( keys & KEY_UP ):
        scrollY=scrollY+1;
    if( keys & KEY_DOWN ):
        scrollY=scrollY-1;
    if( keys & KEY_A ):
        scaleX=scaleX+1;
    if( keys & KEY_B ):
        scaleX=scaleX-1;
    if( keys & KEY_START ):
        rcX=rcX+1;
    if( keys & KEY_SELECT ):
        rcY=rcY-1;
    if( keys & KEY_X ):
        scaleY=scaleY+1;
    if( keys & KEY_Y ):
        scaleY=scaleY-1;


    swiWaitForVBlank();

    bgSetCenter(bg3, rcX, rcY);
    bgSetRotateScale(bg3, angle, scaleX, scaleY);
    bgSetScroll(bg3, scrollX, scrollY);
    bgUpdate();