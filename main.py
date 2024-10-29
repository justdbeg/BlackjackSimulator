# main.py

from casino_rules import CasinoRules
from simulation import BlackjackSimulation

def main():
    # Define specific casino rules (modify as needed for different scenarios)
    casino_rules = CasinoRules(
        decks=8,
        dealer_hits_soft_17=False,
        double_after_split=True,
        double_on_any_two=True,
        max_splits=4,
        resplit_aces=True,
        hit_split_aces=False,
        surrender_option='None',
        blackjack_payout=1.5,
        penetration=0.75
    )

    # Create a simulation with the specified casino rules
    blackjack_sim = BlackjackSimulation(casino_rules)

    # Run automated or targeted tests as needed
    blackjack_sim.simulate_hand()

if __name__ == "__main__":
    main()
