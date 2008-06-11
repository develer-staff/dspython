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

# global variables (static in module level)

totalSizeOfRegistry = 0
itemsInRegistry = 0
registry = []

class AbstractPlugIn:
	"""abstract base classe for plugins"""

	def open(self):
		"""open the plugin and initialize"""
		pass
		
	def update(self,currentTime, elapsedTime):
		"""update action of the plugin
		params: float,float"""
		pass
		
	def redraw(self,currentTime, elapsedTime):
		"""redraw action of the plugin
		params: float,float"""
		pass
		
	def close(self):
		"""close down the plugin and deinitialize"""
		pass

	def reset(self):
		"""reset the plugin"""
		pass

	def name(self):
		"""returns this instance's character name as string"""
		pass

	def selectionOrderSortKey(self):
		"""numeric sort key used to establish user-visible PlugIn ordering
		("built ins" have keys greater than 0 and less than 1)"""
		pass
		
	def requestInitialSelection(self):
		"""allows a PlugIn to nominate itself as SteerTest's initially selected
		(default) PlugIn, which is otherwise the first in "selection order"""
		pass
		
	def handleFunctionKeys(self, keyNumber):
		"""handle function keys (which are reserved by SteerTest for PlugIns)
		params: keynumber as int"""
		pass
			
	def printMiniHelpForFunctionKeys(self):
		"""print "mini help" documenting function keys handled by this PlugIn"""
		pass

	def allVehicles(self):
		"""returns a list [] of AbstractVehicle objects 
		(vehicles/agents/characters) defined by the PlugIn"""
		pass

class PlugIn(AbstractPlugIn):
	"""
		integrate this the python way ...
	
		typedef void (* plugInCallBackFunction) (PlugIn& clientObject);
		typedef void (* voidCallBackFunction) (void);
		typedef void (* timestepCallBackFunction) (const float currentTime,
		                                           const float elapsedTime);
	"""	

	def __init__(self):
		"""Init"""
		pass
	
	def __del__(self):
		"""DeInit"""
		pass

	def reset(self):
		"""default reset method is to do a close then an open"""
		self.close()
		self.open()
		
	def selectionOrderSortKey(self):
		"""default sort key (after the "built ins")"""
		return 1.0
		
	def requestInitialSelection(self):
		"""default is to NOT request to be initially selected"""
		return False
		
	def handleFunctionKeys(self, keyNumber):
		"""default function key handler: ignore all)
		params: keynumber as int"""
		pass

	def printMiniHelpForFunctionKeys(self):
		"""default "mini help": print nothing"""
		pass

	def next(self):
		""" returns next PlugIn in "selection order" """
		return None


	def __str__(self):
		"""convert PlugIn to string, just return the name"""
		return pi.name
		
		
	def findByName(self, name):
		"""search the class registry for a Plugin 
		with the given name and return the PlugIn obejct
		"""
		return None
		
	def applyToAll(self, plugInCallBackFunction):
		"""apply a given function to all PlugIns in the class registry"""
		pass
	
	def sortBySelectionOrder(self):
		"""sort PlugIn registry by "selection order" """
		pass
		
	def findDefault(self):
		"""returns default PlugIn (currently, first in registry) 
		"""
		return None	

	def addToRegistry(self):
		"""save this instance in the class's registry of instances 
		"""
		pass
			