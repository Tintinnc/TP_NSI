from dataclasses import dataclass

import pygame
import pyscroll
import pytmx


@dataclass
class Portal:
    origin_world: str
    origin_point: str
    destination_world: str
    destination_point: str


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]


class MapManager:

    def __init__(self, screen, player):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = "world"

        self.register_map("world", portals=[
            Portal(origin_world="world", origin_point="enter_house", destination_world="house",destination_point="spawn_house")
        ])
        self.register_map("house", portals=[
            Portal(origin_world="house", origin_point="exit_house", destination_world="world",destination_point="enter_house_exit")
        ])

        self.teleport_player("Player")

    def check_collisions(self):
        # portails
        global rect
        for portal in self.get_map().portals:
            if portal.origin_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

            if self.player.feet.colliderect(rect):
                copy_portal = portal
                self.current_map = portal.destination_world
                self.teleport_player(copy_portal.destination_point)
        # Collision
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=None):
        # Chargement map
        if portals is None:
            portals = []
        tmx_data = pytmx.util_pygame.load_pygame(f"./Assets/Carte/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # liste rectangle collision
        walls = []

        for obj in tmx_data.objects:
            if obj.name == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        # Dessin groupe calque
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        group.add(self.player)

        # crée objet Map
        self.maps[name] = Map(name, walls, group, tmx_data, portals)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()
