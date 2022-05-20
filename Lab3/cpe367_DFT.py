#!/usr/bin/python

import sys
import time
import math

import matplotlib.pyplot as plt
import numpy as np


import base64
import random as random

import datetime
import time

from cpe367_wav import cpe367_wav
from my_fifo import my_fifo


	
############################################
############################################
# define routine for implementing a digital filter
def process_wav(fpath_wav_in):
	"""
	: this example implements a very useful system:  y[n] = x[n]
	: input and output is accomplished via WAV files
	: return: True or False 
	"""
	
	# construct objects for reading/writing WAV files
	#  assign each object a name, to facilitate status and error reporting
	wav_in = cpe367_wav('wav_in',fpath_wav_in)
	
	# open wave input file
	ostat = wav_in.open_wav_in()
	if ostat == False:
		print('Cant open wav file for reading')
		return False
		
	# configure wave output file, mimicking parameters of input wave (sample rate...)
	sample_rate_hz = 8000
	
	###############################################################
	###############################################################
	# students - allocate your fifo, with an appropriate length (M)
	
	
	
	###############################################################
	###############################################################
	# process entire input signal
	DFT_arr, x = [], []
	N = 4000
	xin = 0
	j = 0
	while xin != None and j<N:
		# read next sample (assumes mono WAV file)
		# returns None when file is exhausted
		xin = wav_in.read_wav()
		if xin == None: break
		###############################################################
		###############################################################
		# students - go to work!
		x.append(xin)
		j+=1
		# students - well done!
		###############################################################
		###############################################################
	# close input and output files
	#  important to close output file - header is updated (with proper file size)
	wav_in.close_wav()

	#DFT Function
	for k in range(N):
		temp_dic = {'real':0,'imag':0,'mag':0,'fq_hz':0}
		real, imag = 0,0
		for n in range(N):
			#calculate the theta to be used in DFT pass and then save real and imaginary parts in the dictionary
			theta = -k * 2 * math.pi * n / N
			real += x[n]* math.cos(theta)
			imag += x[n]* math.sin(theta)
		temp_dic['real'] = real
		temp_dic['imag'] = imag

		#calculate magnitude and frequency for the DFT pass
		temp_dic['mag'] = 1/N*(math.sqrt(temp_dic['real']**2+temp_dic['imag']**2))
		temp_dic['fq_hz'] = ((sample_rate_hz/N)*k-sample_rate_hz,(sample_rate_hz/N)*k)[k<(N/2)]
		DFT_arr.append(temp_dic)

	#Creating magitude/frequeny plot
	mag, fq = [], []
	for i in range(N):
		if DFT_arr[i]['fq_hz'] > 0 and DFT_arr[i]['fq_hz']<= 2000: 
			mag.append(DFT_arr[i]['mag'])
			fq.append(DFT_arr[i]['fq_hz'])
	#Finding raw maximums and weighted maximums		
	T = max(mag)
	f_max = fq[mag.index(T)]
	w_top,w_bottom = 0,0
	for i in range(len(mag)):
		w_top+=(0,fq[i]*mag[i])[mag[i]>(T/2)]
		w_bottom+=(0,mag[i])[mag[i]>(T/2)]
	f0 = w_top/w_bottom
	L = 343/(2*f0) * 39.37 #Finding length then using conversion factor to get to inches
	print(fpath_wav_in[-6:-4],' ', f_max,' ',f0,' ',L)
	fig,ax = plt.subplots()
	ax.plot(np.array(fq),np.array(mag))
	ax.set(xlabel = "Frequency",ylabel ='Counts',title=fpath_wav_in)
	ax.minorticks_on()
	ax.grid()
	fig.savefig(fpath_wav_in[:-4]+'.png')
	plt.show()
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
			
	# grab file names
	for i in range(1,3):
		for j in range(97,102):
			fpath_wav_in = 'sig_disp_exp_7/tile'+str(i)+chr(j)+'.wav'
			process_wav(fpath_wav_in)
			
	# let's do it!
	return True
	
	
############################################
############################################
# call main function
if __name__ == '__main__':
	
	main()
	quit()
