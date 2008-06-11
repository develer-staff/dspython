#include "Python.h"
#ifdef STACKLESS

#include "compile.h"
#include "frameobject.h"
#include "structmember.h"

#include "stackless_impl.h"
#include "pickling/prickelpit.h"

/* platform specific constants */
#include "platf/slp_platformselect.h"

/* Stackless extension for ceval.c */

/******************************************************

  Static Global Variables

*******************************************************/

/* the flag which decides whether we try to use soft switching */

int slp_enable_softswitch = 1;

/* 
 * flag whether the next call should try to be stackless.
 * The protocol is: This flag may be only set if the called
 * thing supports it. It doesn't matter whether it uses the
 * chance, but it *must* set it to zero before returning.
 * This flags in a way serves as a parameter that we don't have.
 */
int slp_try_stackless = 0;

/* the list of all stacks of all threads */
struct _cstack *slp_cstack_chain = NULL;


/******************************************************

  The C Stack

 ******************************************************/

static PyCStackObject *cstack_cache[CSTACK_SLOTS] = { NULL };
static int cstack_cachecount = 0;

/* this function will get called by PyStacklessEval_Fini */
static void slp_cstack_cacheclear(void)
{
	int i;
	PyCStackObject *stack;

	for (i=0; i < CSTACK_SLOTS; i++) {
		while (cstack_cache[i] != NULL) {
			stack = cstack_cache[i];
			cstack_cache[i] = (PyCStackObject *) stack->startaddr;
			PyObject_Del(stack);
		}
	}
	cstack_cachecount = 0;
}

static void
cstack_dealloc(PyCStackObject *cst)
{
	slp_cstack_chain = cst;
	SLP_CHAIN_REMOVE(PyCStackObject, &slp_cstack_chain, cst, next, 
			 prev);
	if (cst->ob_size >= CSTACK_SLOTS) {
		PyObject_Del(cst);
	}
	else {
		if (cstack_cachecount >= CSTACK_MAXCACHE)
			slp_cstack_cacheclear();
        cst->startaddr = (intptr_t *) cstack_cache[cst->ob_size];
		cstack_cache[cst->ob_size] = cst;
		++cstack_cachecount;
	}
}


PyCStackObject *
slp_cstack_new(PyCStackObject **cst, intptr_t *stackref, PyTaskletObject *task)
{
	PyThreadState *ts = PyThreadState_GET();
	intptr_t *stackbase = ts->st.cstack_base;
	ptrdiff_t size = stackbase - stackref;

	assert(size >= 0);

	if (*cst != NULL) {
		if ((*cst)->task == task)
			(*cst)->task = NULL;
		Py_DECREF(*cst);
	}
	if (size < CSTACK_SLOTS && ((*cst) = cstack_cache[size])) {
		/* take stack from cache */
		cstack_cache[size] = (PyCStackObject *) (*cst)->startaddr;
		--cstack_cachecount;
		_Py_NewReference((PyObject *)(*cst));
	}
	else
		*cst = PyObject_NewVar(PyCStackObject, &PyCStack_Type, size);
	if (*cst == NULL) return NULL;

	(*cst)->startaddr = stackbase;
	(*cst)->next = (*cst)->prev = NULL;
	SLP_CHAIN_INSERT(PyCStackObject, &slp_cstack_chain, *cst, next, prev);
	(*cst)->serial = ts->st.serial;
	(*cst)->task = task;
	(*cst)->tstate = ts;
	(*cst)->nesting_level = ts->st.nesting_level;
	return *cst;
}

size_t
slp_cstack_save(PyCStackObject *cstprev)
{
    size_t stsizeb = (cstprev)->ob_size * sizeof(intptr_t);

	memcpy((cstprev)->stack, (cstprev)->startaddr - 
				 (cstprev)->ob_size, stsizeb);
	return stsizeb;
}

void
slp_cstack_restore(PyCStackObject *cst)
{
	cst->tstate->st.nesting_level = cst->nesting_level;
	/* mark task as no longer responsible for cstack instance */
	cst->task = NULL;
	memcpy(cst->startaddr - cst->ob_size, &cst->stack,
	       (cst->ob_size) * sizeof(intptr_t));
}


static char cstack_doc[] =
"A CStack object serves to save the stack slice which is involved\n\
during a recursive Python call. It will also be used for pickling\n\
of program state. This structure is highly platform dependant.\n\
Note: For inspection, str() can dump it as a string.\
";

#if SIZEOF_VOIDP == SIZEOF_INT
#define T_ADDR T_UINT
#else
#define T_ADDR T_ULONG
#endif


static PyMemberDef cstack_members[] = {
	{"size", T_INT, offsetof(PyCStackObject, ob_size), READONLY},
	{"next", T_OBJECT, offsetof(PyCStackObject, next), READONLY},
	{"prev", T_OBJECT, offsetof(PyCStackObject, prev), READONLY},
	{"task", T_OBJECT, offsetof(PyCStackObject, task), READONLY},
	{"startaddr", T_ADDR, offsetof(PyCStackObject, startaddr), READONLY},
	{0}
};

/* simple string interface for inspection */

static PyObject *
cstack_str(PyObject *o)
{
	PyCStackObject *cst = (PyCStackObject*)o;
	return PyString_FromStringAndSize((char*)&cst->stack,
	    cst->ob_size*sizeof(cst->stack[0]));
}

PyTypeObject PyCStack_Type = {
	PyObject_HEAD_INIT(&PyType_Type)
	0,
	"stackless.cstack",
	sizeof(PyCStackObject),
	sizeof(PyObject *),
	(destructor)cstack_dealloc,	/* tp_dealloc */
	0,				/* tp_print */
	0,				/* tp_getattr */
	0,				/* tp_setattr */
	0,				/* tp_compare */
	0,				/* tp_repr */
	0,				/* tp_as_number */
	0,				/* tp_as_sequence */
	0,				/* tp_as_mapping */
	0,				/* tp_hash */
	0,				/* tp_call */
	(reprfunc)cstack_str,		/* tp_str */
	PyObject_GenericGetAttr,	/* tp_getattro */
	PyObject_GenericSetAttr,	/* tp_setattro */
	0,				/* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,		/* tp_flags */
	cstack_doc,			/* tp_doc */
	0,				/* tp_traverse */
	0,				/* tp_clear */
	0,				/* tp_richcompare */
	0,				/* tp_weaklistoffset */
	0,				/* tp_iter */
	0,				/* tp_iternext */
	0,				/* tp_methods */
	cstack_members,			/* tp_members */
};


static int
make_initial_stub(void)
{
	PyThreadState *ts = PyThreadState_GET();

	if (ts->st.initial_stub != NULL) {
		Py_DECREF(ts->st.initial_stub);
		ts->st.initial_stub = NULL;
	}
	ts->st.serial_last_jump = ++ts->st.serial;
	if (slp_transfer(&ts->st.initial_stub, NULL, NULL)) return -1;
	/* 
	 * from here, we always arrive with a compatible cstack
	 * that also can be used by main, if it is running
	 * in soft-switching mode.
	 * To insure that, it was necessary to re-create the
	 * initial stub for *every* run of a new main.
	 * This will vanish with greenlet-like stack management.
	 */

	return 0;
}

static PyObject *
climb_stack_and_eval_frame(PyFrameObject *f)
{
	/* 
	 * a similar case to climb_stack_and_transfer,
	 * but here we need to incorporate a gap in the
	 * stack into main and keep this gap on the stack.
	 * This way, initial_stub is always valid to be
	 * used to return to the main c stack.
	 */
	PyThreadState *ts = PyThreadState_GET();
    intptr_t probe;
    ptrdiff_t needed = &probe - ts->st.cstack_base;
	/* in rare cases, the need might have vanished due to the recursion */
    intptr_t *goobledigoobs;
	if (needed > 0) {
        goobledigoobs = alloca(needed * sizeof(intptr_t));
		if (goobledigoobs == NULL)
			return NULL;
	}
	return slp_eval_frame(f);
}


PyObject *
slp_eval_frame(PyFrameObject *f)
{
	PyThreadState *ts = PyThreadState_GET();
	PyFrameObject *fprev = f->f_back;
	intptr_t * stackref;

	if (fprev == NULL && ts->st.main == NULL) {
		/* this is the initial frame, so mark the stack base */

		/* 
		 * careful, this caused me a major headache.
		 * it is *not* sufficient to just check for fprev == NULL.
		 * Reason: (observed with wxPython):
		 * A toplevel frame is run as a tasklet. When its frame
		 * is deallocated (in tasklet_end), a Python object
		 * with a __del__ method is destroyed. This __del__
		 * will run as a toplevel frame, with f_back == NULL!
		 */

        stackref = STACK_REFPLUS + (intptr_t *) &f;
		if (ts->st.cstack_base == NULL)
			ts->st.cstack_base = stackref - CSTACK_GOODGAP;
		if (stackref > ts->st.cstack_base)
			return climb_stack_and_eval_frame(f);

		ts->frame = f;
		if (make_initial_stub())
			return NULL;
		return slp_run_tasklet();
	}
	Py_INCREF(Py_None);
	return slp_frame_dispatch(f, fprev, 0, Py_None);
}

void slp_kill_tasks_with_stacks(PyThreadState *ts)
{
	int count = 0;

	while (1) {
		PyCStackObject *csfirst = slp_cstack_chain, *cs;
		PyTaskletObject *t, *task;
		PyTaskletObject **chain;

		if (csfirst == NULL)
			break;
		for (cs = csfirst; ; cs = cs->next) {
			if (count && cs == csfirst) {
				/* nothing found */
				return;
			}
			++count;
			if (cs->task == NULL)
				continue;
			if (ts != NULL && cs->tstate != ts)
				continue;
			break;
		} 
		count = 0;
		t = cs->task;
		Py_INCREF(t);

		/* We need to ensure that the tasklet 't' is in the scheduler
		 * tasklet chain before this one (our main).  This ensures
		 * that this one is directly switched back to after 't' is
		 * killed.  The reason we do this this is because if another
		 * tasklet is switched to, this is of course it being scheduled
		 * and run.  Why we do not need to do this for tasklets blocked
		 * on channels is that when they are scheduled to be run and
		 * killed, they will be implicitly placed before this one,
		 * leaving it to run next.
		 */
		if (!t->flags.blocked && t != cs->tstate->st.main) {
			chain = &t;
			SLP_CHAIN_REMOVE(PyTaskletObject, chain, task, next, prev)
			chain = &cs->tstate->st.main;
			task = cs->task;
			SLP_CHAIN_INSERT(PyTaskletObject, chain, task, next, prev);
			cs->tstate->st.current = cs->tstate->st.main;
			t = cs->task;
		}

		PyTasklet_Kill(t);
		PyErr_Clear();

		if (t->f.frame == 0) {
			/* ensure a valid tstate */
			t->cstate->tstate = slp_initial_tstate;
		}
		Py_DECREF(t);
	}
}

void PyStackless_kill_tasks_with_stacks(int allthreads)
{
	PyThreadState *ts = PyThreadState_Get();

	if (ts->st.main == NULL)
		initialize_main_and_current();
	slp_kill_tasks_with_stacks(allthreads ? NULL : ts);
}


/* cstack spilling for recursive calls */

static PyObject *
eval_frame_callback(PyFrameObject *f, int exc, PyObject *retval)
{
	PyThreadState *ts = PyThreadState_GET();
	PyTaskletObject *cur = ts->st.current;
	PyCStackObject *cst = cur->cstate;
	PyCFrameObject *cf = (PyCFrameObject *) f;

	ts->st.nesting_level = cf->n;
	ts->frame = f->f_back;
	Py_DECREF(f);
	cur->cstate = NULL;
	retval = PyEval_EvalFrameEx_slp(ts->frame, exc, retval);
	if (retval == NULL)
		retval = slp_curexc_to_bomb();
	if (retval == NULL)
		return NULL;
	TASKLET_SETVAL_OWN(cur, retval);
	/* jump back */
	Py_XDECREF(cur->cstate);
	cur->cstate = cst;
	slp_transfer_return(cst);
	/* never come here */
	return NULL;
}

PyObject *
slp_eval_frame_newstack(PyFrameObject *f, int exc, PyObject *retval)
{
	PyThreadState *ts = PyThreadState_GET();
	PyTaskletObject *cur = ts->st.current;
	PyCFrameObject *cf = NULL;
	PyCStackObject *cst;

	if (ts->st.cstack_root == NULL) {
		/* this is a toplevel call */
		ts->st.cstack_root = STACK_REFPLUS + (intptr_t *) &f;
		retval = PyEval_EvalFrameEx_slp(f, exc, retval);
		return retval;
	}

	ts->frame = f;
	cf = slp_cframe_new(eval_frame_callback, 1);
	if (cf == NULL)
		return NULL;
	cf->n = ts->st.nesting_level;
	ts->frame = (PyFrameObject *) cf;
	cst = cur->cstate;
	cur->cstate = NULL;
	Py_XDECREF(retval);
	if (slp_transfer(&cur->cstate, NULL, cur))
		goto finally; /* fatal */
	Py_XDECREF(cur->cstate);
	retval = cur->tempval;
	Py_INCREF(retval);
	if (PyBomb_Check(retval))
		retval = slp_bomb_explode(cur);
finally:
	cur->cstate = cst;
	return retval;
}

/******************************************************

  Generator re-implementation for Stackless

*******************************************************/

typedef struct {
	PyObject_HEAD
	/* The gi_ prefix is intended to remind of generator-iterator. */

	PyFrameObject *gi_frame;

	/* True if generator is being executed. */ 
	int gi_running;

	/* List of weak reference. */
	PyObject *gi_weakreflist;
} genobject;

/*
 * Note:
 * Generators are quite a bit slower in Stackless, because
 * we are jumping in and out so much.
 * I had an implementation with no extra cframe, but it
 * was not faster, but considerably slower than this solution.
 */

static PyObject* gen_iternext_callback(PyFrameObject *f, int exc, PyObject *retval);

PyObject *
slp_gen_send_ex(PyGenObject *ob, PyObject *arg, int exc)
{
	STACKLESS_GETARG();
	genobject *gen = (genobject *) ob;
	PyThreadState *ts = PyThreadState_GET();
	PyFrameObject *f = gen->gi_frame;
	PyFrameObject *stopframe = ts->frame;
	PyObject *retval;

	if (gen->gi_running) {
		PyErr_SetString(PyExc_ValueError,
				"generator already executing");
		return NULL;
	}
	if (f==NULL || f->f_stacktop == NULL) {
		/* Only set exception if called from send() */
		if (arg && !exc)
			PyErr_SetNone(PyExc_StopIteration);
		return NULL;
	}

	if (f->f_back == NULL &&
		(f->f_back = (PyFrameObject *)
			 slp_cframe_new(gen_iternext_callback, 0)) == NULL)
		return NULL;

	if (f->f_lasti == -1) {
		if (arg && arg != Py_None) {
			PyErr_SetString(PyExc_TypeError,
					"can't send non-None value to a "
					"just-started generator");
			return NULL;
		}
	} else {
		/* Push arg onto the frame's value stack */
		retval = arg ? arg : Py_None;
		Py_INCREF(retval);
	        *(f->f_stacktop++) = retval;
	}

	/* XXX give the patch to python-dev */
	f->f_tstate = ts;
	/* Generators always return to their most recent caller, not
	 * necessarily their creator. */
	Py_XINCREF(ts->frame);
	assert(f->f_back != NULL);
	assert(f->f_back->f_back == NULL);
	f->f_back->f_back = ts->frame;

	gen->gi_running = 1;

	f->f_execute = PyEval_EvalFrameEx_slp;

	/* make refcount compatible to frames for tasklet unpickling */
	Py_INCREF(f->f_back);

	Py_INCREF(gen);
	Py_XINCREF(arg);
	((PyCFrameObject *) f->f_back)->ob1 = (PyObject *) gen;
	((PyCFrameObject *) f->f_back)->ob2 = arg;
	Py_INCREF(f);
	ts->frame = f;

	retval = Py_None;
	Py_INCREF(retval);

	if (stackless)
		return STACKLESS_PACK(retval);
	return slp_frame_dispatch(f, stopframe, exc, retval);
}

static PyObject*
gen_iternext_callback(PyFrameObject *f, int exc, PyObject *result)
{
	PyThreadState *ts = PyThreadState_GET();
	PyCFrameObject *cf = (PyCFrameObject *) f;
	genobject *gen = (genobject *) cf->ob1;
	PyObject *arg = cf->ob2;

	gen->gi_running = 0;
	/* make refcount compatible to frames for tasklet unpickling */
	Py_DECREF(f);

	/* Don't keep the reference to f_back any longer than necessary.  It
	 * may keep a chain of frames alive or it could create a reference
	 * cycle. */
	ts->frame = f->f_back;
	Py_XDECREF(f->f_back);
	f->f_back = NULL;

	f = gen->gi_frame;
	/* If the generator just returned (as opposed to yielding), signal
	 * that the generator is exhausted. */
	if (result == Py_None && f->f_stacktop == NULL) {
		Py_DECREF(result);
		result = NULL;
		if (arg)
			PyErr_SetNone(PyExc_StopIteration);
		/* Stackless extra handling */
		/* are we awaited by a for_iter or called by next() ? */
		else if (ts->frame->f_execute != PyEval_EvalFrame_iter) {
			/* do the missing part of the next call */
			if (!PyErr_Occurred())
				PyErr_SetNone(PyExc_StopIteration);
		}
	}

	if (!result || f->f_stacktop == NULL) {
		/* generator can't be rerun, so release the frame */
		gen->gi_frame = NULL;
	}

	cf->ob1 = NULL;
	cf->ob2 = NULL;
	Py_DECREF(gen);
	Py_XDECREF(arg);
	return result;
}


/******************************************************

  Rebirth of software stack avoidance

*******************************************************/

static PyObject *
unwind_repr(PyObject *op)
{
	return PyString_FromString(
		"The invisible unwind token. If you ever should see this,\n"
		"please report the error to tismer@tismer.com"
	);
}

/* dummy deallocator, just in case */
static void unwind_dealloc(PyObject *op) {
}

static PyTypeObject PyUnwindToken_Type = {
	PyObject_HEAD_INIT(&PyUnwindToken_Type)
	0,
	"UnwindToken",
	0,
	0,
	(destructor)unwind_dealloc, /*tp_dealloc*/ /*should never be called*/
	0,		/*tp_print*/
	0,		/*tp_getattr*/
	0,		/*tp_setattr*/
	0,		/*tp_compare*/
	(reprfunc)unwind_repr, /*tp_repr*/
	0,		/*tp_as_number*/
	0,		/*tp_as_sequence*/
	0,		/*tp_as_mapping*/
	0,		/*tp_hash */
};

static PyUnwindObject unwind_token = {
	PyObject_HEAD_INIT(&PyUnwindToken_Type)
	NULL
};

PyUnwindObject *Py_UnwindToken = &unwind_token;

/* 
    the frame dispatcher will execute frames and manage
    the frame stack until the "previous" frame reappears.
    The "Mario" code if you know that game :-)
 */

PyObject *
slp_frame_dispatch(PyFrameObject *f, PyFrameObject *stopframe, int exc, PyObject *retval)
{
	PyThreadState *ts = PyThreadState_GET();

	++ts->st.nesting_level;

/* 
    frame protocol:
    If a frame returns the Py_UnwindToken object, this 
    indicates that a different frame will be run. 
    Semantics of an appearing Py_UnwindToken:
    The true return value is in its tempval field.
    We always use the topmost tstate frame and bail
    out when we see the frame that issued the
    originating dispatcher call (which may be a NULL frame).
 */

	while (1) {
		retval = f->f_execute(f, exc, retval);
		f = ts->frame;
		if (STACKLESS_UNWINDING(retval))
			STACKLESS_UNPACK(retval);
		if (f == stopframe)
			break;
		exc = 0;
	}
	--ts->st.nesting_level;
	/* see whether we need to trigger a pending interrupt */
	/* note that an interrupt handler guarantees current to exist */
	if (ts->st.interrupt != NULL &&
	    ts->st.current->flags.pending_irq)
		slp_check_pending_irq();
	return retval;
}

PyObject *
slp_frame_dispatch_top(PyObject *retval)
{
	PyThreadState *ts = PyThreadState_GET();
	PyFrameObject *f = ts->frame;

	if (f==NULL) return retval;

	while (1) {

		retval = f->f_execute(f, 0, retval);
		f = ts->frame;
		if (STACKLESS_UNWINDING(retval))
			STACKLESS_UNPACK(retval);
		if (f == NULL)
			break;
	}
	return retval;
}

/* Clear out the free list */

void
slp_stacklesseval_fini(void)
{
	slp_cstack_cacheclear();
}

#endif /* STACKLESS */
