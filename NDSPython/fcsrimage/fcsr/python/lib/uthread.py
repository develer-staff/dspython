import stackless

def new(func, *args, **kwargs):
    return stackless.tasklet(func)(*args, **kwargs)

def run():
    while stackless.runcount > 1:
        t = stackless.run(1000)
        if t:
            # Tasklet went out of control.  Kill it or just throw it back in (denial).
            t.insert()

lastID = 0

def uniqueId():
    global lastID
    lastID += 1
    return lastID