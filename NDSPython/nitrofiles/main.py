from wrap_console import *
from wrap_interrupts import *
from wrap_keyboard import *
import sys

consoleDemoInit();
print keyboardDemoInit();
keyboardShow();
while(1):
    key = keyboardUpdate();
    if(key > 0):
        sys.stdout.write("%c" % key)
    swiWaitForVBlank();