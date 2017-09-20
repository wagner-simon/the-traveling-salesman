import random
import math
import itertools
import threading
from Point import Point
from util import RANDOM, PERMUTATION


class Calculator:
    def __init__(self, game):
        self.game = game
        self.width = self.game.width
        self.height = self.game.height

        self.set_thread_states()

        self.set_counters()

        self.set_points()

        self.algorithm = RANDOM
        self.selected_algorithm = self.algorithm

    def set_thread_states(self):
        self.thread_running = False
        self.thread_stop = False
        self.thread_finished = False

    def set_counters(self):
        self.percentage = 0
        self.current_iteration = 0
        self.amount_of_iterations = 1
        self.shortest_distance = 0

    def set_points(self):
        self.shortest_path = []
        self.random_points = []

        self.rangeX = (0, self.width)
        self.rangeY = (0, self.height)
        self.amount_of_points = 9

    def start_thread(self):
        self.thread = threading.Thread(target=Calculator.reset_thread_variables, args=(self,))
        self.thread.daemon = True
        self.thread.start()

    def reset_thread_variables(self):
        self.thread_running = True
        self.thread_finished = False

        self.set_counters()

        self.set_points()

        self.generate_random_points()

        self.amount_of_iterations = math.factorial(self.amount_of_points)

        self.get_distance()

    def generate_random_points(self):
        while len(self.random_points) < self.amount_of_points:
            x = random.randrange(*self.rangeX)
            y = random.randrange(*self.rangeY)
            self.random_points.append(Point(x, y))

    def get_distance(self):
        if self.algorithm == PERMUTATION:
            self.permutations = itertools.permutations(self.random_points)
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
            self.current_path = random.sample(self.random_points, len(self.random_points))
        if self.algorithm == PERMUTATION:
            try:
                self.current_path = next(self.permutations)
            except StopIteration:               # stop if algorithm is finished
                self.thread_finished = True
                self.thread_running = False
                return
            self.percentage = float(self.current_iteration + 1) / float(self.amount_of_iterations) * 100

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
