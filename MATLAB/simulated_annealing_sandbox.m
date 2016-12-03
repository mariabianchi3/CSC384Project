% Script File: simulated_annealing_sandbox.m
close all
clear all
clc

% Just investigating some probability shape functions and their behaviour

n = 30;
i_m = 1000;
iter = 1:1:(i_m-1);

T0 = linspace(50, 400, 3);

figure; hold on; grid;
legendInfo = {};

for j = 1:length(T0)
    p = 100*exp(-n ./ (T0(j) * (1 - iter/i_m)));
    plot(iter, p);
    legendInfo{j} = ['T0 = ' num2str(T0(j))];
end

xlabel('Iteration Number');
ylabel('Probability');
title('Cooling Function');
legend(legendInfo, 'Location', 'Best');

% For a given grid size and number of iterations we may want to choose T0
% in order to have a certain starting probability. Keep in mind of course
% that in reality 'n' isn't constant. The numerator actually represents
% the difference in energies, so there will be noise in this graph.
% And on certain iterations delta_E may be greater than zero, so this
% probability is 100% automatically. Let's try and simulate this...

n = 30;
i_m = 1000;
iter = 1:1:(i_m-1);

T0 = linspace(50, 400, 3);

figure; hold on; grid;
legendInfo = {};

for j = 1:length(T0)
    for i = 1:length(iter)
        
        delta_E = randi([-n n], 1, 1); % not necessarily actual probability distribution
        if delta_E >= 0
            p(i) = 100;
        else
            p(i) = 100*exp(delta_E / (T0(j) * (1 - iter(i)/i_m)));
        end
    end
    plot(iter, p, '.');
    legendInfo{j} = ['T0 = ' num2str(T0(j))];
end

xlabel('Iteration Number');
ylabel('Probability');
title('Cooling Function');
legend(legendInfo, 'Location', 'Best');
