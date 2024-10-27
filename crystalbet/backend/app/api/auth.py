from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import EmailStr
from core.security import verify_password, create_access_token, hash_password
from services.auth import create_user, authenticate_user, send_reset_password_email, reset_password
from schemas.auth import Token, UserCreate, PasswordResetRequest, PasswordReset
from db.mongodb import get_db
from utils.token import decode_token

router = APIRouter()

# Set up OAuth2 password bearer for protected routes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    """
    Log in a user and generate a JWT token.
    """
    user = await authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    # Generate access token for the user
    access_token = create_access_token({"sub": str(user["_id"])})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db=Depends(get_db)):
    """
    Register a new user.
    """
    existing_user = await db["users"].find_one({"email": user.email})
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    
    # Hash the password before saving
    user.password = hash_password(user.password)
    created_user = await create_user(db, user)
    
    return {"message": "User created successfully", "user_id": str(created_user.inserted_id)}

@router.post("/password-reset-request", status_code=status.HTTP_200_OK)
async def password_reset_request(reset_request: PasswordResetRequest, db=Depends(get_db)):
    """
    Handle password reset request by sending an email with a reset token.
    """
    user = await db["users"].find_one({"email": reset_request.email})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Email not found"
        )
    
    await send_reset_password_email(reset_request.email, db)
    
    return {"message": "Password reset email sent"}

@router.post("/password-reset", status_code=status.HTTP_200_OK)
async def password_reset(reset: PasswordReset, db=Depends(get_db)):
    """
    Handle the password reset using the provided reset token.
    """
    user = await db["users"].find_one({"reset_token": reset.token})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid or expired token"
        )
    
    # Reset the user's password
    await reset_password(db, user, reset.new_password)
    
    return {"message": "Password updated successfully"}

@router.get("/me", response_model=UserCreate)
async def read_users_me(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    """
    Get details of the logged-in user using the token.
    """
    user_info = await decode_token(token)
    user = await db["users"].find_one({"_id": user_info["sub"]})

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    """
    Log in a user and generate a JWT token.
    """
    # Authenticate the user with email and password
    user = await authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    # Generate an access token for the authenticated user
    access_token = create_access_token({"sub": str(user.id)})
    
    return {"access_token": access_token, "token_type": "bearer"} 