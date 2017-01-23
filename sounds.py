import os
from os.path import join
from subprocess import call


class sounds:
    
    def __init__(self):
        pass

    def make_sound_dictionary(self, dirName, pygame):
        self.orgDir = os.getcwd()
        self.dirName = dirName
        self.pygame = pygame
        
        self.sound_dict = {}

        self.soundList = [x for x in os.listdir(dirName) if x[-4:].lower() == '.wav']  #list comprehension that gives makes a list of all wav files in directory
        for sound in self.soundList:
            #print(sound)
            temp_sound = pygame.mixer.Sound(join(dirName,sound)) # create sound object for each wav file
            self.sound_dict[sound[:-4]] =  {'sound':temp_sound,
                                            'length':int(temp_sound.get_length() * 1000)
                                            }
        return self.sound_dict
