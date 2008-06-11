//////////////////////////////////////////////////////////////////////
// Extended Keyboard Example v1.0 - By Headspin
//////////////////////////////////////////////////////////////////////

#include <stdio.h>
#include <string.h>
#include <nds.h>
#include <nds/arm9/console.h>	//basic print funcionality
#include <nds/arm9/sound.h>	// sound functions
#include <fat.h>

#include <Python.h>

#include "keyboard.h"

#define PEN_DOWN (~IPC->buttons & (1 << 6))

#define X_KEY (~IPC->buttons & (1 << 0))
#define Y_KEY (~IPC->buttons & (1 << 1))

#define ABS(a) (((a) < 0) ? -(a) : (a))
#define	ROUND(f) ((u32) ((f) < 0.0 ? (f) - 0.5 : (f) + 0.5))

#define ECHO_ON	 0
#define ECHO_OFF 1

#define MAX_TEXT 256

void cf0_init();

PyMODINIT_FUNC initnds(void);
/*PyMODINIT_FUNC initndsos(void);*/

void waitForVBlank() {
	while(!(REG_DISPSTAT & DISP_IN_VBLANK));
	while((REG_DISPSTAT & DISP_IN_VBLANK));
}

int main(void) {
	char keyBuffer[MAX_TEXT] = "";
	char pleaseWaitText[] = "... importing 'site' ...";
	int i;

	//irqs are nice
	//irqInitHandler(irqDefaultHandler);
	//irqSet(IRQ_VBLANK, 0);

	//set the mode for 2 text layers and two extended background layers
	videoSetMode(MODE_5_2D | DISPLAY_BG3_ACTIVE);

	//set the sub background up for text display (we could just print to one
	//of the main display text backgrounds just as easily
	videoSetModeSub(MODE_0_2D | DISPLAY_BG0_ACTIVE); //sub bg 0 will be used to print text

	//set the first bank as background memory and the third as sub background memory
	//B and D are not used (if you want a bitmap greater than 256x256 you will need more
	//memory so another vram bank must be used and mapped consecutivly
	vramSetMainBanks(VRAM_A_MAIN_BG_0x6000000, VRAM_B_MAIN_BG_0x6020000, // VRAM_B_LCD
			VRAM_C_SUB_BG , VRAM_D_LCD);

	////////////////set up text background for text/////////////////////
	SUB_BG0_CR = BG_MAP_BASE(31);

	BG_PALETTE_SUB[255] = RGB15(31,31,31);//by default font will be rendered with color 255

	//consoleInit() is a lot more flexible but this gets you up and running quick
	consoleInitDefault((u16*)SCREEN_BASE_BLOCK_SUB(31), (u16*)CHAR_BASE_BLOCK_SUB(0), 16);

	///////////////set up our bitmap background///////////////////////

	BG3_CR = BG_BMP16_256x256;

	lcdSwap();
	initKeyboard();

    iprintf("Python %s on %s\n", Py_GetVersion(), Py_GetPlatform());
    iprintf(pleaseWaitText);

	/* This needs to be initialised before Python is, so the
	   import paths can actually be located. */
	if (fatInitDefault()) {
		// Success
	} else {
		// Failure
	}

	Py_SetPythonHome("/python");

	/* Py_VerboseFlag = 3; */
    Py_Initialize();

	for (i = 0; i < strlen(pleaseWaitText); i++)
		iprintf("\x1b[1D \x1b[1D");

	/* Register our custom modules.
	initnds();
	initndsos();
	*/

	iprintf("> ");

	while (1) {
		scanKeys();

		if(processKeyboard(&keyBuffer[0], MAX_TEXT, ECHO_ON)=='\n') {
			// We have a line of input!  Try and evaluate it or something.
            PyRun_SimpleString(keyBuffer);
			strcpy(keyBuffer, "");
            iprintf("> ");
		}

		waitForVBlank();
	}
	return 0;
}
