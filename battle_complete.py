import random
import pygame
import config
from state import State
from support import Tilesheet, Timer


class BattleComplete(State):
    def __init__(self, game, name, xp, coins, level_up, player):
        State.__init__(self, game, name)
        self.xp = xp #xp earned from battle
        self.coins = coins #coins earned from battle
        self.player = player #player stats
        self.level_up = level_up #if player leveled up
        self.player_rem_xp = self.player.level.xp - self.player.xp #xp needed to level up
        self.font = pygame.font.Font('assets/8-bit-hud.ttf', 20)
        self.large_font = pygame.font.Font('assets/8-bit-hud.ttf', 40)
        self.xp_font = pygame.font.Font('assets/8-bit-hud.ttf', 40)
        self.battle_timer = Timer(200) #timer reset
        self.count = 100 #timer reset
        self.coin_tiles = Tilesheet('assets/coin.png', 100, 100, 1, 5)
        self.coin_image = pygame.transform.scale(self.coin_tiles.get_tile(0, 0), (100,100))
        self.xp_label = self.xp_font.render('XP', True, self.game.BLACK)
        self.xp_earned = self.large_font.render(f'{self.xp}', True, self.game.BLACK)
        self.coins_earned = self.large_font.render(f'{self.coins}', True, self.game.BLACK)

        if self.level_up:
            #added stats
            self.health = 0
            self.mana = 0
            self.speed = 0
            self.strength = 0
            self.intelligence = 0

            #randomly increase stats 5 times
            for i in range(5):
                skill = random.choice(list(self.player.stats.keys()))
                match skill:
                    case 'VIT':
                        self.health += 1
                    case 'ERU':
                        self.mana += 1
                    case 'AGI':
                        self.speed += 1
                    case 'STR':
                        self.strength += 1
                    case 'INT':
                        self.intelligence += 1
                self.player.stats[skill] += 1

                     

            #text and stuff on the screen
            self.space = self.font.render('Press Enter to Continue', True, self.game.BLACK)
            self.header = self.font.render(f'LEVEL UP! You are now level {self.player.level.level}', True, self.game.BLACK)
            self.coin_rect = self.coin_image.get_rect(center=(config.DISPLAY_W/4, config.DISPLAY_H/2 - 50))
            self.xp_label_rect = self.xp_label.get_rect(topleft=self.coin_rect.bottomleft)
            self.coins_earned_rect = self.coins_earned.get_rect(center=(self.coin_rect.centerx + 100, self.coin_rect.centery))
            self.xp_earned_rect = self.xp_earned.get_rect(center=(self.xp_label_rect.centerx + 100, self.xp_label_rect.centery))
            
            #more text and stuff on the screen
            self.str = self.font.render(f'Strength: {self.player.stats['STR']}', True, self.game.BLACK)
            self.int = self.font.render(f'Intelligence: {self.player.stats['INT']}', True, self.game.BLACK)
            self.vit = self.font.render(f'Max Health: {self.player.stats['VIT']}', True, self.game.BLACK)
            self.eru = self.font.render(f'Max Mana: {self.player.stats['ERU']}', True, self.game.BLACK)
            self.agi = self.font.render(f'Speed: {self.player.stats['AGI']}', True, self.game.BLACK)
            self.str_rect = self.str.get_rect(center=(config.DISPLAY_W/2 + 140 , config.DISPLAY_H/2 - 100))
            self.int_rect = self.int.get_rect(topleft=self.str_rect.bottomleft)
            self.vit_rect = self.vit.get_rect(topleft=self.int_rect.bottomleft)
            self.eru_rect = self.eru.get_rect(topleft=self.vit_rect.bottomleft)
            self.agi_rect = self.agi.get_rect(topleft=self.eru_rect.bottomleft)

            self.increased_stats = [] #simplifying the screen blitting with a list
            if self.health > 0:
                self.health_text = self.font.render(f'+{self.health}', True, self.game.GREEN)
                self.health_rect = self.health_text.get_rect(topleft=self.vit_rect.topright)
                self.increased_stats.append([self.health_text, self.health_rect])
            if self.mana > 0:
                self.mana_text = self.font.render(f'+{self.mana}', True, self.game.GREEN)
                self.mana_rect = self.mana_text.get_rect(topleft=self.eru_rect.topright)
                self.increased_stats.append([self.mana_text, self.mana_rect])
            if self.speed > 0:
                self.speed_text = self.font.render(f'+{self.speed}', True, self.game.GREEN)
                self.speed_rect = self.speed_text.get_rect(topleft=self.agi_rect.topright)
                self.increased_stats.append([self.speed_text, self.speed_rect])
            if self.strength > 0:
                self.strength_text = self.font.render(f'+{self.strength}', True, self.game.GREEN)
                self.strength_rect = self.strength_text.get_rect(topleft=self.str_rect.topright)
                self.increased_stats.append([self.strength_text, self.strength_rect])
            if self.intelligence > 0:
                self.intelligence_text = self.font.render(f'+{self.intelligence}', True, self.game.GREEN)
                self.intelligence_rect = self.intelligence_text.get_rect(topleft=self.int_rect.topright)
                self.increased_stats.append([self.intelligence_text, self.intelligence_rect])

        else:
            self.space = self.font.render('Press Enter to Continue', True, self.game.BLACK)
            self.header = self.large_font.render('Battle Complete!', True, self.game.BLACK)
            self.coin_rect = self.coin_image.get_rect(center=(config.DISPLAY_W/2 - 100, config.DISPLAY_H/2 - 50))
            self.xp_label_rect = self.xp_label.get_rect(topleft=self.coin_rect.bottomleft)
            self.coins_earned_rect = self.coins_earned.get_rect(center=(self.coin_rect.centerx + 100, self.coin_rect.centery))
            self.xp_earned_rect = self.xp_earned.get_rect(center=(self.xp_label_rect.centerx + 100, self.xp_label_rect.centery))

        self.space_rect = self.space.get_rect(center=(config.DISPLAY_W/2, config.DISPLAY_H - 30))
        self.next = self.font.render(f'{self.player_rem_xp} XP to next level', True, self.game.BLACK)
        self.next_rect = self.next.get_rect(center=(config.DISPLAY_W/2, config.DISPLAY_H - 100))
        self.header_rect = self.header.get_rect(center=(config.DISPLAY_W/2, 50))

    def render(self, surface):
        surface.fill(self.game.PURPLE)
        surface.blit(self.header, self.header_rect)
        surface.blit(self.xp_label, self.xp_label_rect)
        surface.blit(self.xp_earned, self.xp_earned_rect)
        surface.blit(self.space, self.space_rect)
        surface.blit(self.next, self.next_rect)
        if self.level_up:
            surface.blit(self.str, self.str_rect)
            surface.blit(self.int, self.int_rect)
            surface.blit(self.vit, self.vit_rect)
            surface.blit(self.eru, self.eru_rect)
            surface.blit(self.agi, self.agi_rect)
            for stat in self.increased_stats:
                surface.blit(stat[0], stat[1]) #the simplification mentioned above


    def update(self, dt, actions):
        if actions['enter']:
            if self.level_up:
                self.exit_state() #exits the current screen, goes back to the world
            else:
                self.exit_state() 
