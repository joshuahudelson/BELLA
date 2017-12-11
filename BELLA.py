from Menu import Menu
from KeyCrush import KeyCrush
from Whack_A_Dot import Whack_A_Dot
from Cell_Spotter import Cell_Spotter
from Alphabet_Cards import Alphabet_Cards
from Braille_Tale import Braille_Tale
import numpy
from keyboard import keyboard
import pygame
import sounds
from sys import exit

pygame.mixer.pre_init(22050, -16,  2, 512)

pygame.init()
pygame.mixer.init()

braille_keyboard = keyboard()
braille_keyboard.test_coms()

clock = pygame.time.Clock()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
current_display_state = 0

white, black, yellow, blue = (255, 255, 255), (0, 0, 0), (255, 255, 0), (0, 0, 255)

display_data = {'screen_width':SCREEN_WIDTH, 'screen_height':SCREEN_HEIGHT, 'current_display_state':current_display_state}

display_names = ['white_black', 'black_white', 'blue_yellow']

display_states = {'black_white':{'background':black, 'text':white},
                       'white_black':{'background':white, 'text':black},
                       'blue_yellow':{'background':blue, 'text':yellow}}


serial_delay_factor = 0.5

gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

fps = 100

BELLA_start_up = True

gametools = {'pygame':pygame,
             'numpy':numpy,
             'sounds':sounds,
             'keyboard':braille_keyboard,
             'display':gameDisplay,
             'fps':fps,
             'serial_delay_factor':serial_delay_factor}

game_choice = "Menu"

initialized = {'KeyCrush':False, 'Menu':False, 'Whack-A-Dot':False,
               'Cell Spotter':False, 'Alphabet Cards':False, 'Braille Tale':False}

selection = None

input_control = None

while(True):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    input_dict = braille_keyboard.update_keyboard()

    input_control = input_dict['standard']


    if input_control == 'display':
        current_display_state = (current_display_state + 1) % len(display_names)
        display_data = {'screen_width':SCREEN_WIDTH, 'screen_height':SCREEN_HEIGHT, 'current_display_state':current_display_state}

    if input_control == 'quit':
        print("Quit!!")
        game_choice = 'Menu'
        for game in initialized:
            initialized[game] = False
        print(initialized)

    if game_choice == "Menu":
        if initialized[game_choice]:
            selection = Opening_Menu.iterate(input_dict)
            clock.tick(fps)
            if selection != None:
                Opening_Menu = None
                initialized[game_choice] = False
                game_choice = selection
        else:
            Opening_Menu = Menu(gametools, display_data,BELLA_start_up)
            initialized[game_choice] = True
            BELLA_start_up = False

    if game_choice == "KeyCrush":
        if initialized[game_choice]:
            KeyCrush_game.iterate(input_dict)
            clock.tick(fps)
        else:
            KeyCrush_game = KeyCrush(gametools, display_data)
            initialized[game_choice] = True

    if game_choice == "Whack-A-Dot":
        if initialized[game_choice]:
            Whack_A_Dot_game.iterate(input_dict)
            clock.tick(fps)
        else:
            Whack_A_Dot_game = Whack_A_Dot(gametools, display_data)
            initialized[game_choice] = True

    if game_choice == "Cell Spotter":
        if initialized[game_choice]:
            Cell_Spotter_game.iterate(input_dict)
            clock.tick(fps)
        else:
            Cell_Spotter_game = Cell_Spotter(gametools, display_data)
            initialized[game_choice] = True

    if game_choice == "Alphabet Cards":
        if initialized[game_choice]:
            Alphabet_Cards_game.iterate(input_dict)
            clock.tick(fps)
        else:
            Alphabet_Cards_game= Alphabet_Cards(gametools, display_data)
            initialized[game_choice] = True

    if game_choice == "Braille Tale":
        if initialized[game_choice]:
            Braille_Tale_game.iterate(input_dict)
            clock.tick(fps)
        else:
            Braille_Tale_game = Braille_Tale(gametools, display_data)
            initialized[game_choice] = True

"""
    Load_Profile, New_Profile, Delete_Profile
    if game_choice == ""

    game starts updating dictionary, and BELLA.py saves the dict every... 10 seconds or so to a file?


- every typed letter of alphabet: num right, wrong, (num right of most recent 10?)
- every read cell of braille: num right, wrong, (num right of most recent 10)
- record each time a game starts and as long as it's not 0: how long played for, score
- then: total time playing each game, high score for each.
- 

"""
