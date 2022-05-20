cent = [697,770,1209,1336];
rad = [0.93,0.92,0.92,0.92];

fileID = fopen("bpf_coef.txt",'W');
C = 1024;
fs = 4000;
for i = 1:length(cent)
    fc = cent(i);
    r = rad(i);
    wc = 2*pi*fc/fs;
    
    zzz = [exp(j*wc),exp(-j*wc)];
    bk = poly(zzz);
    ppp = [r*exp(j*wc),r*exp(-j*wc)];
    ak = poly(ppp);
    fvtool(bk,ak,'Fs',fs)

    fprintf(fileID,'%f %f %f\n',bk);
    fprintf(fileID,'%f %f %f\n',ak);
end
fclose(fileID);