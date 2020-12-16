import operator
import numpy as np
import pandas as pd
from random import random, sample
from Fitness import Fitness


def rank_paths(population):
    fitness_results = dict()
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
        pick = 100 * random()
        for j in range(0, len(pop_ranked)):
            if pick <= df.iat[j, 3]:
                selection_results.append(pop_ranked[j][0])
                break
    return selection_results


def create_mating_pool(population, selection_results):
    mating_pool = []
    for i in range(0, len(selection_results)):
        index = selection_results[i]
        mating_pool.append(population[index])
    return mating_pool


def breed(parent_1, parent_2):
    child = []

    gene_a = int(random() * len(parent_1))
    gene_b = int(random() * len(parent_2))

    start_gene = min(gene_a, gene_b)
    end_gene = max(gene_a, gene_b)

    for i in range(start_gene, end_gene):
        child.append(parent_1[i])

    for item in parent_2:
        if item not in child:
            child.append(item)

    return child


def breed_population(mating_pool, elite_size):
    children = []
    length = len(mating_pool) - elite_size
    pool = sample(mating_pool, len(mating_pool))

    for i in range(0, elite_size):
        children.append(mating_pool[i])

    for i in range(0, length):
        child = breed(pool[i + elite_size], pool[len(mating_pool) - i - 1])
        children.append(child)
    return children


def mutate(individual, mutation_rate):
    for swapped in range(len(individual)):
        if random() < mutation_rate:
            swap_with = int(random() * len(individual))

            point1 = individual[swapped]
            point2 = individual[swap_with]

            individual[swapped] = point2
            individual[swap_with] = point1
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
