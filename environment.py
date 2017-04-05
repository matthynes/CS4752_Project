"""This is the environment the Reinforcement Learning agent will use. It uses Q-learning with Monte Carlo (random 
sampling) methods to play a game of blackjack. Much of this code was inspired by Chapter 5 in the text 'Reinforcement 
Learning: An Introduction' by R. Sutton and A. Barto"""


class RLEnvironment:
    def __init__(self):
        # Create a list of all possible states
        self.states = []
        for card in range(1, 11):
            for val in range(11, 22):
                self.states.append((val, False, card))
                self.states.append((val, True, card))

        # Create Q-value look up table of all possible state-actions and their values
        self.q_table = {}
        for state in self.states:
            self.q_table[(state, 0)] = 0.0
            self.q_table[(state, 1)] = 0.0

        # Dictionary of state-actions to record how many times a state-action pair has been chosen
        self.counts = {}
        for sa in self.q_table:
            self.counts[sa] = 0

    # Calculate the reward of the game: +1 for winning, 0 for draw, or -1 for losing
    def get_reward(self, result):
        return 3 - result

    # Recalculate the average rewards for lookup table
    def update_table(self, q_table, q_count, returns):
        for key in returns:
            q_table[key] = q_table[key] + (1 / q_count[key]) * (returns[key] - q_table[key])
        return q_table

    # returns Q-value/avg rewards for each action given a state
    def get_q_reward(self, state, av_table):
        stay = av_table[(state, 0)]
        hit = av_table[(state, 1)]
        return [stay, hit]

    # Converts a game state formatted as ((player_total, ace), (dealer_total, ace), status) to a condensed state
    # formatted as (player total, usable ace, dealer card). This isn't necessary but makes it easier to work with
    def get_rl_state(self, state):
        player_hand, dealer_hand, status = state
        player_val, player_ace = player_hand
        return player_val, player_ace, dealer_hand[0]
