import stackless

class B:
    def __del__(self):
        1 << 4 # good breakpoint for ceval :-)
        print "__del__"
        # even this works now!
        stackless.schedule()

class A:
    def T2(self, b):
        pass

    def bug(self):
        b = B()
        t=stackless.tasklet(self.T2)(b)
        t.remove()

a = A()
a.bug()
