#define CHANNEL_SEND_HEAD(func) \
	PyObject * func (PyChannelObject *self, PyObject *arg)

#define CHANNEL_SEND_EXCEPTION_HEAD(func) \
	PyObject * func (PyChannelObject *self, PyObject *klass, PyObject *args)

#define CHANNEL_RECEIVE_HEAD(func) \
	PyObject * func (PyChannelObject *self)


typedef struct _pychannel_heaptype {
	PyFlexTypeObject type;
	/* the fast callbacks */
	CHANNEL_SEND_HEAD(           (*send)             );
	CHANNEL_SEND_EXCEPTION_HEAD( (*send_exception)   );
	CHANNEL_RECEIVE_HEAD(	     (*receive)          );
} PyChannel_HeapType;

int init_channeltype(void);
