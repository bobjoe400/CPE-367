N = 8;
D = dftmtx(N);
xn = [ 1, 2, 0, 0, 0, 0, 0, 0 ];
xn = transpose(xn);
Xk = D * xn