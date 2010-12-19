TIMER_HZ=(33513982)
ClockDivider_1 = 0# //!< divides the timer clock by 1 (~33513.982 kHz)
ClockDivider_64 = 1#    //!< divides the timer clock by 64 (~523.657 kHz)
ClockDivider_256 = 2#   //!< divides the timer clock by 256 (~130.914 kHz)
ClockDivider_1024 = 3#  //!< divides the timer clock by 1024 (~32.7284 kHz)
cdef extern from "nds/timers.h":
    ctypedef enum ClockDivider:
        pass
    unsigned short int c_timerElapsed "timerElapsed" (int timer)
    unsigned short int c_timerTick "timerTick" (int timer)
    unsigned short int c_timerPause "timerPause" (int timer)
    void c_timerStart "timerStart" (int timer, ClockDivider divider, unsigned short int ticks, int callback)
    void c_timerUnpause "timerUnpause" (int timer)
    unsigned short int c_timerStop "timerStop" (int timer)
    void c_cpuStartTiming "cpuStartTiming" (int timer)
    unsigned int c_cpuGetTiming "cpuGetTiming" ()
    unsigned int c_cpuEndTiming "cpuEndTiming" ()

def timerElapsed(timer):
    return c_timerElapsed(timer)
def timerTick(timer):
    return c_timerTick(timer)
def timerPause(timer):
    return c_timerPause(timer)
def timerStart(timer,divider,ticks,callback):
    c_timerStart(timer,divider,ticks,callback)
def timerUnpause(timer):
    c_timerUnpause(timer)
def timerStop(timer):
    return c_timerStop(timer)
def cpuStartTiming(timer):
    c_cpuStartTiming(timer)
def cpuGetTiming():
    return c_cpuGetTiming()
def cpuEndTiming():
    return c_cpuEndTiming()
