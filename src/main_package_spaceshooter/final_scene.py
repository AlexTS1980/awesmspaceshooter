'''
Created on Jun 14, 2015

@author: Morgan
'''
import pygame


class FinalScene(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.bgr_image = pygame.image.load("final_scene.png").convert_alpha()
        self.main_text = pygame.font.Font(None, 32)
        self.text_win = "Well done dude, go get some beer from the fridge!"
        self.text_lose = "Sorry dude you lost!"
        self.wanna_play_again = "Wanna play again, Y/N ?"

    def display_final_scene(self, nsteps, which_screen, outcome, screen_size):

        which_screen.blit(self.bgr_image, (0, 0))

        if outcome:
            which_screen.blit(self.main_text.render(self.text_win, True, (0, 255, 255), None),
                              (screen_size[0] / 2 - self.main_text.size(self.text_win)[0] / 2, screen_size[1] / 2))
        else:
            which_screen.blit(self.main_text.render(self.text_lose, True, (0, 255, 255), None),
                              (screen_size[0] / 2 - self.main_text.size(self.text_lose)[0] / 2, screen_size[1] / 2))

        which_screen.blit(self.main_text.render(self.wanna_play_again, True, (0, 255, 255), None),
                          (screen_size[0] / 2 - self.main_text.size(self.wanna_play_again)[0] / 2,
                          screen_size[1] / 2 + self.main_text.size(self.text_win)[1]))
