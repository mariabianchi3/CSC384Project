# CSC384Project

## Project Overview

This is the repo for our Fall 2016 [CSC384] Final Project!

We are interested in addressing the problem of constrained waypoint path
optimization. Given a map with an initial and goal position, along with sets of
waypoints, we are interested in finding the optimal ordering in which to visit
the waypoints of interest that results in the shortest overall path. There may
also exist constraints on the order in which certain waypoints must be visited. 

A simple example may be as follows. Say we want to walk from the Bahen Centre to
Queen's park subway station, and along the way we want to stop at an ATM to
withdraw money, a coffee shop to buy a drink, and a library to pick up a book.
And we have the constraint that we want to visit the ATM _before_ the coffee
shop so that we can have cash to purchase the drink. There may exist multiple ATM's, 
coffee shops, and libraries that we can visit, so the question is which ATM,
coffee shop, and library do we choose (from their respective sets) and in what
order do we visit them? 

It is immediately obvious that some solutions simply violate the constraints: 

Start -> Coffee Shop -> ATM -> Library -> End

But others may not: 

Start -> ATM -> Coffee Shop -> Library -> End
Start -> ATM -> Library -> Coffee Shop -> End

Additionally, the presence of multiple options (in a spatial sense) for each
waypoint adds another dimension of complexity to the problem! Which is better? 

Start -> ATM(1) -> Coffee Shop -> Library -> End
Start -> ATM(2) -> Coffee Shop -> Library -> End


