import sys
import os
import pygame
from pygame import mixer

from player import Joueur
from src.map import MapManager

pygame.init()


class Jeux:
    """Classe du déroulement du jeu"""

    def __init__(self, Widthw, Widhth):
        """Constructeur avec les paramétres de pygame"""
        # définie que la map s'appele world en principale
        self.map = "world"
        # Creation de la fenetre du jeu
        self.screen = pygame.display.set_mode((Widthw, Widhth))
        pygame.display.set_caption("Twilight's Journey")
        # Lancement de la musique
        mixer.init()
        mixer.music.load('./Assets/Musique/BackgroundV2.wav')
        mixer.music.play(loops=-1)

        # instancier un joueur
        self.player = Joueur()

        # integration de mapmanager
        self.map_manager = MapManager(self.screen, self.player)

    def handle_input(self):
        """Gére les input clavier et souris"""
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


class Menu:
    """Classe du menu principal"""

    def __init__(self, width, height):
        """Constructeur avec les paramètres de pygame"""
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Menu principal")
        # Lancement de la musique
        mixer.init()
        mixer.music.load('./Assets/Musique/Menu_Background.mp3')
        mixer.music.play(loops=-1)
        # Charger l'image de fond
        self.background_image = pygame.image.load("./Assets/Images/menu_background.jpg")

        # Redimensionner l'image de fond pour qu'elle s'adapte à la taille de l'écran
        self.background_image = pygame.transform.scale(self.background_image, (width, height))

        # Créer les boutons
        font = pygame.font.Font("./Assets/Fronts/The Wild Breath of Zelda.otf", 48)
        self.play_button = font.render("Lancer la partie", True, (185, 159, 101))
        self.play_button_rect = self.play_button.get_rect(center=(width // 2, height // 2))

        # Créer le bouton "Exit Game"
        self.exit_button = font.render("Quitter le jeu", True, (185, 159, 101))
        self.exit_button_rect = self.exit_button.get_rect(center=(width // 2, height // 2 + 75))

    def run(self):
        """Gère l'affichage et la logique du menu"""
        clock = pygame.time.Clock()
        run = True
        while run:
            # Gérer les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Lancer la partie si le joueur a cliqué sur le bouton "Lancer la partie"
                    if self.play_button_rect.collidepoint(pygame.mouse.get_pos()):
                        self.touche()
                        self.scroll_text()
                        Jeux(self.width, self.height).running()

                        run = False

                    # Quitter le jeu si le joueur a cliqué sur le bouton "Quitter le jeu"
                    elif self.exit_button_rect.collidepoint(pygame.mouse.get_pos()):
                        run = False

            # Dessiner l'écran du menu
            self.screen.blit(self.background_image, (0, 0))
            self.play_button_rect.center = (self.width // 2, self.height // 2)
            self.screen.blit(self.play_button, self.play_button_rect)
            self.play_button_rect.center = (self.width // 2, self.height // 2)
            self.screen.blit(self.exit_button, self.exit_button_rect)
            pygame.display.flip()

            # Limiter la vitesse d'affichage à 60 images par seconde
            clock.tick(60)

        pygame.quit()

    def touche(self):
        """Affiche les touches que le joueur doit utiliser pour jouer"""

        # Dictionnaire des noms de fichiers des images des touches
        touch_images = {
            "↑": "keyboard_keys_up.png",
            "↓": "keyboard_keys_down.png",
            "→": "keyboard_keys_right.png",
            "←": "keyboard_keys_left.png",
            "F1": "keyboard_keys_F1.png"
        }

        # Diviser le texte en plusieurs lignes
        text_lines = ['↑: permet de se diriger vers le haut',
                      '↓: permet de se diriger vers le bas',
                      '→: permet de se diriger vers la droite',
                      '←: permet de se diriger vers la gauche',
                      'F1: permet de quitter le jeu']

        # Charger les images des touches
        touch_surfaces = {}
        for key, value in touch_images.items():
            touch_surfaces[key] = pygame.image.load(os.path.join("Assets/Images", value)).convert_alpha()

        for key, surface in touch_surfaces.items():
            new_size = (surface.get_width() // 2, surface.get_height() // 2)
            touch_surfaces[key] = pygame.transform.scale(surface, new_size)

        # Créer une surface pour chaque ligne de texte
        font = pygame.font.Font("./Assets/Fronts/The Wild Breath of Zelda.otf", 30)
        text_surfaces = []
        for line in text_lines:
            # Séparer la ligne en deux parties : la touche et la description
            split_line = line.split(": ")
            key = split_line[0]  # la touche est la première partie de la ligne
            desc = split_line[1]  # la description est la deuxième partie de la ligne

            # Combinaison de l'image de la touche et la description
            desc_surface = font.render(desc, True, (185, 159, 101))
            full_surface = pygame.Surface((touch_surfaces[key].get_width() + desc_surface.get_width() + 20,
                                           max(touch_surfaces[key].get_height(), desc_surface.get_height())))
            full_surface.fill((255, 255, 255))
            full_surface.blit(touch_surfaces[key],
                              (0, (full_surface.get_height() - touch_surfaces[key].get_height()) // 2))
            full_surface.blit(desc_surface, (
                touch_surfaces[key].get_width() + 20, (full_surface.get_height() - desc_surface.get_height()) // 2))
            text_surfaces.append(full_surface)

        # Obtenir les dimensions de la surface de texte
        text_width, text_height = text_surfaces[0].get_size()

        # Coordonnées initiales
        x = (self.width - text_width) // 2
        y = (self.height - (text_height * len(text_lines))) // 2

        # Afficher un écran noir
        self.screen.fill((255, 255, 255))

        # Afficher chaque ligne de texte à sa position respective
        for i in range(len(text_lines)):
            self.screen.blit(text_surfaces[i], (x, y + (text_height * i)))

        # Mettre à jour l'affichage
        pygame.display.flip()

        # Attendre 20 secondes
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 5000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        pygame.quit()
                        sys.exit()

    def scroll_text(self):
        # Diviser le texte en plusieurs lignes
        text_lines = ['Dans un royaume perdu, apparu de maniere inexpliquee un hero.',
                      'Il avait perdu sa memoire mais avait un objectif.',
                      'Retablir la paix dans le royaume.']

        # Créer une surface pour chaque ligne de texte
        font = pygame.font.Font("./Assets/Fronts/The Wild Breath of Zelda.otf", 30)
        text_surfaces = []
        for line in text_lines:
            text_surface = font.render(line, True, (185, 159, 101))
            text_surfaces.append(text_surface)

        # Obtenir les dimensions de la surface de texte
        text_width, text_height = text_surfaces[0].get_size()

        # Coordonnées initiales
        x = (self.width - text_width) // 2
        y = (self.height - (text_height * len(text_lines))) // 2

        # Afficher un écran noir
        self.screen.fill((0, 0, 0))

        # Afficher chaque ligne de texte à sa position respective
        for i in range(len(text_lines)):
            self.screen.blit(text_surfaces[i], (x, y + (text_height * i)))

        # Mettre à jour l'affichage
        pygame.display.flip()

        # Attendre 20 secondes
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 10000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        pygame.quit()
                        sys.exit()
