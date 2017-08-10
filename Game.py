import pygame, sys, random

class Game():
    def __init__(self):
        pygame.init()
        self.size = width, height = 1000, 1000
        self.background_color = 200, 200, 200
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.rangeX = (0, 1000)
        self.rangeY = (0, 1000)
        self.qty = 5  # or however many points you want

        self.random_points = []
        i = 0
        while i < self.qty:
            x = random.randrange(*self.rangeX)
            y = random.randrange(*self.rangeY)
            self.random_points.append((x, y))
            i += 1

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
            pygame.display.flip()


    def draw(self):
        for coordinate in self.random_points:
            pygame.draw.rect(self.screen,(0, 0, 0),[coordinate[0],coordinate[1],10,10])