import copy
import random
import numpy as np

from poi_base import *
from poiDB import *
from wp_search import *
from wp_search_helpers import *

# Perform search with simulated annealing.
# TODO: Make sure user inputs make sense / we have all that we want
def searchSimulatedAnnealing(wp_map, init_node, iter_max):

	###########################################################
	# Step 1: Initialize all algorithm specific parameters    #
	###########################################################
	
	# TODO: We need to decide which of these are user controlled, and which 
	#       we fix. 
	mutation_type_prob = 0.5 # Equal probability of both mutations occuring
	# This is a probability in (0,100). Closer to 100 corresponds to a "hotter"
	# initial temperature, while closer to 0 corresponds to a "colder" initial
	# temperature
	# TODO: Explain the math behind this better
	temp_shape_param = 50
	T_0 = - np.mean((wp_map.width, wp_map.height)) / np.log(temp_shape_param / 100)
	
	###########################################################
	# Step 2: Initialize saved information + file output      #
	###########################################################
	best_node = copy.deepcopy(init_node)
	best_score, best_steps = waypoint_search(wp_map, best_node) # Need to load it with a score
	
	parent_node = copy.deepcopy(init_node)
	target = open('MATLAB/simulated_annealing_output.txt', 'w') #TODO: How to integrate this? 
	
	###########################################################
	# Step 3: Iterate iter_max times and perform search       #
	###########################################################
	for i in range(0, iter_max):
		# Current temperature
		# TODO: Should this be a user defined function passed in? 
		#       Problem with this is that it needs to go to zero at iter_max
		#       So I'm not too sure if it's a smart idea to let the user play 
		#       with this...
		T_cur = T_0 * (1 - i/iter_max) # Currently straight-line decrease
		
		# Now mutate the parent node
		child_node = randomMutation(wp_map.table, parent_node, mutation_type_prob)
		
		# TODO: Add constraint checking portion!!!
		
		# Calculate energies
		# TODO: Perhaps this function isn't really aptly named. Change? 
		#       Also we can probably move these assignments to be inside the 
		#       function, correct?
		parent_energy, parent_map_states = waypoint_search(wp_map, parent_node)
		parent_node.score = parent_energy
		parent_node.map_states = parent_map_states
		
		child_energy, child_map_states = waypoint_search(wp_map, child_node)
		child_node.score = child_energy
		child_node.map_states = child_map_states
		
		delta_E = parent_energy - child_energy
				
		# Calculate acceptance probabilities
		if delta_E > 0: # Child is better, accept
			p_accept = 1.0
		else: # Child is worse, accept with probability e^(DeltaE/T)
			p_accept = np.exp( delta_E / T_cur )
			
		# Update parent_node appropriately
		parent_node = np.random.choice([child_node, parent_node], 1, False, [p_accept, 1-p_accept])[0]
		
		# Save best parent_node so far
		if parent_node.score < best_node.score:
			best_node = copy.deepcopy(parent_node)
			
		# Log information to file
		output_data = [i, T_cur, delta_E, p_accept, parent_node.score, best_node.score]
		str_out = '\t'.join(map(str, output_data)) + '\n' 
		target.write(str_out)
		
	# Algorithm is complete. Return best node found so far
	print("\n================ DONE!!! =======================\n")
	
	wp_map.print_state()
	
	print(best_node)
	
	print('\n')
	
	for state in best_node.map_states:
		state.print_full_path()
		
	return best_node
		
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

			#Swap the node's pois
			m1_node.pois[ind_swap[0]], m1_node.pois[ind_swap[1]] = \
			m1_node.pois[ind_swap[1]], m1_node.pois[ind_swap[0]]
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
	else:
		raise Exception("No possible mutations")
	
	return m2_node



#Makes a Node object from a user specified path and the appropriate table in the database
def makeNode(table, locationTypePath):
	nodePOIs = [table.data[poi_type.code][0] for poi_type in locationTypePath]
	newNode = Node(nodePOIs)
	
	return newNode


#Generate a list of Location objects without descriptions
def generateLocationTypes(typeList):
	listOfLocs = []
	for locationType in typeList:
		listOfLocs.append(Location(locationType, locationType[0]))
	return listOfLocs

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
	
	init_node = makeNode(table, [L, C, A])
	
	init_node.score, init_path = waypoint_search(wp_map, init_node) 
	
	'''
	print("Initial Node")
	print("===========================================================")
	print(init_node)
	print("\nType 1 Mutated Node")
	print("===========================================================")
	print(randomMutation(table, init_node, 1))
	print("\nType 2 Mutated Node")
	print("===========================================================")
	print(randomMutation(table, init_node, 0))
	'''
	
	#print("\nSimulated Annealing Test Run")	
	#print("===========================================================")
	searchSimulatedAnnealing(wp_map, init_node, 200)
	
	
