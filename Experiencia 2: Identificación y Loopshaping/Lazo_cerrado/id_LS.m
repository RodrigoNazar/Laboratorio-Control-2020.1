clear; clc;
set(0, 'DefaultFigureWindowStyle', 'docked');
%%
clc;
Ts = 0.0005;
t = 0:Ts:2;
Cs = 0.3;
kd = 7.5e-4;
ki = 0.9;
% Entrada 0
u1 = [t', 1+0*t', 0*t'];
r = [];
k = 1;
m = [0.1, 1, 10, 100, 500, 1000];
for i = 1%:250
%     a = m(randi(6))*abs(rand()); 
%     b = m(randi(6))*abs(rand()); 
    try
    [t_entrada0,~,y_entrada0] = sim('loopshape',t(end),[],u1);
    figure;
    plot(t_entrada0, y_entrada0(:,1), 'LineWidth', 2, 'Color', rand(1,3));
    title('Intento 3');
    r(k) = 100 * norm(y_entrada0(:,1)-1)/norm(t*0+1); k = k + 1;
    end
end

%% PSBR
clc;
N = 2^16-1;
P = 30;

PRBS = idinput([N, 1, P], 'prbs');
L2 = length(PRBS);
t2 = (0:L2-1)'*Ts;

entrada_prbs = [t2, ones(size(t2)), PRBS];

tic;
[t_prbs, ~, salida_prbs] = sim('loopshape', t2(end), [], entrada_prbs);
toc;

%%
