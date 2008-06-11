#include "Python.h"

#ifdef STACKLESS
#include "core/stackless_impl.h"

#ifdef WITH_THREAD
#include "pythread.h"
#endif

/******************************************************

  The Bomb object -- making exceptions convenient

 ******************************************************/

static PyBombObject *free_list = NULL;
static int numfree = 0;		/* number of bombs currently in free_list */
#define MAXFREELIST 20		/* max value for numfree */

static void
bomb_dealloc(PyBombObject *bomb)
{
	_PyObject_GC_UNTRACK(bomb);
	Py_XDECREF(bomb->curexc_type);
	Py_XDECREF(bomb->curexc_value);
	Py_XDECREF(bomb->curexc_traceback);
	if (numfree < MAXFREELIST) {
		++numfree;
		bomb->curexc_type = (PyObject *) free_list;
		free_list = bomb;
	}
	else
		PyObject_GC_Del(bomb);
}

static int
bomb_traverse(PyBombObject *bomb, visitproc visit, void *arg)
{
	int err;

#define VISIT(o) if (o) {if ((err = visit((PyObject *)(o), arg))) return err;}

	VISIT(bomb->curexc_type);
	VISIT(bomb->curexc_value);
	VISIT(bomb->curexc_traceback);

#undef VISIT
	return 0;
}

static void
bomb_clear(PyBombObject *bomb)
{
#define ZAP(x) \
	if (x != NULL) { \
		PyObject *_hold = (PyObject *) x; \
		x = NULL; \
		Py_XDECREF(_hold); \
	}

	ZAP(bomb->curexc_type);
	ZAP(bomb->curexc_value);
	ZAP(bomb->curexc_traceback);

#undef ZAP
}

static PyBombObject *
new_bomb(void)
{
	PyBombObject *bomb;

	if (free_list == NULL) {
		bomb = PyObject_GC_New(PyBombObject, &PyBomb_Type);
		if (bomb == NULL)
			return NULL;
	}
	else {
		assert(numfree > 0);
		--numfree;
		bomb = free_list;
		free_list = (PyBombObject *) free_list->curexc_type;
		_Py_NewReference((PyObject *) bomb);
	}
	bomb->curexc_type = NULL;
	bomb->curexc_value = NULL;
	bomb->curexc_traceback = NULL;
	PyObject_GC_Track(bomb);
	return bomb;
}

static PyObject *
bomb_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	static char *kwlist[] = {"type", "value", "traceback", NULL};
	PyBombObject *bomb = new_bomb();

	if (bomb == NULL)
		return NULL;

	if (PyTuple_GET_SIZE(args) == 1 &&
	    PyTuple_Check(PyTuple_GET_ITEM(args, 0)))
		args = PyTuple_GET_ITEM(args, 0);
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|OOO:bomb", kwlist,
					 &bomb->curexc_type,
					 &bomb->curexc_value,
					 &bomb->curexc_traceback)) {
		Py_DECREF(bomb);
		return NULL;
	}
	Py_XINCREF(bomb->curexc_type);
	Py_XINCREF(bomb->curexc_value);
	Py_XINCREF(bomb->curexc_traceback);
	return (PyObject*) bomb;
}

PyObject *
slp_make_bomb(PyObject *klass, PyObject *args, char *msg)
{
	PyBombObject *bomb;
	PyObject *tup;

	if (! (PyObject_IsSubclass(klass, PyExc_BaseException) == 1 ||
	       PyString_Check(klass) ) ) {
		char s[256];

		sprintf(s, "%.128s needs Exception or string"
			   " subclass as first parameter", msg);
		TYPE_ERROR(s, NULL);
	}
	if ( (bomb = new_bomb()) == NULL)
		return NULL;
	Py_INCREF(klass);
	bomb->curexc_type = klass;
	tup = Py_BuildValue(PyTuple_Check(args) ? "O" : "(O)", args);
	bomb->curexc_value = tup;
	if (tup == NULL) {
		Py_DECREF(bomb);
		return NULL;
	}
	return (PyObject *) bomb;
}

PyObject *
slp_curexc_to_bomb(void)
{
	PyBombObject *bomb = new_bomb();

	if (bomb != NULL)
		PyErr_Fetch(&bomb->curexc_type, &bomb->curexc_value,
			    &bomb->curexc_traceback);
	return (PyObject *) bomb;
}

/* set exception, destroy bomb reference and return NULL */

PyObject *
slp_bomb_explode(PyTaskletObject *task)
{
	PyBombObject *bomb = (PyBombObject *) task->tempval;

	assert(PyBomb_Check(bomb));
	Py_XINCREF(bomb->curexc_type);
	Py_XINCREF(bomb->curexc_value);
	Py_XINCREF(bomb->curexc_traceback);
	PyErr_Restore(bomb->curexc_type, bomb->curexc_value,
		      bomb->curexc_traceback);
	Py_DECREF(bomb);
	/* avoid periodical re-bombing */
	TASKLET_SETVAL(task, Py_None);
	return NULL;
}

static PyObject *
bomb_reduce(PyBombObject *bomb)
{
	PyObject *tup;

	tup = slp_into_tuple_with_nulls(&bomb->curexc_type, 3);
	if (tup != NULL)
		tup = Py_BuildValue("(O()O)", &PyBomb_Type, tup);
	return tup;
}

static PyObject *
bomb_setstate(PyBombObject *bomb, PyObject *args)
{
	if (PyTuple_GET_SIZE(args) != 4)
		VALUE_ERROR("bad exception tuple for bomb", NULL);
	bomb_clear(bomb);
	slp_from_tuple_with_nulls(&bomb->curexc_type, args);
	Py_INCREF(bomb);
	return (PyObject *) bomb;
}

static PyMemberDef bomb_members[] = {
	{"type",	T_OBJECT, offsetof(PyBombObject, curexc_type), READONLY},
	{"value",	T_OBJECT, offsetof(PyBombObject, curexc_value), READONLY},
	{"traceback",	T_OBJECT, offsetof(PyBombObject, curexc_traceback), READONLY},
	{0}
};

static PyMethodDef bomb_methods[] = {
	{"__reduce__",		(PyCFunction)bomb_reduce,	METH_NOARGS},
	{"__reduce_ex__",	(PyCFunction)bomb_reduce,	METH_VARARGS},
	{"__setstate__",	(PyCFunction)bomb_setstate,	METH_O},
	{NULL,     NULL}             /* sentinel */
};

static char bomb__doc__[] =
"A bomb object is used to hold exceptions in tasklets.\n\
Whenever a tasklet is activated and its tempval is a bomb,\n\
it will explode as an exception.\n\
\n\
You can create a bomb by hand and attach it to a tasklet if you like.\n\
Note that bombs are 'sloppy' about the argument list, which means that\n\
the following works, although you should use '*sys.exc_info()'.\n\
\n\
from stackless import *; import sys\n\
t = tasklet(lambda:42)()\n\
try: 1/0\n\
except: b = bomb(sys.exc_info())\n\
\n\
t.tempval = b\n\
t.run()  # let the bomb explode";

PyTypeObject PyBomb_Type = {
	PyObject_HEAD_INIT(&PyType_Type)
	0,
	"stackless.bomb",
	sizeof(PyBombObject),
	0,
	(destructor)bomb_dealloc,		/* tp_dealloc */
	0,					/* tp_print */
	0,					/* tp_getattr */
	0,					/* tp_setattr */
	0,					/* tp_compare */
	0,					/* tp_repr */
	0,					/* tp_as_number */
	0,					/* tp_as_sequence */
	0,					/* tp_as_mapping */
	0,					/* tp_hash */
	0,					/* tp_call */
	0,					/* tp_str */
	PyObject_GenericGetAttr,		/* tp_getattro */
	PyObject_GenericSetAttr,		/* tp_setattro */
	0,					/* tp_as_buffer */
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC, /* tp_flags */
	bomb__doc__,				/* tp_doc */
 	(traverseproc)bomb_traverse,		/* tp_traverse */
	(inquiry) bomb_clear,			/* tp_clear */
	0,					/* tp_richcompare */
	0,					/* tp_weaklistoffset */
	0,					/* tp_iter */
	0,					/* tp_iternext */
	bomb_methods,				/* tp_methods */
	bomb_members,				/* tp_members */
	0,					/* tp_getset */
	0,					/* tp_base */
	0,					/* tp_dict */
	0,					/* tp_descr_get */
	0,					/* tp_descr_set */
	0,					/* tp_dictoffset */
	0,					/* tp_init */
	0,					/* tp_alloc */
	bomb_new,				/* tp_new */
	_PyObject_GC_Del,			/* tp_free */
};


/*******************************************************************

  Exception handling revised.

  Every tasklet has its own exception state. The thread state
  exists only once for the current thread, so we need to simulate
  ownership.

  Whenever a tasklet is run for the first time, it should clear
  the exception variables and start with a clean state.

  When it dies normally, it should clean up these.

  When a transfer occours from one tasklet to another,
  the first tasklet should save its exception in local variables,
  and the other one should restore its own.

  When a tasklet dies with an uncaught exception, this will
  be passed on to the main tasklet. The main tasklet must
  clear its exception state, if any, and take over those of
  the tasklet resting in peace.

  2002-08-08 This was a misconception. This is not the current
  exception, but the one which ceval provides for exception
  handlers. That means, sharing of this variable is totally
  unrelated to the current error, and we always swap the data.

  Added support for trace/profile as well.

 ********************************************************************/

slp_schedule_hook_func *_slp_schedule_fasthook;
PyObject *_slp_schedule_hook;

static int
transfer_with_exc(PyCStackObject **cstprev, PyCStackObject *cst, PyTaskletObject *prev)
{
	PyThreadState *ts = PyThreadState_GET();

	int tracing = ts->tracing;
	int use_tracing = ts->use_tracing;

	Py_tracefunc c_profilefunc = ts->c_profilefunc;
	Py_tracefunc c_tracefunc = ts->c_tracefunc;
	PyObject *c_profileobj = ts->c_profileobj;
	PyObject *c_traceobj = ts->c_traceobj;

	PyObject *exc_type = ts->exc_type;
	PyObject *exc_value = ts->exc_value;
	PyObject *exc_traceback = ts->exc_traceback;
	int ret;

	ts->exc_type = ts->exc_value = ts->exc_traceback = NULL;
	ts->c_profilefunc = ts->c_tracefunc = NULL;
	ts->c_profileobj = ts->c_traceobj = NULL;
	ts->use_tracing = ts->tracing = 0;

	/* note that trace/profile are set without ref */
	Py_XINCREF(c_profileobj);
	Py_XINCREF(c_traceobj);

	ret = slp_transfer(cstprev, cst, prev);

	ts->tracing = tracing;
	ts->use_tracing = use_tracing;

	ts->c_profilefunc = c_profilefunc;
	ts->c_tracefunc = c_tracefunc;
	ts->c_profileobj = c_profileobj;
	ts->c_traceobj = c_traceobj;
	Py_XDECREF(c_profileobj);
	Py_XDECREF(c_traceobj);

	ts->exc_type = exc_type;
	ts->exc_value = exc_value;
	ts->exc_traceback = exc_traceback;
	return ret;
}

/* scheduler monitoring */

int
slp_schedule_callback(PyTaskletObject *prev, PyTaskletObject *next)
{
	PyObject *args;

	if (prev == NULL) prev = (PyTaskletObject *)Py_None;
	if (next == NULL) next = (PyTaskletObject *)Py_None;
	args = Py_BuildValue("(OO)", prev, next);
	if (args != NULL) {
		PyObject *type, *value, *traceback, *ret;

		PyErr_Fetch(&type, &value, &traceback);
		ret = PyObject_Call(_slp_schedule_hook, args, NULL);
		if (ret != NULL)
			PyErr_Restore(type, value, traceback);
		else {
			Py_XDECREF(type);
			Py_XDECREF(value);
			Py_XDECREF(traceback);
		}
		Py_XDECREF(ret);
		Py_DECREF(args);
		return ret ? 0 : -1;
	}
	else
		return -1;
}

#define NOTIFY_SCHEDULE(prev, next, errflag) \
	if (_slp_schedule_fasthook != NULL) { \
		int ret; \
		if (ts->st.schedlock) { \
			RUNTIME_ERROR( \
			    "Recursive scheduler call due to callbacks!", \
			    errflag); \
		} \
		ts->st.schedlock = 1; \
		ret = _slp_schedule_fasthook(prev, next); \
		ts->st.schedlock = 0; \
		if (ret) return errflag; \
	}

static void
kill_wrap_bad_guy(PyTaskletObject *prev, PyTaskletObject *bad_guy)
{
	/*
	 * just in case a transfer didn't work, we pack the bad
	 * tasklet into the exception and remove it from the runnables.
	 *
	 */
	PyThreadState *ts = PyThreadState_GET();
	PyObject *newval = PyTuple_New(2);
	if (bad_guy->next != NULL) {
		ts->st.current = bad_guy;
		slp_current_remove();
	}
	/* restore last tasklet */
	if (prev->next == NULL)
		slp_current_insert(prev);
	ts->frame = prev->f.frame;
	ts->st.current = prev;
	if (newval != NULL) {
		/* merge bad guy into exception */
		PyObject *exc, *val, *tb;
		PyErr_Fetch(&exc, &val, &tb);
		PyTuple_SET_ITEM(newval, 0, val);
		PyTuple_SET_ITEM(newval, 1, (PyObject*)bad_guy);
		Py_INCREF(bad_guy);
		PyErr_Restore(exc, newval, tb);
	}
}

/* slp_schedule_task is moved down and merged with soft switching */

/* non-recursive scheduling */

static PyObject *
restore_exception(PyFrameObject *f, int exc, PyObject *retval)
{
	PyThreadState *ts = PyThreadState_GET();
	PyCFrameObject *cf = (PyCFrameObject *) f;

	f = cf->f_back;
	ts->exc_type = cf->ob1;
	ts->exc_value = cf->ob2;
	ts->exc_traceback = cf->ob3;
	cf->ob1 = cf->ob2 = cf->ob3 = NULL;
	Py_DECREF(cf);
	ts->frame = f;
	return STACKLESS_PACK(retval);
}

static PyObject *
restore_tracing(PyFrameObject *f, int exc, PyObject *retval)
{
	PyThreadState *ts = PyThreadState_GET();
	PyCFrameObject *cf = (PyCFrameObject *) f;

	f = cf->f_back;
	ts->c_tracefunc = cf->any1;
	ts->c_profilefunc = cf->any2;
	ts->c_traceobj = cf->ob1;
	ts->c_profileobj = cf->ob2;
	ts->tracing = cf->i;
	ts->use_tracing = cf->n;
	/* the objects *have* extra references here */
	Py_DECREF(cf);
	ts->frame = f;
	return STACKLESS_PACK(retval);
}

/* jumping from a soft tasklet to a hard switched */

static PyObject *
jump_soft_to_hard(PyFrameObject *f, int exc, PyObject *retval)
{
	PyThreadState *ts = PyThreadState_GET();

	ts->frame = f->f_back;
	Py_DECREF(f);
	/* ignore retval. everything is in the tasklet. */
	slp_transfer_return(ts->st.current->cstate);
	/* we either have an error or don't come back, so: */
	return NULL;
}


/* combined soft/hard switching */

int
slp_ensure_linkage(PyTaskletObject *t)
{
	if (t->cstate->task == t)
		return 0;
	if (!slp_cstack_new(&t->cstate, t->cstate->tstate->st.cstack_base, t))
		return -1;
	t->cstate->nesting_level = 0;
	return 0;
}


/* check whether a different thread can be run */

static int
is_thread_runnable(PyThreadState *ts)
{
#ifdef WITH_THREAD
	if (ts == PyThreadState_GET())
		return 0;
	return !ts->st.thread.is_locked;
#endif
	return 0;
}

static int
check_for_deadlock(void)
{
	PyThreadState *ts = PyThreadState_GET();
	PyInterpreterState *interp = ts->interp;

	/* see if anybody else will be able to run */

	for (ts = interp->tstate_head; ts != NULL; ts = ts->next)
		if (is_thread_runnable(ts))
			return 0;
	return 1;
}

static PyObject *
make_deadlock_bomb(void)
{
	PyErr_SetString(PyExc_RuntimeError,
		"Deadlock: the last runnable tasklet cannot be blocked.");
	return slp_curexc_to_bomb();
}

static int
is_thread_alive(long thread_id)
{
	PyThreadState *ts = PyThreadState_Get();
	PyInterpreterState *interp = ts->interp;

	for (ts = interp->tstate_head; ts != NULL; ts = ts->next)
		if (ts->thread_id == thread_id)
			return 1;
	return 0;
}

# if 0
#define PR(s) printf("%d: %04x-%04x %04x-%04x %2d " s "\n", prev->cstate->tstate->thread_id, \
	(int)prev & 0xffff, \
(int)prev->cstate->tstate & 0xffff, (int)next & 0xffff, \
	next ? (int)next->cstate->tstate & 0xffff : 0, \
next ? next->flags.blocked : 0)

# else
#define PR(s)

# endif

#ifdef WITH_THREAD

static
PyThread_type_lock interthread_lock = NULL;

/* thread communication (protected by the lock) */

static struct {
	PyTaskletObject *unlock_target;
	PyObject *other_lock;
	long thread_id;
} temp = {0, 0, 0};

/* make sure that locks live longer than their threads */

static void
destruct_lock(PyThread_type_lock lock)
{
	PyThread_acquire_lock(lock, 0);
	PyThread_release_lock(lock);
	PyThread_free_lock(lock);
}

static PyObject *
new_lock(void)
{
	PyThread_type_lock lock;

	lock = PyThread_allocate_lock();
	if (lock == NULL) return NULL;

	return PyCObject_FromVoidPtr(lock, destruct_lock);
}

#define get_lock(obj) PyCObject_AsVoidPtr(obj)

#define acquire_lock(lock, flag) PyThread_acquire_lock(get_lock(lock), flag)
#define release_lock(lock) PyThread_release_lock(get_lock(lock))

#endif

static PyObject *
schedule_task_block(PyTaskletObject *prev, int stackless)
{
	PyThreadState *ts = PyThreadState_GET();
	PyObject *retval;
	PyTaskletObject *next = NULL;
	PyObject *unlocker_lock;

	if (check_for_deadlock()) {
		/* revive real main if floating */
		if (ts == slp_initial_tstate && ts->st.main->next == NULL) {
			/* emulate old revive_main behavior:
			 * passing a value only if it is an exception
			 */
			if (PyBomb_Check(prev->tempval))
				TASKLET_SETVAL(ts->st.main, prev->tempval);
			return slp_schedule_task(prev, ts->st.main, stackless);
		}
		if (!(retval = make_deadlock_bomb()))
			return NULL;
		TASKLET_SETVAL_OWN(prev, retval);
		return slp_schedule_task(prev, prev, stackless);
	}
#ifdef WITH_THREAD
	if (ts->st.thread.self_lock == NULL) {
		if (!(ts->st.thread.self_lock = new_lock()))
			return NULL;
		acquire_lock(ts->st.thread.self_lock, 1);
		if (!(ts->st.thread.unlock_lock = new_lock()))
			return NULL;
	}

	/* let somebody reactivate us */

	ts->st.thread.is_locked = 1; /* flag as blocked and wait */

	PyEval_SaveThread();
	PR("locker waiting for my lock");
	acquire_lock(ts->st.thread.self_lock, 1);
	PR("HAVE my lock");
	PyEval_RestoreThread(ts);

	if (temp.unlock_target != NULL) {
		next = temp.unlock_target;
		temp.unlock_target = NULL;
	}
	else
		next = prev;

	/*
	 * get in shape. can't do this with schedule here because
	 * hard switching might not get us back, soon enough.
	 */
	if (next->flags.blocked) {
		/* unblock from channel */
		slp_channel_remove_slow(next);
		slp_current_insert(next);
	}
	else if (next->next == NULL) {
		/* reactivate floating task */
		Py_INCREF(next);
		slp_current_insert(next);
	}

	if (temp.other_lock != NULL) {
		PR("releasing unlocker");
		unlocker_lock = temp.other_lock;
		temp.other_lock = NULL;
		release_lock(unlocker_lock);
		Py_DECREF(unlocker_lock);
	}

	ts->st.thread.is_locked = 0;
#else
	(void)unlocker_lock;
	next = prev;
#endif
	/* this must be after releasing the locks because of hard switching */
	retval = slp_schedule_task(prev, next, stackless);
	PR("schedule() is done");
	return retval;
}

#ifdef WITH_THREAD

static PyObject *schedule_task_unblock(PyTaskletObject *prev,
				       PyTaskletObject *next,
				       int stackless)
{
	PyThreadState *ts = PyThreadState_GET();
	PyThreadState *nts = next->cstate->tstate;
	PyObject *retval;
	long thread_id = nts->thread_id;
	PyObject *unlock_lock;

	if (ts->st.thread.self_lock == NULL) {
		if (!(ts->st.thread.self_lock = new_lock()))
			return NULL;
		acquire_lock(ts->st.thread.self_lock, 1);
		if (!(ts->st.thread.unlock_lock = new_lock()))
			return NULL;
		if (interthread_lock == NULL) {
			if (!(interthread_lock = PyThread_allocate_lock()))
				return NULL;
		}
	}

	/*
	 * make sure nobody else tries a transaction at the same time
	 * on this tasklet's thread state, because two tasklets of the
	 * same thread could be talking to different threads. They must
	 * be serviced in fifo order.
	 */

	if (nts->st.thread.unlock_lock == NULL) {
		if (!(nts->st.thread.unlock_lock = new_lock()))
			return NULL;
	}
	unlock_lock = nts->st.thread.unlock_lock;
	Py_INCREF(unlock_lock);

	PyEval_SaveThread();
	PR("unblocker waiting for unlocker lock");
	acquire_lock(unlock_lock, 1);
	PR("unblocker HAS unlocker lock");

	/*
	 * also make sure that only one single interthread transaction
	 * is performed at any time.
	 */

	PR("unblocker waiting for interthread lock");
	PyThread_acquire_lock(interthread_lock, 1);
	PR("unblocker HAS interthread lock");
	PyEval_RestoreThread(ts);

	/* get myself ready */
	retval = slp_schedule_task(prev, prev, stackless);

	/* see whether the other thread still exists and is really blocked */
	if (is_thread_alive(thread_id) && nts->st.thread.is_locked) {
		/* tell the blocker what comes next */
		temp.unlock_target = next;
		temp.other_lock = ts->st.thread.self_lock;
		/* give it an extra ref, in case I would die early */
		Py_INCREF(temp.other_lock);

		/* unblock it */
		release_lock(nts->st.thread.self_lock);

		/* wait for the transaction to finish */

		PyEval_SaveThread();
		PR("unblocker waiting for own lock");
		acquire_lock(ts->st.thread.self_lock, 1);
		PR("unblocker HAS own lock");
		PyEval_RestoreThread(ts);
	}
	else {
		PR("unlocker: other is NOT LOCKED or dead");
		if (next->flags.blocked) {
			/* unblock from channel */
			slp_channel_remove_slow(next);
			slp_current_insert(next);
		}
		else if (next->next == NULL) {
			/* reactivate floating task */
			Py_INCREF(next);
			slp_current_insert(next);
		}
	}
	PR("unblocker releasing interthread lock");
	PyThread_release_lock(interthread_lock);
	PR("unblocker RELEASED interthread lock");
	PR("unblocker releasing unlocker lock");
	release_lock(unlock_lock);
	Py_DECREF(unlock_lock);
	PR("unblocker RELEASED unlocker lock");

	return retval;
}

#endif

PyObject *
slp_schedule_task(PyTaskletObject *prev, PyTaskletObject *next, int stackless)
{
	PyThreadState *ts = PyThreadState_GET();
	PyCStackObject **cstprev;
	PyObject *retval;
	int (*transfer)(PyCStackObject **, PyCStackObject *, PyTaskletObject *);

	if (next == NULL) {
		return schedule_task_block(prev, stackless);
	}
#ifdef WITH_THREAD
	/* note that next->cstate is undefined if it is ourself */
	if (next->cstate != NULL && next->cstate->tstate != ts) {
		return schedule_task_unblock(prev, next, stackless);
	}
#endif
	if (next->flags.blocked) {
		/* unblock from channel */
		slp_channel_remove_slow(next);
		slp_current_insert(next);
	}
	else if (next->next == NULL) {
		/* reactivate floating task */
		Py_INCREF(next);
		slp_current_insert(next);
	}
	if (prev == next) {
		retval = prev->tempval;
		Py_INCREF(retval);
		if (PyBomb_Check(retval))
			retval = slp_bomb_explode(prev);
		return retval;
	}

	NOTIFY_SCHEDULE(prev, next, NULL);

	ts->st.ticker = ts->st.interval;
	prev->recursion_depth = ts->recursion_depth;
	prev->f.frame = ts->frame;

	if (!stackless || ts->st.nesting_level != 0)
		goto hard_switching;

	/* start of soft switching code */

	if (prev->cstate != ts->st.initial_stub) {
		Py_DECREF(prev->cstate);
		prev->cstate = ts->st.initial_stub;
		Py_INCREF(prev->cstate);
	}
	if (ts != slp_initial_tstate) {
		/* ensure to get all tasklets into the other thread's chain */
		if (slp_ensure_linkage(prev) || slp_ensure_linkage(next))
			return NULL;
	}

	/* handle exception */
	if (ts->exc_type == Py_None) {
		Py_XDECREF(ts->exc_type);
		ts->exc_type = NULL;
	}
	if (ts->exc_type != NULL) {
		/* build a shadow frame */
		PyCFrameObject *f = slp_cframe_new(restore_exception, 1);
		if (f == NULL)
			return NULL;
		f->ob1 = ts->exc_type;
		f->ob2 = ts->exc_value;
		f->ob3 = ts->exc_traceback;
		prev->f.frame = (PyFrameObject *) f;
		ts->exc_type = ts->exc_value =
			       ts->exc_traceback = NULL;
	}
	if (ts->use_tracing || ts->tracing) {
		/* build a shadow frame */
		PyCFrameObject *f = slp_cframe_new(restore_tracing, 1);
		if (f == NULL)
			return NULL;
		f->any1 = ts->c_tracefunc;
		f->any2 = ts->c_profilefunc;
		ts->c_tracefunc = ts->c_profilefunc = NULL;
		f->ob1 = ts->c_traceobj;
		f->ob2 = ts->c_profileobj;
		/* trace/profile does not add references */
		Py_XINCREF(f->ob1);
		Py_XINCREF(f->ob2);
		ts->c_traceobj = ts->c_profileobj = NULL;
		f->i = ts->tracing;
		f->n = ts->use_tracing;
		ts->tracing = ts->use_tracing = 0;
		prev->f.frame = (PyFrameObject *) f;
	}
	ts->frame = next->f.frame;
	next->f.frame = NULL;

	ts->recursion_depth = next->recursion_depth;

	ts->st.current = next;
	retval = next->tempval;

	assert(next->cstate != NULL);
	if (next->cstate->nesting_level != 0) {
		/* create a helper frame to restore the target stack */
		ts->frame = (PyFrameObject *)
			    slp_cframe_new(jump_soft_to_hard, 1);
		if (ts->frame == NULL) {
			ts->frame = prev->f.frame;
			return NULL;
		}
		/* note that we don't explode the bomb now and don't incref! */
		return STACKLESS_PACK(retval);
	}

	Py_INCREF(retval);
	if (PyBomb_Check(retval))
		retval = slp_bomb_explode(next);

	return STACKLESS_PACK(retval);

hard_switching:
	/* since we change the stack we must assure that the protocol was met */
	STACKLESS_ASSERT();

	/* note: nesting_level is handled in cstack_new */
	cstprev = &prev->cstate;

	ts->st.current = next;

	if (ts->exc_type == Py_None) {
		Py_XDECREF(ts->exc_type);
		ts->exc_type = NULL;
	}
	ts->recursion_depth = next->recursion_depth;
	ts->frame = next->f.frame;
	next->f.frame = NULL;

	++ts->st.nesting_level;
	if (ts->exc_type != NULL || ts->use_tracing || ts->tracing)
		transfer = transfer_with_exc;
	else
		transfer = slp_transfer;

	if (transfer(cstprev, next->cstate, prev) == 0) {
		--ts->st.nesting_level;
		retval = prev->tempval;
		Py_INCREF(retval);
		if (PyBomb_Check(retval))
			retval = slp_bomb_explode(prev);
		return retval;
	}
	else {
		--ts->st.nesting_level;
		kill_wrap_bad_guy(prev, next);
		return NULL;
	}
}

int
initialize_main_and_current(void)
{
	PyThreadState *ts = PyThreadState_GET();
	PyTaskletObject *task;
	PyObject *noargs;

	/* refuse executing main in an unhandled error context */
	if (! (PyErr_Occurred() == NULL || PyErr_Occurred() == Py_None) ) {
#ifdef _DEBUG
		PyObject *type, *value, *traceback;
		PyErr_Fetch(&type, &value, &traceback);
		Py_XINCREF(type);
		Py_XINCREF(value);
		Py_XINCREF(traceback);
		PyErr_Restore(type, value, traceback);
		printf("Pending error while entering Stackless subsystem:\n");
		PyErr_Print();
		printf("Above exception is re-raised to the caller.\n");
		PyErr_Restore(type, value, traceback);
#endif
        return 1;
	}

	noargs = PyTuple_New(0);
	task = (PyTaskletObject *) PyTasklet_Type.tp_new(
		    &PyTasklet_Type, noargs, NULL);
	Py_DECREF(noargs);
	if (task == NULL) return -1;
	assert(task->cstate != NULL);
	ts->st.main = task;
	Py_INCREF(task);
	slp_current_insert(task);
	ts->st.current = task;

	NOTIFY_SCHEDULE(NULL, task, -1);

	return 0;
}


/* scheduling and destructing the previous one */

static PyObject *
schedule_task_destruct(PyTaskletObject *prev, PyTaskletObject *next)
{
	/*
	 * The problem is to leave the dying tasklet alive
	 * until we have done the switch.
	 * This cannot easily be done by hard switching, since
	 * the C stack we are leaving is never returned to,
	 * and who should do the dereferencing?
	 * Therefore, we enforce a soft-switch.
	 */
	PyThreadState *ts = PyThreadState_GET();
	PyObject *retval;

	/* we should have no nesting level */
	assert(ts->st.nesting_level == 0);
	/* even there is a (buggy) nesting, ensure soft switch */
	if (ts->st.nesting_level != 0) {
		printf("XXX error, nesting_level = %d\n", ts->st.nesting_level);
		ts->st.nesting_level = 0;
	}

	/* update what's not yet updated */
	assert(ts->recursion_depth == 0);
	prev->recursion_depth = 0;
	assert(ts->frame == NULL);
	prev->f.frame = NULL;

	/* do a soft switch */
	if (prev != next)
		retval = slp_schedule_task(prev, next, 1);
	else {
		retval = prev->tempval;
		Py_INCREF(retval);
		if (PyBomb_Check(retval))
			retval = slp_bomb_explode(prev);
	}

	prev->ob_type->tp_clear((PyObject *)prev);
	/* now it is safe to derefence prev */
	Py_DECREF(prev);
	return retval;
}

/* defined in pythonrun.c */
extern void PyStackless_HandleSystemExit();

static PyObject *
tasklet_end(PyObject *retval)
{
	PyThreadState *ts = PyThreadState_GET();
	PyTaskletObject *task = ts->st.current;
	PyTaskletObject *next;

	int ismain = task == ts->st.main;

	/*
	 * see whether we have a SystemExit, which is no error.
	 * Note that TaskletExit is a subclass.
	 * otherwise make the exception into a bomb.
	 */
	if (retval == NULL) {
		if (PyErr_ExceptionMatches(PyExc_SystemExit)) {
			/* but if it is truly a SystemExit on the main thread, we want the exit! */
			if (ts == slp_initial_tstate && !PyErr_ExceptionMatches(PyExc_TaskletExit))
				PyStackless_HandleSystemExit();
			PyErr_Clear();
			Py_INCREF(Py_None);
			retval = Py_None;
		}
		else {
			retval = slp_curexc_to_bomb();
			if (retval == NULL)
				return NULL;
		}
	}

	/*
	 * put the result back into the dead tasklet, to give
	 * possible referers access to the return value
	 */
	TASKLET_SETVAL_OWN(task, retval);

	if (ismain) {
		/*
		 * See whether we need to adjust main's context before
		 * returning
		 */
		if (ts->st.serial_last_jump != ts->st.serial) {
			slp_transfer_return(task->cstate);
		}
	}

	/* remove from runnables */
	slp_current_remove();

	/*
	 * clean up any current exception - this tasklet is dead.
	 * This only happens if we are killing tasklets in the middle
	 * of their execution.
         */
	if (ts->exc_type != NULL && ts->exc_type != Py_None) {
		Py_DECREF(ts->exc_type);
		Py_XDECREF(ts->exc_value);
		Py_XDECREF(ts->exc_traceback);
		ts->exc_type = ts->exc_value = ts->exc_traceback = NULL;
	}

	/* capture all exceptions */
	if (ismain) {
		/*
		 * Main wants to exit. We clean up, but leave the
		 * runnables chain intact.
		 */
		ts->st.main = NULL;
		Py_DECREF(task);
		return schedule_task_destruct(task, task);
	}

	next = ts->st.current;
	if (next == NULL) {
		int blocked = ts->st.main->flags.blocked;

		if (blocked) {
			char *txt;
			/* main was blocked and nobody can send */
			if (blocked < 0)
				txt = "the main tasklet is receiving"
				    " without a sender available.";
			else
				txt = "the main tasklet is sending"
				    " without a receiver available.";
			PyErr_SetString(PyExc_StopIteration, txt);
			/* fall through to error handling */
			retval = slp_curexc_to_bomb();
			if (retval == NULL)
				return NULL;
		}
		next = ts->st.main;
	}

	if (PyBomb_Check(retval)) {
		/*
		 * error handling: continue in the context of the main tasklet.
		 */
		next = ts->st.main;
		TASKLET_SETVAL(next, retval);
	}

	return schedule_task_destruct(task, next);
}

/*
  the following functions only have to handle "real"
  tasklets, those which need to switch the C stack.
  The "soft" tasklets are handled by frame pushing.
  It is not so much simpler than I thought :-(
*/

PyObject *
slp_run_tasklet(void)
{
	PyThreadState *ts = PyThreadState_GET();
	PyObject *retval;

	if ( (ts->st.main == NULL) && initialize_main_and_current()) {
		ts->frame = NULL;
		return NULL;
	}

	retval = ts->st.current->tempval;
	Py_INCREF(retval);

	if (PyBomb_Check(retval))
		retval = slp_bomb_explode(ts->st.current);
	while (ts->st.main != NULL) {
		/* XXX correct condition? or current? */
		retval = slp_frame_dispatch_top(retval);
		retval = tasklet_end(retval);
		if (STACKLESS_UNWINDING(retval))
			STACKLESS_UNPACK(retval);
	}
	return retval;
}

/* Clear out the free list */

void
slp_scheduling_fini(void)
{
	while (free_list != NULL) {
		PyBombObject *bomb = free_list;
		free_list = (PyBombObject *) free_list->curexc_type;
		PyObject_GC_Del(bomb);
		--numfree;
	}
	assert(numfree == 0);
}

#endif
