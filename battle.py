from random import randint
import pygame
import config
from game_over import GameOver
from menu import Menu
from misc.action import Attack, Potion, Spell
from state import State
from battle_complete import BattleComplete

class Battle(State, Menu):
    def __init__(self, game, name, enemy, player):
        State.__init__(self, game, name)
        Menu.__init__(self, game)
        self.enemy = enemy #enemy stats
        self.player = player #player stats
        #image loading
        self.enemy_image = pygame.transform.scale(self.enemy.image, (256,256))
        self.enemy_rect = self.enemy_image.get_rect(topright=(config.DISPLAY_W, -40))
        self.player_image = pygame.transform.scale(self.player.image, (256,256))
        self.player_flip =  pygame.transform.flip(self.player_image, True, False)
        self.player_rect = self.player_flip.get_rect(bottomleft=(0, config.DISPLAY_H + 20))
        self.player_banner = pygame.transform.scale(pygame.image.load('assets/ui-banner.png').convert_alpha(), (500, 40))
        self.enemy_banner = pygame.transform.scale(pygame.image.load('assets/ui-banner.png').convert_alpha(), (500, 40))
        
        #more image loading
        self.player_banner_rect = self.player_banner.get_rect(topleft=(20, 50))
        self.enemy_banner_rect = self.enemy_banner.get_rect(topleft=self.player_banner_rect.bottomleft)
        self.lunge_img = pygame.transform.scale(pygame.image.load('assets/ui-banner2.png').convert_alpha(), (150, 50))
        self.heavystrike_img = pygame.transform.scale(pygame.image.load('assets/ui-banner2.png').convert_alpha(), (150, 50))
        self.fireball_img = pygame.transform.scale(pygame.image.load('assets/ui-banner2.png').convert_alpha(), (150, 50))
        self.shieldthrow_img = pygame.transform.scale(pygame.image.load('assets/ui-banner2.png').convert_alpha(), (150, 50))

        #even more image loading related stuff(this time for the rectangles, to be used for positioning)
        self.lunge_rect = self.lunge_img.get_rect(bottomleft=(40, self.player_banner_rect.centery + 320))
        self.heavystrike_rect = self.heavystrike_img.get_rect(bottomleft=self.lunge_rect.bottomright)
        self.fireball_rect = self.fireball_img.get_rect(bottomleft=self.heavystrike_rect.bottomright)
        self.shieldthrow_rect = self.shieldthrow_img.get_rect(bottomleft=self.fireball_rect.bottomright)
        self.ribbon_image = pygame.transform.scale(pygame.image.load('assets/ui-banner.png').convert_alpha(), (150, 50))
        self.font = pygame.font.Font('assets/8-bit-hud.ttf', 15)
        self.font2 = pygame.font.Font('assets/8-bit-hud.ttf', 5)

        #text within the images
        self.lunge_text = self.font2.render('Lunge 5mp', True, self.game.BLACK)
        self.heavystrike_text = self.font2.render('Heavy Strike 7mp', True, self.game.BLACK)
        self.fireball_text = self.font2.render('Fireball 5mp', True, self.game.BLACK)
        self.shieldthrow_text = self.font2.render('Shield Throw 3mp', True, self.game.BLACK)
        self.melee_text = self.font2.render('Melee Attack', True, self.game.BLACK)
        self.potion_text = self.font2.render(f'Health Potion: {self.player.inventory["Health"]}', True, self.game.BLACK)
        self.mana_text = self.font2.render(f'Mana Potion: {self.player.inventory["Mana"]}', True, self.game.BLACK)
        self.flee_text = self.font2.render('Flee', True, self.game.BLACK)

        #to position the text
        self.lunge_text_rect = self.lunge_text.get_rect(center=(self.lunge_rect.centerx, self.lunge_rect.centery))
        self.heavystrike_text_rect = self.heavystrike_text.get_rect(center=(self.heavystrike_rect.centerx, self.heavystrike_rect.centery))
        self.fireball_text_rect = self.fireball_text.get_rect(center=(self.fireball_rect.centerx, self.fireball_rect.centery))
        self.shieldthrow_text_rect = self.shieldthrow_text.get_rect(center=(self.shieldthrow_rect.centerx, self.shieldthrow_rect.centery))

        #more positioning
        self.melee_rect = self.ribbon_image.get_rect(bottomleft=self.heavystrike_rect.topleft)
        self.potion_rect = self.ribbon_image.get_rect(topleft=self.melee_rect.topright)
        self.mana_rect = self.ribbon_image.get_rect(topleft=self.potion_rect.topright)
        self.flee_rect = self.ribbon_image.get_rect(topleft=self.mana_rect.topright)

        #even more positioning
        self.melee_text_rect = self.melee_text.get_rect(center=self.melee_rect.center)
        self.potion_text_rect = self.potion_text.get_rect(center=self.potion_rect.center)
        self.mana_text_rect = self.mana_text.get_rect(center=self.mana_rect.center)
        self.flee_text_rect = self.flee_text.get_rect(center=self.flee_rect.center)

        #header text for encounters
        self.header_text = 'You encountered an enemy!'
        self.header = self.font.render(self.header_text, True, self.game.BLACK)
        self.header_rect = self.header.get_rect(center=self.player_banner_rect.center)

        #header text for enemy attacks
        self.enemy_header_text = ''
        self.enemy_header = self.font.render(self.enemy_header_text, True, self.game.BLACK)
        self.enemy_header_rect = self.enemy_header.get_rect(center=self.enemy_banner_rect.center)

        #enemy hp
        self.enemy_hp = self.font.render(f'HP: {self.enemy.hp}', True, self.game.BLACK)
        self.enemy_hp_rect = self.enemy_hp.get_rect(center=(self.enemy_rect.centerx, self.enemy_rect.centery + 50))

        #player hp and mp
        self.hp = self.font.render(f'HP: {self.player.hp}', True, self.game.BLACK)
        self.hp_rect = self.hp.get_rect(bottomleft=self.melee_rect.topleft)
        self.mp = self.font.render(f'MP: {self.player.mp}', True, self.game.BLACK)
        self.mp_rect = self.mp.get_rect(bottomleft=self.hp_rect.topleft)

        #cursor positioning and selection verification
        self.menu_options = {
            0: (self.melee_text_rect.centerx - 40, config.DISPLAY_H - 75),
            1: (self.potion_text_rect.centerx - 40, config.DISPLAY_H - 75),
            2: (self.mana_text_rect.centerx - 40, config.DISPLAY_H - 75),
            3: (self.flee_text_rect.centerx - 40, config.DISPLAY_H - 75),
            4: (self.lunge_text_rect.centerx - 40, config.DISPLAY_H - 25),
            5: (self.heavystrike_text_rect.centerx - 40, config.DISPLAY_H - 25),
            6: (self.fireball_text_rect.centerx - 40, config.DISPLAY_H - 25),
            7: (self.shieldthrow_text_rect.centerx - 40, config.DISPLAY_H - 25),
        }
        
        #more cursor stuff
        self.index = 0
        self.cursor_rect.center = (self.melee_text_rect.centerx - 40, config.DISPLAY_H - 70)
        self.turn = 'Player'

        pygame.mixer.init()
        pygame.mixer.music.load('assets/battle.mp3')
        pygame.mixer_music.set_volume(0.7)
        pygame.mixer.music.play()


    
    def update(self, delta_time, actions):
        self.player.update(delta_time) #updating the player
        self.battle(actions) #checking for and initiating the battle
        self.game.reset_keys() #resetting the keys to prevent repeated inputs

    def render(self, surface):
        #a lot of blitting(just skip this part)
        surface.fill(self.game.WHITE)
        surface.blit(self.enemy_image, self.enemy_rect)
        surface.blit(self.player_image, self.player_rect)
        surface.blit(self.player_banner, self.player_banner_rect)
        surface.blit(self.enemy_banner, self.enemy_banner_rect)
        surface.blit(self.lunge_img, self.lunge_rect)
        surface.blit(self.heavystrike_img, self.heavystrike_rect)
        surface.blit(self.fireball_img, self.fireball_rect)
        surface.blit(self.shieldthrow_img, self.shieldthrow_rect)
        surface.blit(self.ribbon_image, self.melee_rect)
        surface.blit(self.ribbon_image, self.potion_rect)
        surface.blit(self.ribbon_image, self.mana_rect)
        surface.blit(self.ribbon_image, self.flee_rect)
        surface.blit(self.lunge_text, self.lunge_text_rect)
        surface.blit(self.heavystrike_text, self.heavystrike_text_rect)
        surface.blit(self.fireball_text, self.fireball_text_rect)
        surface.blit(self.shieldthrow_text, self.shieldthrow_text_rect)
        surface.blit(self.melee_text, self.melee_text_rect)
        surface.blit(self.potion_text, self.potion_text_rect)
        surface.blit(self.mana_text, self.mana_text_rect)
        surface.blit(self.flee_text, self.flee_text_rect)
        surface.blit(self.header, self.header_rect)
        surface.blit(self.enemy_header, self.enemy_header_rect)
        surface.blit(self.enemy_hp, self.enemy_hp_rect)
        surface.blit(self.hp, self.hp_rect)
        surface.blit(self.mp, self.mp_rect)
        self.draw_cursor2() #drawing the cursor for battle

    #cursor movement for battle
    def move_cursor(self, actions):
        if actions['right']:
            self.index += 1
            if self.index == 8:
                self.index = 0
        if actions['move right']:
            self.index += 1
            if self.index == 8:
                self.index = 0
        if actions['left']:
            self.index -= 1
            if self.index < 0:
                self.index = 7
        if actions['move left']:
            self.index -= 1
            if self.index < 0:
                self.index = 7
        if actions['up']:
            if self.index >= 4:
                self.index -= 4
            else:
                self.index += 4
        if actions['move up']:
            if self.index >= 4:
                self.index -= 4
            else:
                self.index += 4
        if actions['down']:
            if self.index >= 4:
                self.index -= 4
            else:
                self.index += 4
        if actions['move down']:
            if self.index >= 4:
                self.index -= 4
            else:
                self.index += 4
        self.cursor_rect.center = self.menu_options[self.index]

    def player_turn(self, actions):
        action = None #if not pressed then the action is none
        if actions['enter']:
            if self.index == 0:
                action = 'Melee' 
            elif self.index == 1:
                action = 'Health'
            elif self.index == 2:
                action = 'Mana'
            elif self.index == 3:
                action = 'Flee'
            elif self.index == 4:
                action = 'Lunge'
            elif self.index == 5:
                action = 'Heavy Strike'
            elif self.index == 6:
                action = 'Fireball'
            elif self.index == 7:
                action = 'Shield Throw'
            
            if self.index >= 4: #postition of spells are indexed from 4 to 7
                move = Spell(action, self.player)
                chance = randint(1,20) + int((self.player.stats['AGI']-10)/2) #chance to hit is based on player agility
                dodge_chance = randint(1, 20) + int((self.enemy.level.speed - 10) / 2)
                if self.player.mp >= move.mp_cost:
                    if chance > dodge_chance: #checks if the spell hits
                        damage_amount = move.use() #spell damage calculation
                        self.player.mp -= move.mp_cost
                        self.enemy.hp -= damage_amount
                        self.enemy_hp = self.font.render(f'HP: {self.enemy.hp}', True, self.game.BLACK)
                        self.header_text = f'Your {move.type} dealt {damage_amount} damage to the Orc!'
                        self.header = self.font2.render(self.header_text, True, self.game.BLACK)
                        self.header_rect = self.header.get_rect(center=self.player_banner_rect.center)
                        self.mp = self.font.render(f'MP: {self.player.mp}', True, self.game.BLACK)
                        self.turn = 'Enemy' 
                    else:
                        self.player.mp -= move.mp_cost
                        self.header_text = f'Your move missed!'
                        self.header = self.font.render(self.header_text, True, self.game.BLACK)
                        self.header_rect = self.header.get_rect(center=self.player_banner_rect.center)
                        self.mp = self.font.render(f'MP: {self.player.mp}', True, self.game.BLACK)
                        self.turn = 'Enemy' 
                else:
                    self.header_text = 'Not enough mana!'
                    self.header = self.font.render(self.header_text, True, self.game.BLACK)
                    self.header_rect = self.header.get_rect(center=self.player_banner_rect.center)

            elif action == 'Melee':
                chance = randint(1,20) + int((self.player.stats['AGI']-10)/2) #chance to hit is based on player agility
                dodge_chance = randint(1, 20) + int((self.enemy.level.speed - 10) / 2)
                if chance > dodge_chance: #check if the attack hits
                    move = Attack(self.player)
                    damage_amount = move.use() #damage amount calculation
                    self.enemy.hp -= damage_amount
                    self.enemy_hp = self.font.render(f'HP: {self.enemy.hp}', True, self.game.BLACK)
                    self.header_text = f'Your melee attack does {damage_amount} damage to the Orc!'
                    self.header = self.font2.render(self.header_text, True, self.game.BLACK)
                    self.header_rect = self.header.get_rect(center=self.player_banner_rect.center)
                else:
                    self.header_text = 'Your melee attack misses!'
                    self.header = self.font.render(self.header_text, True, self.game.BLACK)
                    self.header_rect = self.header.get_rect(center=self.player_banner_rect.center)
                self.turn = 'Enemy'

            elif action == 'Flee':
                chance = randint(1,20) + int((self.player.stats['AGI']-10)/2) #chance to flee is based on player agility
                fail_chance = randint(1, 20) + int((self.enemy.level.speed - 10) / 2) #chance to fail is based on enemy speed
                if chance > fail_chance: #check if the player flees
                    self.exit_state()
                    pygame.mixer.music.load('assets/game.mp3')
                    pygame.mixer_music.set_volume(0.7)
                    pygame.mixer.music.play()
                else:
                    self.header_text = 'You fail to flee!'
                    self.header = self.font.render(self.header_text, True, self.game.BLACK)
                    self.header_rect = self.header.get_rect(center=self.player_banner_rect.center)
                    self.turn = 'Enemy'

            else:
                move = Potion(action, self.player)
                if self.player.inventory[action] >= 1: #self.player.inventory is a dictionary with the type and amount of potions
                    amount = move.use() #heal amount calculation
                    if action == 'Health':
                        self.player.hp += amount
                        if self.player.hp >= self.player.max_hp:
                            self.player.hp = self.player.max_hp
                            self.header_text = f'You healed to full health!'
                        else:
                            self.header_text = f'You healed {amount} hp!'
                        self.player.inventory['Health'] -= 1
                        self.hp = self.font.render(f'HP: {self.player.hp}', True, self.game.BLACK)
                        self.potion_text = self.font2.render(f'Health Potion: {self.player.inventory["Health"]}', True, self.game.BLACK)
                        self.header = self.font.render(self.header_text, True, self.game.BLACK)
                        self.header_rect = self.header.get_rect(center=self.player_banner_rect.center)
                        self.turn = 'Enemy'    
                    else:
                        self.player.mp += amount
                        if self.player.mp >= self.player.max_mp:
                            self.player.mp = self.player.max_mp
                            self.header_text = f'You recovered all your mana!'
                        else:
                            self.header_text = f'You healed {amount} mp!'
                        self.player.inventory['Mana'] -= 1
                        self.mp = self.font.render(f'MP: {self.player.mp}', True, self.game.BLACK)
                        self.mana_text = self.font2.render(f'Mana Potion: {self.player.inventory["Mana"]}', True, self.game.BLACK)
                        self.header = self.font.render(self.header_text, True, self.game.BLACK)
                        self.header_rect = self.header.get_rect(center=self.player_banner_rect.center)
                        self.turn = 'Enemy'
                else:
                    self.header_text = 'You do not have any potions!'
                    self.header = self.font.render(self.header_text, True, self.game.BLACK)
                    self.header_rect = self.header.get_rect(center=self.player_banner_rect.center)


    def enemy_turn(self): #what the enemy does in a turn
        dodge_chance = randint(1, 20) + int((self.player.stats['AGI'] - 10) / 2) #chance to dodge is based on player agility
        hit_chance = randint(1, 20) + int((self.enemy.level.speed - 10) / 2) #chance to hit player is based on enemy speed
        if hit_chance >= dodge_chance:
            damage = self.enemy.attack()
            self.player.hp -= damage
            self.hp = self.font.render(f'HP: {self.player.hp}', True, self.game.BLACK)
            self.enemy_header_text = f'The Orc attacks you for {damage} damage!'
            self.enemy_header = self.font2.render(self.enemy_header_text, True, self.game.BLACK)
            self.enemy_header_rect = self.enemy_header.get_rect(center=self.enemy_banner_rect.center)
        else:
            self.enemy_header_text = f'You dodge the attack!'
            self.enemy_header = self.font.render(self.enemy_header_text, True, self.game.BLACK)
            self.enemy_header_rect = self.enemy_header.get_rect(center=self.enemy_banner_rect.center)
        self.turn = 'Player'

    def battle(self, actions): #battle logic
        if self.player.hp > 0 and self.enemy.hp > 0: #checks if both player and enemy are alive
            if self.turn == 'Player':
                self.move_cursor(actions)
                self.player_turn(actions)
            else:
                self.enemy_turn()
        elif self.enemy.hp <= 0: #checks if the enemy is dead
            xp = randint(self.enemy.level.xp_range[0], self.enemy.level.xp_range[1])
            coins = randint(self.enemy.level.gold_range[0], self.enemy.level.gold_range[1])
            self.player.coins += coins
            self.player.xp += xp
            level_up = False
            if self.player.xp > self.player.level.xp: #checks if the player levels up
                rem_xp = self.player.xp - self.player.level.xp
                new_level = self.player.level.level + 1
                self.player.xp = rem_xp
                self.player.level = config.player_levels[new_level]
                level_up = True
            self.exit_state()
            self.game.next_state = BattleComplete(self.game, 'Battle Complete', xp, coins, level_up, self.player) #switches to battle complete screen
            self.game.next()
            pygame.mixer.music.load('assets/game.mp3')
            pygame.mixer_music.set_volume(0.7)
            pygame.mixer.music.play()
        elif self.player.hp <= 0: #checks if the player is dead
            pygame.time.wait(30)
            self.game.player = None
            game_over = GameOver(self.game, 'Game Over') #switches to game over screen
            self.game.next_state = game_over
            self.game.next()