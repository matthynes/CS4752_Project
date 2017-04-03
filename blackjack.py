import random


# the Game class facilitates the game operations such as dealing cards and determining winners
class Game:
    # start a game of blackjack, returns a random initial state
    def __init__(self):
        self.status = 1  # 1=in progress; 2=player won; 3=dealer won/player loses/draw
        self.player_hand = self.add_card((0, False))
        self.player_hand = self.add_card(self.player_hand)
        self.dealer_hand = self.add_card((0, False))

        # evaluate if player wins from first hand
        if self.total_value(self.player_hand) == 21:
            if self.total_value(self.dealer_hand) != 21:
                self.status = 2  # player wins after first deal!
            else:
                self.status = 3  # draw

        self.state = (self.player_hand, self.dealer_hand, self.status)

    def get_status(self):
        return self.status

    def get_player_hand(self):
        return self.player_hand

    def get_dealer_hand(self):
        return self.dealer_hand

    def get_state(self):
        return self.state

    # A hand is a tuple e.g. (14, False) is a total card value of 14 without a usable ace
    # This function accepts a hand and determines if it has a usable Ace.
    # An Ace is usable if it has a value of 11 without busting the hand.
    def usable_ace(self, hand):
        val, ace = hand
        return ace and ((val + 10) <= 21)

    def total_value(self, hand):
        val, ace = hand
        if self.usable_ace(hand):
            return val + 10
        else:
            return val

    def add_card(self, hand):
        val, ace = hand

        card = random.randint(1, 13)
        if card > 10:
            card = 10
        if card == 1:
            ace = True

        return val + card, ace

    # The first is first dealt a single card, this method finishes off his hand
    def eval_dealer(self, hand):
        while self.total_value(hand) < 17:
            hand = self.add_card(hand)
        return hand

    # state: (player total, usable_ace), (dealer total, usable ace), game status; e.g. ((15, True), (9, False), 1)
    # stay or hit => dec == 0 or 1
    def play(self, decision):
        # evaluate
        player_hand = self.get_state()[0]  # val, usable ace
        dealer_hand = self.get_state()[1]
        if decision == 0:  # action = stay
            # evaluate game; dealer plays
            dealer_hand = self.eval_dealer(dealer_hand)

            player_tot = self.total_value(player_hand)
            dealer_tot = self.total_value(dealer_hand)
            status = 1
            if dealer_tot > 21:
                status = 2  # player wins
            elif dealer_tot == player_tot:
                status = 3  # draw
            elif dealer_tot < player_tot:
                status = 2  # player wins
            elif dealer_tot > player_tot:
                status = 4  # player loses

        elif decision == 1:  # action = hit
            # if hit, add new card to player's hand
            player_hand = self.add_card(player_hand)
            d_hand = self.eval_dealer(dealer_hand)
            player_tot = self.total_value(player_hand)
            status = 1
            if player_tot == 21:
                if self.total_value(d_hand) == 21:
                    status = 3  # draw
                else:
                    status = 2  # player wins!
            elif player_tot > 21:
                status = 4  # player loses
            elif player_tot < 21:
                # game still in progress
                status = 1
        self.state = (player_hand, dealer_hand, status)
