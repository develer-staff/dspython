/*
	io_scsd.c 

	By chishm (Michael Chisholm)

	Hardware Routines for reading a secure digital card
	using the SuperCard

	SD routines based on sd.s by Romman 

	This software is completely free. No warranty is provided.
	If you use it, please give me credit and email me about your
	project at chishm@hotmail.com

	See gba_nds_fat.txt for help and license details.
*/


#include "io_scsd.h"

#ifdef SUPPORT_SCSD

//---------------------------------------------------------------
// SD Addresses & Commands

#define SD_COMADD (*(vu16*)(0x09800000))
#define SD_DATAADD (*(vu16*)(0x09000000))
#define SD_DATARADD_16 (*(vu16*)(0x09100000))
#define SD_DATARADD_32 (*(vu32*)(0x09100000))

// SD Card status
#define SD_STS_BUSY			0x100
#define SD_STS_INSERTED		0x300

// Improved CRC7 function provided by cory1492
u8 SCSD_CRC7(u8* data, int cnt)
{
    int i, a;
    u8 crc, temp;

    crc = 0;
    for (a = 0; a < cnt; a++)
    {
        temp = data[a];
        for (i = 0; i < 8; i++)
        {
            crc <<= 1;
            if ((temp & 0x80) ^ (crc & 0x80)) crc ^= 0x09;
            temp <<= 1;
        }
    }
    crc = (crc << 1) | 1;
    return(crc);
} 

void SCSD_WriteCommand (u8* src, int length)
{
	u16 dataByte;
	int curBit;
	while ((SD_COMADD & 0x01) == 0);
		
	dataByte = SD_COMADD;

	do {
		dataByte = *src++;
		for (curBit = 7; curBit >=0; curBit--){
			SD_COMADD = dataByte;
			dataByte = dataByte << 1;
		}
	} while (length--);
	
	return;
}

void SCSD_Command (u8 command, u8 num, u32 sector )
{
	u8 databuff[6];
	u8 *tempDataPtr = databuff;

	*tempDataPtr++ = command | 0x40;
	*tempDataPtr++ = sector>>24;
	*tempDataPtr++ = sector>>16;
	*tempDataPtr++ = sector>>8;
	*tempDataPtr++ = sector;
	*tempDataPtr = SCSD_CRC7 (databuff, 5);

	SCSD_WriteCommand (databuff, 6);
	return;
}

void SCSD_ReadCommand(u16* buff, int length)
{
	u16 temp;

	while (SD_COMADD & 0x01);
	
	length = length * 8;
	
	do {
		temp = SD_COMADD;
	} while (length--);
	
	return;
}

void SCSD_GetResp(void)
{
	SCSD_ReadCommand ( 0, 6);
}

void SCSD_SendClock(int numClocks)
{	
	u16 temp;
	do {
		temp = SD_COMADD;
	} while (numClocks--);
}	


void SCSD_ReadData(u16 *buff)
{
	u16 temp;
	u32 data_1, data_2;
	int i;
	
	while (SD_DATARADD_16 & SD_STS_BUSY);
			
	for (i = 0; i < 512; i+=2) {
		data_1 = SD_DATARADD_32;
		data_2 = SD_DATARADD_32;
		*buff++ = data_2 >> 16;
	}
	
	for (i = 0; i < 8; i++) {
		data_2 = SD_DATARADD_32;
	}
	
	temp = SD_DATARADD_16;
	
	return;
}

void SCSD_CRC16 (u8* buff, int buffLength, u8* crc16buff)
{
	u32 a, b, c, d;
	int count;
	u32 bitPattern = 0x80808080;	// r7
	u32 crcConst = 0x1021;	// r8
	u32 dataByte = 0;	// r2

	a = 0;	// r3
	b = 0;	// r4
	c = 0;	// r5
	d = 0;	// r6
	
	buffLength = buffLength * 8;
	
	
	do {
		if (bitPattern & 0x80) dataByte = *buff++;
		
		a = a << 1;
		if ( a & 0x10000) a ^= crcConst;
		if (dataByte & (bitPattern >> 24)) a ^= crcConst;
		
		b = b << 1;
		if (b & 0x10000) b ^= crcConst;
		if (dataByte & (bitPattern >> 25)) b ^= crcConst;
	
		c = c << 1;
		if (c & 0x10000) c ^= crcConst;
		if (dataByte & (bitPattern >> 26)) c ^= crcConst;
		
		d = d << 1;
		if (d & 0x10000) d ^= crcConst;
		if (dataByte & (bitPattern >> 27)) d ^= crcConst;
		
		bitPattern = (bitPattern >> 4) | (bitPattern << 28);
	} while (buffLength-=4);
	
	count = 16;	// r8
	
	do {
		bitPattern = bitPattern << 4;
		if (a & 0x8000) bitPattern |= 8;
		if (b & 0x8000) bitPattern |= 4;
		if (c & 0x8000) bitPattern |= 2;
		if (d & 0x8000) bitPattern |= 1;
	
		a = a << 1;
		b = b << 1;
		c = c << 1;
		d = d << 1;
		
		count--;
		
		if (!(count & 0x01)) {
			*crc16buff++ = (u8)(bitPattern & 0xff);
		}
	} while (count != 0);
	
	return;
}

void SCSD_WriteData (u16 *buff, u16* crc16buff)
{
	int pos;
	u16 dataHWord;
	u16 temp;
	while (SD_DATAADD & SD_STS_BUSY);
		
	temp = SD_DATAADD;
	
	SD_DATAADD = 0;		// start bit;
		
	for ( pos = BYTE_PER_READ; pos != 0; pos -=2) {
		dataHWord = *buff++;
		
		SD_DATAADD = dataHWord;
		SD_DATAADD = dataHWord << 4;
		SD_DATAADD = dataHWord << 8;
		SD_DATAADD = dataHWord << 12;
	}
	
	if (crc16buff != 0) {
		for ( pos = 8; pos != 0; pos -=2) {
			dataHWord = *crc16buff++;
			
			SD_DATAADD = dataHWord;
			SD_DATAADD = dataHWord << 4;
			SD_DATAADD = dataHWord << 8;
			SD_DATAADD = dataHWord << 12;
		}
	}
	
	SD_DATAADD = 0xff;		// end bit
	
	while (SD_DATAADD & 0x100);

	temp = SD_DATAADD;
	temp = SD_DATAADD;
	temp = SD_DATAADD;
	temp = SD_DATAADD;

	return;
}

/*-----------------------------------------------------------------
SCSD_IsInserted
Is a secure digital card inserted?
bool return OUT:  true if a CF card is inserted
-----------------------------------------------------------------*/
bool SCSD_IsInserted (void) 
{
	return ((SD_COMADD & SD_STS_INSERTED) == 0);
}


/*-----------------------------------------------------------------
SCSD_ClearStatus
Tries to make the SD card go back to idle mode
bool return OUT:  true if a CF card is idle
-----------------------------------------------------------------*/
bool SCSD_ClearStatus (void) 
{
	return false;
}


/*-----------------------------------------------------------------
SCSD_ReadSectors
Read 512 byte sector numbered "sector" into "buffer"
u32 sector IN: address of first 512 byte sector on SD card to read
u8 numSecs IN: number of 512 byte sectors to read,
 1 to 256 sectors can be read, 0 = 256
void* buffer OUT: pointer to 512 byte buffer to store data in
bool return OUT: true if successful
-----------------------------------------------------------------*/
bool SCSD_ReadSectors (u32 sector, u8 numSecs, void* buffer)
{
	int maxSectors,curSector;
	maxSectors = (numSecs == 0 ? 256 : numSecs);

	SCSD_Command (18, 0, sector << 9); 	// Read multiple blocks
	
	for (curSector=0; curSector<maxSectors; curSector++)
	{
		SCSD_ReadData((u16*)buffer + (curSector * (BYTE_PER_READ/2)));
	}
	
	SCSD_Command (12,0,0); 				// Stop transmission
	SCSD_GetResp();
	SCSD_SendClock(0x10);
	return true;
}



/*-----------------------------------------------------------------
SCSD_WriteSectors
Write 512 byte sector numbered "sector" from "buffer"
u32 sector IN: address of 512 byte sector on SC card to read
u8 numSecs IN: number of 512 byte sectors to read,
 1 to 256 sectors can be read, 0 = 256
void* buffer IN: pointer to 512 byte buffer to read data from
bool return OUT: true if successful
-----------------------------------------------------------------*/
bool SCSD_WriteSectors (u32 sector, u8 numSecs, void* buffer)
{
	int maxSectors,curSector;
	u16 crc16[5];
	maxSectors = (numSecs == 0 ? 256 : numSecs);

	sector = sector * BYTE_PER_READ;

	SCSD_Command(25,0,sector); 
	SCSD_GetResp();
	SCSD_SendClock(0x10); 

	for (curSector=0; curSector<maxSectors; curSector++)
	{
		SCSD_CRC16(((u8*)buffer) + (curSector * BYTE_PER_READ), BYTE_PER_READ, (u8*)crc16);
		SCSD_WriteData(((u16*)buffer) + (curSector * (BYTE_PER_READ/2)), crc16);
		SCSD_SendClock(0x10); 
	}
	SCSD_Command(12,0,0); 
	SCSD_GetResp();
	SCSD_SendClock(0x10);
	while((SD_DATAADD &0x0100)==0);
	return true;
}

/*-----------------------------------------------------------------
SCSD_Shutdown
unload the Supercard SD interface
-----------------------------------------------------------------*/
bool SCSD_Shutdown(void) 
{
	return SCSD_ClearStatus() ;
}

/*-----------------------------------------------------------------
SCSD_Mode (was SC_Unlock)
Added by MightyMax
Modified by Chishm
Modified again by loopy
1=ram(readonly), 5=ram, 3=SD interface?
-----------------------------------------------------------------*/
void SCSD_Mode(u8 mode)
{
	vu16 *unlockAddress = (vu16*)0x09FFFFFE;
	*unlockAddress = 0xA55A ;
	*unlockAddress = 0xA55A ;
	*unlockAddress = mode ;
	*unlockAddress = mode ;
} 

/*-----------------------------------------------------------------
SCSD_StartUp
initializes the CF interface, returns true if successful,
otherwise returns false
-----------------------------------------------------------------*/
bool SCSD_StartUp(void)
{
	vu32 *p=(u32*)0x8000000;	//see if we can write to SCSD ram
	SCSD_Mode(5);
	*p=0x5555aaaa;
	*p=~*p;
	if(*p!=0xaaaa5555)
		return false;
		
	SCSD_Mode(3);
	return SCSD_IsInserted();
}

/*-----------------------------------------------------------------
the actual interface structure
-----------------------------------------------------------------*/
IO_INTERFACE io_scsd = {
	DEVICE_TYPE_SCSD,
	FEATURE_MEDIUM_CANREAD | FEATURE_MEDIUM_CANWRITE | FEATURE_SLOT_GBA,
	(FN_MEDIUM_STARTUP)&SCSD_StartUp,
	(FN_MEDIUM_ISINSERTED)&SCSD_IsInserted,
	(FN_MEDIUM_READSECTORS)&SCSD_ReadSectors,
	(FN_MEDIUM_WRITESECTORS)&SCSD_WriteSectors,
	(FN_MEDIUM_CLEARSTATUS)&SCSD_ClearStatus,
	(FN_MEDIUM_SHUTDOWN)&SCSD_Shutdown
} ;

/*-----------------------------------------------------------------
SCSD_GetInterface
returns the interface structure to host
-----------------------------------------------------------------*/
LPIO_INTERFACE SCSD_GetInterface(void) {
	return &io_scsd ;
} ;

#endif // SUPPORT_SCSD
