cdef extern from "nds/ndstypes.h":
    ctypedef struct touchPosition:
        unsigned short rawx # Raw x value from the A2D
        unsigned short rawy # Raw y value from the A2D
        unsigned short px   # Processes pixel X value
        unsigned short py   # Processes pixel Y value
        unsigned short z1   # Raw cross panel resistance
        unsigned short z2   # Raw cross panel resistance

cdef extern from "nds/arm7/touch.h":
    void c_touchReadXY "touchReadXY"(touchPosition *touchPos)

def touchReadXY():
    cdef touchPosition touchPos
    c_touchReadXY(&touchPos)
    return (touchPos.rawx, touchPos.rawy, touchPos.px, touchPos.py, touchPos.z1, touchPos.z2)
