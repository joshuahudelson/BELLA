from random import choice, randint

class Etudes:
    """ A game in which the user is prompted to press vibrating
        keys.
    """

    def __init__(self, gametools, starting_level=0):
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
        self.alphabet = 'aeickbdfhjlmousgnprtvwxzqy'
        
        self.letters_in_play = ''
        self.levels = [5, 14, 23, 25]
        self.current_level = 0
        
        self.current_prompt = ''
        
        self.responses_correct = self.np.ones(26)
        self.max_correct = 6

        self.total_attempted_responses = 0
        self.num_correct_responses = 0
        self.response_streak = 0

        self.prompt_vibrated = False

#---SOUNDS---

        self.alpha = self.sounds.sounds('alphabet', self.pygame)
        
        self.alpha.sound_dict[' '] = {'sound':self.pygame.mixer.Sound('alphabet/space.wav'),
                                     'length':int(self.pygame.mixer.Sound('alphabet/space.wav').get_length() * 1000)
                                     }
        
        self.sfx = self.sounds.sounds('sfx', self.pygame)
        self.correct = self.sounds.sounds('correct', self.pygame)
        self.voice = self.sounds.sounds('voice', self.pygame)


#---CENTRAL FUNCTIONS---

    def iterate(self, input_letter):
        """ One iteration of the game loop.
            Receives input and calls appropriate
            function depending on the state of the
            game.
        """

        self.gameDisplay.blit(self.bg, (0,0))
        self.current_input = input_letter
        self.display_status_box()

        if self.game_state == 'introduction':
            self.introduction()
        elif self.game_state == 'play_game':
            self.play_game()

        self.display_chord()
        self.pygame.display.update()


    def introduction(self):
        """ The introduction screen of the game.
            Waits for space bar to begin prompting.
        """
        
        self.display_message('Press Space')
        if self.current_input == 'space':
            self.game_state = 'play_game'
            self.get_new_prompt()


    def play_game(self):
        """ The main game-play function.
            Vibrates the prompted character,
            tests whether the player's input
            is correct or not, and then calls
            the appropriate update function.
        """
        
        self.display_letter_prompt()

        if self.prompt_vibrated == False:
            self.vibrate_buttons()
            self.prompt_vibrated = True
        
        if self.current_input != None:
            if self.current_input == self.current_prompt:
                self.correct_response()
            else:
                self.incorrect_response()
                

    def correct_response(self):
        """ If the response is correct, update
            the game variables accordingly and
            get a new prompt.
        """
        
        self.play_correct('correct')
        self.update_points(True)
        self.check_level()
        self.get_new_prompt()


    def incorrect_response(self):
        """ If the response is incorrect, update
            the game variables accordingly and vibrate
            the current prompt again.
        """
        
        self.play_sfx('wrong')
        self.update_points(False)
        self.vibrate_buttons()


    def update_points(self, correct):
        """ Increment or decrement the value in the list that
            tracks responses per character.  Can't decrement
            past 0 nor increment past self.max_correct.
        """
        
        alpha_loc = self.alphabet.index(self.current_prompt)
        
        if correct:
            self.responses_correct[alpha_loc] += 1
            if self.responses_correct[alpha_loc] > self.max_correct:
                self.responses_correct[alpha_loc] = self.max_correct
        else:
            self.responses_correct[alpha_loc] -= 1
            if self.responses_correct[alpha_loc] < 0:
                self.responses_correct[alpha_loc] = 0
                
        print(self.responses_correct[:len(self.letters_in_play)])


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
            if self.current_level > len(self.levels)-1:
                self.current_level = len(self.levels)-1
                self.letters_in_play = self.alphabet[:self.levels[self.current_level]]
                print("Level up")


    def get_new_prompt(self):
        """ Choose a new prompt from the list of letters in
            play, unless it's the one that has just been prompted.
        """
        
        previous_prompt = self.current_prompt
        
        while(previous_prompt == self.current_prompt):
            self.current_prompt = choice(self.letters_in_play)

        self.prompt_vibrated = False


    def vibrate_buttons(self):
        """ Vibrate the buttons that correspond to the current prompt.
        """
        
        self.braille_keyboard.vibrate_letter(self.current_prompt, sim=True)


#---SOUND FUNCTIONS---
        
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


#---DISPLAY FUNCTIONS---

    def display_letter_prompt(self):
        """ Write the current letter prompt to the screen.
        """

        text = self.font.render(self.current_prompt, True, self.black)
        temp_width = text.get_rect().width
        self.pygame.draw.rect(self.gameDisplay, self.gray1, ((self.SCREEN_WIDTH / 2) - 100, 102, 200, 55))
        self.gameDisplay.blit(text, ((self.SCREEN_WIDTH / 2) - (temp_width / 2), 100))


    def display_message(self, message):
        """ Write the current word prompt to the screen.
        """
        displaybox = self.pygame.draw.rect(self.gameDisplay, self.gray1, ((self.SCREEN_WIDTH/2)-200, 108, 400, 50))
        text = self.font.render(message, True, self.black)
        temp_width = text.get_rect().width
        self.gameDisplay.blit(text, ((self.SCREEN_WIDTH / 2) - (temp_width/2), 100))


    def display_status_box(self):
        """ Write the current word prompt to the screen.
        """
        
        text = self.font_small.render("Level: " + str(self.current_level), True, self.black, self.gray1)
        temp_width = text.get_rect().width
        self.gameDisplay.blit(text, ((self.SCREEN_WIDTH / 10) - (temp_width/2), 10))


    def draw_single_button(self, color, position):
        """ Draw a single button to the screen.
        """

        self.pygame.draw.ellipse(self.gameDisplay, color, position)


    def display_chord(self):
        """ Draw the keys to the screen
        """

        key_order = [3, 4, 5, 2, 1, 0]

        current_chord = self.braille_keyboard.letter_to_chord[self.current_prompt]

        for i in range(len(current_chord)):
            if current_chord[key_order[i]] == '1':
                color = self.light_blue
            elif current_chord[key_order[i]] == '0':
                color = self.gray2
    
            if i > 2:
                xpos = (50 + 40 + (i*110))
            else:
                xpos = (50 + (i*110))
                
            position = (xpos, 300, 100, 150) 
            self.draw_single_button(self.black, position)
            position_small = (xpos+20, 320, 60, 110)
            self.draw_single_button(color, position_small)
