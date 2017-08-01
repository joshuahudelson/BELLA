from random import choice, randint, random
import numpy as np
from BELLA_GAME import Bella_Game

class KeyCrush(Bella_Game):

    def __init__(self, gametools, display_data, starting_level=0):
        super().__init__(gametools, display_data, starting_level)

        """
        self.alphabet: list; letters to be tested, in order.

        self.list_word_prompts: list, words to be tested.

        self.letters_correct: list, int between 0 and self.max_correct.

        self.game_state: string; introduction, test_leter, test_word,
                                 or announcement.

        self.max_correct: int, maximum number of times letter must be
                          answered corectly to advance a level.

        self.level: int, the current player's level.

        self.zero_level_letters: int, the number of letters to be
                                 tested when the level is zero.

        self.letters_in_play: string, the letters currently being
                              tested.

        self.letter_prompt: string, the current single-letter
                             prompt.

        self.previous_prompt: string, the previous single-letter
                               prompt.

        self.input_letter: string, the letter most recently typed.

        self.input_control = string, holds input from keyboard (used
                             here to change display and receive space bar)

        self.total_attempted_letters_answered: int, total number of attempted
                                     answers.

        self.total_attempted_letters_answered_correctly: int, number of attempts that were
                              successful.

        self.letter_streak: int, length of most recent series of
                            all-correct letter answers.

        self.career_streak: int, longest streak of this game.

        self.letter_attempts_before_word: int, tallies answered letters;
                                          helps switch to word if above some #.

        self.letter_attempts_before_hint = int, number of wrong answers for current letter
                                           (after 2, a hint is given on subsequent ones)

        self.letter_attempts_threshold: int, number of attempts before possible
                                        to switch to word.

        self.total_words_answered: int, total number of words answered.

        self.words_answered_correctly: int, number of words answered
                                       correctly.

        self.word_streak: int, length of most recent series of all-correct
                           word answers.

        self.word_string: string, the concatenated player input when
                          answering a word.

        self.word_prompt: string, the word to be answered.

        self.word_has_been_said = boolean, whether current word soundfile has been
                                  played by game yet.

        self.intro_done: boolean, has the introduction sound been played?

        self.points_to_be_awarded: int, base number of points, adjusted depending on
                                    whether earned in a streak or after a wrong letter, etc.

        self.total_points: int, tally of all points so far in game.

        self.using_card: boolean, whether game is using an inserted card or the game's own
                         alphabet.

        self.card_str: string, the set of letters read from an inserted card.  If a card is
                       being used, the letters to be tested are chosen from tis, rather than
                       the game's self.alphabet string.
        """

#---GAME VARIABLES---

        self.game_name = 'KeyCrush'
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.alphabet_length = len(self.alphabet)

        self.words_by_letters = []
        for i in range(self.alphabet_length):
            self.words_by_letters.append([])

        self.sort_words() # populates self.words_by_letters.

        self.game_state = 'introduction'
        self.level = starting_level
        self.level_advance_threshold = 5

        self.max_correct = 1000
        self.max_incorrect = 1000

        self.zero_level_letters = 3
        self.level_letter_increment = 1

        self.num_letters_in_play = self.zero_level_letters;
        self.letters_in_play = ""

        self.letter_prompt = None
        self.previous_prompt = None

        self.input_letter = None
        self.input_control = None

        self.letters_correct = self.np.ones(self.alphabet_length)
        self.letters_incorrect = self.np.ones(self.alphabet_length)
        self.letters_ratio = self.np.ones(self.alphabet_length)

        self.correct_letter_increment_amount = 1
        self.incorrect_letter_increment_amount = 3

        self.total_attempted_letters_answered = 0
        self.total_attempted_letters_answered_correctly = 0

        self.letter_streak = 0
        self.career_streak = 0

        self.letter_attempts_before_word = 0
        self.letter_attempts_before_hint = 0
        self.letter_attempts_threshold = 3

        self.total_words_answered = 0
        self.words_answered_correctly = 0
        self.word_streak = 0

        self.word_string = ""
        self.word_prompt = ""
        self.word_has_been_said = False

        self.intro_done = False

        self.points_to_be_awarded = None # put in docstring, from here down...
        self.total_points = 0

        self.using_card = False
        self.card_str = ''

#---LOCAL GAME SOUNDS---

        self.game_sounds = self.sound_object.make_sound_dictionary(self.game_name + '_sounds', self.pygame)

#---CENTRAL FUNCTIONS---

    def iterate(self, input_dictionary):
        """ A single iteration of the game loop.
            Runs either introduction, test_letter,
            or test_word each time.
        """

        self.gameDisplay.fill(self.display_states[self.display_names[self.current_display_state]]['background'])

        self.input_letter = input_dictionary['letter']
        self.input_control = input_dictionary['standard']

        if (self.input_control == 'display'):
            self.change_display_state()

        if input_dictionary['card_trigger']:
            self.get_card_data()

        if self.input_letter != None:
            self.play_sound('type', self.standard_sfx)

        if self.game_state == "introduction":
            self.introduction()
        elif self.game_state == "testing letter":
            self.test_letter()
        elif self.game_state == "testing word":
            self.test_word()

        self.pygame.display.update()

    def introduction(self):
        """ Populates the lists of words.
            Plays instructions and waits for space-bar
            to be pressed.
        """
        if self.intro_done == False:
            self.play_sound('instructions', self.game_sounds)
            self.intro_done = True
        else:
            if self.input_control == 'space':
                self.switch_to_letter()

        self.display_word_prompt('Press Space')
        self.draw_buttons()


    def test_letter(self):
        """ Just displays if the user hasn't typed anything.
            Calls correct/wrong responses if user types something.
        """
        if self.input_control == 'space':
            self.give_hint(self.letter_prompt)
        else:
            if self.input_letter != None:
                if self.input_letter == self.letter_prompt:
                    self.letter_is_correct()
                else:
                    self.letter_is_wrong()

        self.display_letter_prompt()
        self.display_status_box()
        self.draw_buttons()


    def test_word(self):
        """ Test user on a word prompt.
        """
        if self.input_control == 'space':
            self.give_hint(self.word_prompt[len(self.word_string)])
        else:
            if self.word_has_been_said:
                self.update_and_check_word()
            else:
                #self.play_sound(self.word_prompt, self.game_sounds) - Need text-to-speech or recordings.
                self.word_has_been_said = True

        self.display_word_prompt()
        self.draw_buttons()
        self.display_status_box()

#---OTHER FUNCTIONS---

    def get_card_data(self):
        """ Read data from card, check to make sure characters
            are ones that KeyCrush would test--and also not already
            in the string to be tested, and if so, include
            them.
        """

        self.using_card = True
        temp_string = input_dictionary['card_str']
        for character in temp_string:
            if (character in self.alphabet) & (character not in self.card_str):
                self.card_str += character
        self.letters_correct = self.np.ones(len(self.card_str))
        self.switch_to_letter()

    def update_and_check_word(self):
        """ Add the most recent typed letter to a string and check
            whether the string as long as the word string or whether the
            user has typed space.  If either is true, compare the words.
        """

        if self.input_letter != None:
            self.word_string += self.input_letter
        elif (len(self.word_string) >= len(self.word_prompt)):
            if self.word_string == self.word_prompt:
                self.word_is_correct()
            else:
                self.word_is_wrong()

    def letter_is_correct(self):
        """ Update variables for a correctly-answered letter,
            play response sound, and call for a new letter prompt.
        """

        self.total_attempted_letters_answered += 1
        self.total_attempted_letters_answered_correctly += 1

        self.letter_streak += 1
        self.total_points += self.letter_streak * self.points_to_be_awarded
        print(self.total_points)
        self.letter_attempts_before_hint = 0
        self.letter_attempts_before_word += 1

        if self.letter_streak > self.career_streak:
            self.career_streak = self.letter_streak

        self.update_letter_tracking(True)

        if self.letter_streak % 5 == 0:
            self.play_streak_sound()
        else:
            self.play_sound('correct_coins', self.game_sounds)

        self.check_level()

        if (self.letter_attempts_before_word > self.letter_attempts_threshold) & (not self.using_card):
            self.gamble_switch_to_word()
        else:
            self.get_new_letter()

    def play_streak_sound(self):
        pass

    def letter_is_wrong(self):
        """ Update variables for an incorrectly-answered letter,
            play response sound, and possibly give a hint.
        """
        self.play_sound('wrong_buzz', self.game_sounds)

        self.total_attempted_letters_answered += 1
        self.letter_streak = 0
        self.letter_attempts_before_hint += 1
        self.points_to_be_awarded = int(self.points_to_be_awarded * 0.5)

        if self.letter_attempts_before_hint > 2:
            self.points_to_be_awarded = 0
            self.give_hint(self.letter_prompt)

        self.update_letter_tracking(False)
        print('Wrong letter!')

    def word_is_correct(self):
        """ Update variables for a correctly-answered word,
            play response sound, and switch to testing letter.
        """
        self.total_words_answered += 1
        self.words_answered_correctly += 1
        self.word_streak += 1
        self.total_points += self.points_to_be_awarded
        self.play_sound('hang_of_it', self.game_sounds, wait=True)

        self.switch_to_letter()

    def word_is_wrong(self):
        """ Update variables for an incorrectly-answered word,
            play response sound, and switch to testing letter.
        """
        self.total_words_answered += 1
        self.word_streak = 0
        self.play_sound('wrong_buzz', self.game_sounds)
        self.switch_to_letter()

    def update_letter_tracking(self, boolean):
        """ If the correct letter was typed, increment that letter's value
            in the list of letters_correct.  Decrement if incorrect.
    """
        if self.using_card:
            temp_index = self.card_str.index(self.letter_prompt)
        else:
            temp_index = self.alphabet.index(self.letter_prompt)

        if boolean:
            self.letters_correct[temp_index] += self.correct_letter_increment_amount
            print("added to letters_correct")
            if self.letters_correct[temp_index] > self.max_correct:
                self.letters_correct[temp_index] = self.max_correct
        else:
            self.letters_incorrect[temp_index] += self.incorrect_letter_increment_amount
            print("added to letters_incorrect")
            if self.letters_incorrect[temp_index] > self.max_incorrect:
                self.letters_incorrect[temp_index] = self.max_incorrect

        print("About to compute...")
        self.compute_letters_ratio()

    def compute_letters_ratio(self):
        for i in range(self.num_letters_in_play):
            self.letters_ratio[i] = self.letters_incorrect[i] / self.letters_correct[i]
        print(self.letters_ratio)

    def give_hint(self, prompt):
        """ Play response sound, show correct buttons.
            Vibrate the correct keys for the letter prompt.
        """
        self.draw_buttons(self.braille_keyboard.letter_to_chord[prompt])
        self.pygame.display.update()
        self.pygame.time.wait(500)
        self.play_sound('hint', self.game_sounds, wait=True)
        self.braille_keyboard.vibrate_letter(prompt)

    def gamble_switch_to_word(self):
        """ Roll dice to see if a word should be tested now.
        """

        tossup = randint(0, 4)

        if tossup == 0:
            self.game_state = "testing_word"
            self.switch_to_word()
        else:
            self.get_new_letter()

    def switch_to_word(self):
        """ Get a word prompt and test it.
        """
        self.points_to_be_awarded = 100
        self.letter_prompt = None
        self.get_new_word_prompt()
        self.game_state = "testing word"
        self.play_sound('lets_try_word', self.game_sounds, True)

    def switch_to_letter(self):
        """ Get a letter prompt and test it.
        """
        self.points_to_be_awarded = 10
        self.word_prompt = ""
        self.word_string = ""
        self.word_has_been_said = False
        self.get_new_letter()
        self.game_state = "testing letter"

    def get_new_letter(self):
        """ Set the letter_prompt to a letter that's currently
            in play and not the previous letter_prompt.
        """

        if self.using_card:
            self.letters_in_play = self.card_str
        else:
            if self.num_letters_in_play > self.alphabet_length:
                self.num_letters_in_play = self.alphabet_length

            self.letters_in_play = self.alphabet[:self.num_letters_in_play]

        self.choose_letter()

        while(self.letter_prompt == self.previous_prompt):
            print("Chose the same!")
            self.choose_letter()

        self.previous_prompt = self.letter_prompt

        self.play_sound(self.letter_prompt, self.game_sounds)

    def choose_letter(self):
        """ Choose a random number, multiply it by the sum of letters_ratio
            and then find that value in the cumulative sum of letters_ratio.
            Letters that have a higher ratio are more likely to be chosen.
        """

        temp_cumsum = np.cumsum(self.letters_ratio[:self.num_letters_in_play])
        temp_scalar = random()
        temp_search_term = temp_scalar * temp_cumsum[-1]

        self.letter_prompt = self.letters_in_play[sum(temp_cumsum < temp_search_term)]

    def get_new_word_prompt(self):
        """ Randomly select a new word from the list of possible
            words available at the current level.
        """
        self.word_prompt = choice(self.words_by_letters[self.zero_level_letters - 1 + self.level])

    def check_level(self):
        """ Check if all letters have received enough correct responses
            to increment the level.  If so, increment the level.
        """
        temp_flag = True

        for i in range(self.num_letters_in_play):
            if self.letters_correct[i] < self.level_advance_threshold:
                temp_flag = False

        if temp_flag:
            self.play_sound('level_up_sfx', self.game_sounds, True)
            self.play_sound('level_up', self.game_sounds, True)
            self.level += 1
            self.num_letters_in_play = self.zero_level_letters + (self.level * self.level_letter_increment)
            print("Level up!")

        print(self.letters_correct[:self.num_letters_in_play])


    def sort_words(self):
        """ Go through a long list of words and sort them
            by the highest letter in each.  Print how many
            words there are for each letter.
        """

        f = open('./KeyCrush/Oxford3000plus.txt', 'r')

        num_lines = sum([1 for line in f])
        f.seek(0)

        for i in range(num_lines):

            current_word = f.readline().rstrip()

            if (len(current_word) > 1):

                temp_highest = 0
                temp_add_flag = True

                for letter in current_word:
                    try:
                        if letter not in self.alphabet:
                            temp_add_flag = False

                        if self.alphabet.index(letter) > temp_highest:
                            temp_highest = self.alphabet.index(letter)

                    except ValueError:
                        temp_add_flag = False
                        print(str(letter) + " not found in alphabet.")

                if temp_add_flag:
                    print(current_word)
                    self.words_by_letters[temp_highest].append(current_word)

        for index, container in enumerate(self.words_by_letters):
            print(self.alphabet[index])
            print(len(container))

    @property
    def score(self):
        """ Returns the score, a calculation based on
            several variables.
        """
        return self.total_points
