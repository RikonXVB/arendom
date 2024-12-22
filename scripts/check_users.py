import sys
import os

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import SessionLocal
from models.user import User

def check_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"Total users: {len(users)}")
        for user in users:
            print(f"User ID: {user.id}, Email: {user.email}, Name: {user.name}")
    finally:
        db.close()

if __name__ == "__main__":
    check_users() 