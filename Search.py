from random import choice, randint

class Search:

    def __init__(self, gametools, starting_level=0):

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


        self.game_state = 'introduction'
        
        self.current_input = None

        self.current_prompt = ''
        
        self.word_prompt = 'insert card'

        self.card_str = '                    '

        self.card_inserted = False

        self.freq_dict = {}

        self.search_list = []

        self.search_letter_num = 0
        
        self.hidden_pos = []

        self.found_pos = []

        self.intro_played = False
        
#---SOUND---
        
        self.alpha = self.sounds.sounds('alphabet', self.pygame) #creates self.alpha.sound_dict dictionary
        self.alpha.sound_dict[' '] = {'sound':self.pygame.mixer.Sound('alphabet/space.wav'),
                                     'length':int(self.pygame.mixer.Sound('alphabet/space.wav').get_length() * 1000)
                                     }

        self.sfx = self.sounds.sounds('sfx', self.pygame)
        self.correct = self.sounds.sounds('correct', self.pygame)
        self.voice = self.sounds.sounds('voice', self.pygame)


#---FUNCTIONS---

    def iterate(self, input_letter):
        
        self.gameDisplay.blit(self.bg, (0,0))

        self.current_input = input_letter

        if self.game_state == 'introduction':
            self.introduction()
        elif self.game_state == 'game_play':
            self.game_play()
         
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
                self.intro_done = True
                self.game_state = 'game_play'
                self.get_search_letters()
                self.search_letter_num = 0
                self.current_prompt = self.search_list[self.search_letter_num]
                self.get_search_positions(self.current_prompt)

        self.display_word_prompt()



    def game_play(self):
        if self.braille_keyboard.last_button != None:
            if (self.braille_keyboard.last_button in self.hidden_pos):
                self.correct_choice()
            else:
                if(self.braille_keyboard.last_button in self.found_pos):
                    self.play_sfx('double')
                    self.play_voice('already_found') 
                else:
                    self.play_sfx('wrong')

        self.display_letter_prompt()  


    def get_search_letters(self):
        """ Makes a histogram of the characters on the card.
            Delete the space entry.
            Turns it into a list sorted by frequency.
        """

        self.freq_dict = {i:self.card_str.count(i) for i in self.card_str} # can this be a temp variable?

        try:
            del self.freq_dict[' ']
        except KeyError:
            pass

        self.search_list = sorted(self.freq_dict,key=self.freq_dict.get)
        print(self.search_list)


    def get_search_positions(self, letter): # Can I just make this compare on the fly?

        self.hidden_pos = [pos for pos,char in enumerate(self.card_str) if char == letter]
        print("letter = {}  positions = {}".format(letter,self.hidden_pos))
        self.found_pos = []
        
        self.play_voice('find_all')
        self.pygame.time.wait(round(self.voice.sound_dict['find_all']['length'] * .9))
        self.play_alpha(self.current_prompt)
        self.pygame.time.wait(round(self.alpha.sound_dict[self.current_prompt]['length'] * .75))
        self.play_voice('_s',wait=True)


    def correct_choice(self):
        self.hidden_pos.remove(self.braille_keyboard.last_button)
        self.found_pos.append(self.braille_keyboard.last_button)
        if len(self.hidden_pos)<= 0:            
            self.search_letter_num +=1
            if self.search_letter_num >= len(self.search_list):  # you finished searching the whole card
                self.play_sfx('win')
                self.play_voice('great_job',wait=True)
                self.game_state = 'introduction'
                self.card_inserted = False
                self.intro_done = False
            else:
                print("yay you found them all")
                self.play_sfx('level_up')
                self.play_voice('nice_work',wait=True)
                self.current_prompt = self.search_list[self.search_letter_num]
                self.get_search_positions(self.current_prompt)
        else:
            self.play_correct('correct')
                

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

