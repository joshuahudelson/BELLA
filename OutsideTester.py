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
braille_keyboard.test_coms()    # automatically finds keyboard

clock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

input_letter = None

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

KeyCrush_initialized = False
menu_initialized = False
etudes_initialized = False
search_initialized = False
alphabet_game_initialized = False
storybook_initialized = False

selection = None

input_letter = None
the_input = None

while(True):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitGame = True

    input_dict = braille_keyboard.update_keyboard()

    input_letter = input_dict['standard']
    

    if game_choice == "Menu":
        if menu_initialized:
            selection = Opening_Menu.iterate(input_letter)
            clock.tick(fps)
            if selection != None:
                print(selection)
                Opening_Menu = None
                menu_initialized = False
                game_choice = selection
        else:
            Opening_Menu = Menu(gametools)
            menu_initialized = True

    if game_choice == "KeyCrush":
        if KeyCrush_initialized:
            KeyCrush_game.iterate(input_dict)
            clock.tick(fps)
        else:
            KeyCrush_game = KeyCrush(gametools)
            KeyCrush_initialized = True

    if game_choice == "Etudes":
        if etudes_initialized:
            Etudes_Game.iterate(input_dict)
            clock.tick(fps)
        else:
            Etudes_Game = Etudes(gametools)
            etudes_initialized = True

    if game_choice == "Search":
        if search_initialized:
            Search_Game.iterate(input_dict)
            clock.tick(fps)
        else:
            Search_Game = Search(gametools)
            search_initialized = True

    if game_choice == "Alphabet Game":
        if alphabet_game_initialized:
            Alphabet_Game.iterate(input_dict)
            clock.tick(fps)
        else:
            Alphabet_Game = AlphabetGame(gametools)
            alphabet_game_initialized = True

    if game_choice == "StoryBook":
        if storybook_initialized:
            StoryBook.iterate(input_dict)
            clock.tick(fps)
        else:
            StoryBook = StoryBook(gametools)
            storybook_initialized = True
