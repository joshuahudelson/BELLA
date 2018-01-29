from BELLA_GAME import Bella_Game
import louis
from espeak import espeak

class Contraction_Action(Bella_Game):

    def __init__(self, gametools, display_data):
        super().__init__(gametools, display_data)

        self.input_letter = None
        self.key_was_pressed = None
        self.game_name = 'Contraction Action'

        self.pygame.display.set_caption('BELLA: Braille Early Learning & Literacy Arcade')

        self.options_list = ['KeyCrush', 'Whack-A-Dot', 'Cell Spotter', 'Alphabet Cards', 'Braille Tale']
        self.card_codes = {'a':'Alphabet Cards', 'b':'Braille Tale', 'k':'KeyCrush',
                           'w':'Whack-A-Dot', 'm':'Menu', 'c':'Cell Spotter'}

        self.braille_string = ''
        self.word_string = None


#---CENTRAL FUNCTIONS---

    def iterate(self, input_dict):
        self.update_dict.clear()
        self.input_letter = input_dict['letter']
        self.input_control = input_dict['standard']
        if self.input_control == 'display':
            self.current_display_state = (self.current_display_state + 1) % len(self.display_names)
        self.gameDisplay.fill(self.display_states[self.display_names[self.current_display_state]]['background'])
        self.display_sub_word_prompt(self.braille_string)
        self.pygame.display.update()

        if self.input_control == 'space':
            self.read_word_string()
        elif input_dict['braille_unicode'] != None:
            self.braille_string += input_dict['braille_unicode']

        return(self.update_dict)


    def read_word_string(self):
        try:
            self.word_string = louis.backTranslateString(['en-us-g2.ctb'], self.braille_string)
            espeak.synth(self.word_string)
            self.display_word_prompt(self.word_string)
            self.pygame.display.update()
            self.pygame.time.wait(1000)
            self.word_string = None
            self.braille_string = ''
        except(KeyError):
            espeak.synth("That's not a word.")
