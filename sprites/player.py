import pygame
import config
from support import Tilesheet

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, game, groups, collision_sprites, name, stats):
        super().__init__(groups)
        self.game = game #checks for game events
        self.name = name #should be retrieved for save files but then again i had no time :(
        self.z = config.layers['trees'] #setting the player layer for collision and rendering
        self.level = config.player_levels[0] #gets the initial level of the player
        self.stats = stats #player stats
        self.base_tiles = Tilesheet('assets/soldier/Soldier-Idle.png', 100, 100, 2, 6) #player tilesheet
        self.walk_tiles = Tilesheet('assets/soldier/Soldier-Walk.png', 100, 100, 2, 8) #player walk tilesheet
        #player anims
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
        self.moving = False #check for movement
        self.frame_index = 0 #cycling through tilesheet
        self.status = 'right_idle' #initial idle pose
        self.idle_statuses = ['right_idle', 'left_idle'] #idle poses
        self.image = pygame.transform.scale(self.animations[self.status][self.frame_index], (100,100)) #image blitting
        self.collision_sprites = collision_sprites #collision checks
        self.rect = self.image.get_rect(center=pos) #player rect for collision
        self.hitbox = self.rect.copy().inflate((-25, -25)) #hitbox for cameras
        self.direction = pygame.math.Vector2() #player direction
        self.pos = pygame.math.Vector2(self.rect.centerx, self.rect.centery) #player position
        self.speed = 200 #movespeed
        #player inventory for battle
        self.inventory = {
            'Health': 5,
            'Mana': 5,
            'Weapon': [] #i also had no time for weapons :(
        }
        self.weapon = None #no weapons :(
        self.max_hp = self.stats['VIT'] #max hp based on VITALITY
        self.hp = self.max_hp
        self.max_mp = self.stats['ERU'] #max mp based on ERUDITION
        self.mp = self.max_mp
        self.coins = 10 #coins for shop but no shop :(
        self.xp = 0 #initial xp

    #checks for movement
    def check_idle(self):
        if self.status not in self.idle_statuses:
            self.moving = True
        else:
            self.moving = False

    #animation handling
    def animate(self, dt):
        self.frame_index += 4*dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = pygame.transform.scale(self.animations[self.status][int(self.frame_index)], (100,100))

    #input handling
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

    #checks if player is idle
    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
            self.moving = False

    #movement handling
    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.pos.x += round(self.direction.x * self.speed * dt) #needs to be rounded or it'll turn out weird
        self.hitbox.centerx = self.pos.x
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal') #collision check

        self.pos.y += round(self.direction.y * self.speed * dt) #needs to be rounded or it'll turn out weird
        self.hitbox.centery = self.pos.y
        self.rect.centery = self.hitbox.centery
        self.collision('vertical') #collision check
 
    #collision handling
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

    #updating the player for animation, movement, and idling
    def update(self, dt):
        self.input(self.game.actions)
        self.get_status()
        self.check_idle()
        self.move(dt)
        self.animate(dt)

    