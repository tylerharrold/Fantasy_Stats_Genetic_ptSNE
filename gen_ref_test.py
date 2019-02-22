from Genetics_Refactored import Genetics

gh = Genetics(maximum_possible_layers = 10 , bits_per_layer = 5, layer_crossbreed=True)

family = gh.breed_generation(10)

x = family[0]
y = family[1]

newfamily = gh.breed_generation(10, parents=[x,y])

p = newfamily[5]

Genetics.print_chromosomes(p)
a,b = Genetics.decode_dna(p)
print(a)
print(b)
