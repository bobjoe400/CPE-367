
% setup LPF coefficients
fc = 2000;
fs = 16000;
wc = 2 * pi * fc / fs;
M = 21;
% this half-length expression works when M is odd
Mm1o2 = (M-1)/2;
% define sequence for length 3
n = -Mm1o2:Mm1o2;
% evaluate h[n]
hn = sin(wc * n) ./ (pi * n);
% the middle value of hn is screwed up - fix it
hn(Mm1o2+1) = wc / pi;
% apply window
hamm_win = hamming(M);
hamm_win = transpose(hamm_win);
hn = hn .* hamm_win;

hn

fvtool(hn,'Fs',fs)