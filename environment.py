import numpy as np


class RLEnvironment:
    def __init__(self):
        # Create a list of all possible states (ie; all
        self.states = []
        for card in range(1, 11):
            for val in range(11, 22):
                self.states.append((val, False, card))
                self.states.append((val, True, card))

        # Create a dictionary (key-value pairs) of all possible state-actions and their values
        # This creates our Q-value look up table
        self.av = {}
        for state in self.states:
            self.av[(state, 0)] = 0.0
            self.av[(state, 1)] = 0.0

        # Setup a dictionary of state-actions to record how many times we've experienced
        # a given state-action pair. We need this to re-calculate reward averages
        self.counts = {}
        for sa in self.av:
            self.counts[sa] = 0

    # This calculates the reward of the game, either +1 for winning, 0 for draw, or -1 for losing
    # We can determine this by simply substracting the game status value from 3
    def calcReward(outcome):
        return 3 - outcome

    # This recalculates the average rewards for our Q-value look-up table
    def updateQtable(av_table, av_count, returns):
        for key in returns:
            av_table[key] = av_table[key] + (1 / av_count[key]) * (returns[key] - av_table[key])
        return av_table

    # returns Q-value/avg rewards for each action given a state
    def qsv(state, av_table):
        stay = av_table[(state, 0)]
        hit = av_table[(state, 1)]
        return np.array([stay, hit])

    # converts a game state of the form ((player total, ace), (dealer total, ace), status)
    # to a condensed state we'll use for our RL algorithm (player total, usable ace, dealer card)
    def getRLstate(state):
        player_hand, dealer_hand, status = state
        player_val, player_ace = player_hand
        return (player_val, player_ace, dealer_hand[0])
