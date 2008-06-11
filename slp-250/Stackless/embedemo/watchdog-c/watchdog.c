/*
  A simple example of using the watchdog in C.
  Implements the BeNice yielding method in the soft switching manner
  so tasklets which are blocked on it can be pickled.
*/

#include "Python.h"
#include "stackless_api.h"

PyChannelObject *niceChannel;

PyObject *BeNice(PyObject *self) {
	PyObject *ret;
	/* By using PyChannel_Receive_nr to block the current tasklet on
	   the channel, we ensure that soft switching is used (we can
	   check this by looking at what is returned and making sure it
	   is the unwind token. */
	ret = PyChannel_Receive_nr(niceChannel);
	assert(ret == (PyObject *)Py_UnwindToken);
	return ret;
}

static PyMethodDef util_methods[] = {
	{ "BeNice", (PyCFunction)BeNice, METH_NOARGS, "Yield the tasklet." },
	{ NULL, NULL }
};

void CheckForErrors() {
	if (PyErr_Occurred() != NULL) {
		PyErr_Print();
		PyErr_Clear();
	}
}

int main(int argc, char **argv)
{
	PyObject *gameModule, *utilModule, *func, *ret, *args;
	PyTaskletObject *tasklet;
	int i;

	Py_SetProgramName(argv[0]);
	Py_Initialize();

	niceChannel = PyChannel_New(NULL);

	utilModule = Py_InitModule("util", util_methods);
	gameModule = PyImport_ImportModule("game");
	if (gameModule == NULL) {
		CheckForErrors();
	}

	/*
	Allow the startup script "game.py" to start some
	tasklets in its Run method.  I initially tried calling
	it directly as a function but it seemed to be called
	twice.
	*/
	func = PyObject_GetAttrString(gameModule, "Run");
	if (func == NULL) {
		CheckForErrors();
	}
	tasklet = PyTasklet_New(NULL, func);
	Py_DECREF(func);
	PyTasklet_SetBlockTrap(tasklet, 1);
	args = PyTuple_New(0);
	PyTasklet_Setup(tasklet, args, NULL);
	Py_DECREF(args);
	PyTasklet_Run(tasklet);

	while (1) {
		for (i = niceChannel->balance; i < 0; i++) {
			PyChannel_Send(niceChannel, Py_None);
			CheckForErrors();
		}

		do {
			ret = PyStackless_RunWatchdog(2000000);
			if (ret != NULL && ret != Py_None) {
				PyTasklet_Kill((PyTaskletObject *)ret);
				CheckForErrors();
			}
			Py_XDECREF(ret);
		} while (!ret);
		CheckForErrors();
	}

	Py_DECREF(utilModule);
	Py_DECREF(gameModule);

	Py_DECREF(niceChannel);

	Py_Finalize();
	return 0;
}
