from fastapi import APIRouter, HTTPException, status
from services.transaction import (
    create_transaction,
    fetch_all_transactions,
    fetch_transaction_by_id,
    update_transaction,
    delete_transaction,
    fetch_transaction_history,
    fetch_bet_history,
    fetch_live_bet,
)
from models.transaction import TransactionSchema, TransactionUpdateSchema
from schemas.transaction import (
    TransactionCreateSchema,
    TransactionResponseSchema,
    TransactionDetailSchema,
    TransactionHistoryResponseSchema,
)

from models.transaction import TransactionSchema, TransactionUpdateSchema

router = APIRouter()

# 1. Home route - Display general information or statistics
@router.get("/", response_model=dict)
async def home_route():
    """
    Home route that shows general information or statistics.
    """
    return {"message": "Welcome to the Betting App", "stats": {"users": 120, "bets": 340}}

# 2. Bets - Fetch all bet transactions
@router.get("/bets", response_model=list)
async def get_all_bets():
    """
    Fetch all bet transactions.
    """
    return await fetch_all_transactions()

# 3. Live Bets - Fetch live bet transactions
@router.get("/live-bets", response_model=list)
async def get_live_bets():
    """
    Fetch live bet transactions.
    """
    return await fetch_live_bet()

# 4. Profile - Fetch user profile details
@router.get("/profile/{user_id}", response_model=dict)
async def get_user_profile(user_id: str):
    """
    Fetch the user's profile information.
    """
    profile = await fetch_transaction_history(user_id)
    if profile:
        return {"profile": profile}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

# 5. Login - Placeholder for login logic
@router.post("/login", response_model=dict)
async def login_route(credentials: dict):
    """
    Handles user login.
    """
    # Placeholder login logic
    return {"message": "User logged in", "user": credentials["username"]}

# 6. Register - Placeholder for registration logic
@router.post("/register", response_model=dict)
async def register_route(user_info: dict):
    """
    Handles user registration.
    """
    # Placeholder registration logic
    return {"message": "User registered successfully", "user": user_info["username"]}

# 7. AZMenu - Fetch sports category (A-Z menu)
@router.get("/AZMenu", response_model=list)
async def get_sports_category():
    """
    Fetch the list of sports categories for betting.
    """
    return await fetch_all_transactions()  # Use a different function for sports category if applicable

# 8. Quick Links - Quick links for users
@router.get("/quick-links", response_model=dict)
async def get_quick_links():
    """
    Fetch quick links for users.
    """
    return {"links": ["Home", "Bets", "Live Bets", "Profile"]}

# 9. Book Bet - Create a new bet (transaction)
@router.post("/book-bet", response_model=dict)
async def book_new_bet(transaction: TransactionSchema):
    """
    Book a new bet.
    """
    return await create_transaction(transaction)

# 10. Bet Slip - Fetch current user's bet slip
@router.get("/betslip/{user_id}", response_model=list)
async def get_bet_slip(user_id: str):
    """
    Fetch the current user's bet slip.
    """
    return await fetch_bet_history(user_id)

# 11. Live - Placeholder for live events (could be bets or match updates)
@router.get("/live", response_model=dict)
async def get_live_events():
    """
    Fetch live events or updates.
    """
    return {"live": "Live events or bets"}

# 12. Sports - Fetch bets by sports category
@router.get("/sports/{category}", response_model=list)
async def get_bets_by_category(category: str):
    """
    Fetch bets by sports category.
    """
    return await fetch_all_transactions()  # Modify this to filter by category

# 13. Live Stream - Fetch live stream of a match
@router.get("/live-stream/{matchId}", response_model=dict)
async def get_live_stream(matchId: str):
    """
    Fetch live stream details of a match.
    """
    return {"matchId": matchId, "live_stream_url": "http://livestream.com/match"}

# 14. Match - Fetch details of a specific match
@router.get("/match/{id}", response_model=dict)
async def get_match_details(id: str):
    """
    Fetch match details.
    """
    return {"match_id": id, "details": "Match details"}

# 15. Casino - Fetch casino game transactions
@router.get("/casino", response_model=list)
async def get_casino_transactions():
    """
    Fetch casino game transactions.
    """
    return await fetch_all_transactions()

# 16. Casino Live - Fetch live casino games
@router.get("/casino-live", response_model=dict)
async def get_live_casino_games():
    """
    Fetch live casino games.
    """
    return {"casino_live": "Live casino games"}

# 17. Virtuals - Fetch virtual sports transactions
@router.get("/virtuals", response_model=list)
async def get_virtual_sports():
    """
    Fetch virtual sports transactions.
    """
    return await fetch_all_transactions()

# 18. Coupon Check - Check the coupon status
@router.get("/coupon-check/{coupon_code}", response_model=dict)
async def check_coupon(coupon_code: str):
    """
    Check the status of a coupon.
    """
    return {"coupon_code": coupon_code, "status": "Valid"}

# 19. CMS - Placeholder for CMS functionality
@router.get("/cms", response_model=dict)
async def cms_route():
    """
    Content Management System (CMS) route.
    """
    return {"cms": "CMS functionality"}

# 20. Odds Less Than - Fetch bets with odds less than a given number
@router.get("/odds-less-than/{odds}", response_model=list)
async def get_bets_by_odds(odds: float):
    """
    Fetch bets with odds less than the given value.
    """
    return await fetch_all_transactions()  # Modify this to filter by odds

# 21. Today's Event - Fetch events happening today
@router.get("/todays-event", response_model=list)
async def get_todays_events():
    """
    Fetch today's events.
    """
    return await fetch_all_transactions()  # Modify this to filter events by today’s date
