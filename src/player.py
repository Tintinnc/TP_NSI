import pygame


class Entity(pygame.sprite.Sprite):
    """Assemble le joueur"""

    def __init__(self, name, x, y):
        """Crée le joueur"""
        super().__init__()
        self.sprite_sheet = pygame.image.load(f'./Assets/Player/{name}.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        # Crée un dictionnaire pour lier le deplacement au image
        self.images = {
            "down": self.get_image(64, 0),
            "up": self.get_image(128, 352),
            "left": self.get_image(128, 0),
            "right": self.get_image(0, 0)

        }
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        # Réglage de la vitesse de déplacement
        self.speed = 3

    def save_location(self): self.old_position = self.position.copy()

    def change_animation(self, name):
        self.image = self.images[name]
        self.image.set_colorkey((0, 0, 0))

    def move_right(self):
        """Déplace le joueur a droite"""
        self.position[0] += self.speed

    def move_left(self):
        """Déplace le joueur a gauche"""
        self.position[0] -= self.speed

    def move_up(self):
        """Déplace le joueur vers le haut"""
        self.position[1] -= self.speed

    def move_down(self):
        """Déplace le joueur vers la droite"""
        self.position[1] += self.speed

    def update(self):
        """actualise la position du personnage"""
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, x, y):
        """importe le sprite du personnage et le decoupe"""
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image


class Joueur(Entity):

    def __init__(self):
        super().__init__("Eon", 0, 0)


class PNJ(Entity):

    def __init__(self, name, nb_points):
        super().__init__(name, 0, 0)
        self.nb_points = nb_points
        self.points = []
        self.current_point = 0
        self.name = name

    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()
    def charger_points(self, map):
        for num in range(1, self.nb_points+1):
            point = map.get_object(f'{self.name}_path{num}')
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)

