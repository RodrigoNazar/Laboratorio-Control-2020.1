clear all;

a1 = 0.071;
a2 = 0.057;
a3 = 0.071;
a4 = 0.057;

A1 = 28;
A2 = 32;
A3 = 28;
A4 = 32;

k1 = 3.33;
k2 = 3.33;

g = 981;

y1 = 0.7;
y2 = 0.6;


% y1 = 0.35;
% y2 = 0.35;

h1_0 = 40;
h2_0 = 40;
h3_0 = 40;
h4_0 = 40;

%% plot

figure;

subplot(221);
plot(h3.Time, h3.Data, 'LineWidth', 2, 'Color',  rand(1,3));
ylim([0, 50]);
ylabel('Altura', 'Interpreter', 'latex', 'FontSize', 30);
xlabel('(s)', 'Interpreter', 'latex', 'FontSize', 30);
title('Tanque3', 'Interpreter', 'latex', 'FontSize', 30);

subplot(222);
plot(h4.Time, h4.Data, 'LineWidth', 2, 'Color',  rand(1,3));
ylim([0, 50]);
ylabel('Altura', 'Interpreter', 'latex', 'FontSize', 30);
xlabel('(s)', 'Interpreter', 'latex', 'FontSize', 30);
title('Tanque4', 'Interpreter', 'latex', 'FontSize', 30);

subplot(223);
plot(h1.Time, h1.Data, 'LineWidth', 2, 'Color',  rand(1,3));
ylim([0, 50]);
ylabel('Altura', 'Interpreter', 'latex', 'FontSize', 30);
xlabel('(s)', 'Interpreter', 'latex', 'FontSize', 30);
title('Tanque1', 'Interpreter', 'latex', 'FontSize', 30);

subplot(224);
plot(h2.Time, h2.Data, 'LineWidth', 2, 'Color',  rand(1,3));
ylim([0, 50]);
ylabel('Altura', 'Interpreter', 'latex', 'FontSize', 30);
xlabel('(s)', 'Interpreter', 'latex', 'FontSize', 30);
title('Tanque2', 'Interpreter', 'latex', 'FontSize', 30);

