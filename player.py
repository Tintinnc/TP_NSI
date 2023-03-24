import pygame


class Joueur(pygame.sprite.Sprite):
    """Assemble le joueur"""

    def __init__(self):
        super().__init__()
        self.sprite_sheet = pygame.image.load('Assets/Player/player.png')
        self.image = self.get_image(0, 0)
        self.rect = self.image.get_rect()

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image
