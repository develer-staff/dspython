
/* extension to type_new in typeobject.c */

#include "Python.h"
#include "flextype.h"

/* 
 * this does not work in general with python 2.3, since it refuses to deallocate
 * variables or slots if the type is not GC. For the local purpose in this module 
 * it works. See for instance below in flextype_new(...) and type_clone(...)
 * XXX maybe discuss on python-dev again?
 * Note: we still need it in clone.
 */

static void
reset_gc(PyTypeObject *type)
{
	PyTypeObject *base = type->tp_base;
	/* convince the type *not* to use GC unless intended */
	if (type->tp_flags & Py_TPFLAGS_HAVE_GC && !(base->tp_flags & Py_TPFLAGS_HAVE_GC)) {
		type->tp_free = base->tp_free;
		type->tp_traverse = base->tp_traverse;
		type->tp_clear = base->tp_clear;
		type->tp_is_gc = base->tp_is_gc;
		type->tp_flags &= ~Py_TPFLAGS_HAVE_GC;
	}
}

static int
find_size(PyObject * bases, int size)
{
	int i, n = PyTuple_GET_SIZE(bases);

	for (i=0; i<n; ++i) {
		PyObject *op = PyTuple_GET_ITEM(bases, i);
		int sz = op->ob_type->tp_basicsize;
		if (sz > size)
			size = sz;
	}
	return size;
}

static PyObject *
builddict(char *modulename, char *doc)
{
	return Py_BuildValue("{s:s,s:s,s:[]}",
			     "__module__", modulename,
			     "__doc__", doc,
			     "__slots__");
	/* no slots because we have tp_members. But the entry is needed
	   to stop typeobject from creating weakrefs and dicts.
	 */
}

static PyTypeObject *methdescr_type = NULL;

static int bind_last_to_first( PyTypeObject *type, PyTypeObject *current)
{
	PyCMethodDef *ml;
	if (current->tp_base != NULL &&
	    PyType_IsSubtype(current->tp_base->ob_type, &PyFlexType_Type))
		if (bind_last_to_first(type, current->tp_base))
			return -1;
	ml = ((PyFlexTypeObject *) current)->tp_cmethods;
	while (ml && ml->name) {
		char *p = (char*) type;
		void **fp = (void*) (p+ml->offset);
		int use_fast = 0;

		if (ml->match != NULL) {
			/* public Python method, see if it is overridden */
			PyObject *op = PyObject_GetAttrString(
			    (PyObject *) type, ml->name);
			if (op == NULL) 
				return -1; /* this may never happen */
			if (PyType_IsSubtype(op->ob_type, methdescr_type)) {
				PyMethodDescrObject *descr;
				
				descr = (PyMethodDescrObject *) op;
				if (descr->d_method->ml_meth == ml->match)
					use_fast = 1;
			}
			Py_DECREF(op);
		}
		else {
			/* private C only method, always use fast */
			use_fast = 1;
		}
		*fp = use_fast ? ml->fast : ml->wrap;
		++ml;
	}
	return 0;
}

static int
bindmethods( PyTypeObject *type )
{
        if (methdescr_type == NULL) {
	        /* 
		 * PyMethodDescr_Type is not published. We retrieve a
		 * known method. 
		 */
		PyObject *mro_descr = PyObject_GetAttrString(
		    (PyObject *)&PyType_Type, "mro");
		if (mro_descr == NULL) return -1;
		methdescr_type = mro_descr->ob_type;
		Py_DECREF(mro_descr);
	}
	/* walk down through the bases and resolve methods */
	return bind_last_to_first(type, type);
}

/* this one method is exposed to Python */
static PyObject *
flextype_new(PyTypeObject *meta, PyObject *args, PyObject *kwds)
{
        PyObject *name, *bases, *dict;
	static char *kwlist[] = {"name", "bases", "dict", 0};
	PyFlexTypeObject *type;
	int basicsize = meta->tp_basicsize;
	int type_size = basicsize;

	if (!PyArg_ParseTupleAndKeywords(args, kwds, "SO!O!:type", kwlist,
					 &name,
					 &PyTuple_Type, &bases,
					 &PyDict_Type, &dict))
		return NULL;
	assert(PyType_IsSubtype(meta, &PyFlexType_Type));
	type_size = find_size(bases, type_size);
	meta->tp_basicsize = type_size;
	type = (PyFlexTypeObject *) PyType_Type.tp_new(meta, args, kwds);
	meta->tp_basicsize = basicsize;
	if (type == NULL) 
		return NULL;
	/* we can't do that in 2.3, it would break */
#if 0
	reset_gc( (PyTypeObject *) type);
#endif
	if (bindmethods((PyTypeObject *) type)) {
		Py_DECREF((PyObject *) type);
		return NULL;
	}
	return (PyObject *) type;
}


static PyTypeObject *
type_clone(PyTypeObject *meta, PyTypeObject *base, char *typename, PyObject *dict,
	   size_t type_size, PyCMethodDef *ml)
{
        PyObject *args = Py_BuildValue("(s(O)O)", typename, base, dict);
	int basicsize = meta->tp_basicsize;
	PyFlexTypeObject *type;

        assert(type_size >= (size_t) meta->tp_basicsize);
	if (args == NULL) 
		return NULL;
	meta->tp_basicsize = type_size;
	type = (PyFlexTypeObject *) meta->tp_new(meta, args, NULL);
	meta->tp_basicsize = basicsize;
	Py_DECREF(args);
	if (type == NULL) 
		return NULL;
	reset_gc( (PyTypeObject *) type);
	type->tp_cmethods = ml;
	if (bindmethods( (PyTypeObject *) type) ) {
		Py_DECREF( (PyObject *) type);
		return NULL;
	}
	return (PyTypeObject *) type;
}

static PyTypeObject *
make_meta(char *modulename, char *type_name, size_t type_size)
{
	char metaname[200];
	PyObject *dict;
	PyTypeObject *meta, *ft = &PyFlexType_Type;

	sprintf(metaname, "%.128s-meta", type_name);
	if ( (dict = builddict(modulename, ft->tp_doc)) == NULL) 
		return NULL;
	meta = type_clone( ft, ft, metaname, dict, type_size, NULL);
	if (meta == NULL) 
		return NULL;
	meta->tp_new = flextype_new;
	Py_DECREF(dict);
	return meta;
}

PyTypeObject * PyFlexType_Build( char *modulename,
				 char *type_name,
				 char *doc,
				 PyTypeObject *base,
				 size_t type_size,
				 PyCMethodDef *ml )
{
	PyObject *dict;
	PyTypeObject *t = NULL, *meta = NULL;

	if ( (dict = builddict(modulename, doc)) == NULL) 
		return NULL;
	if ((meta = make_meta(modulename, type_name, type_size)) == NULL)
		return NULL;
	t = type_clone( meta, base, type_name, dict, type_size, ml);
	if (t == NULL) return NULL;
	Py_DECREF(meta);
	Py_DECREF(dict);
	return t;
}

PyTypeObject * PyFlexType_TypePtr = NULL;

static char pyflextype__doc__[] =
"An extension type that supports cached virtual C methods";

int
init_flextype(void)
{
	PyObject *dict;
	PyTypeObject *type;

	if ( (dict = builddict("stackless", pyflextype__doc__)) == NULL)
		return -1;
	type = (PyTypeObject *)
	    type_clone( &PyType_Type, &PyType_Type, "flextype", dict,
			sizeof(PyFlexTypeObject), NULL);
	if (type == NULL) return -1;
	type->tp_new = flextype_new;
	Py_DECREF(dict);
	PyFlexType_TypePtr = type;
	return 0;
}

