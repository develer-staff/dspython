/* libnds wrappers for Python */

#include <stdio.h>
#include <string.h>
#include <fat.h>

#include <Python.h>

PyMODINIT_FUNC initnds(void);
/*PyMODINIT_FUNC initndsos(void);*/
PyMODINIT_FUNC initwrap_console(void);
PyMODINIT_FUNC initwrap_system(void);
PyMODINIT_FUNC initwrap_video(void);
PyMODINIT_FUNC initwrap_interrupts(void);
PyMODINIT_FUNC initwrap_videoGL(void);
PyMODINIT_FUNC initwrap_rumble(void);
PyMODINIT_FUNC initwrap_touch(void);
PyMODINIT_FUNC initwrap_input(void);
PyMODINIT_FUNC initwrap_bios(void);

int pyMain(void) {
	FILE *fp;

	printf("Console init...\n");
	consoleDemoInit();
	printf("done\n");
	
	printf("Fat init...\n");
	fatInitDefault();
	Py_SetPythonHome("/python");
	printf("done\n");

	printf("Python init...\n");
	Py_Initialize();
	printf("done\n");

	printf("Wrappers init...\n");
	initwrap_console();
	initwrap_system();
	initwrap_video();
	initwrap_interrupts();
	initwrap_videoGL();
	initwrap_rumble();
	initwrap_touch();
    initwrap_input();
    initwrap_bios();
	printf("done\n");
	
    printf("All done. Starting execution\n");
	fp = fopen("/python/main.py", "r");
	PyRun_SimpleFile(fp, "/python/main.py");
	fclose(fp);

	return 0;
}

int main(void) {
	return pyMain();
}
