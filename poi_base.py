###############################################################################
''' 
	Basic class definitions that will be used in the Waypoint search project
'''
###############################################################################

'''
	Class:
		Point
	
	Description:
		A point in 2D or 3D space
		
	Notes:
		
'''
class Point:
	def __init__(self, *args):
		'''
		@param x: x coordinate
		@param y: y coordinate
		@param z: z coordinate
		'''
		#Exception handling
		if len(args) < 2 or len(args) > 3:
			raise Exception("Points only accept 2D or 3D")
		for i in range(0, len(args)):
			if type(args[i]) != int:
				raise Exception("Point only takes in integers as arguments")
		 
		self.x = args[0]
		self.y = args[1]
		
		if(len(args) == 3):
			self.z = args[2]
		else:
			self.z = None
	
	#Conversion functions for other functions that do not take in Point objects
	def toTuple(self):
		return tuple((self.x, self.y)) if self.z == None else tuple((self.x, self.y, self.z))
	
	def toList(self):
		return list((self.x, self.y)) if self.z == None else list((self.x, self.y, self.z))
	
	#Enables equivalence checking (i.e. == and != comparison of Point objects)
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y and self.z == other.z
	
	def __ne__(self, other):
		return not self.__eq__(other)
	
	#Enables human readable object representation
	def __str__(self):
		pos = tuple((self.x, self.y, self.z)) if self.z != None else tuple((self.x, self.y))
		return str(pos)

	def __repr__(self):
		return str(self)



'''
	Class:
		Waypoint
	
	Description:
		A Waypoint is a user defined location that has a name and a position
	
	Notes:
		
'''
class Waypoint:
	def __init__(self, *args):
		'''
		@param name: Waypoint name (optional)
		@param position: Waypoint position defined by either a Point object,
						tuple, or seperate numbers
		'''
		if (args == ()):
			raise Exception("Waypoint takes at least 1 argument\n")
		
		#Set the waypoint's name
		self.name = ("", args[0])[type(args[0]) == str]
		
		#Create position index and dim count
		i = (0, 1)[type(args[0]) == str]
		dim = len(args[i:] if type(args[i]) == int else args[i].toTuple())
		
		#Exception handling			
		if (type(args[0]) == str or type(args[i]) == int or type(args[i]) == tuple):
			if (dim < 2 or dim > 3):
				raise Exception("Waypoints must be defined by at least 2D or 3D coordinates\n")
		
		if (type(args[i]) != int) and (type(args[i]) != Point) and (type(args[i]) != tuple):
			raise Exception("Waypoints only take a Point, tuple or integers for position\n")

		if type(args[i]) == Point:
			self.position = args[i]
		else:
			#Convert coordinate input to list
			pos = list(args[i:] if type(args[i]) == int else args[i])
			self.position = Point(pos[0], pos[1]) if dim == 2 else Point(pos[0], pos[1], pos[2])


	
	#Enables equivalence checking (i.e. == and != comparison of Waypoint objects)
	def __eq__(self, other):
		return self.name == other.name and self.position.__eq__(other.position)
	
	def __ne__(self, other):
		return not self.__eq__(other)
	
	#Enables human readable object representation
	def __str__(self):
		waypoint = self.name + " | " + str(self.position)
		return str(waypoint)
		
	def __repr__(self):
		return str(self)



'''
	Class:
		POI
		
	Description:
		A POI is a Waypoint with a name and location type taken from a standardized
		database, (i.e. Starbucks/Tim's - Coffee Shop, St. George station - Subway 
		Station are POIs)
	
	Notes:
		
'''
class POI(Waypoint):
	def __init__(self, name, place, *args):
		'''
		@param name: POI name (from super, cannot be empty string)
		@param place: Type of place the POI is
		@param *args: Takes in variable number fo arguments for position (passed to super)
		'''
		#Exception handling
		eCount = 0
		eMsg = 'Need to fix:\n'
		if (name == '' or type(name) != str):
			eCount += 1
			eMsg += str(eCount) + (". POIs must have a non-empty name of type str\n")
		if (type(place) != Place or place.pType == ''):
			eCount += 1
			eMsg += str(eCount) + (". POIs must have a valid, non-null, location of type Place\n")
		if eCount > 0:
			eCount = 0
			raise Exception(eMsg)
		
		Waypoint.__init__(self, name, *args)
		self.location = place
	
	#Enables equivalence checking (i.e. == and != comparison of POI objects)	
	def __eq__(self, other):
		return self.location == other.location and Waypoint.__eq__(self, other)
	
	def __ne__(self, other):
		return not self.__eq__(other)

	#Enables human readable object representation
	def __str__(self):
		poi = str(self.location.pType) + " | " + str(self.name) + " | " + str(self.position)
		return str(poi)
		
	def __repr__(self):
		return str(self)



'''
	Class:
		Place
		
	Description:
		Formalizes what a place is into an object. It currently contains a 
		type, code, and description, but can be later extended to include other 
		information.
	
	Notes:
		
'''
class Place:
	def __init__(self, pType, pCode, pDesc=''):
		'''
		@param pType: The type of the place (Coffee Shope, Library, etc.)
		@param code: Single letter code for place type used for map representation
		@param description: Generic description of place type (Optional)
		'''
		self.pType = pType
		self.pCode = pCode
		self.pDesc = pDesc
	
	#Enables equivalence checking (i.e. == and != comparison of Place objects)
	def __eq__(self, other):
		return self.pType == other.pType and \
		self.pDesc == other.pDesc and \
		self.pCode == other.pCode
		
	def __ne__(self, other):
		return not self.__eq__(other)
	
	
	def __hash__(self):
		return hash((self.pType, self.pCode, self.pDesc))
	
	#Enables human readable object representation
	def __str__(self):
		return self.pType
	
	def __repr__(self):
		return str(self)


		
'''
	Class:
		Node
	
	Description:
		Node is a container for a user defined path that contains location types
		the user wants to visit along with a possible configuration of coordinates
		where those location types are on a map.
	
	Notes:
		1 - Nodes should be created using the Database as it will contain all
		data relating a location type with all possible positions where that 
		location type is found on the map.
		
		2 - Node will be mutated by the simulated annealing algo by either 
		swaping locations' indices or changing the coordinate position of 
		the location.  
		
'''
class Node:
	def __init__(self, pois):
		'''
		@param pois: A list of POIS
		@param map_states: A list of map states from the waypoint search
		@param score: A score for the arrangement of the path
		'''
		self.pois = pois
		self.map_states = [] # Initialize as empty
		self.score = float('inf')
	
	def types(self):
		return [poi.location.pType for poi in self.pois]
	
	def coords(self):
		return [poi.position.toTuple() for poi in self.pois]
	
	def codes(self):
		return [poi.location.pCode for poi in self.pois]
	
	#Enables equivalence checking (i.e. == and != comparison of Node objects)
	def __eq__(self, other):
		return self.pois == other.pois and \
				self.score == other.score
	
	def __ne__(self, other):
		return not self.__eq__(other)
	
	#Enables human readable object representation
	def __str__(self):
		return "POIs: " + str(self.pois) + \
				"\nPlace Types: " + str([poi.location.pType for poi in self.pois]) + \
				"\nPlace Names: " + str([poi.name for poi in self.pois]) + \
				"\nPlace Coord: " + str([poi.position for poi in self.pois]) + \
				"\nPath Score: " + str(self.score)
	
	def __repr__(self):
		 return str(self)



'''
	Class:
		Constraint
	
	Description:
		A binary constraint for position of Place types in a node with an
		immediate flag to indicate whether or not a location type must be
		immediately or loosely before another location type
	
	Notes:
		
'''
class Constraint:
	def __init__(self, name, var1, var2, immediate = False):
		self.name = name
		self.var1 = var1
		self.var2 = var2
		self.immediate = immediate
	
	def getScope(self):
		return list(self.var1, self.var2)
	
	def getConstraintStrength(self):
		return "Strong" if self.immediate else "Weak"
	
	#Enables equivalence checking (i.e. == and != comparison of Node objects)
	def __eq__(self, other):
		return self.name == other.name and \
				self.var1 == other.var1 and \
				self.var2 == other.var2 and \
				self.immediate == other.immediate
	
	def __ne__(self, other):
		return not self.__eq__(other)
	
	#Enables human readable object representation
	def __str__(self):
		return "{" + str(self.var1) + ("}=={" if self.immediate else "}--{") + str(self.var2) + "}"
	
	def __repr__(self):
		return str(self)


'''
	Class:
		CSP
	
	Description:
		Container for all constraints
	
	Notes:
		Again using Borg since we only want a single CSP for the current map and db
		
'''
class CSP:
	_cons = []
	def __init__(self, name):
		self.cons = self._cons
	
	def addConstraint(self, con):
		self.cons.append(con)
	
	def getAllConstraints(self):
		return self.cons
	
	def _dropCSP(self):
		while self.cons != []:
			del self.cons[0]
		self._cons = []


