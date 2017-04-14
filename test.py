from blackjack import Blackjack
import random
import copy

def draw_card_limited(deck, hand):
    val, ace = hand
    max = sum(deck[1])
    pick = random.uniform(0, max)
    current = 0
    for i, j in enumerate(deck[1]):
        current += j
        if current > pick:
            deck[1][i] -= 1
            card = deck[0][i]
    if card == 1:
        ace = True
    print("Total: ", val, " New Card: ", card)
    return (val + card, ace), deck

def roulette(deck):
    max = sum(deck[1])
    pick = random.uniform(0, max)
    current = 0
    for i, j in enumerate(deck[1]):
        current += j
        if current > pick:
            return deck[0][i]


def mod (a, b):
    a = a+1
    b = b+a

    return a, b


def main():
    a = 4
    b = 5
    print (a, " ", b)
    a, b = mod(a, b)
    print(a, " ", b)


if __name__ == "__main__":
    main()




 # Start a new game
            game = Blackjack()

            state = game.get_state()
            player_hand = game.get_player_hand()
            dealer_hand = game.get_dealer_hand()
            status = game.get_status()

            # If player's total is less than 11, draw another card
            # while player_hand[0] < 11:
            #    player_hand = game.draw(player_hand)
            #    state = (player_hand, dealer_hand, status)
            rl_state = self.get_rl_state(state, game)  # Convert to condensed RL state

            # Create dictionary to temporarily hold the current game's state-actions
            returns = {}  # (state, decision): reward
            while game.get_status() == 1:  # While game state is not terminal
                # Epsilon-greedy action selection
                action_probs = self.get_q_reward(rl_state, q_t)
                if random.random() < EPISILON:
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