import copy
import random
import poi_base
import poiDB
import numpy as np

#Mutates the node to either a type 1 or type 2 mutation based on p
def randomMutation(table,node, p):
	#Force node to be of type node
	if type(node) != Node:
		raise Exception("node must be of type Node")
	
	#Initialize mutations
	m1_node = copy.deepcopy(node)
	m2_node = copy.deepcopy(node)
	
	#TYPE 1 MUTATION
	#TODO(SLatychev): What happens when someone wants to just visit one and only one location
	#along their path from start to goal.
	#Get 2 random indices
	ind_swap = random.sample(0, len(list(node.lType)) - 1, 2)
	#Swap the node's location types
	m1_node.lType[ind_swap[0]], m1_node.lType[ind_swap[1]] = \
	m1_node.lType[ind_swap[1]], m1_node.lType[ind_swap[0]]
	#Swap the node's location positions
	m1_node.lPos[ind_swap[0]], m1_node.lPos[ind_swap[1]] = \
	m1_node.lPos[ind_swap[1]], m1_node.lPos[ind_swap[0]]
	
	
	#TYPE 2 MUTATION
	poi_waypoints = [0]
	possibleChoices = list(range(0, len(m2_node.lType)))
	while len(poi_waypoints) < 2 or possibleChoices != []:
		ind_mod = random.choice(possibleChoices)
		poi_waypoints = table.data[m2_node[ind_mod]]
		if len(poi_waypoints) < 2:
			possibleChoices = list(set(possibleChoices) - set(list(ind_mod)))
	
	if possibleChoice != []:
		poi_waypoints.remove(m2_node[ind_mod])
		ind_replace = random.randint(0, len(poi_waypoints)-1) if (len(poi_waypoints) > 1) else 0
		m2_node[ind_mod] = poi_waypoints[ind_replace]
	else:
		raise Exception("No possible mutations")
	
	mutations = list(m1_node, m2_node)
	probabilities = list(p, 1-p)
	
	return np.random.choice(mutations, 1, probabilities)
