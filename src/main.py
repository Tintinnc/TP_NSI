import pygame
from pygame import mixer

from jeux import Jeux

if __name__ == '__main__':
    pygame.init()
    game = Jeux(800,600)
    game.running()
