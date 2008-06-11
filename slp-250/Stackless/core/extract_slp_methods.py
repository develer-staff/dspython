################################################################
#
# extract_slp_methods.py
#
# scan all C sources for the STACKLESS_DECLARE_METHOD macro
# and create and include file for the module.
#
################################################################

import os

srcname = "../.."
dstname = "stackless_methods.h"

def cfiles(rootpath):
    work = [rootpath]
    while work:
        path = work.pop(0)
        for name in os.listdir(path):
            fname = os.path.join(path, name)
            if os.path.isdir(fname):
                work.append(fname)
            elif os.path.splitext(fname)[-1] == ".c":
                yield fname
        

def parse(fname):
    find = "STACKLESS_DECLARE_METHOD"
    txt = file(fname).read()
    if txt.find(find) < 0:
        return

    lines = txt.split("\n")
    res = [line for line in lines if line.startswith(find)]
    return res

def generate():
    f = file(dstname, "w")
    print >> f, """\
/*
 * this file was generated from the Python C sources using the script
 * Stackless/core/extract_slp_methods.py .
 * please don't edit this output, but work on the script.
 */

typedef struct {
    void *type;
    size_t offset;
} _stackless_method;

#define MFLAG_IND 0x8000
#define MFLAG_OFS(meth) offsetof(PyTypeObject, slpflags.meth)
#define MFLAG_OFS_IND(meth) MFLAG_OFS(meth) + MFLAG_IND

static _stackless_method _stackless_methtable[] = {\
"""
    for fname in cfiles(srcname):
        found = parse(fname);
        if not found:
            continue
        name = os.path.split(fname)[-1]
        print >> f, "\t/* from %s */" % name
        for line in found:
            typ, meth = line.split("(")[-1].split(")")[0].split(", ")
            tabs = "\t"
            lng = len(typ) + 2
            while lng < 24:
                tabs += "\t"
                lng += 8
            ind = ""
            if not typ.startswith("&"):
                # indirection flag
                ind = "_IND"
                typ = "&" + typ
            print >> f, "\t{%s,%sMFLAG_OFS%s(%s)}," % \
                  (typ, tabs, ind, meth)
    print >> f, "\t{0, 0} /* sentinel */"
    print >> f, "};"

if __name__ == "__main__":
    generate()
