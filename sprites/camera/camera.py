import pygame
import config

class Camera(pygame.sprite.Group):

    def __init__(self, y_max, x_max):
        super().__init__()
        self.y_max = y_max 
        self.x_max = x_max 
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.y_min = 0
        self.x_min = 0
        l = 200
        t = 100
        w = self.display_surface.get_size()[0]
        h = self.display_surface.get_size()[1]
        self.camera_rect = pygame.Rect(l, t, w, h)

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - config.DISPLAY_W/2
        self.offset.y = player.rect.centery - config.DISPLAY_H/2
        if self.offset.x > self.x_max - self.camera_rect.width:
            self.offset.x = self.x_max - self.camera_rect.width
        if self.offset.y > self.y_max:
            self.offset.y = self.y_max
        if self.offset.x < self.x_min:
            self.offset.x = self.x_min
        if self.offset.y < self.y_min:
            self.offset.y = self.y_min
        
        for layer in config.layers.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
            