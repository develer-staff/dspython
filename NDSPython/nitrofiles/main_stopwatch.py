from wrap_input import *
from wrap_interrupts import *
from wrap_console import *
from wrap_timers import *

TIMER_SPEED=TIMER_HZ/1024
timerState_Stop=0
timerState_Pause=1
timerState_Running=2
consoleDemoInit();

ticks = 0;
state = timerState_Stop;
down = keysDown();

while not(down & KEY_START):
    swiWaitForVBlank();
    consoleClear();
    scanKeys();
    down = keysDown();
    if(state == timerState_Running):
        ticks =ticks+timerElapsed(0);
    if(down & KEY_A):
        if(state == timerState_Stop):
            timerStart(0, ClockDivider_1024, 0, 0);
            state = timerState_Running;
        elif(state == timerState_Pause):
            timerUnpause(0);
            state = timerState_Running;
        elif(state == timerState_Running):
            ticks = ticks+timerPause(0);
            state = timerState_Pause;
    elif(down & KEY_B):
        timerStop(0);
        ticks = 0;
        state = timerState_Stop;
    print ("Press A to start and pause the \ntimer, B to clear the timer \nand start to quit the program.\n\n");
    print "ticks:  %u\n" % ticks
    print ("second: %u:%u\n" % (ticks/TIMER_SPEED, ((ticks%TIMER_SPEED)*1000) /TIMER_SPEED))
if(state != timerState_Stop):
    timerStop(0);
