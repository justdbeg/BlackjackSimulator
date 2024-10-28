# casino_rules.py

class CasinoRules:
    def __init__(self, 
                 decks=6,                        # Number of decks in play (typically 6 or 8)
                 dealer_hits_soft_17=True,       # Dealer hits on soft 17 (True) or stands (False)
                 double_after_split=True,        # Player can double after splitting a hand
                 double_on_any_two=True,         # Player can double on any two cards
                 max_splits=4,                   # Maximum number of hands player can split to
                 resplit_aces=True,              # Player can resplit aces
                 hit_split_aces=False,           # Player can hit split aces (False = only one card dealt)
                 surrender_option='late',        # Surrender rule ('late' or None if not allowed)
                 blackjack_payout=1.5            # Payout for blackjack (3:2 = 1.5, 6:5 = 1.2)
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

    def __repr__(self):
        return (f"Casino Rules: {self.decks} decks, "
                f"Dealer {'hits' if self.dealer_hits_soft_17 else 'stands'} on soft 17, "
                f"{'Double after split allowed' if self.double_after_split else 'No double after split'}, "
                f"{'Double on any two cards' if self.double_on_any_two else 'Double restricted'}, "
                f"Max Splits: {self.max_splits}, "
                f"{'Resplit aces allowed' if self.resplit_aces else 'No resplit aces'}, "
                f"{'Hit allowed on split aces' if self.hit_split_aces else 'Hit not allowed on split aces'}, "
                f"Surrender: {self.surrender_option}, "
                f"Blackjack Payout: {'3:2' if self.blackjack_payout == 1.5 else '6:5'}")
