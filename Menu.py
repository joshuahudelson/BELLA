from BELLA_GAME import Bella_Game

class Menu(Bella_Game):

    def __init__(self, gametools, display_data, BELLA_start_up):
        super().__init__(gametools, display_data)

        self.input_letter = None
        self.key_was_pressed = None
        self.BELLA_start_up = BELLA_start_up

        self.game_name = 'Menu'

        self.pygame.display.set_caption('BELLA: Braille Early Learning & Literacy Arcade')

        self.options_list = ['KeyCrush', 'Whack-A-Dot', 'Cell Spotter', 'Alphabet Cards', 'Braille Tale']
        self.card_codes = {'a':'Alphabet Cards', 'b':'Braille Tale', 'k':'KeyCrush',
                           'w':'Whack-A-Dot', 'm':'Menu', 'c':'Cell Spotter'}
        self.option_tracker = 0
        self.introduction_done = False

#---LOCAL GAME SOUNDS---

        self.game_sounds = self.sound_object.make_sound_dictionary(self.game_name + '_sounds', self.pygame)

#---CENTRAL FUNCTIONS---

    def iterate(self, input_dict):

        if input_dict['card_trigger']:
            for letter in self.card_codes:
                if input_dict['card_ID'] == letter:
                    #self.play_sound('playing', self.game_sounds, wait = True)
                    #self.play_sound(self.card_codes[input_dict['card_ID']], self.game_sounds, wait = True)
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
            self.pygame.mixer.stop()
            self.option_tracker += 1
            self.play_sound(self.options_list[self.selection], self.game_sounds)
            return None
        elif self.input_control == 'backspace':
            self.pygame.mixer.stop()
            self.option_tracker -= 1
            self.play_sound(self.options_list[self.selection], self.game_sounds)
            return None
        elif self.input_control == 'space':
            self.pygame.mixer.stop()
#            self.play_sound('press_main_menu', self.game_sounds, True)
#            self.play_sound('display', self.game_sounds, True)
            self.play_sound('letsplay_'+self.options_list[self.selection], self.game_sounds, wait = True)
            #self.play_sound(self.options_list[self.selection], self.game_sounds, wait = True)
            return self.options_list[self.selection]
        else:
            return None


    def introduction(self):
        if self.BELLA_start_up:
            self.play_sound('intro', self.game_sounds)
        else:
            self.play_sound('main_menu', self.game_sounds)
        self.introduction_done = True

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
