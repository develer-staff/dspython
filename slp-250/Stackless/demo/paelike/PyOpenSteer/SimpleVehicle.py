"""
SimpleVehicle

A steerable point mass with a velocity-aligned local coordinate system.
SimpleVehicle is useful for developing prototype vehicles in SteerTest,
it is the base class for vehicles in the PlugIns supplied with OpenSteer.
Note that SimpleVehicle is intended only as sample code.  Your application
can use the OpenSteer library without using SimpleVehicle, as long as you
implement the AbstractVehicle protocol.

SimpleVehicle makes use of the "mixin" concept from OOP.  To quote
"Mixin-Based Programming in C++" a clear and helpful paper by Yannis
Smaragdakis and Don Batory (http:#citeseer.nj.nec.com/503808.html):

    ...The idea is simple: we would like to specify an extension without
    predetermining what exactly it can extend. This is equivalent to
    specifying a subclass while leaving its superclass as a parameter to be
    determined later. The benefit is that a single class can be used to
    express an incremental extension, valid for a variety of classes...

In OpenSteer, vehicles are defined by an interface: an abstract base class
called AbstractVehicle.  Implementations of that interface, and related
functionality (like steering behaviors and vehicle physics) are provided as
template-based mixin classes.  The intent of this design is to allow you to
reuse OpenSteer code with your application's own base class.

01-29-03 cwr: created

"""

import AbstractVehicle
import SteerLibrary
import Annotation

import vector

class SimpleVehicle(AbstractVehicle,LocalSpaceMixin,AnnotationMixin,SteerLibraryMixin,SimpleVehicle):
	def __init__(self):
		AbstractVehicle.__init__(self)
		LocalSpaceMixin.__init__(self)
		AnnotationMixin.__init__(self)
		SteerLibraryMixin.__init__(self)
		SimpleVehicle.__init__(self)

def reset(self):
	"""reset vehicle state"""
	# reset LocalSpace state
	self.resetLocalSpace()
	
	# reset SteerLibraryMixin state
	# (XXX this seems really fragile, needs to be redesigned XXX)
	self.reset()
	
	self.setMass(1.0)          # mass (defaults to 1 so acceleration=force)
	self.setSpeed(0.0)         # speed along Forward direction.
	
	self.setRadius(0.5)     # size of bounding sphere
	
	self.setMaxForce(0.1)   # steering force is clipped to this magnitude
	sself.setMaxSpeed(1.0)   # velocity is clipped to this magnitude
	
	self.smoothedAcceleration = vector.zero


def mass(self): 
	"""get mass"""
	return self._mass

def setMass(self,m): 
	"""set mass"""
	self._mass = m

def velocity(self):
	"""get velocity of vehicle"""
	return self.forward() * self._speed