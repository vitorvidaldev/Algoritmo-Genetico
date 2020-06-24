import numpy as np
# import matplotlib as plt
import random
import math
from bitstring import BitArray

# A classe GeneticAlgorithm é instânciada ao executar o arquivo.
# população = X indivíduos randômicos, levando em conta os limites superior e inferior estabelecidos.
# Conversão do fenótipo para genótipo. Separa-se a parte decimal da parte inteira de cada número e
# aplica-se uma conversão inteiro->binário para cada indivíduo. As strings resultantes são concatenadas.
# Conversão de genótipo para fenótipo ocorre de maneira análoga. A população anterior é sobrescrita

class GeneticAlgorithm():

    population = []
    genotype = []
    numeric_fitness = []

    tuple_x_limits = (-20, 20)


    def __init__(self):
        print("Class instance created")


    def generate_population(self, population_size):
        ''' Generates a random list of floating point numbers, given the range and the list size.'''

        lower_limit, upper_limit = self.tuple_x_limits

        for i in range(population_size):
            individual = random.uniform(lower_limit, upper_limit).__round__(4)
            self.population.append(individual)


    def fenotype_to_genotype(self):
        '''Converts the population values to a binary representation'''
        
        for individual in self.population:
            integer, dec = str(individual).split('.')
            self.genotype.append(str(np.binary_repr(int(integer), width=6) + np.binary_repr(int(dec), width=14)))


    def genotype_to_fenotype(self):
        '''Convets the binary string back to a floating point number. Overrides the previous population value'''

        new_fenotype = []

        for individual in self.genotype:
            integer_section = individual[:6]
            dec_section = individual[6:]

            integer_str = str(int(BitArray(bin=integer_section).int))
            dec_str = str(int(dec_section, 2))

            concat = integer_str + '.' + dec_str
            new_fenotype.append(float(concat))

        self.population = new_fenotype


    def fitness_function(self):
        ''' Creates a list from the fitness value for each individual '''
        self.numeric_fitness = [round(math.sin(i) + math.cos(i * math.sqrt(3)), 4) for i in self.population]


    def crossover(self):
        ''' TODO: Implement '''

    def mutation(self):
        ''' TODO: Implement '''

    def roulette_selection(self):
        ''' TODO: Implement '''
        


    def print_table(self):
        for i in range(len(self.population)):
            print('individual: {} , genotype: {} , fitness: {}\n'.format(self.population[i], self.genotype[i], self.numeric_fitness[i]))

if __name__ == '__main__':
    ga = GeneticAlgorithm()
    ga.generate_population(100)
    ga.fenotype_to_genotype()
    ga.genotype_to_fenotype()
    ga.fitness_function()
    ga.roulette_selection()
    ga.print_table()