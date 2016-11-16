###############################################################################
''' 
	Basic class definitions that will be used in the Waypoint search project
'''
###############################################################################

'''
	(x, y, z) point in space
'''
class Point:
	def __init__(self, *args):
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
	A Waypoint is a user defined location
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
	A POI is a Waypoint with a name and location type taken from a standardized
	database, (i.e. Starbucks/Tim's - Coffee Shop, St. George station - Subway 
	Station are POIs)
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
		if (type(location) != Location or location.locType == ''):
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


class Location:
	def __init__(self, locType, desc=''):
		self.locType = locType
		self.description = desc
		
	''' Enables equivalence checking (i.e. == and != comparison of Location objects)'''
	def __eq__(self, other):
		return self.locType == other.locType and self.description == other.description
		
	def __ne__(self, other):
		return not self.__eq__(self, other)
		
	def __str__(self):
		return self.locType
	
	def __repr__(self):
		return self.locType + "\n" + self.description

#TODO(SLatychev): Decide on the following:
#	a) 	Do we want to build a Path class, that will store particular Waypoints along a path
#			-This may reduce the difficulty of the search algorithm by allowing the creation and
#			storage of an explicit Path object that can store a set of Waypoints, pathScore, and
#			other relevant information.
#
#			-This may also minimize csp use to just checking location
#			type constraints 
#				=> CSP will simply keep as variables the location types, and the 
#				constraints between them, once an appropriate ordering of location types has been 
#				built we build a path of actual waypoints based on the search algorithm, then can 
#				do some fancy things with the path object
#				=> cspbase needs no code modifications at all
#
#		NOTE(SLatychev): Changing this to Node class
#							-LocationTypes
#							-LocationPositions
#							-NodeScore
#						=>A Node will be created when the user specifies a list
#							of location types they want to visit
#						=>Mutation alg will then modify the Initial and subsequently
#							mutated nodes
#						=>Node score will be determined later by the search
#		
#	b)	Do we want to build a Database class, that can organize waypoints and perform
#		specialized functions on them and on the database of them like:
#			-Extract all Waypoints of type blah
#			-Extract all Waypoints of type blah with name bleh
#			-Extract all Waypoints that have non unique positions (i.e. find me a mall)
#		
#		NOTE(SLatychev): Database built, need to build function for non-unique position extraction
#
#
#


