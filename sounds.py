import os
from os.path import join
from subprocess import call
import pygame

pygame = pygame
pygame.mixer.pre_init(22050, -16,  2, 512)
pygame.mixer.init()

class sounds:
    def __init__(self,dirName):
        print('initializing') 
        self.orgDir = os.getcwd()
        self.dirName = dirName
        if not os.path.exists(self.dirName):
            os.mkdir(self.dirName)
            print('making directory {}'.format(dirName))
            self.sound_dict = {}
        else:
            print('directory exists')
            self.sound_dict = {}
            self.soundList = [x for x in os.listdir(dirName) if x[-4:].lower() == '.wav']  #list comprehension that gives makes a list of all wav files in directory
            for sound in self.soundList:
                print(sound)
                temp_sound = pygame.mixer.Sound(join(dirName,sound)) # create sound object for each wav file
                self.sound_dict[sound[:-4]] =  {'sound':temp_sound,
                                                'length':int(temp_sound.get_length() * 1000)
                                                }
