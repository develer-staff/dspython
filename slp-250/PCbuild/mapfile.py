###############################################
## MAP file reader
## Christian Tismer
## 2002-06-23 to 25
##
## Purpose:
## first steps towards thread pickling and
## stack compression. We'd like to get some
## insight into cstack objects.

"""
This module tries to gather information about
the stack layout of the Python interpreter.

From the mapfile, names and addresses of
public and private functions are collected.
Additionally, linenumber info is extracted.
The advantage is that line numbers are provided
even for include files which produced code.
The drawback of this approach is, that we get
addresses of line numbers, but what we really
need are the expected return addresses on the stack.

This information can be found by parsing the .cod
files from the assembly. Unfortunately, these files
give us line numbers as comments, but don't tell us
the names of the source files. We can find every
line which contains a call and compute the resulting
return address.
By comparing this address with the addresses from the
.map file's line info, we can also deduce the correct
source file name.
"""

import os, re, stackless, bisect, time

if stackless.debug:
    CODEDIR = "x86-temp-debug\\pythoncore"
    MAPFILE = CODEDIR + "\\python23_d.map"
else:
    CODEDIR = "x86-temp-release\\pythoncore"
    MAPFILE = "python23.map"

# find the code class
# determine state
# generate objects

def makepairs(lis):
    if len(lis) % 2:
        raise ValueError, "odd number of elements:" + repr(lis)
    return [ (lis[i], lis[i+1]) for i in range(0, len(lis), 2) ]

class MapFileReader:
    
    def __init__(self, fname):
        self.fname = fname
        self.stage = None
        self.objectfiles = {}
        self.functions = {}
        self.funcadr = {}
        self.alladr = {}
        self.alladrlis = []
        self.callmap = {}
        
    # we look at the first three words of a header line:
    # these stages appear in order.
    # stage 4 is repeated for all source files.
    stage1 = "Start Length Name".split()
    stage2 = "Address Publics by".split()
    stage3 = "Static symbols".split()
    stage4 = "Line numbers for".split()

    def handle_stage1(self, header, lines):
        # stage 1: just look for the code segment.
        # probably always 0001.
        for line in lines:
            if len(line)==4:
                start, length, name, klass = line
                if klass == "CODE":
                    seg, ofs = start.split(":")
                    self.codeseg = seg # keep as string
                    self.codeofs = int(ofs, 16)
                    if length[-1] == "H":
                        length = length[:-1]
                    self.codelen = int(length, 16)
                    self.codename = name
                    break
    
    def handle_stage2(self, header, lines, public=True):
        # stage 2:
        # find all entries of the form
        # 0001:00000e50       _init_codecs               1e001e50 f   _codecsmodule.obj
        codeseg = self.codeseg
        obfiles = self.objectfiles
        funcs = self.functions
        fadr = self.funcadr
        for line in lines:
            if len(line)==5:
                adr, name, absadr, f, obj = line
                seg, ofs = adr.split(":")
                if seg == codeseg and f=="f":
                    ofs = int(ofs, 16)
                    objfile = obfiles.get(obj, None)
                    if not objfile:
                        objfile = Objectfile(obj)
                        obfiles[obj] = objfile
                    func = Function(name, ofs, public, objfile)
                    if public:
                        funcs[name] = func
                    else:
                        # make private names unique
                        mangled = "%s/%s" % (name, objfile.modname)
                        funcs[mangled] = func
                    fadr[ofs] = func
    
    def handle_stage3(self, header, lines):
        # same as stage 2, but not public
        self.handle_stage2(header, lines, False)
    
    def handle_stage4(self, header, lines):
        # the header is of the form
        # Line numbers for .\x86-temp-release\pythoncore\_hotshot.obj(D:\Stackless\src\2.2\stackless\src\Modules\_hotshot.c) segment .text
        info = header[3]
        path, rest = info.split("(")
        src, rest = rest.split(")")
        # prune src path
        pieces = src.split("\\src\\")
        if len(pieces) > 1:
            src = "..\\"+pieces[-1]
        objname =os.path.basename(path)
        obj = self.objectfiles[objname]
        srcfile = Sourcefile(src)
        obj.sources.append(srcfile)
        srcfile.objfiles.append(obj)
        # now process line entries of the form
        #     96 0001:0001b2a0    98 0001:0001b2c3    99 0001:0001b2e1   100 0001:0001b2ff
        mp = makepairs
        fadr = self.funcadr
        func = None
        for line in lines:
            for lineno, adr in mp(line):
                lineno = int(lineno)
                seg, ofs = adr.split(":")
                # assuming seg is codeseg without check
                ofs = int(ofs, 16)
                func = fadr.get(ofs, func)
                lineobj = LineNumber(lineno, ofs, srcfile, func)
                self.alladr[ofs] = lineobj
    
    nextstage = {
        None         : (stage1, None),
        tuple(stage1): (stage2, handle_stage1),
        tuple(stage2): (stage3, handle_stage2),
        tuple(stage3): (stage4, handle_stage3),
        tuple(stage4): (stage4, handle_stage4),
        }

    def do_parse(self):
        expect_next, handler = self.nextstage[self.stage]
        start = 0
        lines = [line.split() for line in file(self.fname).readlines()]
        for i in range(len(lines)):
            line = lines[i]
            if line[:3] == expect_next:
                if handler:
                    header = lines[start]
                    data = lines[start+1:i-1]
                    handler(self, header, data)
                start = i
                self.stage = tuple(expect_next)
                expect_next, handler = self.nextstage[self.stage]
        # process last one
        if handler:
            header = lines[start]
            data = lines[start+1:]
            handler(self, header, data)
        # now build alladrlis for bisection search
        lines = self.alladr.items()
        lines.sort()
        self.alladrlis = [ value for key, value in lines]

    def get_loadadr(self):
        # after the initial analysis, we have the
        # offset of stackless._peek (hopefully),
        # and we get its absolute address by calling it with None.
        peek_ofs = self.functions["__peek/stacklessmodule"].ofs
        peek_adr = stackless._peek(None)
        self.peek_ofs = peek_ofs
        self.loadadr = peek_adr - peek_ofs

    def nearest_line(self, ofs):
        idx = bisect.bisect_left(self.alladrlis, ofs)
        line = self.alladrlis[idx]
        if line.ofs >= ofs:
            line = self.alladrlis[idx-1]
        return line

    def parse_code(self, verbose=True, single=False):
        # parse all code files.
        # find all calls and build our call map.
        for fname in os.listdir(CODEDIR):
            if os.path.splitext(fname)[-1] == ".cod":
                modname = os.path.basename(os.path.splitext(fname)[0])
                fname = os.path.join(CODEDIR, fname)
                cp=CodeParser(fname)
                if verbose: print fname
                cp.parse()
                for (ofs, lng, lineno, funcname, callee) in cp.calls:
                    # find the function by name
                    mangled = "%s/%s" % (funcname, modname)
                    func = self.functions.get(mangled)
                    if not func:
                        # it is a public
                        func = self.functions[funcname]
                    fadr = func.ofs
                    # find the line number by address
                    lineadr = fadr + ofs
                    lineobj = self.nearest_line(lineadr)
                    # now we have the source file.
                    srcname = lineobj.srcfile.name
                    if verbose>1: print "f=%s line=%d, nearest=%d callee=%s" % (
                        funcname, lineno, lineobj.lineno, callee)
                    entry = (funcname, modname, srcname, lineno, lng, callee)
                    self.callmap[lineadr+lng] = entry
            if single:
                break
        self.get_loadadr()

    def make_map(self, fname="ccall_map.py"):
        calls = self.callmap.items()
        calls.sort()
        f = open(fname, "w")
        print>>f, "# generated at %s" % time.ctime(time.time())
        print>>f
        print>>f, "peek_ofs = 0x%05x # relocation" % self.peek_ofs
        print>>f
        print>>f, "# Call map"
        print>>f, "CallMap = {"
        for ofs, (funcname, modname, srcname, lineno, lng, callee) in calls:
            tup = ofs, funcname, modname, srcname, lineno, lng, callee
            fmt = "  0x%05x: ('%s', '%s', r'%s', %d, %d, '%s'),"
            print>>f, fmt % tup
        print>>f, "}"

class Objectfile:
    def __init__(self, name):
        self.name = name
        self.sources = []
        self.modname = os.path.basename(os.path.splitext(name)[0])
    def __repr__(self):
        return "<object file %s>" % self.name
    def __str__(self):
        return self.name

class Sourcefile:
    def __init__(self, name):
        self.name = name
        self.objfiles = []
    def __repr__(self):
        return "<source file %s>" % self.name
    def __str__(self):
        return self.name
        
class Function:
    def __init__(self, name, ofs, public, objfile):
        self.name = name
        self.ofs = ofs
        self.public = public
        self.objfile = objfile
    def __repr__(self):
        return "<function %s at %08x (%s)>" % (
            self.name, self.ofs, ["private", "public"][self.public])
    def __hash__(self):
        return self.ofs

class LineNumber(object):
    __slots__ = "lineno ofs srcfile func".split()
    def __init__(self, lineno, ofs, srcfile, func):
        self.lineno = lineno
        self.ofs = ofs
        self.srcfile = srcfile
        self.func = func
    def __repr__(self):
        if self.func:
            funcname = self.func.name
            funcofs = self.func.ofs
        else:
            funcname = "(unknown)"
            funcofs = -1
        return "<line %4d of %s at %08x f=%s%s>" % (
            self.lineno, self.srcfile, self.ofs, funcname,
            ["", " (entry)"][self.ofs==funcofs])
    def __hash__(self):
        return self.ofs
    def __cmp__(self, other):
        if type(other) is int:
            return cmp(self.ofs, other)
        return cmp(self.ofs, other.ofs)

_nohex_cache = {}

def split_hex_nohex(lis,
                    _nohex_cache=_nohex_cache,
                    len=len,
                    allowed=(2, 5)):
    """find the first string that is not a valid hex value"""
    i = 0
    try:
        for item in lis:
            if _nohex_cache[item]: return i
            i += 1
        return i
    except:
        if len(item) in allowed:
            try:
                int(item, 16)
                _nohex_cache[item] = False
                return split_hex_nohex(lis)
            except:
                _nohex_cache[item] = True
                return i
        else:
            _nohex_cache[item] = True
        return i


class CodeParser:
    def __init__(self, fname):
        self.fname = fname
        self.calls = []

    def parse(self):
        split_h_nh = split_hex_nohex
        longline = None
        for line in file(self.fname).readlines():
            stuff = line.split()
            if len(stuff) >= 2:
                if stuff[0] == ";":
                    if len(stuff) >=3 and stuff[2] == ":" :
                        lineno = int(stuff[1])
                    continue
                if stuff[1] == "PROC":
                    funcname = stuff[0]
                    continue
                nhex = split_h_nh(stuff)
                if nhex == len(stuff):
                    # long code line, concatenate
                    longline = stuff
                    continue
                if longline:
                    stuff = longline + stuff
                    nhex += len(longline)
                    longline = None
                hexpart = stuff[:nhex]
                if not hexpart:
                    continue
                asmpart = stuff[nhex:]
                if not asmpart:
                    continue
                if asmpart[0] == "call":
                    ofs = int(hexpart[0], 16)
                    lng = len(hexpart)-1
                    callee = " ".join(asmpart[1:])
                    self.calls.append( (ofs, lng, lineno, funcname, callee) )
                    continue
                if hexpart[0] == "00000":
                    # function entry
                    self.calls.append( (0, 0, lineno, funcname, "") )
                    continue

if __name__ == "__main__":
    mfr = MapFileReader(MAPFILE)
    mfr.do_parse()
    mfr.get_loadadr()
    mfr.parse_code()
    mfr.make_map()