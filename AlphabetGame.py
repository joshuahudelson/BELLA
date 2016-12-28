
class AlphabetGame:
    """
    """

    def __init__(self, gametools, starting_game_state='introduction'):

        self.pygame = gametools['pygame']
        self.sounds = gametools['sounds']
        self.np = gametools['numpy']
        self.gameDisplay = gametools['display']
        self.fps = gametools['fps']

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.bg = self.pygame.image.load("English_braille_sample.jpg")
        self.pygame.display.set_caption('Typing Tutor')

        self.braille_keyboard = gametools['keyboard']
        
        self.font = self.pygame.font.SysFont(None, 80)
        self.font_small = self.pygame.font.SysFont(None, 40)
        
        self.white, self.black, self.red, self.blue = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255)
        self.gray1, self.gray2 = (160, 160, 160), (80, 80, 80)
        self.light_blue, self.yellow = (0, 100, 255), (0, 255, 255)

        self.card_str = None

        self.game_state = starting_game_state

        self.current_button = None

        self.press_counter = 0

        self.timer = 0

        self.number_of_seconds_to_wait = 3

        self.num_prompts = 0

        self.max_num_prompts = 1

        self.intro_played = False

        self.current_cursor_button = None

        self.current_display_state = 0

        self.display_names = ['black_white', 'red_blue']

        self.display_states = {'black_white':{'background':self.black, 'letters':self.white},
                               'red_blue':{'background':self.red, 'letters':self.blue}}

#---SOUND---
        
        self.alpha = self.sounds.sounds('alphabet', self.pygame) #creates self.alpha.sound_dict dictionary
        self.alpha.sound_dict[' '] = {'sound':self.pygame.mixer.Sound('alphabet/space.wav'),
                                     'length':int(self.pygame.mixer.Sound('alphabet/space.wav').get_length() * 1000)
                                     }

        self.sfx = self.sounds.sounds('sfx', self.pygame)
        self.correct = self.sounds.sounds('correct', self.pygame)
        self.voice = self.sounds.sounds('voice', self.pygame)

        self.alphabet_sounds = self.sounds.sounds('alphabet_sounds', self.pygame)
        



    def iterate(self, input_dict):

        self.current_cursor_button = input_dict['cursor_key']

        self.gameDisplay.fill(self.display_states[self.display_names[self.current_display_state]]['background'])

        self.timer += 1

        if self.current_cursor_button == 'backspace':  # Display shift stuff... move and change
            self.current_display_state = (self.current_display_state + 1) % (len(self.display_names))

        if int(self.timer/float(self.fps)) > self.number_of_seconds_to_wait:
            if self.num_prompts < self.max_num_prompts:
                print('reminder!')
                
        if self.game_state == 'introduction':
            self.introduction(input_dict)
        elif self.game_state == 'game_play':
            self.game_play(self.current_cursor_button)

        print(self.timer)

        self.pygame.display.update()


    def introduction(self, input_dict):
        if self.intro_played == False:
            self.play_voice('insert_card')
            self.intro_played = True
        else:
            if input_dict['card_trigger']:
                self.card_str = input_dict['card_str']
                self.play_sfx('cardinserted',wait=True) # we need to rename this sound effect.  Just call it beep.
                self.game_state = 'game_play'


    def game_play(self, cursor_button):

        print(cursor_button)

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


#---SOUND AND DISPLAY FUNCTIONS

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

   
    def display_letter_prompt(self, prompt):
        """ Write the current letter prompt to the screen.
        """
        text = self.font.render(prompt, True, self.display_states[self.display_names[self.current_display_state]]['letters'])
        temp_width = text.get_rect().width
        self.pygame.draw.rect(self.gameDisplay, self.display_states[self.display_names[self.current_display_state]]['background'], ((self.SCREEN_WIDTH / 2) - 100, 102, 200, 55))
        self.gameDisplay.blit(text, ((self.SCREEN_WIDTH / 2) - (temp_width / 2), 100))


    def display_word_prompt(self, prompt):
        """ Write the current word prompt to the screen.
        """
        displaybox = self.pygame.draw.rect(self.gameDisplay, self.display_states[self.display_names[self.current_display_state]]['letters'], ((self.SCREEN_WIDTH/2)-200, 108, 400, 50))
        text = self.font.render(prompt, True, self.display_states[self.current_display_state][self.background])
        temp_width = text.get_rect().width
        self.gameDisplay.blit(text, ((self.SCREEN_WIDTH / 2) - (temp_width/2), 100))


