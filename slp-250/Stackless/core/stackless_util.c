#include "Python.h"

#ifdef STACKLESS
#include "stackless_impl.h"

/* Shorthands to return certain errors */

PyObject *
slp_type_error(const char *msg)
{
	PyErr_SetString(PyExc_TypeError, msg);
	return NULL;
}

PyObject *
slp_runtime_error(const char *msg)
{
	PyErr_SetString(PyExc_RuntimeError, msg);
	return NULL;
}

PyObject *
slp_value_error(const char *msg)
{
	PyErr_SetString(PyExc_ValueError, msg);
	return NULL;
}

PyObject *
slp_null_error(void)
{
	if (!PyErr_Occurred())
		PyErr_SetString(PyExc_SystemError,
		    "null argument to internal routine");
	return NULL;
}


/* CAUTION: This function returns a borrowed reference */
PyFrameObject *
slp_get_frame(PyTaskletObject *task)
{
	PyThreadState *ts = PyThreadState_GET();

	return ts->st.current == task ? ts->frame : task->f.frame;
}

void slp_check_pending_irq()
{
	PyThreadState *ts = PyThreadState_GET();
	PyTaskletObject *current = ts->st.current;

	if (current->flags.pending_irq) {
		if (current->flags.atomic)
			return;
		if (ts->st.nesting_level && !current->flags.ignore_nesting)
			return;
		/* trigger interrupt */
		if (_Py_Ticker > 0)
			_Py_Ticker = 0;
		ts->st.ticker = 0;
		current->flags.pending_irq = 0;
	}
}

int 
slp_return_wrapper(PyObject *retval)
{
	STACKLESS_ASSERT();
	if (retval == NULL)
		return -1;
	if (STACKLESS_UNWINDING(retval)) {
		STACKLESS_UNPACK(retval);
		Py_XDECREF(retval);
		return 1;
	}
	Py_DECREF(retval);
	return 0;
}

int 
slp_int_wrapper(PyObject *retval)
{
	int ret = -909090;

	STACKLESS_ASSERT();
	if (retval != NULL) {
		ret = PyInt_AsLong(retval);
		Py_DECREF(retval);
	}
	return ret;
}

int 
slp_current_wrapper( int(*func)(PyTaskletObject*), PyTaskletObject *task )
{
	PyThreadState *ts = PyThreadState_GET();

	int ret;
	ts->st.main = (PyTaskletObject*)Py_None;
	ret = func(task);
	ts->st.main = NULL;
	return ret;
}

int
slp_resurrect_and_kill(PyObject *self, void(*killer)(PyObject *))
{
	/* modelled after typeobject.c's call_finalizer */

	PyObject *error_type, *error_value, *error_traceback;

	/* Temporarily resurrect the object. */
#ifdef Py_TRACE_REFS
#  ifndef Py_REF_DEBUG
#    error "Py_TRACE_REFS defined but Py_REF_DEBUG not."
#  endif
	/* much too complicated if Py_TRACE_REFS defined */
	_Py_NewReference((PyObject *)self);
#  ifdef COUNT_ALLOCS
	/* compensate for boost in _Py_NewReference; note that
	 * _Py_RefTotal was also boosted; we'll knock that down later.
	 */
	self->ob_type->tp_allocs--;
#  endif
#else /* !Py_TRACE_REFS */
	/* Py_INCREF boosts _Py_RefTotal if Py_REF_DEBUG is defined */
	Py_INCREF(self);
#endif /* !Py_TRACE_REFS */

	/* Save the current exception, if any. */
	PyErr_Fetch(&error_type, &error_value, &error_traceback);

	killer(self);

	/* Restore the saved exception. */
	PyErr_Restore(error_type, error_value, error_traceback);

	/* Undo the temporary resurrection; can't use DECREF here, it would
	 * cause a recursive call.
	 */
#ifdef Py_REF_DEBUG
	/* _Py_RefTotal was boosted either by _Py_NewReference or
	 * Py_INCREF above.
	 */
	_Py_RefTotal--;
#endif
	if (--self->ob_refcnt > 0) {
#ifdef COUNT_ALLOCS
		self->ob_type->tp_frees--;
#endif
		return -1; /* __del__ added a reference; don't delete now */
	}
#ifdef Py_TRACE_REFS
	_Py_ForgetReference((PyObject *)self);
#  ifdef COUNT_ALLOCS
	/* compensate for increment in _Py_ForgetReference */
	self->ob_type->tp_frees--;
#  endif
#endif
	return 0;
}

#endif
