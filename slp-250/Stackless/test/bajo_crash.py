import stackless

class A:
    def T1(self):
        print "T1"

    def bug(self):
        t1 = stackless.tasklet(self.T1)()
        t1.remove()
        stackless.schedule()

def Start():
    try:
        a = A()
        stackless.tasklet(a.bug)()
        stackless.schedule()
        raise Exception

    finally:
        this = stackless.getcurrent()
        while stackless.getruncount() > 1:
            this.next.kill()

Start()