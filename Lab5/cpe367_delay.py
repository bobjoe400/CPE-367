#!/usr/bin/python

import sys
import time

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
	: this example does not implement an echo!
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
		
	# setup configuration for output WAV
	num_channels = 1
	sample_width_8_16_bits = 16
	sample_rate_hz = 16000
	wav_out.set_wav_out_configuration(num_channels,sample_width_8_16_bits,sample_rate_hz)

	# open WAV output file
	ostat = wav_out.open_wav_out()
	if ostat == False:
		print('Cant open wav file for writing')
		return False
	
	###############################################################
	###############################################################
	# students - allocate your fifo, with an appropriate length (M)
	M = 2000

	#using an array of fifos instead of many different values allows for easier manipulation
	in_fifo = []
	out_fifo = []
	for i in range(6):
		in_fifo.append(my_fifo(M))
		out_fifo.append(my_fifo(M))
 
	# students - allocate filter coefficients as needed, length (M)
	# students - these are not the correct filter coefficients
	###############################################################
	###############################################################

	# process entire input signal
	xin = 0
	while xin != None:
	
		# read next sample (assumes mono WAV file)
		#  returns None when file is exhausted
		xin = wav_in.read_wav()
		if xin == None: break
		

		###############################################################
		###############################################################
		# students - there is work to be done here!
		
		# update history with most recent input
		# evaluate your difference equation	to yield the desired effect!
		#  this example just copies the mono input into the left and right channel
		

		# students - well done!
		###############################################################
		###############################################################
	    #creation of the different taus
		t1 = [0.030*sample_rate_hz,0.035*sample_rate_hz,0.040*sample_rate_hz,0.045*sample_rate_hz,0.0017*sample_rate_hz]
		t = [int(a) for a in t1]

		#setting final gain of the reverb
		f_gain = 0.4
		g = [0.7,f_gain]

		#my 4 initial IIRs, since they all take the same input, i can just update each of them using a for loop
		r = [0]*4
		for i in range(4):
			#updating the input
			in_fifo[i].update(xin)
			#w[n] = x[n-d] + w[n-2d]
			r[i] = in_fifo[i].get(t[i]) + g[0]*out_fifo[i].get(2*t[i])
			#updating output as a result of the filter when you see in-r-out they do the same as above
			out_fifo[i].update(r[i])
		#quick summation of all of the intial IIRs
		w = sum(r)
		in_fifo[4].update(w)
		r = in_fifo[4].get(t[4]) + g[0]*out_fifo[4].get(2*t[4])
		out_fifo[4].update(r)
		#final output of 5th IIR
		y = -g[0]*w + (1-g[0]**2)*r
		in_fifo[5].update(y)
		r = in_fifo[5].get(t[4]) + g[0]*out_fifo[5].get(2*t[4])
		out_fifo[5].update(r)
		#final output of 6th IIR
		z = -g[0]*y + (1-g[0]**2)*r
		#final output of the program. To prevent clipping, I adjusted the total gain for the program as some as 
		#some of the input values already are at abs(32768) as not to mess with the ratio of reverb vs origional
		#signal. 
		yout = 0.45*(xin + g[1]*z)

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
	fpath_wav_in = 'impulse.wav'
	fpath_wav_out = 'impulse_reverb.wav'
	
	
	
	############################################
	############################################
	# test signal history
	#  feel free to comment this out, after verifying
		
	# # allocate history
	# M = 3
	# fifo = my_fifo(M)

	# # add some values to history
	# fifo.update(1)
	# fifo.update(2)
	# fifo.update(3)
	# fifo.update(4)
	
	# # print out history in order from most recent to oldest
	# print('signal history - test')
	# for k in range(M):
	# 	print('hist['+str(k)+']='+str(fifo.get(k)))

	############################################
	############################################
	


	# let's do it!
	return process_wav(fpath_wav_in,fpath_wav_out)
	
			
	
	
	
############################################
############################################
# call main function
if __name__ == '__main__':
	
	main()
	quit()
