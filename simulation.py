# simulation.py

import random
from betting_strategy import calculate_bet
from basic_strategy import basic_strategy  # Import the strategy matrix

class BlackjackSimulation:
    def __init__(self, decks=6, base_bet=10):
        self.decks = decks
        self.base_bet = base_bet
        self.shoe = self.initialize_shoe()
        self.running_count = 0
        self.true_count = 0

    def initialize_shoe(self):
        single_deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
        shoe = single_deck * self.decks
        random.shuffle(shoe)
        return shoe

    def deal_card(self):
        if len(self.shoe) == 0:
            self.shoe = self.initialize_shoe()
            self.running_count = 0

        card = self.shoe.pop()
        self.update_count(card)
        print(f"Dealt card: {card}, Updated Running Count: {self.running_count}")
        return card

    def update_count(self, card):
        if card in [2, 3, 4, 5, 6]:  # Low cards (2-6) increase the count
            self.running_count += 1
        elif card in [10, 11]:       # High cards (10, J, Q, K, A) decrease the count
            self.running_count -= 1

    def calculate_true_count(self):
        decks_remaining = len(self.shoe) / 52
        if decks_remaining > 0:
            self.true_count = self.running_count / decks_remaining
        return self.true_count

    def calculate_hand_value(self, hand):
        """Calculates the total value of a hand, treating Ace as 1 or 11."""
        total = 0
        aces = 0
        for card in hand:
            if card == 11:  # Ace
                aces += 1
                total += 11
            else:
                total += card
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def get_action(self, player_hand, dealer_card):
        """Determines the player's optimal action based on basic strategy."""
        player_value = self.calculate_hand_value(player_hand)

        # Check if hand is a pair (both cards are the same)
        if len(player_hand) == 2 and player_hand[0] == player_hand[1]:
            action = basic_strategy['pairs'].get(player_hand[0], {}).get(dealer_card, 'stand')
        # Check if hand is a soft total (contains an Ace counted as 11)
        elif 11 in player_hand:
            action = basic_strategy['soft_totals'].get(player_value, {}).get(dealer_card, 'hit')
        # Hard totals
        else:
            action = basic_strategy['hard_totals'].get(player_value, {}).get(dealer_card, 'hit')

        return action

    # In simulation.py

    def simulate_hand(self):
        print(f"Starting running count for this hand: {self.running_count}")

        # Player's initial hand and dealer's up card
        player_hand = [self.deal_card(), self.deal_card()]
        dealer_card = self.deal_card()
        
        print(f"Player starting hand: {player_hand}")
        print(f"Dealer showing: {dealer_card}")

        # Player's turn using basic strategy
        while True:
            action = self.get_action(player_hand, dealer_card)
            print(f"Player chooses to {action}.")

            if action == 'hit':
                player_hand.append(self.deal_card())
                if self.calculate_hand_value(player_hand) > 21:
                    print("Player busts!")
                    return "Busts"  # Return bust outcome
            elif action == 'stand':
                print("Player stands.")
                break
            elif action == 'double':
                print("Player doubles down.")
                player_hand.append(self.deal_card())
                break
            elif action == 'split':
                print("Player splits.")
                # Implement split logic if desired

        # Dealer's turn (standard rules)
        dealer_hand = [dealer_card, self.deal_card()]
        print(f"Dealer's full hand: {dealer_hand}")

        while self.calculate_hand_value(dealer_hand) < 17:
            dealer_hand.append(self.deal_card())
            print(f"Dealer hits: {dealer_hand}")
            if self.calculate_hand_value(dealer_hand) > 21:
                print("Dealer busts! Player wins!")
                return "Player wins!"

        # Determine the outcome
        player_value = self.calculate_hand_value(player_hand)
        dealer_value = self.calculate_hand_value(dealer_hand)

        print(f"Final Player hand: {player_hand} (Value: {player_value})")
        print(f"Final Dealer hand: {dealer_hand} (Value: {dealer_value})")
        
        if player_value > dealer_value:
            print("Player wins!")
            return "Player wins!"
        elif player_value < dealer_value:
            print("Dealer wins!")
            return "Dealer wins!"
        else:
            print("Push - Tie game.")
            return "Push - Tie game."

