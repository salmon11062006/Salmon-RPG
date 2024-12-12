import pygame
import config
from menu import Menu
from state import State
from create import CreateCharacter
class Title(State, Menu):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        Menu.__init__(self,game)

        self.open = False
        self.image = pygame.transform.scale(pygame.image.load('assets/swordtitle.png'), (config.DISPLAY_W, config.DISPLAY_H))
        self.rect = self.image.get_rect(center=(self.mid_w, self.mid_h))
        self.font = pygame.font.Font('assets/8-bit-hud.ttf', 20)

        self.title_text = self.font.render('Salmon RPG', True, self.game.WHITE)
        self.new_text = self.font.render('New Game', True, self.game.WHITE)
        self.load_text = self.font.render('Load Game', True, self.game.WHITE)
        self.quit_text = self.font.render('Quit', True, self.game.WHITE)

        self.title_rect = self.title_text.get_rect(center=(self.mid_w, self.mid_h - 30))
        self.new_rect = self.new_text.get_rect(center=(self.mid_w, self.mid_h + 50))
        self.load_rect = self.load_text.get_rect(center=(self.mid_w, self.mid_h + 100))
        self.quit_rect = self.quit_text.get_rect(center=(self.mid_w, self.mid_h + 150))

        self.cursor_rect.center = (self.mid_w - 120, self.mid_h + 50)

        self.menu_options = {
            0: self.mid_h + 50,
            1: self.mid_h + 100,
            2: self.mid_h + 150
        }

        self.index = 0 

    def move_cursor(self, actions):
        if actions['down']:
            self.index +=1
            if self.index == 3:
                self.index = 0
        if actions['move down']:
            self.index +=1
            if self.index == 3:
                self.index = 0
        if actions['up']:
            self.index -=1
            if self.index < 0:
                self.index = 2
        if actions['move up']:
            self.index -=1
            if self.index < 0:
                self.index = 2
        self.cursor_rect.y = self.menu_options[self.index]

    def render(self, screen):
            screen.fill(self.game.BLACK)
            screen.blit(self.image, self.rect)
            if not self.open:
                screen.blit(self.title_text, self.title_rect)
                screen.blit(self.new_text, self.new_rect)
                screen.blit(self.load_text, self.load_rect)
                screen.blit(self.quit_text, self.quit_rect)
                self.draw_cursor()

    def update(self, delta_time, actions):
        self.move_cursor(actions)
        if actions['enter']:
            if self.index == 0:
                self.open  = True
                self.game.create_character = CreateCharacter(self.game, 'Create Character')
                self.game.next_state = self.game.create_character
                self.game.next()
            elif self.index == 1:
                print('Load Game') #yeah i didnt finish the save file thing in time ;-;
            elif self.index == 2:
                pygame.quit()
        self.game.reset_keys()

