
class Menu:

    def __init__(self, gametools, display_data):

        
        self.input_letter = None
        self.key_was_pressed = None

        self.pygame = gametools['pygame']
        self.sounds = gametools['sounds']
        self.np = gametools['numpy']
        self.gameDisplay = gametools['display']

        self.SCREEN_WIDTH = display_data['screen_width']
        self.SCREEN_HEIGHT = display_data['screen_height']
        
        self.pygame.display.set_caption('BrailleCade Game Suite')

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

        self.options_list = ['KeyCrush', 'Etudes', 'Search', 'Alphabet Game', 'StoryBook']

        self.card_codes = {'a':'Alphabet Game', 'b':'StoryBook', 'k':'KeyCrush',
                      'e':'Etudes', 'm':'Menu', 'w':'Search'}

        self.option_tracker = 0

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

        if self.input_control == 'newline':
            self.option_tracker += 1
            return None
        elif self.input_control == 'backspace':
            self.option_tracker -= 1
            return None
        elif self.input_control == 'space':
            return self.options_list[self.selection]
        else:
            return None


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

        
