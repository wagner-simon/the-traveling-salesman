import operator
import random
import numpy as np
import pandas as pd
from Fitness import Fitness


def rank_paths(population):
    fitness_results = {}
    for i in range(0, len(population)):
        fitness_results[i] = Fitness(population[i]).path_fitness()
    return sorted(fitness_results.items(), key=operator.itemgetter(1), reverse=True)


def selection(pop_ranked, elite_size):
    selection_results = []
    df = pd.DataFrame(np.array(pop_ranked), columns=["Index", "Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_percentage'] = 100 * df.cum_sum / df.Fitness.sum()

    for i in range(0, elite_size):
        selection_results.append(pop_ranked[i][0])
    for i in range(0, len(pop_ranked) - elite_size):
        pick = 100 * random.random()
        for j in range(0, len(pop_ranked)):
            if pick <= df.iat[j, 3]:
                selection_results.append(pop_ranked[j][0])
                break
    return selection_results


def create_mating_pool(population, selection_results):
    _mating_pool = []
    for i in range(0, len(selection_results)):
        index = selection_results[i]
        _mating_pool.append(population[index])
    return _mating_pool


def breed(parent1, parent2):
    child_p1 = []

    gene_a = int(random.random() * len(parent1))
    gene_b = int(random.random() * len(parent1))

    start_gene = min(gene_a, gene_b)
    end_gene = max(gene_a, gene_b)

    for i in range(start_gene, end_gene):
        child_p1.append(parent1[i])

    child_p2 = [item for item in parent2 if item not in child_p1]

    child = child_p1 + child_p2
    return child


def breed_population(_mating_pool, elite_size):
    children = []
    length = len(_mating_pool) - elite_size
    pool = random.sample(_mating_pool, len(_mating_pool))

    for i in range(0, elite_size):
        children.append(_mating_pool[i])

    for i in range(0, length):
        child = breed(pool[i], pool[len(_mating_pool) - i - 1])
        children.append(child)
    return children


def mutate(individual, mutation_rate):
    for swapped in range(len(individual)):
        if random.random() < mutation_rate:
            swap_with = int(random.random() * len(individual))

            city1 = individual[swapped]
            city2 = individual[swap_with]

            individual[swapped] = city2
            individual[swap_with] = city1
    return individual


def mutate_population(population, mutation_rate):
    mutated_pop = []

    for index in range(0, len(population)):
        mutated_index = mutate(population[index], mutation_rate)
        mutated_pop.append(mutated_index)
    return mutated_pop


def next_generation(current_gen, elite_size, mutation_rate):
    pop_ranked = rank_paths(current_gen)
    selection_results = selection(pop_ranked, elite_size)
    mating_pool = create_mating_pool(current_gen, selection_results)
    children = breed_population(mating_pool, elite_size)
    next_gen = mutate_population(children, mutation_rate)
    return next_gen
