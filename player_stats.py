import pickle
import os

class player_stats:

    def __init__(self):

        self.loaded_stats = {}

    def load_stats(self, filename):

        if os.path.isfile('filename'):
            self.loaded_stats = pickle.load(open(filename, 'rb'))
        else:
            self.loaded_stats = {'total_time_on_game':0,
                                 'KC_n_l_t_correct':{},
                                 'KC_n_l_t_incorrect':{},
                                 'KC_n_w_t_correct':{},
                                 'KC_n_w_t_incorrect':{},
                                 'KC_n_c_t_correct':{},
                                 'KC_n_c_t_incorrect':{},
                                 'KeyCrush':0,
                                 'CS_n_l_t_correct':{},
                                 'CS_n_l_t_incorrect':{},
                                 'CS_n_w_t_correct':{},
                                 'CS_n_w_t_incorrect':{},
                                 'CS_n_c_t_correct':{},
                                 'CS_n_c_t_incorrect':{},
                                 'Cell Spotter':0,
                                 'Menu':0,
                                 'Alphabet Cards':0,
                                 'Whack-A-Dot':0,
                                 'Braille Tale':0
                                 }

    def save_stats(self, filename):
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

    def make_report_card(self, filename):
        report_card = open("report_card.txt", 'w')
        for key in self.loaded_stats:
            report_card.write(str(key) + ": " + str(self.loaded_stats[key]) + "\n")
