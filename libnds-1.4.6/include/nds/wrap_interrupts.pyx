def BIT(n):
	return 1 << n

IRQ_VBLANK=BIT(0) #vertical blank interrupt mask */
IRQ_HBLANK=BIT(1) #horizontal blank interrupt mask */
IRQ_VCOUNT=BIT(2) #vcount match interrupt mask */
IRQ_TIMER0=BIT(3) #timer 0 interrupt mask */
IRQ_TIMER1=BIT(4) #timer 1 interrupt mask */
IRQ_TIMER2=BIT(5) #timer 2 interrupt mask */
IRQ_TIMER3=BIT(6) #timer 3 interrupt mask */
IRQ_NETWORK=BIT(7) #serial interrupt mask */
IRQ_DMA0=BIT(8)  #DMA 0 interrupt mask */
IRQ_DMA1=BIT(9)  #DMA 1 interrupt mask */
IRQ_DMA2=BIT(10) #DMA 2 interrupt mask */
IRQ_DMA3=BIT(11) #DMA 3 interrupt mask */
IRQ_KEYS=BIT(12) #Keypad interrupt mask */
IRQ_CART=BIT(13) #GBA cartridge interrupt mask */
IRQ_IPC_SYNC=BIT(16)            #IPC sync interrupt mask */
IRQ_FIFO_EMPTY=BIT(17)          #Send FIFO empty interrupt mask */
IRQ_FIFO_NOT_EMPTY=BIT(18)      #Receive FIFO not empty interrupt mask */
IRQ_CARD=BIT(19)                #interrupt mask DS Card Slot*/
IRQ_CARD_LINE=BIT(20)           #interrupt mask */
IRQ_GEOMETRY_FIFO=BIT(21)	#geometry FIFO interrupt mask */
IRQ_LID	=BIT(22)	        #interrupt mask DS hinge*/
IRQ_SPI	=BIT(23)	        #SPI interrupt mask */
IRQ_WIFI=BIT(24)	        #WIFI interrupt mask (ARM7)*/
IRQ_ALL	=(~0)		        #'mask' for all interrupt */

ctypedef int VoidFn
ctypedef int u32
cdef extern from "nds/interrupts.h":
	void c_irqInit "irqInit" ()
	void c_irqSet "irqSet" (u32 irq, VoidFn handler)
	void c_swiWaitForVBlank "swiWaitForVBlank" () 

def irqInit():
	c_irqInit()

def irqSet(irq, handler):
	c_irqSet(irq, handler)
def swiWaitForVBlank():
	c_swiWaitForVBlank()