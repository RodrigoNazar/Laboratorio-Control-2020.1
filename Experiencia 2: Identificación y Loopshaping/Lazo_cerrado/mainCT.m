%% CT
% Previo a este archivo se debe ejecutar el módulo de rutina_ID.m desde un PC Windows
% rutina_CT;
clear all; close all; clc;
set(0, 'DefaultFigureWindowStyle', 'docked');

load('workspaceCT.mat');

% Entrada 0
figure;
plot(t_entrada0(:), y_entrada0(:,1), 'LineWidth', 2, 'Color', rand(1,3));
set(gca, 'FontSize', 20);
% title('Respuesta a entrada 0', 'FontSize', 45, 'Interpreter', 'latex');
grid();
xlabel('$t$', 'Interpreter', 'latex', 'FontSize', 30);
t = text(0.22, 2.8,sprintf('Media: %f', mean(y_entrada0(:,1))));
set(t, 'FontSize', 15);
t = text(0.22, 2.65, sprintf('D. Std: %f', std(y_entrada0(:,1))));
set(t, 'FontSize', 15);

y = salida_prbs(:,1);
u = salida_prbs(1:N,2);

figure;
plot(t2, y, 'LineWidth', 2, 'Color', rand(1,3));
set(gca, 'FontSize', 20);
% title('Salida', 'FontSize', 45, 'Interpreter', 'latex');
grid();
xlabel('$t$', 'Interpreter', 'latex', 'FontSize', 30);
xlim([1 600])

y = detrend(y, 'linear');

figure;
plot(t2, y, 'LineWidth', 2, 'Color', rand(1,3));
set(gca, 'FontSize', 20);
% title('Detrend', 'FontSize', 45, 'Interpreter', 'latex');
grid();
xlabel('$t$', 'Interpreter', 'latex', 'FontSize', 30);
xlim([1 600])

% promedio
y2 = reshape(y, [length(y)/P, P]);
y2 = y2(:,2:end);
y2 = sum(y2, 2) / (P-1);

figure;
plot(t2(1:length(y2)), y2, 'LineWidth', 2, 'Color', rand(1,3));
set(gca, 'FontSize', 20);
% title('Promedio', 'FontSize', 45, 'Interpreter', 'latex');
grid();
xlabel('$t$', 'Interpreter', 'latex', 'FontSize', 30);
xlim([1 32])

% correlacion
uu = mycorr(u, u);
uy = mycorr(u, y2);
yy = mycorr(y2, y2);

% Enventanado
filter = hann(length(uu));
w_uu = uu .* filter;
w_uy = uy .* filter;
w_yy = yy .* filter;

n = 2^nextpow2(length(uu));
W_UU = fft(w_uu, n);
W_UY = fft(w_uy, n);
W_YY = fft(w_yy, n);

f = (1/Ts)*(0:(n/2))/n;
Gw = W_UY ./ (W_UU+eps);


figure;
subplot(211);
semilogx(f, 20* log10( abs(Gw(1:end/2+1))), 'LineWidth', 2, 'Color', rand(1,3));
grid();
xlim([0.5 10^(3)])
set(gca, 'FontSize', 20);
% title('Magnitud $|Gw|$', 'FontSize', 34, 'Interpreter', 'latex');
xlabel('f[$Hz$]', 'FontSize', 20, 'Interpreter', 'latex');
ylabel('Magnitud', 'FontSize', 20, 'Interpreter', 'latex');

subplot(212);
semilogx(f, rad2deg(-phase(Gw(1:end/2+1))), 'LineWidth', 2, 'Color', rand(1,3));
grid();
xlim([0.5 10^(3)])
set(gca, 'FontSize', 20);
% title('Fase $\angle Gw$', 'FontSize', 34, 'Interpreter', 'latex');
xlabel('f[$Hz$]', 'FontSize', 20, 'Interpreter', 'latex');
ylabel('Angulo', 'FontSize', 20, 'Interpreter', 'latex');
% l = suptitle('Diagrama de Bode');
% set(l, 'FontSize', 40, 'Interpreter', 'latex');

D = W_YY - abs(W_UY).^2 ./ (W_UU+eps);
figure;
semilogx(f, abs(D(1:end/2+1)), 'LineWidth', 2, 'Color', rand(1,3));
xlim([1 10^3]);
set(gca, 'FontSize', 20);
xlabel('f[$Hz$]', 'FontSize', 20, 'Interpreter', 'latex');
grid();
% title('Espectro de Perturbacion', 'FontSize', 40, 'Interpreter', 'latex');

C = sqrt((abs(W_UY).^2)./(W_YY.*W_UU + eps));
figure ;
semilogx(f, abs(C(1:end/2+1)), 'LineWidth', 2, 'Color', rand(1,3));
xlim([0.5 10^(3)]);
set(gca, 'FontSize', 20);
% title('Espectro de Coherencia','FontSize', 40, 'Interpreter', 'latex');
xlabel('f[$Hz$]', 'FontSize', 20, 'Interpreter', 'latex');
grid();

r = 0.99; % nivel de confianza

figure;
plot(real(Gw), imag(Gw), 'LineWidth', 1.5, 'Color', rand(1,3));
set(gca, 'FontSize', 20);
% title('Nyquist','FontSize', 40, 'Interpreter', 'latex');
grid();

figure;
plot(real(Gw(abs(C)>r)), imag(Gw(abs(C)>r)), 'LineWidth', 1.5, 'Color', rand(1,3));
set(gca, 'FontSize', 20);
% title(['Nyquist en frecuencias confiables al ', num2str(r)],'FontSize', 40, 'Interpreter', 'latex');
grid();


%% Animación del diagrama de Nyquist

figure;
curve = animatedline;

x = real(Gw(abs(C)>r));
y = imag(Gw(abs(C)>r));

for i=1:50:length(x)
    addpoints(curve, x(i), y(i));
    drawnow
end

save_all_figures('./', 'Lazo_cerrado_');
