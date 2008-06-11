import stackless

class CallCounter:
	def __init__(self):
		self.count = 0
	def __call__(self, prev, next):
		self.count += 1
		#print "callback %s" % self.count


callback1 = CallCounter()
stackless.set_schedule_callback(callback1)
stackless.tasklet(stackless.test_cframe)(3)
stackless.tasklet(stackless.test_cframe)(3)
assert callback1.count==0, "No callbacks before run"
stackless.run()
count1 = callback1.count
assert count1>= 2*3, "At least as may callbacks as many test_cframe calls"

callback2 = CallCounter()
stackless.set_schedule_callback(callback2)
stackless.tasklet(stackless.test_cframe)(5)
stackless.tasklet(stackless.test_cframe)(5)
stackless.run()
count2 = callback2.count
assert count2>=2*5, "At least as may callbacks as many test_cframe calls"
assert callback1.count==count1, "No calls to previous callback"
assert count2>count1, "More test_cframe calls => more callbacks on second run"

stackless.set_schedule_callback(None)
stackless.tasklet(stackless.test_cframe)(7)
stackless.tasklet(stackless.test_cframe)(7)
stackless.run()
assert callback1.count==count1, "No calls to previous callback after setting it to None"
assert callback2.count==count2, "No calls to previous callback after setting it to None"

print "all ok"
