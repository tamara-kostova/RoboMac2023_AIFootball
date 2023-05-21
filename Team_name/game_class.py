from necessary_classes import *
from Team_name.render_data import *
from Team_name.Manager import *

pygame.init()

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

colors_left = [0, 0, 255]
colors_right = [0, 255, 0]

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
half_time_duration = 15
short_pause_countdown_time = 0
goal_pause_countdown_time = 0

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

displacement = random.randint(0, 10)
player_1_initial_position = [int((center[0] - playground[0]) / 2) + playground[0] - displacement, post_screen_top]
player_2_initial_position = [int((center[0] - playground[0]) / 2) + playground[0] - displacement, center[1]]
player_3_initial_position = [int((center[0] - playground[0]) / 2) + playground[0] - displacement,
                             post_screen_bottom]
player_4_initial_position = [player_1_initial_position[0] + half_playground_rect[2] + displacement, post_screen_top]
player_5_initial_position = [player_2_initial_position[0] + half_playground_rect[2] + displacement, center[1]]
player_6_initial_position = [player_3_initial_position[0] + half_playground_rect[2] + displacement,
                             post_screen_bottom]

initial_positions_team_left = [player_1_initial_position, player_2_initial_position, player_3_initial_position]
initial_positions_team_right = [player_4_initial_position, player_5_initial_position, player_6_initial_position]

SPEED = 1


class FootBallGame:
    def __init__(self):
        self.team_1_properties = team_1_script.team_properties()
        self.team_2_properties = team_2_script.team_properties()
        self.team_1 = [
            Player(self.team_1_properties['player_names'][0], weights[0], radiuses[0], accelerations[0], speeds[0],
                   shot_powers[0]),
            Player(self.team_1_properties['player_names'][1], weights[1], radiuses[1], accelerations[1], speeds[1],
                   shot_powers[1]),
            Player(self.team_1_properties['player_names'][2], weights[2], radiuses[2], accelerations[2], speeds[2],
                   shot_powers[2])]
        self.team_2 = [
            Player(self.team_2_properties['player_names'][0], weights[0], radiuses[0], accelerations[0], speeds[0],
                   shot_powers[0]),
            Player(self.team_2_properties['player_names'][1], weights[1], radiuses[1], accelerations[1], speeds[1],
                   shot_powers[1]),
            Player(self.team_2_properties['player_names'][2], weights[2], radiuses[2], accelerations[2], speeds[2],
                   shot_powers[2])]

        self.ball = Ball(420, 250, 15, 0.5)
        self.posts = [Post(post_screen_left, post_screen_top, post_radius, post_mass),
                      Post(post_screen_left, post_screen_bottom, post_radius, post_mass),
                      Post(post_screen_right, post_screen_top, post_radius, post_mass),
                      Post(post_screen_right, post_screen_bottom, post_radius, post_mass)]
        self.team_1_score, self.team_2_score = 0, 0
        displacement = random.randint(0, 10)
        self.reset()
        self.time_to_play = half_time_duration
        self.half = 1
        self.game_exit = False
        self.is_half = False
        self.clock = pygame.time.Clock()
        self.sum_dt = 0
        self.ball.reset()

    def reset(self):
        displacement = random.randint(0, 10)
        player_1_initial_position = [int((center[0] - playground[0]) / 2) + playground[0] - displacement,
                                     post_screen_top]
        player_2_initial_position = [int((center[0] - playground[0]) / 2) + playground[0] - displacement, center[1]]
        player_3_initial_position = [int((center[0] - playground[0]) / 2) + playground[0] - displacement,
                                     post_screen_bottom]
        player_4_initial_position = [player_1_initial_position[0] + half_playground_rect[2] + displacement,
                                     post_screen_top]
        player_5_initial_position = [player_2_initial_position[0] + half_playground_rect[2] + displacement, center[1]]
        player_6_initial_position = [player_3_initial_position[0] + half_playground_rect[2] + displacement,
                                     post_screen_bottom]

        self.initial_positions_team_left = [player_1_initial_position, player_2_initial_position,
                                            player_3_initial_position]
        self.initial_positions_team_right = [player_4_initial_position, player_5_initial_position,
                                             player_6_initial_position]
        for i in range(3):
            self.team_1[i].reset(initial_positions_team_left[i], 0)
        for i in range(3):
            self.team_2[i].reset(initial_positions_team_right[i], 0)

    def reset_game(self):
        self.team_1_properties = team_1_script.team_properties()
        self.team_2_properties = team_2_script.team_properties()
        self.team_1 = [
            Player(self.team_1_properties['player_names'][0], weights[0], radiuses[0], accelerations[0], speeds[0],
                   shot_powers[0]),
            Player(self.team_1_properties['player_names'][1], weights[1], radiuses[1], accelerations[1], speeds[1],
                   shot_powers[1]),
            Player(self.team_1_properties['player_names'][2], weights[2], radiuses[2], accelerations[2], speeds[2],
                   shot_powers[2])]
        self.team_2 = [
            Player(self.team_2_properties['player_names'][0], weights[0], radiuses[0], accelerations[0], speeds[0],
                   shot_powers[0]),
            Player(self.team_2_properties['player_names'][1], weights[1], radiuses[1], accelerations[1], speeds[1],
                   shot_powers[1]),
            Player(self.team_2_properties['player_names'][2], weights[2], radiuses[2], accelerations[2], speeds[2],
                   shot_powers[2])]

        self.ball = Ball(420, 250, 15, 0.5)
        self.posts = [Post(post_screen_left, post_screen_top, post_radius, post_mass),
                      Post(post_screen_left, post_screen_bottom, post_radius, post_mass),
                      Post(post_screen_right, post_screen_top, post_radius, post_mass),
                      Post(post_screen_right, post_screen_bottom, post_radius, post_mass)]
        self.team_1_score, self.team_2_score = 0, 0
        self.reset()
        self.time_to_play = half_time_duration
        self.half = 1
        self.game_exit = False
        self.is_half = False
        self.sum_dt = 0
        self.ball.reset()

    def update(self, final_move, decision2, screen, start=0):

        velocity_step = 10000
        angle_step = 0.1
        angle_change = 0
        velocity_change = 0

        circles = [self.team_1[0], self.team_1[1], self.team_1[2], self.team_2[0], self.team_2[1], self.team_2[2],
                   self.ball, self.posts[0], self.posts[1], self.posts[2], self.posts[3]]
        goal = False

        if self.sum_dt >= 50:
            # print(self.sum_dt)
            return True
        #
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         self.game_exit = True
        #         pygame.quit()
        #         quit()
        #         return True

        if not goal:
            manager_1_decision = final_move

            manager_2_decision = decision2

            manager_decision = [manager_1_decision[0], manager_1_decision[1], manager_1_decision[2],
                                manager_2_decision[0], manager_2_decision[1], manager_2_decision[2]]

            manager_decision[0]['alpha'] += angle_change
            manager_decision[0]['force'] += velocity_change

            for i, player in enumerate(circles[:6]):
                player.move(manager_decision[i])
            self.ball.move()

            if not goal:
                goal_team_right = post_screen_top < self.ball.y < post_screen_bottom and self.ball.x < post_screen_left
                goal_team_left = post_screen_top < self.ball.y < post_screen_bottom and self.ball.x > post_screen_right
                if goal_team_left:
                    if self.half == 1:
                        self.team_1_score += 1
                    else:
                        self.team_2_score += 1
                    self.ball.reset()
                    self.reset()
                if goal_team_right:
                    if self.half == 1:
                        self.team_2_score += 1
                    else:
                        self.team_1_score += 1
                    self.ball.reset()
                    self.reset()
                goal = goal_team_left or goal_team_right


            if not goal:
                for i in range(len(circles[:-4])):
                    circles[i].snelius()
                    for j in range(i + 1, len(circles)):
                        if collision(circles[i], circles[j]):
                            circles[i], circles[j] = resolve_collision(circles[i], circles[j])

            # render(screen, self.team_1, self.team_2, self.ball, self.posts,
            #        self.team_1_score, self.team_2_score, self.time_to_play, start, self.half,
            #        False,
            #        'ManUtd', 'Real', [0, 0, 255], [0, 255, 0])

        return

    def updated_time(self, time):
        self.time_to_play -= time

    def change_half(self):
        self.half = 2
        self.time_to_play = half_time_duration
        your_side = 'left' if self.half == 1 else 'right'
        if your_side == 'right':
            for i, player in enumerate(self.team_1):
                player.reset(initial_positions_team_right[i], np.pi)
            for i, player in enumerate(self.team_2):
                player.reset(initial_positions_team_left[i], 0)
        else:
            for i, player in enumerate(self.team_1):
                player.reset(initial_positions_team_left[i], 0)
            for i, player in enumerate(self.team_2):
                player.reset(initial_positions_team_right[i], np.pi)
        self.ball.reset()
        # self.play_step()
        self.reset()

    def updated_dt(self):
        self.sum_dt += dt
