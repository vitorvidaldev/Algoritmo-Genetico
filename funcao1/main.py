import numpy as np
import matplotlib.pyplot as plt


def _fitness(x):
    y = np.sin(x) + np.cos(x * np.sqrt(3))
    return round(y, 10)


fitness = np.vectorize(_fitness)

x = np.linspace(start=-20, stop=20, num=200)  # population range
# plt.plot(x, fitness(x))
# plt.show()


def mutate(parents, fitness_function):
    n = int(len(parents))
    scores = fitness_function(parents)
    idx = scores > 0  # positive values only
    scores = scores[idx]
    parents = np.array(parents)[idx]

    # resample parents with probabilities proportional to fitness
    # then, add some noise for 'random' mutation
    children = np.random.choice(parents, size=n, p=scores/scores.sum())
    # add some noise to mutate
    children = children + np.random.uniform(-0.51, 0.51, size=n)
    return children.tolist()  # convert array to list


def GA(parents, fitness_function, popsize=100, max_iter=1000):
    History = []
    # initial parents; gen zero
    best_parent, best_fitness = _get_fittest_parent(
        parents, fitness)  # extract fittest individual

    # first plot the initial parents
    x = np.linspace(start=-20, stop=20, num=200)  # population range
    plt.plot(x, fitness_function(x))
    # plt.scatter(parents, fitness_function(parents), marker='x')

    # for each next generation
    for i in range(1, max_iter):
        parents = mutate(parents, fitness_function=fitness_function)

        curr_parent, curr_fitness = _get_fittest_parent(
            parents, fitness_function)  # extract fittest individual

        # update best fitness values
        if curr_fitness < best_fitness:
            best_fitness = curr_fitness
            best_parent = curr_parent

        curr_parent, curr_fitness = _get_fittest_parent(
            parents, fitness_function)
        # save generation MIN fitness
        History.append((i, np.min(fitness_function(parents))))

    # plt.scatter(parents, fitness_function(parents))
    plt.scatter(best_parent, fitness_function(
        best_parent), marker='.', c='b', s=200)
    plt.show()

    # return best parent
    print('generation {}| best fitness {}| best_parent {}'.format(
        i, best_fitness, best_parent))

    return best_parent, best_fitness, History


def _get_fittest_parent(parents, fitness):
    _fitness = fitness(parents)
    PFitness = list(zip(parents, _fitness))
    PFitness.sort(key=lambda x: x[1], reverse=False)
    best_parent, best_fitness = PFitness[0]
    return round(best_parent, 4), round(best_fitness, 4)


x = np.linspace(start=-20, stop=20, num=200)
init_pop = np.random.uniform(low=-20, high=20, size=100)

parent_, fitness_, history_ = GA(init_pop, fitness)
print('top parent {}, top fitness {}'.format(parent_, fitness_))
