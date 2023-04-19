import sys
from dataclasses import dataclass

import pygame
import pyscroll
import pytmx

from player import PNJ


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
    pnjs: list[PNJ]


class MapManager:
    """Va gérer toute les actions sur la map"""

    def __init__(self, screen, player):
        # Instanciation du menu de fin
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = "world"
        # Enregistre tout les point à activer afin de les rendre dynamique
        self.register_map("world", portals=[
            Portal(origin_world="world", origin_point="enter_house", destination_world="house",
                   destination_point="spawn_house"),
            Portal(origin_world="world", origin_point="enter_house2", destination_world="house2",
                   destination_point="spawn_house"),
            Portal(origin_world="world", origin_point="enter_house3", destination_world="house3",
                   destination_point="spawn_house"),
            Portal(origin_world="world", origin_point="enter_dungeon", destination_world="grotte",
                   destination_point="spawn_dungeon")
        ], pnjs=[
            PNJ("Niklas", nb_points=4)
        ])
        self.register_map("house", portals=[
            Portal(origin_world="house", origin_point="exit_house", destination_world="world",
                   destination_point="enter_house_exit")
        ])
        self.register_map("house2", portals=[
            Portal(origin_world="house2", origin_point="exit_house", destination_world="world",
                   destination_point="exit_house2"),
            Portal(origin_world="house2", origin_point="enter_cave", destination_world="cave",
                   destination_point="spawn_cave")
        ])

        self.register_map("cave", portals=[
            Portal(origin_world="cave", origin_point="exit_cave", destination_world="house2",
                   destination_point="spawn_house2")
        ])

        self.register_map("house3", portals=[
            Portal(origin_world="house3", origin_point="exit_house", destination_world="world",
                   destination_point="enter_house_exit3")
        ])

        self.register_map("grotte", portals=[
            Portal(origin_world="grotte", origin_point="exit_dungeon", destination_world="world",
                   destination_point="dungeon_exit_spawn"),
            Portal(origin_world="grotte", origin_point="mort", destination_world="grotte",
                   destination_point="spawn_dungeon")
        ], pnjs=[
            PNJ("DarkDante", nb_points=4)
        ])

        self.teleport_player("Player")
        self.teleport_pnjs()

    def check_collisions(self):
        """Vérifie s'il y a une collision avec un portail"""
        # Collision avec les portails
        for portal in self.get_map().portals:
            if portal.origin_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)
                if self.player.feet.colliderect(rect):
                    self.current_map = portal.destination_world
                    self.teleport_player(portal.destination_point)
                    return  # On sort de la méthode pour éviter de traiter les autres collisions

        # Collision avec les murs
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

        # Collision avec le carré menu pour lancer le menu de fin
        if self.current_map == "grotte":
            menu_square = pygame.Rect(644, 135, 26, 24)
            if self.player.feet.colliderect(menu_square):
                from jeux import Menu
                EndMenu = Menu(800, 600)
                EndMenu.End()

    def teleport_player(self, name):
        """Téléporte le joueur en enregistrant sa position initiale"""
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=None, pnjs=None):
        """Enregistre tous les objets dans la map rentrer dans le constructeur"""
        # Chargement map
        if pnjs is None:
            pnjs = []
        if portals is None:
            portals = []
        tmx_data = pytmx.util_pygame.load_pygame(f"../Assets/Carte/{name}.tmx")
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

        # recup PNJ ajoute au groupe
        for pnj in pnjs:
            group.add(pnj)
        # crée objet Map
        self.maps[name] = Map(name, walls, group, tmx_data, portals, pnjs)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def teleport_pnjs(self):
        for map in self.maps:
            map_data = self.maps[map]
            pnjs = map_data.pnjs

            for pnj in pnjs:
                pnj.load_points(map_data.tmx_data)
                pnj.teleport_spawn()

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        """Actualise les variables de collisions et le déplacement des pnj"""
        self.get_group().update()
        self.check_collisions()

        for pnj in self.get_map().pnjs:
            pnj.move()
