#####################################################
#                     Imports                       #
#####################################################
from simulatedAnnealing import *
from poi_base import *
from poiDB import *
from wp_search import *
from wp_search_helpers import *
from NameGenerator import *
from visualization_helpers import *

import sys
import numpy as np

###########################
#     1: Build DB         #
###########################

DB = Database()
table_name = "poiTab"
DB.createTable(table_name, "Type", ["Place", "Location"])

table = DB.tables[table_name]	
	
# Location types
A = Location('ATM', 'ATM', 'A')
C = Location('Coffee', 'Coffee', 'C')
L = Location('Library', 'Library', 'L')
H = Location('Hotdog', 'Hotdog', 'H')

# Build all locations
A1 = POI(A, Point(1,3))
A2 = POI(A, Point(5,7))
A3 = POI(A, Point(15,2))
A4 = POI(A, Point(6,28))
A5 = POI(A, Point(12,18))
A6 = POI(A, Point(4,22))
C1 = POI(C, Point(2,8))
C2 = POI(C, Point(9,9))
C3 = POI(C, Point(9,10))
C4 = POI(C, Point(14,13))
C5 = POI(C, Point(0,2))
C6 = POI(C, Point(22,5))
C7 = POI(C, Point(21,28))
C8 = POI(C, Point(3,7))
C9 = POI(C, Point(5,9))
C10 = POI(C, Point(9,12))
C11 = POI(C, Point(9,25))
C12 = POI(C, Point(15,8))
C13 = POI(C, Point(29,0))
L1 = POI(L, Point(3,10))
L2 = POI(L, Point(11,19))
L3 = POI(L, Point(2,2))
L4 = POI(L, Point(1,18))
L5 = POI(L, Point(15,15))
L6 = POI(L, Point(14,14))
L7 = POI(L, Point(12,7))
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

# Populate table with location data
DB.tables[table_name].addValToKey(A.pCode, A1)
DB.tables[table_name].addValToKey(A.pCode, A2)
DB.tables[table_name].addValToKey(A.pCode, A3)
DB.tables[table_name].addValToKey(A.pCode, A4)
DB.tables[table_name].addValToKey(A.pCode, A5)
DB.tables[table_name].addValToKey(A.pCode, A6)
DB.tables[table_name].addValToKey(C.pCode, C1)
DB.tables[table_name].addValToKey(C.pCode, C2)
DB.tables[table_name].addValToKey(C.pCode, C3)
DB.tables[table_name].addValToKey(C.pCode, C4)
DB.tables[table_name].addValToKey(C.pCode, C5)
DB.tables[table_name].addValToKey(C.pCode, C6)
DB.tables[table_name].addValToKey(C.pCode, C7)
DB.tables[table_name].addValToKey(C.pCode, C8)
DB.tables[table_name].addValToKey(C.pCode, C9)
DB.tables[table_name].addValToKey(C.pCode, C10)
DB.tables[table_name].addValToKey(C.pCode, C11)
DB.tables[table_name].addValToKey(C.pCode, C12)
DB.tables[table_name].addValToKey(L.pCode, L1)
DB.tables[table_name].addValToKey(L.pCode, L2)
DB.tables[table_name].addValToKey(L.pCode, L3)
DB.tables[table_name].addValToKey(L.pCode, L4)
DB.tables[table_name].addValToKey(L.pCode, L5)
DB.tables[table_name].addValToKey(L.pCode, L6)
DB.tables[table_name].addValToKey(L.pCode, L7)
DB.tables[table_name].addValToKey(H.pCode, H1)
DB.tables[table_name].addValToKey(H.pCode, H2)
DB.tables[table_name].addValToKey(H.pCode, H3)
DB.tables[table_name].addValToKey(H.pCode, H4)
DB.tables[table_name].addValToKey(H.pCode, H5)
DB.tables[table_name].addValToKey(H.pCode, H6)
DB.tables[table_name].addValToKey(H.pCode, H7)
DB.tables[table_name].addValToKey(H.pCode, H8)
DB.tables[table_name].addValToKey(H.pCode, H9)
DB.tables[table_name].addValToKey(H.pCode, H10)


###########################
#     2: Constraints      #
###########################
csp = CSP('csp1')

con1 = Constraint('con1', A, C, True) # ATM immediately before Coffee (NEED MONEY!)
csp.addConstraint(con1)
con2 = Constraint('con2', L, C, False) # Library at least before Coffee (can't drink in library)
csp.addConstraint(con2)


###########################
#     3: Obstacles        #
###########################

# Generate obstacles for the map
obs_list = []

# Donald Trump's Great Wall	
wall_y = 21
for i in range(0,21):
	obs_list.append((i,wall_y))

wall_x = 20
for i in range(1,21):
	obs_list.append((wall_x,i))

obs_list = tuple(obs_list)

###########################
#    4: WaypointMap       #
###########################
wp_map = WaypointMapState("START", 0, None, 30, 30, # Dimensions
							(0,0), # Initial Position 
							(29,29), # Desired Position 
							DB.tables[table_name], # Table
							frozenset( obs_list ), # Obstacles
							)

# Print the initial map
wp_map.print_state()

###########################
#    4: Find T_50         #
###########################

# Before running the SA algorithm, we need to come up with 
# some value for the initial temperature T_0. Based on the word of my 
# structural mechanics professor (Prasanth Nair), we want to choose
# T_0 such that the probability of accepting a bad solution is about 
# 50%. 

# To find this value (which will be HIGHLY problem specific) we will simply 
# test a range of different initial temperatures and roughly calculate the 
# rejection probability after performing a large number of trials. 
search_poi_codes = [A.pCode, H.pCode, L.pCode, C.pCode]
test_T50 = False

# Remember that T_50 is Map and Table specific! 
if test_T50:
	T_test = list(np.arange(5,40,1))
	iters = 10
	T_50 = findT50(table, wp_map, T_test, search_poi_codes, iters)
else: T_50 = 24 # Found from previous experiments


init_node = makeNode(table, search_poi_codes)
init_node.score, init_path = waypoint_search(wp_map, init_node) 


#print("\nSimulated Annealing Test Run")	
#print("===========================================================")
best_node = searchSimulatedAnnealing(wp_map, init_node, csp, T_50, 1000)

print(best_node)

#searchBruteForce(table, wp_map, [H, C, L])
