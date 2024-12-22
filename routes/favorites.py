from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from config.database import get_db
from models.favorites import Favorite
from models.listing import Listing
import uuid
from sqlalchemy.orm import selectinload

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/api/favorites/toggle/{listing_id}")
async def toggle_favorite(
    listing_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    session_id = request.cookies.get("favorites_session")
    response = JSONResponse({"status": "success"})
    
    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(key="favorites_session", value=session_id)

    # Проверяем существование товара в избранном
    favorite_query = select(Favorite).where(
        Favorite.session_id == session_id,
        Favorite.listing_id == listing_id
    )
    result = await db.execute(favorite_query)
    favorite = result.scalar_one_or_none()

    if favorite:
        # Если товар уже в избранном - удаляем
        await db.delete(favorite)
    else:
        # Если товара нет в избранном - добавляем
        favorite = Favorite(
            session_id=session_id,
            listing_id=listing_id
        )
        db.add(favorite)

    await db.commit()
    return response

@router.get("/favorites", response_class=HTMLResponse)
async def view_favorites(request: Request, db: AsyncSession = Depends(get_db)):
    session_id = request.cookies.get("favorites_session")
    favorite_items = []

    if session_id:
        # Получаем избранные товары с их изображениями
        query = select(Listing).join(
            Favorite, 
            Favorite.listing_id == Listing.id
        ).where(
            Favorite.session_id == session_id
        ).options(
            selectinload(Listing.images)  # Загружаем связанные изображения
        )
        result = await db.execute(query)
        favorite_items = result.scalars().all()

    return templates.TemplateResponse("favorites.html", {
        "request": request,
        "favorite_items": favorite_items
    }) 

@router.get("/api/favorites/check/{listing_id}")
async def check_favorite(
    listing_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    session_id = request.cookies.get("favorites_session")
    is_favorite = False

    if session_id:
        favorite_query = select(Favorite).where(
            Favorite.session_id == session_id,
            Favorite.listing_id == listing_id
        )
        result = await db.execute(favorite_query)
        favorite = result.scalar_one_or_none()
        is_favorite = favorite is not None

    return JSONResponse({"is_favorite": is_favorite}) 