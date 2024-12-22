from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.database import get_db
from models.user import User
from schemas.user import UserCreate, UserLogin
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
from sqlalchemy.sql import or_

router = APIRouter(prefix="/api/auth")
templates = Jinja2Templates(directory="templates")

# Настройки безопасности
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register")
async def register(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        data = await request.json()
        print("Полученные данные:", data)
        
        # Создаем объект UserCreate для валидации
        user_data = UserCreate(
            email=data['email'],
            username=data['name'],
            password=data['password']
        )
        
        # Проверяем, не занят ли email или username
        query = select(User).where(
            or_(User.email == user_data.email, User.username == user_data.username)
        )
        result = await db.execute(query)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            if existing_user.email == user_data.email:
                raise HTTPException(
                    status_code=400,
                    detail="Пользователь с таким email уже существует"
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Пользователь с таким логином уже существует"
                )
        
        # Создаем нового пользователя
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        
        db.add(new_user)
        await db.commit()
        
        return JSONResponse(
            content={"message": "Регистрация успешна"},
            status_code=200
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as he:
        raise he
    except Exception as e:
        print("Ошибка при регистрации:", str(e))
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.post("/login")
async def login(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")
        
        if not email or not password:
            raise HTTPException(
                status_code=400,
                detail="Необходимо указать email и пароль"
            )
        
        # Ищем пользователя по email
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=400,
                detail="Неверный email или пароль"
            )
        
        # Создаем токен
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        response = JSONResponse(
            content={"message": "Вход выполнен успешно"},
            status_code=200
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=1800,
            expires=1800,
        )
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as he:
        raise he
    except Exception as e:
        print("Ошибка при входе:", str(e))
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except JWTError:
        return None
    
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    return user

@router.get("/profile")
async def get_profile(request: Request, db: AsyncSession = Depends(get_db)):
    user = await get_current_user(request, db)
    if not user:
        if "application/json" in request.headers.get("accept", ""):
            raise HTTPException(status_code=401, detail="Не авторизован")
        return RedirectResponse(url="/", status_code=303)
    
    if "application/json" in request.headers.get("accept", ""):
        return {"authenticated": True}
    
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": user
    })

@router.post("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response