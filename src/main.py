import pygame
from jeux import Jeux
from jeux import Menu
if __name__ == '__main__':
    # Lancement du menu
    pygame.init()
    menu = Menu(800, 600)
    if menu.run():
        # Si bouton lacer la partie lancement du jeu
        game = Jeux(800, 600)
        game.running()
