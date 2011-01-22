// Main executable.
// Runs /python/main.py if it exists, displays
// an interactive keyboard otherwise.

#include <stdio.h>
#include <string.h>
#include <Python.h>
#include <nds.h>

#define USE_FAT 1

#ifdef USE_FAT
#include <fat.h>
#else
#include <filesystem.h>
#endif

PyMODINIT_FUNC initnds(void);
PyMODINIT_FUNC initndsos(void);
PyMODINIT_FUNC initwrap_console(void);
PyMODINIT_FUNC initwrap_system(void);
PyMODINIT_FUNC initwrap_video(void);
PyMODINIT_FUNC initwrap_interrupts(void);
PyMODINIT_FUNC initwrap_videoGL(void);
PyMODINIT_FUNC initwrap_rumble(void);
PyMODINIT_FUNC initwrap_input(void);
PyMODINIT_FUNC initwrap_background(void);
PyMODINIT_FUNC initwrap_timers(void);
PyMODINIT_FUNC initwrap_keyboard(void);

// Keyboard functions
void moveCursorLeft(u32 times);
void moveCursorRight(u32 times);
void clearBuf(char *buf,u32 len);

// Keyboard buffer
#define MAXBUFLEN (1024*5)
char inputBuf[MAXBUFLEN] = {0};

// Keyboard offset
int i = 0;

void run_keyboard(void)
{
	const int STATE_RUN = 1;
	const int STATE_EXIT = 0;
	
	lcdMainOnBottom();
	videoSetMode(MODE_0_2D);
	keyboardInit(NULL, 3, BgType_Text4bpp, BgSize_T_256x512, 20, 0, true, true);
	keyboardShow();

	consoleClear();

	int key=0,len=0,j=0;
	u8 flag_show=1,frame=0,state=STATE_EXIT,count=0;
	while(1)
	{
		swiWaitForVBlank();
		frame++;
		key = keyboardUpdate();
		consoleClear();
		if(key>0)
		{
			len=strlen(inputBuf);
			if(key==DVK_BACKSPACE)
			{
				for(j=i+1;j<=len;j++)
				{
					inputBuf[j-1]=inputBuf[j];
				}
				i--;
				if(i<0)i=0;
			}
			else
			{
				inputBuf[i]=key;
				i++;
				if(len-1>=i)
				{
					for(j=len-1;j>=i;j--)
					{
						inputBuf[j+1]=inputBuf[j];
					}
				}
			}
		}
		else if(key==DVK_LEFT)
		{
			moveCursorLeft(1);
		}
		else if(key==DVK_RIGHT)
		{
			moveCursorRight(1);
		}
		else if(key==DVK_UP)
		{
			moveCursorLeft(32);
		}
		else if(key==DVK_DOWN)
		{
			moveCursorRight(32);
		}
		else if(key==DVK_CTRL)
		{
			i=0;
			clearBuf(inputBuf,MAXBUFLEN);
		}
		else if(key==DVK_MENU)
		{
			state=STATE_RUN;
			count=0;
			while(state)
			{
				swiWaitForVBlank();
				if(count==0)
				{
					iprintf("run!\n");
					inputBuf[i]=0;
					PyRun_SimpleString(inputBuf);
					count=1;
				}
				key = keyboardUpdate();
				if(key==DVK_MENU)
				{
					state=STATE_EXIT;
					consoleClear();
				}
			}
		}
		
		if(flag_show)
		{
			inputBuf[i]='_';
		}
		else
		{
			inputBuf[i]=' ';
		}
		if(frame==35)
		{
			flag_show=1-flag_show;//swap
			frame=0;
		}
		iprintf("%s",inputBuf);
    }
}
void clearBuf(char *buf,u32 len)
{
	u32 j=0;
	for(j=0;j<len;j++)buf[j]=0;
}
void moveCursorLeft(u32 times)
{
	u32 n=0;
	for(n=0;n<times;n++)
	{
		if(i==0)break;
		i--;
		inputBuf[i+1]=inputBuf[i];
		if(inputBuf[i]=='\n')break;
	}
}
void moveCursorRight(u32 times)
{
	u32 n=0;
	for(n=0;n<times;n++)
	{
		if(inputBuf[i+1]==0)break;
		i++;
		inputBuf[i-1]=inputBuf[i];
		if(inputBuf[i]=='\n')break;
	}
}

// Common initialization code.  Must init the fs interface even if
// it's going to use the interactive keyboard, because the
// interpreter will load the Python libraries (if any) from the fs.
void init(void)
{
	int fs_init = 0;

	consoleDemoInit();
	printf("Console init OK\n");
	
#ifdef USE_FAT
	fs_init = fatInitDefault();
#else
	fs_init = nitroFSInit();
#endif

	if (fs_init)
		printf("Fat init OK\n");
	else
		printf("Fat init failed!\n");

	Py_SetPythonHome("/python");
	printf("PYTHONHOME set to /python\n");

	printf("Python init...\n");
	Py_Initialize();
	printf("done\n");

	printf("Wrappers init...\n");
	initnds();
	initndsos();
	initwrap_console();
	initwrap_system();
	initwrap_video();
	initwrap_interrupts();
	initwrap_videoGL();
	initwrap_rumble();
	initwrap_input();
	printf("done\n");

	printf("Starting execution\n");
}

int main(void)
{
	FILE *fp;

	init();
	
	fp = fopen("/python/main.py", "rb");
	if (fp) {
		PyRun_SimpleFile(fp, "/python/main.py");
		fclose(fp);
	} else {
		printf("Unable to find /python/main.py\n");
		run_keyboard();
	}
	return 0;
}
