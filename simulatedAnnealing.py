import copy
import random
import numpy as np

from poi_base import *
from poiDB import *
from wp_search import *
from wp_search_helpers import *

#Choose which mutation to apply to the node with a weighted probability p (type1 = p, type2 = 1-p)
def randomMutation(table, node, p = 0.5):
	if type(node) != Node:
		raise Exception("node must be of type Node")
	
	mut_node = None
	isType1 = np.random.choice([True, False], 1, False, [p, 1-p])[0]
	if isType1:
		m1_node = copy.deepcopy(node)
		mut_node = type1Mutation(m1_node)
	else:
		m2_node = copy.deepcopy(node)
		mut_node = type2Mutation(table, m2_node)
	
	return mut_node
	
#Type 1: Randomly select 2 of the node's elements and swap their order
def type1Mutation(m1_node):
	#Allow swaps to happen only if there is more than 1 element to swap
	if len(m1_node.pois) > 1:
		ind_swap = random.sample(range(0, len(list(m1_node.pois))), 2)
		
		#Allow the swap only if the two chosen elements don't share the same position
		if m1_node.pois[ind_swap[0]].position != m1_node.pois[ind_swap[1]].position:
			#NOTE(ALL): This is indicative that node is not a well built class
			#			We should consider dropping locations and positions
			#			and just using the poi as it already contains all this
			#			information
			#			We would only need to swap pois if we reduced node to just
			#			being a container of pois with a score

			#Swap the node's pois
			m1_node.pois[ind_swap[0]], m1_node.pois[ind_swap[1]] = \
			m1_node.pois[ind_swap[1]], m1_node.pois[ind_swap[0]]
			
			#NOTE(ALL): Depricated
			#Swap the node's location types
			#m1_node.locations[ind_swap[0]], m1_node.locations[ind_swap[1]] = \
			#m1_node.locations[ind_swap[1]], m1_node.locations[ind_swap[0]]

			#Swap the node's location positions
			#m1_node.positions[ind_swap[0]], m1_node.positions[ind_swap[1]] = \
			#m1_node.positions[ind_swap[1]], m1_node.positions[ind_swap[0]]
		else:
			raise Exception("Chosen positions for swapping have the same position")
	else:
		raise Exception("No possible mutations")
	
	return m1_node

#Type 2: Randomly select one of the node's elements and change it to an element of equal type
def type2Mutation(table, m2_node):	
	#Initialize dummy poi list and a list of indices for pois that are non-unique
	poi_list = [0]
	possibleChoices = list(range(0, len(m2_node.pois)))
	
	#Attempt to choose an index that gives
	while len(poi_list) < 2 and possibleChoices != []:
		ind_mod = random.choice(possibleChoices)
		poi_list = copy.deepcopy(table.data[m2_node.pois[ind_mod].location.code])
		
		#If a poi is unique remove its node index from being a possible choice
		if len(poi_list) < 2:
			possibleChoices = list(set(possibleChoices) - set([ind_mod]))
	
	#Only change the poi if it is non-unique
	if possibleChoices != []:
		#Remove the current poi from the list of available pois and choose a random one's index
		poi_list.remove(m2_node.pois[ind_mod])
		ind_replace = random.randint(0, len(poi_list)-1) if (len(poi_list) > 1) else 0
		
		#Change all the data of the old element to the newly selected element
		m2_node.pois[ind_mod] = poi_list[ind_replace]
		
		#NOTE(ALL): Depricated
		#m2_node.locations = [poi.location.lType for poi in m2_node.pois]
		#m2_node.positions = [poi.position.toTuple() for poi in m2_node.pois]
	else:
		raise Exception("No possible mutations")
	
	return m2_node



#Makes a Node object from a user specified path and the appropriate table in the database
def makeNode(table, locationTypePath):
	nodePOIs = [table.data[poi_type.code][0] for poi_type in locationTypePath]
	newNode = Node(nodePOIs)
	
	#NOTE(ALL): Depricated
	#nodeTypes, nodePoses,
	#nodePoses = [poi.position.toTuple() for poi in nodePOIs]
	#nodeTypes = locationTypePath
	
	return newNode


if __name__ == "__main__":
	#Build DB
	DB = Database()
	
	#Build all location TYPES
	A = Location("ATM", "A")
	C = Location("Coffee", "C")
	L = Location("Library", "L")
	
	#Build all locations
	A1 = POI("BMO", A, Point(1,3))
	A2 = POI("RBC", A, Point(5,7))
	C1 = POI("Starbucks", C, Point(2,8))
	C2 = POI("Tims", C, Point(9,9))
	C3 = POI("Second Cup", C, Point(2,2))
	L1 = POI("Robarts", L, Point(5,5))
	
	DB.createTable("poiTab", "Type", ["Type", "POI"])
	DB.tables["poiTab"].addValToKey(A.code, A1)
	DB.tables["poiTab"].addValToKey(A.code, A2)
	DB.tables["poiTab"].addValToKey(C.code, C1)
	DB.tables["poiTab"].addValToKey(C.code, C2)
	DB.tables["poiTab"].addValToKey(C.code, C3)
	DB.tables["poiTab"].addValToKey(L.code, L1)
	
	wp_map = WaypointMapState("START", 0, None, 10, 10, # Dimensions
					 (0,0), # Initial Position 
					 (6,9), # Desired Position 
					 DB.tables["poiTab"], # Dict of POI... Needs thinking about...
					 #frozenset(((2,4),(3,3))) # Obstacles
					 frozenset(())
					)

	table = DB.tables["poiTab"]

	wp_map.print_state()
	
	init_node = makeNode(table, [A, C])
	
	init_node.score = waypoint_search(wp_map, init_node) 
	
	print("Initial Node")
	print("===========================================================")
	print(init_node)
	print("\nType 1 Mutated Node")
	print("===========================================================")
	print(randomMutation(table, init_node, 1))
	print("\nType 2 Mutated Node")
	print("===========================================================")
	print(randomMutation(table, init_node, 0))
