import pygame

from animation import AnimateSprite


class Entity(AnimateSprite):
    """Assemble le joueur"""

    def __init__(self, name, x, y):
        """Crée le joueur"""
        super().__init__(name)
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
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
        self.change_animation("right2")
        self.position[0] += self.speed

    def move_left(self):
        """Déplace le joueur a gauche"""
        self.change_animation("left2")
        self.position[0] -= self.speed

    def move_up(self):
        """Déplace le joueur vers le haut"""
        self.change_animation("up2")
        self.position[1] -= self.speed

    def move_down(self):
        """Déplace le joueur vers la droite"""
        self.change_animation("down2")
        self.position[1] += self.speed

    def update(self):
        """actualise la position du personnage"""
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


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
        self.speed = 0.8

    def move(self):
        current_point = self.current_point
        target_point = self.current_point + 1
        if target_point >= self.nb_points:
            target_point = 0
        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_down()
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_up()
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_left()
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_right()

        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    def teleport_spawn(self):

        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):

        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f'{self.name}_path{num}')
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)
