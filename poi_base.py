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
	
	'''Enables equivalence checking (i.e. == and != comparison of Point objects)'''
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y and self.z == other.z
	
	def __ne__(self, other):
		return not self.__eq__(self, other)
	
	''' Enables human readable object representation '''
	def __str__(self):
		pos = (self.x, self.y, self.z) if self.z != None else (self.x, self.y)
		return str(pos)

	def __repr__(self):
		pos = (self.x, self.y, self.z) if self.z != None else (self.x, self.y)
		return str(pos)



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
		dim = len(args[i:] if type(args[i]) == int else args[i])
		
		#Exception handling			
		if (type(args[0]) == str or type(args[i]) == int or type(args[i]) == tuple):
			if (dim < 2 or dim > 3):
				raise Exception("Waypoints must be defined by at least 2D or 3D coordinates\n")
		
		if (type(args[i]) != int) and (type(args[i]) != Point) and (type(args[i]) != tuple):
			raise Exception("Waypoints only take a Point, tuple or integers for position\n")
		
		#Allow for multiple types of input(Point, tuple, or seperate numbers)

		if type(args[i]) == Point:
			self.position = args[i]
		else:
			#Convert coordinate input to list
			pos = list(args[i:] if type(args[i]) == int else args[i])
			self.position = Point(pos[0], pos[1]) if dim == 2 else Point(pos[0], pos[1], pos[2]) 
	
	'''Enables equivalence checking (i.e. == and != comparison of Waypoint objects)'''
	def __eq__(self, other):
		return self.name == other.name and self.position.__eq__(self, other)
	
	def __ne__(self, other):
		return not self.__eq__(self, other)
	
	''' Enables human readable object representation '''
	def __str__(self):
		Waypoint = self.name + " | " + str(self.position)
		return Waypoint
		
	def __repr__(self):
		Waypoint = self.name + " | " + str(self.position)
		return Waypoint



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
	def __init__(self, name, location, *args):
		'''
		@param name: POI name (from super, cannot be empty string)
		@param position: POI (x,y,z) coordinates (from super)
		@param locationType: Type of location the POI is
		'''
		#Exception handling
		eCount = 0
		eMsg = 'Need to fix:\n'
		if (name == '' or type(name) != str):
			eCount += 1
			eMsg += str(eCount) + (". POIs must have a non-empty name of type str\n")
		if (type(location) != Location or location.lType == ''):
			eCount += 1
			eMsg += str(eCount) + (". POIs must have a valid, non-null, location of type Location\n")
		if eCount > 0:
			eCount = 0
			raise Exception(eMsg)
		
		Waypoint.__init__(self, name, *args)
		#TODO(SLatychev): Need to add location type checking so that this class 
		#is consistent description: "... taken from a standardized database..."
		self.location = location
	
	'''Enables equivalence checking (i.e. == and != comparison of POI objects)'''	
	def __eq__(self, other):
		return self.location == other.location and Waypoint.__eq__(self, other)
	
	def __ne__(self, other):
		return not self.__eq__(self, other)

	''' Enables human readable object representation '''
	def __str__(self):
		poi = self.name + " | " + str(self.location) + " | " + str(self.position)
		return poi
		
	def __repr__(self):
		poi = self.name + " | " + str(self.location) + " | " + str(self.position)
		return poi



'''
	Class:
		Location
		
	Description:
		Formalizes what a location is into an object. It currently contains a 
		type and description, but can be later extended to include other 
		information.
	
	Notes:
		
'''
class Location:
	def __init__(self, lType, desc=''):
		'''
		@param lType: The type of the location (Coffee Shope, Library, etc.)
		@param description: Generic description of location type (Optional)
		'''
		self.lType = lType
		self.description = desc
		
	''' Enables equivalence checking (i.e. == and != comparison of Location objects)'''
	def __eq__(self, other):
		return self.lType == other.lType and self.description == other.description
		
	def __ne__(self, other):
		return not self.__eq__(self, other)
	
	''' Enables human readable object representation '''
	def __str__(self):
		return self.lType
	
	def __repr__(self):
		return self.lType + "\n" + self.description


		
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
	def __init__(self, lType, lPos):
		'''
		@param lType: A list containing Location types
		@param lPos: A list containing the Location types' positions
		@param score: A score for the arrangement of the path
		'''
		self.lType = lType
		self.lPos = lPos
		self.score = -1
	
	''' Enables equivalence checking (i.e. == and != comparison of Node objects)'''
	def __eq__(self, other):
		return self.lType == other.lType and \
				self.lPos == other.lPos and \
				self.score == other.score
	
	def __ne__(self, other):
		return not self.__eq__(self, other)
	
	''' Enables human readable object representation '''
	def __str__(self):
		return "Location Order: " + str(self.lType) + \
				"\nLocation Coordinates: " + str(self.lPos) + \
				"\nPath Score: " + str(self.score)
	
	def __repr__(self):
		 return "Location Order: " + str(self.lType) + \
				"\nLocation Coordinates: " + str(self.lPos) + \
				"\nPath Score: " + str(self.score)



