# Created by ? (Christian?)
# Updated for changes to the Stackless atomicity by N. J. Harman.

from stackless import *

debug = 1

class mutex:
    def __init__(self, capacity=1):
        self.queue = channel()
        self.capacity = capacity

    def isLocked(self):
        '''return non-zero if locked'''
        return self.capacity == 0

    def lock(self):
        '''acquire the lock'''
        currentTasklet = stackless.getcurrent()
        atomic = currentTasklet.set_atomic(True)
        try:
            if self.capacity:
                self.capacity -= 1
            else:
                self.queue.receive()
        finally:
            currentTasklet.set_atomic(atomic)

    def unlock(self):
        '''release the lock'''
        currentTasklet = stackless.getcurrent()
        atomic = currentTasklet.set_atomic(True)
        try:
            if self.queue.balance < 0:
                self.queue.send(None)
            else:
                self.capacity += 1
        finally:
            currentTasklet.set_atomic(atomic)

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

m = mutex()

def f():
    name = getcurrent().name
    print name, "acquiring"
    m.lock()
    print name, "switching"
    schedule()
    print name, "releasing"
    m.unlock()

MyTasklet(f, "tick")()
MyTasklet(f, "trick")()
MyTasklet(f, "track")()

def channel_cb(channel, tasklet, sending, willblock):
    print tasklet, ("recv", "send")[sending], ("nonblocking", "blocking")[willblock]

def schedule_cb(prev, next):
    if not prev:
        print "starting", next
    elif not next:
        print "ending", prev
    else:
        print "jumping from %s to %s" % (prev, next)

if __name__ == "__main__":
    if debug:
        set_channel_callback(channel_cb)
        set_schedule_callback(schedule_cb)

    run()

    set_channel_callback(None)
    set_schedule_callback(None)
