# modified, oop version of genetic_helpers, designed to modify
# the interpreted sizes of layers dynamically

import random as rand

'''
    Note on schema:
        dna will comprise of 6 bits representing the perplexity (clamped between
        5 and 50). There will then be maximum_possible_layers number of layers,
        each composed of bits_per_layer bits. The first bit will be on/off. The
        subsequent bits will form the dimentionality specification for the layer

        The DNA will prepend itself with information on maximum_possible_layers and bits_per_layer
        From a practicality perspective, the current design of Gentics limits the number of layers
        and the allowable bits per layer to a byte (255 values, not including zero)
'''

class Genetics(object):
    def __init__(self, maximum_possible_layers=8 , bits_per_layer=12, mutation_chance=0.1, layer_crossbreed=False):
        self.maximum_possible_layers = maximum_possible_layers
        if self.maximum_possible_layers <= 0 or self.maximum_possible_layers >= 256:
            self.maximum_possible_layers = 8
        self.bits_per_layer = bits_per_layer
        if self.bits_per_layer <= 1 or self.bits_per_layer >= 256:
            self.bits_per_layer = 12
        self.mutation_chance = mutation_chance
        if self.mutation_chance < 0 or self.mutation_chance > 1:
            self.mutation_chance = 0.1
        self.layer_crossbreed = layer_crossbreed

    def _generate_blueprint(self):
        blueprint = ''

        for i in range(self.maximum_possible_layers):
            num_bits = self.bits_per_layer
            for k in range(num_bits):
                blueprint = blueprint + str(rand.randint(0,1))

        perplexity = self._generate_perplexity_prepend()
        blueprint = perplexity + blueprint

        '''
        while not self._is_valid_structure(blueprint):
            blueprint = ''
            blueprint = self._generate_blueprint()
        '''
        blueprint = self._correct_genetic_errors(blueprint)


        structural_prepend = self._generate_structure_prepend()
        blueprint = structural_prepend + blueprint

        return blueprint

    def _generate_perplexity_prepend(self):
        perplexity = rand.randint(5,50)
        bin_perp = '{0:06b}'.format(perplexity)
        return bin_perp

    def _generate_structure_prepend(self):
        bits_per_layer = self.bits_per_layer
        max_layers = self.maximum_possible_layers
        bin_bits_per_layer = '{0:08b}'.format(bits_per_layer)
        bin_max_layers = '{0:08b}'.format(max_layers)
        bin_struct_prepend = bin_max_layers + 't' + bin_bits_per_layer + 't'
        return bin_struct_prepend

    def _random_splice_point(self, len):
        return rand.randint(1, len-2)

    def _breed_bitstrings(self, b1, b2):
        if self.layer_crossbreed:
            return self._breed_bitstrings_layerwise(b1,b2)
        else:
            if len(b1) != len(b2):
                print("critical error")
                quit()

            m1 = self._mutate(b1)
            m2 = self._mutate(b2)
            splice_point = self._random_splice_point(len(m1))

            newchild = m1[:splice_point] + m2[splice_point:]
            newchild = self._correct_genetic_errors(newchild)
            return newchild

    def _breed_bitstrings_layerwise(self, b1, b2):
        if len(b1) is not len(b2):
            print("critical error")
            quit()

        b1 = self._mutate(b1)
        b2 = self._mutate(b2)

        # using params, ascertain the amount of layer specifying genes plus perplexity specifyer
        num_genes = self.maximum_possible_layers + 1
        swap_segment = []

        for i in range(num_genes):
            rand_val = rand.random()
            if rand_val <= self.mutation_chance:
                swap_segment.append(1)
            else:
                swap_segment.append(0)

        # iterate through, swapping segments if directed to
        newchild = ""

        # see if we need to swap perplexities
        if swap_segment[0]:
            newchild = newchild + b2[:6]
        else:
            newchild = newchild + b1[:6]

        # potentially swap the rest
        start = 6
        end = start + self.bits_per_layer
        for i in range(self.maximum_possible_layers):
            if swap_segment[i+1]:
                newchild = newchild + b2[start:end]
            else:
                newchild = newchild + b1[start:end]
            start = end
            end = start + self.bits_per_layer

        newchild = self._correct_genetic_errors(newchild)
        return newchild

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
        mutant = self._correct_genetic_errors(mutant)
        return mutant

    def _correct_genetic_errors(self, blueprint):
        # we accept our structur_prepend-less blueprint (only perp and layers)
        perplexity = blueprint[:6]
        perplexity_int = int(perplexity , 2)
        while perplexity_int < 5 or perplexity_int > 50:
            perplexity = self._generate_perplexity_prepend()
            perplexity_int = int(blueprint[:6] , 2)
        blueprint = blueprint[6:]
        start = 0
        for i in range(len(blueprint) // self.bits_per_layer):
            end = start + self.bits_per_layer
            layer_bits = blueprint[start:end]
            active = int(layer_bits[0] , 2)
            if active:
                relevant_bits = layer_bits[1:]
                if int(relevant_bits , 2) < 0:
                    relevant_bits = '1' + relevant_bits[:-2] + '1'
                    blueprint = blueprint[:start] + relevant_bits + blueprint[end:]
            start = end
        return perplexity + blueprint


    '''
    def _is_valid_structure(self, blueprint):
        is_valid = True
        MIN_PERPLEXITY = 5
        MAX_PERPLEXITY = 50
        perplexity, structure = Genetics.decode_dna(blueprint, legacy_dna=True) #this is terribly lazy btw
        if perplexity < 5:
            is_valid = False
        elif perplexity > 50:
            is_valid = False

        for val in structure:
            if val <= 0:
                is_valid = False
        return is_valid
    '''

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
            max_layers , bits_per_layer , parent_one = parents[0].split('t')
            _ , _ , parent_two = parents[0].split('t')
            for i in range(gensize -2):
                newchild = self._breed_bitstrings(parent_one , parent_two)
                newchild = max_layers + 't' + bits_per_layer + 't' + newchild
                generation.append(newchild)
        return generation

    @staticmethod
    def decode_dna(blueprint , legacy_dna=False):
        if legacy_dna:
            bits_per_layer = 12
        else:
            max_layers , bits_per_layer , blueprint = blueprint.split('t')
            max_layers = int(max_layers , 2)
            bits_per_layer = int(bits_per_layer , 2)
        blueprint_list = []
        perplexity = int(blueprint[:6] , 2)

        blueprint = blueprint[6:]
        start = 0
        for i in range(len(blueprint) // bits_per_layer):
            end = start + bits_per_layer
            layer_bits = blueprint[start:end]
            active = int(layer_bits[0] , 2)
            if active:
                relevant_bits = layer_bits[1:]
                blueprint_list.append(int(relevant_bits , 2))

            start = end
        return perplexity , blueprint_list

    @ staticmethod
    def print_chromosomes(blueprint, legacy_dna=False):
        if legacy_dna:
            bits_per_layer = 12
        else:
            max_layers , bits_per_layer, blueprint = blueprint.split('t')
            max_layers = int(max_layers , 2)
            bits_per_layer = int(bits_per_layer , 2)

        perplexity = blueprint[:6]
        print(perplexity)
        blueprint = blueprint[6:]
        start = 0
        for i in range(len(blueprint) // bits_per_layer):
            end = start + bits_per_layer
            layer_bits = blueprint[start:end]
            print(layer_bits)
            start = end
