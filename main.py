from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes import auth, products, listings, favorites
from config.database import engine, Base, get_db
from models.product import Product
from models.listing import Listing, ListingImage
from models.cart import Cart, CartItem
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc
from fastapi.responses import HTMLResponse

app = FastAPI()

# Создаем таблицы в базе данных
@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(listings.router)
app.include_router(favorites.router)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse, name="root")
async def read_root(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        # Получаем последние 4 объявления
        query = select(Listing).order_by(desc(Listing.created_at)).limit(4)
        result = await db.execute(query)
        latest_listings = result.scalars().all()
        
        # Получаем изображения для каждого объявления
        listings_with_images = []
        for listing in latest_listings:
            image_query = select(ListingImage).where(
                ListingImage.listing_id == listing.id
            ).limit(1)
            image_result = await db.execute(image_query)
            first_image = image_result.scalar_one_or_none()
            
            listings_with_images.append({
                "listing": listing,
                "image_id": first_image.id if first_image else None
            })
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "latest_listings": listings_with_images
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "latest_listings": []
        })

@app.get("/catalog", name="catalog")
async def catalog(request: Request, db=Depends(get_db)):
    # Получаем все объявления
    query = select(Listing).order_by(Listing.created_at.desc())
    result = await db.execute(query)
    listings = result.scalars().all()
    
    # Получаем первые изображения для каждого объявления
    listings_with_images = []
    for listing in listings:
        image_query = select(ListingImage).where(
            ListingImage.listing_id == listing.id
        ).limit(1)
        image_result = await db.execute(image_query)
        first_image = image_result.scalar_one_or_none()
        
        listings_with_images.append({
            "listing": listing,
            "image_id": first_image.id if first_image else None
        })
    
    return templates.TemplateResponse("catalog.html", {
        "request": request,
        "listings": listings_with_images
    })

@app.get("/product/{product_id}")
async def get_product(request: Request, product_id: int, db=Depends(get_db)):
    query = select(Product).where(Product.id == product_id)
    result = await db.execute(query)
    product = result.scalar_one_or_none()
    
    if not product:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("product.html", {
        "request": request,
        "product": product
    })

# ... rest of your code ... 