import pygame
import config
class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = config.DISPLAY_W / 2, config.DISPLAY_H / 2
        self.cursor_rect = pygame.Rect(0,0,20,20)

    def draw_cursor(self):
        self.game.draw_text(self.game.WINDOW, '>', self.game.WHITE, 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.WINDOW.blit(self.game.DISPLAY, (0,0))
        pygame.display.update()
        self.game.reset_keys()
