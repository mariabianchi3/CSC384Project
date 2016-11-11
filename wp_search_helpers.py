# Script File: wp_search_helpers.py
#
# A collection of helper functions for the search aspect of this assignment


####################################
#             Imports              #
####################################
from search import *
from wp_search import WaypointMapState, Direction, PROBLEMS, waypoint_map_goal_state
import numpy as np
import sys
import copy

####################################
#           Heuristics             #
####################################
def heur_manhattan_dist(state):
    return np.sum(np.absolute(np.subtract(state.cur_pos, state.des_pos)))
    
####################################
#           A* Helpers             #
####################################
def fval_function(node, weight):
    g = node.gval  # The "cost-to-come"
    h = node.hval  # Estmated "cost-to-go" from heuristic function
    
    # Return a weighted f-value
    return (1-weight)*g + weight*h 
    
####################################
#        Waypoint Search           #
####################################
def waypoint_search(initial_state, POI):
    score = 0
    
    se = SearchEngine('astar', 'full')
    se.trace_on(0)    
    timebound = 1
    
    initial_state_copy = copy.deepcopy(initial_state)
    
    for start, end in zip(POI[0:len(POI)-1], POI[1:len(POI)]):
        initial_state_copy.cur_pos = start
        initial_state_copy.des_pos = end
        
        attempt = se.search(initial_state_copy, waypoint_map_goal_state, heur_manhattan_dist, timebound)
                
        if attempt:
            attempt.print_full_path()
            score += attempt.gval
        else:
            return 1000
        
    return score

if __name__ == "__main__":
    
    # Just some testing code

    timebound = 1
    
    s0 = PROBLEMS[1]
    se = SearchEngine('astar', 'full')
    se.trace_on(0)

    final = se.search(s0, waypoint_map_goal_state, heur_manhattan_dist, timebound)
    
    if final:
        print("Solution Found!")
        final.print_full_path()
    else:
        print(final)
        print("No Solution Found!")
  
    print('----------------------')
    
    POI = [(0,0),(0,5),(3,2),(5,5)]
    
    score = waypoint_search(s0, POI)
    print(score)
