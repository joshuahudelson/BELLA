import pickle
import os

class player_stats:

    def __init__(self):

        self.loaded_stats = {}
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"

        self.total_time_on_game = 0

        self.KeyCrush_num_letters_typed_correctly = {}
        self.KeyCrush_num_letters_typed_incorrectly = {}
        self.KeyCrush_num_words_typed_correctly = {}
        self.KeyCrush_num_words_typed_incorrectly = {}
        self.KeyCrush_num_contractions_typed_correctly = {}
        self.KeyCrush_num_contractions_typed_incorrectly = {}
        self.KeyCrush_time_on_game = 0

        self.Cell_Spotter_num_letters_read_correctly = {}
        self.Cell_Spotter_num_letters_read_incorrectly = {}
        self.Cell_Spotter_num_words_read_correctly = {}
        self.Cell_Spotter_num_words_read_incorrectly = {}
        self.Cell_Spotter_num_contractions_read_correctly = {}
        self.Cell_Spotter_num_contractions_read_incorrectly = {}
        self.Cell_Spotter_time_on_game = 0


    def load_stats(self, filename):

        if os.path.isfile('filename'):

            self.loaded_stats = pickle.load(open(filename, 'rb'))

            self.total_time_on_game = self.loaded_stats['total_time_on_game']

            self.KeyCrush_num_letters_typed_correctly = self.loaded_stats['KC_n_l_t_correct']
            self.KeyCrush_num_letters_typed_incorrectly = self.loaded_stats['KC_n_l_t_incorrect']
            self.KeyCrush_num_words_typed_correctly = self.loaded_stats['KC_n_w_t_correct']
            self.KeyCrush_num_words_typed_incorrectly = self.loaded_stats['KC_n_w_t_incorrect']
            self.KeyCrush_num_contractions_typed_correctly = self.loaded_stats['KC_n_c_t_correct']
            self.KeyCrush_num_contractions_typed_incorrectly = self.loaded_stats['KC_n_c_t_incorrect']
            self.KeyCrush_time_on_game = self.loaded_stats['KeyCrush']

            self.Cell_Spotter_num_letters_read_correctly = self.loaded_stats['CS_n_l_t_correct']
            self.Cell_Spotter_num_letters_read_incorrectly = self.loaded_stats['CS_n_l_t_incorrect']
            self.Cell_Spotter_num_words_read_correctly = self.loaded_stats['CS_n_w_t_correct']
            self.Cell_Spotter_num_letters_read_incorrectly = self.loaded_stats['CS_n_w_t_incorrect']
            self.Cell_Spotter_num_contractions_read_correctly = self.loaded_stats['CS_n_c_t_correct']
            self.Cell_Spotter_num_contractions_read_incorrectly = self.loaded_stats['CS_n_c_t_incorrect']
            self.Cell_Spotter_time_on_game = self.loaded_stats['Cell Spotter']


    def save_stats(self, filename):

        self.loaded_stats['total_time_on_game'] = self.total_time_on_game

        self.loaded_stats['KC_n_l_t_correct'] = self.KeyCrush_num_letters_typed_correctly
        self.loaded_stats['KC_n_l_t_incorrect'] = self.KeyCrush_num_letters_typed_incorrectly
        self.loaded_stats['KC_n_w_t_correct'] = self.KeyCrush_num_words_typed_correctly
        self.loaded_stats['KC_n_w_t_incorrect'] = self.KeyCrush_num_words_typed_incorrectly
        self.loaded_stats['KC_n_c_t_correct'] = self.KeyCrush_num_contractions_typed_correctly
        self.loaded_stats['KC_n_c_t_incorrect'] = self.KeyCrush_num_contractions_typed_incorrectly
        self.loaded_stats['KeyCrush'] = self.KeyCrush_time_on_game

        self.loaded_stats['CS_n_l_t_correct'] = self.Cell_Spotter_num_letters_read_correctly
        self.loaded_stats['CS_n_l_t_incorrect'] = self.Cell_Spotter_num_letters_read_incorrectly
        self.loaded_stats['CS_n_w_t_correct'] = self.Cell_Spotter_num_words_read_correctly
        self.loaded_stats['CS_n_w_t_incorrect'] = self.Cell_Spotter_num_letters_read_incorrectly
        self.loaded_stats['CS_n_c_t_correct'] = self.Cell_Spotter_num_contractions_read_correctly
        self.loaded_stats['CS_n_c_t_incorrect'] = self.Cell_Spotter_num_contractions_read_incorrectly
        self.loaded_stats['Cell Spotter'] = self.Cell_Spotter_time_on_game

        pickle.dump(self.loaded_stats, open(filename, "wb"))


    def update_stats(self, update_dict):
        """ stat_element: 'a', 'b', 'c', 'lip', 'lap', etc. and contractions.
            stat_type: the string name of an entry (such as 'CS_n_w_t_correct')
        """
        if len(update_dict) > 0:
            if update_dict['stat_element'] not in self.loaded_stats[update_dict['stat_type']]:
                self.loaded_stats[update_dict['stat_type']][update_dict['stat_element']] = 1
            else:
                self.loaded_stats[update_dict['stat_type']][update_dict['stat_element']] += 1


    def update_time(self, time_dict):

        self.loaded_stats[time_dict['game_name']] += time_dict['time_on_game']
        self.loaded_stats['total_time_on_game'] += time_dict['time_on_game']


    def make_report_card(self):
        pass

"""
an_update = {'stat_type': 'CS_n_w_t_incorrect',
             'stat_element':'abacadabra',
             'time_game_name':'CS_t_o_game',
             'time_on_game': 123}

x = player_stats()
x.save_stats("a_pickle")
x.load_stats("a_pickle")
x.update_stats(an_update)

print(x.loaded_stats['total_time_on_game'])
"""
