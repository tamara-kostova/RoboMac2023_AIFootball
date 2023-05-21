import time
import random
import numpy as np
import pandas as pd
import pygame
from Team_name import Manager as team_1_script
from Team_name import Manager as team_2_script
import os
import platform
import AIFootball


class FootballGame:
    def __init__(self):
        self.team_1_properties = team_1_script.team_properties()
        self.team_2_properties = team_2_script.team_properties()
        self.team_1 = [
            AIFootball.Player(self.team_1_properties['player_names'][0], weights[0], radiuses[0], accelerations[0],
                              speeds[0],
                              shot_powers[0]),
            Player(team_1_properties['player_names'][1], weights[1], radiuses[1], accelerations[1], speeds[1],
                   shot_powers[1]),
            Player(team_1_properties['player_names'][2], weights[2], radiuses[2], accelerations[2], speeds[2],
                   shot_powers[2])]
        team_2 = [Player(team_2_properties['player_names'][0], weights[0], radiuses[0], accelerations[0], speeds[0],
                         shot_powers[0]),
                  Player(team_2_properties['player_names'][1], weights[1], radiuses[1], accelerations[1], speeds[1],
                         shot_powers[1]),
                  Player(team_2_properties['player_names'][2], weights[2], radiuses[2], accelerations[2], speeds[2],
                         shot_powers[2])]

        the_ball = Ball(420, 250, 15, 0.5)
        the_posts = [Post(post_screen_left, post_screen_top, post_radius, post_mass),
                     Post(post_screen_left, post_screen_bottom, post_radius, post_mass),
                     Post(post_screen_right, post_screen_top, post_radius, post_mass),
                     Post(post_screen_right, post_screen_bottom, post_radius, post_mass)]

        if platform.system() == "Windows":
            red_logo = pygame.image.load(os.getcwd() + '\\Team_name\\' + team_1_properties['image_name'])
            blue_logo = pygame.image.load(os.getcwd() + '\\Team_name\\' + team_2_properties['image_name'])
        else:
            red_logo = pygame.image.load(os.getcwd() + '/Team_name/' + team_1_properties['image_name'])
            blue_logo = pygame.image.load(os.getcwd() + '/Team_name/' + team_2_properties['image_name'])
        logos = {team_1_properties['team_name']: red_logo, team_2_properties['team_name']: blue_logo}
        game(team_1, team_2, the_ball, the_posts, team_1_properties['team_name'], team_2_properties['team_name'], red,
             blue,
             team_1_script, team_2_script)
