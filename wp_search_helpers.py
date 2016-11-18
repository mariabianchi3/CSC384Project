# Script File: wp_search_helpers.py
#
# A collection of helper functions for the search aspect of this assignment


####################################
#			 Imports			   #
####################################
from search import *
from wp_search import *
import numpy as np
import sys
import copy

####################################
#		   Heuristics			   #
####################################
def heur_manhattan_dist(state):
	return np.sum(np.absolute(np.subtract(state.cur_start, state.cur_end)))
	
####################################
#		   A* Helpers			   #
####################################
def fval_function(node, weight):
	g = node.gval  # The "cost-to-come"
	h = node.hval  # Estmated "cost-to-go" from heuristic function
	
	# Return a weighted f-value
	return (1-weight)*g + weight*h 
	
####################################
#		Waypoint Search			   #
####################################
def waypoint_search(initial_state, node):
	score = 0
	
	se = SearchEngine('astar', 'full')
	se.trace_on(0)	
	timebound = 1
	
	initial_state_copy = copy.deepcopy(initial_state)
	
	# Make new copy of location tuples
	POI = copy.deepcopy(node.positions)
	
	# Add the global start and goal locations to the list
	POI.insert(0, initial_state.global_start)
	POI.append(initial_state.global_end)
	
	for start, end in zip(POI[0:len(POI)-1], POI[1:len(POI)]):
		initial_state_copy.cur_start = start
		initial_state_copy.cur_end = end
		
		attempt = se.search(initial_state_copy, waypoint_map_goal_state, heur_manhattan_dist, timebound)
		attempt.global_start = initial_state_copy.global_start
		attempt.global_end = initial_state_copy.global_end
		
		if attempt:
			attempt.print_full_path()
			score += attempt.gval
		else:
			return 1000
		
	return score

