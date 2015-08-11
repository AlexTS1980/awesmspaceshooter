'''
Created on May 17, 2015

@author: Morgan aka Alex
mwahaha
'''
from operator import add

from pygame import sprite
import pygame
import numpy as np

import main_functions as mf

SCREEN_SIZE = [1024, 544]
GRID = (32, 32)
GRID_SIZE = [SCREEN_SIZE[0] // GRID[0], SCREEN_SIZE[1] // GRID[1]]


class Asteroids(sprite.Sprite):
    def __init__(self, loc):
        sprite.Sprite.__init__(self)

        self.loc = loc
        self.angle = 1
        self.image = pygame.image.load("asteroid1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, GRID)
        self.rect = self.image.get_rect()
        (self.rect.x, self.rect.y) = self.loc


class WeakEnemy(sprite.Sprite):
    '''
    classdocs
    '''

    # loc:true location
    def __init__(self, loc, grid_loc):
        '''
        Constructor
        '''
        sprite.Sprite.__init__(self)
        self.loc = loc
        self.angle = 1
        self.image = pygame.image.load("bad_guy_1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, GRID)
        self.rect = self.image.get_rect()
        (self.rect.x, self.rect.y) = self.loc
        self.health = 1
        self.grid_loc = grid_loc
        self.step = 1
        self.path = []
        self.true_path = []
        self.done = False
        self.now_move_laser = False
        self.animate_nme_laser = False
        self.done_moving_laser = False
        self.target_pos = (0, 0)
        self.dy, self.dx = self.loc
        self.half_grid = [x // 2 for x in GRID]
        print(self.half_grid)

    def move_enemy(self, move_pts):
        self.rect.move_ip(move_pts[0], move_pts[1])

    def init_laser(self, fighter_loc):
        self.enemy_laser_image = pygame.transform.scale(pygame.image.load("laser_charge_nme.png").convert_alpha(),
                                                        (GRID[0] // 2, GRID[1]))

        # self.enemy_laser_rect = self.enemy_laser_image.get_rect()
        self.clock_enemy_laser = pygame.time.Clock()
        self.target_pos = np.dot(fighter_loc, GRID[0])
        self.target_pos = list(map(add, self.target_pos, self.half_grid))
        self.dy, self.dx = -self.target_pos[1] + self.rect.y + GRID[1] // 2, self.target_pos[0] - self.rect.x - GRID[
            0] // 2
        self.rot_angle = 0
        if self.dx:
            self.rot_angle = np.arctan(self.dy / self.dx) * 180 / np.pi
            #print('vvv', self.rot_angle)
        else:
            self.rot_angle = 0
        # get the correct angle to rotate the laser
        self.true_rot_angle = 0
        if self.target_pos[0] > self.rect.x + GRID[0] // 2:
            self.true_rot_angle = self.rot_angle - 90
        elif self.target_pos[0] < self.rect.x + GRID[0] // 2:
            self.true_rot_angle = self.rot_angle + 90
        else:
            self.true_rot_angle = 180

        self.enemy_laser_image = pygame.transform.rotate(self.enemy_laser_image, self.true_rot_angle)
        self.enemy_laser_rect = self.enemy_laser_image.get_rect()
        self.enemy_laser_rect.x, self.enemy_laser_rect.y = self.rect.x + GRID[0] // 2, self.rect.y + GRID[1] // 2
        #print(self.rot_angle, self.true_rot_angle, self.dy, self.dx, self.target_pos, self.enemy_laser_rect.x,
        #      self.enemy_laser_rect.y)

    def move_laser(self, FPS, which_screen, time):
        # self.time = self.clock_enemy_laser.tick(FPS)
        # print(self.enemy_laser_rect.x, self.enemy_laser_rect.y, 'bebebebe', self.dx, self.dy, self.target_pos,
        #     time / 100)
        self.new_pos = mf.get_pos([self.enemy_laser_rect.x, self.enemy_laser_rect.y], self.target_pos, self.dx, self.dy,
                                  time / 500)
        self.dy, self.dx = self.target_pos[1] - self.enemy_laser_rect.y, self.target_pos[0] - self.enemy_laser_rect.x
        mf.draw_missile(self.enemy_laser_image, self.new_pos, which_screen)
        self.enemy_laser_rect.x, self.enemy_laser_rect.y = self.new_pos
