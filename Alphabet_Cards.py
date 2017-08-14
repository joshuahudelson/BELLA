from BELLA_GAME import Bella_Game

class Alphabet_Cards(Bella_Game):
    """
    """

    def __init__(self, gametools, display_data):
        super().__init__(gametools, display_data)

#---META-GAME STUFF---

        self.pygame = gametools['pygame']
        self.sounds = gametools['sounds']
        self.np = gametools['numpy']
        self.gameDisplay = gametools['display']
        self.braille_keyboard = gametools['keyboard']

        self.sound_object = self.sounds.sounds()
        self.game_name = 'Alphabet_Cards'

#---SOUNDS---

        self.game_sounds = self.sound_object.make_sound_dictionary(self.game_name + '_sounds', self.pygame)

#---GAME VARIABLES---

        self.game_state = None
        self.card_str = None
        self.current_button = None
        self.press_counter = 0
        self.number_of_seconds_to_wait = 3
        self.num_prompts = 0
        self.max_num_prompts = 1
        self.intro_played = False
        self.current_cursor_button = None

#---CENTRAL FUNCTIONS---

    def iterate(self, input_dict):
        """ One iteration of the game loop.
        """

        self.current_cursor_button = input_dict['cursor_key']
        self.input_control = input_dict['standard']

        self.gameDisplay.fill(self.display_states[self.display_names[self.current_display_state]]['background'])

        if self.input_control == 'display':
            self.change_display_state()

        if input_dict['card_trigger']:
            self.game_state = 'introduction'

        if self.game_state == 'introduction':
            self.introduction(input_dict)
        elif self.game_state == 'game_play':
            self.game_play(self.current_cursor_button)

        self.pygame.display.update()


    def introduction(self, input_dict):
        """ Play the intro sound.
            Check to see if a card has been inserted.
            If so, change the game state.
        """

        if input_dict['card_state']:
            self.card_str = input_dict['card_str']
            self.play_sound('cardinserted', self.standard_sfx, wait=True) # we need to rename this sound effect.  Just call it beep.
            self.play_sound('press_dots',self.game_sounds, wait=True)
            self.game_state = 'game_play'
        elif self.intro_played == False:
            self.play_sound('insert_a_card', self.standard_voice)
            self.intro_played = True


    def game_play(self, cursor_button):
        """ If a button is pressed, play the sound associated with
            that button (depending on how many times it has been
            pressed in a row).
        """

        if cursor_button != None:

            if self.current_button != cursor_button:  # make own function...
                self.current_button = cursor_button
                self.press_counter = 0

            character = self.card_str[self.current_button]

            if (character == ' ') or (character == '_'):   # make own function...
                self.play_sound('wrong', self.standard_sfx)
            else:
                self.play_sound(character + str(self.press_counter), self.game_sounds)
                self.press_counter = (self.press_counter + 1) % 3

        if self.current_button == None:
            self.display_letter_prompt(' ')
        else:
            self.display_letter_prompt(self.card_str[self.current_button])
