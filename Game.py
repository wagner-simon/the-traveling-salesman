import pygame
import sys
import random
import math
import threading
import itertools
import time
from Point import Point

RANDOM = 1
PERMUTATION = 2

ALGORITHM_NAMES = {
    RANDOM: "random",
    PERMUTATION: "permutation"
}


class Game():
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 640, 640
        self.background_color = 200, 200, 200
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.thread_running = False
        self.thread_stop = False
        self.thread_finished = False
        self.screenshot_requested = False
        self.algorithm = RANDOM
        self.selected_algorithm = self.algorithm
        self.percentage = 0
        self.amount_of_iterations = 1

        self.shortest_path = []
        self.random_points = []

        self.font = pygame.font.Font('assets/fonts/joystix monospace.ttf', 30)

        self.rangeX = (0, self.width)
        self.rangeY = (0, self.height)
        self.amount_of_points = 9

        self.marker_size = 9
        self.loading_bar_thickness = 4
        self.padding = 32

        self.current_iteration = 0

        self.shortest_distance = 0

        while True:
            delta_time = 1 / float(self.clock.tick(60))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            self.update(delta_time, events)
            self.screen.fill(self.background_color)
            self.draw()
            if self.screenshot_requested:
                self.save_screenshot()
                self.screenshot_requested = False
            pygame.display.flip()

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

    def save_screenshot(self):
        timestamp = int(time.time())
        pygame.image.save(self.screen, str(timestamp) + ".png")

    def draw(self):
        self.draw_shortest_path()
        for point in self.random_points:
            pygame.draw.rect(self.screen, (0, 0, 0), [point.x - math.floor(self.marker_size / 2), point.y - math.floor(self.marker_size / 2), self.marker_size, self.marker_size])

        text_distance = self.font.render(str(int(math.floor(self.shortest_distance))), False, (255, 0, 0))
        self.screen.blit(text_distance, (self.padding, self.padding))

        if self.algorithm == RANDOM:
            text_width, text_height = self.font.size(str(self.current_iteration))
            text_iterations = self.font.render(str(self.current_iteration), False, (255, 0, 0))
        if self.algorithm == PERMUTATION:
            text_width, text_height = self.font.size(str(round(self.percentage, 2)) + "%")
            text_iterations = self.font.render(str(round(self.percentage, 2)) + "%", False, (255, 0, 0))
            pygame.draw.rect(self.screen, (255, 0, 0), [0, self.height - self.loading_bar_thickness, self.percentage / 100 * self.width, self.loading_bar_thickness])
        self.screen.blit(text_iterations, (self.width - text_width - self.padding, self.height - text_height - self.padding))

        text_algorithm_type = self.font.render(ALGORITHM_NAMES[self.algorithm], False, (255, 0, 0))
        text_type_width, text_type_height = self.font.size(ALGORITHM_NAMES[self.algorithm])
        self.screen.blit(text_algorithm_type, (self.width - text_type_width - self.padding, self.padding))

    def draw_shortest_path(self):
        for index, point in enumerate(self.shortest_path):
            try:
                pygame.draw.line(self.screen, (100, 100, 100), (point.x, point.y), (self.shortest_path[index+1].x, self.shortest_path[index+1].y), 2)
            except IndexError:
                pass

    def update(self, delta_time, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.thread_stop = True
                    self.thread_finished = False
                if event.key == pygame.K_s:
                    self.screenshot_requested = True
                if event.key == pygame.K_1:
                    self.thread_stop = True
                    self.thread_finished = False
                    self.selected_algorithm = RANDOM
                if event.key == pygame.K_2:
                    self.thread_stop = True
                    self.thread_finished = False
                    self.selected_algorithm = PERMUTATION
        if not self.thread_running and not self.thread_finished:
            self.algorithm = self.selected_algorithm
            self.thread = threading.Thread(target=self.generate_random_points)
            self.thread.daemon = True
            self.thread.start()
