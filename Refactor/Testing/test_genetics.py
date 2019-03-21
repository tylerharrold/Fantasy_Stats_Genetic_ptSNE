# file testing behavior of our Genetics class
from pathlib import Path
import sys
parent_dir = str(Path.cwd().parent)
sys.path.append(parent_dir)

from Genetics import Genetics as G
import unittest
import random as rand

# utility function for testing, returns intval for bitstring
def _bitstring_to_binary(bitstring):
    value = 0
    place_counter = 0
    for bit in reversed(bitstring):
        value = value + (2**place_counter * int(bit))
        place_counter = place_counter + 1
    return value

def _get_random_G():
    rand_max_layers = rand.randint(-256 , 256)
    rand_bits_per_layer = rand.randint(-256 , 256)
    gh = G(maximum_possible_layers=rand_max_layers , bits_per_layer=rand_bits_per_layer)
    return gh

class TestGenetics(unittest.TestCase):
    # make sure the basic setup works
    def test_basic(self):
        gh = G()

    # INITIALIZATION TESTS
    def test_maximum_possible_layers(self):
        gh = G(maximum_possible_layers=-1)
        self.assertTrue(gh.maximum_possible_layers > 0 and gh.maximum_possible_layers < 256)
        gh = G(maximum_possible_layers=0)
        self.assertTrue(gh.maximum_possible_layers > 0 and gh.maximum_possible_layers < 256)
        gh = G(maximum_possible_layers=255)
        self.assertTrue(gh.maximum_possible_layers > 0 and gh.maximum_possible_layers < 256)
        gh = G(maximum_possible_layers=256)
        self.assertTrue(gh.maximum_possible_layers > 0 and gh.maximum_possible_layers < 256)
        gh = G(maximum_possible_layers=1)
        self.assertTrue(gh.maximum_possible_layers > 0 and gh.maximum_possible_layers < 256)

    def test_bits_per_layer(self):
        gh = G(bits_per_layer=-1)
        self.assertTrue(gh.bits_per_layer > 0 and gh.bits_per_layer < 256)
        gh = G(bits_per_layer=0)
        self.assertTrue(gh.bits_per_layer > 0 and gh.bits_per_layer < 256)
        gh = G(bits_per_layer=255)
        self.assertTrue(gh.bits_per_layer > 0 and gh.bits_per_layer < 256)
        gh = G(bits_per_layer=256)
        self.assertTrue(gh.bits_per_layer > 0 and gh.bits_per_layer < 256)
        gh = G(bits_per_layer=1)
        self.assertTrue(gh.bits_per_layer > 0 and gh.bits_per_layer < 256)

    # TESTS FOR GENERATE_PERPLEXITY_PREPEND
    def test_perplexity_is_six_bits(self):
        gh = G()
        for i in range(10000):
            perp = gh._generate_perplexity_prepend()
            self.assertEqual(len(perp) , 6)

    def test_perplexity_is_between_5_50(self):
        gh = G()
        for i in range(10000):
            perp = gh._generate_perplexity_prepend()
            perp = _bitstring_to_binary(perp)
            self.assertTrue(perp >= 5 and perp <= 50)

    # TESTS FOR GENERATE STRUCTURE PREPEND
    def test_generate_structure_prepend(self):
        for i in range(10000):
            rand_max_layers = rand.randint(-256 , 256)
            rand_bits_per_layer = rand.randint(-256 , 256)
            gh = G(maximum_possible_layers=rand_max_layers , bits_per_layer=rand_bits_per_layer)
            structure = gh._generate_structure_prepend()
            layers , bits, _ = structure.split('t')
            layers = _bitstring_to_binary(layers)
            bits = _bitstring_to_binary(bits)
            self.assertEqual(layers, gh.maximum_possible_layers)
            self.assertEqual(bits , gh.bits_per_layer)

    def test_structure_len(self):
        for i in range(10000):
            gh = _get_random_G()
            dna = gh._generate_blueprint()
            # the length of the dna should be the max layers times bits per layer plus 6 perp bits plus 16 struct bitstring
            layers, bits , code = dna.split('t')
            layers = _bitstring_to_binary(layers)
            bits = _bitstring_to_binary(bits)
            self.assertTrue(len(dna) == (layers * bits + 6 + 8 + 8 + 2)) # the xtra 2 is the split char t's

    # test breed bitstrings






if __name__ == '__main__':
    unittest.main()
