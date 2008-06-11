import cgtypes
import types, math

from Utilities import frandom01

class vec3(cgtypes.vec3):
	def __init__(self, *args):
		cgtypes.vec3.__init__(self,args)
		

	
	def __repr__(self):
		return 'vec3('+`self.x`+', '+`self.y`+', '+`self.z`+')'
	
	def __str__(self):
		fmt="%1.4f"
		return '('+fmt%self.x+', '+fmt%self.y+', '+fmt%self.z+')'
	
	
	def __eq__(self, other):
		"""== operator
	
		>>> a=vec3(1.0, 0.5, -1.8)
		>>> b=vec3(-0.3, 0.75, 0.5)
		>>> c=vec3(-0.3, 0.75, 0.5)
		>>> print a==b
		0
		>>> print b==c
		1
		>>> print a==None
		0
		"""
		if isinstance(other, vec3):
			return self.x==other.x and self.y==other.y and self.z==other.z
		else:
			return 0
	
	def __ne__(self, other):
		"""!= operator
	
		>>> a=vec3(1.0, 0.5, -1.8)
		>>> b=vec3(-0.3, 0.75, 0.5)
		>>> c=vec3(-0.3, 0.75, 0.5)
		>>> print a!=b
		1
		>>> print b!=c
		0
		>>> print a!=None
		1
		"""
		if isinstance(other, cgtypes.vec3):
			return self.x!=other.x or self.y!=other.y or self.z!=other.z
		else:
			return 1
	
	
	def __add__(self, other):
		"""Vector addition.
	
		>>> a=vec3(1.0, 0.5, -1.8)
		>>> b=vec3(-0.3, 0.75, 0.5)
		>>> print a+b
		(0.7000, 1.2500, -1.3000)
		"""
		if isinstance(other, cgtypes.vec3):
			return vec3(self.x+other.x, self.y+other.y, self.z+other.z)
		else:
			raise TypeError, "unsupported operand type for +"
	
	def __sub__(self, other):
		"""Vector subtraction.
	
		>>> a=vec3(1.0, 0.5, -1.8)
		>>> b=vec3(-0.3, 0.75, 0.5)
		>>> print a-b
		(1.3000, -0.2500, -2.3000)
		"""
		if isinstance(other, cgtypes.vec3):
			return vec3(self.x-other.x, self.y-other.y, self.z-other.z)
		else:
			raise TypeError, "unsupported operand type for -"
	
	def __mul__(self, other):
		"""Multiplication with a scalar or dot product.
	
		>>> a=vec3(1.0, 0.5, -1.8)
		>>> b=vec3(-0.3, 0.75, 0.5)
		>>> print a*2.0
		(2.0000, 1.0000, -3.6000)
		>>> print 2.0*a
		(2.0000, 1.0000, -3.6000)
		>>> print a*b
		-0.825
		"""
	
		T = type(other)
		# vec3*scalar
		if T==types.FloatType or T==types.IntType or T==types.LongType:
			return vec3(self.x*other, self.y*other, self.z*other)
		# vec3*vec3
		if isinstance(other, cgtypes.vec3):
			return self.x*other.x + self.y*other.y + self.z*other.z
		# unsupported
		else:
			# Try to delegate the operation to the other operand
			if getattr(other,"__rmul__",None)!=None:
				return other.__rmul__(self)
			else:
				raise TypeError, "unsupported operand type for *"
	
	__rmul__ = __mul__
	
	def __div__(self, other):
		"""Division by scalar
	
		>>> a=vec3(1.0, 0.5, -1.8)
		>>> print a/2.0
		(0.5000, 0.2500, -0.9000)
		"""
		T = type(other)
		# vec3/scalar
		if T==types.FloatType or T==types.IntType or T==types.LongType:
			return vec3(self.x/other, self.y/other, self.z/other)
		# unsupported
		else:
			raise TypeError, "unsupported operand type for /"
	
	def __mod__(self, other):
		"""Modulo (component wise)
	
		>>> a=vec3(3.0, 2.5, -1.8)
		>>> print a%2.0
		(1.0000, 0.5000, 0.2000)
		"""
		T = type(other)
		# vec3%scalar
		if T==types.FloatType or T==types.IntType or T==types.LongType:
			return vec3(self.x%other, self.y%other, self.z%other)
		# unsupported
		else:
			raise TypeError, "unsupported operand type for %"
	
	def __iadd__(self, other):
		"""Inline vector addition.
	
		>>> a=vec3(1.0, 0.5, -1.8)
		>>> b=vec3(-0.3, 0.75, 0.5)
		>>> a+=b
		>>> print a
		(0.7000, 1.2500, -1.3000)
		"""
		if isinstance(other, cgtypes.vec3):
			self.x+=other.x
			self.y+=other.y
			self.z+=other.z
			return self
		else:
			raise TypeError, "unsupported operand type for +="
	
	def __isub__(self, other):
		"""Inline vector subtraction.
	
		>>> a=vec3(1.0, 0.5, -1.8)
		>>> b=vec3(-0.3, 0.75, 0.5)
		>>> a-=b
		>>> print a
		(1.3000, -0.2500, -2.3000)
		"""
		if isinstance(other, cgtypes.vec3):
			self.x-=other.x
			self.y-=other.y
			self.z-=other.z
			return self
		else:
			raise TypeError, "unsupported operand type for -="
	
	def __imul__(self, other):
		"""Inline multiplication (only with scalar)
	
		>>> a=vec3(1.0, 0.5, -1.8)
		>>> a*=2.0
		>>> print a
		(2.0000, 1.0000, -3.6000)
		"""
		T = type(other)
		# vec3*=scalar
		if T==types.FloatType or T==types.IntType or T==types.LongType:
			self.x*=other
			self.y*=other
			self.z*=other
			return self
		else:
			raise TypeError, "unsupported operand type for *="
	
	def __idiv__(self, other):
		"""Inline division with scalar
	
		>>> a=vec3(1.0, 0.5, -1.8)
		>>> a/=2.0
		>>> print a
		(0.5000, 0.2500, -0.9000)
		"""
		T = type(other)
		# vec3/=scalar
		if T==types.FloatType or T==types.IntType or T==types.LongType:
			self.x/=other
			self.y/=other
			self.z/=other
			return self
		else:
			raise TypeError, "unsupported operand type for /="
	
	def __imod__(self, other):
		"""Inline modulo
	
		>>> a=vec3(3.0, 2.5, -1.8)
		>>> a%=2.0
		>>> print a
		(1.0000, 0.5000, 0.2000)
		"""
		T = type(other)
		# vec3%=scalar
		if T==types.FloatType or T==types.IntType or T==types.LongType:
			self.x%=other
			self.y%=other
			self.z%=other
			return self
		else:
			raise TypeError, "unsupported operand type for %="
	
	def __neg__(self):
		"""Negation
	
		>>> a=vec3(3.0, 2.5, -1.8)
		>>> print -a
		(-3.0000, -2.5000, 1.8000)
		"""
		return vec3(-self.x, -self.y, -self.z)
	
	def __pos__(self):
		"""
		>>> a=vec3(3.0, 2.5, -1.8)
		>>> print +a
		(3.0000, 2.5000, -1.8000)
		"""
		return vec3(+self.x, +self.y, +self.z)
	
	def __abs__(self):
		"""Return the length of the vector.
	
		abs(v) is equivalent to v.length().
	
		>>> a=vec3(1.0, 0.5, -1.8)
		>>> print abs(a)
		2.11896201004
		"""
		return math.sqrt(self*self)
	
	
	def __len__(self):
		"""Length of the sequence (always 3)"""
		return 3
	
	def __getitem__(self, key):
		"""Return a component by index (0-based)
	
		>>> a=vec3(1.0, 0.5, -1.8)
		>>> print a[0]
		1.0
		>>> print a[1]
		0.5
		>>> print a[2]
		-1.8
		"""
		T=type(key)
		if T!=types.IntType and T!=types.LongType:
			raise TypeError, "index must be integer"
	
		if   key==0: return self.x
		elif key==1: return self.y
		elif key==2: return self.z
		else:
			raise IndexError,"index out of range"
	
	def __setitem__(self, key, value):
		"""Set a component by index (0-based)
	
		>>> a=vec3()
		>>> a[0]=1.5; a[1]=0.7; a[2]=-0.3
		>>> print a
		(1.5000, 0.7000, -0.3000)
		"""
		T=type(key)
		if T!=types.IntType and T!=types.LongType:
			raise TypeError, "index must be integer"
	
		if   key==0: self.x = value
		elif key==1: self.y = value
		elif key==2: self.z = value
		else:
			raise IndexError,"index out of range"
	
	def cross(self, other):
		"""Cross product.
	
		>>> a=vec3(1.0, 0.5, -1.8)
		>>> b=vec3(-0.3, 0.75, 0.5)
		>>> c=a.cross(b)
		>>> print c
		(1.6000, 0.0400, 0.9000)
		"""
		
		if isinstance(other, cgtypes.vec3):
			return vec3(self.y*other.z-self.z*other.y,
						self.z*other.x-self.x*other.z,
						self.x*other.y-self.y*other.x)
		else:
			raise TypeError, "unsupported operand type for cross()"
		
	
	def length(self):
		"""Return the length of the vector.
	
		v.length() is equivalent to abs(v).
	
		>>> a=vec3(1.0, 0.5, -1.8)
		>>> print a.length()
		2.11896201004
		"""
	
		return math.sqrt(self*self)
	
	def normalize(self):
		"""Return normalized vector.
	
		>>> a=vec3(1.0, 0.5, -1.8)
		>>> print a.normalize()
		(0.4719, 0.2360, -0.8495)
		"""
	
		nlen = 1.0/math.sqrt(self*self)
		return vec3(self.x*nlen, self.y*nlen, self.z*nlen)
	
	def angle(self, other):
		"""Return angle (in radians) between self and other.
	
		>>> a=vec3(1.0, 0.5, -1.8)
		>>> b=vec3(-0.3, 0.75, 0.5)
		>>> print a.angle(b)
		1.99306755584
		"""
		
		if isinstance(other, cgtypes.vec3):
			return math.acos((self*other) / (abs(self)*abs(other)))
		else:
			raise TypeError, "unsupported operand type for angle()"
	
	def reflect(self, N):
		"""Return the reflection vector.
	
		N is the surface normal which has to be of unit length.
	
		>>> a=vec3(1.0, 0.5, -1.8)
		>>> print a.reflect(vec3(1,0,1))
		(2.6000, 0.5000, -0.2000)
		"""
	
		return self - 2.0*(self*N)*N
	
	def refract(self, N, eta):
		"""Return the transmitted vector.
	
		N is the surface normal which has to be of unit length.
		eta is the relative index of refraction. If the returned
		vector is zero then there is no transmitted light because
		of total internal reflection.
		
		>>> a=vec3(1.0, -1.5, 0.8)
		>>> print a.refract(vec3(0,1,0), 1.33)
		(1.3300, -1.7920, 1.0640)
		"""
	
		dot = self*N
		k   = 1.0 - eta*eta*(1.0 - dot*dot)
		if k<0:
			return vec3(0.0,0.0,0.0)
		else:
			return eta*self - (eta*dot + math.sqrt(k))*N
	
	def ortho(self):
		"""Returns an orthogonal vector.
	
		Returns a vector that is orthogonal to self (where
		self*self.ortho()==0).
	
		>>> a=vec3(1.0, -1.5, 0.8)
		>>> print round(a*a.ortho(),8)
		0.0
		"""
	
		x=abs(self.x)
		y=abs(self.y)
		z=abs(self.z)
		# Is z the smallest element? Then use x and y
		if z<=x and z<=y:
			return vec3(-self.y, self.x, 0.0)
		# Is y smallest element? Then use x and z
		elif y<=x and y<=z:
			return vec3(-self.z, 0.0, self.x)
		# x is smallest
		else:
			return vec3(0.0, -self.z, self.y)
	
	def set(self,_x,_y,_z):
		self.x = _x
		self.y = _y
		self.z = _z
		
	def dot(self,v):
		return self*v
	
	def lengthSquared(self):
		"""
		Just provide another name for the dot product operation
		to make it more compatible to the original opensteer implementation
		"""
		return self*self
	
	def parallelComponent(self, unitBasis):
		"""
		return component of vector parallel to a unit basis vector
		(IMPORTANT NOTE: assumes "basis" has unit magnitude (length==1))
		"""        
		projection = self*unitBasis
		return unitBasis * projection
	
	def perpendicularComponent(self, unitBasis):
		"""
		return component of vector perpendicular to a unit basis vector
		(IMPORTANT NOTE: assumes "basis" has unit magnitude (length==1))
		"""
		return self - self.parallelComponent(unitBasis)
	
	def truncateLength(self,maxLength):
		"""
		clamps the length of a given vector to maxLength.  If the vector is
		shorter its value is returned unaltered, if the vector is longer
		the value returned has length of maxLength and is paralle to the
		original input.
		"""
		maxLengthSquared = maxLength * maxLengthSquared
		vecLengthSquared = self.lengthSquared()
		if (vecLengthSquared <= maxLengthSquared):
			return self
		else:
			return self * (maxLength / math.sqrt(vecLengthSquared))
	
	def setYtoZero(self):
		"""forces a 3d position onto the XZ (aka y=0) plane"""
		return vec3(self.x,0.0,self.z)
	
	def rotateAboutGlobalY(self,angle, _sin=0.0,_cos=0.0):
		"""rotate this vector about the global Y (up) axis by the given angle"""
	
		if ((_sin==0.0) & (_cos==0.0)):               
			s = math.sin(angle)
			c = math.cos(angle)
		else:
			# use cached values for computation
			s = _sin
			c = _cos
		return (vec3(((self.x*c) + (self.z*s)), self.y, ((self.z*c) + (self.x*s))), s, c)
	
	def sphericalWrapAround(self,center,radius):
		""" """
		offset = self - center
		r = offset.length()
		if (r > radius):
			return self + ((offset/r) * radius * -2)
		else:
			return self
		
	
	
	def RandomVectorInUnitRadiusSphere(self):
		"""
		Returns a position randomly distributed inside a sphere of unit radius
		centered at the origin.  Orientation will be random and length will range
		between 0 and 1
		"""
		v = vec3()
		while 1:
			v.set (	(frandom01()*2) - 1,
					(frandom01()*2) - 1,
					(frandom01()*2) - 1)
			if (v.length()>=1):
				break
		return v
	
	def randomVectorOnUnitRadiusXZDisk(self):
		"""
		Returns a position randomly distributed on a disk of unit radius
		on the XZ (Y=0) plane, centered at the origin.  Orientation will be
		random and length will range between 0 and 1
		"""
		v = vec3()
		while 1:
			v.set( ((frandom01()*2) - 1, 0, (frandom01()*2) - 1))
			if (v.length()>=1):
				break
		return v
		
	def RandomUnitVector(self):
		"""
		Returns a position randomly distributed on a disk of unit radius
		on the XZ (Y=0) plane, centered at the origin.  Orientation will be
		random and length will range between 0 and 1
		"""
		return self.RandomVectorInUnitRadiusSphere().normalize();
	
	
	
	def RandomUnitVectorOnXZPlane(self):
		"""
		Returns a position randomly distributed on a circle of unit radius
		on the XZ (Y=0) plane, centered at the origin.  Orientation will be
		random and length will be 1
		"""
		return self.RandomVectorInUnitRadiusSphere().setYtoZero().normalize()
	
	
	def vecLimitDeviationAngleUtility(self, insideOrOutside, source, cosineOfConeAngle, basis):
		"""
		Does a "ceiling" or "floor" operation on the angle by which a given vector
		deviates from a given reference basis vector.  Consider a cone with "basis"
		as its axis and slope of "cosineOfConeAngle".  The first argument controls
		whether the "source" vector is forced to remain inside or outside of this
		cone.  Called by vecLimitMaxDeviationAngle and vecLimitMinDeviationAngle.
		"""

		# immediately return zero length input vectors
		sourceLength = source.length()
		if (sourceLength == 0): return source
	
		# measure the angular deviation of "source" from "basis"
		direction = source / sourceLength
		cosineOfSourceAngle = direction.dot(basis)
	
		# Simply return "source" if it already meets the angle criteria.
		# (note: we hope this top "if" gets compiled out since the flag
		# is a constant when the function is inlined into its caller)
		if (insideOrOutside):
			# source vector is already inside the cone, just return it
			if (cosineOfSourceAngle >= cosineOfConeAngle): return source
		else:
			# source vector is already outside the cone, just return it
			if (cosineOfSourceAngle <= cosineOfConeAngle): return source

		# find the portion of "source" that is perpendicular to "basis"
		perp = source.perpendicularComponent(basis)
	
		# normalize that perpendicular
		unitPerp = perp.normalize()
	
		# construct a new vector whose length equals the source vector,
		# and lies on the intersection of a plane (formed the source and
		# basis vectors) and a cone (whose axis is "basis" and whose
		# angle corresponds to cosineOfConeAngle)
		perpDist = math.sqrt(1 - (cosineOfConeAngle * cosineOfConeAngle))
		c0 = basis * cosineOfConeAngle
		c1 = unitPerp * perpDist
		return (c0 + c1) * sourceLength


	
	
	
	def limitMaxDeviationAngle(self, source, cosineOfConeAngle, basis):
		"""
		Enforce an upper bound on the angle by which a given arbitrary vector
		diviates from a given reference direction (specified by a unit basis
		vector).  The effect is to clip the "source" vector to be inside a cone
		defined by the basis and an angle.
		"""
		return self.vecLimitDeviationAngleUtility( True, # force source INSIDE cone
											  source,
											  cosineOfConeAngle,
											  basis)
	
	
	
	def limitMinDeviationAngle(self, source, cosineOfConeAngle, basis):
		"""
		Enforce an lower bound on the angle by which a given arbitrary vector
		diviates from a given reference direction (specified by a unit basis
		vector).  The effect is to clip the "source" vector to be inside a cone
		defined by the basis and an angle.
		"""
		return vecLimitDeviationAngleUtility(True, # force source INSIDE cone
                                          		 source,
											 cosineOfConeAngle,
                                          		 basis)


	def distanceFromLine( point, lineOrigin, lineUnitTangent):
		"""
		Returns the distance between a point and a line.  The line is defined in
		terms of a point on the line ("lineOrigin") and a UNIT vector parallel to
		the line ("lineUnitTangent")
		"""
		offset = point - lineOrigin
		perp = offset.perpendicularComponent(lineUnitTangent)
		return perp.length()


	def  findPerpendicularIn3d(direction):
		"""
		given a vector, return a vector perpendicular to it (note that this
		arbitrarily selects one of the infinitude of perpendicular vectors)
		"""

		quasiPerp = vec3()
		result = vec3()
	
		# three mutually perpendicular basis vectors
		i = vec3(1.0, 0.0, 0.0)
		j = vec3(0.0, 1.0, 0.0)
		k = vec3(0.0, 0.0, 1.0)
		
	
		# measure the projection of "direction" onto each of the axes
		id = i.dot(direction);
		jd = j.dot(direction);
		kd = k.dot(direction);
	
	   # set quasiPerp to the basis which is least parallel to "direction"
		if ((id <= jd) & (id <= kd)):
			quasiPerp = i  # projection onto i was the smallest
		else:
			if ((jd <= id) & (jd <= kd)):
				quasiPerp = j  # projection onto j was the smallest
			else:
				quasiPerp = k  # projection onto k was the smallest
	
		# return the cross product (direction x quasiPerp)
		# which is guaranteed to be perpendicular to both of them
		result.cross(direction, quasiPerp)
		return result

#names for frequently used vector constants
zero = vec3(0.0,0.0,0.0)
side = vec3(-1.0,0.0,0.0)
up = vec3(0.0,1.0,0.0)
forward = vec3(0.0,0.0,1.0)