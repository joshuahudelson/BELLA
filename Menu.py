
class Menu:

    def __init__(self, gametools, display_data):

        
        self.input_letter = None
        self.key_was_pressed = None

        self.pygame = gametools['pygame']
        self.sounds = gametools['sounds']
        self.np = gametools['numpy']
        self.gameDisplay = gametools['display']

        self.sound_object = self.sounds.sounds()
        self.game_name = 'Menu'

        self.SCREEN_WIDTH = display_data['screen_width']
        self.SCREEN_HEIGHT = display_data['screen_height']
        
        self.pygame.display.set_caption('BELLA: Braille Early Learning & Literacy Arcade')

        self.braille_keyboard = gametools['keyboard']
                
        self.font = self.pygame.font.SysFont(None, 80)
        self.font_small = self.pygame.font.SysFont(None, 40)
        self.font_large = self.pygame.font.SysFont(None, 500)
        
        self.white, self.black, self.yellow, self.blue = (255, 255, 255), (0, 0, 0), (255, 255, 0), (0, 0, 255)


        self.current_display_state = display_data['current_display_state']

        self.display_names = ['white_black', 'black_white', 'blue_yellow']

        self.display_states = {'black_white':{'background':self.black, 'text':self.white},
                               'white_black':{'background':self.white, 'text':self.black},
                               'blue_yellow':{'background':self.blue, 'text':self.yellow}}

        self.options_list = ['KeyCrush', 'Whack-A-Dot', 'Cell Spotter', 'Alphabet Cards', 'Braille Tale']

        self.card_codes = {'a':'Alphabet Cards', 'b':'Braille Tale', 'k':'KeyCrush',
                      'w':'Whack-A-Dot', 'm':'Menu', 'c':'Cell Spotter'}

        self.option_tracker = 0

        self.introduction_done = False


#---SOUNDS---

        standard_alphabet_dir= self.sounds.join('standardsounds', 'Alphabet')
        standard_sfx_dir = self.sounds.join('standardsounds', 'Sfx')
        standard_voice_dir = self.sounds.join('standardsounds', 'Voice')


        self.standard_alphabet = self.sound_object.make_sound_dictionary(standard_alphabet_dir, self.pygame)
        self.standard_sfx = self.sound_object.make_sound_dictionary(standard_sfx_dir, self.pygame)
        self.standard_voice = self.sound_object.make_sound_dictionary(standard_voice_dir, self.pygame)

        self.game_sounds = self.sound_object.make_sound_dictionary(self.game_name + '_sounds', self.pygame)

        
        self.standard_alphabet[' '] = {'sound':self.pygame.mixer.Sound(self.sounds.join(standard_alphabet_dir, 'space.wav')),
                                     'length':int(self.pygame.mixer.Sound(self.sounds.join(standard_alphabet_dir, 'space.wav')).get_length() * 1000)}



    def iterate(self, input_dict):

        if input_dict['card_trigger']:
            for letter in self.card_codes:
                if input_dict['card_ID'] == letter:
                    return self.card_codes[input_dict['card_ID']]
                else:
                    print(input_dict['card_ID'])

        self.input_letter = input_dict['letter']
        self.input_control = input_dict['standard']

        if self.input_control == 'display':
            self.current_display_state = (self.current_display_state + 1) % len(self.display_names)

        self.gameDisplay.fill(self.display_states[self.display_names[self.current_display_state]]['background'])

        self.display_options()
        self.pygame.display.update()

        if self.introduction_done == False:
            self.introduction()

        if self.input_control == 'newline':
            self.option_tracker += 1
            self.play_sound(self.options_list[self.selection], self.game_sounds)
            return None
        elif self.input_control == 'backspace':
            self.option_tracker -= 1
            self.play_sound(self.options_list[self.selection], self.game_sounds)
            return None
        elif self.input_control == 'space':
#            self.play_sound('press_main_menu', self.game_sounds, True)
#            self.play_sound('display', self.game_sounds, True)
            return self.options_list[self.selection]
        else:
            return None


    def introduction(self):
        self.play_sound('intro', self.game_sounds, True)
#        self.play_sound('lets_play', self.game_sounds, True)
#        self.play_sound('instructions', self.game_sounds, True)
#        self.play_sound(self.options_list[self.selection], self.game_sounds)

        self.introduction_done = True


#---SOUND FUNCTIONS---
    
    def play_sound(self, sound, dictionary, wait=False):
        dictionary[sound]['sound'].play()
        if wait:
            self.pygame.time.wait(dictionary[sound]['length'])



#---DISPLAY FUNCTIONS---

    def display_options(self):

        num_options = len(self.options_list)

        division_len = self.SCREEN_HEIGHT / num_options

        buffer = 20

        diminisher = 0.8
        
        for i in range(len(self.options_list)):
            self.display_single_option(self.options_list[i], ((i * division_len) * diminisher) + buffer, i==self.selection)


    def display_single_option(self, word, location, highlight=False):
        
        if highlight:
            color = self.display_states[self.display_names[self.current_display_state]]['background']

            displaybox = self.pygame.draw.rect(self.gameDisplay,
                                       self.display_states[self.display_names[self.current_display_state]]['text'],
                                       ((self.SCREEN_WIDTH/2)-200, location, 400, 50))
        else:
            color = self.display_states[self.display_names[self.current_display_state]]['text']
            
        text = self.font.render(word, True, color)
        temp_width = text.get_rect().width
        self.gameDisplay.blit(text, ((self.SCREEN_WIDTH / 2) - (temp_width/2), location))


    @property
    def selection(self):
        return self.option_tracker % len(self.options_list)


