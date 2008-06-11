// testbench.cpp : Defines the entry point for the application.
//

#include "stdafx.h"
#include "python.h"
#include "simwrapper.h"


class rTasklet;

typedef struct {
	PyObject_HEAD
	rTasklet *m_foo;
} PyPythonScriptObject;

static PyObject *PyPythonScript_NewScript(rTasklet *script);
static void PyPythonScript_DeallocScript(PyPythonScriptObject *pso);
static PyObject *PyPythonScript_GetAttr(PyPythonScriptObject *self, char *name);

PyTypeObject PyPythonScript_Type = {
	PyObject_HEAD_INIT(NULL)
	0,			/*ob_size*/
	"simscript",    	/*tp_name*/
	sizeof(PyPythonScriptObject),	/*tp_basicsize*/
	0,			/*tp_itemsize*/
	/* methods */
	(destructor)PyPythonScript_DeallocScript, /*tp_dealloc*/
	0,			/*tp_print*/
	(getattrfunc)PyPythonScript_GetAttr, /*tp_getattr*/
	(setattrfunc)0, /*tp_setattr*/
	0,			/*tp_compare*/
	0,			/*tp_repr*/
	0,			/*tp_as_number*/
	0,			/*tp_as_sequence*/
	0,			/*tp_as_mapping*/
	0,			/*tp_hash*/
};


/* Allocation and deallocation of pythonscript Objects */

static PyObject *
PyPythonScript_NewScript(rTasklet *foo)
{
  PyPythonScriptObject *pso;
  pso = PyObject_NEW(PyPythonScriptObject, &PyPythonScript_Type);
  if (pso == NULL) return NULL;
  pso->m_foo = foo;
  return (PyObject *)pso;
}

static void
PyPythonScript_DeallocScript(PyPythonScriptObject *pso)
{
  PyObject_DEL(pso);
}

static PyObject *
PyPythonScript_getname(PyPythonScriptObject *self, PyObject* args)
{
  // Parse arguments
  static char *str;
  if(PyTuple_Size(args) == 1)
  {
    if (!PyArg_ParseTuple(args,"s", &str))
      return NULL;
  }
  else
  {
    return PyString_FromString(str);
  }

  return Py_None;
}

extern int PyStackless_Schedule();

static PyObject *
PyPythonScript_breaker(PyPythonScriptObject *self, PyObject* args)
{
  // Parse arguments
  static char *str;
  if(PyTuple_Size(args) == 1)
  {
    if (!PyArg_ParseTuple(args,"s", &str))
      return NULL;
  }
  else
  {
    return Py_None;
  }

  // Suspend script execution and switch execution back
  // This call should save this execution stack for this tasklet
  // and restore 
  PySW_SuspendTasklet();

  return Py_None;
}

// Object method registration structure
static PyMethodDef PyPythonScript_methods[] =
{
  {"foobar",           (PyCFunction)PyPythonScript_getname, METH_VARARGS},
  {"breaker",          (PyCFunction)PyPythonScript_breaker, METH_VARARGS},
  {NULL,		  NULL}		/* sentinel */
};

static PyObject *
PyPythonScript_GetAttr(PyPythonScriptObject *self, char *name)
{
  return Py_FindMethod(PyPythonScript_methods, (PyObject *)self, name);
}

int TestConditionFunction( PyObject *condf )
{
  if (condf && PyCallable_Check(condf))
  {
    int cret = 0;
    PyObject *fargs = PyTuple_New(0);
    PyObject *pValue = PyObject_CallObject(condf, fargs);
    if (pValue != NULL)
	{
      cret = PyInt_AsLong(pValue);
      Py_DECREF(pValue);
	}
    Py_DECREF(fargs);
	return cret;
  }
  return -1;
}

/* note: to switch back to windows mode, change
 * /subsystem:console   back to
 * /subsystem:windows   in the configuration window.
 */

/* q&d function to check, print and clear errors */

#include "malloc.h"

void CPCE (int ret, char *msg)
{
	if (ret) {
		printf("%s\n", msg);
		PyErr_Print();
	}
	else
		printf("%s OK\n", msg);
}


// Wrapper tasklet class 
class rTasklet
{
public:
//	PyThreadState       *m_interp;
	PyObject            *m_script_code;
	PyObject            *m_tasklet;

public:
	rTasklet() 
	{
//	  m_interp = Py_NewInterpreter();
//	  PyThreadState_Swap(m_interp);

      PyPythonScript_Type.ob_type = &PyType_Type;
      PyObject *iface_class = PyPythonScript_NewScript(this);
      PyImport_AddModule("simscript");
      Py_InitModule4("simscript", PyPythonScript_methods, NULL, iface_class, PYTHON_API_VERSION);

      PyObject *pName, *pModule, *pDict;
      pName = PyString_FromString("__main__");
      pModule = PyImport_Import(pName);

      PySW_SetPath("C:\\codebase\\main\\development\\3rdparty\\stackless_wrapper\\testbench");
      PyObject *stacklessmodule = PyImport_AddModule("stackless");
      pDict = PyModule_GetDict(pModule);
	}

	void CompileAndExecuteMain( char* code )
	{
//	  PyThreadState_Swap(m_interp);
      m_script_code = Py_CompileString(code, "pythoncode", Py_file_input);
	  Py_INCREF(m_script_code);

	  PyObject *mainobj = PyImport_ExecCodeModule("__main__", m_script_code);
	  if( !mainobj )
		PyErr_Print();
	}


    PyObject *CreateTask(char* func_name )
	{
//	  PyThreadState_Swap(m_interp);
      PyObject *pName, *pModule, *pDict;
      pName = PyString_FromString("__main__");
      pModule = PyImport_Import(pName);
      pDict = PyModule_GetDict(pModule);

	  m_tasklet = NULL;
      PyObject *func = PyDict_GetItemString(pDict, func_name);
      if (func && PyCallable_Check(func))
        m_tasklet = PySW_CreateTasklet( func );
      Py_XINCREF(m_tasklet);
	  return m_tasklet;
    }

	void RunTask( char* msg )
	{
//	  PyThreadState_Swap(m_interp);
      CPCE(PySW_RunTasklet(m_tasklet), msg);
	}

	void ContinueTask(char* msg )
	{
//	  PyThreadState_Swap(m_interp);
      CPCE(PySW_ContinueTasklet(m_tasklet), msg);
	}

	void ResetTask(char* msg )
	{
//	  PyThreadState_Swap(m_interp);
      CPCE(PySW_ResetTasklet(m_tasklet), msg);
	}


	void DeleteTask( char* msg )
	{
	  if( m_tasklet )
	  {
//		PyThreadState_Swap(m_interp);
		CPCE(PySW_CleanupTasklet( m_tasklet ), msg);
		Py_XDECREF(m_tasklet);
		m_tasklet = NULL;
	  }
	}

    PyObject *GetTask()
	{
      return m_tasklet;
	}

    PyObject *GetFunction(char *func_name)
	{
//	  PyThreadState_Swap(m_interp);
      PyObject *pName, *pModule, *pDict;
      pName = PyString_FromString("__main__");
      pModule = PyImport_Import(pName);
      pDict = PyModule_GetDict(pModule);
      return PyDict_GetItemString(pDict, func_name);
	}


	void Destroy( char* msg )
	{

//	  PyThreadState *old_state = PyThreadState_Swap(m_interp);

//      PyThreadState_Clear(m_interp);
      // Interpreter deletion does not work yet! And it leakes now memory ...
	  // PyThreadState_Swap(NULL); // Should not be required ... nobody has tested these python calls together
      // PyThreadState_Delete(m_interp);
	  // PyThreadState_Swap(NULL);
	  // PyThreadState_Swap(m_interp);
      // CPCE( true, msg);
//	  Py_EndInterpreter( m_interp );

    }	
 
};





char sourcecode[] = "           \n\
                                    \n\
import simscript                    \n\
# import winsound                     \n\
# import sdk32                      \n\
                                    \n\
# winsound.PlaySound(\"c:\\WINDOWS\\MEDIA\\tada.wav\", winsound.SND_FILENAME') \n\
# sdk32.MessageBox(\"Jep\",\"foobar\",win32con.MB_OK) \n\
simscript.foobar(\"mainA\")         \n\
                                    \n\
def condition_func():               \n\
  return 42                         \n\
                                    \n\
def run1():                         \n\
  print 'run1 starting'				\n\
  simscript.breaker('A\')           \n\
  print 'run1 between A/B'			\n\
  simscript.breaker('B')            \n\
  print 'run1 finished'				\n\
                                    \n\
def run2():                         \n\
  print 'run2 starting'				\n\
  simscript.breaker('C')            \n\
  print 'run2 between C/D'			\n\
  simscript.breaker('D')			\n\
  print 'run2 finished'				\n\
                                    \n\
simscript.foobar('mainB')			\n\
";



#if 0
int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
#else
int
main(int argc, char **argv)
#endif
{
  char *msg = NULL;
  // 1. Init python and stackless 
  PyEval_InitThreads();
  Py_Initialize();
  int code = Py_IsInitialized();
  /* no threads needed */

  // 2. Init execution wrapper
  PySW_InitWrapper();

/*

  // 3. Store this instances threadstate
  PyThreadState *m_interp = PyEval_SaveThread();

  // 4. Each script will have its own interpreter
  PyEval_AcquireLock();
  m_interp = Py_NewInterpreter();
  PyThreadState_Swap(m_interp);

*/

  for( int loops = 0; loops<100; loops++)
  {
    // 5. Create two task objects (both contain independent interpreter and tasklet defs)
    rTasklet *task1 = new rTasklet();
    rTasklet *task2 = new rTasklet();

    // 6. Assign source code and execute main level for both tasklets objects
    task1->CompileAndExecuteMain( sourcecode );
    task2->CompileAndExecuteMain( sourcecode );

    // 7. Create new tasklet for both tasklet objects
    task1->CreateTask( "run1" );
    task2->CreateTask( "run2" );

    // 8. Start executing tasks in sequence
    task1->RunTask("8. Execute tasklet 1 till point \"A\"");
    task2->RunTask("9. Execute tasklet 2 till point \"C\"");
    task1->ContinueTask("10. Continue tasklet 1 till point \"B\"");

    /* CT dropped */

    msg = "11. Call condition func in a middle of tasklet 1 execution";
    PyObject *condf = task1->GetFunction("condition_func");
    printf("%s returns %d\n", msg, TestConditionFunction( condf ));
        
    task2->ContinueTask("12. Continue tasklet 2 till point \"D\"");
    task1->ContinueTask("13. Continue tasklet 1 till end");

    task1->ResetTask("14. Reset tasklet 1");
    task1->DeleteTask("15. Delete tasklet 1");


    task2->DeleteTask("16. Delete tasklet 2 (suspended)");

    task1->Destroy( "17. Destroy tasklet 1 internals (interpreter etc.)");
    task2->Destroy( "18. Destroy tasklet 2 internals (interpreter etc.)");

	delete task1;
    delete task2;
  }

  return 0;
}



