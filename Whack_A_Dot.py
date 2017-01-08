from random import choice, randint

class Whack_A_Dot:
    """ A game in which the user is prompted to press vibrating
        keys.
    """

    def __init__(self, gametools, display_data, starting_level=0):
        """

            self.game_state: string, what part of the game is currently running

            self.alphabet: string, the characters--in order--that will be added
                           to the set of possible prompts as the player advances
                           levels.

            self.letters_in_play: string, the current set of characters being
                                  prompted.

            self.levels: list, the substring from self.alphabet that should be
                         used as self.letters_in_play for each level (the index
                         of self.levels).

            self.current_level: int, the player's current level.

            self.current_prompt: string, the character being prompted now.

            self.responses_correct: list, a tally for each letter of self.alphabet
                                    of how many times it has been answered correctly.

            self.max_correct: int, the number of correct responses required for each
                              letter within a level before the player can advance to
                              the next level.

            self.total_attempted_responses: int, the total number of player responses
                                            whether correct or not.

            self.num_correct_responses: int, the number of player responses that have been
                                        correct so far.

            self.response_streak: int, number of correct responses given since the most
                                  recent incorrect response (or beginning of the game).

            self.prompt_vibrated: boolean, whether self.current_prompt has vibrated the
                                  keys yet.

        """

#---META-GAME STUFF---

        self.pygame = gametools['pygame']
        self.sounds = gametools['sounds']
        self.np = gametools['numpy']
        self.gameDisplay = gametools['display']
        self.braille_keyboard = gametools['keyboard']

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600

        self.pygame.display.set_caption('Whack-A-Dot')

        self.sound_object = self.sounds.sounds()
        self.game_name = 'Whack_A_Dot'

        self.delay = gametools['serial_delay_factor']
        self.fps = gametools['fps']


#---DISPLAY---
        
        self.SCREEN_WIDTH = display_data['screen_width']
        self.SCREEN_HEIGHT = display_data['screen_height']

        self.pygame.display.set_caption('Etudes')
   
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

        self.game_sounds = self.sound_object.make_sound_dictionary(self.game_name + '_sounds', self.pygame)

        
        self.standard_alphabet[' '] = {'sound':self.pygame.mixer.Sound(self.sounds.join(standard_alphabet_dir, 'space.wav')),
                                     'length':int(self.pygame.mixer.Sound(self.sounds.join(standard_alphabet_dir, 'space.wav')).get_length() * 1000)}


#---GAME VARIABLES---

        self.correct_sfx = ["correct_one","correct_two","correct_three","correct_four","correct_five","correct_six"]
        self.correct_voice = ["fantastic","keep_it_up","good_job","great_job","outstanding"]

        self.game_state = 'introduction'
        self.alphabet = 'aeickbdfhjlmousgnprtvwxzqy'
        
        self.letters_in_play = ''
        self.levels = [10, 28, 46, 50]
        self.current_level = 0
        
        self.current_prompt = '000000'
        
        self.responses_correct = self.np.ones(26)
        self.max_correct = 2

        self.total_attempted_responses = 0
        self.num_correct_responses = 0
        self.response_streak = 0

        self.prompt_vibrated = False

        self.intro_played = False

        self.points = 0

        self.frames_passed = 0

#---CENTRAL FUNCTIONS---

    def iterate(self, input_dict):
        """ One iteration of the game loop.
            Receives input and calls appropriate
            function depending on the state of the
            game.
        """

        self.gameDisplay.fill(self.display_states[self.display_names[self.current_display_state]]['background'])

        self.input_letter = input_dict['chord']

        if self.input_letter == '000000':
            self.input_letter = None
        
        self.input_control = input_dict['standard']

        if self.input_control == 'display':
            self.change_display_state()

        self.display_status_box()

        if self.game_state == 'introduction':
            self.introduction()
        elif self.game_state == 'play_game':
            self.play_game()

        self.draw_buttons(self.current_prompt)

        self.pygame.display.update()


    def introduction(self):
        """ The introduction screen of the game.
            Waits for space bar to begin prompting.
        """
        
        self.display_message('Press Space')

        if self.intro_played:
        
            if self.input_control == 'space':
                self.game_state = 'play_game'
#            self.update_letters_in_play()
                self.get_new_prompt()

        else:
            self.play_sound('press_space_when', self.standard_voice)
            self.intro_played = True


    def play_game(self):
        """ The main game-play function.
            Vibrates the prompted character,
            tests whether the player's input
            is correct or not, and then calls
            the appropriate update function.
        """
        
#        self.display_letter_prompt()

        if self.input_letter != None:
            if self.input_letter == self.current_prompt:
                self.correct_response()
            else:
                self.incorrect_response()

        self.frames_passed += 1

        if self.prompt_vibrated == False:
            self.vibrate_buttons()
            self.prompt_vibrated = True

        if self.frames_passed > (self.delay * self.fps * 0.07):
            self.vibrate_buttons()
            self.frames_passed = 0

        
                

    def correct_response(self):
        """ If the response is correct, update
            the game variables accordingly and
            get a new prompt.
        """
        
        self.play_sound(choice(self.correct_sfx), self.standard_sfx, wait=True)
        self.update_points(True)
#        self.check_level()
        self.get_new_prompt()
        self.frames_passed = 0



    def incorrect_response(self):
        """ If the response is incorrect, update
            the game variables accordingly and vibrate
            the current prompt again.
        """
        
        self.play_sound('wrong', self.standard_sfx, wait=True)
        self.update_points(False)
        #self.vibrate_buttons() # this is a little confusing when we are hinting more often
        self.frames_passed = 0


    def update_points(self, correct):
        """ Increment or decrement the value in the list that
            tracks responses per character.  Can't decrement
            past 0 nor increment past self.max_correct.
        """

        if correct:
            self.points += 10
            
        if self.points > ((self.current_level + 1) * 100):
            self.play_sound('level_up', self.standard_sfx, True)
            self.play_sound(choice(self.correct_voice),self.standard_voice, wait=True)
            self.play_sound('combinations',self.game_sounds, wait=True)
            self.current_level += 1
            print(self.current_level)
            if self.current_level > 4:
                self.current_level = 4
                


    def update_points_deprecated(self, correct):
        """ Increment or decrement the value in the list that
            tracks responses per character.  Can't decrement
            past 0 nor increment past self.max_correct.
        """

        alpha_loc = self.alphabet.index(self.current_prompt, None)
        
        print(alpha_loc)

        if alpha_loc != None:
            
            
            if correct:
                self.responses_correct[alpha_loc] += 1
                if self.responses_correct[alpha_loc] > self.max_correct:
                    self.responses_correct[alpha_loc] = self.max_correct
            else:
                self.responses_correct[alpha_loc] -= 1
                if self.responses_correct[alpha_loc] < 0:
                    self.responses_correct[alpha_loc] = 0
                
            print(self.responses_correct[:self.levels[self.current_level]])


    def check_level(self):
        """ If all values in the list that tracks responses per
            character are equal to self.max_correct, then the
            player advances a level.
        """
        
        temp_flag = True
        
        for i in range(len(self.letters_in_play)):
            if self.responses_correct[i] < self.max_correct:
                levelup_flag = False

        if temp_flag:
            self.current_level += 1
            print("Level up")
            if self.current_level > len(self.levels)-1:
                self.current_level = len(self.levels)-1
                self.update_letters_in_play
                print("Level up")


    def get_new_prompt(self):
        """ Choose a new prompt from the list of letters in
            play, unless it's the one that has just been prompted.
        """
        
        previous_prompt = self.current_prompt
        
        while(previous_prompt == self.current_prompt):
            self.current_prompt = self.generate_chord(self.current_level + 1)

        self.prompt_vibrated = False


    def update_letters_in_play(self):
        
        self.letters_in_play = self.alphabet[:self.levels[self.current_level]]


    def vibrate_buttons(self):
        """ Vibrate the buttons that correspond to the current prompt.
        """
        
        self.braille_keyboard.vibrate_chord(self.current_prompt, sim=True)


    def generate_chord(self, num_keys):
        num_keys = choice(range(num_keys))
        if num_keys > 5:
            num_keys = 5
        if num_keys < 1:
            num_keys = 1

        press_list = []        

        while len(press_list) < num_keys:
            x = randint(0, 5)
            if x not in press_list:
                press_list.append(x)

        chord = ''

        for i in range(6):
            if i in press_list:
                chord += '1'
            else:
                chord += '0'

        return chord


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



    def display_message(self, message):
        """ Write the current word prompt to the screen.
        """
        text = self.font.render(message, True,
                                self.display_states[self.display_names[self.current_display_state]]['text'])
        temp_width = text.get_rect().width
        self.gameDisplay.blit(text, ((self.SCREEN_WIDTH / 2) - (temp_width/2), 100))


    def display_status_box(self):
        """ Write the current word prompt to the screen.
        """
        
        text = self.font_small.render("Level: " + str(self.current_level), True,
                                      self.display_states[self.display_names[self.current_display_state]]['text'],
                                      self.display_states[self.display_names[self.current_display_state]]['background'])
        temp_width = text.get_rect().width
        self.gameDisplay.blit(text, ((self.SCREEN_WIDTH / 10) - (temp_width/2), 10))


    def draw_single_button(self, color, position):
        """ Draw a single button to the screen.
        """

        self.pygame.draw.ellipse(self.gameDisplay, color, position)


    def draw_buttons(self, keys='000000'):
        """ Draw all six buttons to the screen.
            Color depends on input code.
        """
        
        xpos = None
        ypos = 500
        button_width = 60
        button_height = 80
        offset = 7

        x_divisor = self.SCREEN_WIDTH / 6
        x_scalar = 0.8
        x_buffer = (1.0 - x_scalar) * self.SCREEN_WIDTH * 0.5
        x_middle = self.SCREEN_WIDTH * 0.07

        key_order = [3, 4, 5, 2, 1, 0]
        
        for i in range(len(keys)):
            if keys[key_order[i]] == '1':
                color = self.display_states[self.display_names[self.current_display_state]]['text']
            elif keys[key_order[i]] == '0':
                color = self.display_states[self.display_names[self.current_display_state]]['background']
            
            if i > 2:
                xpos = (i* x_divisor * x_scalar) + x_buffer + x_middle
            else:
                xpos = (i* x_divisor * x_scalar) + x_buffer

            position = (xpos, ypos, button_width, button_height)
            position_small = (xpos + offset, ypos + offset, button_width - (2 * offset), button_height - (2 * offset))

            self.draw_single_button(self.display_states[self.display_names[self.current_display_state]]['text'], position)
            self.draw_single_button(color, position_small)


