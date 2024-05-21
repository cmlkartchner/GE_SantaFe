### ALGORITHM ###

# SENSE: get agent neighbors' genotypes (either probabilistically across population or through sensing radius)

# ACT: add own genotype to pool of collected genotypes
#      select fit genotypes (e.g. using a tournament or randomly)
#      perform crossover on selected genotypes
#      mutate children
#      evaluate children
#      return most fit child

# UPDATE: if new genotype from act() is better than current genotype,
#         replace current genotype with new genotype
