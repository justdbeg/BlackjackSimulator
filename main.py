# main.py

from simulation import BlackjackSimulation

def automated_test(num_hands=10):
    blackjack_sim = BlackjackSimulation(decks=6, base_bet=10)
    results = {"Player Wins": 0, "Dealer Wins": 0, "Pushes": 0, "Busts": 0}

    for i in range(num_hands):
        print(f"\n--- Simulating Hand {i+1} ---")
        outcome = blackjack_sim.simulate_hand()
        
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
    print("\n--- Automated Test Summary ---")
    print(f"Total Hands Simulated: {num_hands}")
    for result, count in results.items():
        print(f"{result}: {count}")

def targeted_test():
    blackjack_sim = BlackjackSimulation(decks=6, base_bet=10)
    target_totals = [17, 18, 19, 20]
    results = {total: {"Player Wins": 0, "Dealer Wins": 0, "Pushes": 0, "Busts": 0} for total in target_totals}

    for total in target_totals:
        print(f"\n--- Targeted Test for Player Hard Total {total} ---")
        outcome = blackjack_sim.simulate_hand(target_total=total)
        
        # Track outcomes for reporting
        if outcome == "Player wins!":
            results[total]["Player Wins"] += 1
        elif outcome == "Dealer wins!":
            results[total]["Dealer Wins"] += 1
        elif outcome == "Push - Tie game.":
            results[total]["Pushes"] += 1
        elif outcome == "Busts":
            results[total]["Busts"] += 1

    # Print summary for each target total
    for total, outcome in results.items():
        print(f"\n--- Summary for Hard Total {total} ---")
        for result, count in outcome.items():
            print(f"{result}: {count}")

def main():
    # Run automated test
    print("\nRunning Automated Test:")
    automated_test(num_hands=10)  # Adjust the number as needed

    # Run targeted test for hard totals of 17, 18, 19, and 20
    print("\nRunning Targeted Test:")
    targeted_test()

if __name__ == "__main__":
    main()
