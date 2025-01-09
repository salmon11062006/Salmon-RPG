import pygame
import pygame_widgets
from pygame_widgets.textbox import TextBox

import config
from state import State
from menu import Menu
from world.world.salmonella import Salmonella


class CreateCharacter(State, Menu):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        Menu.__init__(self, game)
        #until the next comment, all these things below are related to what you can see visually
        self.font = pygame.font.Font('assets/8-bit-hud.ttf', 15) 
        self.font2 = pygame.font.Font('assets/8-bit-hud.ttf', 25)
        self.font3 = pygame.font.Font('assets/8-bit-hud.ttf', 10)
        self.image = pygame.transform.scale(pygame.image.load('assets/book_middle.png'), (
            config.DISPLAY_W, config.DISPLAY_H))
        self.rect = self.image.get_rect(center=(self.mid_w, self.mid_h))
        self.name_text = self.font2.render('Name:', True, self.game.BLACK)
        self.name_rect = self.name_text.get_rect(topleft=(self.mid_w - 170, 50))
        self.textbox = TextBox(self.game.WINDOW, self.mid_w + 15, self.mid_h - 170, 200, 70, fontSize=50, 
                               borderColour=self.game.GREY, textColour=self.game.BLACK, 
                               colour=self.game.YELLOW, radius=10, borderThickness=5, font=self.font)
        self.plus_img = pygame.transform.scale(pygame.image.load(
            'assets/statsarrow.png').convert_alpha(), (64, 64))
        self.minus_img = pygame.transform.flip(self.plus_img, True, False)
        self.number_img = pygame.transform.scale(pygame.image.load(
            'assets/statsbox.png').convert_alpha(), (64, 64))
        self.set_text = self.font2.render('Stat:', True, self.game.BLACK)
        self.set_rect = self.set_text.get_rect(topleft=(self.mid_w - 170, 120))
        self.points_text = self.font3.render('Points remaining: ', True, self.game.BLACK)
        self.points_text_rect = self.points_text.get_rect(topleft=(self.mid_w - 210, 220))   

        self.str = self.font.render('STR', True, self.game.BLACK)
        self.int = self.font.render('INT', True, self.game.BLACK)
        self.vit = self.font.render('VIT', True, self.game.BLACK)
        self.eru = self.font.render('ERU', True, self.game.BLACK)
        self.agi = self.font.render('AGI', True, self.game.BLACK)
        #ok except this one, this shows the initial stats of the player
        self.points = 10 #points to be spent
        self.str_points = 10 #initial strength points
        self.int_points = 10 #initial intelligence points
        self.vit_points = 30 #initial vitality points
        self.eru_points = 20 #initial erudition points
        self.agi_points = 10 #initial agility points

        self.points_disp = self.font2.render(
            f'{self.points}', True, self.game.BLACK) #blitting the points remaining
        self.points_rect = self.points_disp.get_rect(center=(self.points_text_rect.centerx, 260))

        #str point container and buttons
        self.str_rect = self.str.get_rect(topleft=(self.mid_w + 10, 120))
        self.str_minus = self.minus_img.get_rect(topleft=(self.mid_w + 50, 100))
        self.str_num = self.number_img.get_rect(topleft=self.str_minus.topright)
        self.str_plus = self.plus_img.get_rect(topleft=self.str_num.topright)
        
        #int point container and buttons
        self.int_rect = self.int.get_rect(topleft=(self.mid_w + 10, 170))
        self.int_minus = self.minus_img.get_rect(topleft=(self.mid_w + 50, 150))
        self.int_num = self.number_img.get_rect(topleft=self.int_minus.topright)
        self.int_plus = self.plus_img.get_rect(topleft=self.int_num.topright)

        #vit point container and buttons
        self.vit_rect = self.vit.get_rect(topleft=(self.mid_w + 10, 220))
        self.vit_minus = self.minus_img.get_rect(topleft=(self.mid_w + 50, 200))
        self.vit_num = self.number_img.get_rect(topleft=self.vit_minus.topright)
        self.vit_plus = self.plus_img.get_rect(topleft=self.vit_num.topright)

        #eru point container and buttons
        self.eru_rect = self.eru.get_rect(topleft=(self.mid_w + 10, 270))
        self.eru_minus = self.minus_img.get_rect(topleft=(self.mid_w + 50, 250))
        self.eru_num = self.number_img.get_rect(topleft=self.eru_minus.topright)
        self.eru_plus = self.plus_img.get_rect(topleft=self.eru_num.topright)

        #agi point container and buttons
        self.agi_rect = self.agi.get_rect(topleft=(self.mid_w + 10, 320))
        self.agi_minus = self.minus_img.get_rect(topleft=(self.mid_w + 50, 300))
        self.agi_num = self.number_img.get_rect(topleft=self.agi_minus.topright)
        self.agi_plus = self.plus_img.get_rect(topleft=self.agi_num.topright)

        #the number of points in each stat
        self.str_amt = self.font3.render(f'{self.str_points}', True, self.game.WHITE)
        self.str_amt_rect = self.str_amt.get_rect(center=self.str_num.center)
        self.int_amt = self.font3.render(f'{self.int_points}', True, self.game.WHITE)
        self.int_amt_rect = self.int_amt.get_rect(center=self.int_num.center)
        self.vit_amt = self.font3.render(f'{self.vit_points}', True, self.game.WHITE)
        self.vit_amt_rect = self.vit_amt.get_rect(center=self.vit_num.center)
        self.eru_amt = self.font3.render(f'{self.eru_points}', True, self.game.WHITE)
        self.eru_amt_rect = self.eru_amt.get_rect(center=self.eru_num.center)
        self.agi_amt = self.font3.render(f'{self.agi_points}', True, self.game.WHITE)
        self.agi_amt_rect = self.agi_amt.get_rect(center=self.agi_num.center)

        #start button
        self.start = self.font.render('Start Game', True, self.game.BLACK)
        self.start_rect = self.start.get_rect(topleft=(self.mid_w - 200, self.mid_h + 100))


    #rendering all the things above
    def render(self, surface):
        surface.fill(self.game.BLACK)
        surface.blit(self.image, self.rect)
        surface.blit(self.name_text, self.name_rect)
        surface.blit(self.set_text, self.set_rect)
        surface.blit(self.points_text, self.points_text_rect)
        surface.blit(self.points_disp, self.points_rect)

        surface.blit(self.str, self.str_rect)
        self.str_down_button = surface.blit(self.minus_img, self.str_minus) #creating the button
        surface.blit(self.number_img, self.str_num)
        self.str_up_button = surface.blit(self.plus_img, self.str_plus) #creating the button

        surface.blit(self.int, self.int_rect)
        self.int_down_button = surface.blit(self.minus_img, self.int_minus) #creating the button
        surface.blit(self.number_img, self.int_num)
        self.int_up_button = surface.blit(self.plus_img, self.int_plus) #creating the button

        surface.blit(self.vit, self.vit_rect)
        self.vit_down_button = surface.blit(self.minus_img, self.vit_minus) #creating the button
        surface.blit(self.number_img, self.vit_num)
        self.vit_up_button = surface.blit(self.plus_img, self.vit_plus) #creating the button

        surface.blit(self.eru, self.eru_rect)
        self.eru_down_button = surface.blit(self.minus_img, self.eru_minus) #creating the button
        surface.blit(self.number_img, self.eru_num)
        self.eru_up_button = surface.blit(self.plus_img, self.eru_plus) #creating the button

        surface.blit(self.agi, self.agi_rect)
        self.agi_down_button = surface.blit(self.minus_img, self.agi_minus) #creating the button
        surface.blit(self.number_img, self.agi_num)
        self.agi_up_button = surface.blit(self.plus_img, self.agi_plus) #creating the button

        #blitting the numbers for each stat
        surface.blit(self.str_amt, self.str_amt_rect)
        surface.blit(self.int_amt, self.int_amt_rect)
        surface.blit(self.vit_amt, self.vit_amt_rect)
        surface.blit(self.eru_amt, self.eru_amt_rect)
        surface.blit(self.agi_amt, self.agi_amt_rect)
        self.textbox.draw() #textbox for the player name (unused again because we can't load files)
        self.start_button = surface.blit(self.start, self.start_rect) #start button


    #update the mouse clicks to add the points to the stats
    def update(self, delta_time, actions):
        pos = pygame.mouse.get_pos()
        events = pygame.event.get()
        pygame_widgets.update(events)
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running, self.game.playing = False, False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.str_up_button.collidepoint(pos):
                        if self.points > 0:
                            self.points -= 1
                            self.str_points += 1
                            self.str_amt = self.font3.render(f'{self.str_points}', True, self.game.WHITE)
                            self.points_disp = self.font2.render(f'{self.points}', True, self.game.BLACK)

                    if self.int_up_button.collidepoint(pos):
                        if self.points > 0:
                            self.points -= 1
                            self.int_points += 1
                            self.int_amt = self.font3.render(f'{self.int_points}', True, self.game.WHITE)
                            self.points_disp = self.font2.render(f'{self.points}', True, self.game.BLACK) 

                    if self.vit_up_button.collidepoint(pos):
                        if self.points > 0:
                            self.points -= 1
                            self.vit_points += 1
                            self.vit_amt = self.font3.render(f'{self.vit_points}', True, self.game.WHITE)
                            self.points_disp = self.font2.render(f'{self.points}', True, self.game.BLACK)

                    if self.eru_up_button.collidepoint(pos):
                        if self.points > 0:
                            self.points -= 1
                            self.eru_points += 1
                            self.eru_amt = self.font3.render(f'{self.eru_points}', True, self.game.WHITE)
                            self.points_disp = self.font2.render(f'{self.points}', True, self.game.BLACK)

                    if self.agi_up_button.collidepoint(pos):
                        if self.points > 0:
                            self.points -= 1
                            self.agi_points += 1
                            self.agi_amt = self.font3.render(f'{self.agi_points}', True, self.game.WHITE)
                            self.points_disp = self.font2.render(f'{self.points}', True, self.game.BLACK)

                    if self.str_down_button.collidepoint(pos):
                        if self.str_points > 10:
                            self.points += 1
                            self.str_points -= 1
                            self.str_amt = self.font3.render(f'{self.str_points}', True, self.game.WHITE)
                            self.points_disp = self.font2.render(f'{self.points}', True, self.game.BLACK)

                    if self.int_down_button.collidepoint(pos):
                        if self.int_points > 10:
                            self.points += 1
                            self.int_points -= 1
                            self.int_amt = self.font3.render(f'{self.int_points}', True, self.game.WHITE)
                            self.points_disp = self.font2.render(f'{self.points}', True, self.game.BLACK) 

                    if self.vit_down_button.collidepoint(pos):
                        if self.vit_points > 10:
                            self.points += 1
                            self.vit_points -= 1
                            self.vit_amt = self.font3.render(f'{self.vit_points}', True, self.game.WHITE)
                            self.points_disp = self.font2.render(f'{self.points}', True, self.game.BLACK)

                    if self.eru_down_button.collidepoint(pos):
                        if self.eru_points > 10:
                            self.points += 1
                            self.eru_points -= 1
                            self.eru_amt = self.font3.render(f'{self.eru_points}', True, self.game.WHITE)
                            self.points_disp = self.font2.render(f'{self.points}', True, self.game.BLACK)

                    if self.agi_down_button.collidepoint(pos):
                        if self.agi_points > 10:
                            self.points += 1
                            self.agi_points -= 1
                            self.agi_amt = self.font3.render(f'{self.agi_points}', True, self.game.WHITE)
                            self.points_disp = self.font2.render(f'{self.points}', True, self.game.BLACK)

                    if self.start_button.collidepoint(pos):
                        if self.points == 0 and self.textbox.getText != '':
                            self.game.salmonella = Salmonella(self.game, 
                                                              'Salmonella') #creating the salmonella world
                            self.game.next_state = self.game.salmonella #transition to the salmonella world
                            self.game.playing = True
                            #player stats
                            stats = {
                                'STR': self.str_points,
                                'INT': self.int_points,
                                'VIT': self.vit_points,
                                'ERU': self.eru_points,
                                'AGI': self.agi_points
                            }
                            self.game.next_state.setup_player(
                                self.game.next_state.player_start, self.textbox.getText(), stats)
                            self.game.next() #transition to the next state
                        elif self.points > 0:
                            #funny thing i added
                            pygame.mixer.init()
                            pygame.mixer.music.load('assets/stinky.mp3')
                            pygame.mixer_music.set_volume(0.3)
                            pygame.mixer.music.play()

        
