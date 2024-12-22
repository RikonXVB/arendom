import sys
import os

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import SessionLocal, engine
from models.product import Product
import models.product

# Создаем таблицы
models.product.Base.metadata.create_all(bind=engine)

# Начальные данные
initial_products = [
    {
        "title": "Зонт",
        "subtitle": "Зонт противоштормовой",
        "price": 1600.0,
        "image_url": "/static/images/zont.png",
        "description": "Надежный противоштормовой зонт для защиты от дождя и ветра",
        "category": "Аксессуары"
    },
    {
        "title": "Сумка шоппер",
        "subtitle": "Сумка шоппер утепленная",
        "price": 3400.0,
        "image_url": "/static/images/sumka.png",
        "description": "Вместительная утепленная сумка для покупок",
        "category": "Сумки"
    },
    {
        "title": "Жилет",
        "subtitle": "Жилет черный утепленный",
        "price": 5600.0,
        "image_url": "/static/images/kurtka.png",
        "description": "Стильный утепленный жилет черного цвета",
        "category": "Одежда"
    },
    {
        "title": "Сумка",
        "subtitle": "Сумка для путешествий",
        "price": 4800.0,
        "image_url": "/static/images/bag.png",
        "description": "Удобная сумка для путешествий и поездок",
        "category": "Сумки"
    },
    {
        "title": "Сумка-шоппер",
        "subtitle": "Сумка-шоппер прозрачная",
        "price": 1400.0,
        "image_url": "/static/images/sumka2.png",
        "description": "Прозрачная сумка для покупок",
        "category": "Сумки"
    },
    {
        "title": "Зонт светоотражающий",
        "subtitle": "Зонт со светоотражающим покрытием",
        "price": 1600.0,
        "image_url": "/static/images/zont.png",
        "description": "Зонт со специальным светоотражающим покрытием",
        "category": "Аксессуары"
    },
    {
        "title": "Панама",
        "subtitle": "Панама двусторонняя",
        "price": 1850.0,
        "image_url": "/static/images/slyapa.png",
        "description": "Стильная двусторонняя панама",
        "category": "Головные уборы"
    },
    {
        "title": "Футболка",
        "subtitle": "Футболка с принтом черная",
        "price": 890.0,
        "image_url": "/static/images/futba.png",
        "description": "Черная футболка с оригинальным принтом",
        "category": "Одежда"
    }
]

def seed_database():
    db = SessionLocal()
    try:
        # Очищаем существующие данные
        db.query(Product).delete()
        
        # Добавляем новые данные
        for product_data in initial_products:
            product = Product(**product_data)
            db.add(product)
        
        db.commit()
        print("База данных успешно заполнена!")
    except Exception as e:
        print(f"Ошибка при заполнении базы данных: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database() 