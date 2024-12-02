import pygame.mixer

from settings import SND_FOLDER



class Sound:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {'background': 'background.mp3', 'explosion': 'explosion.mp3',
                       'lvl_complete': 'complete_lvl.mp3', 'add_sugar': 'sugar_drop.mp3',
                       }
    
    def load_bg(self):
        pygame.mixer.music.load(SND_FOLDER + self.sounds['background'])
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)

    def pause_bg(self):
        pygame.mixer.music.pause()
    
    def unpause_bg(self):
        pygame.mixer.music.unpause()

    def play (self, snd):
        sound = pygame.mixer.Sound(SND_FOLDER + self.sounds[snd])
        sound.play()