from fastapi import APIRouter, Request, Depends, Form, Response, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.auth.auth import get_password_hash, verify_password, create_session, get_user_from_session
import os

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, user=Depends(get_user_from_session)):
    if user:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("auth/register.html", {"request": request, "user": user})

@router.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    error = None
    if db.query(User).filter(User.username == username).first():
        error = "Username already exists"
    elif db.query(User).filter(User.email == email).first():
        error = "Email already exists"

    if error:
        return templates.TemplateResponse(
            "auth/register.html",
            {"request": request, "error": error, "user": None}
        )

    new_user = User(
        username=username,
        email=email,
        password_hash=get_password_hash(password)
    )
    db.add(new_user)
    db.commit()

    return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, user=Depends(get_user_from_session)):
    if user:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("auth/login.html", {"request": request, "user": user})

@router.post("/login")
async def login(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Invalid email or password", "user": None}
        )

    session_token = create_session(user.id)
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="session", value=session_token, httponly=True)
    return response

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("session")
    return response
