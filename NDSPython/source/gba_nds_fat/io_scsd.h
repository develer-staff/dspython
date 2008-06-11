/*
	io_scsd.h 

	Hardware Routines for reading a Secure Digital card
	using the Supercard SD

	This software is completely free. No warranty is provided.
	If you use it, please give me credit and email me about your
	project at chishm@hotmail.com

	See gba_nds_fat.txt for help and license details.
*/

#ifndef IO_SCSD_H
#define IO_SCSD_H

// 'SCSD'
#define DEVICE_TYPE_SCSD 0x44534353

#include "disc_io.h"

// export interface
extern LPIO_INTERFACE SCSD_GetInterface(void) ;

#endif	// define IO_SCSD_H
