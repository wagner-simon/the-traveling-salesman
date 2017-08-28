import pygame, sys, random, math
from Point import Point
from random import shuffle


class Game():
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 640, 640
        self.background_color = 200, 200, 200
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.rangeX = (0, self.width)
        self.rangeY = (0, self.height)
        self.amount_of_coordinates = 5  # or however many points you want
        self.amount_of_iterations = 10
        self.marker_size = 9

        self.generate_random_points()

        while True:
            delta_time = 1 / float(self.clock.tick(60))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            self.screen.fill(self.background_color)
            self.draw()
            self.update(delta_time, events)
            pygame.display.flip()

    def generate_random_points(self):
        self.random_points = []
        while len(self.random_points) < self.amount_of_coordinates:
            x = random.randrange(*self.rangeX)
            y = random.randrange(*self.rangeY)
            self.random_points.append((x, y))
        self.get_distance()
        #self.point = Point(self.random_points[0][0], self.random_points[0][1])
        #print(self.point.distance_to(Point(self.random_points[1][0], self.random_points[1][1])))

    def get_distance(self):
        i = 0
        while i <= self.amount_of_iterations:
            shuffle(self.random_points)
            self.point = Point(self.random_points[0][0], self.random_points[0][1])
            self.distance = self.point.distance_to(Point(self.random_points[1][0], self.random_points[1][1]))
            self.distance = self.distance + self.point.distance_to(Point(self.random_points[2][0], self.random_points[2][1]))
            self.distance = self.distance + self.point.distance_to(Point(self.random_points[3][0], self.random_points[3][1]))
            self.distance = self.distance + self.point.distance_to(Point(self.random_points[4][0], self.random_points[4][1]))
            print self.distance
            i += 1


    def draw(self):
        for coordinate in self.random_points:
            pygame.draw.rect(self.screen,(0, 0, 0),[coordinate[0] - math.floor(self.marker_size / 2),coordinate[1] - math.floor(self.marker_size / 2),self.marker_size,self.marker_size])

    def update(self, delta_time, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.generate_random_points()