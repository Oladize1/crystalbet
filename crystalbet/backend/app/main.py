import logging
from logging.handlers import RotatingFileHandler
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from api import auth, bets, admin, payments, transactions
from db import MongoDBConnection
from core.config import settings

# Environment variables
ALLOW_ORIGINS = os.environ.get("ALLOW_ORIGINS", settings.ALLOW_ORIGINS)
TRUSTED_HOSTS = os.environ.get("TRUSTED_HOSTS", settings.TRUSTED_HOSTS)

# Log file configuration
LOG_FILE = 'app.log'
MAX_LOG_BYTES = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 5  # Keep more backups

# Function to set up rotating log file handler
def setup_logging():
    try:
        file_handler = RotatingFileHandler(
            LOG_FILE, maxBytes=MAX_LOG_BYTES, backupCount=BACKUP_COUNT
        )
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)  # Debugging logs on console

        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[file_handler, console_handler]
        )
    except (PermissionError, FileNotFoundError) as file_error:
        print(f"File logging error: {file_error}")
        exit(1)
    except Exception as e:
        print(f"Unexpected error while setting up logging: {e}")
        exit(1)

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CRYSTALBET API",
    description="API for managing bets, payments, transactions, and administration",
    version="1.0.0"
)

# Middleware setup
def setup_middleware(app: FastAPI):
    try:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=ALLOW_ORIGINS.split(","),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        logger.debug("CORS middleware setup completed.")
    except Exception as e:
        logger.error(f"Error setting up CORS middleware: {e}")

    try:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=TRUSTED_HOSTS.split(","),
        )
        logger.debug("Trusted Host middleware setup completed.")
    except Exception as e:
        logger.error(f"Error setting up Trusted Hosts middleware: {e}")

setup_middleware(app)

# Include routers for different modules
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(bets.router, prefix="/bets", tags=["Bets"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(payments.router, prefix="/payments", tags=["Payments"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

# Health Check Endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Root route
@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to CRYSTALBET API"}

# MongoDB connection setup
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application...")
    try:
        await MongoDBConnection.connect()
        logger.info("MongoDB connection established successfully.")
    except Exception as e:
        logger.critical(f"Failed to initialize MongoDB connection: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application...")
    try:
        await MongoDBConnection.close_connection()
        logger.info("MongoDB connection closed successfully.")
    except Exception as e:
        logger.error(f"Failed to close MongoDB connection: {e}")
        raise HTTPException(status_code=500, detail="Database disconnection error")

# 404 Error handler
@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"404 Error at {request.url}: {exc.detail}")
    return JSONResponse(
        status_code=404,
        content={"message": exc.detail or "Resource not found"},
    )

# General Exception Handler
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception at {request.url}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error. Please try again later."},
    )

# HTTPException handler for more specific status code handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTP Exception: {exc.status_code} at {request.url}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )
