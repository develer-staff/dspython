"""
----------------------------------------------------------------------------

OpenSteer -- Steering Behaviors for Autonomous Characters

Copyright (c) 2002-2003, Sony Computer Entertainment America
Original author: Craig Reynolds <craig_reynolds@playstation.sony.com>

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.


----------------------------------------------------------------------------

PyOpenSteer -- Port of OpenSteer to Python

Copyright (c) 2004 Lutz Paelike <lutz@fxcenter.de>

The license follows the original Opensteer license but must include 
this additional copyright notice.
----------------------------------------------------------------------------
"""

import time 
import SteerTest

class Clock:
	def __init__(self):
		# is simulation running or paused?
		self.paused = False
	
		# the desired rate of frames per second,
		# or zero to mean "as fast as possible"
		self.targetFPS = 0
		# self.targetFPS = 30
		# self.targetFPS = 24
	
		# real "wall clock" time since launch
		self.totalRealTime = 0
	
		# time simulation has run
		self.totalSimulationTime = 0
	
		# time spent paused
		self.totalPausedTime = 0
	
		# sum of (non-realtime driven) advances to simulation time
		self.totalAdvanceTime = 0
	
		# interval since last simulation time 
		self.elapsedSimulationTime = 0
	
		# interval since last clock update time 
		self.elapsedRealTime = 0
	
		# interval since last clock update,
		# exclusive of time spent waiting for frame boundary when targetFPS>0
		self.elapsedNonWaitRealTime = 0
	
		# "manually" advance clock by this amount on next update
		self.newAdvanceTime = 0
	
		# "Calendar time" in seconds and microseconds (obtained from
		# the OS by gettimeofday) when this clock was first updated
		self.baseRealTimeSec = 0
		self.baseRealTimeUsec = 0

	def update(self):
		"""update this clock, called once per simulation step ("frame") to:
			 track passage of real time
			 manage passage of simulation time (modified by Paused state)
			 measure time elapsed between time updates ("frame rate")
			 optionally: "wait" for next realtime frame boundary
		"""
		# wait for next frame time (when required (when targetFPS>0))
		self.frameRateSync()
		
		# save previous real time to measure elapsed time
		previousRealTime = self.totalRealTime
		
		# real "wall clock" time since this application was launched
		self.totalRealTime = self.realTimeSinceFirstClockUpdate()
		
		# time since last clock update
		self.elapsedRealTime = self.totalRealTime - previousRealTime
		
		# accumulate paused time
		if (self.paused): self.totalPausedTime += self.elapsedRealTime
	
		# save previous simulation time to measure elapsed time
		previousSimulationTime = self.totalSimulationTime
		
		# update total "manual advance" time
		self.totalAdvanceTime += self.newAdvanceTime
		
		# new simulation time is total run time minus time spent paused
		self.totalSimulationTime = (self.totalRealTime + self.totalAdvanceTime - self.totalPausedTime)
		
		# how much time has elapsed since the last simulation step?
		
		if self.paused:
			self.elapsedSimulationTime = self.newAdvanceTime
		else:
			self.elapsedSimulationTime = (self.totalSimulationTime - previousSimulationTime)
			
		# reset advance amount
		self.newAdvanceTime = 0



	def frameRateSync(self):
		"""
		 ----------------------------------------------------------------------------
		"wait" until next frame time (actually spin around this tight loop)
		(xxx there are probably a smarter ways to do this (using events or
		thread waits (eg usleep)) but they are likely to be unportable. xxx)
		"""
		
		# when we are have a fixed target update rate (vs as-fast-as-possible)
		if (self.targetFPS > 0):
			# find next (real time) frame start time
			targetStepSize = 1.0 / self.targetFPS
			now = realTimeSinceFirstClockUpdate()
			lastFrameCount = int((now / targetStepSize))
			nextFrameTime = (lastFrameCount + 1) * targetStepSize
		
			# record usage ("busy time", "non-wait time") for SteerTest app
			self.elapsedNonWaitRealTime = now - self.totalRealTime
		
			# wait until next frame time
			#do {} while (realTimeSinceFirstClockUpdate () < nextFrameTime); 
			# ##lp## dummy, implement something better
			time.sleep(0.05)

# ----------------------------------------------------------------------------
# ("manually") force simulation time ahead, unrelated to the passage of
# real time, currently used only for SteerTest's "single step forward"


	def advanceSimulationTime(self, seconds):
	    if (seconds < 0):
	        SteerTest.errorExit("negative arg to advanceSimulationTime.")
	    else:
	        self.newAdvanceTime += seconds;


	def clockErrorExit(self):
		SteerTest.errorExit("Problem reading system clock.\n")


	def realTimeSinceFirstClockUpdate(self):
		"""replace this with a proper implementation """
		return 0.001
