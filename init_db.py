import asyncio
from sqlalchemy import text
from config.database import engine, Base
from models.user import User  # Импортируем модель User

async def init_db():
    async with engine.begin() as conn:
        # Удаляем существующую таблицу users
        await conn.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
        
        # Создаем таблицы заново
        await conn.run_sync(Base.metadata.create_all)
        
        print("База данных успешно инициализирована!")

if __name__ == "__main__":
    asyncio.run(init_db()) 