from wrap_console import *
from wrap_system import *
from wrap_video import *
from wrap_interrupts import *
from wrap_videoGL import *
from wrap_rumble import *
from wrap_touch import *

wconsoleDemoInit()
wvideoSetMode(MODE_FB0)
wvramSetBankA(VRAM_A_LCD)
print "Hello world!"

iters = 0

while 1:
	pos = wtouchReadXY()
	x, y = pos[2], pos[3]
	
	wvramAPutPixel(x, y, RGB15((iters*2 + 24)%31, (iters*2 + 8)%31, (iters*2 + 16)%31))
	
	iters += 1