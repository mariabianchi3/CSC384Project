close all;
clear all;
clc;

folder = '2016_12_01_12:37:09';

%folder = '2016_12_01_12:37:09'; REALLY GOOD RESULTS!

directory = dir(folder);

% Initialize arrays for simulation data
c_vals = [];
c_scores_mean = [];
c_scores_std = [];
c_times_mean = [];
c_times_std = [];

for i = 3:length(directory)
    file = directory(i);
    file_name = file.name;
    file_name_split = strsplit(file_name, '_');
    
    % Handle score matrix files!
    if strcmp(file_name_split(1), 'score')
        grey_val = 200;

        data = load([folder '/' file_name]);
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
        xlabel('Iteration Number','FontSize',15);
        ylabel('Score','FontSize',15);
        c_str = char(file_name_split(end));
        c_str = c_str(1:end-4);
        title(['Convergence Trend for c = ' c_str],'FontSize',18);
                
        % Save out convergence figure
        saveas(gcf, [folder '/SA_convergence_c_' c_str '.pdf']);
        pause(0.1)
        %close all;
    end
    
    % Now handle loading runtime stat files
    if strcmp(file_name_split(1), 'run')
        c_str = char(file_name_split(end));
        c_str = c_str(1:end-4); % Strip '.txt' extension
        c_num = str2double(c_str);

        data = load([folder '/' file_name]);
        data_mean = mean(data);
        data_std = std(data);
        
        c_vals = [c_vals c_num];
        c_scores_mean = [c_scores_mean data_mean(1)];
        c_scores_std = [c_scores_std data_std(1)];
        c_times_mean = [c_times_mean data_mean(2)];
        c_times_std = [c_times_std data_std(2)];
    end
end

f = figure; hold on; grid;
fe = errorbar(c_times_mean, c_scores_mean, c_scores_std);
set(fe, 'LineStyle', 'none', 'Marker', 'o', 'MarkerFaceColor', 'r', 'MarkerSize', 5);

fh = herrorbar(c_times_mean, c_scores_mean, c_times_std);
set(fh(2), 'LineStyle', 'none');

for i = 1:length(c_vals)
    text(c_times_mean(i),c_scores_mean(i),sprintf('c = %0.2f',c_vals(i)), ...
        'HorizontalAlignment', 'left', ...
        'VerticalAlignment', 'bottom');
end

xlabel('Experiment Run Time - [s]','FontSize',15);
ylabel('Average Returned Path Length','FontSize',15);
title('SA Path Length with Algorithm Runtime','FontSize',18);

saveas(gcf, [folder '/runtime_data_c.pdf']);