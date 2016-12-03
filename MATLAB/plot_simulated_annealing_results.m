% Script File: plot_simulated_annealing_results.m

%% Clean Up
close all;
clear all; 
clc;

%% Read in data
results = importdata('simulated_annealing_output.txt');

% This is currently really hacky. Maybe we can write to a struct in python?
% Or write a header line and parse based on those strings...
iterations = results(:,1); % Column 1 is iteration number
temperature = results(:,2); % Column 2 is temperature
delta_E = results(:,3); % Column 3 is energy difference
p_accept = 100*results(:,4); % Column 4 is acceptance probability
cur_score = results(:,5); % Column 5 is score of current node in search
best_score = results(:,6); % Column 6 is best score of all time

%% Plot Results
figure; hold on; grid; 
plot(iterations, p_accept, 'mo', 'MarkerSize', 5, 'MarkerFaceColor', 'm');
xlabel('Iteration Number');
ylabel('Acceptance Probability [%]');
title('Simulated Annealing Cooling Behaviour');

figure; hold on; grid;
plot(iterations, cur_score, 'b-');
plot(iterations, best_score, 'r-');
xlabel('Iteration Number');
ylabel('Node Score');
title('Simulated Annealing Nodal Scores with Time');
legend('Current Algorithm Score', 'Best Score', 'Location', 'Best');

