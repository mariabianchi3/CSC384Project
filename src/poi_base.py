import numpy as np

###############################################################################
''' 
	Basic class definitions that will be used in the Waypoint search project
	
	Classes:
		Point			(ln 29)
		Waypoint		(ln 88)
		POI				(ln 151)
		Place			(ln 209)
		Location		(ln 259)
		Node			(ln 313)
		Constraint		(ln 370)
		ConstraintSet	(ln 421)
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
		:param x: x coordinate
		:param y: y coordinate
		:param z: z coordinate
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
	
	#Conversion functions for processes that do not understand Point objects
	def toTuple(self):
		return tuple((self.x, self.y)) if self.z == None else tuple((self.x, self.y, self.z))
	
	def toList(self):
		return list((self.x, self.y)) if self.z == None else list((self.x, self.y, self.z))
	
	#Enables equivalence checking (i.e. == and != comparison of Point objects)
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y and self.z == other.z
	
	def __ne__(self, other):
		return not self.__eq__(other)
	
	def __hash__(self):
		return hash((self.x, self.y, self.z))
	
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
				raise Exception("Waypoints must be defined by either 2D or 3D coordinates\n")
		
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
	def __init__(self, location, *args):
		'''
		@param name: POI name is either user specified or defaulted to the location name 
		@param location: POI location, containing standardized name, type, code, and description
		@param *args: Takes in variable number of arguments for user defined name and position
		'''
		#Exception handling
		eCount = 0
		eMsg = 'Need to fix:\n'
		if (type(location) != Location):
			eCount += 1
			eMsg += str(eCount) + (". POIs must have a valid, non-null, location of type Location\n")
		if eCount > 0:
			eCount = 0
			raise Exception(eMsg)
		
		Waypoint.__init__(self, *args)
		if self.name == '':
			self.name = location.name
		self.location = location
	
	#Enables equivalence checking (i.e. == and != comparison of POI objects)	
	def __eq__(self, other):
		return self.location == other.location and Waypoint.__eq__(self, other)
	
	def __ne__(self, other):
		return not self.__eq__(other)
	
	def __hash__(self):
		return hash((self.name, self.location, self.position))

	#Enables human readable object representation
	def __str__(self):
		poi = str(self.location.pType) + " | " + \
				str(self.location.name) + " | " + \
				str(self.position)
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
		1) Abstraction to Location for more granular control of data (we could
		   define that coffee shops exist, but we may not know which ones
		   specifically, i.e. Starbucks, Tims, etc.)
'''
class Place:
	def __init__(self, pType, pCode, pDesc=''):
		'''
		@param pType: The type of the place (Coffee Shope, Library, etc.)
		@param pCode: Single letter code for place type used for map representation
		@param description: Generic description of place type (Optional)
		'''
		#Ensure everything passed in is of type str
		if type(pType) != str or type(pCode) != str or type(pDesc) != str:
			raise Exception("pType, pCode, and (if provided) pDesc must be of type str")
		
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
		Location
	
	Description:
		A more specific type of location that contains a name. This is class 
		allows more granular control when dealing with any kind of database 
		manipulation or automating POI creation. Used for taking existing places,
		for example a Coffee Shop, and creating all kinds of Coffee Shops like
		Starbucks, Tim's, etc.
	
	Notes:
		
'''
class Location(Place):
	def __init__(self, name, *args):
		'''
		@param name
		@param pType
		@param pCode
		@param pDesc
		'''
		self.name = name
		if len(args) >=2 and len(args) <= 3:
			Place.__init__(self, *args)
		elif len(args) == 1 and type(args[0]) == Place:
			self.pType = args[0].pType
			self.pCode = args[0].pCode
			self.pDesc = args[0].pDesc
		
	#Enables equivalence checking (i.e. == and != comparison of Location objects)
	def __eq__(self, other):
		return self.name == other.name and Place.__eq__(self, other)
	
	def __ne__(self, other):
		return not self.__eq__(other)
	
	def __hash__(self):
		return hash((self.name, self.pType, self.pCode, self.pDesc))
	
	#Enables human readable object representation
	def __str__(self):
		return str(self.pType) + " - " + str(self.name) 
	
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
	
	#Specific bulk parameter retrieval functions
	def names(self):
		return [poi.location.name for poi in self.pois]
	
	def types(self):
		return [poi.location.pType for poi in self.pois]
	
	def codes(self):
		return [poi.location.pCode for poi in self.pois]
	
	def coords(self):
		return [poi.position.toTuple() for poi in self.pois]
	
	#Enables equivalence checking (i.e. == and != comparison of Node objects)
	def __eq__(self, other):
		return self.pois == other.pois and \
				self.score == other.score
	
	def __ne__(self, other):
		return not self.__eq__(other)
	
	#Enables human readable object representation
	def __str__(self):
		return "POIs: " + str(self.pois) + \
				"\nPlace Types: " + str(self.types()) + \
				"\nPlace Names: " + str(self.names()) + \
				"\nPlace Coord: " + str(self.coords()) + \
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
	
	#Specific data retrieval functions
	def getScope(self):
		return list(self.var1, self.var2)
	
	def getConstraintStrength(self):
		return "Strong" if self.immediate else "Weak"
	
	#Checks if locations are in correct order according to constraint
	def isValidNode(self, node):
		locations = [poi.location for poi in node.pois]
		
		var1_ind = locations.index(self.var1)
		var2_ind = locations.index(self.var2)
		
		return (var1_ind < var2_ind and not self.immediate) or (var2_ind-var1_ind == 1 and self.immediate)
	
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
		ConstraintSet
	
	Description:
		Container for all constraints
	
	Notes:
		Again using Borg since we only want a single ConstraintSet for the current map and db
		
'''
class ConstraintSet:
	_cons = []
	def __init__(self, name):
		self.cons = self._cons
	
	#Adds a constraint to the ConstraintSet
	def addConstraint(self, con):
		self.cons.append(con)
	
	#Retrieve all constraints from ConstraintSet
	def getAllConstraints(self):
		return self.cons
	
	# Check a node against all constraints in the ConstraintSet
	def checkAllCons(self, node):
		for con in self.cons:
			if not con.isValidNode(node): return False
		return True
		
	#Wipes out the shared state of the ConstraintSet, used for restarting
	def _dropCSP(self):
		while self.cons != []:
			del self.cons[0]
		self._cons = []


