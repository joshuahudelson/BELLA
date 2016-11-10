from random import choice, randint
import numpy as np
import pygame as pg
import time as tempo
import pygame.mixer


class TypingTutor:

    def __init__(self, starting_level=0):
        """
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

            self.current_prompt: the current letter being tested.

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

            self.need_prompt: boolean, if prompt has been answered
                correctly, it causes a new prompt to occur.

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

        self.pygame = pg
        self.pygame.init()
        self.gameDisplay = self.pygame.display.set_mode((800, 600))
        self.clock = self.pygame.time.Clock()
        self.font = self.pygame.font.SysFont(None, 80)

        self.bg = self.pygame.image.load("woodbg.jpg")

        self.pygame.display.set_caption('Typing Tutor')
        self.white, self.black, self.red, self.blue = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255)
        self.light_blue, self.yellow = (0, 100, 255), (0, 255, 255)

        self.alphabet = 'etaoinshrdlcumwfgypbvkjxqz'

        self.letters_right = np.ones(len(self.alphabet))

        self.game_state = 'introduction'
        self.level = starting_level
        self.max_right = 6

        self.zero_level_letters = 3

        self.letters_in_play = ""
        self.current_prompt = None
        self.previous_prompt = None

        self.game_in_play = True

        self.key_was_pressed = False
        self.time_to_wait = 0
        
        self.attempts = 0
        self.score = 0

        self.input_letter = None

        self.number_prompts_answered = 0
        self.number_words_correct = 0

        self.response = 'OOOOOO'

        self.word_string = ""
        self.word_prompt = ""

        self.intro_done = False

        self.letter_to_key_combo = {
            'a':'OOXOOO',
            'b':'OXXOOO',
            'c':'OOXXOO',
            'd':'OOXXXO',
            'e':'OOXOXO',
            'f':'OXXXOO',
            'g':'OXXXXO',
            'h':'OXXOXO',
            'i':'OXOXOO',
            'j':'OXOXXO',
            'k':'XOXOOO',
            'l':'XXXOOO',
            'm':'XOXXOO',
            'n':'XOXXXO',
            'o':'XOXOXO',
            'p':'XXXXOO',
            'q':'XXXXXO',
            'r':'XXXOXO',
            's':'XXOXOO',
            't':'XXOXXO',
            'u':'XOXOOX',
            'v':'XXXOOX',
            'w':'OXOXXX',
            'x':'XOXXOX',
            'y':'XOXXXX',
            'z':'XOXOXX'}

        self.list_word_prompts = [["tea","eat", "at", "ate", "tee", "tata", ],
                                  ["tie", "it", "at"],
                                  ["tine", "tint", "net", "ten", "ant", "tan", ],
                                  ["stint", "stone", "notes", "nest"]]

        self.pygame.mixer.init()
        self.sound_keytype = pygame.mixer.Sound("type.wav")
        self.sound_correct = pygame.mixer.Sound("correct.wav")
        self.sound_word = pygame.mixer.Sound("word.wav")
        self.sound_wrong = pygame.mixer.Sound("wrong.wav")
        self.sound_levelup = pygame.mixer.Sound("levelup.wav")


    def get_letters_for_level(self):
        """ Get retrieve all the letters to be tested at the current level.
        """
        
        self.letters_in_play = self.alphabet[:(2 + self.level)]
    

    def play_game(self):
        """ This exists, because I might want to choose instead to run the game
            from outside of the object to make the pygame clock-timing work
            right (calling the self.iterate function).
        """
        
        while(self.game_in_play == True):
            self.iterate()


    def get_new_prompt(self):
        """ Set the current_prompt to a letter that's currently in play and not
            the previous current_prompt.
        """

        self.letters_in_play = self.alphabet[:(self.zero_level_letters + self.level)]
        self.current_prompt = choice(self.letters_in_play)

        while(self.current_prompt == self.previous_prompt):
            self.current_prompt = choice(self.letters_in_play)
            
        self.need_prompt = False
        self.previous_prompt = self.current_prompt


    def get_new_word_prompt(self):
        """ Randomly select a new word from the list of possible words at the current
            level.
        """
        
        self.word_prompt = choice(self.list_word_prompts[self.level])
        self.need_word_prompt = False


    def update_and_respond(self, correct):
        """ If the right letter was typed, increment that letter's value
            in the list of letters_right, and likewise for letters_wrong
            if wrong.
        """
        
        if self.input_letter == "space":  # Can get rid of this?
            return
        else:
            temp_index = self.alphabet.index(self.input_letter)
            if correct:
                self.letters_right[temp_index] += 1
                if self.letters_right[temp_index] > self.max_right:
                    self.letters_right[temp_index] = self.max_right
            else:
                self.letters_right[temp_index] -= 1
                if self.letters_right[temp_index] < 0:
                    self.letters_right[temp_index] = 0
                self.response = self.letter_to_key_combo[self.current_prompt]
                self.time_to_wait = 400
                

    def display_letter_prompt(self):
        """ Write the current letter prompt to the screen.
        """
        
        text = self.font.render(self.current_prompt, True, self.blue)
        self.gameDisplay.blit(text, (390, 100))

    def display_word_prompt(self):
        """ Write the current word prompt to the screen.
        """
        
        text = self.font.render(self.word_prompt, True, self.blue)
        self.gameDisplay.blit(text, (350, 50))


    def display_response(self):
        """ Draw the keys to the screen
        """
        
        for i in range(len(self.response)):
            if self.response[i] == 'X':
                color = self.yellow
            elif self.response[i] == 'O':
                color = self.light_blue
            if i > 2:
                xpos = (50 + 40 + (i*110))
            else:
                xpos = (50 + (i*110))

            position = (xpos, 300, 100, 150) 
            self.draw_single_button(self.blue, position)
            position_small = (xpos+20, 320, 60, 110)
            self.draw_single_button(color, position_small)
            
                
    def draw_single_button(self, color, position):
        """ Draw a single button to the screen.
        """

        self.pygame.draw.ellipse(self.gameDisplay, color, position)


    def check_level(self):
        """ Check if all letters have received enough correct responses
            to increment the level.  If so, increment the level.
        """
        
        temp_flag = True
        for i in range(len(self.letters_in_play)):
            if self.letters_right[i] < self.max_right:
                temp_flag = False

        if temp_flag:
            self.level += 1
            self.sound_levelup.play()
            self.letters_right = np.ones(26)
            print("Level up!")

        print(self.letters_right[:len(self.letters_in_play)])


    def word_or_not(self):
        """ If more than five letter prompts have been answered,
            there is a fifty percent chance to test a word next.
        """
        
        if self.number_prompts_answered > 5:
            if randint(0, 1):
                self.game_state = "testing_word"
                self.switch_to_word()
                return(True)
            else:
                return(False)
        else:
                return(False)


    def switch_to_word(self):
        """ Switch the current prompt to a word.
        """
        
        self.current_prompt = None
        self.get_new_word_prompt()
        self.number_prompts_answered = 0
        self.game_state = "testing word"
        

    def switch_to_letter(self):
        """ Switch the current prompt to a letter.
        """
        
        self.word_prompt = ""
        self.get_new_prompt()
        self.game_state = "testing letter"
            

    def reset_variables(self):
        """ Reset all variables.
        """
        
        self.key_was_pressed = False
        self.input_letter = None
        self.response = 'OOOOOO'
        self.time_to_wait = 0
        

    def introduction(self):
        """ Under construction: add introductory speech,
            music, and instructions.
        """
        
        if self.intro_done == False:
            self.time_to_wait = 200
            self.intro_done = True
        
        else:
            if self.input_letter == 'space':
                self.switch_to_letter()

        self.word_prompt = 'Press Space'
        self.display_word_prompt()
        self.display_response()


    def test_letter(self):
        """ Decision tree for testing a letter.
        """
        
        if self.input_letter != None:
            if self.input_letter == self.current_prompt:
                self.sound_correct.play()
                self.number_prompts_answered += 1
                self.attempts = 0
                self.check_level()
                self.update_and_respond(True)
                if self.word_or_not() == False:
                    self.get_new_prompt()
            else:
                self.sound_wrong.play()
                self.pygame.time.wait(100)
                self.attempts += 1
                self.update_and_respond(False)
        self.display_letter_prompt()
        self.display_response()


    def test_word(self):
        """ Decision tree for testing a word.
        """
        
        if self.input_letter != None and self.input_letter != 'space':
            self.word_string += self.input_letter
        elif self.input_letter == 'space' or len(self.word_string) > len(self.word_prompt):
            if self.word_string == self.word_prompt:
                self.sound_word.play()
                self.number_words_correct += 1
                self.word_prompt = ""
                self.word_string = ""
                self.switch_to_letter()
            else:
                self.sound_wrong.play()
                self.pygame.time.wait(100)
                self.word_prompt = ""
                self.word_string = ""
                self.switch_to_letter()

        self.display_word_prompt()
        self.display_response()


    def iterate(self):
        """ A single iteration of the game loop.
        """
        
        self.reset_variables()

        self.gameDisplay.blit(self.bg, (0,0))

        for event in self.pygame.event.get():
            if event.type == self.pygame.KEYDOWN:
                self.input_letter = self.pygame.key.name(event.key)
                self.key_was_pressed = True # Can I get rid of this?
                self.sound_keytype.play()

        if self.game_state == "introduction":
            self.introduction()

        elif self.game_state == "testing letter":
            self.test_letter()

        elif self.game_state == "testing word":
            self.test_word()

        self.pygame.display.update()

        self.pygame.time.wait(self.time_to_wait)

        self.clock.tick(200)


def test_typing_tutor():
    """ Test the game.
    """
    
    Typing_Tutor = TypingTutor()
    Typing_Tutor.play_game()    


if __name__ == "__main__":
    test_typing_tutor()
