from random import choice, randint
from BELLA_GAME import Bella_Game

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
        self.hidden_pos = []
        self.found_pos = []
        self.intro_played = False
        self.new_card = False


#---CENTRAL FUNCTIONS---

    def iterate(self, input_dict):

        self.gameDisplay.fill(self.display_states[self.display_names[self.current_display_state]]['background'])

        self.current_input = input_dict['cursor_key']
        self.letter_control = input_dict['standard']

        if self.letter_control == 'display':
            self.change_display_state()

        if self.game_state == 'introduction':
            self.introduction(input_dict)
        elif self.game_state == 'game_play_letters':
            self.game_play_letters()
        elif self.game_state == 'game_play_words':
            self.game_play_words()
        elif self.game_state == 'game_play_different':
            self.game_play_different()

        self.pygame.display.update()


    def introduction(self, input_dict):

        if input_dict['card_trigger'] == True:
            self.new_card = True
        elif (input_dict['card_state'] == True) & (self.new_card == True):
            self.play_sound('cardinserted', self.standard_sfx, wait=True)
            self.card_str = input_dict['card_str']
            self.game_state = 'game_play'
            self.get_search_letters()
            self.search_letter_num = 0
            self.letter_prompt = self.search_list[self.search_letter_num]
            self.get_search_positions(self.letter_prompt)
        elif self.intro_played == False:
            self.play_sound('insert_a_card', self.standard_voice)
            self.intro_played = True

        self.display_word_prompt()


    def game_play_letters(self):
        if self.current_input != None:
            print("button pressed!")
            if (self.current_input in self.hidden_pos):
                self.correct_choice()
            else:
                if(self.current_input in self.found_pos):
                    self.play_sound('double', self.standard_sfx)
                    self.play_sound('already_found', self.standard_voice)
                else:
                    self.play_sound('wrong', self.standard_sfx)

        self.display_letter_prompt()

    def game_play_words(self):
        pass
        # read a word from the word list
        # check to see if they found it
        # tell them to type the word
        # update the score

    def game_play_different(self):
        pass
        # find the letter that's different.

    def get_search_words(self):
        self.word_list = self.card_str.split(' ')


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


    def get_search_positions(self, letter): # Can I just make this compare on the fly?

        self.hidden_pos = [pos for pos,char in enumerate(self.card_str) if char == letter]
        print("letter = {}  positions = {}".format(letter,self.hidden_pos))
        self.found_pos = []

        self.play_sound('find_all_the', self.standard_voice, True)
        self.play_sound(self.letter_prompt, self.standard_alphabet, True)
        self.play_sound('_s', self.standard_voice, True)


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
