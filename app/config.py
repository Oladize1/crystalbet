from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Function to retrieve and cast environment variables with default values
def get_env_variable(var_name, default_value=None, var_type=str):
    """Retrieve an environment variable and cast it to the specified type."""
    value = os.getenv(var_name, default_value)
    if value is None:
        raise ValueError(f"Environment variable '{var_name}' is not set.")
    
    try:
        return var_type(value)
    except ValueError:
        raise ValueError(f"Environment variable '{var_name}' cannot be cast to {var_type.__name__}.")

# CORS allowed origins from the environment (split for use in FastAPI)
ALLOW_ORIGINS = get_env_variable("ALLOW_ORIGINS", "*").split(",")

# Trusted hosts for the application
TRUSTED_HOSTS = get_env_variable("TRUSTED_HOSTS", "localhost,127.0.0.1").split(",")

# Secret key for JWT or other purposes
SECRET_KEY = get_env_variable("SECRET_KEY")

# Algorithm for JWT
ALGORITHM = get_env_variable("ALGORITHM", "HS256")

# Token expiration time in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = get_env_variable("ACCESS_TOKEN_EXPIRE_MINUTES", 30, int)

# MongoDB configuration
MONGO_URI = get_env_variable("MONGO_URI")
DATABASE_NAME = get_env_variable("DATABASE_NAME", "crystalbet")

# Connection Pool Sizes
MAX_POOL_SIZE = get_env_variable("MAX_POOL_SIZE", 100, int)
MIN_POOL_SIZE = get_env_variable("MIN_POOL_SIZE", 10, int)

# Optional: Log configuration loading
print("Configuration loaded successfully.")
