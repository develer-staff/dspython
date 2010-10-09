/* Nintendo DS os module implementation
   Adapted from riscosmodule.c

   WARNING: If you remove cf0_stat from the table, you should observe
            that the file is buffered and tell() will differ from
            FAT_tell().

   Your application should start with:

    Py_Initialize();
	PyRun_SimpleString("import ndsos");

	This will hook in the GBA card device, so that file calls just work.

*/


#include <errno.h>
#include <reent.h>
#include <sys/iosupport.h>
#include <sys/fcntl.h>

#include "Python.h"
#include "methodobject.h"
#include "structseq.h"

/*
#include "../gba_nds_fat/gba_nds_fat.h"
*/

static char cwd[MAXPATHLEN] = "/";

void cf0_init(void);
void initndsos(void);

static PyTypeObject StatResultType;

static PyObject *ndsos_error(char *s) {
	PyErr_SetString(PyExc_OSError, s);
	return NULL;
}

/* Maybe we want to put some more fields in later, so use a struct. */


/*char *getcwd(char *__buf, size_t __size) {
	strncpy(__buf, cwd, __size);
	return __buf;
}*/

/* NDS file commands */

static PyObject *ndsos_remove(PyObject *self,PyObject *args)
{
	return ndsos_error("unimplemented");
#if 0
	char *path1;
	if (!PyArg_Parse(args, "s", &path1)) return NULL;
	if (FAT_remove(path1)) return PyErr_SetFromErrno(PyExc_OSError);
	Py_INCREF(Py_None);
	return Py_None;
#endif
}

/*
static PyObject *ndsos_rename(PyObject *self,PyObject *args)
{	char *path1, *path2;
	if (!PyArg_Parse(args, "(ss)", &path1, &path2)) return NULL;
	if (rename(path1,path2)) return PyErr_SetFromErrno(PyExc_OSError);
	Py_INCREF(Py_None);
	return Py_None;
}
*/

static PyObject *ndsos_chdir(PyObject *self,PyObject *args) {
	return ndsos_error("unimplemented");
#if 0
	char *path;
	char tpath[MAXPATHLEN] = "";

	if (!PyArg_Parse(args, "s", &path)) return NULL;

	if (strlen(path)) {
		if (path[0] == '/')
			strcpy(tpath, path);
		else {
			strcpy(tpath, cwd);
			if (cwd[strlen(cwd)-1] != '/')
				strcpy(tpath + strlen(cwd), "/");
			strcpy(tpath, path);
		}
	} else
		strcpy(tpath, "/");

    if (FAT_chdir(tpath)) {
        strcpy(cwd, tpath);
        return 0;
    } else
		return ndsos_error("Bad path or something");

	Py_INCREF(Py_None);
	return Py_None;
#endif
}

static PyObject *ndsos_getcwd(PyObject *self,PyObject *args)
{
	PyObject *v;
	if(!PyArg_NoArgs(args)) return NULL;
	v=PyString_FromString(cwd);
	if(v==NULL) return NULL;
	return v;
}

/*
static PyObject *ndsos_expand(PyObject *self,PyObject *args)
{	char *path;
	if (!PyArg_Parse(args, "s", &path)) return NULL;
        return canon(path);
}
*/

static PyObject *ndsos_mkdir(PyObject *self,PyObject *args) {
	return ndsos_error("unimplemented");
#if 0
	char *path;
	int mode;
	if (!PyArg_ParseTuple(args, "s|i", &path, &mode)) return NULL;
	if(FAT_mkdir(path) < 0) return ndsos_error("mkdir failed");
	Py_INCREF(Py_None);
	return Py_None;
#endif
}

static PyObject *ndsos_listdir(PyObject *self,PyObject *args) {
	return ndsos_error("unimplemented");
#if 0
	char *path, *buf;
	PyObject *d, *v;
	int c=0;
	if (!PyArg_Parse(args, "s", &path)) return NULL;
	d=PyList_New(0);
	if(!d) return ndsos_error("PyList_New failed");
	if (!FAT_chdir(path)) return ndsos_error("FAT_chdir failed");
	buf = PyMem_MALLOC(256);
	c = FAT_FindFirstFileLFN(buf);
	while (c != 0) {
		v=PyString_FromString(buf);
	    if(!v) { Py_DECREF(d);PyMem_FREE(buf);return ndsos_error("PyString_FromString failed");}
	    if(PyList_Append(d,v)) {Py_DECREF(d);Py_DECREF(v);PyMem_FREE(buf);return ndsos_error("PyList_Append failed");}
		c = FAT_FindNextFileLFN(buf);
	}
	PyMem_FREE(buf);
	return d;
#endif
}

PyDoc_STRVAR(stat_result__doc__,
"stat_result: Result from stat or lstat.\n\n\
This object may be accessed either as a tuple of\n\
  (mode,ino,dev,nlink,uid,gid,size,atime,mtime,ctime)\n\
or via the attributes st_mode, st_ino, st_dev, st_nlink, st_uid, and so on.\n\
\n\
RiscOS: The fields st_ftype, st_attrs, and st_obtype are also available.\n\
\n\
See os.stat for more information.");

static PyStructSequence_Field stat_result_fields[] = {
        { "st_mode",  "protection bits" },
        { "st_ino",   "inode" },
        { "st_dev",   "device" },
        { "st_nlink", "number of hard links" },
        { "st_uid",   "user ID of owner" },
        { "st_gid",   "group ID of owner" },
        { "st_size",  "total size, in bytes" },
        { "st_atime", "time of last access" },
        { "st_mtime", "time of last modification" },
        { "st_ctime", "time of last change" },
	{ "st_ftype", "file type" },
	{ "st_attrs", "attributes" },
	{ "st_obtype", "object type" },
	{ 0 }
};

static PyStructSequence_Desc stat_result_desc = {
	"ndsos.stat_result",
	stat_result__doc__,
	stat_result_fields,
	13
};

static PyObject *ndsos_stat(PyObject *self,PyObject *args) {
	return ndsos_error("unimplemented");
#if 0
	PyObject *v;
	char *path;
    int ret;
	struct stat *st;

	if (!PyArg_Parse(args, "s", &path)) return NULL;

	st = PyMem_MALLOC(sizeof(struct stat));
	ret = cf0_stat(NULL, path, st);

	if (ret < 0) {
		PyMem_FREE(st);
		return ndsos_error("fstat failed");
	}

	v = PyStructSequence_New(&StatResultType);
	PyStructSequence_SET_ITEM(v, 0,
				  PyInt_FromLong((long) st->st_mode)); /*st_mode*/
	PyStructSequence_SET_ITEM(v, 1, PyInt_FromLong((long) 0)); /*st_ino*/
	PyStructSequence_SET_ITEM(v, 2, PyInt_FromLong((long) st->st_dev)); /*st_dev*/
	PyStructSequence_SET_ITEM(v, 3, PyInt_FromLong((long) 0)); /*st_nlink*/
	PyStructSequence_SET_ITEM(v, 4, PyInt_FromLong((long) 0)); /*st_uid*/
	PyStructSequence_SET_ITEM(v, 5, PyInt_FromLong((long) 0)); /*st_gid*/
	PyStructSequence_SET_ITEM(v, 6,
				  PyInt_FromLong((long) st->st_size)); /*st_size*/
	PyStructSequence_SET_ITEM(v, 7, PyInt_FromLong((long) st->st_atime)); /*st_atime*/
	PyStructSequence_SET_ITEM(v, 8, PyInt_FromLong((long) st->st_mtime)); /*st_mtime*/
	PyStructSequence_SET_ITEM(v, 9, PyInt_FromLong((long) st->st_ctime)); /*st_ctime*/
	PyStructSequence_SET_ITEM(v, 10,
				  PyInt_FromLong((long) 0)); /*file type*/
	PyStructSequence_SET_ITEM(v, 11,
				  PyInt_FromLong((long) 0)); /*attributes*/
	PyStructSequence_SET_ITEM(v, 12,
				  PyInt_FromLong((long) 0)); /*object type*/
	PyMem_FREE(st);

    if (PyErr_Occurred()) {
        Py_DECREF(v);
        return NULL;
    }

    return v;
#endif
}

static PyMethodDef ndsos_methods[] = {

	{"unlink",	ndsos_remove},
	{"remove",	ndsos_remove},
	/* {"rename",	ndsos_rename}, */
	{"rmdir",	ndsos_remove},
	{"chdir",	ndsos_chdir},
	{"getcwd",	ndsos_getcwd},
	/* {"expand",  ndsos_expand}, */
	{"mkdir",	ndsos_mkdir, METH_VARARGS},
	{"listdir",	ndsos_listdir},
	{"stat",	ndsos_stat},
	{"lstat",	ndsos_stat},
	{NULL,		NULL}		 /* Sentinel */
};

static int
ins(PyObject *module, char *symbol, long value)
{
	return PyModule_AddIntConstant(module, symbol, value);
}


static int
all_ins(PyObject *d)
{
#ifdef F_OK
        if (ins(d, "F_OK", (long)F_OK)) return -1;
#endif
#ifdef R_OK
        if (ins(d, "R_OK", (long)R_OK)) return -1;
#endif
#ifdef W_OK
        if (ins(d, "W_OK", (long)W_OK)) return -1;
#endif
#ifdef X_OK
        if (ins(d, "X_OK", (long)X_OK)) return -1;
#endif
#ifdef NGROUPS_MAX
        if (ins(d, "NGROUPS_MAX", (long)NGROUPS_MAX)) return -1;
#endif
#ifdef TMP_MAX
        if (ins(d, "TMP_MAX", (long)TMP_MAX)) return -1;
#endif
#ifdef WCONTINUED
        if (ins(d, "WCONTINUED", (long)WCONTINUED)) return -1;
#endif
#ifdef WNOHANG
        if (ins(d, "WNOHANG", (long)WNOHANG)) return -1;
#endif
#ifdef WUNTRACED
        if (ins(d, "WUNTRACED", (long)WUNTRACED)) return -1;
#endif
#ifdef O_RDONLY
        if (ins(d, "O_RDONLY", (long)O_RDONLY)) return -1;
#endif
#ifdef O_WRONLY
        if (ins(d, "O_WRONLY", (long)O_WRONLY)) return -1;
#endif
#ifdef O_RDWR
        if (ins(d, "O_RDWR", (long)O_RDWR)) return -1;
#endif
#ifdef O_NDELAY
        if (ins(d, "O_NDELAY", (long)O_NDELAY)) return -1;
#endif
#ifdef O_NONBLOCK
        if (ins(d, "O_NONBLOCK", (long)O_NONBLOCK)) return -1;
#endif
#ifdef O_APPEND
        if (ins(d, "O_APPEND", (long)O_APPEND)) return -1;
#endif
#ifdef O_DSYNC
        if (ins(d, "O_DSYNC", (long)O_DSYNC)) return -1;
#endif
#ifdef O_RSYNC
        if (ins(d, "O_RSYNC", (long)O_RSYNC)) return -1;
#endif
#ifdef O_SYNC
        if (ins(d, "O_SYNC", (long)O_SYNC)) return -1;
#endif
#ifdef O_NOCTTY
        if (ins(d, "O_NOCTTY", (long)O_NOCTTY)) return -1;
#endif
#ifdef O_CREAT
        if (ins(d, "O_CREAT", (long)O_CREAT)) return -1;
#endif
#ifdef O_EXCL
        if (ins(d, "O_EXCL", (long)O_EXCL)) return -1;
#endif
#ifdef O_TRUNC
        if (ins(d, "O_TRUNC", (long)O_TRUNC)) return -1;
#endif
#ifdef O_BINARY
        if (ins(d, "O_BINARY", (long)O_BINARY)) return -1;
#endif
#ifdef O_TEXT
        if (ins(d, "O_TEXT", (long)O_TEXT)) return -1;
#endif
#ifdef O_LARGEFILE
        if (ins(d, "O_LARGEFILE", (long)O_LARGEFILE)) return -1;
#endif

/* MS Windows */
#ifdef O_NOINHERIT
	/* Don't inherit in child processes. */
        if (ins(d, "O_NOINHERIT", (long)O_NOINHERIT)) return -1;
#endif
#ifdef _O_SHORT_LIVED
	/* Optimize for short life (keep in memory). */
	/* MS forgot to define this one with a non-underscore form too. */
        if (ins(d, "O_SHORT_LIVED", (long)_O_SHORT_LIVED)) return -1;
#endif
#ifdef O_TEMPORARY
	/* Automatically delete when last handle is closed. */
        if (ins(d, "O_TEMPORARY", (long)O_TEMPORARY)) return -1;
#endif
#ifdef O_RANDOM
	/* Optimize for random access. */
        if (ins(d, "O_RANDOM", (long)O_RANDOM)) return -1;
#endif
#ifdef O_SEQUENTIAL
	/* Optimize for sequential access. */
        if (ins(d, "O_SEQUENTIAL", (long)O_SEQUENTIAL)) return -1;
#endif

/* GNU extensions. */
#ifdef O_DIRECT
        /* Direct disk access. */
        if (ins(d, "O_DIRECT", (long)O_DIRECT)) return -1;
#endif
#ifdef O_DIRECTORY
        /* Must be a directory.	 */
        if (ins(d, "O_DIRECTORY", (long)O_DIRECTORY)) return -1;
#endif
#ifdef O_NOFOLLOW
        /* Do not follow links.	 */
        if (ins(d, "O_NOFOLLOW", (long)O_NOFOLLOW)) return -1;
#endif

	/* These come from sysexits.h */
#ifdef EX_OK
	if (ins(d, "EX_OK", (long)EX_OK)) return -1;
#endif /* EX_OK */
#ifdef EX_USAGE
	if (ins(d, "EX_USAGE", (long)EX_USAGE)) return -1;
#endif /* EX_USAGE */
#ifdef EX_DATAERR
	if (ins(d, "EX_DATAERR", (long)EX_DATAERR)) return -1;
#endif /* EX_DATAERR */
#ifdef EX_NOINPUT
	if (ins(d, "EX_NOINPUT", (long)EX_NOINPUT)) return -1;
#endif /* EX_NOINPUT */
#ifdef EX_NOUSER
	if (ins(d, "EX_NOUSER", (long)EX_NOUSER)) return -1;
#endif /* EX_NOUSER */
#ifdef EX_NOHOST
	if (ins(d, "EX_NOHOST", (long)EX_NOHOST)) return -1;
#endif /* EX_NOHOST */
#ifdef EX_UNAVAILABLE
	if (ins(d, "EX_UNAVAILABLE", (long)EX_UNAVAILABLE)) return -1;
#endif /* EX_UNAVAILABLE */
#ifdef EX_SOFTWARE
	if (ins(d, "EX_SOFTWARE", (long)EX_SOFTWARE)) return -1;
#endif /* EX_SOFTWARE */
#ifdef EX_OSERR
	if (ins(d, "EX_OSERR", (long)EX_OSERR)) return -1;
#endif /* EX_OSERR */
#ifdef EX_OSFILE
	if (ins(d, "EX_OSFILE", (long)EX_OSFILE)) return -1;
#endif /* EX_OSFILE */
#ifdef EX_CANTCREAT
	if (ins(d, "EX_CANTCREAT", (long)EX_CANTCREAT)) return -1;
#endif /* EX_CANTCREAT */
#ifdef EX_IOERR
	if (ins(d, "EX_IOERR", (long)EX_IOERR)) return -1;
#endif /* EX_IOERR */
#ifdef EX_TEMPFAIL
	if (ins(d, "EX_TEMPFAIL", (long)EX_TEMPFAIL)) return -1;
#endif /* EX_TEMPFAIL */
#ifdef EX_PROTOCOL
	if (ins(d, "EX_PROTOCOL", (long)EX_PROTOCOL)) return -1;
#endif /* EX_PROTOCOL */
#ifdef EX_NOPERM
	if (ins(d, "EX_NOPERM", (long)EX_NOPERM)) return -1;
#endif /* EX_NOPERM */
#ifdef EX_CONFIG
	if (ins(d, "EX_CONFIG", (long)EX_CONFIG)) return -1;
#endif /* EX_CONFIG */
#ifdef EX_NOTFOUND
	if (ins(d, "EX_NOTFOUND", (long)EX_NOTFOUND)) return -1;
#endif /* EX_NOTFOUND */

        return 0;
}

void
initndsos()
{
	PyObject *m, *d;

	m = Py_InitModule("ndsos", ndsos_methods);

	if (all_ins(m))
		return;

	d = PyModule_GetDict(m);

	Py_INCREF(PyExc_OSError);
	PyModule_AddObject(m, "error", PyExc_OSError);

	PyStructSequence_InitType(&StatResultType, &stat_result_desc);
	PyDict_SetItemString(d, "stat_result", (PyObject*) &StatResultType);
}
