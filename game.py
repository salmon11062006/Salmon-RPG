import pygame
from title import Title
import config
class Game():
    def __init__(self):
        pygame.init() #initializing pygame
        pygame.display.set_caption("Salmon RPG") #setting the window title
        self.running, self.playing = True, False #to check for the game loop
        self.DISPLAY = pygame.Surface((config.DISPLAY_W, config.DISPLAY_H)) #setting the display size
        self.WINDOW = pygame.display.set_mode(((config.DISPLAY_W, config.DISPLAY_H))) #setting the window size
        #bunch of colors, should be in config but i put it here and was too lazy to move them
        self.BLACK, self.WHITE, self.PURPLE, self.GREY, self.YELLOW, self.GREEN = (
            0, 0, 0), (255, 255, 255), (135, 92, 242), (199, 200, 201), (234, 237, 183), (19, 173, 55)
        self.main_menu = Title(self, 'Title') #creating the main menu
        self.clock = pygame.time.Clock() #fps
        self.fading = None #fade out transition
        self.next_state = None #to check for the next state
        self.create_character = None #creating the character
        self.alpha = 0 #alpha for the fade out transition
        sr = pygame.display.get_surface().get_rect() #getting the surface rect
        self.veil = pygame.Surface(sr.size) #creating the veil for the fade out transition
        self.veil.fill((0,0,0)) #filling the veil with black
        self.all_sprites = pygame.sprite.Group() 
        self.player = None #initial player is none
        self.state_stack = [] #state stack
        self.dt = 0 #delta time for animations and such

        #below are the list of keys that you can use
        self.actions = {
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
        self.state_stack.append(self.title) #title screen is inital screen

    #main game loop for all the states
    def game_loop(self):
        while self.running and not self.playing:
            self.check_events()
            self.render()
            self.update()
        while self.playing:
            self.dt = self.clock.tick() / 1000 #fps
            self.check_events()
            self.render()
            self.update()

    #for text drawing in other classes
    def draw_text(self, surface, text, color, size, x, y):
        font = pygame.font.Font('assets/8-bit-hud.ttf', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x,y))
        surface.blit(text_surface, text_rect)      

    #to prevent multiple inputs
    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False
    
    #to fade to the next state
    def next(self):
        if not self.fading:
            self.fading = 'OUT'
            self.alpha = 0


    def update(self):
        self.WINDOW.fill(self.BLACK)
        self.state_stack[-1].update(self.dt, self.actions)
        self.all_sprites.update(self.dt)
        #fade transition
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
        self.state_stack[-1].render(self.WINDOW) #rendering the current state(the appended state)
        self.WINDOW.blit(pygame.transform.scale(self.WINDOW, (config.DISPLAY_W, config.DISPLAY_H)), (0,0))
        if self.fading:
            self.veil.set_alpha(self.alpha)
            self.WINDOW.blit(self.veil, (0,0) )
        pygame.display.flip()


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #to check for quitting the game
                self.running, self.playing = False, False
                pygame.quit()
            if event.type == pygame.KEYDOWN: #to check for key presses
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
            if event.type == pygame.MOUSEBUTTONDOWN: #to check for mouse clicks
                if event.button == 1:
                    self.actions['left mouse']= True
            
            if event.type == pygame.KEYUP: #to check for key releases
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
            if event.type == pygame.MOUSEBUTTONUP: #to check for mouse releases
                if event.button == 1:
                    self.actions['left mouse']= False

    
