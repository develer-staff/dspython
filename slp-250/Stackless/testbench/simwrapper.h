#ifndef Py_SIMWRAPPER_H
#define Py_SIMWRAPPER_H

#include "Python.h"

#ifndef SIM_WRAPPER_EXPORTS
#define SIM_WRAPPER_EXPORTS __declspec(dllexport)
#endif

#ifndef SIM_WRAPPER_IMPORTS
#define SIM_WRAPPER_IMPORTS __declspec(dllimport)
#endif


#ifdef __cplusplus
extern "C" {
#endif

extern DL_EXPORT(int) PySW_InitWrapper();
extern DL_EXPORT(void) PySW_SetPath(char *path);
extern DL_EXPORT(PyObject*) PySW_CreateTasklet( PyObject *func );
extern DL_EXPORT(int) PySW_IsTaskletRunning( PyObject* tasklet );
extern DL_EXPORT(int) PySW_DeleteTasklet(PyObject* tasklet);
extern DL_EXPORT(int) PySW_ResetTasklet(PyObject* tasklet);
extern DL_EXPORT(int) PySW_RunTasklet(PyObject* tasklet);
extern DL_EXPORT(int) PySW_SuspendTasklet();
extern DL_EXPORT(int) PySW_ContinueTasklet( PyObject* tasklet );
extern DL_EXPORT(int) PySW_CleanupTasklet( PyObject* tasklet );


#ifdef __cplusplus
}
#endif

#endif /* !Py_SIMWRAPPER_H */
