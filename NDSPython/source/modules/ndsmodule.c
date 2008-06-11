#include "Python.h"
#include <malloc.h>
#include <stdio.h>

PyDoc_STRVAR(nds_mallinfo_doc,
"mallinfo() -> returns memory allocation information");

static PyObject *
nds_mallinfo(PyObject *self, PyObject *args)
{
	struct mallinfo m;
    PyObject *d = NULL;
	PyObject *k, *v;

    d = PyDict_New();
    if (d == NULL)
        return NULL;

	m = mallinfo();

	/* The total amount of space in the heap. */
	k = PyString_FromString("arena");
	v = PyInt_FromLong((long)m.arena);
	PyDict_SetItem(d, k, v);
	Py_DECREF(k);
	Py_DECREF(v);

	/* The number of chunks not in use. */
	k = PyString_FromString("ordblks");
	v = PyInt_FromLong((long)m.ordblks);
	PyDict_SetItem(d, k, v);
	Py_DECREF(k);
	Py_DECREF(v);

	/* The total amount of space allocated by malloc. */
	k = PyString_FromString("uordblks");
	v = PyInt_FromLong((long)m.uordblks);
	PyDict_SetItem(d, k, v);
	Py_DECREF(k);
	Py_DECREF(v);

	/* The total amount of space not in use. */
	k = PyString_FromString("fordblks");
	v = PyInt_FromLong((long)m.fordblks);
	PyDict_SetItem(d, k, v);
	Py_DECREF(k);
	Py_DECREF(v);

	/* The size of the topmost memory block. */
	k = PyString_FromString("keepcost");
	v = PyInt_FromLong((long)m.keepcost);
	PyDict_SetItem(d, k, v);
	Py_DECREF(k);
	Py_DECREF(v);

	return d;
}

PyDoc_STRVAR(nds_meminfo_doc,
"meminfo() -> prints stack usage information");

/* from ds_arm9.ld */
#define NDS_STACK_END (unsigned int)0x023ff000

extern char *fake_heap_end;

static PyObject *
nds_meminfo(PyObject *self, PyObject *args)
{
	unsigned int stackSize = NDS_STACK_END - (unsigned int)fake_heap_end;
	/* Next line taken from the newlib patches.. */
	extern char   end asm ("end");	/* Defined by the linker.  */
	struct mallinfo m = mallinfo();
	unsigned int heapSize = (unsigned int)fake_heap_end - (unsigned int)&end;

	printf("Heap:\n");
	printf(" start          %x\n", (unsigned int)&end);
	printf(" end            %x\n", (unsigned int)fake_heap_end);
	printf(" size  (system) %d\n", heapSize);
	printf(" size  (malloc) %d\n", m.arena);
	printf(" usage (malloc) %2d%% (%d)\n", (100 * m.uordblks)/m.arena, m.uordblks);
	printf(" usage (system) %2d%%\n", (100 * m.uordblks)/heapSize);

	printf("Stack:\n");
	printf(" start    %x\n", (unsigned int)fake_heap_end);
	printf(" end      %x\n", (unsigned int)NDS_STACK_END);
	printf(" current  %x\n", (unsigned int)&stackSize);
	printf(" usage    %2d%% (%d/%d)\n", \
	    (unsigned int)((100*(NDS_STACK_END-(unsigned int)&stackSize))/(float)stackSize), \
	    NDS_STACK_END-(unsigned int)&stackSize, \
	    stackSize);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyMethodDef nds_methods[] = {
	{"mallinfo",	nds_mallinfo,	METH_NOARGS,	nds_mallinfo_doc},
	{"meminfo",		nds_meminfo,	METH_NOARGS,	nds_meminfo_doc},
	{NULL,			NULL}		/* sentinel */
};


PyDoc_STRVAR(module_doc,
"This module is always available.  It provides access to the Nintendo DS support functionality.");

PyMODINIT_FUNC
initnds(void)
{
	Py_InitModule3("nds", nds_methods, module_doc);
	return;
}
