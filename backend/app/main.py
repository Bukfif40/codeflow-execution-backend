import os
from fastapi import FastAPI, Query, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from app.services.search_providers import get_provider
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
except ImportError:
    pass  # python-dotenv not installed; .env loading skipped

"""
Main FastAPI application for the backend.
"""

# --- User and Auth Setup ---
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# In-memory user store for demo purposes
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("adminpass"),
        "role": "premium"
    },
    "user": {
        "username": "user",
        "hashed_password": pwd_context.hash("userpass"),
        "role": "free"
    },
}


class User(BaseModel):
    username: str
    role: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Utility functions

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username: str) -> Optional[UserInDB]:
    user = fake_users_db.get(username)
    if user:
        return UserInDB(**user)
    return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user

def require_premium(user: User = Depends(get_current_user)):
    if user.role != "premium":
        raise HTTPException(status_code=403, detail="Premium access required for this provider.")

# --- FastAPI App and Endpoints ---
app = FastAPI(title="Codeflow Execution Backend")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Only allow your local frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to your FastAPI backend!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/register", summary="Register a new user")
def register(form: OAuth2PasswordRequestForm = Depends()):
    if form.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    fake_users_db[form.username] = {
        "username": form.username,
        "hashed_password": get_password_hash(form.password),
        "role": "free"
    }
    return {"msg": "User registered successfully"}

@app.post("/login", response_model=Token, summary="User login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form.username, form.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=User, summary="Get current user profile")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/search", summary="Perform a web search")
def search(
    query: str = Query(..., description="Search query"),
    num_results: int = Query(10, description="Number of results"),
    provider: str = Query("serpapi", description="Search provider (serpapi, bing, ddg)"),
    current_user: Optional[User] = Depends(get_current_user)
):
    # Restrict premium providers
    if provider.lower() == "serpapi":
        require_premium(current_user)
    ProviderClass = get_provider(provider)
    results = ProviderClass.search(query, num_results)
    return {"results": results}
