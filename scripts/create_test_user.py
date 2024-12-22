import sys
import os

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import SessionLocal, engine, Base
from models.user import User
from utils.security import get_password_hash

def create_test_user():
    db = SessionLocal()
    try:
        # Создаем таблицы, если они еще не существуют
        Base.metadata.create_all(bind=engine)
        
        # Проверяем, существует ли уже тестовый пользователь
        test_user = db.query(User).filter(User.email == "test@example.com").first()
        
        if not test_user:
            # Создаем тестового пользователя
            hashed_password = get_password_hash("test123")
            test_user = User(
                email="test@example.com",
                name="Test User",
                hashed_password=hashed_password,
                is_active=True,
                is_admin=True
            )
            db.add(test_user)
            db.commit()
            print("Тестовый пользователь успешно создан")
        else:
            print("Тестовый пользователь уже существует")
            
        # Проверяем создание
        users = db.query(User).all()
        print(f"\nВсего пользователей в базе: {len(users)}")
        for user in users:
            print(f"ID: {user.id}, Email: {user.email}, Name: {user.name}, Active: {user.is_active}")
            
    except Exception as e:
        print(f"Ошибка при создании тестового пользователя: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user() 