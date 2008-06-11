#define TASKLET_INSERT_HEAD(func) \
	int func (PyTaskletObject *task)

#define TASKLET_RUN_HEAD(func) \
	PyObject *func (PyTaskletObject *task)

#define TASKLET_REMOVE_HEAD(func) \
	int func (PyTaskletObject *task)

#define TASKLET_SETATOMIC_HEAD(func) \
	int func (PyTaskletObject *task, int flag)

#define TASKLET_SETIGNORENESTING_HEAD(func) \
	int func (PyTaskletObject *task, int flag)

#define TASKLET_BECOME_HEAD(func) \
	PyObject *func (PyTaskletObject *task, PyObject *retval)

#define TASKLET_CAPTURE_HEAD(func) \
	PyObject *func (PyTaskletObject *task, PyObject *retval)

#define TASKLET_CALL_HEAD(func) \
	int func (PyTaskletObject *task, PyObject *args, PyObject *kwds)

#define TASKLET_RAISE_EXCEPTION_HEAD(func) \
    PyObject *func (PyTaskletObject *self, PyObject *klass, PyObject *args)

#define TASKLET_KILL_HEAD(func) \
    PyObject *func (PyTaskletObject *task)


typedef struct _pytasklet_heaptype {
	PyFlexTypeObject type;
	/* the fast callbacks */
	TASKLET_INSERT_HEAD(		(*insert)            );
	TASKLET_RUN_HEAD(		(*run)               );
	TASKLET_REMOVE_HEAD(		(*remove)            );
	TASKLET_SETATOMIC_HEAD(		(*set_atomic)        );
	TASKLET_SETIGNORENESTING_HEAD(	(*set_ignore_nesting));
	TASKLET_BECOME_HEAD(		(*become)            );
	TASKLET_CAPTURE_HEAD(		(*capture)           );
	TASKLET_RAISE_EXCEPTION_HEAD(	(*raise_exception)   );
	TASKLET_KILL_HEAD(		(*kill)              );
} PyTasklet_HeapType;

int init_tasklettype(void);
