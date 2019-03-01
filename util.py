import pygame
import time

RANDOM = 1
PERMUTATION = 2

ALGORITHM_NAMES = {
    RANDOM: 'random',
    PERMUTATION: 'permutation'
}


def save_screenshot(game):
    timestamp = int(time.time())
    pygame.image.save(game.screen, 'screenshots/{0}.png'.format(str(timestamp)))
