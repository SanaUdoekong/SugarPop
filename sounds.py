import pygame.mixer

from settings import SND_FOLDER, SOUNDS



class Sound:
    def __init__(self):
        """ 
        Initialize the sound class that plays sound files
        from a dictionary containing file names
        """
        pygame.mixer.init()
        pygame.mixer.set_num_channels(8)
        self.sounds = SOUNDS
    
   
    def play (self, snd):
        """
        Play a sound
        
        :param snd: gets the file name and channel for the sound to be played
        """

        sound = pygame.mixer.Sound(SND_FOLDER + self.sounds[snd][0])
        pygame.mixer.Channel(self.sounds[snd][1]).play(sound)


    def play_bg(self, bg):

        """ Implement a function to continuosly play bg music"""
        sound = pygame.mixer.Sound(SND_FOLDER + self.sounds[bg][0])
        pygame.mixer.Channel(self.sounds[bg][1]).play(sound, -1)

