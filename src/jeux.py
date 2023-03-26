import pygame
import pyscroll
import pytmx
from pygame import mixer

import player
from player import Joueur
from src.map import MapManager

pygame.init()


class Jeux:
    """Classe du déroulement du jeux"""

    def __init__(self, Widthw, Widhth):
        """Constructeur avec les paramétres de pygame"""
        # définie que la map s'appele world en principale
        self.map = "world"
        # Creation de la fenetre du jeu
        self.screen = pygame.display.set_mode((Widthw, Widhth))
        pygame.display.set_caption("Epic Adventures")
        # Lancement de la musique
        mixer.init()
        mixer.music.load('./Assets/Musique/BackgroundV2.wav')
        mixer.music.play(loops=-1)

        # instancier un joueur
        self.player = Joueur(0, 0)

        # integration de mapmanager
        self.map_manager = MapManager(self.screen, self.player)

    def handle_input(self):
        """Gére les input clavier"""
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')

    def update(self):
        self.map_manager.update()

    def running(self):
        """Gére l'éveille du jeu et sa fermeture avec une combinaison de touche F1"""
        # Limitatioàn de la vitesse du jeu
        clock = pygame.time.Clock()

        # boucle Jeu
        run = True
        while run:
            # rafraichissement de la page et dessin
            self.player.save_location()
            self.handle_input()
            self.update()
            # centrage de la caméra
            self.map_manager.draw()
            pygame.display.flip()

            # extinction du jeux
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        run = False
            clock.tick(60)
        pygame.quit()
