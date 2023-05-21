import time
import random
import numpy as np
import pandas as pd
import pygame
from Team_name import Manager as team_1_script
from Team_name import Manager as team_2_script
import os
import platform

game_name = 'AI Football'
fps = 60
dt = 1 / fps

resolution = 1366, 768
resolution_rect = [0, 0, resolution[0], resolution[1]]
ground = [0, int(resolution[1] / 5), resolution[0], resolution[1]]
ground_rect = [ground[0], ground[1], resolution[0], resolution[1]]
playground = [50, 50 + int(resolution[1] / 5), resolution[0] - 50, resolution[1] - 50]
playground_rect = [playground[0], playground[1], playground[2] - playground[0], playground[3] - playground[1]]
half_playground_rect = [playground_rect[0], playground_rect[1], int(playground_rect[2] / 2), playground_rect[3]]
center = [int((playground[2] - playground[0]) / 2) + playground[0],
          int((playground[3] - playground[1]) / 2) + playground[1]]

post_radius = 10
post_screen_top = 343
post_screen_bottom = 578
post_screen_left = playground[0]
post_screen_right = playground[2]

player_1_initial_position = [int((center[0] - playground[0]) / 2) + playground[0] - 10, post_screen_top]
player_2_initial_position = [int((center[0] - playground[0]) / 2) + playground[0] - 10, center[1]]
player_3_initial_position = [int((center[0] - playground[0]) / 2) + playground[0] - 10, post_screen_bottom]
player_4_initial_position = [player_1_initial_position[0] + half_playground_rect[2] + 10, post_screen_top]
player_5_initial_position = [player_2_initial_position[0] + half_playground_rect[2] + 10, center[1]]
player_6_initial_position = [player_3_initial_position[0] + half_playground_rect[2] + 10, post_screen_bottom]

initial_positions_team_left = [player_1_initial_position, player_2_initial_position, player_3_initial_position]
initial_positions_team_right = [player_4_initial_position, player_5_initial_position, player_6_initial_position]

# Colors:
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
yellow = [255, 255, 0]
green = [0, 255, 0]
sky_blue = [135, 206, 250]
blue = [0, 0, 255]
grass = [1, 142, 14]

cursor_width = 2

ball_restitution = 0.6
player_player_restitution = 0.5
ball_restitution_under_player_control = 0.4
player_post_restitution = 0.5
half_time_duration = 45
short_pause_countdown_time = 5
goal_pause_countdown_time = 5

shift = 230
team_left_logo_position = [22 + shift, 2, 153, 153]
team_right_logo_position = [527 + shift, 2, 153, 153]
team_left_color_position = [173 + shift, 0, 50, 153]
team_right_color_position = [477 + shift, 0, 50, 153]
post_mass = 1e99

# Player stats: Kylian Mbappé, Joshua Kimmich, Joško Gvardiol
weights = [73, 75, 80]
radiuses = [22, 23, 24]
accelerations = [100, 60, 70]
speeds = [100, 60, 85]
shot_powers = [65, 70, 50]

if platform.system() == "Windows":
    red_logo = pygame.image.load('..\\Team_name\\' + team_1_script.team_properties()['image_name'])
    blue_logo = pygame.image.load('..\\Team_name\\' + team_2_script.team_properties()['image_name'])
else:
    red_logo = pygame.image.load('../Team_name/' + team_1_script.team_properties()['image_name'])
    blue_logo = pygame.image.load('../Team_name/' + team_2_script.team_properties()['image_name'])
logos = {'ManUtd': red_logo, 'Real': blue_logo}


def render_goal_pause(start_goal, screen):
    myfont = pygame.font.SysFont("monospace", 350)
    message = "GOAL!"
    label = myfont.render(message, True, (0, 0, 0))
    while int(time.time() - start_goal) < goal_pause_countdown_time:
        screen.blit(label, (200, 250))
        pygame.display.flip()


def render(screen, team_1, team_2, ball, posts, team_1_score, team_2_score, time_to_play, start, half, countdown,
           team_1_name, team_2_name, team_1_color, team_2_color):
    pygame.draw.rect(screen, white, resolution_rect)
    pygame.draw.rect(screen, grass, ground_rect)
    pygame.draw.rect(screen, black, resolution_rect, 2)
    pygame.draw.rect(screen, black, ground_rect, 2)
    pygame.draw.rect(screen, white, playground_rect, 2)
    pygame.draw.rect(screen, white, half_playground_rect, 2)
    pygame.draw.circle(screen, white, center, 100, 2)
    pygame.draw.circle(screen, white, center, 5)

    if half == 1:
        team_left_logo = logos[team_1_name]
        team_right_logo = logos[team_2_name]

        font = pygame.font.SysFont("roboto", 50)
        img = font.render(team_1_name, True, (0, 0, 0))
        screen.blit(img, (10, 60))

        font = pygame.font.SysFont("roboto", 50)
        img = font.render(team_2_name, True, (0, 0, 0))
        screen.blit(img, (915, 60))

        team_left_color = team_1_color
        team_right_color = team_2_color
    else:
        team_left_logo = logos[team_2_name]
        team_right_logo = logos[team_1_name]

        font = pygame.font.SysFont("roboto", 45)
        img = font.render(team_1_name, True, (0, 0, 0))
        screen.blit(img, (915, 60))

        font = pygame.font.SysFont("roboto", 45)
        img = font.render(team_2_name, True, (0, 0, 0))
        screen.blit(img, (10, 60))

        team_left_color = team_2_color
        team_right_color = team_1_color

    screen.blit(team_left_logo, team_left_logo_position)
    screen.blit(team_right_logo, team_right_logo_position)

    pygame.draw.rect(screen, team_left_color, team_left_color_position)
    pygame.draw.rect(screen, team_right_color, team_right_color_position)

    for player in team_1:
        player.draw(screen, team_1_color)
        font = pygame.font.SysFont("roboto", 30)
    for player in team_2:
        player.draw(screen, team_2_color)
        font = pygame.font.SysFont("roboto", 30)
    for player in team_1 + team_2:
        img = font.render(player.name, True, (0, 0, 0))
        screen.blit(img, (player.x - 50, player.y - 50))
    ball.draw(screen)
    for post in posts:
        post.draw(screen)

    if countdown:
        myfont = pygame.font.SysFont("monospace", 750)
        short_pause_countdown = "{}".format(short_pause_countdown_time - int(time.time() - start))
        label = myfont.render(short_pause_countdown, 1, (0, 0, 0))
        screen.blit(label, (460, 85))

        myfont = pygame.font.SysFont("monospace", 120)
        message = "{}s".format(time_to_play)
        label = myfont.render(message, 1, (0, 0, 0))
        screen.blit(label, (1150, 0))
    else:
        myfont = pygame.font.SysFont("monospace", 120)
        time_screen_value = time_to_play - int(time.time() - start)
        if time_screen_value < 0:
            time_screen_value = 0
        message = "{}s".format(time_screen_value)
        label = myfont.render(message, 1, (0, 0, 0))
        screen.blit(label, (1150, 0))

    myfont = pygame.font.SysFont("roboto", 40)
    if half == 1:
        message = "полувреме: 1"
    else:
        message = "полувреме: 2"

    label = myfont.render(message, 1, (0, 0, 0))
    screen.blit(label, (1175, 125))

    myfont = pygame.font.SysFont("monospace", 150)
    if half == 1:
        message = "{}:{}".format(team_1_score, team_2_score)
    else:
        message = "{}:{}".format(team_2_score, team_1_score)

    label = myfont.render(message, 1, (0, 0, 0))
    screen.blit(label, (215 + shift, 0))

    pygame.display.flip()
    pygame.time.Clock().tick(fps)
