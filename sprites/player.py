import pygame
import config
from support import Tilesheet

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, game, groups, collision_sprites, name, stats):
        super().__init__(groups)
        self.game = game
        self.name = name
        self.z = config.layers['trees']
        self.level = config.player_levels[0]
        self.stats = stats      
        self.base_tiles = Tilesheet('assets/soldier/Soldier-Idle.png', 100, 100, 2, 6)
        self.walk_tiles = Tilesheet('assets/soldier/Soldier-Walk.png', 100, 100, 2, 8)
        self.animations = {
            'right_idle': [self.base_tiles.get_tile(0, 0),
                        self.base_tiles.get_tile(1, 0),
                        self.base_tiles.get_tile(2, 0),
                        self.base_tiles.get_tile(3, 0),
                        self.base_tiles.get_tile(4, 0),
                        self.base_tiles.get_tile(5, 0)],
            'left_idle': [self.base_tiles.get_tile(0, 1),
                        self.base_tiles.get_tile(1, 1),
                        self.base_tiles.get_tile(2, 1),
                        self.base_tiles.get_tile(3, 1),
                        self.base_tiles.get_tile(4, 1),
                        self.base_tiles.get_tile(5, 1)],
            'right': [self.walk_tiles.get_tile(0, 0),
                    self.walk_tiles.get_tile(1, 0),
                    self.walk_tiles.get_tile(2, 0),
                    self.walk_tiles.get_tile(3, 0),
                    self.walk_tiles.get_tile(4, 0),
                    self.walk_tiles.get_tile(5, 0),
                    self.walk_tiles.get_tile(6, 0),
                    self.walk_tiles.get_tile(7, 0)],
            'left': [self.walk_tiles.get_tile(0, 1),
                    self.walk_tiles.get_tile(1, 1),
                    self.walk_tiles.get_tile(2, 1),
                    self.walk_tiles.get_tile(3, 1),
                    self.walk_tiles.get_tile(4, 1),
                    self.walk_tiles.get_tile(5, 1),
                    self.walk_tiles.get_tile(6, 1),
                    self.walk_tiles.get_tile(7, 1)],
        }
        self.moving = False
        self.frame_index = 0
        self.status = 'right_idle'
        self.idle_statuses = ['right_idle', 'left_idle']
        self.image = pygame.transform.scale(self.animations[self.status][self.frame_index], (100,100))
        self.collision_sprites = collision_sprites
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate((-25, -25))          
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        self.speed = 200
        self.inventory = {
            'Health': 1,
            'Mana': 2,
        }
        self.max_hp = self.stats['VIT']
        self.hp = self.max_hp
        self.max_mp = self.stats['ERU']
        self.mp = self.max_mp

    def check_idle(self):
        if self.status not in self.idle_statuses:
            self.moving = True
        else:
            self.moving = False

    def animate(self, dt):
        self.frame_index += 4*dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = pygame.transform.scale(self.animations[self.status][int(self.frame_index)], (100,100))

    def input(self, actions):
        if actions['move up']:
            self.status = 'left'
            self.direction.y -= 1
        elif actions['move down']:
            self.status = 'right'
            self.direction.y = 1
        else:
            self.direction.y = 0

        if actions['move left']:
            self.status = 'left'
            self.direction.x -= 1
        elif actions['move right']:
            self.status = 'right'
            self.direction.x = 1
        else:
            self.direction.x = 0

    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
            self.moving = False

    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.pos.x += round(self.direction.x * self.speed * dt)
        self.hitbox.centerx = self.pos.x
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        self.pos.y += round(self.direction.y * self.speed * dt)
        self.hitbox.centery = self.pos.y
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')
 
    def collision(self, direction):
            for sprite in self.collision_sprites.sprites():
                if hasattr(sprite, 'hitbox'):
                    if sprite.hitbox.colliderect(self.rect):
                        if direction == 'horizontal':
                            if self.direction.x > 0:
                                self.rect.right = sprite.hitbox.left
                            if self.direction.x < 0:
                                self.rect.left = sprite.hitbox.right
                            self.pos.x = self.rect.centerx
                        if direction == 'vertical':
                            if self.direction.y > 0:
                                self.rect.bottom = sprite.hitbox.top
                            if self.direction.y < 0:
                                self.rect.top = sprite.hitbox.bottom
                            self.pos.y = self.rect.centery

    def update(self, dt):
        self.input(self.game.actions)
        self.get_status()
        self.check_idle()
        self.move(dt)
        self.animate(dt)

    