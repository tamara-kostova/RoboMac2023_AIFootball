# Choose names for your players and team
# Choose a funny name for each player and your team
# Use names written only in cyrillic
# Make sure that the name is less than 11 characters
# Don't use profanity!!!
import numpy as np
import random


def team_properties():
    properties = dict()
    player_names = ["Капино", "Венко", "Пашето"]
    properties['team_name'] = "Пелистер"
    properties['player_names'] = player_names
    properties['image_name'] = 'pelister.png'  # use image resolution 153x153
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


def get_angle_attacker(player_x, player_y, ball_x, ball_y):
    direction = get_angle(player_x, player_y, ball_x, ball_y)
    return direction


def get_angle_goal_keeper(x1, y1, x2, y2, your_side, max_force):
    goal_y = y2
    if y2 <= 363:
        goal_y = max(323, y2)
    else:
        goal_y = min(598, y2)
    if your_side == 'right':
        goal_x = 1281
    else:
        goal_x = 85
    direction = get_angle(x1, y1, goal_x, goal_y)
    return direction, max_force


def get_angle_mid(player_x, player_y, other_player_x, other_player_y, your_side):
    if your_side == 'left' and other_player_x > 100:
        x_coor = other_player_x - 50
    elif your_side == 'right' and other_player_x < 1266:
        x_coor = other_player_x + 50
    else:
        x_coor = other_player_x
    return get_angle(player_x, player_y, x_coor, other_player_y)
    # return direction


def get_angle(x1, y1, x2, y2):
    return 2 * np.pi - np.arctan2((y1 - y2), (x2 - x1))


def get_side_attacker(player_x, player_y, ball_x, alpha, your_side):
    goal_top = 578
    goal_bottom = 343
    if your_side == 'left':
        goal_x = 1300
        return player_x < ball_x
    # else:
    #     goal_x = 50
    #     b = player_x>ball_x
    #
    # angle_top = get_angle(player_x, player_y, goal_x, goal_top)
    # angle_bot = get_angle(player_x, player_y, goal_x, goal_bottom)
    # return angle_bot<alpha<angle_top and b
    return player_x > ball_x


def get_closest_player_to_your_goal(their_team, your_side):
    if your_side == 'left':
        g = np.array([50, 460])
    else:
        g = np.array([1316, 460])
    min_dist = 20000
    i = 0
    for player in their_team:
        pl = their_team[player]
        p = np.array([pl['x'], pl['y']])
        dist = np.linalg.norm(g - p)
        if dist < min_dist:
            min_dist = dist
            index = player
        i += 1
    return their_team[index]

def get_closest_player_to_their_goal(their_team, your_side):
    if your_side == 'right':
        g = np.array([50, 460])
    else:
        g = np.array([1316, 460])
    min_dist = 20000
    i = 0
    for player in their_team:
        pl = their_team[player]
        p = np.array([pl['x'], pl['y']])
        dist = np.linalg.norm(g - p)
        if dist < min_dist:
            min_dist = dist
            index = player
        i += 1
    return their_team[index]


def get_random_angle_attacker(player_x, player_y, your_side):
    if your_side == 'left':
        goal = [1316, random.randint(343, 578)]
    else:
        goal = [50, random.randint(343, 578)]
    return get_angle(player_x, player_y, goal[0], goal[1])


def min_distance_from_opponents(player, their_team):
    g = np.array([player['x'], player['y']])
    min_dist = 20000
    i = 0
    for player in their_team:
        pl = their_team[player]
        p = np.array([pl['x'], pl['y']])
        dist = np.linalg.norm(g - p)
        if dist < min_dist:
            min_dist = dist
        i += 1
    return min_dist


def attacker_not_directed_at_side(player, your_side, alpha, ball):
    if your_side == 'left':
        goal_x = 1300
        return player['x'] < ball['x']
    return player['x'] > ball['x']


def attacker_not_directed_at_goal(player, your_side, alpha):
    if your_side == 'left':
        goal_x = 1316
    else:
        goal_x = 50

    y_coordinate_attacker_goal = player['y'] - (np.tan(2 * np.pi - alpha) * (player['x'] - goal_x))

    return 343 < 768 - y_coordinate_attacker_goal < 578


def get_shot_angle_attacker(player, your_side, alpha):
    if your_side == 'left':
        goal_x = 1316
    else:
        goal_x = 50

    y_coordinate_attacker_goal = player['y'] - (np.tan(2 * np.pi - alpha) * (player['x'] - goal_x))
    y_coordinate_attacker_goal = 768 - y_coordinate_attacker_goal
    if 343 < y_coordinate_attacker_goal < 578:
        if abs(y_coordinate_attacker_goal - 343) < abs(y_coordinate_attacker_goal - 578):
            return get_angle(player['x'], player['y'], goal_x, 353)
    return get_angle(player['x'], player['y'], goal_x, 568)


def get_angle_mid_between(player, ball, their_team, your_side):
    if your_side == 'left':
        g = np.array([50, 460])
    else:
        g = np.array([1316, 460])

    dict_by_distances = {k: np.linalg.norm(g - np.array([their_team[k]['x'], their_team[k]['y']])) for k in
                         their_team.keys()}

    sorted_dict = sorted(dict_by_distances.items(), reverse=True)

    p1 = their_team[sorted_dict[0][0]]['x'], their_team[sorted_dict[0][0]]['y']
    p2 = their_team[sorted_dict[1][0]]['x'], their_team[sorted_dict[1][0]]['y']

    x_avg = (p1[0] + p2[0]) / 2
    y_avg = (p1[1] + p2[1]) / 2

    if your_side == 'left' and player['x'] > 450:
        x_avg -= 100
    elif your_side == 'right' and player['x'] < 916:
        x_avg += 100

    return get_angle(player['x'], player['y'], x_avg, y_avg)


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

        w = np.array([player_x, player_y])
        b = np.array([ball_x, ball_y])

        distance_from_ball = np.linalg.norm(w - b)

        shot_request = bool
        force = player['a_max'] * player['mass']
        shot_power = player['shot_power_max']

        if p == 'attacker':  # attacker
            alpha = get_angle_attacker(player_x, player_y, ball_x, ball_y)
            wow = np.array([player_x, player_y])
            goa = np.array([1316, 460]) if your_side == 'left' else np.array([50, 460])

            distance_from_goal = np.linalg.norm(wow - goa)

            manager_decision[i]['shot_request'] = True
            if distance_from_ball < 50 and not attacker_not_directed_at_side(player, your_side, alpha, ball):
                manager_decision[i]['alpha'] = alpha + 3 * np.pi / 8
                manager_decision[i]['shot_request'] = False
            else:
                if distance_from_ball < 50 and distance_from_goal < 300 and attacker_not_directed_at_goal(player,
                                                                                                          your_side,
                                                                                                          alpha):
                    manager_decision[i]['alpha'] = get_shot_angle_attacker(player, your_side, alpha)
                else:
                    manager_decision[i]['alpha'] = get_angle_attacker(player_x, player_y, ball_x, ball_y)
            manager_decision[i]['force'] = force


        elif p == 'mid':  # mid
            alpha = get_angle_attacker(player_x, player_y, ball_x, ball_y)
            manager_decision[i]['shot_request'] = True  # choose if you want to shoot
            opponent_attacker = get_closest_player_to_your_goal(their_team, your_side)
            if our_score < their_score or (our_score == their_score and half == 2):
                opponent_defender = get_closest_player_to_their_goal(their_team, your_side)
                manager_decision[i]['alpha'] = get_angle(player_x, player_y, opponent_defender['x'],opponent_defender['y'])
            else:
                if (your_side == 'left' and opponent_attacker['x'] < 683 and ball_x < 683) or (
                        your_side == 'right' and opponent_attacker['x'] > 683 and ball_x > 683):
                    manager_decision[i]['alpha'] = get_angle_mid(player_x, player_y, opponent_attacker['x'],
                                                                 opponent_attacker['y'], your_side)
                    manager_decision[i]['shot_request'] = True

                else:
                    if distance_from_ball < 50 and not attacker_not_directed_at_side(player, your_side, alpha, ball):
                        manager_decision[i]['alpha'] = alpha + np.pi / 2
                        manager_decision[i]['shot_request'] = False
                    else:
                        manager_decision[i]['alpha'] = get_angle_attacker(player_x, player_y, ball_x, ball_y)
            manager_decision[i]['force'] = force

        else:  # defender
            manager_decision[i]['shot_request'] = True  # choose if you want to shoot
            manager_decision[i]['alpha'] = get_angle_goal_keeper(player_x, player_y, ball_x, ball_y, your_side, force)[
                0]
            manager_decision[i]['force'] = get_angle_goal_keeper(player_x, player_y, ball_x, ball_y, your_side, force)[
                1]
        manager_decision[i]['shot_power'] = shot_power  # use different shot power: (0, 'shot_power_max')
        i += 1
    # print(our_score, their_score)
    return manager_decision