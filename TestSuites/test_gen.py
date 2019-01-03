# File for testing the behavior of our genetic_helpers.py script
from pathlib import Path
import sys
parent_dir = str(Path.cwd().parent)
sys.path.append(parent_dir)
import genetic_helpers as gh
import unittest

def _bitstring_to_binary(bitstring):
    value = 0
    place_counter = 0
    for bit in reversed(bitstring):
        value = value + (2**place_counter * int(bit))
        place_counter = place_counter + 1
    return value


class TestGenHelpers(unittest.TestCase):
    # make sure bitstring to binary method works
    def test_BitstoBin(self):
        ten = '0000001010'
        other_ten = '1010'
        self.assertEqual(10 , _bitstring_to_binary(ten))
        self.assertEqual(10, _bitstring_to_binary(other_ten))

    # make sure that the perplexity will always be between 5 and 50
    def test_Perplexity_limits(self):
        for i in range(10000):
            x = gh.generate_blueprint()
            perp = x[0:8]
            self.assertEqual(8 , len(perp))
            intval = _bitstring_to_binary(perp)
            self.assertTrue(intval >= 5 and intval <= 50)

    # make sure the length of the bitstring is 16 + 1 bytes
    def test_bitstring_len(self):
        for i in range(1000):
            x = gh.generate_blueprint()
            len_bitstring = len(x)
            len_expected = 8 + 16 * 8
            self.assertTrue(len_bitstring == len_expected)

    # test the blueprint perplexity
    def test_perplexity_func(self):
        #generate bitstrings
        for i in range(1000):
            bitstring = gh.generate_blueprint()
            perp = _bitstring_to_binary(bitstring[0:8])
            read_perp = gh._read_blueprint_perplexity(bitstring)
            self.assertEqual(perp, read_perp)

    # make sure that the translate function returns both perplexity and
    # a list of intvals between 0 and 8 in length
    def test_decode_blueprint(self):
        for i in range(1000):
            blueprint = gh.generate_blueprint()
            perp, layers = gh.decode_blueprint(blueprint)
            # types are correct
            self.assertTrue(type(perp) == int)
            self.assertTrue(type(layers) == list)
            lenlayers = len(layers)
            self.assertTrue(lenlayers >= 0 and lenlayers <=8)
            # each layer value is an int between zero and 32,768
            for i in layers:
                self.assertTrue(type(i) == int)
                self.assertTrue(i > 0 and i <= 32768)


    # make sure that mutate function returns a bitsring of appropriate length
    def test_mutate(self):
        for i in range(1000):
            bitstring = gh.generate_blueprint()
            mutant = gh.mutate(bitstring , 0.1)
            self.assertEqual(len(bitstring) , len(mutant))
            self.assertNotEqual(bitstring, mutant)



    # make sure mutate function returns a string that differs from original
    # NOTE this theoretically will fail sometimes, as perhaps a mutation never
    # triggers, however this occurance is unlikely and the majority of the time
    # at least one bit will be different

    # breed function testing
    def test_breed(self):
        for i in range(1000):
            b1 = gh.generate_blueprint()
            b2 = gh.generate_blueprint()
            c1,c2 = gh.breed_bitstrings(b1,b2)
            self.assertEqual(len(b1) , len(c1))
            self.assertEqual(len(b2) , len(c2))

if __name__ == '__main__':
    unittest.main()
