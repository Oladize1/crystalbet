from fastapi import APIRouter  # Import APIRouter here
from api.auth import router as auth_router
from api.bets import router as bets_router  # Ensure this line exists
from api.admin import router as admin_router
from api.payments import router as payments_router
from api.transactions import router as transactions_router

# Combine all routers if needed
api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(bets_router, prefix="/bets")
api_router.include_router(admin_router, prefix="/admin")
api_router.include_router(payments_router, prefix="/payments")
api_router.include_router(transactions_router, prefix="/transactions")
