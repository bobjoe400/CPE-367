#!/usr/bin/python

import sys
import time

import base64
import random as random

import datetime
import time
import math

from cpe367_wav import cpe367_wav



############################################
############################################
# define function to add one note to list
# students - modify this function as needed!

def add_note(xlist,amp,w0,nstart,nlen,treble):

	# this initial version of the function only includes a tone burst
	#  no harmonics and no decaying envelope are included

	#calculating sigma based on the length of the note, so we have the same decay time
	sigma = -nlen/math.log(0.1)
	harm_sigma = -nlen/math.log(0.3)
	attack = 200
	
	#choose how many harmonics, and their aplitudes based on it being treble or bass cleff 
	if(not treble):
		harmonics = [1,2,3,4,6,8,9,11,13]
		harm_amp = [0.295,.301,.15,.13,.019,0.025,.031,0.025,0.019] 
	else:
		harmonics = [1,2,3,4,6,8,9,11]
		harm_amp = [0.415,.2,.15,.13,.019,0.025,.031,0.025]

	"""
	This is my own version of an ADSR envelope, where the attack is 200/16000 of a second, the decay is
	the 50% of the note, the sustain is from 50% to 90%, and the release is the last 10%.

	I cannot hear how this affects the note much, but it was cool as a logic excercise. 

	I tried to make sure that each value lines up with the previous envelope value, and I disabled
	the envelope for harmonics and let them just decay as normal. 
	"""
	def envelope(n,h):
		if h == 0:
			if n < attack:
				return n/attack
			elif n < nlen*0.5:
				return math.e**(-(n-attack)/sigma)
			elif n < nlen*0.9:
				return math.e**(-(nlen*0.5-attack)/sigma)#this value does not change, as the sustain shouldn't as it 
														 #is based upon the length of the note instead of the current
														 #sample number of the note
			else:
				env = ((n-nlen*.9)**2 + 1)*math.e**(-(nlen*0.5-attack)/sigma)
				return (0,env)[env>0]
		else:
			return math.e**(-(n)/harm_sigma)

	
	"""Adding the different harmonic notes to the setup. 
	
	With the envelope always being between 0 and 1, we can just use this as a normal scalar in the equation

	I also am using the harmonic amplitudes from above so that way each harmonic has their own specific amplitude scalar. 

	The amplitudes of the bass notes harmonics were derived from using the freq analyizer of the first lab on the first 
	note of the joy_harp(...).wav file. 
	"""
	for h in range(len(harmonics)):
		w1 = w0*harmonics[h]
		for n in range(nstart,nstart+nlen):
			j = 0
			try:
				env = envelope(j,h)
				xlist[n] += harm_amp[h] * amp * env * math.sin(w1 * n)
			except IndexError:
				break
			j+=1
	# note summed into signal
	return
	
			


############################################
############################################
# define routine for generating signal in WAV format
def gen_wav(fpath_wav_out):
	# : this example generates a WAV file
	# : output is accomplished via WAV files
	# : return: True or False 
	
	
	# construct object for writing WAV file
	# assign object a name, to facilitate status and error reporting
	wav_out = cpe367_wav('wav_out',fpath_wav_out)
		
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
	# students - modify this section here

	# these parameters will need updating!
	#  you may also wish to add more parameters

	start_delay = 3000 #start delay is just to give time for my .wav player to catch up to loading the file, this can be removed
					   #with no effect on the output
	total_num_samples = 41040 + start_delay
	
	# allocate list of zeros to store an empty signal and create lists of trebel notes and bass notes
	xlist = [0] * total_num_samples
	tfqlist = [392,440,493.9,587.33,523.25,523.25,659.26,587.33]
	bfqlist = [98,196,164.8]

	# setup one note
	#  this implementation does not include harmonics or a decay
	amp = 10000

	#delay the start of the treble notes by 1 quarter note, as per the sheet music, and also set up the lenths of the 
	#treble and bass notes
	t_start = 4560 + start_delay
	b_start = 0 + start_delay
	t_durr = 4560
	b_durr = 13680

	#iterating through the treble and bass frequencies, and adding legths to both of them so the decay can actually work. 
	for i in range(8):
		addlen = 2000
		w1 = 2*math.pi*tfqlist[i]/sample_rate_hz
		add_note(xlist,amp,w1,t_start,t_durr+addlen,True)
		t_start += t_durr
	for i in range(3):
		addlen = 6000
		w2 = 2*math.pi*bfqlist[i]/sample_rate_hz
		add_note(xlist,amp,w2,b_start,b_durr+addlen,False)
		b_start += b_durr
		
		

	# students - well done!
	###############################################################
	###############################################################



	# write samples to output file one at a time
	for n in range(total_num_samples):
	
		# convert to signed int
		yout = int(round(xlist[n]))
		
		# output current sample 
		ostat = wav_out.write_wav(yout)
		if ostat == False: break
	
	# close input and output files
	#  important to close output file - header is updated (with proper file size)
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
	# fpath_wav_out = sys.argv[1]
	fpath_wav_out = 'music_synth.wav'

	# let's do it!
	return gen_wav(fpath_wav_out)
	
			
	
	
############################################
############################################
# call main function
if __name__ == '__main__':
	
	main()
	quit()
