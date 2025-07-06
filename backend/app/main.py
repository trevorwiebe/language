# app/main.py
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uuid
from datetime import datetime, timedelta

app = FastAPI(title="Language Learning API")

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cookie settings
COOKIE_NAME = "user_session_id"
COOKIE_MAX_AGE = 30 * 24 * 60 * 60  # 30 days

@app.middleware("http")
async def add_user_session(request: Request, call_next):
    """Middleware to handle user session cookies"""
    user_id = request.cookies.get(COOKIE_NAME)
    
    # Create new user ID if not exists
    if not user_id:
        user_id = str(uuid.uuid4())
        request.state.new_user = True
    else:
        request.state.new_user = False
    
    request.state.user_id = user_id
    
    response = await call_next(request)
    
    # Set cookie if new user
    if request.state.new_user and isinstance(response, Response):
        response.set_cookie(
            key=COOKIE_NAME,
            value=user_id,
            max_age=COOKIE_MAX_AGE,
            httponly=True,
            samesite="lax"
        )
    
    return response

# Include routers
from app.api import content, uploads, users
app.include_router(content.router, prefix="/api/content")
app.include_router(uploads.router, prefix="/api/uploads")
app.include_router(users.router, prefix="/api/users")

@app.get("/api/session")
async def get_session(request: Request):
    """Get current user session info"""
    return {
        "user_id": request.state.user_id,
        "is_new": request.state.new_user
    }