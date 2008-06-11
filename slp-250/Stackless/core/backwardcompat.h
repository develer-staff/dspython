#ifndef PyAPI_DATA

/* 
 * this is a partial extract from 2.3's pyport.h.
 * We try to make new-style declarations work.
 */

#if defined(__CYGWIN__) || defined(__BEOS__)
#	define HAVE_DECLSPEC_DLL
#endif

#if defined(Py_ENABLE_SHARED) /* only get special linkage if built as shared */
#	if defined(HAVE_DECLSPEC_DLL)
#		ifdef Py_BUILD_CORE
#			define PyAPI_FUNC(RTYPE) __declspec(dllexport) RTYPE
#			define PyAPI_DATA(RTYPE) extern __declspec(dllexport) RTYPE
			/* module init functions inside the core need no external linkage */
#			define PyMODINIT_FUNC void
#		else /* Py_BUILD_CORE */
			/* Building an extension module, or an embedded situation */
			/* public Python functions and data are imported */
			/* Under Cygwin, auto-import functions to prevent compilation */
			/* failures similar to http://python.org/doc/FAQ.html#3.24 */
#			if !defined(__CYGWIN__)
#				define PyAPI_FUNC(RTYPE) __declspec(dllimport) RTYPE
#			endif /* !__CYGWIN__ */
#			define PyAPI_DATA(RTYPE) extern __declspec(dllimport) RTYPE
			/* module init functions outside the core must be exported */
#			if defined(__cplusplus)
#				define PyMODINIT_FUNC extern "C" __declspec(dllexport) void
#			else /* __cplusplus */
#				define PyMODINIT_FUNC __declspec(dllexport) void
#			endif /* __cplusplus */
#		endif /* Py_BUILD_CORE */
#	endif /* HAVE_DECLSPEC */
#endif /* Py_ENABLE_SHARED */

/* If no external linkage macros defined by now, create defaults */
#ifndef PyAPI_FUNC
#	define PyAPI_FUNC(RTYPE) RTYPE
#endif
#ifndef PyAPI_DATA
#	define PyAPI_DATA(RTYPE) extern RTYPE
#endif
#ifndef PyMODINIT_FUNC
#	if defined(__cplusplus)
#		define PyMODINIT_FUNC extern "C" void
#	else /* __cplusplus */
#		define PyMODINIT_FUNC void
#	endif /* __cplusplus */
#endif

#endif /* PyAPI_DATA */

#if PY_VERSION_HEX < 0x02030000
/* a couple of compatibility definitions */

/* bool is not yet defined, use int */
#define PyBool_FromLong PyInt_FromLong

#define PyDoc_STR(s) s

/* the ticker is still by thread */
#define _Py_Ticker (ts->ticker)

#endif /* pre 2.3 */
