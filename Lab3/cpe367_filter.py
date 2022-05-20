#!/usr/bin/python

import sys
import time
import math

import base64
import random as random

import datetime
import time

from cpe367_wav import cpe367_wav
from my_fifo import my_fifo


	
############################################
############################################
# define routine for implementing a digital filter
def process_wav(fpath_wav_in,fpath_wav_out):
	"""
	: this example implements a very useful system:  y[n] = x[n]
	: input and output is accomplished via WAV files
	: return: True or False 
	"""
	
	# construct objects for reading/writing WAV files
	#  assign each object a name, to facilitate status and error reporting
	wav_in = cpe367_wav('wav_in',fpath_wav_in)
	wav_out = cpe367_wav('wav_out',fpath_wav_out)
	
	# open wave input file
	ostat = wav_in.open_wav_in()
	if ostat == False:
		print('Cant open wav file for reading')
		return False
		
	# configure wave output file, mimicking parameters of input wave (sample rate...)
	num_channels = 1
	sample_width_8_16_bits = 16
	sample_rate_hz = 5000
	wav_out.set_wav_out_configuration(num_channels,sample_width_8_16_bits,sample_rate_hz)
	
	# open WAV output file
	ostat = wav_out.open_wav_out()
	if ostat == False:
		print('Cant open wav file for writing')
		return False
	
	###############################################################
	###############################################################
	# students - allocate your fifo, with an appropriate length (M)
	
	#number of taps
	M = 11
	fifo = my_fifo(M)
 
	# students - allocate filter coefficients, length (M)
	# students - these are not the correct filter coefficient

	#Our modifying constants
	hamm = True
	cutoff = 750
	bp_center = 4000

	#calculating the digital frequency cutoffs
	w_cutoff = 2 * math.pi * cutoff / sample_rate_hz
	w_center = 2 * math.pi * bp_center / sample_rate_hz

	#since we are using 21 taps, we need to make the array size for h[n] 2*taps + 1 with the + 1 accounting for the zero value
	hn = (2*M+1)*[0]
	for i in range(len(hn)):
		#handling the zero condidition
		if i-M == 0:
			hn[i] = w_cutoff/math.pi#*2*math.cos(w_center*(i-M))
		else:
			#convoluting the bp equation and the sinc function
			hn[i] =  math.sin(w_cutoff * (i-M))/(math.pi * (i-M))#*2*math.cos(w_center*(i-M))
	
	bk_list = M*[0]
	k = 0
	#quick function to output the hamming window values
	def window(index,hamm):
		if hamm:
			return 0.54 - 0.46 * math.cos(2*math.pi*index/(M-1))
		return 1
	#final calulation of the b[k]'s, its just easier to read if we go from -(m-1)/2 to (m-1)/2 and just adjust the index of h[n] accordingly
	for i in range(-(M-1)//2,(M-1)//2+1):
		index = (len(hn)-1)//2 + i
		bk_list[k] = 1.7*((-1)**i)*hn[index] * window(k,hamm)
		k+=1
	
	###############################################################
	###############################################################
	print(bk_list)
	# process entire input signal
	xin = 0
	while xin != None:
	
		# read next sample (assumes mono WAV file)
		#  returns None when file is exhausted
		xin = wav_in.read_wav()
		if xin == None: break
		

		###############################################################
		###############################################################
		# students - go to work!
		
		#I didn't change any of this code. 
		# update history with most recent input
		fifo.update(xin)
		
		# evaluate your difference equation		
		yout = 0
		for k in range(M):

			# use your fifo to access recent inputs when evaluating your diff eq
			# y[n] = sum of b[k] * x[n-k]
			yout += bk_list[k] * fifo.get(k)
		
		
		# evaluate difference equ, here as y[n] = x[n]
		#a simple sum of the 3 most recent inputs using the coefficients in the bk_list
		
		# update history of recent inputs...
		# xprev = ...

		#set the oldest to the previous THEN set the previous as the current
		
		# students - well done!
		###############################################################
		###############################################################


		# convert to signed int
		yout = int(round(yout))
		
		# output current sample
		ostat = wav_out.write_wav(yout)
		if ostat == False: break
	
	# close input and output files
	#  important to close output file - header is updated (with proper file size)
	wav_in.close_wav()
	wav_out.close_wav()
		
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
	fpath_wav_in = 'in_noise.wav'
	fpath_wav_out = 'out_noise.wav'
	
	
	
	'''
	############################################
	############################################
	# test signal history
	#  feel free to comment this out, after verifying
		
	# allocate history
	M = 3
	fifo = my_fifo(M)

	# add some values to history
	fifo.update(1)
	fifo.update(2)
	fifo.update(3)
	fifo.update(4)
	
	# print out history in order from most recent to oldest
	print('signal history - test')
	for k in range(M):
		print('hist['+str(k)+']='+str(fifo.get(k)))

	############################################
	############################################
	'''


	# let's do it!
	return process_wav(fpath_wav_in,fpath_wav_out)
	
			
	
	
	
############################################
############################################
# call main function
if __name__ == '__main__':
	
	main()
	quit()
