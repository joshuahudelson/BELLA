from Menu import Menu
from KeyCrush import KeyCrush
from Whack_A_Dot import Whack_A_Dot
from Cell_Spotter import Cell_Spotter
from Contraction_Action import Contraction_Action
from Alphabet_Cards import Alphabet_Cards
from Braille_Tale import Braille_Tale
import numpy
from keyboard import keyboard
import pygame
import sounds
from sys import exit
from player_stats import player_stats
import time

pygame.mixer.pre_init(22050, -16,  1, 512)

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

channel0 = pygame.mixer.Channel(0)

gametools = {'pygame':pygame,
             'numpy':numpy,
             'sounds':sounds,
             'keyboard':braille_keyboard,
             'display':gameDisplay,
             'fps':fps,
             'serial_delay_factor':serial_delay_factor,
             'channel':channel0}

game_choice = "Menu"

initialized = {'KeyCrush':False, 'Menu':False, 'Whack-A-Dot':False,
               'Cell Spotter':False, 'Contraction Action':False,
               'Alphabet Cards':False, 'Braille Tale':False}

selection = None

input_control = None

current_player_stats = player_stats()
current_player_stats.load_stats('stats')
previous_time = time.time()

volume = 1.0


while(True):

    current_time = time.time()
    if (time.time() - previous_time) > 10:
        previous_time = current_time
        current_player_stats.update_time({'game_name':game_choice, 'time_on_game': 10})
        current_player_stats.save_stats('stats')
        print("Ten seconds has elapsed.")
        current_player_stats.make_report_card('report_card.txt')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    input_dict = braille_keyboard.update_keyboard()
    input_dict['volume'] = volume

    input_control = input_dict['standard']


    if input_control == 'display':
        current_display_state = (current_display_state + 1) % len(display_names)
        display_data = {'screen_width':SCREEN_WIDTH, 'screen_height':SCREEN_HEIGHT, 'current_display_state':current_display_state}

    if input_control == 'volume_up':
        if volume < 1.0:
            volume += .1
            channel0.set_volume(volume)
            print(volume)

    if input_control == 'volume_down':
        if volume > 0.01:
            volume -= 0.1
            channel0.set_volume(volume)
            print(volume)

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
            current_player_stats.update_stats(KeyCrush_game.iterate(input_dict))
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
            current_player_stats.update_stats(Cell_Spotter_game.iterate(input_dict))
            clock.tick(fps)
        else:
            Cell_Spotter_game = Cell_Spotter(gametools, display_data)
            initialized[game_choice] = True

    if game_choice == "Contraction Action":
        if initialized[game_choice]:
            current_player_stats.update_stats(Contraction_Action_game.iterate(input_dict))
            clock.tick(fps)
        else:
            Contraction_Action_game = Contraction_Action(gametools, display_data)
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
