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

int pyMain(void) {
	FILE *fp;

	fatInitDefault();
	Py_SetPythonHome("/python");
	Py_Initialize();

	initwrap_console();
	initwrap_system();
	initwrap_video();
	initwrap_interrupts();
	initwrap_videoGL();

	fp = fopen("/python/main.py", "r");
	PyRun_SimpleFile(fp, "/python/main.py");
	fclose(fp);

	return 0;
}

int main(void) {
	return pyMain();
}
