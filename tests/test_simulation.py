# tests/test_simulation.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import patch
from src.simulation import BlackjackSimulation
from src.casino_rules import CasinoRules
from src.basic_strategy import basic_strategy

class TestBlackjackSimulation(unittest.TestCase):

    def setUp(self):
        """Set up the initial configuration for the Blackjack game."""
        self.casino_rules = CasinoRules(
            decks=8,
            dealer_hits_soft_17=False,
            double_after_split=True,
            double_on_any_two=True,
            max_splits=4,
            resplit_aces=False,
            hit_split_aces=False,
            surrender_option='None',
            blackjack_payout=1.5,
            penetration=0.75
        )
        self.blackjack_sim = BlackjackSimulation(self.casino_rules)

    def test_basic_strategy_hard_totals(self):
        """Test that the player's action matches basic strategy for hard totals."""
        test_cases = [
            # (player hand, dealer card, expected action)
            ([10, 6], 10, 'hit'),
            ([10, 7], 6, 'stand'),
            ([3, 6], 6, 'double'),
            ([13, 5], 6, 'stand'),
        ]

        for player_hand, dealer_card, expected_action in test_cases:
            action = self.blackjack_sim.get_action(player_hand, dealer_card)
            self.assertEqual(action, expected_action, f"Failed for player hand {player_hand} against dealer {dealer_card}")

    def test_basic_strategy_soft_totals(self):
        """Test that the player's action matches basic strategy for soft totals (hands with an Ace valued as 11)."""
        test_cases = [
            # (player hand, dealer card, expected action)
            ([11, 5], 4, 'double'),
            ([11, 6], 7, 'hit'),
            ([11, 4], 6, 'double'),
            ([11, 8], 6, 'double'),
        ]

        for player_hand, dealer_card, expected_action in test_cases:
            action = self.blackjack_sim.get_action(player_hand, dealer_card)
            self.assertEqual(action, expected_action, f"Failed for player hand {player_hand} against dealer {dealer_card}")

    def test_basic_strategy_pairs(self):
        """Test that the player's action matches basic strategy for pairs."""
        test_cases = [
            # (player hand, dealer card, expected action)
            ([8, 8], 6, 'split'),
            ([7, 7], 8, 'hit'),
            ([4, 4], 5, 'split'),
            ([9, 9], 7, 'stand'),
            ([11, 11], 10, 'split'),
        ]

        for player_hand, dealer_card, expected_action in test_cases:
            action = self.blackjack_sim.get_action(player_hand, dealer_card)
            self.assertEqual(action, expected_action, f"Failed for pair {player_hand} against dealer {dealer_card}")

    def test_basic_strategy_after_split(self):
        """Test if the player can correctly perform actions after splitting based on basic strategy."""
        # Mock a scenario where the player splits a pair and then must act on each new hand.
        self.blackjack_sim.shoe = [8, 8, 4, 6, 7, 9]  # Player splits 8s, Dealer shows 6
        dealer_card = self.blackjack_sim.deal_card()
        player_hand = [self.blackjack_sim.deal_card(), self.blackjack_sim.deal_card()]

        # The first action should be split, resulting in two new hands of [8, X]
        action = self.blackjack_sim.get_action(player_hand, dealer_card)
        self.assertEqual(action, 'split', f"Player should split the pair of 8s according to basic strategy.")

        # Verify the new hands are managed correctly
        # Simulate the first split hand
        new_hand_1 = [player_hand[0], self.blackjack_sim.deal_card()]
        action_1 = self.blackjack_sim.get_action(new_hand_1, dealer_card)
        expected_action_1 = 'stand'  # Based on [8, 4] vs dealer's 6

        self.assertEqual(action_1, expected_action_1, f"Expected action after split should be '{expected_action_1}', got '{action_1}'.")

if __name__ == "__main__":
    unittest.main()
