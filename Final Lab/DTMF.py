#%%
#%matplotlib inline
#!/usr/bin/python


import sys
import time

import base64
import random as random

import datetime
import time
import math

import matplotlib.pyplot as plt
import numpy as np
from my_fifo import my_fifo

from cpe367_wav import cpe367_wav
from cpe367_sig_analyzer import cpe367_sig_analyzer





############################################
############################################
# define routine for detecting DTMF tones
def process_wav(fpath_sig_in):
	
		
	###############################
	# define list of signals to be displayed by and analyzer
	#  note that the signal analyzer already includes: 'symbol_val','symbol_det','error'
	more_sig_list = ['sig_1','sig_2']
	
	# sample rate is 4kHz
	fs = 4000
	
	# instantiate signal analyzer and load data
	s2 = cpe367_sig_analyzer(more_sig_list,fs)
	s2.load(fpath_sig_in)
	s2.print_desc()
	
	########################
	# students: setup filters

	#I am using dictionaries to store all the data for the FIFOs and coefficients.
	#This makes it easy to access them and allows for iteration of processing. 
	bpf_coef = {697:{},
				770:{},
				1209:{},
				1336:{}}
	fifo = {}
	bpf_fout = {}
	#Filter length 
	M = {697: 4,
		 770: 2,
		 1209: 5,
		 1336: 7}

	#Peak finder fifo gain, the longer this is the more smooth the ouput
	G = {697: 3,
		 770: 3,
		 1209: 5,
		 1336: 5}

	#Threshold values, lower and upper. I decided to do this to try and improve
	#response. When the signal is off it looks for the lower threshold to turn
	#on and then when on, the upper threshold. 
	T = {697: [625,710],
		 770: [550,550],
		 1209: [630,710],
		 1336: [550,710]}
	
	#Signal on dictionary
	sig_on = {}
	#integer coefficent
	C = 256

	#grabbing the coefficents made from Matlab that are in the text file
	#this was done so I am able to compute the coeficients in Matlab and 
	#view the filters in there while still being able to quickly run my
	#filter in python. 
	f = open("bpf_coef.txt")
	i,j = 0,0
	for line in f.readlines():
		fq = list(bpf_coef.keys())[j]
		line = [float(k) for k in line.split()]
		if not i%2:
			bpf_coef[fq]['bk'] = line
		else:
			bpf_coef[fq]['ak'] = line
			j+=1
		i+=1
	#setting up the fifo's for the BPF's and peak detectors
	for fq in bpf_coef.keys():
		fifo[fq] = {'x':my_fifo(M[fq]),'y':my_fifo(M[fq]),'peak':my_fifo(int(G[fq]*(fs/fq)))}
		sig_on[fq] = 0
	# process input	
	xin = 0

	mod = 'p'
	coeff_print = 0
	for n_curr in range(s2.get_len()):
		# read next input sample from the signal analyzer
		xin = s2.get('xin',n_curr)
		########################
		# students: evaluate each filter and implement other processing blocks
		for fq in bpf_coef.keys():
			#update FIFO, round the coefficeints, then compute the difference
			#equation of the notch filter, and then do 1-Notch to get my inverse
			#notch filter (a bandpass)
			fifo[fq]['x'].update(xin)
			bpf_out = 0
			b = [int(round(C*i)) for i in bpf_coef[fq]['bk']]
			a = [int(round(C*i)) for i in bpf_coef[fq]['ak']]

			if coeff_print < 4:
				print("Coeffcients for "+str(fq)+":")
				print("Scaled Integer Coeffcients:\nb[k]'s = "+str(b))
				print("a[k]'s = "+str(a)+'\nFloating Point Coeffcients:')
				print("b[k]'s = "+str(bpf_coef[fq]['bk']))
				print("a[k]'s = "+str(bpf_coef[fq]['ak'])+'\n')
				coeff_print+=1
			
			x,y = [],[]
			for i in range(3):
				x.append(fifo[fq]['x'].get(i))
				y.append(fifo[fq]['y'].get(i))
			yout = (b[0]*x[0] + b[1]*x[1] + b[2]*x[2] - a[1]*y[1] - a[2]*y[2])/C
			fifo[fq]['y'].update(yout)
			bpf_out = 1-yout

			#Take the aboslute value 
			bpf_fout[fq] = abs(bpf_out)
			s2.set(str(fq),n_curr,bpf_fout[fq])

			#Peak detection, my_fifo.maximum() just returns max(self.buff)
			s2.set('ch'+str(fq),n_curr,fifo[fq]['peak'].check_change(bpf_fout[fq]))
			
			fifo[fq]['peak'].update(bpf_fout[fq])
			peak = fifo[fq]['peak'].maximum()

			s2.set('p'+str(fq),n_curr,peak)

			#turning on the signal and using the correct threshold
			if sig_on[fq]:
				if peak < T[fq][1]:
					sig_on[fq] = 0
			else:
				if peak > T[fq][0]:
					sig_on[fq] = 1
			s2.set("on_"+str(fq),n_curr,sig_on[fq])

			
		  

		########################
		# students: combine results from filtering stages
		#  and find (best guess of) symbol that is present at this sample time
		symbol_val_det = 0

		#symbol detection logic
		if sig_on[697]:
			if sig_on[1336]:
				symbol_val_det = 2
			else:
				symbol_val_det = 1
		else:
			if sig_on[1336]:
				symbol_val_det = 5
			else:
				symbol_val_det = 4
		
		# save intermediate signals as needed, for plotting
		#  add signals, as desired!
		s2.set('sig_1',n_curr,xin)

		# save detected symbol
		s2.set('actual',n_curr,symbol_val_det)

		# get correct symbol (provided within the signal analyzer)
		symbol_val = s2.get('symbol_val',n_curr)

		# compare detected signal to correct signal
		symbol_val_err = 0
		if symbol_val != symbol_val_det: symbol_val_err = 1
		
		# save error signal
		s2.set('error',n_curr,symbol_val_err)
		
	
	# display mean of error signal
	err_mean = s2.get_mean('error')
	print('mean error = '+str( round(100 * err_mean,1) )+'%')

	# define which signals should be plotted
	plot_sig_list = ['sig_1',
					mod+'697',mod+'770',mod+'1209',mod+'1336',
					'symbol_val','actual','error']

	# plot results
	s2.plot(plot_sig_list)
	
	
	return True



	
	
	
############################################
############################################
# define main program
def main():

	# check python version!
	major_version = int(sys.version[0])
	if major_version < 3:
		print('Sorry! must be run using python3.')
		print('Current version: ')
		print(sys.version)
		return False
		
	# assign file name
	
	#fpath_sig_in = 'dtmf_signals_slow.txt'
	fpath_sig_in = 'dtmf_signals_fast.txt'
	
	
	# let's do it!
	return process_wav(fpath_sig_in)


	
	
############################################
############################################
# call main function
if __name__ == '__main__':
	
	main()

 # %%
