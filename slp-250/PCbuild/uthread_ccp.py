"""Python Microthread Library, version 0.1
Microthreads are useful when you want to program many behaviors
happening simultaneously. Simulations and games often want to model
the simultaneous and independent behavior of many people, many
businesses, many monsters, many physical objects, many spaceships, and
so forth. With microthreads, you can code these behaviors as Python
functions. Microthreads use Stackless Python. For more details, see
http://world.std.com/~wware/uthread.html"""

__version__ = "0.1"

__license__ = \
"""Python Microthread Library version 0.1
Copyright (C)2000  Will Ware, Christian Tismer

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the names of the authors not be
used in advertising or publicity pertaining to distribution of the
software without specific, written prior permission.

WILL WARE AND CHRISTIAN TISMER DISCLAIM ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL WILL WARE OR CHRISTIAN TISMER BE LIABLE FOR
ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE."""

#import continuation
import stackless

MAX_TIMESLICE = 20000000

'''
tasks = [ ]
ghandler = None
'''

'''
def endtask():
    """force this thread to die"""
    continuation.uthread_lock(1)
    sched = continuation.uthread_reset()
    if sched != None:
        sched()
'''
# not needed yet

'''
def schedule():
    """force a context switch"""
    continuation.uthread_lock(1)
    sched = continuation.uthread_reset()
    sched(continuation.caller())
'''
# handled internally
schedule = stackless.schedule

'''
def new(func, *args, **kw):
    """Start a new task"""
    if func == None:
        raise "Don't you make me try to call None"
    global tasks
    assert not kw

    def wrapper(func, args):
        continuation.return_current()
        try:
            apply(func, args)
        except:
            continuation.uthread_reset()
            raise
        endtask()

    tmp = continuation.uthread_lock(1)
    task = wrapper(func, args)
    task.caller = None
    tasks.append(task)
    continuation.uthread_lock(tmp)
'''
def new(func, *args, **kw):
    """Start a new task"""
    gen = stackless.taskoutlet(func)
    t = gen(*args, **kw)
    t.insert()

'''
def run():
    """Run a bunch of tasks, until they all complete"""
    global tasks
    pop = tasks.pop
    append = tasks.append
    timeslice = continuation.timeslice
    if not tasks:
        # just enter the loop
        append(None)
    while tasks:
        task = pop(0)
        if task:
            try:
                task = timeslice(task, MAX_TIMESLICE)
            except UserError, e:
                global ghandler
                if ghandler:
                    new(ghandler, e)
                else:
                    print e

        if task:
            import runner
            runner.PostException(
                task,
                "THIS THREAD WAS PROBABLY STUCK IN AN INFINITE LOOP AND HAS BEEN NUKED!!!",
                None)

            #append(task)
'''
def run():
    """Run a bunch of tasks, until they all complete"""
    # have to add error handling like above
    while stackless.getruncount() > 1:
        try:
            # running until the end or until something happens
            victim = stackless.run_watchdog(MAX_TIMESLICE)
            if victim:
                print "THIS THREAD WAS PROBABLY STUCK IN AN INFINITE LOOP AND HAS BEEN NUKED!!!",
            # todo: kill the task cleanly
        except Exception, e:
            print "Exception occoured:", e

idIndex = 0

def sethandler(handler):
    global ghandler
    ghandler = handler


def uniqueId():
    """Microthread-safe way to get unique numbers, handy for
    giving things unique ID numbers"""
    global idIndex
    tmp = stackless.scheduler_lock(1)
    z = idIndex
    idIndex = z + 1
    stackless.scheduler_lock(tmp)
    return z

def irandom(n):
    """Microthread-safe version of random.randrange(0,n)"""
    import random
    tmp = stackless.scheduler_lock(1)
    n = random.randrange(0, n)
    stackless.scheduler_lock(tmp)
    return n

'''
class Semaphore:
    """Semaphores protect globally accessible resources from
    the effects of context switching."""
    __guid__ = 'uthread.Semaphore'
    def __init__(self, maxcount=1):
        self.count = maxcount
        self.waiting = []
    def claim(self):
        tmp = continuation.uthread_lock(1)
        if self.count == 0:
            self.waiting.append(continuation.caller())
            endtask()
        else:
            self.count = self.count - 1
            continuation.uthread_lock(tmp)
    def release(self):
        tmp = continuation.uthread_lock(1)
        if self.waiting:
            tasks.append(self.waiting.pop(0))
        else:
            self.count = self.count + 1
        continuation.uthread_lock(tmp)
'''

class Semaphore:
    """Semaphores protect globally accessible resources from
    the effects of context switching."""
    __guid__ = 'uthread_ccp.Semaphore'
    
    def __init__(self, maxcount=1):
        self.count = maxcount
        self.waiting = stackless.channel()
        
    def acquire(self):
        tmp = stackless.atomic()
        if self.count == 0:
            self.waiting.receive()
        else:
            self.count = self.count - 1
            
    claim = acquire
    
    def release(self):
        tmp = stackless.atomic()
        if self.waiting.queue:
            self.waiting.send(None)
        else:
            self.count = self.count + 1

class Queue:
    """A queue is a microthread-safe FIFO."""
    __guid__ = 'uthread_ccp.Queue'
    
    def __init__(self):
        self.contents = [ ]
        self.channel = stackless.channel()
        
    def put(self, x):
        tmp = stackless.atomic()
        self.contents.append(x)
        while self.channel.queue and self.contents:
            self.channel.send(self.contents.pop(0))
        
    def get(self):
        tmp = stackless.atomic()
        if self.contents:
            return self.contents.pop(0)
        return self.channel.receive()
            
    def unget(self, x):
        tmp = stackless.atomic()
        self.contents.insert(0, x)
        
    def cget(self):
        return self.contents.pop(0)


exports = {
    "uthread_ccp.new":          new,
    "uthread_ccp.irandom":      irandom,
    "uthread_ccp.uniqueId":     uniqueId,
    "uthread_ccp.run":          run,
    "uthread_ccp.schedule":     schedule,
    "uthread_ccp.sethandler":   sethandler,
    }
    
def test(n):
    global cnt
    for cnt in xrange(n):
        if cnt == 12345:
            1/0
            
            