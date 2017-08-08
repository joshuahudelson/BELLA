from random import choice, randint

class Bella_Game:

    def __init__(self, gametools, display_data, starting_level=0):
        """ A class for BELLA games.  Creates all the variables and functions
        that would be duplicated, such as the sound and display functions.
        """

#---META-GAME STUFF---

        self.pygame = gametools['pygame']
        self.sounds = gametools['sounds']
        self.np = gametools['numpy']
        self.gameDisplay = gametools['display']
        self.braille_keyboard = gametools['keyboard']
        self.fps = gametools['fps']
        self.sound_object = self.sounds.sounds()

#---DISPLAY---

        self.SCREEN_WIDTH = display_data['screen_width']
        self.SCREEN_HEIGHT = display_data['screen_height']

        self.pygame.display.set_caption('Typing Tutor')

        self.font = self.pygame.font.SysFont(None, 80)
        self.font_small = self.pygame.font.SysFont(None, 40)
        self.font_medium = self.pygame.font.SysFont(None, 110)
        self.font_large = self.pygame.font.SysFont(None, 500)

        self.white, self.black, self.yellow, self.blue = (255, 255, 255), (0, 0, 0), (255, 255, 0), (0, 0, 255)

        self.current_display_state = display_data['current_display_state']

        self.display_names = ['white_black', 'black_white', 'blue_yellow']

        self.display_states = {'black_white':{'background':self.black, 'text':self.white},
                               'white_black':{'background':self.white, 'text':self.black},
                               'blue_yellow':{'background':self.blue, 'text':self.yellow}}

#---SOUNDS---

        standard_alphabet_dir= self.sounds.join('standardsounds', 'Alphabet')
        standard_sfx_dir = self.sounds.join('standardsounds', 'Sfx')
        standard_voice_dir = self.sounds.join('standardsounds', 'Voice')


        self.standard_alphabet = self.sound_object.make_sound_dictionary(standard_alphabet_dir, self.pygame)
        self.standard_sfx = self.sound_object.make_sound_dictionary(standard_sfx_dir, self.pygame)
        self.standard_voice = self.sound_object.make_sound_dictionary(standard_voice_dir, self.pygame)

        self.standard_alphabet[' '] = {'sound':self.pygame.mixer.Sound(self.sounds.join(standard_alphabet_dir, 'space.wav')),
                                     'length':int(self.pygame.mixer.Sound(self.sounds.join(standard_alphabet_dir, 'space.wav')).get_length() * 1000)}

#---SOUND FUNCTIONS---

    def play_sound(self, sound, dictionary, wait=False):
        """ Plays a sound.  If wait is True, the game loop pauses
            until the sound has finished playing.
        """
        dictionary[sound]['sound'].play()
        if wait:
            self.pygame.time.wait(dictionary[sound]['length'])


#---DISPLAY FUNCTIONS---

    def change_display_state(self):
        """ When called, iterates to the next display state, which
            determines the colors of the text and background.
        """
        self.current_display_state = (self.current_display_state + 1) % len(self.display_names)
        # change this along with the main Bella program so that the main program just sends in the state number, no computing or tracking on this side.


    def display_letter_prompt(self, letter=None):
        """ Write the current letter prompt to the screen.
            If no input is given, displays the game's current letter prompt.
        """
        if letter == None:
            letter = self.letter_prompt

        displaybox = self.pygame.draw.rect(self.gameDisplay,
                                           self.display_states[self.display_names[self.current_display_state]]['background'],
                                           ((self.SCREEN_WIDTH/2)-200, 108, 400, 50))

        text = self.font_large.render(letter, True,
                                      self.display_states[self.display_names[self.current_display_state]]['text'])

        temp_width = text.get_rect().width

        self.gameDisplay.blit(text, ((self.SCREEN_WIDTH / 2) - (temp_width/2), 100))


    def display_word_prompt(self, word=None):
        """ Write the current word prompt to the screen.
            If no input is given, displays the game's current letter prompt.
        """

        if word == None:
            word = self.word_prompt
        displaybox = self.pygame.draw.rect(self.gameDisplay, self.display_states[self.display_names[self.current_display_state]]['background'], ((self.SCREEN_WIDTH/2)-200, 108, 400, 50))
        text = self.font.render(word, True, self.display_states[self.display_names[self.current_display_state]]['text'])
        temp_width = text.get_rect().width
        self.gameDisplay.blit(text, ((self.SCREEN_WIDTH / 2) - (temp_width/2), 100))


    def display_status_box(self):
        """ Displays the current level and points on the screen.
        """
        level = self.font_medium.render("Level: " + str(self.level), True,
                                      self.display_states[self.display_names[self.current_display_state]]['text'],
                                      self.display_states[self.display_names[self.current_display_state]]['background'])

        points = self.font_medium.render("Points: " + str(self.score), True,
                                       self.display_states[self.display_names[self.current_display_state]]['text'],
                                       self.display_states[self.display_names[self.current_display_state]]['background'])

        level_width = level.get_rect().width
        points_width = points.get_rect().width

        self.gameDisplay.blit(level, (((self.SCREEN_WIDTH/2.0) - level_width)/2, 10))
        self.gameDisplay.blit(points, ((((self.SCREEN_WIDTH/2.0) - points_width)/2) + (self.SCREEN_WIDTH/2.0), 10))


    def draw_buttons(self, keys='000000'):
        """ Draw all six buttons to the screen.
            Color depends on input code and display_state.
        """

        xpos = None
        ypos = 500
        button_width = 60
        button_height = 80
        offset = 7

        x_divisor = self.SCREEN_WIDTH / 6
        x_scalar = 0.8
        x_buffer = (1.0 - x_scalar) * self.SCREEN_WIDTH * 0.5
        x_middle = self.SCREEN_WIDTH * 0.07

        key_order = [3, 4, 5, 2, 1, 0]

        for i in range(len(keys)):
            if keys[key_order[i]] == '1':
                color = self.display_states[self.display_names[self.current_display_state]]['text']
            elif keys[key_order[i]] == '0':
                color = self.display_states[self.display_names[self.current_display_state]]['background']

            if i > 2:
                xpos = (i* x_divisor * x_scalar) + x_buffer + x_middle
            else:
                xpos = (i* x_divisor * x_scalar) + x_buffer

            position = (xpos, ypos, button_width, button_height)
            position_small = (xpos + offset, ypos + offset, button_width - (2 * offset), button_height - (2 * offset))

            self.draw_single_button(self.display_states[self.display_names[self.current_display_state]]['text'], position)
            self.draw_single_button(color, position_small)


    def draw_single_button(self, color, position):
        """ Draw a single button to the screen.
        """

        self.pygame.draw.ellipse(self.gameDisplay, color, position)
