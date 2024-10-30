# simulation.py

import random
from src.betting_strategy import calculate_bet
from src.basic_strategy import basic_strategy
from src.casino_rules import CasinoRules #imports the rules for a casino

class BlackjackSimulation:
    def __init__(self, casino_rules):
        # Store the casino rules object to access the rules as needed
        self.casino_rules = casino_rules
        self.shoe = self.casino_rules.initialize_shoe()
        self.running_count = 0
        self.true_count = 0

    def deal_card(self):
        # Use the CasinoRules class's deal_card method to manage reshuffle and count
        card = self.casino_rules.deal_card()
        print(f"Dealt card: {card}, Updated Running Count: {self.casino_rules.running_count}")
        return card

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
        is_soft = 11 in player_hand and player_value <= 21  # Aces counted as 11 are treated as soft totals

        # Check if hand is a pair (both cards are the same)
        if len(player_hand) == 2 and player_hand[0] == player_hand[1]:
            action = basic_strategy['pairs'].get(player_hand[0], {}).get(dealer_card, 'stand')
        # Check if hand is a soft total (contains an Ace counted as 11)
        elif is_soft:
            action = basic_strategy['soft_totals'].get(player_value, {}).get(dealer_card, 'hit')
        # For hard totals, reference the strategy matrix directly
        else:
            action = basic_strategy['hard_totals'].get(player_value, {}).get(dealer_card, 'hit')

        print(f"Player hand: {player_hand} (Value: {player_value}, {'Soft' if is_soft else 'Hard'}), Dealer card: {dealer_card}, Action: {action}")

        return action

    def simulate_hand(self, target_total=None):
        print(f"--- Simulating Hand ---")
        print(f"Starting running count for this hand: {self.running_count}")

        # Initial Dealing Sequence (Player -> Dealer -> Player -> Dealer)
        player_hand = [self.deal_card()]
        dealer_hand = [self.deal_card()]  # Dealer's first card (face-up)

        player_hand.append(self.deal_card())
        dealer_hand.append(self.deal_card())  # Dealer's second card (face-down)

        # Calculate initial totals
        player_total = self.calculate_hand_value(player_hand)
        dealer_total = self.calculate_hand_value(dealer_hand)

        # Output adjustments
        print(f"Player starting hand: {player_hand} (Total: {player_total})")
        print(f"Dealer showing: {dealer_hand[0]}")  # Only show the dealer's face-up card

        # Check for natural blackjack (Player and Dealer)
        if player_total == 21 or dealer_total == 21:
            if player_total == 21 and dealer_total == 21:
                print("Both player and dealer have blackjack. Push - Tie game.")
                return "Push - Tie game."
            elif player_total == 21:
                print("Player has a natural blackjack! Player wins with a 3:2 payout.")
                return "Player wins with blackjack!"
            elif dealer_total == 21:
                print("Dealer has a natural blackjack! Dealer wins.")
                return "Dealer wins with blackjack!"

        # Peek if dealer's face-up card is an Ace or a ten-value card (typically only if Ace)
        if dealer_hand[0] == 11:
            print("Dealer peeks for blackjack...")
            if dealer_total == 21:
                print("Dealer has a blackjack!")
                if player_total == 21:
                    print("Player also has blackjack. Push - Tie game.")
                    return "Push - Tie game."
                else:
                    print("Player does not have blackjack. Dealer wins.")
                    return "Dealer wins with blackjack!"
            else:
                print("Dealer does not have a blackjack. Continuing with player turn.")
                
        # Initialize list to manage split hands
        player_hands = [player_hand]
        hand_index = 0  # Keep track of which hand is being played

        # Play each player hand (including split hands)
        while hand_index < len(player_hands):
            hand = player_hands[hand_index]
            first_action = True

            while True:
                action = self.get_action(hand, dealer_hand[0])
                print(f"Player chooses to {action} with hand {hand} (total: {self.calculate_hand_value(hand)}) against dealer's {dealer_hand[0]}")

                # Handle splits
                if action == 'split' and len(hand) == 2 and hand[0] == hand[1]:
                    if len(player_hands) < self.casino_rules.max_splits:
                        player_hands.append([hand[0], self.deal_card()])
                        hand[1] = self.deal_card()  # Replace the second card of current hand
                        print(f"Player splits: New hands: {player_hands}")
                        first_action = True  # Reset first action for the new split hand
                    else:
                        print("Maximum splits reached.")
                        action = 'hit'  # If unable to split, proceed to hit
                
                elif action == 'hit':
                    hand.append(self.deal_card())
                    if self.calculate_hand_value(hand) > 21:
                        print("Player busts!")
                        break

                elif action == 'stand':
                    print("Player stands.")
                    break

                elif action == 'double' and first_action and self.casino_rules.double_on_any_two:
                    print("Player doubles down.")
                    hand.append(self.deal_card())
                    break

                # Mark that the first action has been taken
                first_action = False

            hand_index += 1  # Move to the next hand

        # Dealer's turn - only if the player did not bust on all hands
        for hand in player_hands:
            if self.calculate_hand_value(hand) <= 21:
                break
        else:
            print("All player hands have busted. Dealer wins.")
            return "Dealer wins!"

        print(f"Dealer's full hand: {dealer_hand}")

        # Dealer hits until 17 or higher
        while self.calculate_hand_value(dealer_hand) < 17 or (
            self.casino_rules.dealer_hits_soft_17 and self.calculate_hand_value(dealer_hand) == 17 and 11 in dealer_hand):
            dealer_hand.append(self.deal_card())
            print(f"Dealer hits: {dealer_hand}")
            if self.calculate_hand_value(dealer_hand) > 21:
                print("Dealer busts! Player wins!")
                return "Player wins!"

        # Determine the outcome if neither busts
        dealer_value = self.calculate_hand_value(dealer_hand)
        for hand in player_hands:
            player_value = self.calculate_hand_value(hand)
            print(f"Final Player hand: {hand} (Value: {player_value})")
            if player_value > dealer_value:
                print("Player wins!")
            elif player_value < dealer_value:
                print("Dealer wins!")
            else:
                print("Push - Tie game.")

        return "Completed"
