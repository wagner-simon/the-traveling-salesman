import random
import math
import itertools
import threading
from Point import Point
from util import RANDOM, PERMUTATION, GENETIC
from genetic_algorithm_functions import rank_paths, next_generation


class Calculator:

    def __init__(self, game):
        self.game = game
        self.width = self.game.width
        self.height = self.game.height

        self.set_thread_states()

        self.set_counters()

        self.set_points()

        self.set_genetic_variables()

        self.algorithm = RANDOM
        self.selected_algorithm = self.algorithm
        self.reset_points = True

    def set_thread_states(self):
        self.thread_running = False
        self.thread_stop = False
        self.thread_finished = False

    def set_counters(self):
        self.percentage = 0
        self.current_iteration = 0
        self.amount_of_permutations = 1
        self.shortest_distance = 0

    def set_points(self):
        # for printing the shortest path
        self.shortest_path = []
        self.random_points = []
        # for switching algorithms but keeping the points
        self.saved_points = []

        self.rangeX = (0, self.width)
        self.rangeY = (0, self.height)
        self.amount_of_points = 9

    def set_genetic_variables(self):
        self.pop_size = 100
        self.elite_size = 20
        self.mutation_rate = 0.01

    def start_thread(self):
        self.thread = threading.Thread(target=Calculator.reset_thread_variables, args=(self,))
        self.thread.daemon = True
        self.thread.start()

    def reset_thread_variables(self):
        self.thread_running = True
        self.thread_finished = False

        self.set_counters()

        self.set_points()

        if self.reset_points:
            self.generate_random_points()
            self.game.saved_points = self.random_points
        else:
            self.random_points = self.game.saved_points

        self.amount_of_permutations = math.factorial(self.amount_of_points)

        self.next_iteration()

    def generate_random_points(self):
        while len(self.random_points) < self.amount_of_points:
            x = random.randrange(*self.rangeX)
            y = random.randrange(*self.rangeY)
            self.random_points.append(Point(x, y))
        self.saved_points = self.random_points

    def next_iteration(self):
        if self.algorithm == PERMUTATION:
            self.permutations = itertools.permutations(self.random_points)
        if self.algorithm == GENETIC:
            self.population = self.initial_population
        i = 0
        while self.thread_running:
            if self.thread_stop:
                self.stop_thread()
            self.current_iteration = i
            self.get_new_path()
            self.calculate_shortest_distance()
            i += 1

    def stop_thread(self):
        self.thread_stop = False
        self.thread_running = False

    def get_new_path(self):
        if self.algorithm == RANDOM:
            self.current_path = self.create_path
        if self.algorithm == PERMUTATION:
            try:
                self.current_path = next(self.permutations)
            except StopIteration:  # stop if algorithm is finished
                self.thread_finished = True
                self.thread_running = False
                return
            self.percentage = float(self.current_iteration) / float(self.amount_of_permutations) * 100

        if self.algorithm == GENETIC:
            self.population = next_generation(self.population, self.elite_size, self.mutation_rate)
            best_path_index = rank_paths(self.population)[0][0]
            self.current_path = self.population[best_path_index]

    def calculate_shortest_distance(self):
        distance = 0
        for index, point in enumerate(self.current_path):
            if self.thread_stop:
                self.stop_thread()
            '''
                checks if algorithm was stopped so you don't have to wait until the 
                distance is calculated until the program ends 
            '''
            try:
                distance += point.distance_to(self.current_path[index + 1])
            except IndexError:
                pass
        self.set_shortest_distance(distance)

    def set_shortest_distance(self, distance):
        if distance < self.shortest_distance or self.shortest_distance == 0:
            self.shortest_distance = distance
            self.shortest_path = self.current_path

    # everything following is needed for the genetic algorithm

    @property
    def create_path(self):
        path = random.sample(self.random_points, len(self.random_points))
        return path

    @property
    def initial_population(self):
        population = []

        for i in range(0, self.pop_size):
            population.append(self.create_path)
        return population
