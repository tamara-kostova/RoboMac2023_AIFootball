# Choose names for your players and team
# Choose a funny name for each player and your team
# Use names written only in cyrillic
# Make sure that the name is less than 11 characters
# Don't use profanity!!!
import numpy as np
import random


def team_properties():
    properties = dict()
    player_names = ["Пандевалдо", "Панчевалдо", "Елмасалдо"]
    properties['team_name'] = "МакЧелзи"
    properties['player_names'] = player_names
    properties['image_name'] = 'Blue.png'  # use image resolution 153x153
    return properties


# This function gathers game information and controls each one of your three players

def getRoles(players):
    roles = dict()
    sorted_by_raduis = sorted(players, key=lambda x: x['radius'])
    roles['attacker'] = sorted_by_raduis[0]
    roles['mid'] = sorted_by_raduis[1]
    roles['defender'] = sorted_by_raduis[2]
    return roles


def get_angle_from_points(x1, y1, x2, y2):
    if x1 > x2:
        return np.arctan((y2 - y1) / (x1 - x2)) - np.pi
    elif x1 < x2:
        return np.arctan((y1 - y2) / (x1 - x2))
    else:
        return 0


def get_data_attacker(player_x, player_y, ball_x, ball_y, your_side):
    distance_from_ball = np.sqrt(np.power((ball_x - player_x), 2) + np.power((ball_y - player_y), 2))
    shot = True

    if your_side == 'left':
        if distance_from_ball <= 10 and player_x < ball_x:
            pos_x = 1316
            pos_y = random.randint(343, 578)
            shot = True
        elif player_x > ball_x:
            pos_x = ball_x
            pos_y = ball_y
            shot = False
        else:
            pos_x = ball_x
            pos_y = ball_y
            shot = True
        direction = get_angle_from_points(player_x, player_y, ball_x, ball_y)

    else:
        if distance_from_ball <= 10 and player_x > ball_x:
            pos_x = 50
            pos_y = random.randint(343, 578)
            shot = True
        elif player_x < ball_x:
            pos_x = ball_x
            pos_y = ball_y
            shot = False
        else:
            pos_x = ball_x
            pos_y = ball_y
            shot = True
        direction = 2 * np.pi - get_angle_from_points(player_x, player_y, ball_x, ball_y)

    return direction, shot


def get_angle_goal_keeper(x1, y1, x2, y2, your_side, max_force):
    goal_y = y2
    if y2 <= 343:
        goal_y = max(343, y2)
    else:
        goal_y = min(578, y2)
    if your_side == 'right':
        goal_x = 1300
        direction = get_angle_from_points(x1, y1, goal_x, goal_y)
    else:
        goal_x = 66
        direction = 2 * np.pi - get_angle_from_points(x1, y1, goal_x, goal_y)
    if abs(x1 - goal_x) < 50:
        force = 50
    else:
        force = max_force
    return direction, max_force


def get_data_mid(player_x, player_y, other_player_x, other_player_y, your_side):
    if your_side == 'left':
        return get_angle_from_points(player_x, player_y, other_player_x, other_player_y)
    else:
        return 2 * np.pi - get_angle_from_points(player_x, player_y, other_player_x, other_player_y)
    # return direction


def decision(our_team, their_team, ball, your_side, half, time_left, our_score, their_score):
    manager_decision = [dict(), dict(), dict()]
    players = our_team
    opponents = their_team

    # pass?, shoot?
    players = getRoles(players)
    their_team = getRoles(their_team)
    i = 0
    for p in players:
        player = players[p]
        ball_x, ball_y = ball['x'], ball['y']
        player_x, player_y = player['x'], player['y']
        force = player['a_max'] * player['mass']
        shot_power = player['shot_power_max']
        # manager_decision[i]['alpha'] = get_angle_from_points(player_x, player_y, )
        manager_decision[i]['shot_request'] = get_data_attacker(player_x, player_y, ball_x, ball_y, your_side)[1]
        manager_decision[i]['force'] = force / 2
        manager_decision[i]['alpha'] = get_data_attacker(player_x, player_y, ball_x, ball_y, your_side)[0]
        manager_decision[i]['shot_power'] = shot_power
        i+=1
    # print(our_score, their_score)
    return manager_decision