from random import choice, randint


class TypingTutor:

    def __init__(self, gametools, starting_level=0):
        """

            self.braille_keyboard: object that handles serial
                IO with the physical keyboard
                
            self.alphabet: list of letters to be tested on,
                in order of english-language frequency.

            self.letters_wrong/right: list keeping track of
                how many times player got that letter wrong
                and right.  Can't be wrong more than five
                times.

            self.ratios: list of ratios of self.letters_wrong/right
                for each letter.  Must be above some amount
                for player to advance to next level.

            self.game_state: string keeping track of whether
                game is in introduction, testing a letter, or
                testing a word.

            self.level: the current level the play is at.

            self.letters_in_play: list of the letters being
                tested.  Determined by self.level.

            self.letter_prompt: the current letter being tested.

            self.previous_prompt: the prompt from the previous attempt;
                used to rule out the possibility of testing the same
                letter twice in a row.

            self.game_in_play: boolean, keeps the object's game loop
                running.

            self.key_was_pressed: boolean, if key is pressed, cause
                delay at the end of the function so that player has
                time to see the response.

            self.attempts: int, how many times the player has attempted
                to respond to a single prompt.

            self.score: int, not sure yet how it will be computed.

            self.input_letter: string, the letter the player has
                pressed on the keyboard.

            self.number_prompts_answered: int, after a certain
                number of prompts, game switches once to prompting
                a full word

            self.number_words_correct: int, number of word-prompts
                answered correctly

            self.response: string that gets posted to screen after
                player responds to a prompt.

            self.list_word_prompts: a list of lists of words to
                test per level.

                
        """

#---META-GAME STUFF---

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600

        self.braille_keyboard = gametools['keyboard'].keyboard() # do I need to instantiate?  Or can't I just pass the previous one?
        self.braille_keyboard.test_coms()    # automatically finds keyboard

        self.pygame = gametools['pygame']
        self.sounds = gametools['sounds']
        self.np = gametools['numpy']
        self.gameDisplay = gametools['display']
                
        self.font = self.pygame.font.SysFont(None, 80)
        self.font_small = self.pygame.font.SysFont(None, 40)
        self.bg = self.pygame.image.load("English_braille_sample.jpg")
        self.pygame.display.set_caption('Typing Tutor')
        self.white, self.black, self.red, self.blue = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255)
        self.gray1, self.gray2 = (160, 160, 160), (80, 80, 80)
        self.light_blue, self.yellow = (0, 100, 255), (0, 255, 255)

#---GAME VARIABLES---

        self.alphabet = 'etaoinshrdlcumwfgypbvkjxqzX'
        self.letters_correct = self.np.ones(len(self.alphabet))

        self.game_state = 'introduction'
        self.level = starting_level
        self.max_right = 6

        self.zero_level_letters = 3

        self.letters_in_play = ""
        self.letter_prompt = None
        self.previous_prompt = None

        self.game_in_play = True

        self.key_was_pressed = False
        self.time_to_wait = 0
        

        self.input_letter = None

        self.attempts_for_this_letter = 0

        self.total_letters_answered = 0
        self.letters_answered_correctly = 0
        self.letter_streak = 0
        self.letter_attempts_before_word = 0
        self.letter_attempts_before_hint = 0

        self.total_words_answered = 0
        self.words_answered_correctly = 0
        self.word_streak = 0

        self.score = 0  # make this a property


        self.response = 'OOOOOO'

        self.word_string = ""
        self.word_prompt = ""

        self.intro_done = False

        self.streak = 0
        self.career_points = 0

        self.list_word_prompts = [["tea","eat", "at", "ate", "tee", "tata", ],
                                  ["tie", "it", "at"],
                                  ["tine", "tint", "net", "ten", "ant", "tan", ],
                                  ["stint", "stone", "notes", "nest"]]

#---SOUNDS---
        
        self.alpha = self.sounds.sounds('alphabet')
        
        self.alpha.sound_dict[' '] = {'sound':self.pygame.mixer.Sound('alphabet/space.wav'),
                                     'length':int(self.pygame.mixer.Sound('alphabet/space.wav').get_length() * 1000)}
        
        self.sfx = self.sounds.sounds('sfx')
        self.correct = self.sounds.sounds('correct')
        self.voice = self.sounds.sounds('voice')


#---MAJOR FUNCTIONS---


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

        self.pygame.time.wait(self.time_to_wait)


    def introduction(self):
        """ Under construction: add introductory speech,
            music, and instructions.
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
        """ Decision tree for testing a letter.
        """
        
        if self.input_letter != None:
            if self.input_letter == self.letter_prompt:
                self.letter_is_correct()
            else:
                self.letter_is_wrong()

        self.display_letter_prompt()
        self.draw_buttons()
        self.display_status_box()


    def letter_is_correct(self):
        self.total_letters_answered += 1
        self.letters_answered_correctly += 1
        self.letter_streak += 1
        self.letter_attempts_before_hint = 0
        self.letter_attempts_before_word += 1
        
        self.update_letter_tracking(True)
        self.check_level()

        if self.streak % 5 == 0:
            self.play_streak_sound()
        else:
            self.play_correct('correct')

        if self.letter_attempts_before_word > 3:
            self.gamble_switch_to_word()
        else:
            self.get_new_letter()


    def letter_is_wrong(self):
        self.total_letters_answered += 1
        self.letter_streak = 0
        self.letter_attempts_before_hint += 1

        if self.letter_attempts_before_hint > 2:
            self.give_hint()
        
        self.update_letter_tracking(False)
        self.play_sfx('wrong')


    def test_word(self):
        """ Decision tree for testing a word.
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
        

    def word_is_correct(self):
        self.total_words_answered += 1
        self.words_answered_correctly += 1
        self.play_voice('nice_work', wait=True)
        self.switch_to_letter()


    def word_is_wrong(self):
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
            if self.letters_correct[temp_index] > self.max_right:
                self.letters_correct[temp_index] = self.max_right
        else:
            self.letters_correct[temp_index] -= 1
            if self.letters_correct[temp_index] < 0:
                self.letters_correct[temp_index] = 0
                

    def give_hint(self):
        """
        """
        print(self.braille_keyboard.letter_to_chord[self.letter_prompt])
        '''
        self.draw_buttons(self.braille_keyboard.letter_to_chord[self.letter_prompt])
        self.play_voice('oops_hint', wait=True)
        self.braille_keyboard.vibrate_letter(self.letter_prompt)
        '''


    def gamble_switch_to_word(self):
        """ There is a 25 percent chance to test a word next.
        """
        tossup = randint(0, 3)
        
        if tossup == 3:
            self.game_state = "testing_word"
            self.switch_to_word()
            return(True)
        else:
            self.get_new_letter()


    def switch_to_word(self):
        """ Switch the current prompt to a word.
        """
        self.play_voice('try_a_word')
        self.letter_prompt = None
        self.get_new_word_prompt()
        self.number_prompts_answered = 0
        self.game_state = "testing word"
        

    def switch_to_letter(self):
        """ Switch the current prompt to a letter.
        """
        
        self.word_prompt = ""
        self.word_string = ""
        self.get_new_letter()
        self.game_state = "testing letter"

        
    def get_new_letter(self):
        """ Set the letter_prompt to a letter that's currently in play and not
            the previous letter_prompt.
        """

        self.letters_in_play = self.alphabet[:(self.zero_level_letters + self.level)]
        self.letter_prompt = choice(self.letters_in_play)

        while(self.letter_prompt == self.previous_prompt):
            self.letter_prompt = choice(self.letters_in_play)
            
        self.previous_prompt = self.letter_prompt

        self.play_alpha(self.letter_prompt)


    def get_new_word_prompt(self):
        """ Randomly select a new word from the list of possible words at the current
            level.
        """
        
        self.word_prompt = choice(self.list_word_prompts[self.level])


    def check_level(self):
        """ Check if all letters have received enough correct responses
            to increment the level.  If so, increment the level.
        """
        
        temp_flag = True
        
        for i in range(len(self.letters_in_play)):
            if self.letters_correct[i] < self.max_right:
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
        self.response = 'OOOOOO'
        self.time_to_wait = 0


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
        text2 = self.font_small.render("Points: " + str(self.career_points), True, self.black, self.gray1)
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
