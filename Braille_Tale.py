from itertools import groupby
import copy

class Braille_Tale:
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

        self.sound_object = self.sounds.sounds()

#---DISPLAY---
        
        self.SCREEN_WIDTH = display_data['screen_width']
        self.SCREEN_HEIGHT = display_data['screen_height']

        self.pygame.display.set_caption('Braille Tale')
   
        self.font = self.pygame.font.SysFont(None, 80)
        self.font_small = self.pygame.font.SysFont(None, 40)
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

        self.samples = None

        self.cursor_keys = None


#---GAME VARIABLES---

    def iterate(self, input_dict):

        self.gameDisplay.fill(self.display_states[self.display_names[self.current_display_state]]['background'])

        self.input_key = input_dict['key']
        self.input_button = input_dict['cursor_key']
        self.input_buttons_list = input_dict['cursor_keys_list']
        self.input_control = input_dict['standard']

        self.input_buttons_multiple = input_dict['cursor_keys_list']

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
            self.card_ranges = list(self.split_card_string(self.card_str))
            self.card_words = self.card_str.split('_')

            self.make_sound_dicts()
            self.play_sound('cardinserted', self.standard_sfx, wait=True)

            self.game_state = 'game_play'

            self.play_sound('seq1', self.sequences)
            self.frames_passed = 0            
        elif self.intro_played == False:
            self.play_sound('insert_card', self.standard_voice, True)
            self.intro_played = True

    def game_play(self):

        if self.frames_passed > (self.fps * self.serial_delay_factor):
            if self.sequence_count < len(self.sequence_triggers):
                self.vibrate_buttons(self.sequence_triggers[self.sequence_count])
                print('Sequence count:' + str(self.sequence_count))
                print('# Triggers:' + str(len(self.sequence_triggers)))
                self.frames_passed = 0

        if self.input_key != None:

            self.play_sound(self.sample_names[self.input_key], self.samples, True)
            
            self.pygame.time.wait(100) # just a little extra time

            if self.sequence_count < len(self.sequence_triggers):
                if self.input_key == self.sequence_triggers[self.sequence_count]:
                    self.pygame.mixer.stop()
                    self.sequence_count += 1
                    self.play_sound('seq' + str(self.sequence_count + 1), self.sequences)
                    self.frames_passed = 0

        if self.input_button != None:

            if self.card_str[self.input_button] == '_':   # make own function...
                self.play_sound('wrong', self.standard_sfx)
                      
            elif sum(self.input_buttons_list) > 1:
                
                    if self.input_buttons_list[self.input_button + 1] != '1':
                        pass
                    else:
                        for i in range(len(self.card_ranges)):
                            if self.input_button in range(self.card_ranges[i][0], self.card_ranges[i][1]):
                                play_sound(self.card_words[i], self.words)
            else:
                self.play_sound(self.card_str[self.input_button], self.standard_alphabet)


    def make_sound_dicts(self):

        try:
            sequences_dir = self.sounds.join(self.card_str, 'sequences')
            print("Card String: " + self.card_str)
            self.sequences = self.sound_object.make_sound_dictionary(sequences_dir, self.pygame)
        except:
            print("Can't find sequences directory.")
            print(sequences_dir)

        try:
            samples_dir = self.sounds.join(self.card_str, 'samples')
            self.samples = self.sound_object.make_sound_dictionary(samples_dir, self.pygame)
        except:
            print("Can't find samples directory.")
            print(samples_dir)

        try:
            words_dir = self.sounds.join(self.card_str, 'words')
            print("Card String: " + self.card_str)
            self.words = self.sound_object.make_sound_dictionary(words_dir, self.pygame)
        except:
            print("Can't find word directory.")
            print(samples_dir)

    def vibrate_buttons(self, character):
        """ Vibrate the buttons that correspond to the current prompt.
        """
        
        self.braille_keyboard.vibrate_single_key(character)


    def split_card_string(self, s, c='_'):
        p = 0
        for k, g in groupby(s, lambda x:x==c):
            q = p + sum(1 for i in g)
            if not k:
                yield p, q-1 # or p, q-1 if you are really sure you want that
            p = q

#---SOUND FUNCTIONS---
    
    def play_sound(self, sound, dictionary, wait=False):
        dictionary[sound]['sound'].play()
        if wait:
            self.pygame.time.wait(dictionary[sound]['length'])


#---DISPLAY FUNCTIONS---

    def change_display_state(self):
        self.current_display_state = (self.current_display_state + 1) % len(self.display_names)




