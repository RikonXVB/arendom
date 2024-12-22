from fastapi import APIRouter, Request, Depends, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from models.listing import Listing, ListingImage
from models.cart import Cart, CartItem
import os
import aiofiles
import uuid
from typing import List, Optional
from sqlalchemy import desc

router = APIRouter()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "static/uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.get("/create-listing", response_class=HTMLResponse)
async def get_create_listing_page(request: Request):
    return templates.TemplateResponse("create_listing.html", {"request": request})

@router.post("/create-listing")
async def create_listing(
    request: Request,
    title: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    location: str = Form(...),
    contact: str = Form(...),
    images: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    # Создаем новое объявление
    listing = Listing(
        title=title,
        category=category,
        description=description,
        price=price,
        location=location,
        contact=contact
    )
    db.add(listing)
    await db.flush()  # Получаем id объявления

    # Сохраняем изображения
    for image in images[:5]:  # Ограничиваем количество изображений до 5
        content = await image.read()
        
        # Создаем запись в базе данных
        db_image = ListingImage(
            listing_id=listing.id,
            image_data=content,
            content_type=image.content_type
        )
        db.add(db_image)

        # Если это первое изображение, сохраняем его как основное
        if listing.image_url is None:
            listing.image_url = f"/listing/{listing.id}/image/{db_image.id}"

    await db.commit()
    
    # Перенаправляем на страницу созданного объявления
    return RedirectResponse(url=f"/listing/{listing.id}", status_code=303)

@router.get("/listing/{listing_id}", response_class=HTMLResponse)
async def get_listing(request: Request, listing_id: int, db: AsyncSession = Depends(get_db)):
    # Получаем объявление
    query = select(Listing).where(Listing.id == listing_id)
    result = await db.execute(query)
    listing = result.scalar_one_or_none()
    
    if not listing:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    
    # Получаем все изображения объявления
    images_query = select(ListingImage).where(ListingImage.listing_id == listing_id)
    images_result = await db.execute(images_query)
    images = images_result.scalars().all()
    
    return templates.TemplateResponse("listing_detail.html", {
        "request": request,
        "listing": listing,
        "images": images
    })

@router.get("/listing/{listing_id}/image/{image_id}")
async def get_listing_image(
    listing_id: int,
    image_id: int,
    db: AsyncSession = Depends(get_db)
):
    query = select(ListingImage).where(
        ListingImage.listing_id == listing_id,
        ListingImage.id == image_id
    )
    result = await db.execute(query)
    image = result.scalar_one_or_none()
    
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return Response(
        content=image.image_data,
        media_type=image.content_type
    )

@router.post("/add-to-cart/{listing_id}")
async def add_to_cart(
    listing_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    # Получаем или создаем session_id из cookies
    session_id = request.cookies.get("cart_session")
    response = RedirectResponse(url="/cart", status_code=303)
    
    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(key="cart_session", value=session_id)

    # Получаем или создаем корзину для сессии
    cart_query = select(Cart).where(Cart.session_id == session_id)
    result = await db.execute(cart_query)
    cart = result.scalar_one_or_none()

    if not cart:
        cart = Cart(session_id=session_id)
        db.add(cart)
        await db.flush()

    # Проверяем, есть ли уже такой товар в корзине
    cart_item_query = select(CartItem).where(
        CartItem.cart_id == cart.id,
        CartItem.listing_id == listing_id
    )
    result = await db.execute(cart_item_query)
    cart_item = result.scalar_one_or_none()

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            listing_id=listing_id
        )
        db.add(cart_item)

    await db.commit()
    return response

@router.get("/cart", response_class=HTMLResponse)
async def view_cart(request: Request, db: AsyncSession = Depends(get_db)):
    session_id = request.cookies.get("cart_session")
    cart_items = []
    total_price = 0

    if session_id:
        # Получаем корзину пользователя
        cart_query = select(Cart).where(Cart.session_id == session_id)
        result = await db.execute(cart_query)
        cart = result.scalar_one_or_none()

        if cart:
            # Получаем все товары в корзине
            items_query = select(CartItem).where(CartItem.cart_id == cart.id)
            result = await db.execute(items_query)
            items = result.scalars().all()

            # Получаем информацию о каждом объявлении
            for item in items:
                listing_query = select(Listing).where(Listing.id == item.listing_id)
                listing_result = await db.execute(listing_query)
                listing = listing_result.scalar_one_or_none()

                if listing:
                    # Получаем первое изображение для объявления
                    image_query = select(ListingImage).where(
                        ListingImage.listing_id == listing.id
                    ).limit(1)
                    image_result = await db.execute(image_query)
                    first_image = image_result.scalar_one_or_none()

                    cart_items.append({
                        "item": item,
                        "listing": listing,
                        "image_id": first_image.id if first_image else None
                    })
                    total_price += listing.price * item.quantity

    return templates.TemplateResponse("cart.html", {
        "request": request,
        "cart_items": cart_items,
        "total_price": total_price
    })

@router.post("/cart/remove/{item_id}")
async def remove_from_cart(
    item_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    session_id = request.cookies.get("cart_session")
    if session_id:
        # Получаем корзину
        cart_query = select(Cart).where(Cart.session_id == session_id)
        result = await db.execute(cart_query)
        cart = result.scalar_one_or_none()

        if cart:
            # Проверяем, принадлежит ли товар этой корзине
            query = select(CartItem).where(
                CartItem.id == item_id,
                CartItem.cart_id == cart.id
            )
            result = await db.execute(query)
            cart_item = result.scalar_one_or_none()

            if cart_item:
                await db.delete(cart_item)
                await db.commit()

    return RedirectResponse(url="/cart", status_code=303)

@router.get("/catalog", response_class=HTMLResponse)
async def get_catalog(request: Request, db: AsyncSession = Depends(get_db)):
    # Получаем все объявления
    query = select(Listing).order_by(desc(Listing.created_at))
    result = await db.execute(query)
    listings = result.scalars().all()

    # Получаем изображения для каждого объявления
    listings_with_images = []
    for listing in listings:
        # Получаем первое изображение для объявления
        image_query = select(ListingImage).where(
            ListingImage.listing_id == listing.id
        ).limit(1)
        image_result = await db.execute(image_query)
        first_image = image_result.scalar_one_or_none()

        if first_image:
            listing.image_url = f"/listing/{listing.id}/image/{first_image.id}"
        
        listings_with_images.append(listing)

    return templates.TemplateResponse("catalog.html", {
        "request": request,
        "listings": listings_with_images
    })