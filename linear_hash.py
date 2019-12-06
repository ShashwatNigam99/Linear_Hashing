from __future__ import print_function
import sys

class LinearHashTable:
	def __init__(self):
		
		self.bucks = dict()
		
		# Initialize two buckets/blocks at the start
		self.bucks[0] = list()
		self.bucks[1] = list()
		self.bucks[0].append([])
		self.bucks[1].append([])

		# number of buckets = 1<<idx_hash
		self.idx_hash = 1
		
		# set number of blocks
		self.total_blocks = 2
		
		# Initially no entries are there in the hast table
		self.keys = 0
		
		# set the split pointer to the first bucket
		self.split_idx = 0

		# set a threshold value
		self.threshold = 0.75


	def getlen(self, x):
		return len(x)

	def calc_mod(self, x, mod):
		return x % (1<<mod)
	
	def add_bucket(self):

		add_idx = len(self.bucks)
		self.bucks[add_idx] = list()
		self.total_blocks+=1		
		to_update = list()
		self.bucks[add_idx].append([])
		
		# After filling full, split 
		if (self.getlen(self.bucks) == (1 << (self.idx_hash+1)+1)):
			self.idx_hash+=1
			self.split_idx = 0
		
		get_rem_idx = 1<<self.idx_hash
		upd_idx = add_idx - get_rem_idx
		get_rem_idx += get_rem_idx/2

		for i in range(0, self.getlen(self.bucks[upd_idx])):
			# reduce the number of blocks
			self.total_blocks-=1
			for val in self.bucks[upd_idx][i]:
				to_update.append(val)
		
		# initialize a new block 
		self.bucks[upd_idx] = list()
		
		self.bucks[upd_idx].append([])
		
		self.total_blocks+=1

		self.split_idx+=1
		
		# redistributing and putting into new blocks after calculating the new mod value
		for val in to_update:
			# calculate new mod value
			hash_val = self.calc_mod(val, self.idx_hash)

			# Put inside the appropriate block
			if hash_val < self.split_idx:
				hash_val = self.calc_mod(val, self.idx_hash + 1)
				last_block_idx = self.getlen(self.bucks[hash_val]) - 1

				# if the size of the block exceeds the maximum block size B
				if 4*(len(self.bucks[hash_val][last_block_idx])+1) > B:
					last_block_idx+=1
					self.total_blocks+=1
					self.bucks[hash_val].append(list())
				self.bucks[hash_val][last_block_idx].append(val)
		

	def insert(self, val):
		global output_buffer
		hash_val = self.calc_mod(val, self.idx_hash)
		
		if hash_val < self.split_idx:
			hash_val = self.calc_mod(val, self.idx_hash + 1)

		# Check if the value already exists in the hash table
		for i in range(0, self.getlen(self.bucks[hash_val])):
			if val in self.bucks[hash_val][i]:
				return 1

		# Value doesnt exist. Hence increment the number of keys
		self.keys+=1
		last_block_idx = self.getlen(self.bucks[hash_val]) - 1

		# if the size of the block exceeds the maximum block size B
		if 4*(len(self.bucks[hash_val][last_block_idx])+1) > B:
			self.total_blocks += 1
			self.bucks[hash_val].append(list())
			last_block_idx += 1

		self.bucks[hash_val][last_block_idx].append(val)
		output_buffer.append(val)
		
		if((self.keys * 4) / (self.total_blocks * B)*1.0 > self.threshold):
			self.add_bucket()


def main():
	input_buffer = []
	global output_buffer
	with open(file, 'r') as f:
		for line in f:
			input_buffer.append(int(line.strip()))

	for val in input_buffer:
		linearhash_table.insert(val)

	for val in output_buffer:
		print(val)
	

output_buffer = list()

if __name__ == "__main__":
	if len(sys.argv) != 2:
		sys.exit("Usage: python file.py input_file")
	
	B = 1024
	args = sys.argv
	file = args[1]

	linearhash_table = LinearHashTable()
	main()
