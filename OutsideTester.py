from TypingTutor import TypingTutor
from Search import Search
from Etudes import Etudes
from Menu import Menu
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

key_was_pressed = False
input_letter = None

gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


gametools = {'pygame':pygame,
             'numpy':numpy,
             'sounds':sounds,
             'keyboard':braille_keyboard,
             'display':gameDisplay}

game_choice = "Menu"

typing_tutor_initialized = False
menu_initialized = False
etudes_initialized = False
search_initialized = False

selection = None

while(True):

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # if the window "x" has been pressed quit the game
            quitGame = True

    braille_keyboard.request_buttons()  # get button presses from keyboard

    if braille_keyboard.last_letter != None :  # if button was pressed
        input_letter = braille_keyboard.last_letter
        print(input_letter)
        key_was_pressed = True
    else:
        input_letter = None
        key_was_pressed = False

    if game_choice == "Menu":
        if menu_initialized:
            selection = Opening_Menu.iterate(input_letter)
            if selection != None:
                print(selection)
                Opening_Menu = None
                menu_initialized = False
                game_choice = selection
        else:
            Opening_Menu = Menu(gametools)
            menu_initialized = True

    if game_choice == "Typing Tutor":
        if typing_tutor_initialized:
            Typing_Tutor.iterate(input_letter, key_was_pressed)
            clock.tick(200)
        else:
            Typing_Tutor = TypingTutor(gametools)
            typing_tutor_initialized = True

    if game_choice == "Etudes":
        if etudes_initialized:
            Etudes_Game.iterate(input_letter)
            clock.tick(200)
        else:
            Etudes_Game = Etudes(gametools)
            etudes_initialized = True

    if game_choice == "Search":
        if search_initialized:
            Search_Game.iterate(input_letter)
            clock.tick(200)
        else:
            Search_Game = Search(gametools)
            search_initialized = True

