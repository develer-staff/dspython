/* DICE demo application for embedded systems, version 1 */

#include "Python.h"

#include "stackless_api.h"


/*=== Python Code ====*/
char * python_prog = "		\
							\n\
import game					\n\
							\n\
def everySecond():   		\n\
	print 'Hello'			\n\
	game.sleepInCpp(5.0)	\n\
	print 'Goodbye'			\n\
							\n\
";
/*=====================*/

/*
 * to my understanding, the above *function* is not called
 * every second (spawning a new task all the time),
 * but the resulting tasklet is called every second, until it
 * is done.
 * So, what we are actually doing is to create a task, that
 * has to wait for some event (in this case, time passing by),
 * and then to resume.
 */


PyObject *timemod;

double pytime(void)
{
	return PyFloat_AsDouble(PyObject_CallMethod(timemod, "clock", ""));
}

void pysleep(double seconds)
{
	PyObject *ret = PyObject_CallMethod(timemod, "sleep", "f", seconds);
	Py_XDECREF(ret);
}

int wrap(PyObject *ign)
{
	Py_XDECREF(ign);
	return ign ? 0 : -1;
}

static PyObject *
sleepInCpp(PyObject *self, PyObject *seconds)
{
	double time_to_wait, wait_until;
	time_to_wait = PyFloat_AsDouble(seconds);
	if (PyErr_Occurred())
		return NULL;
	wait_until = pytime() + time_to_wait;
	while (pytime() < wait_until) {
		/* let other processes run */
		printf("sleepInCpp activated\n");
		if (wrap(PyStackless_Schedule(Py_None, 0)))
			return NULL;
	}
	Py_INCREF(Py_None);
	return Py_None;
}

static PyMethodDef game_methods[] = {
	{ "sleepInCpp", sleepInCpp, METH_O, "run the game for n seconds" },
	{ NULL, NULL }
};

/*
 * The Game Engine  (not so sophisticated :-)
 */

void run_game_engine(void)
{
	printf("Game Engine was started\n");
	while (PyStackless_GetRunCount() > 0) {
		/* note that we are not a tasklet in this context */
		printf("Game is computing for 1 second.\n");
		pysleep(1.0);
		if (wrap(PyStackless_Schedule(Py_None, 0)))
			return;
	}
	printf("Game Engine is shutting down.\n");
}

/* create a simple main program and run it, */

int
main(int argc, char **argv)
{
	PyObject *main, *game;
	PyObject *func, *args;
	PyTaskletObject *process;
	Py_SetProgramName(argv[0]);
	Py_Initialize();
	/* get the time python methods */
	timemod = PyImport_ImportModule("time");
	/* create a module for the game */
	game = Py_InitModule("game", game_methods);
	/* run the definition in main module */
	main = PyImport_AddModule("__main__");
	PyRun_SimpleString(python_prog); /* runs in main */
	/* start the python function as a tasklet */
	func = PyObject_GetAttrString(main, "everySecond");
	process = PyTasklet_New(NULL, func);
	Py_DECREF(func);
	/* initialize the tasklet args */
	args = PyTuple_New(0);
	PyTasklet_Setup(process, args, NULL);
	Py_DECREF(args);

	/* now let's run the "game engine" */
	run_game_engine();

	Py_Finalize();
	return 0;
}
