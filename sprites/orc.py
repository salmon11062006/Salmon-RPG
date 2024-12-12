from random import randint
import pygame
from support import Tilesheet


class Orc:
    def __init__(self, level, size):
        self.level = level #orc level
        self.size = size #orc size
        self.orc_tiles = Tilesheet('assets/Orc/Orc-Idle.png', 100, 100, 1, 6) #orc tilesheet
        self.max_hp = self.level.max_hp #max hp based on level
        self.hp = self.max_hp 
        self.damage_range = self.level.damage_range #damage range based on level and size
        self.xp_range = self.level.xp_range #xp range based on level and size
        self.gold = randint(self.level.gold_range[0], self.level.gold_range[1]) #gold range based on level and size
        self.image = pygame.transform.scale(self.orc_tiles.get_tile(0,0), (256,256)) #blitting the image


    def attack(self):
        return randint(self.damage_range[0], self.damage_range[1]) #random damage based on damage range