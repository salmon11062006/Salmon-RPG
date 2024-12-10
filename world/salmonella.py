
from random import randint
import pygame
import pytmx
from battle import Battle
from sprites.camera.camera import Camera
from sprites.orc import Orc
from sprites.player import Player
from sprites.sprites import Generic
from sprites.sprites import Tree
from state import State
import config
from support import Timer


class Salmonella(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.all_sprites = Camera()
        self.interaction_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.path_sprites = pygame.sprite.Group()
        self.map = True
        self.setup()
        self.battle_timer = Timer(0)
        self.count = 100

    def setup(self):
        map_data = pytmx.load_pygame('C:/Users/csalo/OneDrive/Documents/COMPUTER SCIENCE/ALGOPROFINAL/assets/map.tmx')

        for x, y, surf in map_data.get_layer_by_name('Ground').tiles():
            transformed_surf = pygame.transform.scale(surf, (32,32))
            Generic((x*32, y*32), transformed_surf, [self.all_sprites, self.path_sprites], config.layers['ground'])
        
        for x, y, surf in map_data.get_layer_by_name('Trees').tiles():
            transformed_surf = pygame.transform.scale(surf, (32,32))
            Tree((x*32, y*32), transformed_surf, [self.all_sprites,self.collision_sprites], config.layers['trees'])

        for x, y, surf in map_data.get_layer_by_name('Collision').tiles():
            transformed_surf = pygame.transform.scale(surf, (32,32))
            Tree((x*32, y*32), transformed_surf, [self.all_sprites, self.collision_sprites], config.layers['trees'])

        for obj in map_data.get_layer_by_name('Player'):
            if obj.name == 'Game Start':
                self.player_start = (obj.x, obj.y)

    def setup_player(self, pos, name, stats):
        map_data = pytmx.load_pygame('C:/Users/csalo/OneDrive/Documents/COMPUTER SCIENCE/ALGOPROFINAL/assets/map.tmx')
        self.player_setup = True
        for obj in map_data.get_layer_by_name('Player'):
            if obj.name == 'Game Start':
                self.player_start = (obj.x, obj.y)
                self.player = Player(pos, self.game, self.all_sprites, self.collision_sprites, name, stats)


    def update(self, dt, actions):
        self.game.WINDOW.fill(self.game.BLACK)
        self.all_sprites.custom_draw(self.player)     
        self.battle_timer.update()
        self.check_for_battle()
        self.all_sprites.update(dt)

    def check_for_battle(self):
        if self.player.moving:
            if not self.battle_timer.active:
                self.battle_timer.activate()
                random_number = randint(1,10)
                self.count -= random_number
                if self.count <= 0:
                    self.battle_timer.deactivate()
                    self.count = 100
                    orc = self.determine_enemy()
                    self.game.next_state = Battle(self.game, "Battle", orc, self.player)
                    self.game.next()
            else:
                print('Safe')

    def determine_enemy(self):
        size_num = randint(1,100)
        if size_num <= 25:
            size = 'small'
        elif size_num <= 65:
            size = 'med'
        else:
            size = 'big'
        level_num = randint(1,100)
        if level_num <= 80:
            if size == 'small':
                level = config.small_levels[self.player.level.level]
            elif size == 'med':
                level = config.med_levels[self.player.level.level]
            else:
                level = config.big_levels[self.player.level.level]
        if level_num <= 95:
            if size == 'small':
                if self.player.level.level == 0:
                    level = config.small_levels[self.player.level.level]
                else:
                    level = config.small_levels[self.player.level.level - 1]
            elif size == 'med':
                if self.player.level.level == 0:
                    level = config.med_levels[self.player.level.level]
                else:
                    level = config.med_levels[self.player.level.level - 1]
            else:
                if self.player.level.level == 0:
                    level = config.big_levels[self.player.level.level]
                else:
                    level = config.big_levels[self.player.level.level - 1]

        else:
            if size == 'small':
                if self.player.level.level < len(config.small_levels) - 1:
                    level = config.small_levels[self.player.level.level + 1]
                else:
                    level = config.small_levels[self.player.level.level]
            elif size == 'med':
                if self.player.level.level < len(config.med_levels) - 1:
                    level = config.med_levels[self.player.level.level + 1]
                else:
                    level = config.med_levels[self.player.level.level]
            else:
                if self.player.level.level < len(config.big_levels) - 1:
                    level = config.big_levels[self.player.level.level + 1]
                else:
                    level = config.big_levels[self.player.level.level]
        return Orc(level, size)