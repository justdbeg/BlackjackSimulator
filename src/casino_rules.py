import random

class CasinoRules:
    def __init__(self, 
                 decks=8,                        # Number of decks in play (typically 6 or 8)
                 dealer_hits_soft_17=False,       # Dealer hits on soft 17 (True) or stands (False)
                 double_after_split=True,        # Player can double after splitting a hand
                 double_on_any_two=True,         # Player can double on any two cards
                 max_splits=4,                   # Maximum number of hands player can split to
                 resplit_aces=False,              # Player can resplit aces
                 hit_split_aces=False,           # Player can hit split aces (False = only one card dealt)
                 surrender_option='None',        # Surrender rule ('late' or None if not allowed)
                 blackjack_payout=1.5,           # Payout for blackjack (3:2 = 1.5, 6:5 = 1.2)
                 penetration=0.75                # Deck penetration level (e.g., 0.75 for 75%)
                 ):
        """
        Initializes the rules for a blackjack game based on casino specifications.

        Parameters:
        - decks: Number of decks in the shoe (typically 6 or 8)
        - dealer_hits_soft_17: True if dealer hits on soft 17, False if stands
        - double_after_split: True if player can double after splitting
        - double_on_any_two: True if player can double on any two cards
        - max_splits: Maximum number of hands player can split to
        - resplit_aces: True if player can resplit aces
        - hit_split_aces: True if player can hit split aces, False if only one card allowed
        - surrender_option: 'late' if late surrender allowed, None if surrender not allowed
        - blackjack_payout: Payout for blackjack (1.5 for 3:2, 1.2 for 6:5)
        - penetration: Fraction of the shoe to be dealt before reshuffling
        """
        self.decks = decks
        self.dealer_hits_soft_17 = dealer_hits_soft_17
        self.double_after_split = double_after_split
        self.double_on_any_two = double_on_any_two
        self.max_splits = max_splits
        self.resplit_aces = resplit_aces
        self.hit_split_aces = hit_split_aces
        self.surrender_option = surrender_option
        self.blackjack_payout = blackjack_payout
        self.penetration = penetration  # Set penetration level
        self.shoe = self.initialize_shoe()
        self.running_count = 0
        self.true_count = 0
        self.cards_dealt = 0  # Track the number of cards dealt

    def initialize_shoe(self):
        """Initializes and shuffles a shoe based on the number of decks."""
        single_deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
        shoe = single_deck * self.decks
        random.shuffle(shoe)
        self.cards_dealt = 0  # Reset cards dealt counter when shoe is reshuffled
        return shoe

    def deal_card(self):
        """Deals a card from the shoe and reshuffles if penetration level is reached."""
        # Reshuffle if we've reached the penetration threshold
        if self.cards_dealt >= len(self.shoe) * self.penetration:
            print("Reshuffling shoe based on penetration level.")
            self.shoe = self.initialize_shoe()
            self.running_count = 0  # Reset running count after reshuffle

        # Deal a card and update counts
        card = self.shoe.pop()
        self.update_count(card)
        self.cards_dealt += 1  # Increment cards dealt counter
        return card

    def update_count(self, card):
        """Updates the Hi-Lo running count based on the card dealt."""
        if card in [2, 3, 4, 5, 6]:  # Low cards (2-6) increase the count
            self.running_count += 1
        elif card in [10, 11]:       # High cards (10, J, Q, K, A) decrease the count
            self.running_count -= 1

    def calculate_true_count(self):
        """Calculates the true count based on remaining decks in the shoe."""
        decks_remaining = len(self.shoe) / 52
        if decks_remaining > 0:
            self.true_count = self.running_count / decks_remaining
        return self.true_count

    def __repr__(self):
        return (f"Casino Rules: {self.decks} decks, "
                f"Dealer {'hits' if self.dealer_hits_soft_17 else 'stands'} on soft 17, "
                f"{'Double after split allowed' if self.double_after_split else 'No double after split'}, "
                f"{'Double on any two cards' if self.double_on_any_two else 'Double restricted'}, "
                f"Max Splits: {self.max_splits}, "
                f"{'Resplit aces allowed' if self.resplit_aces else 'No resplit aces'}, "
                f"{'Hit allowed on split aces' if self.hit_split_aces else 'Hit not allowed on split aces'}, "
                f"Surrender: {self.surrender_option}, "
                f"Blackjack Payout: {'3:2' if self.blackjack_payout == 1.5 else '6:5'}, "
                f"Penetration: {self.penetration * 100}%")
