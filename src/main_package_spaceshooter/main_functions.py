'''
Created on May 26, 2015

@author: Morgan
mmmm I'm not too sure tbh) 
'''
from itertools import chain

import numpy as np

import enemies
import pygame

SCREEN_SIZE = [1024, 544]
GRID = (32, 32)
GRID_SIZE = [SCREEN_SIZE[0] // GRID[0], SCREEN_SIZE[1] // GRID[1]]


def draw_missile(img, pos, surface):
    surface.blit(img, pos)


def get_pos(cur_pos, target_pos, dx, dy, time):
    new_pos = (cur_pos[0] + dx * time, cur_pos[1] + dy * time)

    return new_pos


# get admissable tiles
def get_dist_value(loc, n_steps, ast_set, enemy_set, grid_size):
    open_set = {}
    closed_set = set()
    neighbors = ((-1, 0), (0, -1), (+1, 0), (0, +1))
    open_set.update({loc: 0})
    while open_set:
        # print('aaa', open_set)
        temp_set = {}
        # loop over all tiles in the open set
        for tiles in open_set:
            end_of_line = False
            # print(tiles)
            if open_set[tiles] + 1 <= n_steps:
                for vals in neighbors:
                    tentative_tile = (tiles[0] + vals[0], tiles[1] + vals[1])
                    if tentative_tile not in ast_set and tentative_tile not in enemy_set and tentative_tile not in closed_set and tentative_tile not in open_set and tentative_tile not in temp_set and \
                                    tentative_tile[0] >= 0 and tentative_tile[0] < grid_size[0] and tentative_tile[
                        1] >= 0 and tentative_tile[1] <= grid_size[1] - 2 and tentative_tile != loc:
                        temp_set.update({tentative_tile: open_set[tiles] + 1})
                    else:
                        pass
            else:
                end_of_line = True
                # print('aaa', tiles)
                closed_set.add(tiles)

            if not end_of_line and tiles != loc:
                closed_set.add(tiles)

        open_set = temp_set

    return closed_set


# A* for the enemies
# start: enemy start loc
# end: spaceship loc
def astar(start, end, ast_set, nme_set):
    # print(start, end, 'sss')
    NEIGHBOURS = ((-1, 0), (0, -1), (+1, 0), (0, +1))
    # store the tree
    full_tree = {}
    # store the f-values
    open_set = set()
    g_score = {}
    f_score = {}
    closed_set = set()
    dist = abs(start[0] - end[0]) + abs(start[1] - end[1])
    g_score[start] = 0
    f_score[start] = g_score[start] + dist
    open_set.add(start)
    while open_set:
        current_best = min(f_score, key=f_score.get)
        if current_best == end:
            return reconstruct_path(full_tree, end, start)
        else:
            # print(start, open_set,'ddd')
            open_set.remove(current_best)
            closed_set.add(current_best)
            del f_score[current_best]
            for add_vals in NEIGHBOURS:
                vals = (current_best[0] + add_vals[0], current_best[1] + add_vals[1])
                if vals in closed_set or vals in nme_set or vals in ast_set or vals[0] < 0 or vals[1] < 0 or vals[0] > \
                                GRID_SIZE[0] - 1 or vals[1] > GRID_SIZE[1] - 2:
                    pass
                else:
                    new_g_score = g_score[current_best] + 1
                    if vals not in open_set or g_score[vals] > new_g_score:
                        full_tree[vals] = current_best
                        g_score[vals] = new_g_score
                        f_score[vals] = g_score[vals] + abs(vals[0] - end[0]) + abs(vals[1] - end[1])
                        if vals not in open_set:
                            open_set.add(vals)
    return None


def reconstruct_path(full_tree, end, start):
    full_path = []
    full_path.append(end)
    while end in full_tree:
        # print(full_tree[end], 'end')
        full_path.append(full_tree[end])
        end = full_tree[end]

    # print(full_path)
    return full_path[::-1]


def truncline(text, font, maxwidth):
    real = len(text)
    stext = text
    l = font.size(text)[0]
    cut = 0
    a = 0
    done = 1
    old = None
    while l > maxwidth:
        a = a + 1
        n = text.rsplit(None, a)[0]
        if stext == n:
            cut += 1
            stext = n[:-cut]
        else:
            stext = n
        l = font.size(stext)[0]
        real = len(stext)
        done = 0
    return real, done, stext


def wrapline(text, font, maxwidth):
    done = 0
    wrapped = []

    while not done:
        nl, done, stext = truncline(text, font, maxwidth)
        wrapped.append(stext.strip())
        text = text[nl:]
    return wrapped


def wrap_multi_line(text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)


def setup_asteroids(num_ast, asteroid_set, AROUND, asteroids):
    for vals in range(num_ast):
        if not asteroid_set:
            loc = (np.random.randint(0, GRID_SIZE[0] - 1), np.random.randint(0, GRID_SIZE[1] - 2))
            asteroid_set.add(loc)
            true_loc = np.dot(loc, 32)
            ast = enemies.Asteroids(true_loc)
            asteroids.add(ast)
        else:
            while (True):
                this_bad = False
                loc = (np.random.randint(0, GRID_SIZE[0] - 1), np.random.randint(0, GRID_SIZE[1] - 2))
                for neighbours in AROUND:
                    this_pos = (loc[0] + neighbours[0], loc[1] + neighbours[1])
                    if this_pos in asteroid_set:
                        this_bad = True
                        break
                if not this_bad:
                    asteroid_set.add(loc)
                    true_loc = np.dot(loc, 32)
                    ast = enemies.Asteroids(true_loc)
                    asteroids.add(ast)
                    break


def setup_fighter(asteroid_set, fighter):
    while (True):
        good_pos = True
        loc = (np.random.randint(0, GRID_SIZE[0] - 1), np.random.randint(0, GRID_SIZE[1] - 2))

        if loc in asteroid_set:
            good_pos = False

        # if this location is legitimate (i.e. no asteroids)
        if good_pos:
            true_loc = np.dot(loc, 32)
            fighter.set_pos(true_loc)
            fighter_loc = loc
            break

    return fighter_loc


def setup_enemies(enemy_num, weak_enemy_set, asteroid_set, fighter_loc, weak_enemy_group):
    for enemy_loc in range(enemy_num):

        while (True):

            loc = (np.random.randint(0, GRID_SIZE[0] - 1), np.random.randint(0, GRID_SIZE[1] - 2))
            if loc not in asteroid_set and loc != fighter_loc:
                weak_enemy_set.add(loc)
                true_loc = np.dot(loc, GRID_SIZE[0])
                weak_enemy = enemies.WeakEnemy(true_loc, loc)
                weak_enemy_group.add(weak_enemy)
                break


def get_full_path(path, step_size):
    full_path = []
    step = 0

    # so diff can be something like (32,0)..(0,-32) and so on
    while step < len(path) - 1:
        diff = np.dot((path[step + 1][0] - path[step][0], path[step + 1][1] - path[step][1]), GRID_SIZE[0])
        while diff[0] or diff[1]:
            # print(path[step+1],step, len(path), diff,'rrr')
            # reduce the distance the the next step
            full_path.append((np.sign(diff[0]) * step_size, np.sign(diff[1]) * step_size))
            diff[0] += -np.sign(diff[0]) * step_size
            diff[1] += -np.sign(diff[1]) * step_size

        step += 1

    # print(full_path)
    return full_path

def play_sound(sound):
    sound.play()
