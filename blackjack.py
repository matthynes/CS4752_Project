"""A simple implementation of a blackjack game. It does not (currently) do splitting or doubling down. 
Some of this code was inspired by, adapted and/or combined from 
https://inst.eecs.berkeley.edu/~cs188/sp08/projects/blackjack/blackjack.py and 
https://github.com/charleswli/python-blackjack"""

import random
import copy
from settings import *


# The Blackjack class facilitates the game operations such as dealing cards and determining winners
# For simplicity and to reduce the size of the state-action lookup table, hands are implemented as tuples formatted
# as: (hand_total, soft_ace)
class Blackjack:
    # start a game of blackjack
    # initial state of game is always random (this is the random sampling part of the MC method)
    def __init__(self):
        self.g_mode = G_Mode
        # Status is an int used to determine the current state of the game.Fs
        # 1=in progress, 2=player wins, 3=draw, 4=dealer wins
        self.newDeck = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [4, 4, 4, 4, 4, 4, 4, 4, 4, 16]]
        self.deck = copy.deepcopy(self.newDeck)
        self.status = 1
        self.player_hand = self.draw((0, False))
        self.player_hand = self.draw(self.player_hand)
        # Dealer starts with one face-up card
        self.dealer_hand = self.draw((0, False))

        # Determine if player wins on the first deal
        if self.total_value(self.player_hand) == 21:
            if self.total_value(self.dealer_hand) != 21:
                self.status = 2  # player wins after first deal
            else:
                self.status = 3  # draw
        # State is a tuple, formatted: ((player_total, soft_ace), (dealer_total, soft_ace), game_status)
        self.state = (self.player_hand, self.dealer_hand, self.status)

    def get_status(self):
        return self.status

    def get_player_hand(self):
        return self.player_hand

    def get_dealer_hand(self):
        return self.dealer_hand

    def get_state(self):
        return self.state

    # This function accepts a hand and determines if it has a 'soft' Ace.
    # An Ace is soft if it has a value of 11 without busting the hand. Otherwise it is 'hard' and has a value of 1.
    def soft_ace(self, hand):
        val, ace = hand
        return ace and ((val + 10) <= 21)

    def total_value(self, hand):
        val, ace = hand
        if self.soft_ace(hand):
            return val + 10  # note that we add 10 and not 11 because the Ace is already in the hand with a val of 1
        else:
            return val

    # Draws a random card and adds it to the hand provided.
    # Suits (except for Ace) don't matter in blackjack so cards are just values 1 - 10.
    def draw_card_limitless(self, hand):
        val, ace = hand
        # Each card has a 1:13 chance of being drawn but max value is 10.
        # Jack, Queen, and King are normally 11, 12, and 13, respectively, but here they are all 10.
        card = random.randint(1, 13)
        if card > 10:
            card = 10
        if card == 1:
            ace = True
        return val + card, ace

    # Draws a random card and adds it to the hand provided. Also removes card from the deck.
    # Suits (except for Ace) don't matter in blackjack so cards are just values 1 - 10.
    # The drawing method uses a deck. Uses a Weighted Roulette method that has its weights changed
    # as more cards are drawn. If and when a deck runs out, a new deck is "Opened"
    def draw_card_limited(self, hand):
        val, ace = hand
        max = sum(self.deck[1])
        if max == 0:
            self.deck = copy.deepcopy(self.newDeck)
            max = sum(self.deck[1])
        pick = random.uniform(0, max)
        current = 0
        for i, j in enumerate(self.deck[1]):
            current += j
            if current > pick:
                self.deck[1][i] -= 1
                card = self.deck[0][i]
                break
        if card == 1:
            ace = True
        return val + card, ace

    def draw(self, hand):
        if self.g_mode == "limited":
            return self.draw_card_limited(hand)
        elif self.g_mode == "limitless":
            return self.draw_card_limitless(hand)

    def eval_dealer(self, hand):
        # Dealer 'hits' until hand totals >= 17
        while self.total_value(hand) < 17:
            hand = self.draw(hand)
        return hand

    # Main gameplay function.
    # Decision = 0 or 1 for stay or hit, respectively
    def play_game(self, decision):
        p_hand = self.get_player_hand()
        d_hand = self.get_dealer_hand()

        if decision == 0:  # stay
            # Evaluates current game state. Dealer's turn.
            d_hand = self.eval_dealer(d_hand)
            player_total = self.total_value(p_hand)
            dealer_total = self.total_value(d_hand)
            self.status = 1
            if dealer_total > 21:
                self.status = 2  # dealer bust, player wins
            elif dealer_total == player_total:
                self.status = 3  # draw
            elif dealer_total < player_total:
                self.status = 2  # player wins
            elif dealer_total > player_total:
                self.status = 4  # player loses
        elif decision == 1:  # hit
            # Add new card to player's hand
            p_hand = self.draw(p_hand)
            d_hand = self.eval_dealer(d_hand)
            player_total = self.total_value(p_hand)
            self.status = 1
            if player_total == 21:
                if self.total_value(d_hand) == 21:
                    self.status = 3  # draw
                else:
                    self.status = 2  # player wins
            elif player_total > 21:
                self.status = 4  # player bust, dealer wins
            elif player_total < 21:
                self.status = 1  # game still in progress
        self.state = (p_hand, d_hand, self.status)
