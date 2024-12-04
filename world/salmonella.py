
from random import randint
import pygame
import pytmx
from sprites.camera.camera import Camera
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
        self.battle_timer = Timer(400)
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
                    self.determine_enemy()
            else:
                print('Safe')

    def determine_enemy(self):
        print('Enemy found')