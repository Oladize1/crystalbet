import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from api import auth, bets, admin, payments, transactions
from db import MongoDBConnection  # Removed init_db import
from core.config import settings  # Import settings object

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log"),
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Setup CORS and Trusted Hosts Middleware
def setup_middleware(app: FastAPI):
    """Setup middleware for the application."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.ALLOW_ORIGINS],  # Access ALLOW_ORIGINS from settings
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.TRUSTED_HOSTS.split(","),  # Access TRUSTED_HOSTS from settings and split into a list
    )

setup_middleware(app)

# Include routers for different modules
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(bets.router, prefix="/bets", tags=["Bets"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(payments.router, prefix="/payments", tags=["Payments"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

# Root route
@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to CRYSTALBET API"}

# Startup event for MongoDB connection
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application...")
    try:
        await MongoDBConnection.connect()  # Connect to MongoDB
        logger.info("MongoDB connection initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize MongoDB connection: {e}")
        raise HTTPException(status_code=500, detail="Failed to initialize MongoDB connection")

# Shutdown event for MongoDB disconnection
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application...")
    try:
        await MongoDBConnection.close_connection()  # Close MongoDB connection
        logger.info("MongoDB connection closed successfully")
    except Exception as e:
        logger.error(f"Failed to close MongoDB connection: {e}")
        raise HTTPException(status_code=500, detail="Failed to close MongoDB connection")

# 404 Error Handler
@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"404 error at {request.url}: {exc.detail}")
    return JSONResponse(
        status_code=404,
        content={"message": exc.detail or "Resource not found"},
    )

# General Exception Handler
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {exc} at {request.url}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error. Please try again later."},
    )
