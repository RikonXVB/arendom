from config.database import engine, Base
from models.listing import Listing, ListingImage
from models.cart import Cart, CartItem
from models.product import Product
from models.favorites import Favorite
from models.user import User
import asyncio

async def recreate_tables():
    async with engine.begin() as conn:
        # Создаем все таблицы
        await conn.run_sync(Base.metadata.create_all)
        print("Таблицы успешно созданы")

if __name__ == "__main__":
    asyncio.run(recreate_tables()) 