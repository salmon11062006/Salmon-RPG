import pygame
import config
from menu import Menu
from state import State

class GameOver(State, Menu):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        Menu.__init__(self, game)

        self.font = pygame.font.Font('assets/8-bit-hud.ttf', 40)
        self.small_font = pygame.font.Font('assets/8-bit-hud.ttf', 25)
        self.go_text = self.font.render('GAME OVER', True, self.game.WHITE)
        self.go_rect = self.go_text.get_rect(center=(self.mid_w, self.mid_h))
        self.load_text = self.small_font.render('Load Game', True, self.game.WHITE)
        self.load_rect = self.load_text.get_rect(center=(self.mid_w, self.mid_h + 80))
        self.main_text = self.small_font.render('Main Menu', True, self.game.WHITE)
        self.main_rect = self.main_text.get_rect(center=(self.mid_w, self.mid_h + 140))
        self.cursor_rect.center = (self.mid_w - 170, self.mid_h + 80)
        self.menu_options = {
            0: self.mid_h + 80,
            1: self.mid_h + 130
        }
        self.index = 0

    def move_cursor(self, actions):
        if actions['down']:
            self.index += 1
            if self.index == 2:
                self.index = 0
        if actions['up']:
            self.index -= 1
            if self.index < 0:
                self.index = 1
        if actions['move down']:
            self.index += 1
            if self.index == 2:
                self.index = 0
        if actions['move up']:
            self.index -= 1
            if self.index < 0:
                self.index = 1
        self.cursor_rect.y = self.menu_options[self.index]

    def update(self, delta_time, actions):
        pos = pygame.mouse.get_pos()
        self.move_cursor(actions)
        if actions['enter']:
            if self.index == 0:
                self.game.load_game()
            else:
                self.game.title.open = False
                self.game.next_state = self.game.title
                self.game.next()
        self.game.reset_keys()

    def render(self, surface):
        surface.fill(self.game.BLACK)
        surface.blit(self.go_text, self.go_rect)
        self.load_button = surface.blit(self.load_text, self.load_rect)
        self.main_button = surface.blit(self.main_text, self.main_rect)
        self.draw_cursor()