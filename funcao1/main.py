import numpy as np
import matplotlib.pyplot as plt


def _fitness(x):
    y = np.sin(x) + np.cos(x * np.sqrt(3))
    return round(y, 10)


fitness = np.vectorize(_fitness)  # função fitness (eixo y)

x = np.linspace(start=-20, stop=20, num=400)  # população (eixo x)


def mutate(parents, fitness_function):
    n = int(len(parents))
    scores = fitness_function(parents)
    idx = scores > -2
    scores = scores[idx]
    parents = np.array(parents)[idx]

    children = np.random.choice(parents, size=n)
    # adição de ruído
    children = children + np.random.uniform(-0.51, 0.51, size=n)
    return children.tolist()  # retorna o eixo x após a mutação


def GA(parents, fitness_function, popsize=100, max_iter=10):
    History = []
    # gen zero
    best_parent, best_fitness = _get_fittest_parent(
        parents, fitness)  # extrai o individuo mais apto. (parents = posições aleatórias no eixo x, fitness = função da iteração)

    # plota o grafico da função
    x = np.linspace(start=-20, stop=20, num=1000)
    plt.plot(x, fitness_function(x))
    plt.scatter(parents, fitness_function(parents), marker='x')

    # próximas MAX_ITER gerações
    for i in range(1, max_iter):
        parents = mutate(parents, fitness_function=fitness_function)

        curr_parent, curr_fitness = _get_fittest_parent(
            parents, fitness_function)

        # atualiza os melhores valores de fitness
        if curr_fitness < best_fitness:
            best_fitness = curr_fitness
            best_parent = curr_parent

        curr_parent, curr_fitness = _get_fittest_parent(
            parents, fitness_function)
        # salva a menor coordenada
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
    _fitness = fitness(parents)  # 100 pontos no eixo y
    # lista de coordenas (x, y) da função
    PFitness = list(zip(parents, _fitness))
    # ordena a lista de coordenadas em ordem crescente de acordo com a variável do eixo x
    PFitness.sort(key=lambda x: x[1])
    # (best_parent = x, best_fitness = y) ordem crescente
    best_parent, best_fitness = PFitness[0]
    return round(best_parent, 4), round(best_fitness, 4)


x = np.linspace(start=-20, stop=20, num=400)  # 40 / 400 = 0.1 (step size)
# 100 posições randomicas entre -20 e 20 (eixo x).
init_pop = np.random.uniform(low=-20, high=20, size=100)

parent_, fitness_, history_ = GA(init_pop, fitness)
print('top parent {}, top fitness {}'.format(parent_, fitness_))
