import pygame


class AnimateSprite(pygame.sprite.Sprite):
    """Class charger de gérer les animations du personnage en fonction de sa direction"""

    def __init__(self, name):
        super().__init__()
        self.sprite_sheet = pygame.image.load(f'../Assets/Player/{name}.png')
        # Crée un dictionnaire pour lier le déplacement à l'image
        self.images = {
            "down": self.get_image(64, 0),
            "up": self.get_image(128, 352),
            "left": self.get_image(128, 0),
            "right": self.get_image(0, 0),
            "down2": self.get_image(0, 0),
            "up2": self.get_image(0, 96),
            "left2": self.get_image(0, 32),
            "right2": self.get_image(0, 64)
        }

    def get_image(self, x, y):
        """Importe le sprite du personnage et le decoupe"""
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image
