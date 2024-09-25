from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from routes import auth, bets, admin, payments
from database import init_db, MongoDBConnection  # Import correct init and close
from config import ALLOW_ORIGINS, TRUSTED_HOSTS
import logging

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log"),  # Log to a file
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Middleware setup
def setup_middleware(app: FastAPI):
    """Setup middleware for the application."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOW_ORIGINS,  # Ensure this contains trusted origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=TRUSTED_HOSTS,  # Ensure this is a whitelist of trusted hosts
    )

setup_middleware(app)

# Include routers for various functionalities
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(bets.router, prefix="/bets", tags=["Bets"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(payments.router, prefix="/payments", tags=["Payments"])

@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to CRYSTALBET API"}

# Startup event for initializing MongoDB connection
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application...")
    try:
        await init_db()  # Ensure MongoDB is connected
        logger.info("MongoDB connection initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize MongoDB connection: {e}")
        raise e  # Let FastAPI handle the error gracefully

# Shutdown event for closing MongoDB connection
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application...")
    try:
        await MongoDBConnection.close_connection()  # Call the correct close method
        logger.info("MongoDB connection closed successfully")
    except Exception as e:
        logger.error(f"Failed to close MongoDB connection: {e}")
        raise e  # Let FastAPI handle the error gracefully

# Exception handling for 404 not found
@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc):
    logger.warning(f"404 error at {request.url}: {exc}")
    return JSONResponse(
        status_code=404,
        content={"message": "Resource not found"},
    )

# Error handling for unexpected server errors
@app.exception_handler(Exception)  # Catch all exceptions
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {exc} at {request.url}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )
