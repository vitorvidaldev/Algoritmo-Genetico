import numpy as np
import matplotlib.pyplot as plt
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
    selected_positions = []

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

        self.genotype = []
        for individual in self.population:
            integer, dec = str(individual).split('.')
            self.genotype.append(str(np.binary_repr(
                int(integer), width=6) + np.binary_repr(int(dec), width=14)))

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

        for i in range(len(self.population)):
            if self.population[i] > 20 or self.population[i] < -20:
                self.population[i] = random.uniform(-20, 20).__round__(4)
            else:
                self.population[i] = round(self.population[i], 4)

        self.fitness_function()

    def fitness_function(self):
        ''' Creates a list from the fitness value for each individual '''
        self.numeric_fitness = [
            round(math.sin(i) + math.cos(i * math.sqrt(3)), 4) for i in self.population]

    def selection(self):
        ''' Selects the 50 most apt individuos. If the random integer corresponds to a positive fitness value, the random integer is sorted one more time '''

        self.selected_positions = []
        for i in range(50):
            k = random.randint(0, 99)
            if self.numeric_fitness[k] < 0:
                self.selected_positions.append(k)
            else:
                self.selected_positions.append(random.randint(0, 99))

    def crossover(self):
        ''' Creates next generation of individuals '''

        for i in range(0, 100):
            first_position = self.selected_positions[random.randint(0, 49)]
            second_position = self.selected_positions[random.randint(0, 49)]

            first_ind = self.genotype[first_position]
            second_ind = self.genotype[second_position]

            # necessary conversion to change some sections of the string efficiently
            first_ind = list(first_ind)
            second_ind = list(second_ind)

            crossover_position = random.randint(0, 18)

            for i in range(crossover_position, 20):
                first_ind[i], second_ind[i] = second_ind[i], first_ind[i]

            first_ind = ''.join(first_ind)
            second_ind = ''.join(second_ind)

            self.genotype[first_position] = first_ind
            self.genotype[second_position] = second_ind

        self.genotype_to_fenotype()

    def mutation(self):
        ''' Changes one gene of one individual '''
        position = random.randint(0,19)
        individual = random.randint(0, 99)

        a = list(self.genotype[individual])
        if a[position] == '0':
            a[position] = '1'
        else :
            a[position] = '0'

        a = ''.join(a)
        self.genotype[individual] = a

    def print_table(self):
        for i in range(len(self.population)):
            print('individual: {} , genotype: {} , fitness: {}\n'.format(
                self.population[i], self.genotype[i], self.numeric_fitness[i]))
        print('\n')

    def graphic(self, x):
        y = (math.sin(x) + math.cos(x * math.sqrt(3)))
        return y

    def select_fittest(self):
        self.numeric_fitness.sort()
        print(self.numeric_fitness[0])

        x = np.linspace(-20, 20, 400)
        function = np.vectorize(self.graphic)
        plt.plot(x , function(x))
        plt.scatter(self.numeric_fitness[0], function(self.numeric_fitness[0]))
        plt.show()

    def loop(self, iterations):
        while iterations > 0:
            self.fenotype_to_genotype()  # generates the genotype for the current generation
            self.fitness_function()  # generates this generations numeric_fitness values
            self.selection()  # selects the 50 most apt individuals
            self.crossover() # creates next generation
            self.mutation()
            self.genotype_to_fenotype()
            iterations = iterations - 1
        self.select_fittest()

if __name__ == '__main__':
    ga = GeneticAlgorithm()
    ga.generate_population(100)
    ga.loop(50)
