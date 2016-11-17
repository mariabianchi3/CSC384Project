'''
Waypoint Map routines.

	A) Class WaypointMapState

	A specializion of the StateSpace Class that is tailored for this Waypoint Search Problem.

	B) class Direction

	An encoding of the directions of movement that are possible.
'''

from search import *

class WaypointMapState(StateSpace):

	def __init__(self, action, gval, parent, width, height, cur_pos, des_pos, table, obstacles):
		'''
		Creates a new Waypoint Map state.
		@param width: The map X dimension.
		@param height: The map Y dimension.
		@param cur_pos: a tuple of current x and y position 
		@param des_pos: a tuple of the desired position 
		@param POI: a dictionary of all points of interests
		@param obstacles: A frozenset of all the impassable obstacles.
		'''
		StateSpace.__init__(self, action, gval, parent)
		self.width = width
		self.height = height
		self.cur_pos = cur_pos
		self.des_pos = des_pos
		self.table = table
		self.obstacles = obstacles	

	def successors(self):
		'''
		Generates all the actions that can be performed from this state, and the states those actions will create.		
		'''
		successors = []
		transition_cost = 1

		for direction in (UP, RIGHT, DOWN, LEFT):
			new_location = direction.move(self.cur_pos)
			  
			if new_location[0] < 0 or new_location[0] >= self.width:
				continue
			if new_location[1] < 0 or new_location[1] >= self.height:
				continue
			if new_location in self.obstacles:
				continue
			  
			new_state = WaypointMapState(direction.name, self.gval + transition_cost, self, self.width, self.height, new_location, self.des_pos, self.table, self.obstacles)
			successors.append(new_state)

		return successors

	def hashable_state(self):
		'''Return a data item that can be used as a dictionary key to UNIQUELY represent a state.'''
		return hash(self.cur_pos)	  

	def state_string(self):
		'''Returns a string representation of a state that can be printed to stdout.'''		
		map = []
		# Generate empty indexable map string
		for y in range(0, self.height):
			row = []
			for x in range(0, self.width):
				row += [' ']
			map += [row]
		
		# Write the Points of Interest from the Table
		for key in list(self.table.data.keys()):
			for poi in list(self.table.data[key]):
				tup_pos = poi.position.toTuple()
				map[tup_pos[1]][tup_pos[0]] = key

		# Next the goal
		map[self.des_pos[1]][self.des_pos[0]] = '@'
		
		# And then the current position
		map[self.cur_pos[1]][self.cur_pos[0]] = '*'

		# And of course the obstacles
		for obstacle in self.obstacles:
			map[obstacle[1]][obstacle[0]] = '#'

		# Add border!		
		for y in range(0, self.height):
			map[y] = ['#'] + map[y]
			map[y] = map[y] + ['#']
		map = ['#' * (self.width + 2)] + map
		map = map + ['#' * (self.width + 2)]

		# Convert to characters for printing
		s = ''
		for row in map:
			for char in row:
				s += char
			s += '\n'

		return s		

	def print_state(self):
		'''
		Prints the string representation of the state. ASCII art FTW!
		'''		
		print("ACTION was " + self.action)	  
		print(self.state_string())

	# A cool little subroutine that I wrote! It takes a solved puzzle state
	# and loops backwards through each action that was made to get there, and 
	# updates the ASCII representation to include all the steps taken to 
	# get to the solution (from the start). A little easier on the eyes than 
	# seeing a separate print-out for every single step taken. 
	def full_path_string(self):
		# Initial path string from just before solution
		parent_state = self.parent
		path_str = list(parent_state.state_string())
		
		while parent_state != None:
		
			if parent_state.parent == None:
				map_str = '*'
			elif parent_state.action == UP.name:
				map_str = '^'
			elif parent_state.action == DOWN.name:
				map_str = 'v'
			elif parent_state.action == RIGHT.name:
				map_str = '>'
			elif parent_state.action == LEFT.name:
				map_str = '<'
			else:
				map_str = '~' # This would be weird...
		
			# Write a path marker to the current position of the agent
			cur_pos_ind = parent_state.cur_pos
			ind = (self.width+3)*(cur_pos_ind[1]+1) + (cur_pos_ind[0]+1)
			path_str[ind] = map_str
			
			parent_state = parent_state.parent
				
		return "".join(path_str)		

	def print_full_path(self):
		'''
		Prints the string representation of full path until current state
		'''
		print(self.full_path_string())

def waypoint_map_goal_state(state):
	'''Returns True if we have reached a goal state'''
	'''INPUT: a waypoint_map state'''
	'''OUTPUT: True (if goal) or False (if not)'''  
	return state.cur_pos == state.des_pos
  

'''
Movement Directions: encodes directions of movement that are possible for agent.
'''
class Direction():
	'''
	A direction of movement.
	'''
	
	def __init__(self, name, delta):
		'''
		Creates a new direction.
		@param name: The direction's name.
		@param delta: The coordinate modification needed for moving in the specified direction.
		'''
		self.name = name
		self.delta = delta
	
	def __hash__(self):
		'''
		The hash method must be implemented for actions to be inserted into sets 
		and dictionaries.
		@return: The hash value of the action.
		'''
		return hash(self.name)
	
	def __str__(self):
		'''
		@return: The string representation of this object when *str* is called.
		'''
		return str(self.name)
	
	def __repr__(self):
		return self.__str__()
	
	def move(self, location):
		'''
		@return: Moving from the given location in this direction will result in the returned location.
		'''
		return (location[0] + self.delta[0], location[1] + self.delta[1])

#Global Directions
UP = Direction("up", (0, -1))
RIGHT = Direction("right", (1, 0))
DOWN = Direction("down", (0, 1))
LEFT = Direction("left", (-1, 0))
	
  
