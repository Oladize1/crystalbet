def calculate_bet_odds(stake: float, payout: float) -> float:
    """
    Calculate the odds based on stake and payout.

    Args:
        stake (float): The amount of money staked.
        payout (float): The expected payout.

    Returns:
        float: The calculated odds.
    """
    if stake <= 0:
        raise ValueError("Stake must be greater than zero")
    
    odds = payout / stake
    return odds
