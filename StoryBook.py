
class StoryBook:
    """
    """

    def __init__(self, gametools, display_data, starting_game_state='introduction'):

#---META-GAME STUFF---

        self.pygame = gametools['pygame']
        self.sounds = gametools['sounds']
        self.np = gametools['numpy']
        self.fps = gametools['fps']
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
        self.card_words = None

        self.game_state = starting_game_state

        self.sequence_count = 0

        self.sequence_triggers = ['key1', 'key2', 'key3', 'key4', 'key2', 'key5', 'key6']

        self.sample_names = {'key1': 'bark', 'key2': 'door', 'key3': 'sniffing', 'key4': 'squeaktoy',
                             'key5': 'pourfood', 'key6': 'pourwater'}

        self.serial_delay_factor = gametools['serial_delay_factor']

        self.current_button = None

        self.frames_passed = 0

        self.intro_played = False

        self.sequences = None


#---GAME VARIABLES---

    def iterate(self, input_dict):

        self.gameDisplay.fill(self.display_states[self.display_names[self.current_display_state]]['background'])

        self.input_key = input_dict['key']
        self.input_button = input_dict['cursor_key']
        self.input_control = input_dict['standard']

        if self.input_control == 'display':
            self.change_display_state()
        
        self.frames_passed +=1
        print(self.frames_passed)

        if self.input_key == 'backspace':
            self.current_display_state = (self.current_display_state + 1) % (len(self.display_names))

        if self.game_state == 'introduction':
            self.introduction(input_dict)
        elif self.game_state == 'game_play':
            self.game_play()

        self.pygame.display.update()


    def introduction(self, input_dict):

        if input_dict['card_state']:
            self.card_str = input_dict['card_str']
            self.make_sound_dicts()
            self.play_sfx('cardinserted',wait=True)
            self.game_state = 'game_play'
            self.play_sequence('seq1')
            self.frames_passed = 0            
        elif self.intro_played == False:
            self.play_voice('insert_card', True)
            self.intro_played = True

    def game_play(self):

        if self.frames_passed > (self.fps * self.serial_delay_factor):
            if self.sequence_count < len(self.sequence_triggers):
                self.vibrate_buttons(self.sequence_triggers[self.sequence_count])
                print('Sequence count:' + str(self.sequence_count))
                print('# Triggers:' + str(len(self.sequence_triggers)))
                self.frames_passed = 0

        if self.input_key != None:

            self.play_samples(self.sample_names[self.input_key], True)
            
            self.pygame.time.wait(100) # just a little extra time

            if self.sequence_count < len(self.sequence_triggers):
                if self.input_key == self.sequence_triggers[self.sequence_count]:
                    self.pygame.mixer.stop()
                    self.sequence_count += 1
                    self.play_sequence('seq' + str(self.sequence_count + 1))
                    self.frames_passed = 0

        if self.input_button != None:

            if self.card_str[self.input_button] == '_':   # make own function...
                self.play_sfx('wrong')
                      
            else:
                
                self.play_alpha(self.card_str[self.input_button])


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
        
        self.braille_keyboard.vibrate_single_key(character)


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


#---DISPLAY FUNCTIONS---

    def change_display_state(self):
        self.current_display_state = (self.current_display_state + 1) % len(self.display_names)




