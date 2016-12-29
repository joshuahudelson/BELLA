from KeyCrush import KeyCrush
from Search import Search
from Etudes import Etudes
from Menu import Menu
from AlphabetGame import AlphabetGame
from StoryBook import StoryBook
import numpy
from keyboard import keyboard
import pygame
import sounds

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

gametools = {'pygame':pygame,
             'numpy':numpy,
             'sounds':sounds,
             'keyboard':braille_keyboard,
             'display':gameDisplay,
             'fps':fps,
             'serial_delay_factor':serial_delay_factor}

game_choice = "Menu"

initialized = {'KeyCrush':False, 'Menu':False, 'Etudes':False,
               'Search':False, 'Alphabet Game':False, 'StoryBook':False}

selection = None

input_control = None

while(True):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitGame = True

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
            Opening_Menu = Menu(gametools, display_data)
            initialized[game_choice] = True

    if game_choice == "KeyCrush":
        if initialized[game_choice]:
            KeyCrush_game.iterate(input_dict)
            clock.tick(fps)
        else:
            KeyCrush_game = KeyCrush(gametools, display_data)
            initialized[game_choice] = True

    if game_choice == "Etudes":
        if initialized[game_choice]:
            Etudes_Game.iterate(input_dict)
            clock.tick(fps)
        else:
            Etudes_Game = Etudes(gametools, display_data)
            initialized[game_choice] = True

    if game_choice == "Search":
        if initialized[game_choice]:
            Search_Game.iterate(input_dict)
            clock.tick(fps)
        else:
            Search_Game = Search(gametools, display_data)
            initialized[game_choice] = True

    if game_choice == "Alphabet Game":
        if initialized[game_choice]:
            Alphabet_Game.iterate(input_dict)
            clock.tick(fps)
        else:
            Alphabet_Game = AlphabetGame(gametools, display_data)
            initialized[game_choice] = True

    if game_choice == "StoryBook":
        if initialized[game_choice]:
            StoryBook.iterate(input_dict)
            clock.tick(fps)
        else:
            StoryBook = StoryBook(gametools, display_data)
            initialized[game_choice] = True
