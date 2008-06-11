
#include "Python.h"

#ifdef STACKLESS

#ifndef STACKLESS
**********
If you see this error message,
your operating system is not supported yet.
Please provide an implementation of the switch_XXX.h
or disable the STACKLESS flag.
**********
#endif

#include "stackless_impl.h"

/*
 * the following macros are spliced into the OS/compiler
 * specific code, in order to simplify maintenance.
 */

static PyCStackObject **_cstprev, *_cst;
static PyTaskletObject *_prev;

#define __return(x) return (x)

#define SLP_SAVE_STATE(stackref, stsizediff) \
    intptr_t stsizeb; \
	stackref += STACK_MAGIC; \
	if (_cstprev != NULL) { \
        if (slp_cstack_new(_cstprev, stackref, _prev) == NULL) __return(-1); \
		stsizeb = slp_cstack_save(*_cstprev); \
	} \
	else \
        stsizeb = (_cst->startaddr - (intptr_t *)stackref) * sizeof(intptr_t); \
    if (_cst == NULL) __return(0); \
    stsizediff = stsizeb - (_cst->ob_size * sizeof(intptr_t));

#define SLP_RESTORE_STATE() \
	if (_cst != NULL) { \
		slp_cstack_restore(_cst); \
	}

/* This define is no longer needed now? */
#define SLP_EVAL
#include "platf/slp_platformselect.h"

#ifdef EXTERNAL_ASM
/* CCP addition: Make these functions, to be called from assembler.
 * The token include file for the given platform should enable the
 * EXTERNAL_ASM define so that this is included.
 */

/* There are two cases where slp_save_state would return 0, the
 * first where there is no difference in where the stack pointer
 * should be from where it is now.  And the second where
 * SLP_SAVE_STATE returns without restoring because we are only
 * here to save.  The assembler routine needs to differentiate
 * between these, which is why we override the returns and flag
 * the low bit of the return value on early exit.
 */
#undef __return
#define __return(x) { exitcode = x; goto exit; }

int slp_save_state(intptr_t *stack){
	int exitcode;
#ifdef SSIZE_T
	/* Only on Windows apparently. */
	SSIZE_T diff;
#else
	/* Py_ssize_t when we port to 2.5? */
	int diff;
#endif
	SLP_SAVE_STATE(stack, diff);
	return diff;
exit:
	/* hack: flag a problem by setting the value to odd */
	return exitcode | 1;
}

void slp_restore_state(void){
	SLP_RESTORE_STATE();
}

extern int slp_switch(void);

#endif

static int
climb_stack_and_transfer(PyCStackObject **cstprev, PyCStackObject *cst,
			 PyTaskletObject *prev)
{
	/*
	 * there are cases where we have been initialized
	 * in some deep stack recursion, but later on we
	 * need to switch from a higher stacklevel, and the
	 * needed stack size becomes *negative* :-))
	 */
	PyThreadState *ts = PyThreadState_GET();
    intptr_t probe;
    ptrdiff_t needed = &probe - ts->st.cstack_base;
	/* in rare cases, the need might have vanished due to the recursion */
    intptr_t *goobledigoobs;
	if (needed > 0) {
        goobledigoobs = alloca(needed * sizeof(intptr_t));
		if (goobledigoobs == NULL)
			return -1;
	}
	return slp_transfer(cstprev, cst, prev);
}

int
slp_transfer(PyCStackObject **cstprev, PyCStackObject *cst,
	     PyTaskletObject *prev)
{
	PyThreadState *ts = PyThreadState_GET();

	/* since we change the stack we must assure that the protocol was met */
	STACKLESS_ASSERT();

    if ((intptr_t *) &ts > ts->st.cstack_base)
		return climb_stack_and_transfer(cstprev, cst, prev);
	if (cst == NULL || cst->ob_size == 0)
		cst = ts->st.initial_stub;
	if (cst != NULL) {
		if (cst->tstate != ts) {
			PyErr_SetString(PyExc_SystemError,
				"bad thread state in transfer");
			return -1;
		}
		if (ts->st.cstack_base != cst->startaddr) {
			PyErr_SetString(PyExc_SystemError,
				"bad stack reference in transfer");
			return -1;
		}
		/* record the context of the target stack */
		ts->st.serial_last_jump = cst->serial;
		/*
		 * if stacks are same and refcount==1, it must be the same
		 * task. In this case, we would destroy the target before
		 * switching. Therefore, we simply don't switch, just save.
		 */
		if (cstprev && *cstprev == cst && cst->ob_refcnt == 1)
			cst = NULL;
	}
	_cstprev = cstprev;
	_cst = cst;
	_prev = prev;
	return slp_switch();
}

#ifdef Py_DEBUG
int
slp_transfer_return(PyCStackObject *cst)
{
	return slp_transfer(NULL, cst, NULL);
}
#endif

/* experimental feature:
   Doing a real stack switch.
   I still have no exact clue how to fit this
   into the rest of the system...
 */

#define SLP_STACK_BEGIN(stackref, stsizediff) \
	int stsizeb; \
	\
	stackref += STACK_MAGIC; \
	if (_cstprev != NULL) { \
		if (slp_cstack_new(_cstprev, stackref, _prev) == NULL) \
			return -1; \
		stsizeb = slp_cstack_save(*_cstprev); \
	} \
	else \
		stsizeb = (_cst->startaddr - stackref) * sizeof(int*); \
	if (_cst == NULL) return 0; \
	stsizediff = stsizeb - (_cst->ob_size * sizeof(int*));

#define SLP_STACK_END() \
	if (_cst != NULL) { \
		slp_cstack_restore(_cst); \
	}

#if 0
/* disabled by now. Also need support for x64 asm file... */
#include "platf/slp_switch_stack.h"

int
slp_transfer_stack(PyCStackObject **cstprev, PyCStackObject *cst)
{
	/* this is defunct, no idea how it must be */
	return slp_switch_stack();
}
#endif

#endif
