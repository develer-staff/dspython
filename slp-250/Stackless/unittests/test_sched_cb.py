import unittest
import stackless


class SchedulingMonitor:
    "A scheduling monitor acting as a callback for set_schedule_callback()."
    
    def __init__(self):
        self.count = 0

    def __call__(self, prevTasklet, nextTasklet):
        self.count += 1
        

class SchedulingCallbackTestCase(unittest.TestCase):
    "A collection of scheduling callback tests."

    def test0(self):
        "Test #callbacks before and after running isolated monitor."

        mon1 = SchedulingMonitor()
        stackless.set_schedule_callback(mon1)
        stackless.tasklet(stackless.test_cframe)(3)
        stackless.tasklet(stackless.test_cframe)(3)
        # precondition
        self.failUnless(
            mon1.count == 0,
            "No callbacks before running")
        # running
        stackless.run()
        # postcondition
        self.failUnless(
            mon1.count >= 2*3,
            "At least as may callbacks as many test_cframe calls")


    def test1(self):
        "Test multiple monitors, from test/test_set_schedule_callback.py"
        
        fu = self.failUnless
        n = 2
        
        mon1 = SchedulingMonitor()
        stackless.set_schedule_callback(mon1)
        v = 3
        for i in range(n): stackless.tasklet(stackless.test_cframe)(v)
        c1 = mon1.count
        fu(c1 == 0, "No callbacks before running")
        stackless.run()
        c1 = mon1.count
        fu(c1 >= n*v, "At least as may callbacks as many test_cframe calls")

        mon2 = SchedulingMonitor()
        stackless.set_schedule_callback(mon2)
        v = 5
        for i in range(n): stackless.tasklet(stackless.test_cframe)(v)
        stackless.run()
        c2 = mon2.count
        fu(c2 >= n*v, "At least as may callbacks as many test_cframe calls")
        fu(mon1.count == c1, "No calls to previous callback")
        fu(c2 > c1, "More test_cframe calls => more callbacks on second run")
        
        stackless.set_schedule_callback(None)
        v = 7
        for i in range(n): stackless.tasklet(stackless.test_cframe)(v)
        stackless.run()
        c1p = mon1.count
        c2p = mon2.count
        fu(c1p == c1, "No calls to previous callback after setting it to None")
        fu(c2p == c2, "No calls to previous callback after setting it to None")


if __name__ == "__main__":
    unittest.main()
