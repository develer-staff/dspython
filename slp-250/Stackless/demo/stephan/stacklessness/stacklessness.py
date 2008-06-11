from threading import Event, currentThread, Lock, Thread
import time
import sys
import logging
from atexit import register

__all__ = 'run getcurrent getmain tasklet channel schedule'.split()

def prepareLogger(level):
    import os
    try:
        os.unlink('stackless.log')
    except:pass
    logger = logging.getLogger('stackless')
    hdlr = logging.FileHandler('stackless.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(level)

    return logger

log = prepareLogger(logging.INFO)


scheduler = None
maintasklet = None
globallock = Lock()
alltasks = []

def __init():
    global maintasklet
    global scheduler
    global globallock
    mt = tasklet(None)
    mt._active = True
    mt._name = 'MainTask'
    maintask = currentThread()
    log.info(str(maintask))
    maintask.event = Event()
    mt.thread = maintask
    maintask.tasklet = mt
    maintasklet = mt
    scheduler = Scheduler()
    log.info('# %s # is about to acquire the globallock' % getcurrent())
    globallock.acquire()
    log.info('# %s # acquired the globallock' % getcurrent())


# RuntimeError:
# possible messages:
# 'You cannot run a blocked tasklet'
class RuntimeError(Exception):pass

def run():
    schedule()

def getcurrent():
    ct = currentThread()
    return ct.tasklet

def getmain():
    return maintasklet

def schedule():
    scheduler.schedule()

class taskletwrapper(Thread):
    # run is called within the new thread
    def run(self):
        log.info('# %s # is about to acquire the globallock' % getcurrent())
        globallock.acquire()
        log.info('# %s # acquired the globallock' % getcurrent())
        try:
            Thread.run(self)
        finally:
            self.tasklet.remove()
            schedule()

class tasklet(object):
    def __init__(self,func):
        self.func = func
        self._active = False
        self._name = 'Task%s' % str(len(alltasks) + 1)
        self._shouldawake = False

    def __str__(self):
        return self._name

    __repr__ = __str__

    def __call__(self,*argl,**argd):
        self.thread = taskletwrapper(target=self.func,args=argl,kwargs=argd)
        self.thread.tasklet = self
        self.thread.event = Event()
        self.insert()
        self._active = True
        self.thread.start()
        alltasks.append(self)
        return self

    def awake(self):
        log.info('%s calling %s.awake()' % (getcurrent(),self))
        self._shouldawake = True
        self.thread.event.set()

    def sleep(self):
        log.info('%s %s.sleep()' % (getcurrent(),self))
        self._shouldawake = False
        self.thread.event.clear()
        try:
            log.info('# %s # about to release the globallock' % getcurrent())
            globallock.release()
        except:pass
        log.info('%s is going to sleep' % getcurrent())
        while (not self.thread.event.isSet()) and self._active:
            log.info('%s is still waiting' % getcurrent())
            self.thread.event.wait(.01)
            if self._shouldawake:
                self._shouldawake = False
                log.info('%s Event notification did NOT work. Waking up anyway' % getcurrent())
                break
        log.info('%s is waking up' % getcurrent())
        if self._active:
            log.info('\t%s still active' % self)
            log.info('# %s # is about to acquire the globallock' % getcurrent())
            globallock.acquire()
            log.info('# %s # acquired the globallock' % getcurrent())
        else:
            log.info('\t%s not active anymore' % self)

    def run(self):
        scheduler.setnexttask(self)
        schedule()


    def insert(self):
        scheduler.insert(self)

    def remove(self):
        self._active = False
        scheduler.remove(self)
        log.info('# %s # about to release the globallock' % getcurrent())
        try:
            globallock.release()
        except:
            log.info('%s attempted to release globallock, but did not own it' % getcurrent())

    def kill(self):
        self._active = False
        self.awake()

class channel(object):
    def __init__(self):
        self._readq = []
        self._writeq = []
        self.balance = 0
        
    def send(self,msg):
        ct = getcurrent()
        log.info('%s is sending %s' % (ct,msg))
        scheduler.remove(ct)
        self._writeq.append((ct,msg))
        self.balance += 1
        if self._readq:
            nt = self._readq[0]
            del(self._readq[0])
            scheduler.priorityinsert(nt)
        schedule()

    def send_exception(self,exp,msg):
        ct = getcurrent()
        
    def receive(self):
        ct = getcurrent()
        log.info('%s is receiving' % ct)
        if self._writeq:
            log.info('\tfound something in writequeue')
            wt,retval = self._writeq[0]
            scheduler.priorityinsert(wt)
            del(self._writeq[0])
            self.balance -= 1
            return retval
        else:
            log.info('\tneed to block')
            self._readq.append(ct)
            scheduler.remove(ct)
            schedule()
            return self.receive()


class Scheduler(object):
    def __init__(self):
        self.tasklist = []
        self.nexttask = None 

    def empty(self):
        log.info('%s Scheduler.emtpy()' % getcurrent())
        return not self.tasklist

    def __str__(self):
        log.info('%s Scheduler.__str__()' % getcurrent())
        return repr(self.tasklist) + '/%s' % self.nexttask

    def insert(self,obj):
        log.info('%s Scheduler.insert(%s)' % (getcurrent(),obj))
        if (obj not in self.tasklist) and obj is not maintasklet:
            self.tasklist.append(obj)
        if self.nexttask is None:
            self.nexttask = 0

    def priorityinsert(self,obj):
        log.info('%s Scheduler.priorityinsert(%s)' % (getcurrent(),obj))
        log.info('\tbefore: %s' % self)
        if obj in self.tasklist:
            self.tasklist.remove(obj)
        if obj is maintasklet:
            return
        if self.nexttask:
            self.tasklist.insert(self.nexttask,obj)
        else:
            self.tasklist.insert(0,obj)
            self.nexttask = 0
        log.info('\tafter: %s' % self)

    def remove(self,obj):
        log.info('%s Scheduler.remove(%s)' % (getcurrent(),obj))
        try:
            i = self.tasklist.index(obj)
            del(self.tasklist[i])
            if self.nexttask > i:
                self.nexttask -= 1
            if len(self.tasklist) == 0:
                self.nexttask = None
        except ValueError:pass

    def next(self):
        log.info('%s Scheduler.next()' % getcurrent())
        if self.nexttask is not None:
            obj = self.tasklist[self.nexttask]
            self.nexttask += 1
            if self.nexttask == len(self.tasklist):
                self.nexttask = 0
            return obj
        else:
            return maintasklet

    def setnexttask(self,obj):
        log.info('%s Scheduler.setnexttask(%s)' % (getcurrent(),obj))
        if obj not in self.tasklist:
            self.tasklist.insert(obj)
        try:
            i = self.tasklist.index(obj)
            self.nexttask = i
        except IndexError:pass

    def schedule(self):
        log.info('%s Scheduler.schedule()' % getcurrent())
        log.info('\ttasklist:%s' % self)
        ct = currentThread()
        ctask = ct.tasklet
        log.info('\tcurrent tasklet is: %s' % ctask)
        nt = self.next()
        if ctask == nt:
            #raise RuntimeError("No task to schedule")
            pass
        log.info('\twaking up: %s' % nt)
        nt.awake()
        ctask.sleep()

__init()

def cleanup():
    for task in alltasks:
        task.kill()

register(cleanup)

if __name__ == '__main__':
    pass
