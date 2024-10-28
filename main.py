# main.py

from simulation import BlackjackSimulation

def automated_test(num_hands=10):
    blackjack_sim = BlackjackSimulation(decks=6, base_bet=10)
    results = {"Player Wins": 0, "Dealer Wins": 0, "Pushes": 0, "Busts": 0}

    for i in range(num_hands):
        print(f"\n--- Simulating Hand {i+1} ---")
        outcome = blackjack_sim.simulate_hand()  # Ensure simulate_hand returns an outcome
        
        # Track outcomes for reporting
        if outcome == "Player wins!":
            results["Player Wins"] += 1
        elif outcome == "Dealer wins!":
            results["Dealer Wins"] += 1
        elif outcome == "Push - Tie game.":
            results["Pushes"] += 1
        elif outcome == "Busts":
            results["Busts"] += 1

    # Print summary after tests
    print("\n--- Test Summary ---")
    print(f"Total Hands Simulated: {num_hands}")
    for result, count in results.items():
        print(f"{result}: {count}")

def main():
    # Run an automated test of 10 hands
    automated_test(num_hands=10)

if __name__ == "__main__":
    main()
