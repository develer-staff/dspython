def BIT(n):
    return 1 << n

KEY_A      = BIT(0)  #!< Keypad A button.
KEY_B      = BIT(1)  #!< Keypad B button.
KEY_SELECT = BIT(2)  #!< Keypad SELECT button.
KEY_START  = BIT(3)  #!< Keypad START button.
KEY_RIGHT  = BIT(4)  #!< Keypad RIGHT button.
KEY_LEFT   = BIT(5)  #!< Keypad LEFT button.
KEY_UP     = BIT(6)  #!< Keypad UP button.
KEY_DOWN   = BIT(7)  #!< Keypad DOWN button.
KEY_R      = BIT(8)  #!< Right shoulder button.
KEY_L      = BIT(9)  #!< Left shoulder button.
KEY_X      = BIT(10) #!< Keypad X button.
KEY_Y      = BIT(11) #!< Keypad Y button.
KEY_TOUCH  = BIT(12) #!< Touchscreen pendown.
KEY_LID    = BIT(13) #!< Lid state.
    
cdef extern from "nds/arm9/input.h":
    void c_scanKeys "scanKeys" ()
    unsigned int c_keysHeld "keysHeld" ()

def scanKeys():
    c_scanKeys()

def keysHeld():
    return c_keysHeld()
