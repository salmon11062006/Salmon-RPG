import pygame

class Tilesheet:
    def __init__(self, file_name, width, height, rows, cols):
        image = pygame.image.load(file_name).convert_alpha()
        self.tile_table = []
        for tile_x in range(0, cols):
            line = []
            self.tile_table.append(line)
            for tile_y in range(0, rows):
                rect = (tile_x * width, tile_y * height, width, height)
                line.append(image.subsurface(rect).convert_alpha())

    def get_tile(self, x, y):
        return self.tile_table[x][y]
    
class Timer:
    def  __init__(self, duration, func=None):
        self.duration = duration
        self.func = func
        self.time = 0
        self.start_time = 0
        self.active = False

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            if self.func and self.start_time != 0:
                self.func()
            self.deactivate()