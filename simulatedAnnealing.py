import copy
import random
import itertools
import numpy as np

from poi_base import *
from poiDB import *
from wp_search import *
from wp_search_helpers import *
from NameGenerator import *

# Perform search with simulated annealing.
# TODO: Make sure user inputs make sense / we have all that we want
def searchSimulatedAnnealing(wp_map, init_node, iter_max):

	###########################################################
	# Step 1: Initialize all algorithm specific parameters	#
	###########################################################
	
	# TODO: We need to decide which of these are user controlled, and which 
	#	   we fix. 
	mutation_type_prob = 0.5 # Equal probability of both mutations occuring
	# This is a probability in (0,100). Closer to 100 corresponds to a "hotter"
	# initial temperature, while closer to 0 corresponds to a "colder" initial
	# temperature
	# TODO: Explain the math behind this better
	temp_shape_param = 80
	T_0 = - np.mean((wp_map.width, wp_map.height)) / np.log(temp_shape_param / 100)
	
	###########################################################
	# Step 2: Initialize saved information + file output	  #
	###########################################################
	best_node = copy.deepcopy(init_node)
	best_score, best_steps = waypoint_search(wp_map, best_node) # Need to load it with a score
	
	parent_node = copy.deepcopy(init_node)
	target = open('MATLAB/simulated_annealing_output.txt', 'w') #TODO: How to integrate this? 
	
	###########################################################
	# Step 3: Iterate iter_max times and perform search	   #
	###########################################################
	for i in range(0, iter_max):
		# Current temperature
		# TODO: Should this be a user defined function passed in? 
		#	   Problem with this is that it needs to go to zero at iter_max
		#	   So I'm not too sure if it's a smart idea to let the user play 
		#	   with this...
		T_cur = T_0 * (1 - i/iter_max) # Currently straight-line decrease
		
		# Now mutate the parent node
		child_node = randomMutation(wp_map.table, parent_node, mutation_type_prob)
		
		# TODO: Add constraint checking portion!!!
		
		# Calculate energies
		# TODO: Perhaps this function isn't really aptly named. Change? 
		#	   Also we can probably move these assignments to be inside the 
		#	   function, correct?
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

# Brute force searchd
def searchBruteForce(table, wp_map, types = None):
	
	# First grab all of the keys
	if not types:
		types = list(table.data.keys())
	else: types = [i.pCode for i in types]
	
	best_node = Node([])
	
	for type_order in itertools.permutations(types, len(types)):
		wp_array = []
		for wp_type in type_order:
			wp_array.append(table.data[wp_type])
		
		wp_combinations = list(itertools.product(*wp_array))
		
		for test_wp in wp_combinations:
			node = Node(list(test_wp))
			
			node_energy, node_states = waypoint_search(wp_map, node)
			node.score = node_energy
			node.map_states = node_states
			
			print(node.score)
			
			if node.score < best_node.score:
				best_node = copy.deepcopy(node)
		
	print(best_node)

		
#Choose which mutation to apply to the node with a weighted probability p (type1 = p, type2 = 1-p)
def randomMutation(table, node, p = 0.5):
	if type(node) != Node:
		raise Exception("node must be of type Node")
	
	mut_node = None
	isType1 = np.random.choice([True, False], 1, False, [p, 1-p])[0]
	if isType1:
		m1_node = copy.deepcopy(node)
		mut_node = type1Mutation(table, m1_node, False)
	else:
		m2_node = copy.deepcopy(node)
		mut_node = type2Mutation(table, m2_node, False)
	
	return mut_node

#Type 1: Randomly select 2 of the node's elements and swap their order
def type1Mutation(table, m1_node, calledFromOtherMutation):
	#Allow swaps to happen only if there is more than 1 element to swap
	if len(m1_node.pois) > 1:
		ind_swap = random.sample(range(0, len(list(m1_node.pois))), 2)
		
		#Allow the swap only if the two chosen elements don't share the same position
		if m1_node.pois[ind_swap[0]].position != m1_node.pois[ind_swap[1]].position:

			#Swap the node's pois
			m1_node.pois[ind_swap[0]], m1_node.pois[ind_swap[1]] = \
			m1_node.pois[ind_swap[1]], m1_node.pois[ind_swap[0]]
		else:
			#raise Exception("Chosen positions for swapping have the same position")
			#print("COULD NOT FULFILL MUTATION PASSING TO TYPE 2!! (INNER)")
			return type2Mutation(table, m1_node, True)
	elif calledFromOtherMutation:
		raise Exception("No possible mutations")
	else:
		#print("COULD NOT FULFILL MUTATION PASSING TO TYPE 2!! (OUTER)")
		return type2Mutation(table, m1_node, True)
	
	return m1_node

#Type 2: Randomly select one of the node's elements and change it to an element of equal type
def type2Mutation(table, m2_node, calledFromOtherMutation):
	#Initialize dummy poi list and a list of indices for pois that are non-unique
	poi_list = [0]
	possibleChoices = list(range(0, len(m2_node.pois)))
	
	#Attempt to choose an index that gives
	while len(poi_list) < 2 and possibleChoices != []:
		ind_mod = random.choice(possibleChoices)
		poi_list = copy.deepcopy(table.data[m2_node.pois[ind_mod].location.pCode])
		
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
	elif calledFromOtherMutation:
		raise Exception("No possible mutations")
	else:
		#print("COULD NOT FULFILL MUTATION PASSING TO TYPE 1!!")
		return type1Mutation(table, m2_node, True)
	
	return m2_node

#Makes a Node object from a user specified path and the appropriate table in the database
def makeNode(table, pCodePath):
	pois = []
	#Go through all the path codes
	for pCode in pCodePath:
		#Ensure we don't add a duplicate POI to the path
		i = 0
		while i < len(table.data[pCode]) and table.data[pCode][i] in pois:
			i += 1
		#If we've exhausted all pois with key pCode then don't add the poi
		if i >= len(table.data[pCode]):
			continue
		else:
			pois.append(table.data[pCode][i])
			
			
	#nodePOIs = [table.data[pCode][0] for pCode in pCodePath]
	nodePOIs = pois
	newNode = Node(nodePOIs)
	
	return newNode

###############################################################################
#	TEST AUTOMATION															  #
###############################################################################

#Generate random place types
def generateRandomPlaceTypes(numOfTypes):
	placeTypes = []
	for i in range(0, numOfTypes):
		placeTypes.append(generateRandomName(-1, True))
	return placeTypes



#Generate a list of random location names
def generateRandomLocationNames(numOfNames):
	locationNames = []
	for i in range(0, numOfNames):
		locationNames.append(generateRandomName(-1, False, True))
	return locationNames



#Generate a list of Place objects without descriptions from input list of strings
def generatePlaces(placeStrings):
	listOfPlaces = []
	for placeType in placeStrings:
		#Make the place code the first letter of the placeType string
		listOfPlaces.append(Place(placeType, placeType[0]))
	return listOfPlaces



#Generate a list of Location objects
def generateLocations(placeList, listOfNames):
	listOfLocations = []
	for name in listOfNames:
		place = random.randrange(0, len(placeList))
		listOfLocations.append(Location(name, placeList[place]))
	return listOfLocations


#Build a Place table where key isPlace object, and values are associated Location objects
def buildPlaceTable(db, locationList):
	db.createTable("Places", "Place", ["Place", "Location"])
	placeTable = db.tables["Places"]
	
	for location in locationList:
		placeTable.addValToKey(Place(location.pType, location.pCode, location.pDesc), location)
	

#Generate a list of POI objects from a placeTable
def generateRandomPOIs(placeTable, numOfPOIs, mapSize):
	i = 0
	pois = []
	usedPositions = []
	while i < numOfPOIs:
		x = y = None
		place = None
		name = None
		pos = None
		while (x == None and y == None) or pos in usedPositions:
			x = random.randrange(0, mapSize)
			y = random.randrange(0, mapSize)
			pos = Point(x, y)
		
		usedPositions.append(pos)
		
		while place is None:
			place = random.choice(list(placeTable.data.keys()))
			location = random.choice(list(placeTable.data[place]))
		
		pois.append(POI(location, pos))
		i += 1
	#print(pois)
	#print(usedPositions)
	#print(set(pois))
	return list(set(pois)) 



#Build the POI Table from a list of POIs
def buildPOITable(db, poiList):
	db.createTable("poiTab", "Location Code", ["Location Code", "POI"])
	poiTab = db.tables["poiTab"]
	for poi in poiList:
		poiTab.addValToKey(poi.location.pCode, poi)



#Randomly generate a path: list of location types
def generateRandomPath(DB, poiTable):
	print("IN PATH GENERATION")
	print(poiTable)
	locTypes = list(poiTable.data.keys())
	print("ALL LOCATION TYPES: " + str(locTypes))
	numOfLocs = random.randrange(2, len(locTypes))
	
	path = []
	for loc in range(0, numOfLocs):
		locIndx = random.randrange(0, len(locTypes))
		print(locTypes[locIndx])
		path.append(locTypes[locIndx])
	return path




if __name__ == "__main__":
	#Build DB
	DB = Database()
	
	#Make random place types
	placeTypes = generateRandomPlaceTypes(10)
	
	#From random place types, make list of Place objects
	places = generatePlaces(placeTypes)
	
	
	#Make random location names
	locationNames = generateRandomLocationNames(20)
	
	#From random location names, make list of Location objects
	locations = generateLocations(places, locationNames)
	
	#Build the place Table
	buildPlaceTable(DB, locations)
	
	
	#Now that the place table has been created, make random POIS
	placeTable = DB.tables["Places"]
	pois = generateRandomPOIs(placeTable, 10, 10)
	
	#Build the POI Table
	buildPOITable(DB, pois)
	
	#Build a random path of location types for node creation
	poiTable = DB.tables["poiTab"]
	#print(DB)
	path = generateRandomPath(DB, poiTable)
	print("PATH: " + str(path))
	
	#Build Map and Node
	wp_map = WaypointMapState("START", 0, None, 10, 10, # Dimensions
					 (0,0), # Initial Position 
					 (9,9), # Desired Position 
					 poiTable, # Dict of POI... Needs thinking about...
					 #frozenset(((2,4),(3,3))) # Obstacles
					 frozenset(())
					)
	
	init_node = makeNode(poiTable, path)
	
	init_node.score, init_path = waypoint_search(wp_map, init_node)
	
	'''
	#Build all place TYPES
	A = Place("ATM", "A")
	C = Place("Coffee", "C")
	L = Place("Library", "L")
	
	
	#Create Places table and populate it, used for random poi generation
	DB.createTable("Places", "Place", ["Place", "Name"])
	DB.tables["Places"].addValToKey(A, "BMO")
	DB.tables["Places"].addValToKey(A, "RBC")
	DB.tables["Places"].addValToKey(C, "Starbucks")
	DB.tables["Places"].addValToKey(C, "Tim's")
	DB.tables["Places"].addValToKey(C, "Second Cup")
	DB.tables["Places"].addValToKey(L, "Robarts")
	

	#Build all Places
	A = Place("ATM", "A")
	C = Place("Coffee", "C")
	L = Place("Library", "L")
	H = Place("HotDog", "H")
	
	#Build a few Locations
	RBC = Location("RBC", A)
	BMO = Location("BMO", A)
	Starbucks = Location("Starbucks", C)
	Tims = Location("Tims", C)
	SecondCup = Location("Second Cup", C)
	Robarts = Location("Robarts", L)
	H = Location("HOTDOG", H)
	
	#Create Places table and populate it, used for random poi generation
	DB.createTable("Places", "Place", ["Place", "Location"])
	DB.tables["Places"].addValToKey(A, BMO)
	DB.tables["Places"].addValToKey(A, RBC)
	DB.tables["Places"].addValToKey(C, Starbucks)
	DB.tables["Places"].addValToKey(C, Tims)
	DB.tables["Places"].addValToKey(C, SecondCup)
	DB.tables["Places"].addValToKey(L, Robarts)
	
	
	#Build all locations
	A1 = POI(BMO, Point(1,3))
	A2 = POI(RBC, Point(5,7))
	A3 = POI(RBC, Point(15,2))
	A4 = POI(RBC, Point(6,28))
	A5 = POI(RBC, Point(12,18))
	A6 = POI(RBC, Point(4,22))
	C1 = POI(Starbucks, Point(2,8))
	C2 = POI(Tims, Point(9,9))
	C3 = POI(Tims, Point(9,10))
	C4 = POI(Tims, Point(14,13))
	C5 = POI(Tims, Point(0,2))
	C6 = POI(Tims, Point(22,5))
	C7 = POI(Tims, Point(21,28))
	C8 = POI(Tims, Point(3,7))
	C9 = POI(Tims, Point(5,9))
	C10 = POI(Tims, Point(9,12))
	C11 = POI(Tims, Point(9,25))
	C12 = POI(Tims, Point(15,8))
	C13 = POI(Tims, Point(29,0))
	L1 = POI(Robarts, Point(3,10))
	L2 = POI(Robarts, Point(11,19))
	L3 = POI(Robarts, Point(2,2))
	L4 = POI(Robarts, Point(1,18))
	L5 = POI(Robarts, Point(15,15))
	L6 = POI(Robarts, Point(14,14))
	L7 = POI(Robarts, Point(12,7))
	H1 = POI(H, Point(25, 23))
	H2 = POI(H, Point(1, 1))
	H3 = POI(H, Point(5, 23))
	H4 = POI(H, Point(29, 23))
	H5 = POI(H, Point(14, 2))
	H6 = POI(H, Point(18, 26))
	H7 = POI(H, Point(26, 18))
	H8 = POI(H, Point(1, 29))
	H9 = POI(H, Point(29, 1))
	H10 = POI(H, Point(24, 29))
	
	
	
	#Create POI table and populate it
	DB.createTable("poiTab", "Type", ["Type", "POI"])
	DB.tables["poiTab"].addValToKey(A.pCode, A1)
	DB.tables["poiTab"].addValToKey(A.pCode, A2)
	DB.tables["poiTab"].addValToKey(A.pCode, A3)
	DB.tables["poiTab"].addValToKey(A.pCode, A4)
	DB.tables["poiTab"].addValToKey(A.pCode, A5)
	DB.tables["poiTab"].addValToKey(A.pCode, A6)
	DB.tables["poiTab"].addValToKey(C.pCode, C1)
	DB.tables["poiTab"].addValToKey(C.pCode, C2)
	DB.tables["poiTab"].addValToKey(C.pCode, C3)
	DB.tables["poiTab"].addValToKey(C.pCode, C4)
	DB.tables["poiTab"].addValToKey(C.pCode, C5)
	DB.tables["poiTab"].addValToKey(C.pCode, C6)
	DB.tables["poiTab"].addValToKey(C.pCode, C7)
	DB.tables["poiTab"].addValToKey(C.pCode, C8)
	DB.tables["poiTab"].addValToKey(C.pCode, C9)
	DB.tables["poiTab"].addValToKey(C.pCode, C10)
	DB.tables["poiTab"].addValToKey(C.pCode, C11)
	DB.tables["poiTab"].addValToKey(C.pCode, C12)
	DB.tables["poiTab"].addValToKey(L.pCode, L1)
	DB.tables["poiTab"].addValToKey(L.pCode, L2)
	DB.tables["poiTab"].addValToKey(L.pCode, L3)
	DB.tables["poiTab"].addValToKey(L.pCode, L4)
	DB.tables["poiTab"].addValToKey(L.pCode, L5)
	DB.tables["poiTab"].addValToKey(L.pCode, L6)
	DB.tables["poiTab"].addValToKey(L.pCode, L7)
	DB.tables["poiTab"].addValToKey(H.pCode, H1)
	DB.tables["poiTab"].addValToKey(H.pCode, H2)
	DB.tables["poiTab"].addValToKey(H.pCode, H3)
	DB.tables["poiTab"].addValToKey(H.pCode, H4)
	DB.tables["poiTab"].addValToKey(H.pCode, H5)
	DB.tables["poiTab"].addValToKey(H.pCode, H6)
	DB.tables["poiTab"].addValToKey(H.pCode, H7)
	DB.tables["poiTab"].addValToKey(H.pCode, H8)
	DB.tables["poiTab"].addValToKey(H.pCode, H9)
	DB.tables["poiTab"].addValToKey(H.pCode, H10)
	
	
	wp_map = WaypointMapState("START", 0, None, 30, 30, # Dimensions
					 (0,0), # Initial Position 
					 (29,29), # Desired Position 
					 DB.tables["poiTab"], # Dict of POI... Needs thinking about...
					 #frozenset(((2,4),(3,3))) # Obstacles
					 frozenset(())
					)

	table = DB.tables["poiTab"]

	#wp_map.print_state()
	
	init_node = makeNode(table, [L, C, A, H])
	
	init_node.score, init_path = waypoint_search(wp_map, init_node) 
	
	
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
	searchSimulatedAnnealing(wp_map, init_node, 500)
	
	#print("\nDatabase Visualization")
	#print("======================================================")
	#print(DB)
	#print("\nRandomized POI Auto-generation")
	#print("======================================================")
	#print(generateRandomPOIs(DB.tables["Places"], 1, 1000))

	#searchBruteForce(table, wp_map, [H, C, L])
