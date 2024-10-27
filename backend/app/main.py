# main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from db.mongodb import init_db, close_db
from core.config import settings
from logging_config import setup_logging, logger  # Import logging setup

# Import all routers
from api.auth import router as auth_router
from api.bets import router as bet_router
from api.match import router as match_router
from api.users import router as user_router
from api.admin import router as admin_router
from api.payments import router as payments_router
from api.transactions import router as transactions_router
from api.casino import router as casino_router
from api.virtuals import router as virtuals_router
from api.coupon import router as coupon_router
from api.main import router as main_router

# Setup logging
setup_logging()

# Initialize FastAPI app
app = FastAPI(
    title="Betting Platform API",
    description="API for betting, casino, virtual sports, and payment management.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enforce HTTPS redirection in production
if settings.ENVIRONMENT == "production":
    app.add_middleware(HTTPSRedirectMiddleware)

# MongoDB connection setup
@app.on_event("startup")
async def startup_db_client():
    await init_db()
    logger.info("Connected to MongoDB.")

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_db()
    logger.info("MongoDB connection closed.")

# Exception handler for common errors
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error occurred at {request.url}: {exc.detail}")
    return {"error": exc.detail, "status_code": exc.status_code}

# Custom 404 error handling
@app.exception_handler(404)
async def not_found_error(request: Request, exc: HTTPException):
    logger.warning(f"404 error - Resource not found at {request.url}")
    return {"error": "Resource not found", "status_code": 404}

# Generic Exception Handler
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.critical(f"An unexpected error occurred at {request.url}: {exc}")
    return {"error": "An unexpected error occurred.", "status_code": 500}

# Include all routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(bet_router, prefix="/api/bets", tags=["Bets"])
app.include_router(match_router, prefix="/api/matches", tags=["Matches"])
app.include_router(user_router, prefix="/api/users", tags=["User Profile"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admin CMS"])
app.include_router(payments_router, prefix="/api/payments", tags=["Payments"])
app.include_router(transactions_router, prefix="/api/transactions", tags=["Transactions"])
app.include_router(casino_router, prefix="/api/casino", tags=["Casino"])
app.include_router(virtuals_router, prefix="/api/virtuals", tags=["Virtual Sports"])
app.include_router(coupon_router, prefix="/api/coupons", tags=["Coupon Check"])
app.include_router(main_router, tags=["General"])

# Root endpoint
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Betting Platform API!"}

# Health check endpoint for monitoring
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "Healthy", "message": "API is up and running!"}
