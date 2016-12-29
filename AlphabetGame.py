
class AlphabetGame:
    """
    """

    def __init__(self, gametools, display_data, starting_game_state='introduction'):

#---META-GAME STUFF---

        self.pygame = gametools['pygame']
        self.sounds = gametools['sounds']
        self.np = gametools['numpy']
        self.gameDisplay = gametools['display']
        self.braille_keyboard = gametools['keyboard']


#---DISPLAY---
        
        self.SCREEN_WIDTH = display_data['screen_width']
        self.SCREEN_HEIGHT = display_data['screen_height']

        self.pygame.display.set_caption('Typing Tutor')
   
        self.font = self.pygame.font.SysFont(None, 80)
        self.font_small = self.pygame.font.SysFont(None, 40)
        self.font_large = self.pygame.font.SysFont(None, 500)
        
        self.white, self.black, self.yellow, self.blue = (255, 255, 255), (0, 0, 0), (255, 255, 0), (0, 0, 255)

        self.current_display_state = display_data['current_display_state']

        self.display_names = ['white_black', 'black_white', 'blue_yellow']

        self.display_states = {'black_white':{'background':self.black, 'text':self.white},
                               'white_black':{'background':self.white, 'text':self.black},
                               'blue_yellow':{'background':self.blue, 'text':self.yellow}}

#---SOUND---
        
        self.alpha = self.sounds.sounds('alphabet', self.pygame) #creates self.alpha.sound_dict dictionary
        self.alpha.sound_dict[' '] = {'sound':self.pygame.mixer.Sound('alphabet/space.wav'),
                                     'length':int(self.pygame.mixer.Sound('alphabet/space.wav').get_length() * 1000)
                                     }

        self.sfx = self.sounds.sounds('sfx', self.pygame)
        self.correct = self.sounds.sounds('correct', self.pygame)
        self.voice = self.sounds.sounds('voice', self.pygame)

        self.alphabet_sounds = self.sounds.sounds('alphabet_sounds', self.pygame)

#---GAME VARIABLES---

        self.card_str = None

        self.game_state = starting_game_state

        self.current_button = None

        self.press_counter = 0

        self.number_of_seconds_to_wait = 3

        self.num_prompts = 0

        self.max_num_prompts = 1

        self.intro_played = False

        self.current_cursor_button = None


#---CENTRAL FUNCTIONS---

    def iterate(self, input_dict):

        self.current_cursor_button = input_dict['cursor_key']
        self.input_control = input_dict['standard']

        self.gameDisplay.fill(self.display_states[self.display_names[self.current_display_state]]['background'])

        if self.input_control == 'display':
            self.change_display_state()
                
        if self.game_state == 'introduction':
            self.introduction(input_dict)
        elif self.game_state == 'game_play':
            self.game_play(self.current_cursor_button)

        self.pygame.display.update()


    def introduction(self, input_dict):

        if input_dict['card_state']:
            self.card_str = input_dict['card_str']
            self.play_sfx('cardinserted',wait=True) # we need to rename this sound effect.  Just call it beep.
            self.game_state = 'game_play'
        elif self.intro_played == False:
            self.play_voice('insert_card')
            self.intro_played = True

 

    def game_play(self, cursor_button):

        if cursor_button != None:

            if self.current_button != cursor_button:  # make own function...
                self.current_button = cursor_button
                self.press_counter = 0

            character = self.card_str[self.current_button]
            
            if character == ' ':   # make own function...
                self.play_sfx('wrong')
            else:
                self.play_alphabet_sound(character + str(self.press_counter))
                self.press_counter = (self.press_counter + 1) % 3

        if self.current_button == None:
            self.display_letter_prompt(' ')
        else:
            self.display_letter_prompt(self.card_str[self.current_button])


#---SOUND FUNCTIONS

    def play_alpha(self, sound, wait=False):
        self.alpha.sound_dict[sound]['sound'].play()
        if wait:
            self.pygame.time.wait(self.alpha.sound_dict[sound]['length'])

    def play_sfx(self, sound, wait=False):
        self.sfx.sound_dict[sound]['sound'].play()
        if wait:
            self.pygame.time.wait(self.sfx.sound_dict[sound]['length'])


    def play_correct(self, correct, wait=False):
        self.correct.sound_dict[correct]['sound'].play()
        if wait:
            self.pygame.time.wait(self.correct.sound_dict[correct]['length'])


    def play_voice(self, voice, wait=False):
        self.voice.sound_dict[voice]['sound'].play()
        if wait:
            self.pygame.time.wait(self.voice.sound_dict[voice]['length'])

    def play_alphabet_sound(self, sound, wait=False):
        self.alphabet_sounds.sound_dict[sound]['sound'].play()
        if wait:
            self.pygame.time.wait(self.alphabet_sounds.sound_dict[sound]['length'])


#---DISPLAY FUNCTIONS---

    def change_display_state(self):
        self.current_display_state = (self.current_display_state + 1) % len(self.display_names)


    def display_letter_prompt(self, letter=None):
        """ Write the current letter prompt to the screen.
        """
        if letter == None:
            letter = self.current_button
            
        displaybox = self.pygame.draw.rect(self.gameDisplay,
                                           self.display_states[self.display_names[self.current_display_state]]['background'],
                                           ((self.SCREEN_WIDTH/2)-200, 108, 400, 50))

        text = self.font_large.render(letter, True,
                                      self.display_states[self.display_names[self.current_display_state]]['text'])

        temp_width = text.get_rect().width

        self.gameDisplay.blit(text, ((self.SCREEN_WIDTH / 2) - (temp_width/2), 100))

