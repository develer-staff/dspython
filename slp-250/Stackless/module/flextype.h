#ifndef Py_FLEXTYPE_H
#define Py_FLEXTYPE_H
#ifdef __cplusplus
extern "C" {
#endif

#include "structmember.h"

typedef struct _pycmethoddef {
	char        *name;      /* name to lookup in __dict__ */
	PyCFunction match;      /* to be found if non-overridden */
	void        *fast;      /* native C call */
	void        *wrap;      /* wrapped call into Python */
	int         offset;     /* slot offset in heap type */
} PyCMethodDef;

/* helpers for filling these structures in. */

/*
 * a public entry defines 
 * - the function name      "name"
 * - the PyCFunction        class_name       which originally is seen from Python, 
 * - the fast function      impl_class_name  that implements the method for C
 * - the wrapper function   wrap_class_name  that calls back into a Python override.
 */

#define CMETHOD_PUBLIC_ENTRY(type, prefix, name) \
	{ \
	#name, (PyCFunction)prefix##_##name, \
	&impl_##prefix##_##name, &wrap_##prefix##_##name, \
	offsetof(type, name) \
	}

/*
 * a private entry defines 
 * - the function name      "name"
 * - the fast function      impl_class_name  that implements the method for C
 * this allows to do inheritance in C without publishing to Python.
 */

#define CMETHOD_PRIVATE_ENTRY(type, prefix, name) \
    {#name, NULL, \
    &impl_##prefix##_##name, NULL, \
    offsetof(type, name)}

typedef struct _flexheaptypeobject {
	PyHeapTypeObject type;
	PyCMethodDef *tp_cmethods;
} PyFlexTypeObject;

PyAPI_DATA(PyTypeObject *) PyFlexType_TypePtr;
#define PyFlexType_Type (*PyFlexType_TypePtr)
#define PyFlexType_Check(op) PyObject_TypeCheck(op, PyFlexType_TypePtr)
#define PyFlexType_CheckExact(op) ((op)->ob_type == PyFlexType_TypePtr)

/* build a new type and its meta-type */

PyAPI_FUNC(PyTypeObject *) PyFlexType_Build( char *modulename,
					     char *type_name,
					     char *doc,
					     PyTypeObject *base,
					     size_t type_size,
					     PyCMethodDef *ml );

int init_flextype(void);

#ifdef __cplusplus
}
#endif
#endif /* !Py_FLEXTYPE_H */
