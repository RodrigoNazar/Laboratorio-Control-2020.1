%% Rutina de ID 
% Lab de control 2020-1 
% Mile - Rodri - Mathi

clear; clc;
set(0, 'DefaultFigureWindowStyle', 'docked');
open_system('BlackBox');
Ts = 0.0005;
t = 0:Ts:1;
%% 1. Entrada 0 
entrada_0 = [t', 0*t'];
[t_0, ~, salida_0] = sim('BlackBox', t(end), [], entrada_0);

figure;
plot(t_0, salida_0, 'LineWidth', 3, 'Color', rand(1,3));
title('Respuesta a entrada 0', 'FontSize', 34, 'Interpreter', 'latex');


%% 2. Escalones de diferentes magnitudes 

salidas_diff_mag = {};
entradas_diff_mag = {};
k = 1;
tic;
for i = -6:12/399:6
    entrada = [t', i*ones(size(t'))];
    [to, ~, aux] = sim('BlackBox', t(end), [], entrada);
    salidas_diff_mag{k} = [to, aux];
    entradas_diff_mag{k} = entrada;
    k = k + 1;
end
toc;
%% 3. sinusoides de magnitudes  y frecuencia diferentes
        figure;
salidas_diff_cos = {};
entradas_diff_cos = {};
k = 1;
tic;
for m = 0.1%:49.9/39:50
    for f = 1:249/59:250
        entrada = [t', m*cos(2*pi*f*t')];
%         [to, ~, aux] = sim('BlackBox', t(end), [], entrada);
        salidas_diff_cos{k} = [to, aux];
        entradas_diff_cos{k} = entrada;
        k = k + 1;  
        plot(t', m*cos(2*pi*f*t'));
        pause(0.5);
    end 
end
toc;

%% 4. PRBS
clear; clc;
set(0, 'DefaultFigureWindowStyle', 'docked');
open_system('BlackBox');

N = 2^16-1;
P = 20;
Ts = 0.0005;

PRBS = idinput([N, 1, P], 'prbs');
L2 = length(PRBS);
t2 = (0:L2-1)'*Ts;
entrada_prbs = [t2, PRBS];
tic;
[t_prbs, ~, salida_prbs] = sim('BlackBox', t2(end), [], entrada_prbs);
toc;
disp('Done master');


