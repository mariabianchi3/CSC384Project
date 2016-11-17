import copy
import random
import numpy as np

from poi_base import *
from poiDB import *
from wp_search import *

#Mutates the node to either a type 1 with probability p and type 2 with probability 1-p
def randomMutation(table,node, p = 0.5):
	#Force node to be of type node
	if type(node) != Node:
		raise Exception("node must be of type Node")
	
	#Initialize mutations
	m1_node = copy.deepcopy(node)
	m2_node = copy.deepcopy(node)
	#TODO(Anyone): Don't need to run both functions, find a cleaner way of implementing the following
	m1_node = type1Mutation(m1_node)
	m2_node = type2Mutation(m2_node)
	
	#Choose which mutated node by weighted randomization of p
	mutations = list(m1_node, m2_node)
	probabilities = list(p, 1-p)
	return np.random.choice(mutations, 1, probabilities)
	
#TYPE 1 MUTATION
def type1Mutation(m1_node):
	#TODO(SLatychev): What happens when someone wants to just visit one and only one location
	#along their path from start to goal.
	
	#Mutate as long as there are more than one waypoint in the path
	if len(m1_node.lType) > 1:
		#Get 2 random indices
		ind_swap = random.sample(range(0, len(list(m1_node.lType)) - 1), 2)
		if m1_node.lPos[ind_swap[0]] != m1_node.lPod[ind_swap[1]]:
			#Swap the node's location types
			m1_node.lType[ind_swap[0]], m1_node.lType[ind_swap[1]] = \
			m1_node.lType[ind_swap[1]], m1_node.lType[ind_swap[0]]
	
			#Swap the node's location positions
			m1_node.lPos[ind_swap[0]], m1_node.lPos[ind_swap[1]] = \
			m1_node.lPos[ind_swap[1]], m1_node.lPos[ind_swap[0]]
		else:
			raise Exception("Chosen positions for swapping have the same position")
	else:
		raise Exception("No possible mutations")
		
	return m1_node

#TYPE 2 MUTATION
def type2Mutation(table, m2_node):	
	#Initialize dummy waypoints list and list of valid location type indices
	poi_waypoints = [0]
	possibleChoices = list(range(0, len(m2_node.lType)))
	
	#Randomly select a location type that has more than one possible location position
	while len(poi_waypoints) < 2 or possibleChoices != []:
		ind_mod = random.choice(possibleChoices)
		poi_waypoints = table.data[m2_node[ind_mod]]
		#Remove location type indices that have only 1 possible location position
		if len(poi_waypoints) < 2:
			possibleChoices = list(set(possibleChoices) - set(list(ind_mod)))
	
	if possibleChoice != []:
		poi_waypoints.remove(m2_node[ind_mod])
		ind_replace = random.randint(0, len(poi_waypoints)-1) if (len(poi_waypoints) > 1) else 0
		m2_node[ind_mod] = poi_waypoints[ind_replace]
	else:
		raise Exception("No possible mutations")
	
	return m2_node



#Makes a Node object from a user specified path and the appropriate table in the database
def makeNode(table, locationTypePath):
	nodeTypes = locationTypePath
	nodePoses = [table.data[poi_type][0] for poi_type in nodeTypes]
	newNode = Node(nodeTypes, nodePoses)
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
	
	wp_map = WaypointMapState("START", 0, None, 5, 5, # Dimensions
                     (0,0), # Initial Position 
                     (4,4), # Desired Position 
                     DB.tables["poiTab"], # Dict of POI... Needs thinking about...
                     frozenset(((2,4),(3,3))) # Obstacles
                    )
