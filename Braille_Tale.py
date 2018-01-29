from itertools import groupby
import copy
from BELLA_GAME import Bella_Game

class Braille_Tale(Bella_Game):
    """
    """

    def __init__(self, gametools, display_data, starting_game_state='introduction'):
        super().__init__(gametools, display_data)

#---META-GAME STUFF---

        self.pygame = gametools['pygame']
        self.sounds = gametools['sounds']
        self.np = gametools['numpy']
        self.fps = gametools['fps']
        self.gameDisplay = gametools['display']
        self.braille_keyboard = gametools['keyboard']

        self.sound_object = self.sounds.sounds()

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
        self.game_name = 'Braille_Tale'
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

        if self.input_control == 'display':
            self.change_display_state()

        self.frames_passed +=1

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
            self.card_words = self.card_str.split('_')
            print(self.card_words)

            self.make_sound_dicts()
            self.play_sound('cardinserted', self.standard_sfx, wait=True)

            self.game_state = 'game_play'

            self.play_sound('seq1', self.sequences)
            self.frames_passed = 0
        elif self.intro_played == False:
            self.play_sound('insert_a_card', self.standard_voice, True)
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

            print(self.input_button)
            print(self.input_buttons_list)

            if len(self.input_buttons_list) == 2:

                    if self.input_buttons_list[0] != self.input_buttons_list[1] + 1:  # the list is reverse-ordered
                        self.play_sound('wrong', self.standard_sfx)

                    else:
                        print("Did it!")
                        temp_word = self.get_whole_string(self.input_buttons_list[1], self.card_str)
                        try:
                            self.play_sound(temp_word, self.words)
                        except:
                            self.play_sound('wrong', self.standard_sfx)
                            print("Couldn't find word?")

            elif self.card_str[self.input_button] == '_':
                self.play_sound('wrong', self.standard_sfx)

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


    def vibrate_buttons(self, character):
        """ Vibrate the buttons that correspond to the current prompt.
        """
        self.braille_keyboard.vibrate_single_key(character)


    def get_whole_string(self, location, card_str):
        if card_str[location] == '_':
            return None
        else:
            temp_str = ''
            for i in range(location + 1):
                if card_str[location-i] != '_':
                    temp_str = card_str[location-i] + temp_str
                else:
                    break
            for i in range(len(card_str) - location - 1):
                if card_str[location+i+1] != '_':
                    temp_str = temp_str + card_str[location+i+1]
                else:
                    break

            return temp_str
