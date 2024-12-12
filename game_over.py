import pygame
import config
from menu import Menu
from state import State

class GameOver(State, Menu):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        Menu.__init__(self, game)

        #loading the fonts and buttons
        self.font = pygame.font.Font('assets/8-bit-hud.ttf', 40)
        self.small_font = pygame.font.Font('assets/8-bit-hud.ttf', 25)
        self.go_text = self.font.render('GAME OVER', True, self.game.WHITE)
        self.go_rect = self.go_text.get_rect(center=(self.mid_w, self.mid_h))
        self.main_text = self.small_font.render('Main Menu', True, self.game.WHITE)
        self.main_rect = self.main_text.get_rect(center=(self.mid_w, self.mid_h + 80))
        self.cursor_rect.center = (self.mid_w - 170, self.mid_h + 80)
        #button selection for the cursor
        self.menu_options = {
            0: self.mid_h + 80,
        }

        self.cursor_rect.y = self.menu_options[0]

        pygame.mixer.init()
        pygame.mixer.music.load('assets/title.mp3')
        pygame.mixer_music.set_volume(0.7)
        pygame.mixer.music.play()

    #updates the cursor selection
    def update(self, delta_time, actions):
        if actions['enter']:
            self.game.title.open = False
            self.game.next_state = self.game.title
            self.game.next()
        self.game.reset_keys()

    #blits the game over screen
    def render(self, surface):
        surface.fill(self.game.BLACK)
        surface.blit(self.go_text, self.go_rect)
        self.main_button = surface.blit(self.main_text, self.main_rect)
        self.draw_cursor() #draws the cursor