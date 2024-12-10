from random import randint
import pygame
from support import Tilesheet


class Orc:
    def __init__(self, level, size):
        self.level = level
        self.size = size
        self.orc_small_tiles = Tilesheet('assets/Orc/Orc-Idle.png', 100, 100, 1, 6)
        self.orc_med_tiles = Tilesheet('assets/Orc/Orc-Idle.png', 100, 100, 1, 6)
        self.orc_big_tiles = Tilesheet('assets/Orc/Orc-Idle.png', 100, 100, 1, 6)
        self.frame_index = 0

        if self.size == 'med':
            self.animations = [pygame.transform.scale(self.orc_big_tiles.get_tile(0,0), (256,256)),
                               pygame.transform.scale(self.orc_big_tiles.get_tile(1,0), (256,256)),
                               pygame.transform.scale(self.orc_big_tiles.get_tile(2,0), (256,256)),
                               pygame.transform.scale(self.orc_big_tiles.get_tile(3,0), (256,256)),
                               pygame.transform.scale(self.orc_big_tiles.get_tile(4,0), (256,256)),
                               pygame.transform.scale(self.orc_big_tiles.get_tile(5,0), (256,256)),]
        elif self.size == 'small':
            self.animations = [pygame.transform.scale(self.orc_big_tiles.get_tile(0,0), (256,256)),
                               pygame.transform.scale(self.orc_big_tiles.get_tile(1,0), (256,256)),
                               pygame.transform.scale(self.orc_big_tiles.get_tile(2,0), (256,256)),
                               pygame.transform.scale(self.orc_big_tiles.get_tile(3,0), (256,256)),
                               pygame.transform.scale(self.orc_big_tiles.get_tile(4,0), (256,256)),
                               pygame.transform.scale(self.orc_big_tiles.get_tile(5,0), (256,256)),]
        elif self.size == 'big':
            self.animations = [pygame.transform.scale(self.orc_big_tiles.get_tile(0,0), (256,256)),
                               pygame.transform.scale(self.orc_big_tiles.get_tile(1,0), (256,256)),
                               pygame.transform.scale(self.orc_big_tiles.get_tile(2,0), (256,256)),
                               pygame.transform.scale(self.orc_big_tiles.get_tile(3,0), (256,256)),
                               pygame.transform.scale(self.orc_big_tiles.get_tile(4,0), (256,256)),
                               pygame.transform.scale(self.orc_big_tiles.get_tile(5,0), (256,256)),]
            
        self.max_hp = self.level.max_hp
        self.hp = self.max_hp
        self.damage_range = self.level.damage_range
        self.xp_range = self.level.xp_range
        self.gold = randint(self.level.gold_range[0], self.level.gold_range[1])

        self.image = self.animations[self.frame_index]

    def update(self,dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations):
            self.frame_index = 0
        self.image = pygame.transform.scale(self.animations[int(self.frame_index)], (256,256))

    def attack(self):
        return randint(self.damage_range[0], self.damage_range[1])