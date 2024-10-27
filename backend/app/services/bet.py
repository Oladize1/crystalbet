# services/bet.py (Service Layer for Bet Logic)

from app.models.bet import BetModel
from app.schemas.bet import BetCreate, BetResponse
from app.models.user import UserModel

class BetService:

    @staticmethod
    async def get_all_bets(skip: int = 0, limit: int = 10):
        return await BetModel.get_all(skip=skip, limit=limit)

    @staticmethod
    async def get_live_bets():
        return await BetModel.get_live_bets()

    @staticmethod
    async def book_bet(bet: BetCreate, user: UserModel):
        # Calculate potential win based on bet amount and odds
        potential_win = bet.bet_amount * bet.odds
        bet_data = {
            "user_id": str(user.id),
            "match_id": bet.match_id,
            "bet_amount": bet.bet_amount,
            "potential_win": potential_win,
            "odds": bet.odds,
            "is_live": False,  # Default to non-live bet
        }
        return await BetModel.create(bet_data=bet_data)

    @staticmethod
    async def get_bet_slip(user: UserModel):
        user_bets = await BetModel.get_by_user_id(user_id=str(user.id))
        total_bets = len(user_bets)
        total_amount = sum(bet.bet_amount for bet in user_bets)
        total_potential_win = sum(bet.potential_win for bet in user_bets)

        return {
            "bets": user_bets,
            "total_bets": total_bets,
            "total_amount": total_amount,
            "total_potential_win": total_potential_win
        }

    @staticmethod
    async def get_bets_with_odds_less_than(value: float):
        return await BetModel.get_by_odds(max_odds=value)
