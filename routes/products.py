from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.database import get_db
from models.product import Product
from schemas.product import ProductCreate, Product as ProductSchema
from fastapi.templating import Jinja2Templates
from sqlalchemy.future import select

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_model=List[ProductSchema])
async def get_products(db: AsyncSession = Depends(get_db)):
    query = select(Product)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{product_id}")
async def get_product(request: Request, product_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Product).where(Product.id == product_id)
    result = await db.execute(query)
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return templates.TemplateResponse(
        "product.html", 
        {"request": request, "product": product}
    ) 