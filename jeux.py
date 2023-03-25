import pygame
import pyscroll
import pytmx
from pygame import mixer

import player
from player import Joueur

pygame.init()


class Jeux:
    """Classe du déroulement du jeux"""

    def __init__(self, Widthw, Widhth):
        """Constructeur avec les paramétres de pygame"""
        # Creation de la fenetre du jeu
        self.screen = pygame.display.set_mode((Widthw, Widhth))
        pygame.display.set_caption("The Legend of Combat")
        # Lancement de la musique
        mixer.init()
        mixer.music.load('Assets/Musique/Background.wav')
        mixer.music.play(loops = -1)

        # Chargement map
        tmx_data = pytmx.util_pygame.load_pygame("Assets/Carte/Carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # instancier un joueur
        player_position = tmx_data.get_object_by_name("Player")
        self.player = Joueur(player_position.x,player_position.y)

        # liste rectangle collision
        self.murs = []

        for obj in tmx_data.objects:
            if obj.name == "collision":
                self.murs.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        # Dessin groupe calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=2)
        self.group.add(self.player)

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
        self.group.update()

        #verif colision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.murs) > -1:
                sprite.move_back()
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
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
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
