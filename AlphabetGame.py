
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

#---SOUND---
        
        self.alpha = self.sounds.sounds('alphabet', self.pygame) #creates self.alpha.sound_dict dictionary
        self.alpha.sound_dict[' '] = {'sound':self.pygame.mixer.Sound('alphabet/space.wav'),
                                     'length':int(self.pygame.mixer.Sound('alphabet/space.wav').get_length() * 1000)
                                     }

        self.sfx = self.sounds.sounds('sfx', self.pygame)
        self.correct = self.sounds.sounds('correct', self.pygame)
        self.voice = self.sounds.sounds('voice', self.pygame)

        self.alphabet_sounds = self.sounds.sounds('alphabet_sounds', self.pygame)
        

    def iterate(self, cursor_button):

        self.gameDisplay.blit(self.bg, (0,0))

        self.timer += 1

        if int(self.timer/float(self.fps)) > self.number_of_seconds_to_wait:
            if self.num_prompts < self.max_num_prompts:
                print('reminder!')
#                self.play_instruction[self.press_counter]

        if self.game_state == 'introduction':
            self.introduction()
        elif self.game_state == 'game_play':
                self.game_play(cursor_button)

        print(self.timer)

        self.pygame.display.update()


    def introduction(self):
        if self.intro_played == False:
            self.play_voice('insert_card')
            self.intro_played = True
        else:
            if self.braille_keyboard.last_button_state == '11111111111111111111111111111111':
                self.braille_keyboard.request_card()
                self.card_str = self.braille_keyboard.card_str
                self.play_sfx('insert',wait=True) # we need to rename this sound effect.  Just call it beep.
                self.game_state = 'game_play'


    def game_play(self, cursor_button):

        if cursor_button != None:

            if self.current_cursor_button != cursor_button:
                self.current_cursor_button = cursor_button
                self.press_counter = 0

            character = self.card_str[self.current_cursor_button]
            
            if character != ' ':
                self.play_sfx('wrong')
            else:
                self.alphabet_sounds(character + str(self.press_counter))
                self.press_counter += 1
            
            

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

   
    def display_letter_prompt(self):
        """ Write the current letter prompt to the screen.
        """

        text = self.font.render(self.current_prompt, True, self.black)
        temp_width = text.get_rect().width
        self.pygame.draw.rect(self.gameDisplay, self.gray1, ((self.SCREEN_WIDTH / 2) - 100, 102, 200, 55))
        self.gameDisplay.blit(text, ((self.SCREEN_WIDTH / 2) - (temp_width / 2), 100))


    def display_word_prompt(self):
        """ Write the current word prompt to the screen.
        """
        displaybox = self.pygame.draw.rect(self.gameDisplay, self.gray1, ((self.SCREEN_WIDTH/2)-200, 108, 400, 50))
        text = self.font.render(self.word_prompt, True, self.black)
        temp_width = text.get_rect().width
        self.gameDisplay.blit(text, ((self.SCREEN_WIDTH / 2) - (temp_width/2), 100))


