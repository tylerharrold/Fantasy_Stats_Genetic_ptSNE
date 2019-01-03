# modified, oop version of genetic_helpers, designed to modify
# the interpreted sizes of layers dynamically

import random as rand

'''
    Note on schema:
        dna will comprise of 6 bits representing the perplexity (clamped between
        5 and 50). There will then be maximum_possible_layers number of layers,
        each composed of bits_per_layer bits. The first bit will be on/off. The
        subsequent bits will form the dimentionality specification for the layer
'''

class Genetics(object):
    def __init__(self, maximum_possible_layers , bits_per_layer, mutation_chance=0.1):
        self.maximum_possible_layers = maximum_possible_layers
        self.bits_per_layer = bits_per_layer
        self.mutation_chance = mutation_chance

    def _generate_blueprint(self):
        blueprint = ''

        for i in range(self.maximum_possible_layers):
            num_bits = self.bits_per_layer
            for k in range(num_bits):
                blueprint = blueprint + str(rand.randint(0,1))

        perplexity = self._generate_perplexity_prepend()
        blueprint = perplexity + blueprint
        return blueprint

    def _generate_perplexity_prepend(self):
        perplexity = rand.randint(5,50)
        bin_perp = '{0:06b}'.format(perplexity)
        return bin_perp

    def _random_splice_point(self, len):
        return rand.randint(1, len-2)

    def _breed_bitstrings(self, b1, b2):
        if len(b1) != len(b2):
            print("critical error")
            quit()

        m1 = self._mutate(b1)
        m2 = self._mutate(b2)
        splice_point = self._random_splice_point(len(m1))

        newchild = m1[:splice_point] + m2[splice_point:]
        return self._is_valid_structure(newchild)

    def _mutate(self, bitstring):
        mutant = ''
        for bit in bitstring:
            rand_val = rand.random()
            if rand_val <= self.mutation_chance:
                bit_to_flip = int(bit)
                if bit_to_flip:
                    bit_to_flip = 0
                else:
                    bit_to_flip = 1
                mutant = mutant + str(bit_to_flip)
            else:
                mutant = mutant + str(bit)
        return self._is_valid_structure(mutant)

    def _is_valid_structure(self, blueprint):
        MIN_PERPLEXITY = 5
        MAX_PERPLEXITY = 50
        perp_bits = blueprint[:6]
        intval = int(perp_bits , 2)
        if intval < 5:
            perp_bits = '{0:06b}'.format(MIN_PERPLEXITY)
        elif intval > 50:
            perp_bits = '{0:06b}'.format(MAX_PERPLEXITY)
        return perp_bits + blueprint[6:]

    def _read_blueprint_perplexity(self, blueprint):
        perplexity = blueprint[:6]
        return int(perplexity, 2)

    # public functions

    def breed_generation(self, gensize, parents=None):
        generation = []

        if parents is None:
            for i in range(gensize):
                generation.append(self._generate_blueprint())
        else:
            generation.append(parents[0])
            generation.append(parents[1])
            for i in range(gensize -2):
                newchild = self._breed_bitstrings(parents[0] , parents[1])
                generation.append(newchild)
        return generation

    def decode_dna(self, blueprint):
        blueprint_list = []
        perplexity = self._read_blueprint_perplexity(blueprint)

        blueprint = blueprint[6:]
        start = 0
        for i in range(len(blueprint) // self.bits_per_layer):
            end = start + self.bits_per_layer
            layer_bits = blueprint[start:end]
            active = int(layer_bits[0] , 2)
            if active:
                relevant_bits = layer_bits[1:]
                blueprint_list.append(int(relevant_bits , 2))

            start = end
        return perplexity , blueprint_list

    def print_chromosomes(self, blueprint):
        perplexity = blueprint[:6]
        print(perplexity)
        start = 0
        for i in range(len(blueprint) // self.bits_per_layer):
            end = start + self.bits_per_layer
            layer_bits = blueprint[start:end]
            print(layer_bits)
