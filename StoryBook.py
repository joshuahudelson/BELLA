
class StoryBook:
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
        self.card_words = None

        self.game_state = starting_game_state

        self.sequence_count = 0

        self.sequence_triggers = ['a', 'key2', 'key3', 'key4', 'key2', 'key5', 'key6']

        self.sample_names = {'a': 'bark', 'key2': 'door', 'key3': 'sniffing', 'key4': 'squeaktoy',
                             'key5': 'pourfood', 'key6': 'pourwater'}

        self.serial_delay_factor = gametools['serial_delay_factor']

        self.current_button = None

        self.frames_passed = 0

        self.intro_played = False

        self.sequences = None

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
        

    def iterate(self, input_letter, input_button):

        self.frames_passed +=1
        print(self.frames_passed)

        self.gameDisplay.fill(self.display_states[self.display_names[self.current_display_state]]['background'])

        if input_letter == 'backspace':
            self.current_display_state = (self.current_display_state + 1) % (len(self.display_names))

        if self.game_state == 'introduction':
            self.introduction()
        elif self.game_state == 'game_play':
            self.game_play(input_letter, input_button)


    def introduction(self):
        if self.intro_played == False:
            self.play_voice('insert_card', True)
            self.intro_played = True
        else:
            if self.braille_keyboard.last_button_state == '11111111111111111111111111111111':
                self.braille_keyboard.request_card()
                self.card_str = self.braille_keyboard.card_str
                self.make_sound_dicts()
                self.play_sfx('cardinserted',wait=True) # we need to rename this sound effect.  Just call it beep.
                self.game_state = 'game_play'
                self.play_sequence('seq1')
                self.frames_passed = 0


    def game_play(self, input_letter, input_button):

        if self.sequence_count > len(self.sequence_triggers) - 1:
            self.sequence_count = len(self.sequence_triggers) -1

        if self.frames_passed > (self.fps * self.serial_delay_factor):
            if self.sequence_count < len(self.sequence_triggers) - 1:
                self.vibrate_buttons(self.sequence_triggers[self.sequence_count])
                self.frames_passed = 0

        if input_letter != None:

            self.play_samples(self.sample_names[input_letter], True)
            
            self.pygame.time.wait(100) # just a little extra time

            if input_letter == self.sequence_triggers[self.sequence_count]:
                self.pygame.mixer.stop()            
                if self.sequence_count < len(self.sequence_triggers):
                    self.sequence_count += 1
                    self.play_sequence('seq' + str(self.sequence_count + 1))
                    self.frames_passed = 0

        if input_button != None:

            if self.card_str[input_button] == '_':   # make own function...
                self.play_sfx('wrong')
                      
            else:
                
                self.play_alpha(self.card_str[input_button])


    def make_sound_dicts(self):

        try:
            sequences_dir = self.sounds.join(self.card_str, 'sequences')
            print("Card String: " + self.card_str)
            self.sequences = self.sounds.sounds(sequences_dir, self.pygame)
        except:
            print("Can't find sequences directory.")
            print(sequences_dir)

        try:
            samples_dir = self.sounds.join(self.card_str, 'samples')
            self.samples = self.sounds.sounds(samples_dir, self.pygame)
        except:
            print("Can't find samples directory.")
            print(samples_dir)


    def vibrate_buttons(self, character):
        """ Vibrate the buttons that correspond to the current prompt.
        """
        
        self.braille_keyboard.vibrate_letter(character, sim=True)


#---SOUND AND DISPLAY FUNCTIONS

    def play_sequence(self, sound, wait=False):
        self.sequences.sound_dict[sound]['sound'].play()
        if wait:
            self.pygame.time.wait(self.sequences.sound_dict[sound]['length'])


    def play_samples(self, sound, wait=False):
        self.samples.sound_dict[sound]['sound'].play()
        if wait:
            self.pygame.time.wait(self.samples.sound_dict[sound]['length'])

            
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


