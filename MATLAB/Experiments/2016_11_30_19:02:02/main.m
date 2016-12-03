close all
clear all
clc

grey_val = 200;

data = load('score_matrix_c_0.95.txt');
data = data'; % transpose so that mean and std works

dims = size(data);

iters = 0:1:(dims(2)-1);
data_mean = mean(data, 1); % mean along column
data_std = std(data);

up = data_mean + data_std;
down = data_mean - data_std;

ITERS = [iters fliplr(iters)];
UP = [data_mean fliplr(up)];
DOWN = [data_mean fliplr(down)];

h = figure; hold on; grid;
fill(ITERS, UP, [grey_val grey_val grey_val]/255);
fill(ITERS, DOWN, [grey_val grey_val grey_val]/255);
plot(iters, up, 'b', 'LineWidth', 1);
plot(iters, down, 'r', 'LineWidth', 1);
plot(iters, data_mean, 'k', 'LineWidth', 1);



xlabel('Iteration Number');