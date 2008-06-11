def BIT(n):
	return 1 << n

IRQ_VBLANK=BIT(0)

cdef extern from "nds/interrupts.h":
	void irqInit()
	void irqSet(int irq, int handler)

def wirqInit():
	irqInit()

def wirqSet(irq, handler):
	irqSet(irq, handler)