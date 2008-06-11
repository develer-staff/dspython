from stackless import *

enable_softswitch(1)
pr = 01
debug = 1

def schedule_cb(prev, next):
    print
    if not prev:
        print "starting", next
    elif not next:
        print "ending", prev
    else:
        print "suspending", prev
        print "resuming", next

if debug:
    set_schedule_callback(schedule_cb)

def f(x):
    if pr: print x, x, x
    if x:
        name = "Nr %d" % (x-1)
        t = MyTasklet(f, name)(x-1)
        if pr: print "starting", x-1
        t.run()
        schedule()
        del t
        if pr: print "back in", x
        1<<42
        if x == 2:
            pass#1/0

class MyTasklet(tasklet):
    __slots__ = ["name"]

    def __init__(self, func, name=None):
        tasklet.__init__(self, func)
        if not name:
            name = "at %08x" % (id(self))
        self.name = name
    def __new__(self, func, name=None):
        return tasklet.__new__(self, func)
    def __repr__(self):
        return "Tasklet %s" % self.name

num = 1
t = MyTasklet(f, "Nr %d" % num)(num)
print "Now"
t.run()
run()
schedule()
if pr: print "back"
print "main done."

set_schedule_callback(None)
import gc;gc.collect()
