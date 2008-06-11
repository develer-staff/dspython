# Testing compressibility of cstacks
# Christian Tismer
# 2002-05-21

import stackless, struct, operator, sys

try:
	import ccall_map
except ImportError:
	sys.path.insert(0, "")
	try:
		import ccall_map
	except ImportError:
		# platform not supported?
		pass

g = sys.getrefcount

def get_stack(t):
	st = t.frame.cstack
	stack = struct.unpack("%di" % st.size, str(st))
	return stack

def get_stacks(c):
	res = []
	task = c.queue
	for i in range(abs(c.balance)):
		res.append(get_stack(task))
		task = task.next
	return res

def compress_stacks(stacks):
	ref = stacks[-1]
	res = [ref]
	for stack in stacks[:-1]:
		compressed = []
		for i in range(len(stack)):
			word = stack[i]
			if word != ref[i]:
				compressed.extend( [i, word] )
		res.append(compressed)
	return res

def stacks_len(stacks):
	return reduce(operator.add, map(len, stacks))

# checking main task
ch = stackless.channel()
def maintest():
	ch.receive()
	global look, stackref, tstate
	t = stackless.getmain()
	look = get_stack(t)
	stackref = t.frame.cstack.startaddr
	try:
		tstate = stackless._peek(t.frame)
	except AttributeError:
		tstate = None

def view_main():
	g = id(globals())
	baseadr = stackless._peek(None) - ccall_map.peek_ofs
	tstate = stackless._peek(sys._getframe())
	stackend = stackref-4*len(look)
	context = ''
	callee = ''
	codetype = type(sys._getframe().f_code)
	for i in range(len(look)-1,-1,-1):
		data = look[i]
		call = ccall_map.CallMap.get(data-baseadr)
		if call:
			(funcname, modname, srcname, lineno, lng, callee) = call
			if lng:
				# a function call
				s = "*%s line %d call %s +%d   file %s" % (funcname, lineno, callee, lng, srcname)
				s += "\n"+ 60*"-"
			else:
				s = "%s line %d entry   file %s" % (funcname, lineno, srcname)
		elif data == g:
			s = "--globals--"
		elif data == tstate:
			s = "--tstate--"
		elif data < stackref and data >= stackend:
			#print "stackref %d data %d" % (stackref, data)
			sp = (data-stackend)/4
			s = "-->STACK[%d]" % sp
		else:
			x = stackless._peek(data)
			if x is data:
				if x > 256:
					s = "0x%08x" % x
				else:
					s = repr(x)
			else:
				s = repr(x)[:299]
				if s[0] <> "<":
					# add type info
					tname = str(type(x)).split("'")[1]
					s = "%s %s" % (tname, repr(x)[:200])
		print "%-18s [%3d] %s" % (context, i, s)
		if callee:
			context = callee

stackless.tasklet(maintest)().run()
ch.send(1)

def simplefunc(chan):
	chan.receive()
	print "back from simplefunc"

def complexfunc(chan):
	simplefunc(chan)

class worse:
	def __init__(self, arg):
		self.data = arg
	def __add__(self, other):
		simplefunc(self.data)
		return 42

def harderfunc(chan):
	stuff = worse(chan)
	stuff + 5

def simpletest(func, n):
	c = stackless.channel()
	gen = stackless.tasklet(func)
	for i in range(n):
		gen(c).run()
	return c

# simple test
def test(func):
	global look, stackref, tstate, t
	c = simpletest(func, 1)
	t = c.queue
	look = get_stack(t)
	stackref = t.frame.cstack.startaddr
	tstate = stackless._peek(t.frame)
	view_main()
	c.send(0)

def stubtest():
	global look, stackref, tstate, t
	t = stackless.taskoutlet(lambda:None)()
	look = get_stack(t)
	stackref = t.frame.cstack.startaddr
	tstate = stackless._peek(t.frame)
	view_main()

#test(complexfunc)
#test(simplefunc)
#test(harderfunc)
#stubtest()

dump = """
                   [ 63] *_PyEval_EvalCodeEx line 2613 call _slp_eval_frame +5   file ..\Python\ceval.c
------------------------------------------------------------
_slp_eval_frame    [ 62] 0x00c60930
_slp_eval_frame    [ 61] <code object OnCommand at 00CA4920, file "D:\Python22\Pythonwin\pywin\framework\intpyapp.py", line 68>
_slp_eval_frame    [ 60] <frame object at 0x00E0FA30>
_slp_eval_frame    [ 59] *_slp_eval_frame line 627 call _eval_frame +5   file ..\Stackless\stacklesseval.h
------------------------------------------------------------
_eval_frame        [ 58] 0		flags
_eval_frame        [ 57] --tstate--	exc
_eval_frame        [ 56] -->STACK[48]	tb
_eval_frame        [ 55] 0		nk
_eval_frame        [ 54] 0x00e0fb88	freevars
_eval_frame        [ 53] 0		n, callargs
_eval_frame        [ 52] <code object 	co	simplefunc at 01285880, file "D:\Stackless\src\2.2\stackless\src\PCbuild\cstack.py", line 106>
_eval_frame        [ 51] --tstate--	val
_eval_frame        [ 50] 131		opcode
_eval_frame        [ 49] --tstate--	tstate
_eval_frame        [ 48] 0		retval
_eval_frame        [ 47] 0		stream
_eval_frame        [ 46] 0x01286304	first_instr
_eval_frame        [ 45] 0x01286313	next_instr
_eval_frame        [ 44] 0		why
_eval_frame        [ 43] 0		err
_eval_frame        [ 42] 0		oparg
_eval_frame        [ 41] 0x00e0fb8c	stack_pointer
_eval_frame        [ 40] <frame object 	ebx		at 0x00C607D0>
_eval_frame        [ 39] 0		ebp
_eval_frame        [ 38] 0		esi
_eval_frame        [ 37] --tstate--	edi
_eval_frame        [ 36] 0		param na
_eval_frame        [ 35] -->STACK[41]	param &stack_pointer
_eval_frame        [ 34] <built-in 	param func		method receive of channel object at 0x01282DF0>
_eval_frame        [ 33] *_eval_frame line 2035 call _fast_cfunction +5   file ..\Python\ceval.c
------------------------------------------------------------
_fast_cfunction    [ 32] 0x00e0fb88
_fast_cfunction    [ 31] str 'receive'
_fast_cfunction    [ 30] 0
_fast_cfunction    [ 29] 0
_fast_cfunction    [ 28] <channel object at 0x01282DF0>
_fast_cfunction    [ 27] *_fast_cfunction line 3154 call edi +2   file ..\Python\ceval.c
------------------------------------------------------------
edi                [ 26] <channel object at 0x01282DF0>
edi                [ 25] <built-in method receive of channel object at 0x01282DF0>
edi                [ 24] str 'receive'
edi                [ 23] _channel_receive line 336 entry   file ..\Stackless\stacklessmodule.c
edi                [ 22] 0x00cb6fb8
edi                [ 21] <tasklet object at 0x0135E9F8>
edi                [ 20] 0x01282e00
edi                [ 19] 0x0124f500
edi                [ 18] <tasklet object at 0x0135E9F8>
edi                [ 17] *_channel_receive line 365 call _slp_schedule_task +5   file ..\Stackless\stacklessmodule.c
------------------------------------------------------------
_slp_schedule_task [ 16] <traceback 	savets.exc_traceback	object at 0x01252478>
_slp_schedule_task [ 15] str 'There is 	savets.exc_value	no active view.'
_slp_schedule_task [ 14] str 'win32ui'	savets.exc_type
_slp_schedule_task [ 13] 1		savets.recursion_depth
_slp_schedule_task [ 12] <frame object 	savets.frame		at 0x00E0FA30>
_slp_schedule_task [ 11] <channel 	esi			object at 0x01282DF0>
_slp_schedule_task [ 10] --tstate--	edi
_slp_schedule_task [  9] 0x00cb6fb8
_slp_schedule_task [  8] -->STACK[0]
_slp_schedule_task [  7] 0x0128ad40
_slp_schedule_task [  6] --tstate--
_slp_schedule_task [  5] *_slp_schedule_task line 383 call _slp_transfer +5   file ..\Stackless\stacklesseval.h
------------------------------------------------------------
_slp_transfer      [  4] <tasklet object at 0x0135E9F8>
_slp_transfer      [  3] --tstate--
_slp_transfer      [  2] <tasklet object at 0x0135E9F8>
_slp_transfer      [  1] --tstate--
_slp_transfer      [  0] 0x0124f500
"""