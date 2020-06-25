import numpy as np
import matplotlib.pyplot as plt
import random
import math
from bitstring import BitArray


class GeneticAlgorithm():

    population_x = []
    population_y = []
    genotype_x = []
    genotype_y = []
    genotype = []
    numeric_fitness = []
    selected_positions = []
    best = 0

    tuple_x_limits = (-512, 512)
    tuple_y_limits = (-512, 512)

    def __init__(self):
        print("Class instance created")

    def generate_population(self, population_size):
        ''' Generates a random list of floating point numbers, given the range and the list size.'''

        lower_x_limit, upper_x_limit = self.tuple_x_limits
        lower_y_limit, upper_y_limit = self.tuple_y_limits

        for i in range(population_size):
            individual_x = random.uniform(
                lower_x_limit, upper_x_limit).__round__(4)
            individual_y = random.uniform(
                lower_y_limit, upper_y_limit).__round__(4)
            self.population_x.append(individual_x)
            self.population_y.append(individual_y)

    def fenotype_to_genotype(self):
        '''Converts the population values to a binary representation'''

        self.genotype = []
        self.genotype_x = []
        self.genotype_y = []

        for individual in self.population_x:
            integer, dec = str(individual).split('.')
            self.genotype_x.append(str(np.binary_repr(int(integer), width=10) + np.binary_repr(int(dec), width=14)))

        for individual in self.population_y:
            integer, dec = str(individual).split('.')
            self.genotype_y.append(str(np.binary_repr(int(integer), width=10) + np.binary_repr(int(dec), width=14)))

    def genotype_to_fenotype(self):
        '''Convets the binary string back to a floating point number. Overrides the previous population value'''

        new_fenotype = []

        for individual in self.genotype_x:
            integer_section = individual[:10]
            dec_section = individual[10:]

            integer_str = str(int(BitArray(bin=integer_section).int))
            dec_str = str(int(dec_section, 2))

            concat = integer_str + '.' + dec_str
            new_fenotype.append(float(concat))

        self.population_x = new_fenotype

        for i in range(len(self.population_x)):
            if self.population_x[i] > 512 or self.population_x[i] < -512:
                self.population_x[i] = random.uniform(-20, 20).__round__(4)
            else:
                self.population_x[i] = round(self.population_x[i], 4)

        new_fenotype = []

        for individual in self.genotype_y:
            integer_section = individual[:10]
            dec_section = individual[10:]

            integer_str = str(int(BitArray(bin=integer_section).int))
            dec_str = str(int(dec_section, 2))

            concat = integer_str + '.' + dec_str
            new_fenotype.append(float(concat))

        self.population_y = new_fenotype

        for i in range(len(self.population_y)):
            if self.population_y[i] > 512 or self.population_y[i] < -512:
                self.population_y[i] = random.uniform(-20, 20).__round__(4)
            else:
                self.population_y[i] = round(self.population_y[i], 4)

        self.fitness_function()

    def fitness_function(self):
        ''' Creates a list from the fitness value for each individual '''
        self.numeric_fitness = [
            round(-(self.population_y[i] + 47) * math.sin(math.sqrt(abs((self.population_x[i] / 2) + (self.population_y[i] + 47)))) - self.population_x[i] * math.sin(math.sqrt(abs(self.population_x[i] - self.population_y[i] + 47))), 4) for i in range(len(self.population_x))]


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

            first_ind = self.genotype_x[first_position]
            second_ind = self.genotype_x[second_position]

            # necessary conversion to change some sections of the string efficiently
            first_ind = list(first_ind)
            second_ind = list(second_ind)

            crossover_position = random.randint(0, 23)

            for i in range(crossover_position, 20):
                first_ind[i], second_ind[i] = second_ind[i], first_ind[i]

            first_ind = ''.join(first_ind)
            second_ind = ''.join(second_ind)

            self.genotype_x[first_position] = first_ind
            self.genotype_x[second_position] = second_ind

            first_position = self.selected_positions[random.randint(0, 49)]
            second_position = self.selected_positions[random.randint(0, 49)]

            first_ind = self.genotype_y[first_position]
            second_ind = self.genotype_y[second_position]

            # necessary conversion to change some sections of the string efficiently
            first_ind = list(first_ind)
            second_ind = list(second_ind)

            crossover_position = random.randint(0, 23)

            for i in range(crossover_position, 20):
                first_ind[i], second_ind[i] = second_ind[i], first_ind[i]

            first_ind = ''.join(first_ind)
            second_ind = ''.join(second_ind)

            self.genotype_y[first_position] = first_ind
            self.genotype_y[second_position] = second_ind

        self.genotype_to_fenotype()

    def mutation(self):
        ''' Changes one gene of one individual '''
        position = random.randint(0, 23)
        individual = random.randint(0, 99)

        a = list(self.genotype_x[individual])
        if a[position] == '0':
            a[position] = '1'
        else:
            a[position] = '0'

        a = ''.join(a)
        self.genotype_x[individual] = a

        position = random.randint(0, 23)
        individual = random.randint(0, 99)

        a = list(self.genotype_y[individual])
        if a[position] == '0':
            a[position] = '1'
        else:
            a[position] = '0'

        a = ''.join(a)
        self.genotype_y[individual] = a

    def graphic(self, x):
        y = (math.sin(x) + math.cos(x * math.sqrt(3)))
        return y

    def select_fittest(self):
        self.numeric_fitness.sort()
        if self.numeric_fitness[0] < self.best:
            self.best = self.numeric_fitness[0]
        print(self.best)

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
    ga.loop(100)
