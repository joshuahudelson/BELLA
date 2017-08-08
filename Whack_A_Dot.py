from random import choice, randint
from BELLA_GAME import Bella_Game

class Whack_A_Dot(Bella_Game):
    """ A game in which the user is prompted to press vibrating
        keys.
    """

    def __init__(self, gametools, display_data, starting_level=0):
        super().__init__(gametools, display_data, starting_level)
        """

            self.game_state: string, what part of the game is currently running

            self.alphabet: string, the characters--in order--that will be added
                           to the set of possible prompts as the player advances
                           levels.

            self.letters_in_play: string, the current set of characters being
                                  prompted.

            self.letters_by_level: list, the substring from self.alphabet that should be
                         used as self.letters_in_play for each level (the index
                         of self.letters_by_level).

            self.level: int, the player's current level.

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

#---GAME VARIABLES---

        self.correct_sfx = ["correct_one","correct_two","correct_three","correct_four","correct_five","correct_six"]
        self.correct_voice = ["fantastic","keep_it_up","good_job","great_job","outstanding"]

        self.game_name = 'Whack_A_Dot'

        self.game_state = 'introduction'
        self.alphabet = 'aeickbdfhjlmousgnprtvwxzqy'

        self.letters_in_play = ''
        self.letters_by_level = [10, 28, 46, 50]
        self.score = 0
        self.level = 0

        self.delay = 1

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


#---LOCAL GAME SOUNDS---

        self.game_sounds = self.sound_object.make_sound_dictionary(self.game_name + '_sounds', self.pygame)


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

        self.display_word_prompt('Press Space')

        if self.intro_played:

            if self.input_control == 'space':
                self.game_state = 'play_game'
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
        self.get_new_prompt()
        self.frames_passed = 0



    def incorrect_response(self):
        """ If the response is incorrect, update
            the game variables accordingly and vibrate
            the current prompt again.
        """

        self.play_sound('wrong', self.standard_sfx, wait=True)
        self.update_points(False)
        self.frames_passed = 0


    def update_points(self, correct):
        """ Increment or decrement the value in the list that
            tracks responses per character.  Can't decrement
            past 0 nor increment past self.max_correct.
        """

        if correct:
            self.points += 10

        if self.points > ((self.level + 1) * 100):
            self.play_sound('level_up', self.standard_sfx, True)
            self.play_sound(choice(self.correct_voice), self.standard_voice, wait=True)
            self.play_sound('combinations', self.game_sounds, wait=True)
            self.level += 1
            print(self.level)
            if self.level > 4:
                self.level = 4


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
            self.level += 1
            print("Level up")
            if self.level > len(self.letters_by_level)-1:
                self.level = len(self.letters_by_level)-1
                self.update_letters_in_play
                print("Level up")


    def get_new_prompt(self):
        """ Generate a new random prompt.
            Don't keep it if it's the same as
            the one just prompted.
        """

        previous_prompt = self.current_prompt

        while(previous_prompt == self.current_prompt):
            self.current_prompt = self.generate_chord(self.level + 1)

        self.prompt_vibrated = False


    def update_letters_in_play(self):
        """ If the level has changed, set the letters in play
            to reflect that.
        """

        self.letters_in_play = self.alphabet[:self.letters_by_level[self.level]]


    def vibrate_buttons(self):
        """ Vibrate the buttons that correspond to the current prompt.
        """

        self.braille_keyboard.vibrate_chord(self.current_prompt, sim=True)


    def generate_chord(self, num_keys):
        """ Generate and return a random chord with a given number
            of keys in it.
        """
        num_keys = choice(range(num_keys))
        if num_keys > 5:
            num_keys = 5
        if num_keys < 1:
            num_keys = 1

        press_list = []

        while len(press_list) < num_keys:
            possible_key = randint(0, 5)
            if possibly_key not in press_list:
                press_list.append(possibly_key)

        chord = ''

        for i in range(6):
            if i in press_list:
                chord += '1'
            else:
                chord += '0'

        return chord
