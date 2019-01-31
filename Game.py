import pygame
import sys
from Calculator import Calculator
from util import RANDOM, PERMUTATION
import util
from Renderer import Renderer




class Game():
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 640, 640
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.renderer = Renderer(self)
        self.calculator = Calculator(self)
        self.saved_points = []

        self.screenshot_requested = False

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
            self.renderer.draw(self.screen)
            if self.screenshot_requested:
                util.save_screenshot(self)
                self.screenshot_requested = False
            pygame.display.flip()



    def update(self, delta_time, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.calculator.thread_stop = True
                    self.calculator.thread_finished = False
                    self.calculator.reset_points = True
                if event.key == pygame.K_s:
                    self.screenshot_requested = True
                if event.key == pygame.K_1:
                    self.calculator.thread_stop = True
                    self.calculator.thread_finished = False
                    self.calculator.selected_algorithm = RANDOM
                    self.calculator.reset_points = False
                if event.key == pygame.K_2:
                    self.calculator.thread_stop = True
                    self.calculator.thread_finished = False
                    self.calculator.selected_algorithm = PERMUTATION
                    self.calculator.reset_points = False
        if not self.calculator.thread_running and not self.calculator.thread_finished:
            self.calculator.algorithm = self.calculator.selected_algorithm
            self.calculator.start_thread()
