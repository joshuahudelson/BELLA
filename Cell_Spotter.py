from random import choice, randint
from BELLA_GAME import Bella_Game
import re

class Cell_Spotter(Bella_Game):
    """ A game that requires a card to play.  Game prompts a player with a letter, and
        the player finds that letter on the card and presses
        the cursor key above it.
    """

    def __init__(self, gametools, display_data, starting_level=0):
        super().__init__(gametools, display_data, starting_level)
        """
        """

#---GAME VARIABLES---

        self.game_name = 'Cell Spotter'
        self.game_state = 'introduction' # others: game_play_letters, game_play_words, game_play_contractionsz
        self.current_input = None
        self.letter_prompt = ''
        self.word_prompt = 'insert card'
        self.card_str = '                    '
        self.card_inserted = False
        self.freq_dict = {}
        self.search_list = []
        self.search_letter_num = 0
        self.search_word_num = 0
        self.hidden_pos = []
        self.found_pos = []
        self.hidden_pos_word = []
        self.found_pos_word = []
        self.intro_played = False
        self.new_card = False
        self.card_ID = None
        self.word_list = None
        self.word_histogram = None

        self.card_codes = {'1': 'game_play_mccarthy_level_1',
                           '2': 'game_play_mccarthy_level_2',
                           '3': 'game_play_mccarthy_level_3',
                           '4': 'game_play_mccarthy_level_4'
                           'l': 'game_play_letters',
                           'w': 'game_play_words'}

#---CENTRAL FUNCTIONS---

    def iterate(self, input_dict):

        self.gameDisplay.fill(self.display_states[self.display_names[self.current_display_state]]['background'])

        self.current_input = input_dict['cursor_key']
        self.letter_control = input_dict['standard']
        self.card_ID = input_dict['card_ID']

        if self.letter_control == 'display':
            self.change_display_state()

        if self.game_state == 'introduction':
            self.introduction(input_dict)
        elif self.game_state == 'game_play_letters':
            self.game_play_letters()
        elif self.game_state == 'game_play_words':
            self.game_play_words()
        elif self.game_state == 'game_play_mccarthy_level_1':
            self.game_play_mccarthy_level_1
        elif self.game_state == 'game_play_mccarthy_level_2':
            self.game_play_mccarthy_level_2()
        elif self.game_state == 'game_play_mccarthy_level_3':
            self.game_play_mccarthy_level_3()
        elif self.game_state == 'game_play_mccarthy_level_4':
            self.game_play_mccarthy_level_4()
        elif self.game_state == 'game_play_mccarthy_level_5':
            self.game_play_mccarthy_level_5()
        elif self.game_state == 'game_play_mccarthy_level_6':
            self.game_play_mccarthy_level_6()

        self.pygame.display.update()


    def introduction(self, input_dict):
        """ Prompt user to insert a card.  If the card has a code, change the
            game state to the corresponding string.  Otherwise, just play the
            default game.
            Depending on the game state, change the list of search letters or
            words.
        """
        if input_dict['card_trigger'] == True:
            self.new_card = True
        elif (input_dict['card_state'] == True) & (self.new_card == True):
            self.play_sound('cardinserted', self.standard_sfx, wait=True)
            self.card_str = input_dict['card_str']
            try:
                self.game_state = self.card_codes[self.card_ID]
            except KeyError:
                self.game_state = 'game_play_letters'

            if (self.game_state == 'game_play_letters'):
                self.get_search_letters()
                self.search_letter_num = 0
                self.letter_prompt = self.search_list[self.search_letter_num]
                self.get_search_positions(self.letter_prompt)

            elif (self.game_state == 'game_play_words'):
                """ get search words
                    get search positions for wors
                """
                self.get_search_words()
                self.search_word_num = 0
                self.word_prompt = self.search_list_word[self.search_word_num]
                self.get_search_positions_for_word(self.word_prompt)

            elif (self.game_state == 'game_play_mccarthy_level_1'):
                self.get_search_letters()
                if len(self.search_list) < 2:
                    # card won't work for this game
                    self.intro_played = False
                else:
                    self.search_list = self.search_list[-2] # only search for the second-most-frequent letter.
                    self.search_letter_num = 0 # start with whatever the not-most-frequent letter is.
                    self.letter_prompt = self.search_list[self.search_letter_num]  # set search letter to next-most-common letter.
                    self.get_search_positions(self.letter_prompt

            elif (self.game_state == 'game_play_mccarthy_level_2'):
                self.get_search_letters()
                if len(self.search_list) < 2:
                    self.intro_played = False
                else:
                    self.search_list = self.search_list[-1]  # search only for most frequent letter
                    search_letter_num = 0
                    self.letter_prompt = self.search_list[self.search_letter_num]
                    self.get_search_positions(self.letter_prompt)

            elif (self.game_state == 'game_play_mccarthy_level_3'):
                self.get_search_letters()
                # words

        elif self.intro_played == False:
            self.play_sound('insert_a_card', self.standard_voice)
            self.intro_played = True

        self.display_word_prompt() # why is this here?


    def game_play_letters(self):
        if self.current_input != None:
            print("button pressed!")
            if (self.current_input in self.hidden_pos):
                self.correct_choice()
            else:
                if (self.current_input in self.found_pos):
                    self.play_sound('double', self.standard_sfx)
                    self.play_sound('already_found', self.standard_voice)
                else:
                    self.play_sound('wrong', self.standard_sfx)

        self.display_letter_prompt()

    def game_play_words(self):
        """ If the button is within range of the word,

        """
        if self.current_input != None:
            print("button pressed2!")
            if (self.current_input in self.hidden_pos_word):
                self.correct_choice_word()
            else:
                if (self.current_input in self.found_pos_word):
                    self.play_sound('double', self.standard_sfx)
                    self.play_sound('already_found', self.standard_voice)
                else:
                    self.play_sound('wrong', self.standard_sfx)

    def game_play_mccarthy_level_1(self):
        self.game_play_letters()

    def game_play_mccarthy_level_2(self):
        self.game_play_letters()

    def game_play_mccarthy_level_3(self):
        self.game_play_words()

    def game_play_mccarthy_level_4(self):
        self.game_play_words()

    def game_play_mccarthy_level_5(self):
        pass
        # Totally different

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
        try:
            del self.freq_dict['_']
        except KeyError:
            pass
        self.search_list = sorted(self.freq_dict,key=self.freq_dict.get)
        print(self.search_list)

    def get_search_positions(self, letter):
        self.hidden_pos = [pos for pos,char in enumerate(self.card_str) if char == letter]
        print("letter = {}  positions = {}".format(letter,self.hidden_pos))
        self.found_pos = []

        if (self.game_state == 'game_play_letters'):
            self.play_sound('find_all_the', self.standard_voice, True)
            self.play_sound(self.letter_prompt, self.standard_alphabet, True)
            self.play_sound('_s', self.standard_voice, True)
        elif (self.game_state == 'game_play_mccarthy'):
            try:
                self.play_sound('find_the_one_thats_different', self.standard_voice, True)
                print("Exception handled!")
            except:
                self.play_sound('find_all_the', self.standard_voice, True)
                self.play_sound(self.letter_prompt, self.standard_alphabet, True)
                self.play_sound('_s', self.standard_voice, True)

    def get_search_words(self):
        self.search_list_word = self.card_str.split(' ')
        self.word_histogram = {i:self.search_list_word.count(i) for i in self.word_list}

    def get_search_positions_for_word(self, word):
        temp_start_index = re.search(r'\b(word)\b', self.card_str)
        self.hidden_pos_word = [index+temp_start_index for index in range(len(word))]
        print("Word search positions: " + str(self.hidden_pos_word))

    def correct_choice(self):
        self.hidden_pos.remove(self.current_input)
        self.found_pos.append(self.current_input)
        if len(self.hidden_pos)<= 0:
            self.search_letter_num +=1
            if self.search_letter_num >= len(self.search_list):  # you finished searching the whole card
                self.play_sound('win', self.standard_sfx, True)
                self.play_sound('great_job', self.standard_voice, wait=True)
                self.card_inserted = False
                self.intro_played = False
                self.card_state = False
                self.new_card = False
                self.game_state = 'introduction'
            else:
                self.play_sound('level_up', self.standard_sfx, True)
                self.play_sound('nice_work', self.standard_voice, wait=True)
                self.letter_prompt = self.search_list[self.search_letter_num]
                self.get_search_positions(self.letter_prompt)
        else:
            self.play_sound('correct', self.standard_sfx)

    def correct_choice_word
        self.hidden_pos_word.remove(self.current_input)
        self.found_pos_word.append(self.current_input)
        if len(self.hidden_pos_word) <= 0:
            self.search_word_num +=1
            if self.search_word_num >= len(self.search_list_word):  # you finished searching the whole card
                self.play_sound('win', self.standard_sfx, True)
                self.play_sound('great_job', self.standard_voice, wait=True)
                self.card_inserted = False
                self.intro_played = False
                self.card_state = False
                self.new_card = False
                self.game_state = 'introduction'
            else:
                self.play_sound('level_up', self.standard_sfx, True)
                self.play_sound('nice_work', self.standard_voice, wait=True)
                self.letter_prompt = self.search_list[self.search_letter_num]
                self.get_search_positions(self.letter_prompt)
        else:
            self.play_sound('correct', self.standard_sfx)
