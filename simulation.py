# simulation.py

import random
from betting_strategy import calculate_bet
from basic_strategy import basic_strategy

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

        print(f"Player starting hand: {player_hand} (Total: {player_total})")
        print(f"Dealer showing: {dealer_hand[0]}")  # Only show dealer's face-up card

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

        # Initialize player hands for handling splits
        player_hands = [player_hand]
        current_hand = 0
        max_splits = self.casino_rules.max_splits  # Use casino rules to determine max splits allowed

        # Iterate over all player hands (to handle splitting)
        while current_hand < len(player_hands):
            player_hand = player_hands[current_hand]
            first_action = True
            print(f"\n--- Playing Hand {current_hand + 1} ---")
            print(f"Player's current hand: {player_hand}")

            # Player's Turn for current hand
            while True:
                action = self.get_action(player_hand, dealer_hand[0])
                print(f"Player chooses to {action} with hand {player_hand} (total: {self.calculate_hand_value(player_hand)}) against dealer's {dealer_hand[0]}")

                # Enforce double restrictions based on first action
                if action == 'double' and not first_action:
                    print("Double is not allowed after the first action, switching to 'hit'.")
                    action = 'hit'  # Switch to hit if double isn't allowed
                if action == 'hit':
                    player_hand.append(self.deal_card())
                    if self.calculate_hand_value(player_hand) > 21:
                        print("Player busts!")
                        break
                elif action == 'stand':
                    print("Player stands.")
                    break
                elif action == 'double' and first_action:
                    print("Player doubles down.")
                    player_hand.append(self.deal_card())
                    break  # Ensures no further actions can be taken after doubling
                elif action == 'split':
                    # Check if splitting is allowed (cards must be the same, max splits not exceeded)
                    if len(player_hand) == 2 and player_hand[0] == player_hand[1] and len(player_hands) < max_splits:
                        print("Player splits.")

                        # Create two new hands by splitting the pair
                        new_hand_1 = [player_hand[0], self.deal_card()]
                        new_hand_2 = [player_hand[1], self.deal_card()]

                        # If the player splits Aces, only one card is allowed per new hand
                        if player_hand[0] == 11:
                            print("Split Aces: each hand receives one additional card.")
                            player_hands[current_hand] = new_hand_1
                            player_hands.append(new_hand_2)
                            current_hand += 1  # Move to the next hand
                            continue

                        # For non-Ace splits, replace the current hand and add the second new hand to player_hands
                        player_hands[current_hand] = new_hand_1
                        player_hands.append(new_hand_2)
                        print(f"New hands after split: {new_hand_1} and {new_hand_2}")

                        # Mark that the first action has been taken
                        first_action = False
                        continue
                    
                        # Move to the next hand
                    current_hand += 1

                    # Dealer's Turn (Standard rules: must hit if < 17, must stand if >= 17, can hit on soft 17 based on rules)
                    print(f"\nDealer's full hand: {dealer_hand}")
                    
                    while self.calculate_hand_value(dealer_hand) < 17 or (
                            self.casino_rules.dealer_hits_soft_17 and self.calculate_hand_value(dealer_hand) == 17 and 11 in dealer_hand):
                        dealer_hand.append(self.deal_card())
                        print(f"Dealer hits: {dealer_hand}")
                        if self.calculate_hand_value(dealer_hand) > 21:
                            print("Dealer busts! Player wins!")
                            return "Player wins!"

                    # Determine the outcome for each player hand if neither busts
                    dealer_value = self.calculate_hand_value(dealer_hand)
                    results = []

                    for index, hand in enumerate(player_hands):
                        player_value = self.calculate_hand_value(hand)
                        print(f"\nFinal Player hand {index + 1}: {hand} (Value: {player_value})")
                        print(f"Final Dealer hand: {dealer_hand} (Value: {dealer_value})")

                        if player_value > dealer_value:
                            print("Player wins!")
                            results.append("Player wins!")
                        elif player_value < dealer_value:
                            print("Dealer wins!")
                            results.append("Dealer wins!")
                        else:
                            print("Push - Tie game.")
                            results.append("Push - Tie game.")

                    return results
