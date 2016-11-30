% Script File: plot_T50_results.m

%% Clean Up
close all;
clear all; 
clc;

%% Read in data
results = importdata('T50_results.txt');

T = results(:,1);
p_ave = results(:,2);
p_std = results(:,3);

h = errorbar(T, p_ave, p_std); hold on; grid on;
set(h, 'LineStyle', 'none', 'Marker', 'o', 'MarkerFaceColor', 'r', 'MarkerSize', 5);
plot([T(1) T(end)],[0.5 0.5], '-.m');

xlabel('Initial Temperature - T0');
ylabel('Acceptance Probability of Bad Child State - [%]');
title(sprintf(['Acceptance Probability of Bad Child State\n' ...
               'with Initial Temperature T0']));