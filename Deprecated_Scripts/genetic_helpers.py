# Helper functions controling the generation and breeding of neural networks
import random as rand
import tools

# Note on schema
# each layer is represented by BYTES_PER_LAYER, with the 1st bit of the byte string representing
# an on/off toggle, and the remaining bits representing layer capacity
# we will assume a byte will consistently be used to read the number of possible layers, as
# training a NN with more than 255 layers is infeasible

MAX_POSSIBLE_LAYERS = 8
BYTES_PER_LAYER = 2 #current max of 32,768 nodes per layer

# function returns a random bitstring blueprint for a neural network based on defined format
def generate_blueprint():
	blueprint = ''

	# generate the random bitstring
	for i in range(MAX_POSSIBLE_LAYERS):
		num_bits = BYTES_PER_LAYER * 8
		for k in range(num_bits):
			blueprint = blueprint + str(rand.randint(0,1))

	# prepend a byte representing the perplexity
	perplexity = _generate_perplexity_byte()
	blueprint = perplexity + blueprint

	return blueprint

# returns a bitstring representing the perplexity of ptsne model
# the perplexity will be between 5 and 50 (van der maaten recommends between
# 5 and 50)
def _generate_perplexity_byte():
	perplexity = rand.randint(5,50)
	# turn perplexity integer into a left-zero padded string
	bin_perp = '{0:08b}'.format(perplexity)
	return bin_perp

# function that will return the first n bits of a bitstring and return the int value it represents
def _read_blueprint_perplexity(blueprint):
	perplexity = blueprint[:8]
	return int(perplexity , 2)

# function that will read blueprint and return a list of integers represing the size of each layer
def decode_blueprint(blueprint):
	# int list representing the structure of our neural network
	blueprint_list = []
	perplexity = _read_blueprint_perplexity(blueprint)

	# read byte representation of every possible layer, initial values are set such that for loop sets them correctly
	# and ignores first byte (which is just a representation of max bytes in bitstring)
	blueprint = blueprint[8:] #we are done with perplexity
	start = 0
	for i in range(len(blueprint) // (8 * BYTES_PER_LAYER)):
		# move start and end to appropriate positions
		end = start + BYTES_PER_LAYER * 8

		# grab our relevant bits
		layer_bits = blueprint[start:end]

		# check to see if on/off and add them accordingly
		active = int(layer_bits[0] , 2)
		if active:
			relevant_bits = layer_bits[1:]
			blueprint_list.append(int(relevant_bits , 2))

		start = end

	return perplexity , blueprint_list

# function that ensures a perplexity between 5 and 50
def _is_valid_structure(blueprint):
	MIN_PERPLEXITY = 5
	MAX_PERPLEXITY = 50
	perp_bits = blueprint[:8]
	intval = int(perp_bits , 2)
	if intval < 5:
		perp_bits = '{0:08b}'.format(MIN_PERPLEXITY)
	elif intval > 50:
		perp_bits = '{0:08b}'.format(MAX_PERPLEXITY)

	return perp_bits + blueprint[8:]


# function that accepts two bitstring blueprints, and randomly crossbreeds them, returning two new bitstrings
def breed_bitstrings(b1 , b2):
	if (len(b1) != len(b2)):
		print("CRITICAL ERROR") #do this better later

	# grab relevant substrings
	btstr1 = b1
	btstr2 = b2

	splice_point = _random_splice_point(len(btstr1))

	# splice two new bitstrings together
	new_btstr1 = btstr1[:splice_point] + btstr2[splice_point:]
	new_btstr2 = btstr2[:splice_point] + btstr1[splice_point:]

	return _is_valid_structure(new_btstr1) , _is_valid_structure(new_btstr2)


# function that returns a random value within range
def _random_splice_point(len):
	return rand.randint(1 , len-2)


# function that returns random range for crossbreeding
# NOTE currently unused
def gen_random_range(len):
	start = len -1
	end = 0

	while (start >= end):
		start = rand.randint(0 , len-1)
		end = rand.randint(0 , len-1)

	return start , end


# function that accepts a bitstring and randomly mutates bits based on mutation_chance
def mutate(bitstring, mutation_chance):
	# grab the bitstring minus first byte
	#relevant_bits = bitstring[8:]
	#num_bits = len(relevant_bits)

	mutant = '000'

	for bit in bitstring[3:]:
		rand_val = rand.random()
		if custom_mutate_round(rand_val, mutation_chance):
			bit_to_flip = int(bit)
			if bit_to_flip:
				bit_to_flip = 0
			else:
				bit_to_flip = 1
			mutant = mutant + str(bit_to_flip)
		else:
			mutant = mutant + str(bit)

	return _is_valid_structure(mutant)


# function to return a generation of children of size gensize. If the list of
# parents is empty, this will return a completely new list of dna, otherwise
# it will breed from parents. For the moment a generation should be even.
def breed_generation(gensize, parents=None):
	generation = []
	if parents is None:
		for i in range(gensize):
			generation.append(generate_blueprint())
	else:
		generation.append(parents[0])
		generation.append(parents[1])
		for i in range((gensize - 2) // 2):
			c1,c2 = breed_bitstrings(parents[0] , parents[1])
			generation.append(c1)
			generation.append(c2)
	return generation

# custom rounding function for mutating bitstrings
def custom_mutate_round(random_value_float , mutation_chance):
	return (random_value_float <= mutation_chance)

# returns binary
def _bitstring_to_binary(bitstring):
    value = 0
    place_counter = 0
    for bit in reversed(bitstring):
        value = 2**value * int(bit)
        place_counter = place_counter + 1
    return value



##########################################################################
# FUNCTIONS PURELY FOR DEBUGGING                                         #
##########################################################################

# prints blueprint as representative bytes
def view_blueprint_bytes(blueprint, num_layers=MAX_POSSIBLE_LAYERS):
	start = 0
	end = 8
	for i in range(num_layers):
		end = end + 16
		start = end - 16
		layer_bits = blueprint[start:end]
		display = layer_bits[:7] + " " + layer_bits[7:]
		print(layer_bits)

def human_readable(dna):
	print(dna[:8])
	dna = dna[8:]
	for i in range(len(dna) // (BYTES_PER_LAYER * 8)):
		print(dna[:8] , " , " , dna[8:16])
		dna = dna[16:]

def random_bitstring(size):
	bitstring = ''

	for i in range(size):
		bitstring = bitstring + str(rand.randint(0,1))

	return bitstring
