from stackless import *
import stackless

i = 0
def unbounded():
    global i
    i = 0
    try:
        while True:
            i += 1
            print i
    except Exception, e:
        print repr(e), str(e)
    print "actually exit"

def unbounded_notrap():
    global i
    i = 0
    while True:
        i += 1
        print i

class ObjGetter(object):
    def __init__(self, obj):
        self.obj = obj
    def __getitem__(self, item):
        if not item:
            return self.obj
        return getattr(self.obj, item)

def desc_tasklet(t):
    print ("""
Tasklet:             %()r
    alive:           %(alive)r
    paused:          %(paused)r
    scheduled:       %(scheduled)r
    recursion_depth: %(recursion_depth)r
    nesting_level:   %(nesting_level)r
    next:            %(next)r
    prev:            %(prev)r
""" % ObjGetter(t))

def test(fn):
    global i
    print fn.__name__
    print '-- creating tasklet'
    t = tasklet(fn)()
    desc_tasklet(t)
    print '-- runloop'
    stackless.run(13)
    print "-- end inside"
    desc_tasklet(t)
    before = i
    print "-- before GC"
    del t
    print "-- after GC"
    assert(i == before)

test(unbounded)
test(unbounded_notrap)
