function [corr] = mycorr(u, y, gamma) 
if nargin < 3
    gamma = 2^14 - 1;
end

corr = zeros(2*gamma+1, 1);
tic;
for tau = -gamma:gamma
    y_rot = circshift(y, tau);
    corr(tau+gamma+1) = u' * y_rot;
end
toc;
corr = corr / length(u);
end
