# import time
from collections import deque

# import torch

from AIFootball import *
from Team_name.model import *
# from Team_name.helper import plot
from Team_name.game_class import *
from Team_name.necessary_classes import *

from Team_name import Not_move as not_move_script
from Team_name import Offense as offense_script
from Team_name import Defense as defense_script
from Team_name import Manager as manager_script

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


def get_directory_from_3_tensors(output_data):
    final_move = list()

    curr_dict = dict()
    curr_dict['force'] = 1000000
    curr_dict['alpha'] = output_data[0]
    curr_dict['shot_power'] = 1000000
    curr_dict['shot_request'] = True
    final_move.append(curr_dict)

    curr_dict = dict()
    curr_dict['force'] = 1000000
    curr_dict['alpha'] = output_data[1]
    curr_dict['shot_power'] = 1000000
    curr_dict['shot_request'] = True
    final_move.append(curr_dict)

    curr_dict = dict()
    curr_dict['force'] = 1000000
    curr_dict['alpha'] = output_data[2]
    curr_dict['shot_power'] = 1000000
    curr_dict['shot_request'] = True
    final_move.append(curr_dict)

    return final_move


def get_dict_from_array(output_data):
    final_move = list()

    curr_dict = dict()
    curr_dict['force'] = output_data[0]
    curr_dict['alpha'] = output_data[1] % np.pi * 2
    curr_dict['shot_power'] = output_data[2]
    curr_dict['shot_request'] = output_data[3] > 1000
    final_move.append(curr_dict)

    curr_dict = dict()
    curr_dict['force'] = output_data[4]
    curr_dict['alpha'] = output_data[5] % np.pi * 2
    curr_dict['shot_power'] = output_data[6]
    curr_dict['shot_request'] = output_data[7] > 1000
    final_move.append(curr_dict)

    curr_dict = dict()
    curr_dict['force'] = output_data[8]
    curr_dict['alpha'] = output_data[9] % np.pi * 2
    curr_dict['shot_power'] = output_data[10]
    curr_dict['shot_request'] = output_data[11] > 1000
    final_move.append(curr_dict)

    return final_move


class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet()
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        if os.path.exists('model_0.pt'):
            self.model.load_state_dict(torch.load('model_0.pt'))

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        # for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        our_team, their_team, ball, your_side, half, time_left, our_score, their_score = state
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 1500 - self.n_games
        final_move = [dict(), dict(), dict()]
        # if random.randint(0, 400) < self.epsilon:
        if random.randint(0, 2500) < self.epsilon:
            for i in range(3):
                player = our_team[i]
                alpha = player['alpha'] + random.uniform(-2, 2) * np.pi * 0.1
                # alpha = random.uniform(0, 2) * np.pi
                force = random.uniform(0, our_team[i]['mass'] * our_team[i]['a_max'])
                shot_request = random.choice([True, False])
                shot_power = our_team[i]['shot_power_max']
                final_move[i] = {'shot_request': shot_request, 'force': force, 'alpha': alpha, 'shot_power': shot_power}
        else:
            # prediction = self.model(state0)
            # move = torch.argmax(prediction).item()
            # final_move[move] = 1
            # for i in range(3):
            #     player = our_team[i]
            #     alpha = player['alpha'] + random.uniform(-2, 2) * np.pi * 0.1
            #     # alpha = random.uniform(0, 2) * np.pi
            #     force = random.uniform(0, our_team[i]['mass'] * our_team[i]['a_max'])
            #     shot_request = random.choice([True, False])
            #     shot_power = our_team[i]['shot_power_max']
            #     final_move[i] = {'shot_request': shot_request, 'force': force, 'alpha': alpha, 'shot_power': shot_power}
            encoded_state = get_1D_arry_from_dict(state)
            state0 = torch.tensor(encoded_state, dtype=torch.float)
            inputs = torch.tensor(state0)
            outputs = self.model(inputs)
            output_data = outputs.detach().numpy().tolist()
            final_move = get_directory_from_3_tensors(output_data)

            # state_list = state0.cpu().numpy()
            # # final_move = get_state_from_list(state_list)
            # # return self.PolicyNet(Input).argmax(dim=1)
        return final_move

    def get_state(self, game):
        our_team = list()
        for i in range(3):
            player_dict = dict()
            player = game.team_1[i]
            our_team.append(player.data())
        their_team = list()
        for i in range(3):
            player_dict = dict()
            player = game.team_2[i]
            their_team.append(player.data())
        ball = game.ball
        ball = ball.data()
        your_side = 'left' if game.half == 1 else 'right'
        half = game.half
        our_score = game.team_1_score
        their_score = game.team_2_score
        time_left = game.time_to_play
        state = [our_team, their_team, ball, your_side, half, time_left, our_score, their_score]
        return list(state)


def reward(state):
    own_score = state[6]
    their_score = state[7]
    # ball = state[2]['x'], state[2]['y']
    #
    # our_goal = np.array([50, 460])
    # ball = np.array(ball)
    #
    # distance_from_ball_to_our_goal = np.linalg.norm(our_goal - ball)
    #
    # rew = 0
    #
    # for player in state[0]:
    #     p = np.array((player['x'], player['y']))
    #     dist = np.linalg.norm(p - ball)
    #     rew += 100/dist
    #     # if player['y'] < 180 or player['y'] > 718:
    #     #     rew -= 1
    #
    #
    # # if distance_from_ball_to_our_goal > 683:
    # #     rew += distance_from_ball_to_our_goal * 0.001
    # # else:
    # #     rew += 0

    # rew +=

    return (own_score - their_score) * 20


def train():
    # screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
    # pygame.display.set_caption('Game 1')
    record = 0
    agent = Agent()
    f_game = FootBallGame()
    done = False
    start = time.time()

    # plot_scores = []
    # plot_mean_scores = []
    # total_score = 0

    num_games = 1000
    model_index = 0
    while model_index < 4:
        done = False
        state_old = agent.get_state(f_game)
        final_move = agent.get_action(state_old)
        our_team, their_team, ball, your_side, half, time_left, our_score, their_score = state_old
        your_side = 'left' if your_side == 'right' else 'right'
        # decision2 = team_1_script.decision(their_team, our_team, ball, your_side, half, time_left, our_score,
        #                                    their_score)
        if model_index == 0:
            decision2 = not_move_script.decision(their_team, our_team, ball, your_side, half, time_left, our_score,
                                                 their_score)
        elif model_index == 1:
            decision2 = offense_script.decision(their_team, our_team, ball, your_side, half, time_left, our_score,
                                                their_score)
        elif model_index == 2:
            decision2 = defense_script.decision(their_team, our_team, ball, your_side, half, time_left, our_score,
                                                their_score)
        else:
            decision2 = manager_script.decision(their_team, our_team, ball, your_side, half, time_left, our_score,
                                                their_score)

        done = f_game.update(final_move, decision2, screen=None, start=0)
        state_new = agent.get_state(f_game)

        f_game.updated_dt()

        rwd = reward(state_new)
        encoded_state_new_state = get_1D_arry_from_dict(state_new)
        encoded_state_old_state = get_1D_arry_from_dict(state_old)
        encoded_final_move = get_1D_action(final_move)

        agent.train_short_memory(encoded_state_old_state, encoded_final_move, rwd, encoded_state_new_state, done)
        # remember
        agent.remember(encoded_state_old_state, encoded_final_move, rwd, encoded_state_new_state, done)

        if done:
            # train long memory, plot result
            f_game.reset_game()
            agent.n_games += 1
            agent.train_long_memory()

            print('Game', agent.n_games)

            num_games -= 1
            if num_games == 0:
                file_name = 'model_' + str(model_index) + '.pt'
                agent.model.save(file_name)
                agent.n_games = 0
                num_games = 1000
                model_index += 1
    return
    # plot_scores.append(max_score)
    # total_score += max_score
    # mean_score = total_score / agent.n_games
    # plot_mean_scores.append(mean_score)
    # plot(plot_scores, plot_mean_scores)


def get_1D_arry_from_dict(state):
    # state = [our_team, their_team, ball, your_side, half, time_left, our_score, their_score]
    our_team, their_team, ball, your_side, half, time_left, our_score, their_score = state
    arr = list()
    for player in our_team:
        for key in player.keys():
            arr.append(player[key])
    for player in their_team:
        for key in player.keys():
            arr.append(player[key])
    for item in ball.keys():
        arr.append(ball[item])
    arr.append(1 if your_side == "Right" else 0)
    arr.append(half)
    arr.append(time_left)
    arr.append(our_score)
    arr.append(their_score)
    return arr


def get_1D_action(action):
    arr = list()
    for player in action:
        for key in player.keys():
            arr.append(player[key])
    return arr


if __name__ == '__main__':
    train()
