import random
import math
import itertools
import threading
from Point import Point
from util import RANDOM, PERMUTATION


class Calculator():
    def __init__(self, game):
        self.game = game

        self.width = self.game.width
        self.height = self.game.height

        self.thread_running = False
        self.thread_stop = False
        self.thread_finished = False

        self.algorithm = RANDOM
        self.selected_algorithm = self.algorithm
        self.percentage = 0
        self.amount_of_iterations = 1

        self.shortest_path = []
        self.random_points = []

        self.rangeX = (0, self.width)
        self.rangeY = (0, self.height)
        self.amount_of_points = 9

        self.current_iteration = 0

        self.shortest_distance = 0


    def start_thread(self):
        self.thread = threading.Thread(target=Calculator.generate_random_points, args=(self,))
        self.thread.daemon = True
        self.thread.start()

    def generate_random_points(self):
        self.thread_running = True
        self.thread_finished = False
        self.shortest_distance = 0
        self.shortest_path = []
        self.random_points = []
        while len(self.random_points) < self.amount_of_points:
            x = random.randrange(*self.rangeX)
            y = random.randrange(*self.rangeY)
            self.random_points.append(Point(x, y))
        self.amount_of_iterations = math.factorial(self.amount_of_points)
        self.get_distance()

    def get_distance(self):
        if self.algorithm == PERMUTATION:
            permutations = itertools.permutations(self.random_points)
        i = 0
        while True:
            if self.thread_stop:
                self.thread_stop = False
                self.thread_running = False
                return

            self.current_iteration = i

            if self.algorithm == RANDOM:
                current_path = random.sample(self.random_points, len(self.random_points))
            if self.algorithm == PERMUTATION:
                try:
                    current_path = next(permutations)
                except StopIteration:
                    self.thread_finished = True
                    self.thread_running = False
                    #self.screenshot_requested = True
                    return
                self.percentage = float(self.current_iteration + 1) / float(self.amount_of_iterations) * 100

            distance = 0
            for index, point in enumerate(current_path):
                if self.thread_stop:
                    self.thread_stop = False
                    self.thread_running = False
                    return
                try:
                    distance += point.distance_to(current_path[index+1])
                except IndexError:
                    pass
            if distance < self.shortest_distance or self.shortest_distance == 0:
                self.shortest_distance = distance
                self.shortest_path = current_path
            i += 1
