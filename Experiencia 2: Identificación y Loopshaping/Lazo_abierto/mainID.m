%% ID
% Previo a este archivo se debe ejecutar el módulo de rutina_ID.m desde un PC Windows
% rutina_ID;
clear all; close all; clc;
set(0, 'DefaultFigureWindowStyle', 'docked');

% Entrada 0
load('workspaceID.mat');

figure;
plot(t_0(2:end), salida_0(2:end), 'LineWidth', 2, 'Color', rand(1,3));
set(gca, 'FontSize', 20);
% title('Respuesta a entrada 0', 'FontSize', 45, 'Interpreter', 'latex');
grid();
xlabel('$t$', 'Interpreter', 'latex', 'FontSize', 30);
t = text(0.01, 0.37,sprintf('Media: %f', mean(salida_0(2:end))));
set(t, 'FontSize', 15);
t = text(0.01, 0.34, sprintf('D. Std: %f', std(salida_0(2:end))));
set(t, 'FontSize', 15);


% Escalones de diferente magnitud
figure;
k = 1;
for i = fix(1:(length(salidas_diff_mag)-1)/7:length(salidas_diff_mag))
    subplot(2,4,k); k = k + 1;
    plot(salidas_diff_mag{i}(2:end, 1), salidas_diff_mag{i}(2:end, 2), 'LineWidth', 3, 'Color', rand(1,3));
    set(gca, 'FontSize', 15);
    % title(sprintf('Magnitud: %6.3f', entradas_diff_mag{i}(1,2)), 'FontSize', 25, 'Interpreter', 'latex');
    grid();
    xlabel('$t$', 'Interpreter', 'latex', 'FontSize', 17);
    ylim([-30, 30]);
end
% l = suptitle('Respuesta a entrada escalones');
% set(l, 'FontSize', 40, 'Interpreter', 'latex');

% sinusoides de diferente magnitud y freq
mag = 0.1:49.9/39:50;
freqs = 1:249/59:250;
for m = [3, 5]%:15
    figure;
    i = 1;
    for f = [3, 4, 5, 7, 10, 12, 15, 20]
        subplot(2,4,i); i = i + 1;
        k = (m-1)*60 + f;
        plot(salidas_diff_cos{k}(2:end, 1), salidas_diff_cos{k}(2:end, 2), 'LineWidth', 3, 'Color', rand(1,3));
        set(gca, 'FontSize', 15);
        % title(sprintf('Freq: %5.3f', freqs(f)), 'FontSize', 25, 'Interpreter', 'latex');
        grid();
        xlabel('$t$', 'Interpreter', 'latex', 'FontSize', 15);
        ylim([-30, 30]);
    end
    % l = suptitle(sprintf('Respuesta a cos de magnitud: %6.3f', mag(m)));
    % set(l, 'FontSize', 40, 'Interpreter', 'latex');
end

procesamiento_psbr;
save_all_figures('./', 'Lazo_abierto_');
