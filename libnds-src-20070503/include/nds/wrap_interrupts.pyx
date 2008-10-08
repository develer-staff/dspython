def BIT(n):
	return 1 << n

IRQ_VBLANK=BIT(0)

cdef extern from "nds/interrupts.h":
	void c_irqInit "irqInit" ()
	void c_irqSet "irqSet" (int irq, int handler)

def irqInit():
	c_irqInit()

def irqSet(irq, handler):
	c_irqSet(irq, handler)