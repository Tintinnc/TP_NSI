import pygame
from jeux import Jeux
from jeux import Menu

if __name__ == '__main__':
    pygame.init()
    menu = Menu(800, 600)
    if menu.run():
        game = Jeux(800, 600)
        game.running()
