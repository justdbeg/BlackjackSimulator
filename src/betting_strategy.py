# betting_strategy.py

def calculate_bet(true_count, base_bet=10):
    """
    Calculates the bet amount based on the true count using a basic betting strategy.
    
    Parameters:
    - true_count: Current true count in the game.
    - base_bet: Minimum bet amount (default is 10).
    
    Returns:
    - The bet amount based on the true count.
    """
    if true_count >= 4:
        return base_bet * 10  # High bet when true count is very favorable
    elif true_count >= 2:
        return base_bet * 5   # Moderate bet with a positive count
    elif true_count >= 1:
        return base_bet * 2   # Small increase for low positive count
    else:
        return base_bet       # Minimum bet when count is neutral or negative
