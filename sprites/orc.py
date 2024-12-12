from random import randint
import pygame
from support import Tilesheet


class Orc:
    def __init__(self, level, size):
        self.level = level
        self.size = size
        self.orc_tiles = Tilesheet('assets/Orc/Orc-Idle.png', 100, 100, 1, 6)


            
        self.max_hp = self.level.max_hp
        self.hp = self.max_hp
        self.damage_range = self.level.damage_range
        self.xp_range = self.level.xp_range
        self.gold = randint(self.level.gold_range[0], self.level.gold_range[1])
        self.image = pygame.transform.scale(self.orc_tiles.get_tile(0,0), (256,256))


    def attack(self):
        return randint(self.damage_range[0], self.damage_range[1])