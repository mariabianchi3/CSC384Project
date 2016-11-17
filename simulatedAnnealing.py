import copy
import random
import poi_base
import poiDB
import numpy as np

#Mutates the node to either a type 1 or type 2 mutation based on p
def randomMutation(table,node, p = 0.5):
	#Force node to be of type node
	if type(node) != Node:
		raise Exception("node must be of type Node")
	
	#Initialize mutations
	m1_node = copy.deepcopy(node)
	m2_node = copy.deepcopy(node)
	
	#Choose which mutated node by weighted randomization of p
	mutations = list(m1_node, m2_node)
	probabilities = list(p, 1-p)
	mutation = np.random.choice(mutations, 1, probabilities)
	
	if mutation == m1_node:
		return type1Mutation(m1_node)
	else:
		return type2Mutation(m2_node)
	
#TYPE 1 MUTATION
def type1Mutation(m1_node):
	#TODO(SLatychev): What happens when someone wants to just visit one and only one location
	#along their path from start to goal.
	
	#Mutate as long as there are more than one waypoint in the path
	if len(m1_node.lType) > 1:
		#Get 2 random indices
		ind_swap = random.sample(range(0, len(list(m1_node.lType)) - 1), 2)
	
		#Swap the node's location types
		m1_node.lType[ind_swap[0]], m1_node.lType[ind_swap[1]] = \
		m1_node.lType[ind_swap[1]], m1_node.lType[ind_swap[0]]
	
		#Swap the node's location positions
		m1_node.lPos[ind_swap[0]], m1_node.lPos[ind_swap[1]] = \
		m1_node.lPos[ind_swap[1]], m1_node.lPos[ind_swap[0]]
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



