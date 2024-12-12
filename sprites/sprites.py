import pygame
import config
from config import layers

#for hitboxes
class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=config.layers['ground']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.5)

#for hitboxes
class Tree(Generic):
    def __init__(self, pos, surf, groups, z):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.8, -self.rect.height * 0.8)
