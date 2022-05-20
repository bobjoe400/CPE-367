%Run from editor Debug(F5)
%This M file constructs a two pole two zero bandpass filter using the Z Transform 
%transfer function and analyzes the characteristics of the filter such as frequency response and
%phase using the Matlab filter function with input vector x
%to get output y=filter(b,a,x).Frequency domain plots are also provided to
%analyze the bandpass filter.
%The z transform is just basically a transformation from a linear continuous system to
%a sampled system.
%The center frequency and 3dB bandwidth(fBW) of the BPF filter can be set to 
%<100Hz to >1GHz by appropriate setting of the sampling frequency(fs) and
%center frequency(fcent) and by use of the following formula(BW=(1-a)/sqrt(a)) where
%BW=2*pi*fcent/fs and (a) is the imaginary pole magnitudes. To get 0dB of attenuation
%at the center frequency(fcent),the poles must be at an angle of 2*pi*fcent/fs=pi/2.
%This corresponds to +/-j on the unit circle in the z domain. The symbolic math
%processor in Matlab is used with the "solve" function to determine the
%value as shown typed in the command window "solve('2*(1-a)/sqrt(a)=BW')".
%The purpose of constructing this M file was instigated by the following facts.
%I have some knowledge of Laplace transforms and the s plane. Someone mentioned 
%using z transforms and I said "What is a z transform, that sounds complicated?".
%So I am trying to understand what it's all about. Anyway, that's why.
%I have added references at the end of the program that I have found
%helpful and hopefully playing with the program will give you a better
%understanding of the theory. Always remember to set your axis settings on
%plot routines. The following describes the BPF. 
%Bandpass filter 2 poles 2 zeros
%H(z)=(z+1)*(z-1)/(z+jp)*(z-jp)=(z^2-1)/(z^2-(p^2)
%zeros at +/-1
%pole at +j/-j
%
%                                pi/2
%                      Z plane   !+j(imag axis)
%                                x
%                     fs/2       !
%2 poles,2 zeros   (-1)0---------!---------(+1)real axis
%                      pi        !
%                                x
%                                !-j
%
%
%==================================================
%Design example
%==================================================
clear
fcent=6500e6;%center frequency of bandpass filter
fBW=1000e6;%3dB bandwidth
fs=26e9;%sampling frequency(set ~4 times fcent)
%f/fs=.5,set f=.5*fs
f=[0:1e6:13e9];%keep interval steps high for lower 
%computer processing time
Fn=fs/2;%nyquist frequency-used in fft plots
w=2*pi*f/fs;%set so w=pi or 3.14
z=exp(w*j);%z definition
BW=2*pi*fBW/fs;
%solve('2*(1-a)/sqrt(a)=BW')%-solving for a gives a=.8862
%One could also use the symbolic math processor and construct a graph to
%solve for (a).
%type in command window the following:
%syms BW a
%BW=(2*(1-a)/sqrt(a))
%ezplot(BW),axis([0 1 0 1]),ylabel('BW'),grid on
a=.8862;
p=(j^2*a^2);%multiply (j*a)*(-j*a)
gain=.105;%set gain for unity(1) by observing plots 
Hz=gain*(z+1).*(z-1)./(z.^2-(p));%z transform(transfer function)
%===================================================
%Magnitude and phase plots
%===================================================
figure(1)
subplot(3,1,1), plot(f,abs(Hz))
axis([0 13e9 0 1.5]);
grid on
title('Magnitude Response of H(z)')
ylabel('H(z)-voltage')

subplot(3,1,2);
Hz(Hz==0)=10^(-8);%avoid log(0)
plot(f,20*log10(abs(Hz)));
grid on
ylabel('dB')
axis([0 13e9 -3 1]);%set -3 to -60 to zoom out

subplot(3,1,3), plot(f,angle(Hz))
grid on
title('Phase Response of H(z)')
ylabel('radians*57.3=degrees')%one radian=57.3 degrees
xlabel('f [Hertz]')
axis([0 13e9 -2 2]);


fcent=6500e6;%carrier frequency(Hz),notice no loss at 6500e6
%Try 6000e6 and 7000e6 to check for -3dB loss.
T=1/1e6;%sets span of y filter output plot
%x=A1*(cos(2*pi*fc*t)+phi)(cosine wave)
twopi_fc_t=(1:fs*T)*2*pi*fcent/fs; 
A1=1;
phi=0;
x = A1 * cos(twopi_fc_t + phi);

%You could also use a square wave or an impulse signal instead of a cosine
%wave.
%===============================================
%a and b filter coefficients
%===============================================
%To get the a and b coefficients, expand the numerator and denominator.
%a=(z+p)*(z-p)=z^2-(p^2)=[1 0 -(p)]
a=[1 0 .7855];%(1 0 p)
b=[.105 0 -.105];%gain times [1 0 -1)
% ===============================================
%Output y = filter(b,a,x)
% ===============================================
y = filter(b,a,x);
%Plot input x and output y
%Observe amplitude and phase shift of y compared to x. Will need
%much lower center frequency bandpass filter(say 1000Hz) and span to see phase shift.
%Magnitude and phase shift at fc shown in command window.
figure(2);
plot(x,'b-'); hold on;
plot(y,'r-');
grid on
title('input x(blue)  /  output y(red)')
ylabel('Voltage')
hold off;

%Magnitude and phase at fcent
w=2*pi*fcent/fs;
z=exp(w*j);
Hz=gain*(z+1).*(z-1)./(z.^2-(p));
magfcent=abs(Hz)
phaseradfcent=angle(Hz)
%===================================================
%Frequency domain plots
%====================================================
%Lets take a look at y output on a spectrum analyzer. This fft code is
%somewhat complex but comes from the mathworks. Works great as it shows
%one what they would actually see using a spectrum analyzer.

NFFY=2.^(ceil(log(length(y))/log(2)));
FFTY=fft(y,NFFY);%pad with zeros
NumUniquePts=ceil((NFFY+1)/2); 
FFTY=FFTY(1:NumUniquePts);
MY=abs(FFTY);
MY=MY*2;
MY(1)=MY(1)/2;
MY(length(MY))=MY(length(MY))/2;
MY=MY/length(y);
f1=(0:NumUniquePts-1)*2*Fn/NFFY;

figure(3)
subplot(2,2,1); plot(f1,MY);xlabel('FREQUENCY');ylabel('AMPLITUDE');
axis([0 13e9 -1 1.5]);%zoom in/out
grid on;
subplot(2,2,2); plot(f1,10*log10(abs(MY).^2));xlabel('FREQUENCY');ylabel('20LOG10=DB');
axis([0 13e9 -60 5]);
grid on;
title('Frequency domain plots')
%observe that the carrier frequency(fcent) is at 1 or 0 dB on the plots as one would
%expect.

%References
%http://www.eas.asu.edu/~midle/jdsp/jdsp.html
%This site is one of the best. Log on and use the pole-zero demo and the
%filter demo.

%http://www.ece.uvic.ca/~peter/
%A good site for communication and filter theory and m files.
