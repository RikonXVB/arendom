import sys
import os

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import SessionLocal
from models.product import Product

def seed_categories():
    db = SessionLocal()
    try:
        # Список категорий для добавления
        categories = [
            {
                "title": "Компьютеры и ноутбуки",
                "subtitle": "Техника для работы и развлечений",
                "price": 1000.0,
                "image_url": "/static/images/comp.png",
                "description": "Аренда компьютеров и ноутбуков",
                "category": "Техника"
            },
            {
                "title": "Рюкзаки",
                "subtitle": "Рюкзаки для путешествий",
                "price": 500.0,
                "image_url": "/static/images/rukzaki.png",
                "description": "Аренда рюкзаков",
                "category": "Аксессуары"
            },
            {
                "title": "Зарядные устройства",
                "subtitle": "Зарядные устройства для техники",
                "price": 200.0,
                "image_url": "/static/images/zaryadka.png",
                "description": "Аренда зарядных устройств",
                "category": "Техника"
            },
            {
                "title": "Лодки",
                "subtitle": "Лодки для отдыха",
                "price": 2000.0,
                "image_url": "/static/images/lodki.png",
                "description": "Аренда лодок",
                "category": "Спорт и отдых"
            }
        ]

        # Добавляем категории в базу данных
        for category in categories:
            product = Product(**category)
            db.add(product)
        
        db.commit()
        print("Categories added successfully!")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_categories() 