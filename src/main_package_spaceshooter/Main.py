'''
Created on May 16, 2015

@author: Morgan
no, it's actually Alex
'''
import sys
import os

import numpy as np
import pygame




# import other modules
import craft
import main_functions as mf
import final_scene as fs

from pygame import locals

__version__ = '3.0.1'


def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    global SCREEN_SIZE
    global GRID
    global launch

    SCREEN_SIZE = [1024, 544]
    GRID = (32, 32)
    GRID_SIZE = [SCREEN_SIZE[0] // GRID[0], SCREEN_SIZE[1] // GRID[1]]
    launch = True
    FPS = 60
    pygame.init()
    pygame.RESIZABLE = False
    pygame.NOFRAME = False

    main_screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("A Fabulous Space Shooter v3.0.1")
    bgr_image = pygame.image.load("space-background.jpg").convert_alpha()
    target_image = pygame.transform.scale(pygame.image.load("target.png").convert_alpha(), GRID)
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
    laser_sound = pygame.mixer.Sound("183871__m-red__phasingbeam03.wav")
    laser_sound.set_volume(0.1)
    missile_sound = pygame.mixer.Sound("157439__nengisuls__misslie-1.wav")
    missile_sound.set_volume(0.1)
    button_sound = pygame.mixer.Sound("269504__michorvath__button-click.wav")
    fighter_sound = pygame.mixer.Sound("255202__michael-kur95__starship-01.wav")
    # start screen
    start_screen = True
    info_screen = False
    info_screen_2 = False
    start_screen_bg = pygame.image.load("night_sky-1523052.jpg").convert_alpha()
    red_button = pygame.image.load("red_button.jpg").convert_alpha()
    # selection screen
    selection_screen = False
    asteroid_num = 10
    weak_enemy_num = 3
    laser_shots = 3
    missile_shots = 1
    blue_space = pygame.image.load("blue_button.jpg").convert_alpha()
    up_button = pygame.transform.scale(pygame.image.load("up_arrow.png").convert_alpha(), blue_space.get_size())
    down_button = pygame.transform.scale(pygame.image.load("down_arrow.png").convert_alpha(), blue_space.get_size())
    keypad = pygame.transform.scale(pygame.image.load("keypad.png").convert_alpha(), (150, 100))
    list_of_choices = ["Hit Points", "Enemies", "Missiles", "Laser charges", "Asteroids"]
    hit_points_select = "Hit points"
    laser_select = "Laser charges"
    missile_select = "Missiles"
    # main screen
    main_game = False
    weak_enemy_move_range = 5
    step_size = 4
    weak_enemy_set = set()
    asteroid_set = set()
    asteroids = pygame.sprite.RenderPlain()
    fighter_group = pygame.sprite.RenderPlain()
    weak_enemy_group = pygame.sprite.RenderPlain()
    # movement
    move_points = 3
    move = False
    nturns = 0
    # turns
    char_move = False
    char_shoot = False
    enemy_move_calc = False
    enemy_move = False
    enemy_shoot = False
    # shooting
    animate_enemy_missile = False
    animate_missile = False
    laser_was_discharged = False
    enemy_was_hit = False
    # text-info
    start_game_txt = "Start Game"
    pars_game_txt = "Select parameters"
    controls_game_txt = "Controls"
    info_game_txt = "Get Info"
    quit_game_txt = "Quit"
    info_txt = "Game designed by Alex Ter-Sarkisov in Python w/Pygame. No proprietary assets used. A* Algorithm used for pathfinding."
    info_txt_2 = "Your galaxy is under attack! Aliens pretending to be sprites from the 80s have launched an offensive against your peaceful homeworld intending to enslave your race and lay their dirty greedy pincers on your natural resources! Strike back and show these invaders who is the true master of war! It's the question of life and death!"
    info_txt_3 = "...oh, by the way, if you lose, mom wil be very, very angry with ya! So don't disappoint us!"
    main_title = "Fabulous Space Shooter"
    return_title = "Return"
    move_info = "Move the ship"
    lmb_info = "Left Mouse Button"
    lmb_info_ex = "Discharge Laser Cannon (weak)"
    rmb_info = "Right Mouse Button"
    rmb_info_ex = "Fire Missile (strong)"
    spacebar_info = "Spacebar"
    spacebar_info_ex = "Skip turn"
    hp_text = "Hit Points:"
    move_txt = "Move!"
    shoot_txt = "Shoot!"
    hp_val = 10
    title_font_object = pygame.font.Font(None, 64)
    hp_object = pygame.font.Font(None, 32)
    hp_hit_object = pygame.font.Font(None, 24)
    hp_text_loc = [0, GRID_SIZE[1] * 32 - 23]
    mv_points_text = "Movement Points:"
    fps_text = "FPS:"
    laser_shots_text = "Laser charges:"
    missiles_text = 'Missiles:'
    just_started = True
    # final scene
    final_scene_show = False
    f_scene = fs.FinalScene()
    success_in_game = False
    # clock
    clock_this_game = pygame.time.Clock()
    AROUND = ((-1, 0), (-1, -1), (-1, 1), (+1, 0), (+1, +1), (0, +1), (-1, +1), (0, -1))
    main_vals = [hp_val, weak_enemy_num, missile_shots, laser_shots, asteroid_num]
    min_vals = [1, 1, 0, 1, 0]
    max_vals = [15, 15, 5, 10, 15]
    init_vals = [10, 3, 1, 3, 10]
    b_coords = (0, 2, 3, 5, 6, 8, 9, 11, 12, 14)
    button_coords = []
    # fighter_loc = ()
    for c in b_coords:
        button_coords.append((SCREEN_SIZE[0] / 2 - blue_space.get_width() / 2, c * blue_space.get_height()))

    while launch:
        # launch the game
        pygame.display.update()
        # loop through events
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                launch = False
                sys.exit()
            elif events.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                if start_screen:
                    # start game
                    if SCREEN_SIZE[0] / 2 - red_button.get_width() / 2 < click[0] < SCREEN_SIZE[
                        0] / 2 - red_button.get_width() / 2 + red_button.get_width() and SCREEN_SIZE[1] / 4 < click[1] < \
                                            SCREEN_SIZE[1] / 4 + red_button.get_height():
                        mf.play_sound(button_sound)
                        start_screen = False
                        selection_screen = True
                    # info screen
                    elif SCREEN_SIZE[0] / 2 - red_button.get_width() / 2 < click[0] < SCREEN_SIZE[
                        0] / 2 - red_button.get_width() / 2 + red_button.get_width() and SCREEN_SIZE[1] / 2 < click[1] < \
                                            SCREEN_SIZE[1] / 2 + red_button.get_height():
                        mf.play_sound(button_sound)
                        start_screen = False
                        info_screen = True
                        info_split_txt = mf.wrapline(info_txt, hp_object, 500)
                        info_split_txt_2 = mf.wrapline(info_txt_2, hp_object, 500)
                        info_split_txt_3 = mf.wrapline(info_txt_3, hp_object, 500)

                    elif SCREEN_SIZE[0] / 2 - red_button.get_width() / 2 < click[0] < SCREEN_SIZE[
                        0] / 2 - red_button.get_width() / 2 + red_button.get_width() and SCREEN_SIZE[1] * 3 / 4 < click[
                        1] < SCREEN_SIZE[1] * 3 / 4 + red_button.get_height():
                        mf.play_sound(button_sound)
                        launch = False
                        sys.exit()

                elif info_screen:
                    if SCREEN_SIZE[0] / 2 - red_button.get_width() / 2 < click[0] < SCREEN_SIZE[
                        0] / 2 - red_button.get_width() / 2 + red_button.get_width() and SCREEN_SIZE[
                        1] - 2 * red_button.get_height() < click[1] < SCREEN_SIZE[
                        1] - 2 * red_button.get_height() + red_button.get_height():
                        mf.play_sound(button_sound)
                        info_screen = False
                        start_screen = True

                elif selection_screen:
                    # change parameter values
                    # I'm so damn cooooool!!!
                    for idx, coords in enumerate(button_coords):
                        if coords[0] < click[0] < coords[0] + blue_space.get_width() and coords[1] < click[1] < coords[
                            1] + blue_space.get_height():
                            # increase

                            if not idx % 2 and main_vals[idx // 2] < max_vals[idx % 2]:
                                main_vals[idx // 2] += 1
                                mf.play_sound(button_sound)
                            elif idx % 2 and main_vals[(idx - 1) // 2] > min_vals[(idx - 1) // 2]:
                                main_vals[(idx - 1) // 2] -= 1
                                mf.play_sound(button_sound)

                    # get the next screen - game instructions
                    if SCREEN_SIZE[0] / 2 - red_button.get_width() / 2 < click[0] < SCREEN_SIZE[
                        0] / 2 - red_button.get_width() / 2 + red_button.get_width() and SCREEN_SIZE[
                        1] - 1.5 * red_button.get_height() < click[1] < SCREEN_SIZE[1] - .5 * red_button.get_height():
                        user_set_missile_value = main_vals[2]
                        user_set_laser_value = main_vals[3]
                        mf.play_sound(button_sound)
                        selection_screen = False
                        info_screen_2 = True

                elif info_screen_2:
                    if SCREEN_SIZE[0] / 2 - red_button.get_width() / 2 < click[0] < SCREEN_SIZE[
                        0] / 2 - red_button.get_width() / 2 + red_button.get_width() and SCREEN_SIZE[
                        1] - 1.5 * red_button.get_height() < click[1] < SCREEN_SIZE[1] - .5 * red_button.get_height():
                        # asteroids locations
                        mf.setup_asteroids(main_vals[4], asteroid_set, AROUND, asteroids)
                        # now create and position the fighter
                        fighter = craft.Spacecraft()
                        fighter_group.add(fighter)
                        fighter_loc = mf.setup_fighter(asteroid_set, fighter)
                        # starting locations for enemies
                        enemy_num = main_vals[1]
                        mf.setup_enemies(enemy_num, weak_enemy_set, asteroid_set, fighter_loc, weak_enemy_group)
                        mf.play_sound(button_sound)
                        info_screen_2 = False
                        main_game = True
                        char_move = True
                # what happens when the player shoots
                if char_shoot:
                    # target_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) 
                    source_pos = np.dot(fighter_loc, GRID[0])
                    dy = -(click[1] - source_pos[1])
                    dx = click[0] - source_pos[0]
                    rot_angle = np.arctan(dy / dx) * 180 / np.pi
                    # print (rot_angle*180/np.pi) 
                    true_rot_angle = 0
                    if click[0] > source_pos[0]:
                        true_rot_angle = -90 + rot_angle
                    else:
                        true_rot_angle = 90 + rot_angle

                    if events.button == 1 and main_vals[3] > 0:
                        main_vals[3] -= 1
                        mf.play_sound(laser_sound)
                        laser_image = pygame.transform.scale(pygame.image.load("laser_charge.png").convert_alpha(),
                                                             (GRID[0], GRID[1]))
                        laser_was_discharged = True
                        clock_this_missile = pygame.time.Clock()
                        laser_image = pygame.transform.rotate(laser_image, true_rot_angle)
                        laser_rect = laser_image.get_rect()

                    elif events.button == 3 and main_vals[2] > 0:
                        mf.play_sound(missile_sound)
                        missile_image = pygame.transform.scale(pygame.image.load("missile.png").convert_alpha(),
                                                               (GRID[0] // 2, GRID[1]))
                        animate_missile = True
                        main_vals[2] -= 1
                        clock_this_missile = pygame.time.Clock()
                        missile_image = pygame.transform.rotate(missile_image, true_rot_angle)
                        missile_rect = missile_image.get_rect()

            elif events.type == pygame.KEYDOWN:

                if events.key == locals.K_ESCAPE:
                    launch = False
                    sys.exit()

                if char_move:

                    if events.key == locals.K_LEFT and (fighter_loc[0] - 1, fighter_loc[1]) not in asteroid_set and (
                                fighter_loc[0] - 1, fighter_loc[1]) not in weak_enemy_set and fighter_loc[0] - 1 >= 0:
                        move = True
                        fighter.move_fighter('left')
                        fighter_loc = (fighter_loc[0] - 1, fighter_loc[1])
                        move_points -= 1


                    elif events.key == locals.K_RIGHT and (fighter_loc[0] + 1, fighter_loc[1]) not in asteroid_set and (
                                fighter_loc[0] + 1, fighter_loc[1]) not in weak_enemy_set and fighter_loc[0] + 1 <= \
                                    GRID_SIZE[
                                        0] - 1:
                        move = True
                        fighter.move_fighter('right')
                        fighter_loc = (fighter_loc[0] + 1, fighter_loc[1])
                        move_points -= 1


                    elif events.key == locals.K_UP and (fighter_loc[0], fighter_loc[1] - 1) not in asteroid_set and (
                            fighter_loc[0], fighter_loc[1] - 1) not in weak_enemy_set and fighter_loc[1] - 1 >= 0:
                        move = True
                        fighter.move_fighter('up')
                        fighter_loc = (fighter_loc[0], fighter_loc[1] - 1)
                        move_points -= 1


                    elif events.key == locals.K_DOWN and (fighter_loc[0], fighter_loc[1] + 1) not in asteroid_set and (
                            fighter_loc[0], fighter_loc[1] + 1) not in weak_enemy_set and fighter_loc[1] + 1 <= \
                                    GRID_SIZE[
                                        1] - 2:
                        move = True
                        fighter.move_fighter('down')
                        fighter_loc = (fighter_loc[0], fighter_loc[1] + 1)
                        move_points -= 1

                    if move:
                        mf.play_sound(fighter_sound)
                        access_set = mf.get_dist_value(fighter_loc, move_points, asteroid_set, weak_enemy_set,
                                                       GRID_SIZE)
                        move = False

                    if not move_points:
                        char_move = False
                        char_shoot = True

                if events.key == locals.K_SPACE:

                    if char_move:
                        char_shoot = True
                        char_move = False
                        move_points = 0

                    elif char_shoot:
                        main_vals[3] = 0
                        main_vals[2] = 0
                        char_shoot = False
                        enemy_move_calc = True

                if events.key == locals.K_y:
                    if final_scene_show:
                        just_started = True
                        final_scene_show = False
                        success_in_game = False
                        main_game = False
                        start_screen = True
                        pygame.mouse.set_visible(True)
                        weak_enemy_set = set()
                        asteroid_set = set()
                        fighter = craft.Spacecraft()
                        asteroids = pygame.sprite.RenderPlain()
                        fighter_group = pygame.sprite.RenderPlain()
                        weak_enemy_group = pygame.sprite.RenderPlain()

                if events.key == locals.K_n:
                    if final_scene_show:
                        launch = False
                        sys.exit()

        clock_this_game.tick(FPS)
        # intro screen
        if start_screen:
            main_screen.blit(start_screen_bg, (0, 0))
            # buttons and text
            main_screen.blit(title_font_object.render(main_title.upper(), 1, (0, 255, 0), None), (
                SCREEN_SIZE[0] / 2 - title_font_object.size(main_title.upper())[0] / 2, SCREEN_SIZE[1] / 8))
            main_screen.blit(hp_object.render("Version" + str(__version__), 1, (0, 255, 0), None), (
                SCREEN_SIZE[0] / 2 - title_font_object.size(main_title.upper())[0] / 2 +
                title_font_object.size(main_title.upper())[0] + 10,
                SCREEN_SIZE[1] / 8 + title_font_object.size(main_title.upper())[1] / 4))
            main_screen.blit(red_button, (SCREEN_SIZE[0] / 2 - red_button.get_width() / 2, SCREEN_SIZE[1] / 4))
            main_screen.blit(red_button, (SCREEN_SIZE[0] / 2 - red_button.get_width() / 2, SCREEN_SIZE[1] / 2))
            main_screen.blit(red_button, (SCREEN_SIZE[0] / 2 - red_button.get_width() / 2, SCREEN_SIZE[1] * 3 / 4))
            main_screen.blit(hp_object.render(start_game_txt.upper(), 1, (0, 255, 255), None), (
                SCREEN_SIZE[0] / 2 - red_button.get_width() / 2 + hp_object.size(start_game_txt)[0] / 10,
                SCREEN_SIZE[1] / 4 + hp_object.size(start_game_txt)[1] / 2))
            main_screen.blit(hp_object.render(info_game_txt.upper(), 1, (0, 255, 255), None), (
                SCREEN_SIZE[0] / 2 - red_button.get_width() / 2 + hp_object.size(start_game_txt)[0] / 4,
                SCREEN_SIZE[1] / 2 + hp_object.size(start_game_txt)[1] / 2))
            main_screen.blit(hp_object.render(quit_game_txt.upper(), 1, (0, 255, 255), None), (
                SCREEN_SIZE[0] / 2 - red_button.get_width() / 2 + hp_object.size(start_game_txt)[0] / 2,
                SCREEN_SIZE[1] * 3 / 4 + hp_object.size(start_game_txt)[1] / 2))
        # info screen
        elif info_screen:
            main_screen.blit(start_screen_bg, (0, 0))
            for idx, txt in enumerate(info_split_txt):
                main_screen.blit(hp_object.render(txt, 1, (0, 255, 0), None), (
                    SCREEN_SIZE[0] / 2 - hp_object.size(info_split_txt[0])[0] / 2, SCREEN_SIZE[1] / 8 + idx * 20))
            for idx, txt in enumerate(info_split_txt_2):
                main_screen.blit(hp_object.render(txt, 1, (0, 255, 0), None), (
                    SCREEN_SIZE[0] / 2 - hp_object.size(info_split_txt[0])[0] / 2, SCREEN_SIZE[1] / 4 + idx * 20))
            for idx, txt in enumerate(info_split_txt_3):
                main_screen.blit(hp_object.render(txt, 1, (0, 255, 0), None), (
                    SCREEN_SIZE[0] / 2 - hp_object.size(info_split_txt[0])[0] / 2, SCREEN_SIZE[1] * 2 / 3 + idx * 20))
                # return button
            main_screen.blit(red_button, (
                SCREEN_SIZE[0] / 2 - red_button.get_width() / 2, SCREEN_SIZE[1] - 2 * red_button.get_height()))
            main_screen.blit(hp_object.render(return_title.upper(), 1, (0, 255, 255), None), (
                SCREEN_SIZE[0] / 2 - red_button.get_width() / 2 + hp_object.size(return_title)[0] / 2,
                SCREEN_SIZE[1] - 2 * red_button.get_height() + hp_object.size(return_title)[1] / 2))
        # parameter selection
        elif selection_screen:
            #print(main_vals, init_vals)
            main_screen.blit(start_screen_bg, (0, 0))
            main_screen.blit(red_button, (
                SCREEN_SIZE[0] / 2 - red_button.get_width() / 2, SCREEN_SIZE[1] - 1.5 * red_button.get_height()))
            main_screen.blit(hp_object.render(start_game_txt.upper(), 1, (0, 255, 255), None), (
                SCREEN_SIZE[0] / 2 - red_button.get_width() / 2 + hp_object.size(return_title)[0] / 6,
                SCREEN_SIZE[1] - 1.5 * red_button.get_height() + hp_object.size(return_title)[1] / 2))
            # num enemies, num asteroids, num missiles, laser charges, hit points
            num_options = 5
            for t in range(num_options):
                main_screen.blit(blue_space, (
                    SCREEN_SIZE[0] / 2 - blue_space.get_width() / 2, (3 * t + 1) * blue_space.get_height()))
                main_screen.blit(up_button,
                                 (SCREEN_SIZE[0] / 2 - up_button.get_width() / 2, 3 * t * blue_space.get_height()))
                main_screen.blit(down_button, (
                    SCREEN_SIZE[0] / 2 - down_button.get_width() / 2, (3 * t + 2) * blue_space.get_height()))

            for idx, vals in enumerate(list_of_choices):
                main_screen.blit(hp_object.render(vals.upper(), 1, (0, 255, 255), None), (
                    SCREEN_SIZE[0] / 2 - 2 * blue_space.get_width(),
                    (3 * idx + 1) * blue_space.get_height() + blue_space.get_height() / 4))

            for idx, vals in enumerate(main_vals):
                main_screen.blit(hp_object.render(str(vals), 1, (255, 255, 0), None), (
                    SCREEN_SIZE[0] / 2 - hp_object.size(str(vals))[0] / 2,
                    (3 * idx + 1) * blue_space.get_height() + blue_space.get_height() / 4))
        # instructions and game start
        elif info_screen_2:
            main_screen.blit(start_screen_bg, (0, 0))
            main_screen.blit(keypad, (50, 50))
            main_screen.blit(hp_object.render(move_info.upper(), 1, (0, 255, 0), None),
                             (SCREEN_SIZE[0] / 2, 50 + keypad.get_height() / 2))
            main_screen.blit(hp_object.render(lmb_info.upper(), 1, (0, 255, 0), None),
                             (50, 50 + keypad.get_height() + 50))
            main_screen.blit(hp_object.render(rmb_info.upper(), 1, (0, 255, 0), None),
                             (50, 50 + keypad.get_height() + 50 + hp_object.size(lmb_info)[1] + 50))
            main_screen.blit(hp_object.render(spacebar_info.upper(), 1, (0, 255, 0), None), (
                50,
                50 + keypad.get_height() + 50 + hp_object.size(lmb_info)[1] + 50 + hp_object.size(rmb_info)[1] + 50))
            main_screen.blit(hp_object.render(lmb_info_ex.upper(), 1, (0, 255, 0), None),
                             (SCREEN_SIZE[0] / 2, 50 + keypad.get_height() + 50))
            main_screen.blit(hp_object.render(rmb_info_ex.upper(), 1, (0, 255, 0), None),
                             (SCREEN_SIZE[0] / 2, 50 + keypad.get_height() + 50 + hp_object.size(lmb_info)[1] + 50))
            main_screen.blit(hp_object.render(spacebar_info_ex.upper(), 1, (0, 255, 0), None), (SCREEN_SIZE[0] / 2,
                                                                                                50 + keypad.get_height() + 50 +
                                                                                                hp_object.size(
                                                                                                    lmb_info)[1] + 50 +
                                                                                                hp_object.size(
                                                                                                    rmb_info)[1] + 50))
            main_screen.blit(red_button, (
                SCREEN_SIZE[0] / 2 - red_button.get_width() / 2, SCREEN_SIZE[1] - 1.5 * red_button.get_height()))
            main_screen.blit(hp_object.render(start_game_txt.upper(), 1, (0, 255, 255), None), (
                SCREEN_SIZE[0] / 2 - red_button.get_width() / 2 + hp_object.size(return_title)[0] / 6,
                SCREEN_SIZE[1] - 1.5 * red_button.get_height() + hp_object.size(return_title)[1] / 2))

        elif main_game:
            # print(asteroid_set)        
            main_screen.blit(start_screen_bg, (0, 0))
            # print('beebe')
            # player's turn-move
            if char_move:
                if just_started:
                    # print('ddd', fighter_loc)
                    access_set = mf.get_dist_value(fighter_loc, move_points, asteroid_set, weak_enemy_set, GRID_SIZE)
                    timer_move_txt = clock_this_game.tick(60)
                    time_move = 0
                    just_started = False

                # draw dots on accessible tiles
                for vals in access_set:
                    pygame.draw.circle(main_screen, (0, 255, 0), np.dot(vals, 32) + (16, 16), 5, 0)

                    # text update
            main_screen.blit(hp_object.render(hp_text, 1, (0, 255, 255), None), hp_text_loc)
            main_screen.blit(hp_object.render(str(main_vals[0]), 1, (255, 255, 255), None),
                             [hp_object.size(hp_text)[0] + 5, hp_text_loc[1]])
            main_screen.blit(hp_object.render(mv_points_text, 1, (0, 255, 255), None),
                             [1.5 * hp_object.size(hp_text)[0], hp_text_loc[1]])
            main_screen.blit(hp_object.render(str(move_points), 1, (255, 255, 255), None),
                             [1.5 * hp_object.size(hp_text)[0] + hp_object.size(mv_points_text)[0] + 5, hp_text_loc[1]])
            main_screen.blit(hp_object.render(fps_text, 1, (0, 255, 255), None), [
                1.5 * hp_object.size(hp_text)[0] + hp_object.size(mv_points_text)[0] + 5 *
                hp_object.size(str(move_points))[0], hp_text_loc[1]])
            main_screen.blit(hp_object.render(str(clock_this_game.tick_busy_loop(FPS)), 1, (255, 255, 255), None), [
                1.5 * hp_object.size(hp_text)[0] + hp_object.size(mv_points_text)[0] + 5 *
                hp_object.size(str(move_points))[0] + hp_object.size(fps_text)[0] + 5, hp_text_loc[1]])
            main_screen.blit(hp_object.render(laser_shots_text, 1, (0, 255, 255), None), [
                1.5 * hp_object.size(hp_text)[0] + hp_object.size(mv_points_text)[0] + 5 *
                hp_object.size(str(move_points))[0] + hp_object.size(fps_text)[0] + 45, hp_text_loc[1]])
            main_screen.blit(hp_object.render(str(main_vals[3]), 1, (255, 255, 255), None), [
                1.5 * hp_object.size(hp_text)[0] + hp_object.size(mv_points_text)[0] + 5 *
                hp_object.size(str(move_points))[0] + hp_object.size(fps_text)[0] + hp_object.size(laser_shots_text)[
                    0] + 50, hp_text_loc[1]])
            main_screen.blit(hp_object.render(missiles_text, 1, (0, 255, 255), None),
                             [6.5 * hp_object.size(hp_text)[0], hp_text_loc[1]])
            main_screen.blit(hp_object.render(str(main_vals[2]), 1, (255, 255, 255), None),
                             [6.5 * hp_object.size(hp_text)[0] + hp_object.size(missiles_text)[0] + 5, hp_text_loc[1]])
            # wirte 'move' and 'shoot'
            if char_move or char_shoot:
                time_move += timer_move_txt
                if time_move % 100:
                    time_stay_move = 0
                    while time_stay_move < 500:
                        time_stay_move += timer_move_txt
                        if char_move:
                            main_screen.blit(hp_object.render(str(move_txt).upper(), 1, (0, 255, 255), None),
                                             [6.5 * hp_object.size(hp_text)[0] + hp_object.size(missiles_text)[0] + 100,
                                              hp_text_loc[1]])
                        elif char_shoot:
                            main_screen.blit(hp_object.render(str(shoot_txt).upper(), 1, (0, 255, 255), None),
                                             [6.5 * hp_object.size(hp_text)[0] + hp_object.size(missiles_text)[0] + 100,
                                              hp_text_loc[1]])
            # draw sprites
            asteroids.draw(main_screen)
            fighter_group.draw(main_screen)
            weak_enemy_group.draw(main_screen)
            # draw healthbars
            for ship in weak_enemy_group:
                pygame.draw.line(main_screen, (0, 255, 0), (ship.rect.x, ship.rect.y + ship.rect.size[1]), (
                    ship.rect.x + np.dot(ship.rect.size[0], ship.health), ship.rect.y + ship.rect.size[1]), 5)

            if char_shoot:
                pygame.mouse.set_visible(False)
                main_screen.blit(target_image, pygame.mouse.get_pos())
                if animate_missile or laser_was_discharged:
                    ticks = clock_this_missile.tick(FPS)
                    dx = click[0] - source_pos[0]
                    dy = click[1] - source_pos[1]
                    pos = mf.get_pos(source_pos, click, dx, dy, ticks / 100)
                    source_pos = pos
                    if animate_missile:
                        mf.draw_missile(missile_image, pos, main_screen)
                        (missile_rect.x, missile_rect.y) = pos
                        # has the target been reached
                        if (abs(missile_rect.x - click[0]) + abs(missile_rect.y - click[1])) < 5:
                            animate_missile = False
                    elif laser_was_discharged:
                        mf.draw_missile(laser_image, pos, main_screen)
                        (laser_rect.x, laser_rect.y) = pos
                        if (abs(laser_rect.x - click[0]) + abs(laser_rect.y - click[1])) < 5:
                            laser_was_discharged = False

                            # check collision
                for nmes in weak_enemy_group:

                    if laser_was_discharged:

                        if nmes.rect.colliderect(laser_rect):
                            laser_was_discharged = False
                            red = np.random.normal(0.25, 0.1)
                            nmes.health -= red
                            enemy_was_hit = True
                            clock_this_hp = pygame.time.Clock()
                            elapse_time_hp = 0
                            start_loc_hp = nmes.rect.center
                            if nmes.health < 0.01:
                                weak_enemy_group.remove(nmes)
                                weak_enemy_set.remove(nmes.grid_loc)
                                break

                    elif animate_missile:
                        if nmes.rect.colliderect(missile_rect):
                            red = np.random.normal(0.5, 0.1)
                            nmes.health -= red
                            clock_this_hp = pygame.time.Clock()
                            start_loc_hp = nmes.rect.center
                            elapse_time_hp = 0
                            animate_missile = False
                            enemy_was_hit = True
                            if nmes.health < 0.01:
                                weak_enemy_group.remove(nmes)
                                weak_enemy_set.remove(nmes.grid_loc)
                                break

                # end game
                if not weak_enemy_group and not enemy_was_hit:
                    move_points = 3
                    for idx, vals in enumerate(init_vals):
                        main_vals[idx] = vals
                    char_shoot = False
                    asteroids.empty()
                    fighter_group.empty()
                    success_in_game = True
                    final_scene_show = True

                # finish player turn and get the enemies to move around and shoot
                if not main_vals[3] and not main_vals[
                    2] and not animate_missile and not laser_was_discharged and not enemy_was_hit:
                    char_shoot = False
                    nturns += 1
                    enemy_move_calc = True

            # enemies loop-calculate path
            elif enemy_move_calc:
                total_moving_pieces = 0
                for enemy in weak_enemy_group:
                    # if the enemy is farther than weak_enemy_move_range: run A* algorithm and get path to the fighter
                    if abs(enemy.grid_loc[0] - fighter_loc[0]) >= weak_enemy_move_range or abs(
                                    enemy.grid_loc[1] - fighter_loc[1]) >= weak_enemy_move_range:
                        enemy_path = mf.astar(enemy.grid_loc, fighter_loc, asteroid_set, weak_enemy_set)
                        # print(enemy.grid_loc, enemy_path, fighter_loc, weak_enemy_set, 'AAA')
                        # store the path 
                        if enemy_path:
                            # add to the temp_set where the enemy will be at the end of the move - 4 tiles away
                            if enemy_path[weak_enemy_move_range] != fighter_loc:
                                enemy.path = enemy_path[0:weak_enemy_move_range + 1]
                                weak_enemy_set.add(enemy.path[weak_enemy_move_range])
                                enemy.full_path = mf.get_full_path(enemy.path, step_size)
                            else:
                                # ...or 3 if the 4th is fighter
                                enemy.path = enemy_path[0:weak_enemy_move_range]
                                weak_enemy_set.add(enemy.path[weak_enemy_move_range - 1])
                                enemy.full_path = mf.get_full_path(enemy.path, step_size)
                                # remove where the enemy was at the beginning and add where he will be at the end of the move
                            # to 
                            # print(enemy.path, weak_enemy_set)
                            weak_enemy_set.remove(enemy.path[0])
                            total_moving_pieces += 1

                enemy_move_calc = False
                enemy_move = True
                step = 0
                total = 0

            elif enemy_move:
                for enemy in weak_enemy_group:
                    if abs(enemy.grid_loc[0] - fighter_loc[0]) >= weak_enemy_move_range or abs(
                                    enemy.grid_loc[1] - fighter_loc[1]) >= weak_enemy_move_range:
                        if step < len(enemy.full_path):
                            enemy.move_enemy(enemy.full_path[step])
                        else:
                            if not enemy.done:
                                enemy.done = True
                                total += 1
                                # and change its grid position too
                                if len(enemy.path) == weak_enemy_move_range + 1:
                                    enemy.grid_loc = enemy.path[weak_enemy_move_range]
                                else:
                                    enemy.grid_loc = enemy.path[weak_enemy_move_range - 1]

                                    # print(len(enemy.path), enemy.grid_loc, 'grgrgrg')

                # check if total number of moved pieces = number of pieces that can move
                if total == total_moving_pieces:
                    for enemy in weak_enemy_group:
                        enemy.done = False
                    enemy_move = False
                    enemy_shoot = True
                    total_shoot = 0
                    total_done_shoot = 0
                else:
                    step += 1

            elif enemy_shoot:

                for enemy in weak_enemy_group:

                    if abs(enemy.grid_loc[0] - fighter_loc[0]) < weak_enemy_move_range and abs(
                                    enemy.grid_loc[1] - fighter_loc[1]) < weak_enemy_move_range:

                        if not enemy.animate_nme_laser:
                            total_shoot += 1
                            mf.play_sound(laser_sound)
                            enemy.init_laser(fighter_loc)

                            enemy.animate_nme_laser = True
                            enemy.now_move_laser = True

                        if enemy.now_move_laser:
                            shoot_time = enemy.clock_enemy_laser.tick(FPS)
                            enemy.move_laser(FPS, main_screen, shoot_time)
                            if abs(enemy.enemy_laser_rect.x - np.dot(fighter_loc, GRID[0])[0]) < 20 and abs(
                                            enemy.enemy_laser_rect.y - np.dot(fighter_loc, GRID[1])[1]) < 20:
                                main_vals[0] -= 1
                                enemy.now_move_laser = False
                                enemy.done_moving_laser = True
                                total_done_shoot += 1
                    else:
                        pass

                # restore parameters, get back to the char_move stage
                if total_done_shoot == total_shoot:
                    move_points = 3
                    main_vals[2] = user_set_missile_value
                    main_vals[3] = user_set_laser_value
                    enemy_shoot = False
                    char_move = True
                    pygame.mouse.set_visible(True)
                    just_started = True
                    for nmes in weak_enemy_group:
                        nmes.animate_nme_laser = False
                        nmes.now_move_laser = False

            if main_vals[0] <1:
                move_points = 3
                for idx, vals in enumerate(init_vals):
                    main_vals[idx] = vals
                enemy_shoot = False
                char_move = False
                final_scene_show = True

            if enemy_was_hit:
                hp_tick = clock_this_hp.tick(60)
                elapse_time_hp += hp_tick
                m_l, m_r = 50, 50
                # until 1 second/1000 ms pass show the lost hps
                if elapse_time_hp < 1000:
                    main_screen.blit(hp_hit_object.render("-" + str(round(red, 2)), 1, (255, 0, 0), False), (
                        start_loc_hp[0] + m_r * elapse_time_hp / 1000, start_loc_hp[1] - m_l * elapse_time_hp / 1000))
                else:
                    enemy_was_hit = False

            if final_scene_show:
                # main_game = False
                # print('bla')
                f_scene.display_final_scene(nturns, main_screen, success_in_game, SCREEN_SIZE)


# launch
if __name__ == '__main__':
    # print(__version__)
    main()
