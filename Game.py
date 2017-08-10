import pygame, sys, random, math

class Game():
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 640, 640
        self.background_color = 200, 200, 200
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

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
        self.rangeX = (0, self.width)
        self.rangeY = (0, self.height)
        self.qty = 5  # or however many points you want

        self.random_points = []
        i = 0
        while i < self.qty:
            x = random.randrange(*self.rangeX)
            y = random.randrange(*self.rangeY)
            self.random_points.append((x, y))
            i += 1

    def draw(self):
        for coordinate in self.random_points:
            pygame.draw.rect(self.screen,(0, 0, 0),[coordinate[0] - math.floor(self.marker_size / 2),coordinate[1] - math.floor(self.marker_size / 2),self.marker_size,self.marker_size])


    def update(self, delta_time, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.generate_random_points()