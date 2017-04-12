import random
import pickle
import numpy as np

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

    def get_states(self):
        return self.states

    def get_q_table(self):
        return self.q_table

    def get_counts(self):
        return self.counts

    # Calculate the reward of the game: +1 for winning, 0 for draw, or -1 for losing
    def get_reward(self, result):
        return 2 - result

    # Recalculate the average rewards for lookup table
    def update_table(self, q_table, q_count, returns):
        for key in returns:
            q_table[key] = q_table[key] + (1 / q_count[key]) * (returns[key] - q_table[key])
        return q_table

    # returns Q-value/avg rewards for each action given a state
    def get_q_reward(self, state, av_table):
        stay = av_table[(state, 0)]
        hit = av_table[(state, 1)]
        return np.array([stay, hit])

    # Converts a game state formatted as ((player_total, ace), (dealer_total, ace), status) to a condensed state
    # formatted as (player total, usable ace, dealer card). This isn't necessary but makes it easier to work with.
    def get_rl_state(self, state):
        player_hand, dealer_hand, status = state
        player_val, player_ace = player_hand
        return player_val, player_ace, dealer_hand[0]

    def main(self):
        print("Gonna learn real good.")
        q_table = self.get_q_table()
        q_count = self.get_counts()

        for i in range(EPOCHS):
            # Start a new game
            game = Blackjack()

            state = game.get_state()
            player_hand = game.get_player_hand()
            dealer_hand = game.get_dealer_hand()
            status = game.get_status()

            # If player's total is less than 11, draw another card
            while player_hand[0] < 11:
                player_hand = game.draw_card_limitless(player_hand)
                state = (player_hand, dealer_hand, status)
            rl_state = self.get_rl_state(state)  # Convert to condensed RL state

            # Create dictionary to temporarily hold the current game's state-actions
            returns = {}  # (state, decision): reward
            while state[2] == 1:  # While game state is not terminal
                # Epsilon-greedy action selection
                action_probs = self.get_q_reward(rl_state, q_table)
                if random.random() < EPISILON:
                    decision = random.randint(0, 1)
                else:
                    decision = np.argmax(action_probs)  # Select an action with the highest probability
                sa = (rl_state, decision)
                # Add an action-value pair to returns list. Default value is 0
                returns[sa] = 0
                q_count[sa] += 1  # Increment average counter

                game.play_game(decision)  # Make a move
                state = game.get_state()  # Get the new game state
                rl_state = self.get_rl_state(state)  # Compress state
            # After a game is finished, assign rewards to all state-actions that took place in the game
            for key in returns:
                returns[key] = self.get_reward(state[2])
            q_table = self.update_table(q_table, q_count, returns)

        print("Finished learning.")

        with open('results.txt', 'w') as file:
            for key, val in q_table.items():
                file.write(str(key) + ':' + str(val) + '\n')


if __name__ == '__main__':
    rl_e = RLEnvironment()
    rl_e.main()
