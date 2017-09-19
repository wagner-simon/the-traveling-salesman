import pygame
import time
import math
from util import RANDOM, PERMUTATION, ALGORITHM_NAMES

class Renderer():
    def __init__(self, game):
        self.game = game
        self.background_color = 200, 200, 200
        self.marker_size = 9
        self.loading_bar_thickness = 4
        self.padding = 32
        
        self.font = pygame.font.Font('assets/fonts/joystix monospace.ttf', 30)


    def draw(self):
        self.game.screen.fill(self.background_color)
        self.draw_shortest_path()
        for point in self.game.calculator.random_points:
            pygame.draw.rect(self.game.screen, (0, 0, 0), [point.x - math.floor(self.marker_size / 2), point.y - math.floor(self.marker_size / 2), self.marker_size, self.marker_size])

        text_distance = self.font.render(str(int(math.floor(self.game.calculator.shortest_distance))), False, (255, 0, 0))
        self.game.screen.blit(text_distance, (self.padding, self.padding))

        if self.game.calculator.algorithm == RANDOM:
            text_width, text_height = self.font.size(str(self.game.calculator.current_iteration))
            text_iterations = self.font.render(str(self.game.calculator.current_iteration), False, (255, 0, 0))
        if self.game.calculator.algorithm == PERMUTATION:
            text_width, text_height = self.font.size(str(round(self.game.calculator.percentage, 2)) + "%")
            text_iterations = self.font.render(str(round(self.game.calculator.percentage, 2)) + "%", False, (255, 0, 0))
            pygame.draw.rect(self.game.screen, (255, 0, 0), [0, self.game.height - self.loading_bar_thickness, self.game.calculator.percentage / 100 * self.game.width, self.loading_bar_thickness])
        self.game.screen.blit(text_iterations, (self.game.width - text_width - self.padding, self.game.height - text_height - self.padding))

        text_algorithm_type = self.font.render(ALGORITHM_NAMES[self.game.calculator.algorithm], False, (255, 0, 0))
        text_type_width, text_type_height = self.font.size(ALGORITHM_NAMES[self.game.calculator.algorithm])
        self.game.screen.blit(text_algorithm_type, (self.game.width - text_type_width - self.padding, self.padding))

    def draw_shortest_path(self):
        for index, point in enumerate(self.game.calculator.shortest_path):
            try:
                pygame.draw.line(self.game.screen, (100, 100, 100), (point.x, point.y), (self.game.calculator.shortest_path[index+1].x, self.game.calculator.shortest_path[index+1].y), 2)
            except IndexError:
                pass

