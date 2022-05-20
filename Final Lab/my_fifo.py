#!/usr/bin/env python

############################################
# this EMPTY python fifo class was written by dr fred depiero at cal poly
# distribution is unrestricted provided it is without charge and includes attribution

import statistics as stats

class my_fifo:
	
	
	############################################
	# constructor for signal history object
	def __init__(self,buff_len):

		#simplified the buffer creation and added our index tracker. 	
		self.buff_len = buff_len
		self.buff = buff_len*[0]
		self.curr_index = 0
		self.curr_max = 0
		
		# initialize more stuff, as needed	
	
	 
	############################################
	# update history with newest input and advance head / tail
	def update(self,current_in):
		"""
		:current_in: a new input value to add to recent history
		:return: T/F with any error message
		"""

		# students - need to make space for newest sample and include it in history
		
		#set the current index, which was updated on the last run of update, to the new data
		#then increment the index up and use modulo to wrap back around to the beginning of the list
		self.buff[self.curr_index] = current_in
		self.curr_index = (self.curr_index + 1)%self.buff_len
		self.curr_max = max(self.buff)
		return True

	

	############################################
	# get value from the recent history, specified by age_indx
	def get(self,age_indx):
		"""
		:indx: an index in the history
			age_indx == 0    ->  most recent historical value
			age_indx == 1    ->  next most recent historical value
			age_indx == M-1  ->  oldest historical value
		:return: value stored in the list of historical values, as requested by indx 
		"""
		
		#Because python accepts negative values for indices, we can just simply subract the age index from the current index
		val = self.buff[self.curr_index - age_indx]
		
		return val

	def maximum(self):
		return max(self.buff)
	
	def check_change(self,new):
		mean = stats.mean(self.buff)
		temp_fifo = self
		temp_fifo.update(new)
		new_mean = stats.mean(temp_fifo.buff)
		change = new_mean - mean
		return (0,change)[change>0]
