
// set it to 1 (align on byte)
#pragma pack (1)

char strtstr[] = "\nMTOOLS   Make DOS Image  v00.12.50    Forever Young Software 1984-2002\n";

struct BPB {
  unsigned  char jmps[2];       // The jump short instruction
  unsigned  char nop;           // nop instruction;
            char oemname[8];    // OEM name
  unsigned short nBytesPerSec;  // Bytes per sector
  unsigned  char nSecPerClust;  // Sectors per cluster
  unsigned short nSecRes;       // Sectors reserved for Boot Record
  unsigned  char nFATs;         // Number of FATs
  unsigned short nRootEnts;     // Max Root Directory Entries allowed
  unsigned short nSecs;         // Number of Logical Sectors (0B40h)
  unsigned  char mDesc;         // Medium Descriptor Byte
  unsigned short nSecPerFat;    // Sectors per FAT
  unsigned short nSecPerTrack;  // Sectors per Track
  unsigned short nHeads;        // Number of Heads
  unsigned  long nSecHidden;    // Number of Hidden Sectors
  unsigned  long nSecsExt;      // This value used when there are more
  unsigned  char DriveNum;      // Physical drive number
  unsigned  char nResByte;      // Reserved (we use for FAT type (12- 16-bit)
  unsigned  char sig;           // Signature for Extended Boot Record
  unsigned  long SerNum;        // Volume Serial Number
            char VolName[11];   // Volume Label
            char FSType[8];     // File system type
  unsigned  char filler[448];
  unsigned short boot_sig;
} bpb;

unsigned char boot_code[] = {
	0xFA,           //CLI
	0xB8,0xC0,0x07, //MOV	AX,07C0
	0x8E,0xD8,      //MOV	DS,AX
	0x8E,0xD0,      //MOV	SS,AX
	0xBC,0x00,0x40, //MOV	SP,4000
	0xFB,           //STI
	0xBE,0x6B,0x00, //MOV	SI,006B
	0xE8,0x06,0x00, //CALL	0156
	0x30,0xE4,      //XOR	AH,AH
	0xCD,0x16,      //INT	16
	0xCD,0x18,      //INT	18
	0x50,           //PUSH	AX
	0x53,           //PUSH	BX
	0x56,           //PUSH	SI
	0xB4,0x0E,      //MOV	AH,0E
	0x31,0xDB,      //XOR	BX,BX
	0xFC,           //CLD
	0xAC,           //LODSB
	0x08,0xC0,      //OR	AL,AL
	0x74,0x04,      //JZ	0167
	0xCD,0x10,      //INT	10
	0xEB,0xF6,      //JMP	015D
	0x5E,           //POP	SI
	0x5B,           //POP	BX
	0x58,           //POP	AX
	0xC3,           //RET
	13,10
};
unsigned char boot_data[] = "Error reading disk or Non-System Disk"
                            "\x0D\x0A"
                            "Press a key to reboot\x00";
