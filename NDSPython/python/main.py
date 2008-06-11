from wrap_console import *
from wrap_system import *
from wrap_video import *
from wrap_interrupts import *
from wrap_videoGL import *

wconsoleDemoInit()
wvideoSetMode(MODE_FB0)
wvramSetBankA(VRAM_A_LCD)
print "Buon PyCon Uno a tutti!"

minX = -1.5
maxX = 1.5
width = 192
height = 192
aspectRatio = 1

yScale = (maxX-minX)*(float(height)/width)*aspectRatio

for y in xrange(height):
	wvramAPutPixel(255, y, RGB15(31, 31, 31))
	for x in xrange(width):
		c = complex(minX+x*(maxX-minX)/width, y*yScale/height-yScale/2)
		z = c
		for iter in xrange(15):
			if abs(z) > 2:
				break
			z = z*z+c

		wvramAPutPixel(x, y, RGB15((iter*2 + 24)%31, (iter*2 + 8)%31, (iter*2 + 16)%31))

wvramAPutPixel(1, 1, RGB15(31, 31, 31))