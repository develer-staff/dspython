#ifndef Py_PRICKELPIT_H
#define Py_PRICKELPIT_H
#ifdef __cplusplus
extern "C" {
#endif

/******************************************************

  code object and frame pickling plugin

*******************************************************/

PyAPI_FUNC(int) slp_register_execute(PyTypeObject *t, char *name,
				     PyFrame_ExecFunc *good,
				     PyFrame_ExecFunc *bad);

PyAPI_FUNC(int) slp_find_execfuncs(PyTypeObject *type, PyObject *exec_name,
				   PyFrame_ExecFunc **good, 
				   PyFrame_ExecFunc **bad);
            
PyAPI_FUNC(PyObject *) slp_find_execname(PyFrameObject *f, int *valid);

PyAPI_FUNC(PyObject *) slp_cannot_execute(PyFrameObject *f, char *exec_name,
					  PyObject *retval);

/* macros to define and use an invalid frame executor */

#define DEF_INVALID_EXEC(procname) \
static PyObject *\
cannot_##procname(PyFrameObject *f, int exc, PyObject *retval) \
{ \
	return slp_cannot_execute(f, #procname, retval); \
}

#define REF_INVALID_EXEC(procname) (cannot_##procname)


/* pickling of arrays with nulls */

PyAPI_FUNC(PyObject *) slp_into_tuple_with_nulls(PyObject **start, int length);
/* creates a tuple of length+1 with the first element holding null markers */

PyAPI_FUNC(int) slp_from_tuple_with_nulls(PyObject **start, PyObject *tup);
/* loads data from a tuple where the first element holds null markers.
   return value is the number of elements (length-1)
 */

/* helper functions for module dicts */

PyAPI_FUNC(PyObject *) PyStackless_Pickle_ModuleDict(PyObject *pickler,
						     PyObject *self);
PyAPI_FUNC(PyObject *) slp_pickle_moduledict(PyObject *self, PyObject *args);
PyAPI_DATA(char slp_pickle_moduledict__doc__[]);

/* initialization */

int init_prickelpit(void);

#ifdef __cplusplus
}
#endif
#endif /* !Py_PRICKELPIT_H */
