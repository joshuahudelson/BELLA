from random import choice, randint
from BELLA_GAME import Bella_Game
import re
import louis

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

        self.game_name = 'Cell_Spotter'
        self.game_state = 'introduction' # others: game_play_letters, game_play_words, game_play_contractionsz
        self.current_input = None
        self.letter_prompt = ''
        self.word_prompt = None
        self.card_str = '                    '
        self.card_inserted = False
        self.freq_dict = {}

        self.search_list = []
        self.search_list_words = []
        self.search_letter_num = 0
        self.search_word_num = 0

        self.hidden_pos = []
        self.found_pos = []
        self.hidden_pos_word = []
        self.found_pos_word = []
        self.intro_played = False
        self.new_card = False
        self.card_ID = None
        self.word_histogram = None

        self.word_sf_list = [word[0:-4] for word in self.words_file]

        self.card_codes = {'1': 'game_play_mccarthy_level_1',
                           '2': 'game_play_mccarthy_level_2',
                           '3': 'game_play_mccarthy_level_3',
                           '4': 'game_play_mccarthy_level_4',
                           'l': 'game_play_letters',
                           'w': 'game_play_words'}

        self.update_dict = {}


#---LOCAL GAME SOUNDS---

        self.game_sounds = self.sound_object.make_sound_dictionary(self.game_name + '_sounds', self.pygame)

#---CENTRAL FUNCTIONS---

    def iterate(self, input_dict):
        self.update_dict.clear()

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
            self.game_play_letters()
        elif self.game_state == 'game_play_mccarthy_level_2':
            self.game_play_letters()
        elif self.game_state == 'game_play_mccarthy_level_3':
            self.game_play_words()
        elif self.game_state == 'game_play_mccarthy_level_4':
            self.game_play_words()
        self.pygame.display.update()
        return(self.update_dict)

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
            self.initialize_game()
            return
        elif self.intro_played == False:
            self.play_sound('insert_a_card', self.standard_voice)
            self.intro_played = True
        self.word_prompt = "Insert a card."
        self.display_word_prompt()                                               # Why is this here?

    def initialize_game(self):
        """
        """
        if (self.game_state == 'game_play_letters'):
            self.get_search_letters()
            self.search_letter_num = 0
            self.letter_prompt = self.search_list[self.search_letter_num]
            self.get_search_positions(self.letter_prompt)
        elif (self.game_state == 'game_play_words'):
            self.get_search_words()
            self.search_word_num = 0
            self.word_prompt = self.search_list_words[self.search_word_num]
            print("THIS IS THE WORD PROMPT: " + str(self.word_prompt))
            self.get_search_positions_for_word(self.word_prompt)
        elif (self.game_state == 'game_play_mccarthy_level_1'):
            self.get_search_letters()
            if len(self.search_list) < 2:
                self.play_sound('sorrythatcardisntforthisgame', self.game_sounds)
                self.intro_played = False
            else:
                self.search_list = self.search_list[-2]                         # only search for the second-most-frequent letter.
                self.search_letter_num = 0                                      # start with whatever the not-most-frequent letter is.
                self.letter_prompt = self.search_list[self.search_letter_num]   # set search letter to next-most-common letter.
                self.get_search_positions(self.letter_prompt)
        elif (self.game_state == 'game_play_mccarthy_level_2'):
            self.get_search_letters()
            if len(self.search_list) < 2:
                self.play_sound('sorrythatcardisntforthisgame', self.game_sounds)
                self.intro_played = False
            else:
                self.search_list = self.search_list[-1]                         # search only for most frequent letter
                search_letter_num = 0
                self.letter_prompt = self.search_list[self.search_letter_num]
                self.get_search_positions(self.letter_prompt)
        elif (self.game_state == 'game_play_mccarthy_level_3'):
            self.get_search_words()
            if len(self.search_list_words) < 2:
                self.play_sound('sorrythatcardisntforthisgame', self.game_sounds)
                self.intro_played = False
            else:
                self.search_list_words = self.search_list_words[0]
                self.search_word_num = 0
                self.word_prompt = self.search_list_words[self.search_word_num]
                self.get_search_positions_for_word(self.word_prompt)

    def game_play_letters(self):
        if self.current_input != None:
            if (self.current_input in self.hidden_pos):
                self.correct_choice()
            else:
                if (self.current_input in self.found_pos):
                    self.play_sound('double', self.standard_sfx)
                    self.play_sound('already_found', self.standard_voice)
                    self.update_dict = {'stat_type':'CS_n_l_t_incorrect',
                                    'stat_element':self.letter_prompt}
                else:
                    self.play_sound('wrong', self.standard_sfx)
                    self.update_dict = {'stat_type':'CS_n_l_t_incorrect',
                                    'stat_element':self.letter_prompt}

        self.display_letter_prompt()

    def game_play_words(self):
        """ If the button is within range of the word,
        """
        if self.current_input != None:
            for word_index in range(len(self.hidden_pos_word)):
                if self.current_input in self.hidden_pos_word[word_index]:
                    self.correct_choice_word(word_index)
                    return
            for word_index in range(len(self.found_pos_word)):
                if self.current_input in self.found_pos_word[word_index]:
                    self.play_sound('double', self.standard_sfx)
                    self.play_sound('already_found', self.standard_voice)
                    self.update_dict = {'stat_type':'CS_n_w_t_incorrect',
                                        'stat_element':self.word_prompt}
                    return
            self.play_sound('wrong', self.standard_sfx)
            self.update_dict = {'stat_type':'CS_n_w_t_incorrect',
                                'stat_element':self.word_prompt}

        self.display_word_prompt()

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
        try:
            del self.freq_dict['\r']
        except KeyError:
            pass
        self.search_list = sorted(self.freq_dict,key=self.freq_dict.get)
        print(self.search_list)

    def get_search_positions(self, letter):
        self.hidden_pos = [pos for pos,char in enumerate(self.card_str) if char == letter]
        print("letter = {}  positions = {}".format(letter,self.hidden_pos))
        self.found_pos = []

        if (self.game_state == 'game_play_letters'):
            self.play_sound('findalloftheletter', self.game_sounds, True)
            self.play_sound(self.letter_prompt, self.standard_alphabet, True)
            #self.play_sound('_s', self.standard_voice, True)
        elif (self.game_state == 'game_play_mccarthy'):
            try:
                self.play_sound('find_the_one_thats_different', self.standard_voice, True)
                print("Exception handled!")
            except:
                self.play_sound('findtheonethatsdifferent', self.game_sounds, True)
                self.play_sound(self.letter_prompt, self.standard_alphabet, True)
                self.play_sound('_s', self.standard_voice, True)

    def get_search_words(self):
        self.search_list_words = self.card_str.split(' ')
        self.search_list_words = set(self.search_list_words)
        self.search_list_words = list(self.search_list_words)                   # Now contains only unique words.
        temp_nothing = ''
        if temp_nothing in self.search_list_words:
            self.search_list_words.remove(temp_nothing)
        print("LIST OF WORDS:" + str(self.search_list_words))
        self.word_histogram = {i:self.search_list_words.count(i) for i in self.search_list_words}

    def get_search_positions_for_word(self, word):
        # temp_start_index = re.search(r'\b(word)\b', self.card_str)
        temp_start_index = [word_copy.start() for word_copy in re.finditer(word, self.card_str)]
        print("This is the TEMP START INDEX: " + str(temp_start_index))          # THIS IS RETURNING NONE RIGHT NOW.
        self.hidden_pos_word = [[index + letter for letter in range(len(word))] for index in temp_start_index]
        print("Word search positions: " + str(self.hidden_pos_word))
        self.play_sound('findtheword', self.game_sounds, True)
        if self.word_prompt in self.word_sf_list:
            self.play_sound(self.word_prompt, self.standard_words)


    def correct_choice(self):
        self.update_dict = {'stat_type':'CS_n_l_t_correct',
                            'stat_element':self.letter_prompt}
        self.hidden_pos.remove(self.current_input)
        self.found_pos.append(self.current_input)
        if len(self.hidden_pos)<= 0:
            self.search_letter_num +=1
            if self.search_letter_num >= len(self.search_list):  # you finished searching the whole card
                self.play_sound('win', self.standard_sfx, True)
                self.play_sound('great_job', self.standard_voice, wait=True)
                self.reset_game()
            else:
                self.play_sound('level_up', self.standard_sfx, True)
                self.play_pos_feedback(True, 1)
                self.letter_prompt = self.search_list[self.search_letter_num]
                self.get_search_positions(self.letter_prompt)
        else:
            self.play_sound('correct', self.standard_sfx)

    def correct_choice_word(self, word_index):
        self.update_dict = {'stat_type':'CS_n_w_t_correct',
                            'stat_element':self.word_prompt}
        self.found_pos_word.append(self.hidden_pos_word[word_index])
        self.hidden_pos_word.remove(self.hidden_pos_word[word_index])
        if len(self.hidden_pos_word) <= 0:
            self.search_word_num +=1
            if self.search_word_num >= len(self.search_list_words):  # you finished searching the whole card
                self.play_sound('win', self.standard_sfx, True)
                self.play_sound('great_job', self.standard_voice, wait=True)
                self.reset_game()

            else:
                self.play_sound('level_up', self.standard_sfx, True)
                self.play_sound('nice_work', self.standard_voice, wait=True)
                self.word_prompt = self.search_list_words[self.search_word_num]
                self.get_search_positions_for_word(self.word_prompt)
        else:
            self.play_sound('correct', self.standard_sfx)

    def reset_game(self):
        self.card_inserted = False
        self.intro_played = False
        self.card_state = False
        self.new_card = False
        self.game_state = 'introduction'
        self.hidden_pos = []
        self.hidden_pos_word = []
        self.found_pos = []
        self.found_pos_word = []
