'''
Created on May 17, 2015

@author: Morganochka 
'''
import pygame
from pygame import sprite


class Spacecraft(sprite.Sprite):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        sprite.Sprite.__init__(self)

        self.image = pygame.image.load("fighter.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()

    def set_pos(self, pos):
        self.rect.x, self.rect.y = pos

    def move_fighter(self, direct):

        if direct == 'left' and self.rect.x > 0:
            self.rect.x -= 32
        elif direct == 'right' and self.rect.x < 1024 - 32:
            self.rect.x += 32
        elif direct == 'up' and self.rect.y > 0:
            self.rect.y -= 32
        elif direct == 'down' and self.rect.y < 512 - 32:
            self.rect.y += 32

    def rotate_fighter(self, direct):

        if direct == 'left':
            self.image = pygame.transform.rotate(self.image, -90)
        elif direct == 'right':
            self.image = pygame.transform.rotate(self.image, 90)
        elif direct == 'up':
            self.image = pygame.transform.rotate(self.image, 180)
