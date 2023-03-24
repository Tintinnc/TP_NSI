import pygame


class Joueur(pygame.sprite.Sprite):
    """Assemble le joueur"""

    def __init__(self, x, y):
        """Crée le joueur"""
        super().__init__()
        self.sprite_sheet = pygame.image.load('Assets/Player/player.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.speed = 3

    def move_right(self):
        """Déplace le joueur a droite"""
        self.position[0] += 3

    def move_left(self):
        """Déplace le joueur a gauche"""
        self.position[0] -= 3

    def move_up(self):
        """Déplace le joueur vers le haut"""
        self.position[1] -= 3

    def move_down(self):
        """Déplace le joueur vers la droite"""
        self.position[1] += 3

    def update(self):
        """actualise la position du personnage"""
        self.rect.topleft = self.position

    def get_image(self, x, y):
        """importe le sprite du personnage et le decoupe"""
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image
