from random import choice, randint


class TypingTutor:

    def __init__(self, gametools, starting_level=0):
        """

        self.alphabet: list, letters to be tested, in order.
        
        self.list_word_prompts: list, words to be tested.
        
        self.letters_correct: list, int between 0 and self.max_correct.

        self.max_correct: int, maximum number of times letter must be
                          answered corectly to advance a level.

        self.game_state: string; introduction, test_leter, test_word,
                                 or announcement.

        self.level: int, the current player's level.

        self.zero_level_letters: int, the number of letters to be
                                 tested when the level is zero.

        self.letters_in_play: string, the letters currently being
                              tested.

        self.letter_prompt: string, the current single-letter
                             prompt.
        
        self.previous_prompt: string, the previous single-letter
                               prompt.

        self.key_was_pressed: boolean, True if a key was pressed
                               on this iteration.        

        self.input_letter: string, the letter most recently typed.

        self.total_attempted_letters_answered: int, total number of attempted
                                     answers.
                                     
        self.letters_answered_correctly: int, number of attempts that were
                              successful.

        self.letter_streak: int, length of most recent series of
                            all-correct letter answers.

        self.career_streak: int, longest streak of this game.
        
        self.letter_attempts_before_word: int, tallies answered letters;
                                          helps switch to word if above some #.
                                          
        self.letter_attempts_before_hint: int, tallies incorrect responses;
                                          gives hint if above some #.
                                          
        self.total_words_answered: int, total number of words answered.
        
        self.words_answered_correctly: int, number of words answered
                                       correctly.
                                       
        self.word_streak: int, length of most recent series of all-correct
                           word answers.

        self.word_string: string, the concatenated player input when
                          answering a word.
                          
        self.word_prompt: string, the word to be answered.

        self.intro_done: boolean, has the introduction sound been played?
                
        """

#---META-GAME STUFF---

        self.pygame = gametools['pygame']
        self.sounds = gametools['sounds']
        self.np = gametools['numpy']
        self.gameDisplay = gametools['display']

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.bg = self.pygame.image.load("English_braille_sample.jpg")
        self.pygame.display.set_caption('Typing Tutor')

        self.braille_keyboard = gametools['keyboard'].keyboard() # do I need to instantiate?  Or can't I just pass the previous one?
        self.braille_keyboard.test_coms()    # automatically finds keyboard
                
        self.font = self.pygame.font.SysFont(None, 80)
        self.font_small = self.pygame.font.SysFont(None, 40)
        
        self.white, self.black, self.red, self.blue = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255)
        self.gray1, self.gray2 = (160, 160, 160), (80, 80, 80)
        self.light_blue, self.yellow = (0, 100, 255), (0, 255, 255)

#---GAME VARIABLES---

        self.alphabet = 'etaoinshrdlcumwfgypbvkjxqzX'

        self.list_word_prompts = [["tea","eat", "at", "ate", "tee", "tata", ],
                                  ["tie", "it", "at"],
                                  ["tine", "tint", "net", "ten", "ant", "tan", ],
                                  ["stint", "stone", "notes", "nest"]]
        
        self.letters_correct = self.np.ones(len(self.alphabet))

        self.game_state = 'introduction'
        self.level = starting_level
        self.max_correct = 6

        self.zero_level_letters = 3

        self.letters_in_play = ""
        self.letter_prompt = None
        self.previous_prompt = None

        self.key_was_pressed = False
        
        self.input_letter = None

        self.total_attempted_letters_answered = 0
        self.letters_answered_correctly = 0
        
        self.letter_streak = 0
        self.career_streak = 0
        
        self.letter_attempts_before_word = 0
        self.letter_attempts_before_hint = 0

        self.total_words_answered = 0
        self.words_answered_correctly = 0
        self.word_streak = 0

        self.word_string = ""
        self.word_prompt = ""

        self.intro_done = False


#---SOUNDS---
        
        self.alpha = self.sounds.sounds('alphabet')
        
        self.alpha.sound_dict[' '] = {'sound':self.pygame.mixer.Sound('alphabet/space.wav'),
                                     'length':int(self.pygame.mixer.Sound('alphabet/space.wav').get_length() * 1000)}
        
        self.sfx = self.sounds.sounds('sfx')
        self.correct = self.sounds.sounds('correct')
        self.voice = self.sounds.sounds('voice')


#---CENTRAL FUNCTIONS---


    def iterate(self, input_letter=None, key_was_pressed=None):
        """ A single iteration of the game loop.
        """

        self.reset_variables()

        self.input_letter = input_letter
        self.key_was_pressed = key_was_pressed

        if self.input_letter != None:
            self.play_sfx('type')
        
        self.gameDisplay.blit(self.bg, (0,0))
            
        if self.game_state == "introduction":
            self.introduction()

        elif self.game_state == "testing letter":
            self.test_letter()

        elif self.game_state == "testing word":
            self.test_word()

        self.pygame.display.update()


    def introduction(self):
        """ Plays instructions and waits for space-bar
            to be pressed.
        """
        
        if self.intro_done == False:
            self.play_voice('press_spacebar')
            self.intro_done = True
        else:
            if self.input_letter == 'space':
                self.switch_to_letter()

        self.display_word_prompt('Press Space')
        self.draw_buttons()


    def test_letter(self):
        """ Test users on a letter prompt.
        """
        
        if self.input_letter != None:
            if self.input_letter == self.letter_prompt:
                self.letter_is_correct()
            else:
                self.letter_is_wrong()

        self.display_letter_prompt()
        self.draw_buttons()
        self.display_status_box()


    def test_word(self):
        """ Test user on a word prompt.
        """
        
        if self.input_letter != None and self.input_letter != 'space':
            self.word_string += self.input_letter
        elif self.input_letter == 'space' or len(self.word_string) > len(self.word_prompt):
            if self.word_string == self.word_prompt:
                self.word_is_correct()
            else:
                self.word_is_wrong()

        self.display_word_prompt()
        self.draw_buttons()
        self.display_status_box()


#---OTHER FUNCTIONS---


    def letter_is_correct(self):
        """ Update variables for a correclty-answered letter,
            play response sound, and call for a new letter prompt.
        """
        
        self.total_attempted_letters_answered += 1
        self.letters_answered_correctly += 1
        self.letter_streak += 1
        
        if self.letter_streak > self.career_streak:
            self.career_streak = self.letter_streak
            
        self.letter_attempts_before_hint = 0
        self.letter_attempts_before_word += 1
        
        self.update_letter_tracking(True)
        self.check_level()

        if self.letter_streak % 5 == 0:
            self.play_streak_sound()
        else:
            self.play_correct('correct')

        if self.letter_attempts_before_word > 3:
            self.gamble_switch_to_word()
        else:
            self.get_new_letter()


    def letter_is_wrong(self):
        """ Update variables for an incorrectly-answered letter,
            play response sound, and possibly give a hint.
        """
        
        self.total_attempted_letters_answered += 1
        self.letter_streak = 0
        self.letter_attempts_before_hint += 1

        if self.letter_attempts_before_hint > 2:
            self.give_hint()
        
        self.update_letter_tracking(False)
        self.play_sfx('wrong')


    def word_is_correct(self):
        """ Update variables for a correctly-answered word,
            play response sound, and switch to testing letter.
        """
        self.total_words_answered += 1
        self.words_answered_correctly += 1
        self.play_voice('nice_work', wait=True)
        self.switch_to_letter()


    def word_is_wrong(self):
        """ Update variables for an incorrectly-answered word,
            play response sound, and switch to testing letter.
        """
        self.total_words_answered += 1
        self.play_sfx('wrong')
        self.switch_to_letter()


    def update_letter_tracking(self, correct):
        """ If the correct letter was typed, increment that letter's value
            in the list of letters_correct.  Decrement if incorrect.
        """
        
        temp_index = self.alphabet.index(self.input_letter)
        
        if correct:
            self.letters_correct[temp_index] += 1
            if self.letters_correct[temp_index] > self.max_correct:
                self.letters_correct[temp_index] = self.max_correct
        else:
            self.letters_correct[temp_index] -= 1
            if self.letters_correct[temp_index] < 0:
                self.letters_correct[temp_index] = 0
                

    def give_hint(self):
        """ Play response sound, show correct buttons.
            Vibrate the correct keys for the letter prompt.  
        """
        
        self.draw_buttons(self.braille_keyboard.letter_to_chord[self.letter_prompt])
        self.play_voice('oops_hint', wait=True)
        self.braille_keyboard.vibrate_letter(self.letter_prompt)


    def gamble_switch_to_word(self):
        """ Roll dice to see if a word should be tested now.
        """
        
        tossup = randint(0, 4)
        
        if tossup == 0:
            self.game_state = "testing_word"
            self.switch_to_word()
            return(True)
        else:
            self.get_new_letter()


    def switch_to_word(self):
        """ Get a word prompt and test it.
        """
        self.letter_prompt = None
        self.get_new_word_prompt()
        self.game_state = "testing word"
        self.play_voice('try_a_word')


    def switch_to_letter(self):
        """ Get a letter prompt and test it.
        """
        
        self.word_prompt = ""
        self.word_string = ""
        self.get_new_letter()
        self.game_state = "testing letter"

        
    def get_new_letter(self):
        """ Set the letter_prompt to a letter that's currently
            in play and not the previous letter_prompt.
        """

        self.letters_in_play = self.alphabet[:(self.zero_level_letters + self.level)]
        self.letter_prompt = choice(self.letters_in_play)

        while(self.letter_prompt == self.previous_prompt):
            self.letter_prompt = choice(self.letters_in_play)
            
        self.previous_prompt = self.letter_prompt

        self.play_alpha(self.letter_prompt)


    def get_new_word_prompt(self):
        """ Randomly select a new word from the list of possible
            words available at the current level.
        """
        
        self.word_prompt = choice(self.list_word_prompts[self.level])


    def check_level(self):
        """ Check if all letters have received enough correct responses
            to increment the level.  If so, increment the level.
        """
        
        temp_flag = True
        
        for i in range(len(self.letters_in_play)):
            if self.letters_correct[i] < self.max_correct:
                temp_flag = False

        if temp_flag:
            self.play_sfx('level_up')
            self.play_voice('nice_work')
            self.level += 1
            print("Level up!")

        print(self.letters_correct[:len(self.letters_in_play)])
            

    def reset_variables(self):
        """ Reset all variables.
        """
        
        self.key_was_pressed = False
        self.input_letter = None


    @property
    def score(self):
        """ Returns the score, a calculation based on
            several variables.
        """
        return self.letters_answered_correctly


#---SOUND FUNCTIONS---

    def play_streak_sound(self):
        pass
    

    def play_alpha(self, sound, wait=False):
        self.alpha.sound_dict[sound]['sound'].play()
        if wait:
            self.pygame.time.wait(self.alpha.sound_dict[sound]['length'])


    def play_sfx(self, sound, wait=False):
        self.sfx.sound_dict[sound]['sound'].play()
        if wait:
            self.pygame.time.wait(self.sfx.sound_dict[sound]['length'])


    def play_correct(self, sound, wait=False):
        self.correct.sound_dict[sound]['sound'].play()
        if wait:
            self.pygame.time.wait(self.correct.sound_dict[sound]['length'])


    def play_voice(self, sound, wait=False):
        self.voice.sound_dict[sound]['sound'].play()
        if wait:
            self.pygame.time.wait(self.voice.sound_dict[sound]['length'])


#---DISPLAY FUNCTIONS---

    def display_letter_prompt(self, letter=None):
        """ Write the current letter prompt to the screen.
        """
        if letter == None:
            letter = self.letter_prompt
        displaybox = self.pygame.draw.rect(self.gameDisplay, self.gray1, ((self.SCREEN_WIDTH/2)-200, 108, 400, 50))
        text = self.font.render(letter, True, self.black)
        temp_width = text.get_rect().width
        self.gameDisplay.blit(text, ((self.SCREEN_WIDTH / 2) - (temp_width/2), 100))


    def display_word_prompt(self, word=None):
        """ Write the current word prompt to the screen.
        """

        if word == None:
            word = self.word_prompt
        displaybox = self.pygame.draw.rect(self.gameDisplay, self.gray1, ((self.SCREEN_WIDTH/2)-200, 108, 400, 50))
        text = self.font.render(word, True, self.black)
        temp_width = text.get_rect().width
        self.gameDisplay.blit(text, ((self.SCREEN_WIDTH / 2) - (temp_width/2), 100))


    def display_status_box(self):
        """ Write the current word prompt to the screen.
        """
        
        text = self.font_small.render("Level: " + str(self.level), True, self.black, self.gray1)
        text2 = self.font_small.render("Points: " + str(self.score), True, self.black, self.gray1)
        temp_width = text.get_rect().width
        self.gameDisplay.blit(text, ((self.SCREEN_WIDTH / 10) - (temp_width/2), 10))
        self.gameDisplay.blit(text2, ((self.SCREEN_WIDTH / 10) - (temp_width/2), 45))


    def draw_buttons(self, keys='000000'):
        """ Draw all six buttons to the screen.
            Color depends on input code.
        """
        
        for i in range(len(keys)):
            if keys[i] == '1':
                color = self.light_blue
            elif keys[i] == '0':
                color = self.gray2
                
            if i > 2:
                xpos = (50 + 40 + (i*110))
            else:
                xpos = (50 + (i*110))

            position = (xpos, 300, 100, 150) 
            self.draw_single_button(self.black, position)
            position_small = (xpos+20, 320, 60, 110)
            self.draw_single_button(color, position_small)

    
    def draw_single_button(self, color, position):
        """ Draw a single button to the screen.
        """
        
        self.pygame.draw.ellipse(self.gameDisplay, color, position)
