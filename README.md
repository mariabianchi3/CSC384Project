# CSC384Project

All of our Python files are located in the 'src' folder.

A minimum functioning example of the Simulated Annealing algorithm search optimizing the POI
ordering for a specific map can be found in the executable: 'maindriver.py'

To run, cd into 'src' and execute the command: python3 maindriver.py

NOTE: Ensure that the terminal window is fully maximized. 
      There is an outstanding bug with the progress bar printing which 
      occurs if the progress bar is wider than the terminal window. 

The following is a list of our Python files and a description of what they contain

maindriver.py
- Builds the database, contraints and the map we used for the project
- Additionally this file can run a T_50 analysis, a brute force search for the optimal solution, and
  multiple tests for different cooling schedule parameters and logs the convergence data. 
- By default, the T_50 analysis and brute force search are skipped. To have 'maindriver.py' 
  run these tests, enable the boolean flags on lines 168 and 182 respectively. 

poiDB.py
- Contains Class definitions for our database

poi_base.py
- Contains class definitions for our data stuctures. 
- Includes, Point class, Waypoint class, POI class, Place class, Location class, Node class, Contraint class and ConstraintSet class.
  Please see report for details on classes.

search.py
- Contains class and function definitions nessesary to run a search.
- This file has been borrowed from Assignment 1

simulatedAnnealing.py
- Contains function definitions needed to perform simulated annealing related methods

visualizationHelpers.py
- Contains function definitions for visualizing our algorithm progress

wp_search.py
- Contains class definitions needed to perform Waypoint search

wp_search_helpers.py
- Contains helper functions for waypoint search
