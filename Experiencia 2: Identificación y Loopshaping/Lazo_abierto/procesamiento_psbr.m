%% Procesamiento PRBS

figure;
plot(t2, salida_prbs(3:end), 'LineWidth', 2, 'Color', rand(1,3));
set(gca, 'FontSize', 20);
% title('Salida de la PRBS', 'FontSize', 45, 'Interpreter', 'latex');
grid();
xlabel('$t$', 'Interpreter', 'latex', 'FontSize', 30);

figure;
plot(t2(1:500), PRBS(1:500), 'LineWidth', 2, 'Color', rand(1,3));
set(gca, 'FontSize', 20);
% title('PRBS', 'FontSize', 45, 'Interpreter', 'latex');
grid();
xlabel('$t$', 'Interpreter', 'latex', 'FontSize', 30);

y = detrend(salida_prbs, 'linear');
y(2:3) = [];

figure;
plot(t2, y, 'LineWidth', 2, 'Color', rand(1,3));
set(gca, 'FontSize', 20);
% title('Detrend', 'FontSize', 45, 'Interpreter', 'latex');
grid();
xlabel('$t$', 'Interpreter', 'latex', 'FontSize', 30);

% promedio
y2 = reshape(y, [length(y)/P, P]);
y2 = y2(:, 2:end);
y2 = sum(y2, 2) / (P-1);

% sennal
t = t_prbs(1:N);
u = entrada_prbs(1:N,2);

figure;
plot(t, y2, 'LineWidth', 2, 'Color', rand(1,3));
set(gca, 'FontSize', 20);
% title('Promedio', 'FontSize', 45, 'Interpreter', 'latex');
grid();
xlabel('$t$', 'Interpreter', 'latex', 'FontSize', 30);


% Correlacion
uu = mycorr(u, u);
uy = mycorr(u, y2);
yy = mycorr(y2, y2);

% Enventanado
filter = hann(length(uu)).^0.9;
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
semilogx(f, 20*log10(abs(Gw(1:end/2+1))), 'LineWidth', 2, 'Color', rand(1,3));
grid();
xlim([0.5 1.4*10^(2)])
set(gca, 'FontSize', 20);
% title('Magnitud $|Gw|$', 'FontSize', 34, 'Interpreter', 'latex');
xlabel('f[$Hz$]', 'FontSize', 20, 'Interpreter', 'latex');
ylabel('Magnitud', 'FontSize', 20, 'Interpreter', 'latex');

subplot(212);
semilogx(f, rad2deg(-phase(Gw(1:end/2+1))), 'LineWidth', 2, 'Color', rand(1,3));
grid();
xlim([0.5 1.4*10^(2)])
set(gca, 'FontSize', 20);
% title('Fase $\angle Gw$', 'FontSize', 34, 'Interpreter', 'latex');
xlabel('f[$Hz$]', 'FontSize', 20, 'Interpreter', 'latex');
ylabel('Angulo', 'FontSize', 20, 'Interpreter', 'latex');
% l = suptitle('Diagrama de Bode');
% set(l, 'FontSize', 40, 'Interpreter', 'latex');

D = W_YY - abs(W_UY).^2 ./ (W_UU+eps);
figure;
semilogx(f, abs(D(1:end/2+1)), 'LineWidth', 2, 'Color', rand(1,3));
xlim([1 10^2]);
set(gca, 'FontSize', 20);
xlabel('f[$Hz$]', 'FontSize', 20, 'Interpreter', 'latex');
grid();
% title('Espectro de Perturbacion', 'FontSize', 40, 'Interpreter', 'latex');

C = sqrt((abs(W_UY).^2)./(W_YY.*W_UU + eps));
figure ;
semilogx(f, abs(C(1:end/2+1)), 'LineWidth', 2, 'Color', rand(1,3));
xlim([0.5 2*10^(2)]);
set(gca, 'FontSize', 20);
% title('Espectro de Coherencia','FontSize', 40, 'Interpreter', 'latex');
xlabel('f[$Hz$]', 'FontSize', 20, 'Interpreter', 'latex');
grid();
