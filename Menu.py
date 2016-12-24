
class Menu:

    def __init__(self, gametools):
        self.input_letter = None
        self.key_was_pressed = None

        self.pygame = gametools['pygame']
        self.sounds = gametools['sounds']
        self.np = gametools['numpy']
        self.gameDisplay = gametools['display']

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

        self.options_list = ['Typing Tutor', 'Etudes', 'Search', 'Alphabet Game']

        self.option_tracker = 0

    def iterate(self, input_letter):

        self.input_letter = input_letter

        self.gameDisplay.blit(self.bg, (0,0))

        self.display_options()
        self.pygame.display.update()

        if self.input_letter == 'newline':
            self.option_tracker += 1
            return None
        elif self.input_letter == 'backspace':
            self.option_tracker -= 1
            return None
        elif self.input_letter == 'space':
            return self.options_list[self.selection]
        else:
            return None


    def display_options(self):
        for i in range(len(self.options_list)):
            self.display_single_option(self.options_list[i], (i * 100) + 200, i==self.selection)


    def display_single_option(self, word, location, highlight=False):
        if highlight:
            color = self.blue
        else:
            color = self.black
        text = self.font.render(word, True, color)
        temp_width = text.get_rect().width
        self.gameDisplay.blit(text, ((self.SCREEN_WIDTH / 2) - (temp_width/2), location))


    @property
    def selection(self):
        return self.option_tracker % len(self.options_list)

        
