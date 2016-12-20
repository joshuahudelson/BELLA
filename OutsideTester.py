from TypingTutor import TypingTutor
import numpy
import keyboard
import pygame
import sounds

pygame.mixer.pre_init(22050, -16,  2, 512)

pygame.init()


braille_keyboard = keyboard.keyboard()
braille_keyboard.test_coms()    # automatically finds keyboard

clock = pygame.time.Clock()

input_letter = None

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

key_was_pressed = False

gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


gametools = {'pygame':pygame,
             'numpy':numpy,
             'sounds':sounds,
             'keyboard':keyboard,
             'display':gameDisplay}

test_instance = TypingTutor(gametools)




while(True):

    input_letter = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # if the window "x" has been pressed quit the game
            quitGame = True

    braille_keyboard.request_buttons()  # get button presses from keyboard

    if braille_keyboard.last_letter!=None :  # if button was pressed
        input_letter = braille_keyboard.last_letter
        key_was_pressed = True
    else:
        key_was_pressed = False
    
    test_instance.iterate(input_letter, key_was_pressed)

    clock.tick(200)

