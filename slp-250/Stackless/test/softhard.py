from stackless import *

"""
Perform soft switching to A and B, then do a hard switch B to C.
Switch back from C to B, which still has a cstack attached.
Switch from B to A, and B's cframe should disappear.
"""

class MyTasklet(tasklet):
    __slots__ = ["name"]

    def __init__(self, func, name=None):
        tasklet.__init__(self, func)
        if not name:
            name = "at " + hex(id(self))
        self.name = name
    def __new__(self, func, name):
        return tasklet.__new__(self, func)
    def __repr__(self):
        return "Tasklet %s" % self.name

def get_css(t):
    return t.cstate and len(str(t.cstate))//4 or 0

def schedule_cb(prev, next):
    print
    if not prev:
        print "starting  ", next, get_css(next)
    elif not next:
        print "ending    ", prev, get_css(prev)
    else:
        print "suspending", prev, get_css(prev)
        print "resuming  ", next, get_css(next)

set_schedule_callback(schedule_cb)

def f1():
    schedule()

def f2():
    schedule()
    schedule()

A = MyTasklet(f1, "A")()
B = MyTasklet(f2, "B")()
C = MyTasklet(test_cframe, "C")(1)
print "first schedule():"
schedule()
B.remove().insert()
A.remove().insert()
print "reordered, now running"
run()

set_schedule_callback(None)
print "cleaning up:"
run()
import gc;gc.collect()
