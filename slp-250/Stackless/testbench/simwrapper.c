#define simwrapperCPP
#include "simwrapper.h"

#include "stackless_api.h"

static int fs_wrapper_init = 1;


int PendingCalls(void *data)
{
  return 0;
}


int PySW_InitWrapper()
{
  if( fs_wrapper_init )
  {
	fs_wrapper_init = 0;
	// Add pending call handler to allow returning from never-ending loops.
    Py_AddPendingCall(PendingCalls, NULL);

  }
  return 0;
}


void PySW_SetPath(char *path)
{
  // This defines path from where for example modules are trying to be loaded
  PySys_SetPath(path);
}


void PySW_GetError(char *path)
{

}


PyObject* PySW_CreateTasklet( PyObject *func )
{
  PyObject *tasklet = (PyObject *) PyTasklet_New( NULL /* PyTypeObject *type */, func);
  return tasklet;
}

int PySW_DeleteTasklet(PyObject *tasklet)
{
  PyTaskletObject *task = (PyTaskletObject *) tasklet;
  int ret = 0;
  if( tasklet ) {
	if ( PyTasklet_Alive( task ))
		ret = PyTasklet_Kill( task );
    Py_DECREF( task );
  }
  return ret;
}

int PySW_IsTaskletRunning( PyObject *tasklet )
{
  PyTaskletObject *task = (PyTaskletObject *) tasklet;
  int ret = 0;
  if( tasklet ) {
	ret = PyTasklet_IsCurrent( task );
  }
  return ret;
}


int PySW_ResetTasklet(PyObject *tasklet)
{
  if( tasklet )
    PyTasklet_Remove( (PyTaskletObject *) tasklet);
  return 0;
}

/*************************************

  Note:
  In order to always clear the runnables
  chain, we should rewrite all of the
  following.
  I just can't completely figure out,
  how you would like them.

*************************************/

int PySW_RunTasklet(PyObject *tasklet )
{
  if( tasklet )
  {
	int ret;
    PyObject  *args = PyTuple_New(0);
	PyTaskletObject *task = (PyTaskletObject *) tasklet;
	
	ret = PyTasklet_Setup(task, args, NULL );
	if (ret) return ret;
	ret = PyTasklet_Run(task);
	return ret;
  }

  return -1;
}

int wrap(PyObject *ign)
{
	Py_XDECREF(ign);
	return ign ? 0 : -1;
}

int PySW_SuspendTasklet()
{
  PyTaskletObject *task = (PyTaskletObject* ) PyStackless_GetCurrent();
  if( task )	
  {
    Py_DECREF(task);
	return wrap(PyStackless_Schedule(Py_None, 0));
  }
  else
  {
    return -1;
  }
}

int PySW_ContinueTasklet( PyObject *tasklet )
{
  if( tasklet )	
  {
	int ret;
	PyTaskletObject *task = (PyTaskletObject* ) tasklet;

	ret = PyTasklet_Insert(task);
    if (ret == 0)
	    ret = wrap(PyStackless_Schedule(Py_None, 0));
	return ret;
  }
  else
  {
    return -1;
  }
}

int PySW_CleanupTasklet( PyObject *tasklet )
{
  if( tasklet && PyTasklet_Alive((PyTaskletObject *) tasklet))	
  {
	return PyTasklet_Kill( (PyTaskletObject *) tasklet);
  }
  else
  {
    return -1;
  }
}

