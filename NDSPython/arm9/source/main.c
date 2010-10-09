/* libnds wrappers for Python */

#include <stdio.h>
#include <string.h>
#include <fat.h>
#include <Python.h>
#include <nds.h>
#include <filesystem.h>

#define STATE_RUN 1
#define STATE_EXIT 0
#define MAXBUFLEN 1024*5
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

void moveCursorLeft(u32 times);
void moveCursorRight(u32 times);
void clearBuf(char *buf,u32 len);
char inputBuf[MAXBUFLEN]={0};
int i=0;

int pyMain_nitro(void) {
	
	lcdMainOnBottom();
	videoSetMode(MODE_0_2D);//set main screen 2d mode
	consoleDemoInit();  //setup the sub screen for printing
	//Keyboard *  keyboardInit (Keyboard *keyboard, int layer, BgType type, BgSize size, int mapBase, int tileBase, bool mainDisplay, bool loadGraphics) 
	keyboardInit (NULL,3, BgType_Text4bpp,BgSize_T_256x512,20, 0,true,true);
	keyboardShow();
	//FILE *fp;
	//consoleDemoInit();
	
	printf("console init\n");
	printf("done\n");
	if (nitroFSInit()) {
		printf("nitroFSInit is done\n");
	}
	else
		printf("nitro isnt ok\n");
	
	Py_SetPythonHome("/python");
	printf("PythonHome=/python\n");

	printf("Python init...\n");
	Py_Initialize();
	if ( !Py_IsInitialized() )  
	{
		iprintf("Python can't initialize!\n");
		return -1;
	}
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
	initwrap_background();
	initwrap_timers();
	initwrap_keyboard();
	printf("done\n");
	printf("All done. Starting execution\n");
	consoleClear();
	int key=0,len=0,j=0;
	u8 flag_show=1,frame=0,state=STATE_EXIT,count=0;
	while(1) {
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
		else
		{
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
	
	//fp = fopen("main.py", "rb");
	//PyRun_SimpleFile(fp, "main.py");
	//fclose(fp);
	//while(1){
	//	swiWaitForVBlank();
	//	}
	return 0;
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
/*u8 getCurLoc(u32 cur_index)
{
	u32 j=cur_index;
	int n=-1;
	while(inputBuf[j]!='\n')
	{
		if(j==0)
		j--;
		n++;
	}
	return n;
}*/
	
int pyMain_fat(void){
	FILE *fp;
	
	consoleDemoInit();
	printf("console init\n");
	printf("done\n");
	if (fatInitDefault()) {
		printf("fat is done");
	}
	else
		printf("fat isnt ok\n");
	
	Py_SetPythonHome("/python");
	printf("done\n");

	printf("Python init...\n");
	Py_Initialize();
	printf("done\n");

	printf("Wrappers init...\n");
	initnds();
	//initndsos();
	initwrap_console();
	initwrap_system();
	initwrap_video();
	initwrap_interrupts();
	initwrap_videoGL();
	initwrap_rumble();
        initwrap_input();
	printf("done\n");
	printf("All done. Starting execution\n");
	fp = fopen("main.py", "rb");
	PyRun_SimpleFile(fp, "main.py");
	fclose(fp);
	while(1){
		swiWaitForVBlank();
		}
	return 0;
	}

int main(void) {
	return pyMain_nitro();
	//return pyMain_fat();
}
