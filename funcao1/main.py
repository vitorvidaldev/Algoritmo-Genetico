import numpy as np
import matplotlib.pyplot as plt


def CalculaFitness(x):
    y = np.sin(x) + np.cos(x * np.sqrt(3))
    return round(y, 4)


def mutate(parents, funcao_fitness):
    n = int(len(parents))
    scores = funcao_fitness(parents)
    scores = scores[scores > -2]
    parents = np.array(parents)[scores > -2]

    children = np.random.choice(parents, size=n)
    return children.tolist()  # retorna o eixo x após a mutação


def GA(parents, funcao_fitness, numero_geracoes=1000):
    histograma = []
    # geracao zero
    melhor_pai, melhor_fitness = GetFittestParent(
        parents, funcao_fitness)  # extrai o individuo mais apto. (parents = posições aleatórias no eixo x, fitness = função da iteração)

    # plota o grafico da função
    x = np.linspace(start=-20, stop=20, num=1000)
    plt.plot(x, funcao_fitness(x))
    plt.scatter(parents, funcao_fitness(parents), marker='o')

    # próximas gerações
    for i in range(1, numero_geracoes):
        parents = mutate(parents, funcao_fitness=funcao_fitness)

        pai_atual, fitness_atual = GetFittestParent(
            parents, funcao_fitness)

        # atualiza os melhores valores de fitness
        if fitness_atual < melhor_fitness:
            melhor_fitness = fitness_atual
            melhor_pai = pai_atual

        pai_atual, fitness_atual = GetFittestParent(
            parents, funcao_fitness)
        # salva a menor coordenada
        histograma.append((i, np.min(funcao_fitness(parents))))

    plt.scatter(parents, funcao_fitness(parents))
    plt.scatter(melhor_pai, funcao_fitness(
        melhor_pai), marker='.', c='b', s=200)
    plt.show()

    print('generation {}| best fitness {}| melhor_pai {}'.format(
        i, melhor_fitness, melhor_pai))

    return melhor_pai, melhor_fitness, histograma


def GetFittestParent(parents, fitness):
    _fitness = fitness(parents)
    # lista de coordenas (x, y) da função
    PFitness = list(zip(parents, _fitness))
    # ordena a lista de coordenadas em ordem crescente de acordo com a variável do eixo x
    PFitness.sort(key=lambda x: x[1])
    melhor_pai, melhor_fitness = PFitness[0]
    return round(melhor_pai, 4), round(melhor_fitness, 4)


fitness = np.vectorize(CalculaFitness)
tamanho_populacao = np.random.uniform(low=-20, high=20, size=5)
pai_, fitness_, histograma_ = GA(tamanho_populacao, fitness)
print('melhor pai {}, melhor fitness {}'.format(pai_, fitness_))