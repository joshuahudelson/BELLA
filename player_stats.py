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
                                 'Braille Tale':0,
                                 'Contraction Action':0
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
        report_card.write("REPORT CARD:\n")
        report_card.write("-----------\n")
        temp_seconds = self.loaded_stats['total_time_on_game']
        temp_minutes = int(temp_seconds/60)
        temp_seconds_remainder = temp_seconds % 60
        report_card.write("Total time spent on BELLA: " + str(temp_minutes) + " minutes and " + str(temp_seconds) + " seconds.\n")

        report_card.write("-----------\n")
        temp_Menu_seconds = self.loaded_stats['Menu']
        temp_Menu_minutes = int(temp_seconds/60)
        temp_Menu_seconds_remainder = temp_seconds % 60
        report_card.write("Menu: " + str(temp_Menu_minutes) + " minutes and " + str(temp_Menu_seconds_remainder) + " seconds.\n" )

        report_card.write("-----------\n")
        temp_AC_seconds = self.loaded_stats['Alphabet Cards']
        temp_AC_minutes = int(temp_seconds/60)
        temp_AC_seconds_remainder = temp_seconds % 60
        report_card.write("Alphabet Cards: " + str(temp_AC_minutes) + " minutes and " + str(temp_AC_seconds_remainder) + " seconds.\n" )

        report_card.write("-----------\n")
        temp_WD_seconds = self.loaded_stats['Whack-A-Dot']
        temp_WD_minutes = int(temp_seconds/60)
        temp_WD_seconds_remainder = temp_seconds % 60
        report_card.write("Whack-A-Dot: " + str(temp_WD_minutes) + " minutes and " + str(temp_WD_seconds_remainder) + " seconds.\n" )

        report_card.write("-----------\n")
        temp_BT_seconds = self.loaded_stats['Braille Tale']
        temp_BT_minutes = int(temp_seconds/60)
        temp_BT_seconds_remainder = temp_seconds % 60
        report_card.write("Braille Tale: " + str(temp_BT_minutes) + " minutes and " + str(temp_BT_seconds_remainder) + " seconds.\n" )

        report_card.write("-----------\n")
        temp_CA_seconds = self.loaded_stats['Contraction Action']
        temp_CA_minutes = int(temp_seconds/60)
        temp_CA_seconds_remainder = temp_seconds % 60
        report_card.write("Contraction Action: " + str(temp_CA_minutes) + " minutes and " + str(temp_CA_seconds_remainder) + " seconds.\n" )

        report_card.write("-----------\n")
        temp_KC_seconds = self.loaded_stats['KeyCrush']
        temp_KC_minutes = int(temp_seconds/60)
        temp_KC_seconds_remainder = temp_seconds % 60
        report_card.write("KeyCrush: " + str(temp_KC_minutes) + " minutes and " + str(temp_KC_seconds_remainder) + " seconds.\n" )

        report_card.write("Letters typed correctedly:\n")
        for key in self.loaded_stats['KC_n_l_t_correct']:
            report_card.write(key + ": " + str(self.loaded_stats['KC_n_l_t_correct'][key]) + " times.\n")
        report_card.write("Letters typed incorrectedly:\n")
        for key in self.loaded_stats['KC_n_l_t_incorrect']:
            report_card.write(key + ": " + str(self.loaded_stats['KC_n_l_t_incorrect'][key]) + " times.\n")

        report_card.write("Words typed correctedly:\n")
        for key in self.loaded_stats['KC_n_w_t_correct']:
            report_card.write(key + ": " + str(self.loaded_stats['KC_n_w_t_correct'][key]) + " times.\n")
        report_card.write("Words typed incorrectedly:\n")
        for key in self.loaded_stats['KC_n_w_t_incorrect']:
            report_card.write(key + ": " + str(self.loaded_stats['KC_n_w_t_incorrect'][key]) + " times.\n")

        report_card.write("Contractions typed correctedly:\n")
        for key in self.loaded_stats['KC_n_c_t_correct']:
            report_card.write(key + ": " + str(self.loaded_stats['KC_n_c_t_correct'][key]) + " times.\n")
        report_card.write("Contractions typed correctedly:\n")
        for key in self.loaded_stats['KC_n_c_t_incorrect']:
            report_card.write(key + ": " + str(self.loaded_stats['KC_n_c_t_incorrect'][key]) + " times.\n")

        temp_CS_seconds = self.loaded_stats['Cell Spotter']
        temp_CS_minutes = int(temp_seconds/60)
        temp_CS_seconds_remainder = temp_seconds % 60
        report_card.write("-----------\n")
        report_card.write("Cell Spotter: " + str(temp_CS_minutes) + " minutes and " + str(temp_CS_seconds_remainder) + " seconds.\n" )

        report_card.write("Letters read correctedly:\n")
        for key in self.loaded_stats['CS_n_l_t_correct']:
            report_card.write(key + ": " + str(self.loaded_stats['CS_n_l_t_correct'][key]) + " times.\n")
        report_card.write("Letters read incorrectedly:\n")
        for key in self.loaded_stats['CS_n_l_t_incorrect']:
            report_card.write(key + ": " + str(self.loaded_stats['CS_n_l_t_incorrect'][key]) + " times.\n")

        report_card.write("Words read correctedly:\n")
        for key in self.loaded_stats['CS_n_w_t_correct']:
            report_card.write(key + ": " + str(self.loaded_stats['CS_n_w_t_correct'][key]) + " times.\n")
        report_card.write("Words read incorrectedly:\n")
        for key in self.loaded_stats['CS_n_w_t_incorrect']:
            report_card.write(key + ": " + str(self.loaded_stats['CS_n_w_t_incorrect'][key]) + " times.\n")

        report_card.write("Contractions read correctedly:\n")
        for key in self.loaded_stats['CS_n_c_t_correct']:
            report_card.write(key + ": " + str(self.loaded_stats['CS_n_c_t_correct'][key]) + " times.\n")
        report_card.write("Contractions read incorrectedly:\n")
        for key in self.loaded_stats['CS_n_c_t_incorrect']:
            report_card.write(key + ": " + str(self.loaded_stats['CS_n_c_t_incorrect'][key]) + " times.\n")
