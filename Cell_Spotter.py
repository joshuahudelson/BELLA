from random import choice, randint

class Cell_Spotter:
    """ A game that prompts a player with a letter, and
        the player finds that letter on the card and presses
        the cursor key above it.
    """

    def __init__(self, gametools, display_data, starting_level=0):
        """
        """


#---META-GAME STUFF---

        self.pygame = gametools['pygame']
        self.sounds = gametools['sounds']
        self.np = gametools['numpy']
        self.gameDisplay = gametools['display']
        self.braille_keyboard = gametools['keyboard']

        self.sound_object = self.sounds.sounds()


#---DISPLAY---
        
        self.SCREEN_WIDTH = display_data['screen_width']
        self.SCREEN_HEIGHT = display_data['screen_height']

        self.pygame.display.set_caption('Cell Spotter')
   
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


#---CENTRAL FUNCTIONS---

    def iterate(self, input_dict):
        
        self.gameDisplay.fill(self.display_states[self.display_names[self.current_display_state]]['background'])

        self.current_input = input_dict['cursor_key']
        self.current_control = input_dict['standard']

        if self.current_control == 'display':
            self.change_display_state()

        if self.game_state == 'introduction':
            self.introduction(input_dict)
        elif self.game_state == 'game_play':
            self.game_play()
         
        self.pygame.display.update()


    def introduction(self, input_dict):

        if input_dict['card_state']:
            self.card_str = input_dict['card_str']
            self.game_state = 'game_play'
            self.get_search_letters()
            self.search_letter_num = 0
            self.current_prompt = self.search_list[self.search_letter_num]
            self.get_search_positions(self.current_prompt)
        elif self.intro_played == False:
            self.play_sound('insert_a_card', self.standard_voice)
            self.intro_played = True

        self.display_word_prompt()


    def game_play(self):
        if self.current_input != None:
            if (self.current_input in self.hidden_pos):
                self.correct_choice()
            else:
                if(self.current_input in self.found_pos):
                    self.play_sound('double', self.standard_sfx)
                    self.play_sound('already_found', self.standard_voice) 
                else:
                    self.play_sound('wrong', self.standard_sfx)

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
        
        self.play_sound('find_all_the', self.standard_voice, True)
        self.play_sound(self.current_prompt, self.standard_alphabet, True)
        self.play_sound('_s', self.standard_voice, True)


    def correct_choice(self):
        self.hidden_pos.remove(self.current_input)
        self.found_pos.append(self.current_input)
        if len(self.hidden_pos)<= 0:            
            self.search_letter_num +=1
            if self.search_letter_num >= len(self.search_list):  # you finished searching the whole card
                self.play_sound('win', self.standard_sfx)
                self.play_sound('great_job', self.standard_voice, wait=True)
                self.game_state = 'introduction'
                self.card_inserted = False
                self.intro_played = False
            else:
                print("yay you found them all")
                self.play_sound('level_up', self.standard_sfx)
                self.play_sound('nice_work', self.standard_voice, wait=True)
                self.current_prompt = self.search_list[self.search_letter_num]
                self.get_search_positions(self.current_prompt)
        else:
            self.play_sound('correct', self.standard_sfx)
                

#---SOUND FUNCTIONS---
    
    def play_sound(self, sound, dictionary, wait=False):
        dictionary[sound]['sound'].play()
        if wait:
            self.pygame.time.wait(dictionary[sound]['length'])



#---DISPLAY FUNCTIONS---

    def change_display_state(self):
        self.current_display_state = (self.current_display_state + 1) % len(self.display_names)


    def display_letter_prompt(self, letter=None):
        """ Write the current letter prompt to the screen.
        """
        if letter == None:
            letter = self.current_prompt
            
        displaybox = self.pygame.draw.rect(self.gameDisplay,
                                           self.display_states[self.display_names[self.current_display_state]]['background'],
                                           ((self.SCREEN_WIDTH/2)-200, 108, 400, 50))

        text = self.font_large.render(letter, True,
                                      self.display_states[self.display_names[self.current_display_state]]['text'])

        temp_width = text.get_rect().width

        self.gameDisplay.blit(text, ((self.SCREEN_WIDTH / 2) - (temp_width/2), 100))


    def display_word_prompt(self, word=None):
        """ Write the current word prompt to the screen.
        """

        if word == None:
            word = self.word_prompt
        displaybox = self.pygame.draw.rect(self.gameDisplay, self.display_states[self.display_names[self.current_display_state]]['background'], ((self.SCREEN_WIDTH/2)-200, 108, 400, 50))
        text = self.font.render(word, True, self.display_states[self.display_names[self.current_display_state]]['text'])
        temp_width = text.get_rect().width
        self.gameDisplay.blit(text, ((self.SCREEN_WIDTH / 2) - (temp_width/2), 100))


