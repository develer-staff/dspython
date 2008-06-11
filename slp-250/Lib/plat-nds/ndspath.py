# Token path module.

import ndsos
import stat

curdir = "."
pardir = ".."
sep = "/"
pathsep = ":"
defpath = "NOT-DEFINED"
extsep = "."
altsep = None
devnull = None

def split(path):
    idx = path.rfind(sep)
    if idx == -1:
        return path, ""
    return path[:idx], path[idx+len(sep):]

def exists(path):
    try:
        ndsos.stat(path)
    except OSError:
        return False
    return True

def join(*args):
    s1 = ""
    notFirst = False
    for s2 in args:
        if notFirst and not s2.startswith(sep):
            s2 = sep + s2
        if s2.endswith(sep):
            s2 = s2[:-len(sep)]
        s1 += s2
        notFirst = True
    return s1

def normpath(path):
    l = []
    while len(path):
        prefix, path = split(path)
        if prefix == "" or prefix == ".":
            continue
        if prefix == "..":
            l = l[:-1]
        else:
            l.append(prefix)
    return join(*l)

def abspath(path):
    return normpath(join(ndsos.getcwd(), path))

def normcase(path):
    return path

def dirname(path):
    return split(path)[0]

def isfile(path):
    return exists(path) and stat.S_ISREG(ndsos.stat(path)[0])

def isdir(path):
    return exists(path) and stat.S_ISDIR(ndsos.stat(path)[0])

def islink(path):
    return False
