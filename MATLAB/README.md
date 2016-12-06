Hello fellow human, 

You have stumbled across the README.md for the MATLAB subfolder! Fancy that!

The files here have been used exclusively for post-processing and thus may not be of much interest
to you.

a) plot_T50_results.m: plots a graph showing the dependence of bad successor state acceptance
probability with initial temperaure. Relies on the data file 'T50_results.txt' which is written by
'maindriver.py' if the analysis is performed.

b) simulated_annealing_sandbox.m: just some code where I was playing around with some of the
simulated annealing parameters to investigate what they did to the search. 

The 'Experiments' subfolder contains the data from each experiment run by 'maindriver' in further
subfolders named by the experiment run time. In here there is a single file:
'plot_experiment_results.m' which just processes the data of a specified experiment folder and 
produces all the relevant figures. 
