import pygame
from title import Title
import config
class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Salmon RPG")
        self.running, self.playing = True, False
        self.DISPLAY = pygame.Surface((config.DISPLAY_W, config.DISPLAY_H))
        self.WINDOW = pygame.display.set_mode(((config.DISPLAY_W, config.DISPLAY_H)))
        self.BLACK, self.WHITE, self.PURPLE, self.GREY, self.YELLOW = (0, 0, 0), (255, 255, 255), (135, 92, 242), (199, 200, 201), (234, 237, 183)
        self.main_menu = Title(self, 'Title')
        self.clock = pygame.time.Clock()
        self.fading = None
        self.next_state = None
        self.create_character = None
        self.alpha = 0
        sr = pygame.display.get_surface().get_rect()
        self.veil = pygame.Surface(sr.size)
        self.veil.fill((0,0,0))
        self.all_sprites = pygame.sprite.Group()
        self.player = None
        self.state_stack = []
        self.dt = 0
        self.map_width = 1024
        self.map_height = 1024

        self.actions = {
            'z': False,
            'x': False,
            'left': False,
            'right': False,
            'up': False,
            'down': False,
            'move left': False,
            'move right': False,
            'move down': False,
            'move up': False,
            'enter': False,
            'escape': False,
            'backspace': False,
            'left mouse': False,
        }
        self.load_states()

    def load_states(self):
        self.title = Title(self, 'Title')
        self.state_stack.append(self.title)

    def game_loop(self):
        while self.running and not self.playing:
            self.check_events()
            self.render()
            self.update()
        while self.playing:
            self.dt = self.clock.tick() / 1000
            self.check_events()
            self.render()
            self.update()

    def draw_text(self, surface, text, color, size, x, y):
        font = pygame.font.Font('assets/8-bit-hud.ttf', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x,y))
        surface.blit(text_surface, text_rect)      

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False
    
    def next(self):
        if not self.fading:
            self.fading = 'OUT'
            self.alpha = 0

    def update(self):
        self.WINDOW.fill(self.BLACK)
        self.state_stack[-1].update(self.dt, self.actions)
        self.all_sprites.update(self.dt)
        if self.fading == 'OUT':
            self.alpha += 8
            if self.alpha >= 255:
                self.fading = 'IN'
                self.state_stack.append(self.next_state)
        else:
            self.alpha -= 8
            if self.alpha <= 0:
                self.fading = None
    
    def render(self):
        self.state_stack[-1].render(self.WINDOW)
        self.WINDOW.blit(pygame.transform.scale(self.WINDOW, (config.DISPLAY_W, config.DISPLAY_H)), (0,0))
        if self.fading:
            self.veil.set_alpha(self.alpha)
            self.WINDOW.blit(self.veil, (0,0) )
        pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.actions['enter'] = True
                elif event.key == pygame.K_BACKSPACE:
                    self.actions['backspace'] = True
                elif event.key == pygame.K_DOWN:
                    self.actions['down']= True
                elif event.key == pygame.K_UP:
                    self.actions['up']= True
                elif event.key == pygame.K_ESCAPE:
                    self.actions['escape'] = True
                elif event.key == pygame.K_LEFT:
                    self.actions['left']= True
                elif event.key == pygame.K_RIGHT:
                    self.actions['right']= True
                elif event.key == pygame.K_z:
                    self.actions['z'] = True
                elif event.key == pygame.K_x:
                    self.actions['x'] = True
                elif event.key == pygame.K_a:
                    self.actions['move left']= True
                elif event.key == pygame.K_d:
                    self.actions['move right']= True
                elif event.key == pygame.K_s:
                    self.actions['move down']= True
                elif event.key == pygame.K_w:
                    self.actions['move up']= True
                elif event.key == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.actions['left mouse']= True
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self.actions['enter'] = False
                elif event.key == pygame.K_BACKSPACE:
                    self.actions['backspace'] = False
                elif event.key == pygame.K_DOWN:
                        self.actions['down']= False
                elif event.key == pygame.K_UP:
                    self.actions['up']= False
                elif event.key == pygame.K_ESCAPE:
                    self.actions['escape'] = False
                elif event.key == pygame.K_LEFT:
                    self.actions['left']= False
                elif event.key == pygame.K_RIGHT:
                    self.actions['right']= False
                elif event.key == pygame.K_z:
                    self.actions['z'] = False
                elif event.key == pygame.K_x:
                    self.actions['x'] = False
                elif event.key == pygame.K_a:
                    self.actions['move left']= False
                elif event.key == pygame.K_d:
                    self.actions['move right']= False
                elif event.key == pygame.K_s:
                    self.actions['move down']= False
                elif event.key == pygame.K_w:
                    self.actions['move up']= False
                elif event.key == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.actions['left mouse']= False


    
