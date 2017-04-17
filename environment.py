import random
import numpy as np
from matplotlib import pyplot, cm
from mpl_toolkits.mplot3d import Axes3D

from settings import *
from blackjack import Blackjack

"""This is the environment the Reinforcement Learning agent will use. It uses Q-learning with Monte Carlo (random 
sampling) methods to play_game a game of blackjack. Much of this code was inspired by Chapter 5 in the text 
'Reinforcement 
Learning: An Introduction' by R. Sutton and A. Barto"""


class RLEnvironment:
    def __init__(self):
        # Create a list of all possible states
        self.states = []
        for card in range(1, 11):
            for val in range(11, 22):
                self.states.append((val, False, card))
                self.states.append((val, True, card))

        # Create Q-value (action-value) look up table of all possible state-actions and their values
        self.q_table = {}
        for state in self.states:
            self.q_table[(state, 0)] = 0.0
            self.q_table[(state, 1)] = 0.0

        # Dictionary of state-actions to record how many times a state-action pair has been chosen
        self.counts = {}
        for sa in self.q_table:
            self.counts[sa] = 0

        self.figure = pyplot.figure(figsize=(20, 12))

    def get_states(self):
        return self.states

    def get_q_table(self):
        return self.q_table

    def get_counts(self):
        return self.counts

    # Calculate the reward of the game: +1 for winning, 0 for a draw, or -1 for losing
    def get_reward(self, result):
        return 3 - result

    # Recalculate the average rewards for lookup table
    def update_table(self, q_table, q_count, returns):
        for key in returns:
            q_table[key] = q_table[key] + (1 / q_count[key]) * (returns[key] - q_table[key])
        return q_table

    # returns Q-value/avg rewards for each action given a state
    def get_q_reward(self, state, q_table):
        stay = q_table[(state, 0)]
        hit = q_table[(state, 1)]
        return np.array([stay, hit])

    # Converts a game state formatted as ((player_total, ace), (dealer_total, ace), status) to a condensed state
    # formatted as (player total, usable ace, dealer card). This isn't necessary but makes it easier to work with.
    def get_rl_state(self, state, game):
        player_hand, dealer_hand, status = state
        player_val, player_ace = player_hand
        return player_val, player_ace, game.dealer_first_card

    def visualize(self, index, q_table):

        ax = self.figure.add_subplot(int('23' + str(index + 1)), projection='3d')
        ax.set_title('Test for Scripted Deck' + str(index + 1))
        ax.set_xlabel('Player Card')
        ax.set_ylabel('Dealer Card')
        ax.set_zlabel('Q Value')

        x, y, z = [], [], []
        for state in self.get_states():
            if state[0] > 11 and not state[1] and state[2] < 21:
                x.append(state[0])
                y.append(state[2])
                q_val = max([q_table[(state, 0)], q_table[(state, 1)]])  # select the most likely action
                z.append(q_val)
        ax.azim = 230
        ax.plot_trisurf(x, y, z, linewidth=.02, cmap=cm.jet)

    def run_Black_Jack_environment(self, q_t, q_c, mode):
        # Start a new game
        game = Blackjack(mode)

        state = game.get_state()

        rl_state = self.get_rl_state(state, game)  # Convert to condensed RL state

        # Create dictionary to temporarily hold the current game's state-actions
        returns = {}  # (state, decision): reward
        while game.get_status() == 1:  # While game state is not terminal
            # Epsilon-greedy action selection
            action_probs = self.get_q_reward(rl_state, q_t)
            if random.random() < EPSILON:
                decision = random.randint(0, 1)
            else:
                decision = np.argmax(action_probs)  # Select an action with the highest probability
            sa = (rl_state, decision)
            # Add an action-value pair to returns list. Default value is 0
            returns[sa] = 0
            q_c[sa] += 1  # Increment average counter

            game.play_game(decision)  # Make a move
            state = game.get_state()  # Get the new game state
            rl_state = self.get_rl_state(state, game)  # Compress state
        # After a game is finished, assign rewards to all state-actions that took place in the game
        for key in returns:
            returns[key] = self.get_reward(state[2])
        q_t = self.update_table(q_t, q_c, returns)

        return q_t, q_c

    def main(self):
        print("Gonna learn real good.")
        q_t = self.get_q_table()
        q_c = self.get_counts()

        for i in range(EPOCHS):
            q_t, q_c = self.run_Black_Jack_environment(q_t, q_c, G_Mode)

        print("Finished learning.")

        for i in range(5):
            print("Running Test: ", i + 1, " Of 5")
            q_t, q_c = self.run_Black_Jack_environment(q_t, q_c, i)
            self.visualize(i, q_t)
        pyplot.savefig('fig.png')

        with open('results.txt', 'w') as file:
            for key, val in q_t.items():
                file.write(str(key) + ':' + str(val) + '\n')


if __name__ == '__main__':
    rl_e = RLEnvironment()
    rl_e.main()
